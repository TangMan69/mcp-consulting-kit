import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from mcp_tools import (
    SlackMessageRequest,
    GitHubIssueRequest,
    StripeCustomerLookupRequest,
    send_slack_message,
    create_issue_and_optionally_notify,
    lookup_stripe_customer,
)

PORT = int(os.getenv("PORT", "8102"))

app = FastAPI(title="API Integration Hub MCP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/slack/send")
def slack_send(req: SlackMessageRequest):
    try:
        return send_slack_message(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/github/create-issue")
def github_create_issue(req: GitHubIssueRequest):
    try:
        return create_issue_and_optionally_notify(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stripe/customer")
def stripe_customer(req: StripeCustomerLookupRequest):
    try:
        return lookup_stripe_customer(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
