# MCP Consulting Kit

Everything you need to launch an AI automation consulting business in 30 days.

This repo contains:

- **Three production-ready MCP servers** (FastAPI + Docker)
  - Business Intelligence MCP (databases)
  - API Integration Hub (Slack, GitHub, Stripe)
  - Content Automation MCP (scraping, monitoring)
- **Consulting materials**
  - Landing page
  - Outreach strategy & templates
  - Pitch deck outline
  - Quick-start execution plan
- **Project scaffolding**
  - Roadmap
  - Changelog
  - Case studies

---

## Architecture

```text
Claude Desktop
    │
    │  (MCP)
    ▼
FastAPI MCP servers (Docker)
    │
    ├── Databases (PostgreSQL / MySQL / SQLite)
    ├── APIs (Slack / GitHub / Stripe / custom)
    └── Web / RSS / scraping targets
