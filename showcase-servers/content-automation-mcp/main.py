import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mcp_tools import (
    ScrapeRequest,
    RSSRequest,
    scrape_article,
    scrape_links,
    scrape_tables,
    parse_rss,
)

PORT = int(os.getenv("PORT", "8103"))

app = FastAPI(title="Content Automation MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scrape/article")
def scrape_article_endpoint(req: ScrapeRequest):
    try:
        return scrape_article(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/scrape/links")
def scrape_links_endpoint(req: ScrapeRequest):
    try:
        return scrape_links(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/scrape/tables")
def scrape_tables_endpoint(req: ScrapeRequest):
    try:
        return scrape_tables(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rss/parse")
def rss_parse_endpoint(req: RSSRequest):
    try:
        return parse_rss(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
