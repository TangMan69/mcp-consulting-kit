from types import SimpleNamespace
import json

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

import security


def build_request(path: str = "/nl-query", ip: str = "127.0.0.1"):
    app = SimpleNamespace(state=SimpleNamespace(rate_limit_store={}))
    return SimpleNamespace(
        app=app,
        client=SimpleNamespace(host=ip),
        url=SimpleNamespace(path=path),
    )


def test_get_allowed_origins_from_env(monkeypatch):
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://a.com, https://b.com ")
    assert security.get_allowed_origins() == ["https://a.com", "https://b.com"]


def test_verify_api_key_rejects_missing_config(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(HTTPException) as exc:
        security.verify_api_key("secret")
    assert exc.value.status_code == 500


def test_verify_api_key_rejects_invalid_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "expected")
    with pytest.raises(HTTPException) as exc:
        security.verify_api_key("wrong")
    assert exc.value.status_code == 401


def test_verify_api_key_accepts_valid_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "expected")
    security.verify_api_key("expected")


def test_enforce_rate_limit_blocks_after_limit(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "1")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")

    request = build_request()
    security.enforce_rate_limit(request)

    with pytest.raises(HTTPException) as exc:
        security.enforce_rate_limit(request)
    assert exc.value.status_code == 429


def test_enforce_rate_limit_resets_after_window(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "1")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "1")

    request = build_request()
    security.enforce_rate_limit(request)

    key = "127.0.0.1:/nl-query"
    request.app.state.rate_limit_store[key]["reset_at"] = 0

    security.enforce_rate_limit(request)


def test_enforce_rate_limit_increments_within_window(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_REQUESTS", "3")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SECONDS", "60")

    request = build_request()
    security.enforce_rate_limit(request)
    security.enforce_rate_limit(request)

    key = "127.0.0.1:/nl-query"
    assert request.app.state.rate_limit_store[key]["count"] == 2


def test_observability_adds_request_id_header_and_logs(monkeypatch, caplog):
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.setenv("LOG_HEALTH_REQUESTS", "false")
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    app = FastAPI(title="Test Service")
    security.configure_observability(app)

    @app.get("/ping")
    def ping():
        return {"ok": True}

    client = TestClient(app)

    with caplog.at_level("INFO", logger=security.LOGGER_NAME):
        response = client.get("/ping", headers={security.REQUEST_ID_HEADER: "req-123"})

    assert response.status_code == 200
    assert response.headers[security.REQUEST_ID_HEADER] == "req-123"
    payload = json.loads(caplog.records[-1].message)
    assert payload["event"] == "http_request"
    assert payload["request_id"] == "req-123"
    assert payload["path"] == "/ping"
    assert payload["status_code"] == 200
    assert payload["service"] == "Test Service"


def test_observability_skips_health_logs_by_default(monkeypatch, caplog):
    monkeypatch.setenv("LOG_HEALTH_REQUESTS", "false")

    app = FastAPI(title="Health Test")
    security.configure_observability(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app)
    caplog.clear()
    with caplog.at_level("INFO", logger=security.LOGGER_NAME):
        response = client.get("/health")

    assert response.status_code == 200
    assert len(caplog.records) == 0


def test_observability_logs_health_when_enabled(monkeypatch, caplog):
    monkeypatch.setenv("LOG_HEALTH_REQUESTS", "true")

    app = FastAPI(title="Health Logging")
    security.configure_observability(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    client = TestClient(app)

    with caplog.at_level("INFO", logger=security.LOGGER_NAME):
        response = client.get("/health")

    assert response.status_code == 200
    payload = json.loads(caplog.records[-1].message)
    assert payload["path"] == "/health"
