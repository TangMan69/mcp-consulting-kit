import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from mcp_tools import handle_nl_query

PORT = int(os.getenv("PORT", "8101"))

app = FastAPI(title="Business Intelligence MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NLQueryRequest(BaseModel):
    query: str
    schema_hint: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/nl-query")
def nl_query(req: NLQueryRequest):
    try:
        result = handle_nl_query(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
