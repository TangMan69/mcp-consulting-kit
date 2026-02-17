
---

## 🧭 ROADMAP.md

```markdown
# Roadmap

## v0.1.0 – Initial Reconstruction

- [x] Rebuild three MCP servers with FastAPI
- [x] Dockerize each server
- [x] Restore consulting materials
- [x] Add unified repo README
- [x] Add Quick Start, Roadmap, Changelog, Case Studies

## v0.2.0 – Unified Server & Local AI

- [ ] Optional unified FastAPI app on port 8100
- [ ] Abstract LLM provider behind interface
- [ ] Add `LLM_PROVIDER` env switch (`claude` / `local`)
- [ ] Implement local provider stub

## v0.3.0 – Production Hardening

- [ ] Add auth for API endpoints
- [ ] Add logging & metrics
- [ ] Add tests for each server
- [ ] Add CI workflow
- [ ] Track detailed security hardening backlog in GitHub Issues (SEC-01 to SEC-10)

## v1.0.0 – Public Release

- [ ] Polish docs
- [ ] Add example configs
- [ ] Tag v1.0.0
