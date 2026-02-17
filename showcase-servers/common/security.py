import os
import time
import json
import uuid
import logging

from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware

LOGGER_NAME = "mcp.observability"
REQUEST_ID_HEADER = "X-Request-ID"


def get_allowed_origins() -> list[str]:
    raw = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def get_rate_limit() -> tuple[int, int]:
    requests = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
    window_seconds = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    return requests, window_seconds


def get_log_level() -> str:
    return os.getenv("LOG_LEVEL", "INFO").upper()


def should_log_health_requests() -> bool:
    return os.getenv("LOG_HEALTH_REQUESTS", "false").strip().lower() == "true"


def _resolve_service_name(app: FastAPI) -> str:
    return os.getenv("SERVICE_NAME", app.title)


def _get_or_create_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(get_log_level())
    logger.propagate = True
    return logger


def _build_log_payload(
    request: Request,
    request_id: str,
    status_code: int,
    duration_ms: float,
    service_name: str,
) -> dict:
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    return {
        "event": "http_request",
        "service": service_name,
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        "client_ip": client_ip,
        "user_agent": user_agent,
    }


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_allowed_origins(),
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_observability(app: FastAPI) -> None:
    logger = _get_or_create_logger()
    service_name = _resolve_service_name(app)

    @app.middleware("http")
    async def observability_middleware(request: Request, call_next):
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()
        status_code = 500
        response: Response | None = None

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers[REQUEST_ID_HEADER] = request_id
            return response
        finally:
            if request.url.path != "/health" or should_log_health_requests():
                duration_ms = (time.perf_counter() - start) * 1000
                payload = _build_log_payload(
                    request=request,
                    request_id=request_id,
                    status_code=status_code,
                    duration_ms=duration_ms,
                    service_name=service_name,
                )
                logger.info(json.dumps(payload, separators=(",", ":")))


def initialize_rate_limit_store(app: FastAPI) -> None:
    app.state.rate_limit_store = {}


def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    expected_api_key = os.getenv("API_KEY")
    if not expected_api_key:
        raise HTTPException(status_code=500, detail="API_KEY is not configured")
    if x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


def enforce_rate_limit(request: Request) -> None:
    limit, window = get_rate_limit()
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{request.url.path}"
    now = time.time()

    bucket = request.app.state.rate_limit_store.get(key)
    if not bucket or now >= bucket["reset_at"]:
        request.app.state.rate_limit_store[key] = {"count": 1, "reset_at": now + window}
        return

    if bucket["count"] >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    bucket["count"] += 1
