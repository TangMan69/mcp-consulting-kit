# Content Automation MCP

Web scraping, table extraction, and RSS parsing for Claude Desktop.

## Features

- Extract article text from a URL
- Extract all links
- Extract HTML tables
- Parse RSS feeds

## Env vars

- `API_KEY` (required for all POST endpoints via `X-API-Key` header)
- `ALLOWED_ORIGINS` (comma-separated, default: `http://localhost,http://127.0.0.1`)
- `RATE_LIMIT_REQUESTS` (default: `60`)
- `RATE_LIMIT_WINDOW_SECONDS` (default: `60`)
- `LOG_LEVEL` (default: `INFO`)
- `LOG_HEALTH_REQUESTS` (`true`/`false`, default: `false`)
- `SERVICE_NAME` (optional service label in logs)
- `PORT` (default 8103)

All responses include `X-Request-ID` for request tracing.

## Run

```bash
docker build -t content-mcp-showcase .
docker run --env-file .env -p 8103:8103 content-mcp-showcase
