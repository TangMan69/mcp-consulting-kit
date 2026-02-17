import os
import httpx

GITHUB_API_URL = "https://api.github.com"

class GitHubClient:
    def __init__(self) -> None:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise RuntimeError("GITHUB_TOKEN not set")
        self.token = token
        self.client = httpx.Client(timeout=10.0)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

    def create_issue(self, owner: str, repo: str, title: str, body: str | None = None):
        resp = self.client.post(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues",
            headers=self._headers(),
            json={"title": title, "body": body or ""},
        )
        resp.raise_for_status()
        return resp.json()

    def search_code(self, query: str):
        resp = self.client.get(
            f"{GITHUB_API_URL}/search/code",
            headers=self._headers(),
            params={"q": query},
        )
        resp.raise_for_status()
        return resp.json()

    def list_pull_requests(self, owner: str, repo: str, state: str = "open"):
        resp = self.client.get(
            f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls",
            headers=self._headers(),
            params={"state": state},
        )
        resp.raise_for_status()
        return resp.json()
