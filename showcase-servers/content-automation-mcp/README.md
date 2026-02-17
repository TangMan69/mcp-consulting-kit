# Content Automation MCP

Web scraping, table extraction, and RSS parsing for Claude Desktop.

## Features

- Extract article text from a URL
- Extract all links
- Extract HTML tables
- Parse RSS feeds

## Env vars

- `PORT` (default 8103)

## Run

```bash
docker build -t content-mcp-showcase .
docker run --env-file .env -p 8103:8103 content-mcp-showcase
