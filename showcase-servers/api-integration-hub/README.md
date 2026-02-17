# API Integration Hub MCP

Control Slack, GitHub, and Stripe from Claude Desktop.

## Features

- Slack: send messages, list channels, search
- GitHub: create issues, list PRs, search code
- Stripe: lookup customers, charges, subscriptions

## Env vars

- `SLACK_BOT_TOKEN`
- `GITHUB_TOKEN`
- `STRIPE_API_KEY`
- `PORT` (default 8102)

## Run

```bash
docker build -t api-hub-showcase .
docker run --env-file .env -p 8102:8102 api-hub-showcase
