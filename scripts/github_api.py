import os
import requests
from typing import Any, Dict, List, Optional

GITHUB_API = "https://api.github.com"


class GitHubClient:
    def __init__(self, owner: str, repo: str, token: str):
        if not owner or not repo or not token:
            raise ValueError("owner, repo, token are required")
        self.owner = owner
        self.repo = repo
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    @property
    def base(self) -> str:
        return f"{GITHUB_API}/repos/{self.owner}/{self.repo}"

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self.base}{path}"
        response = self.session.request(method, url, timeout=30, **kwargs)
        if response.status_code >= 400:
            raise RuntimeError(f"GitHub API error {response.status_code}: {response.text}")
        if response.text:
            return response.json()
        return None

    def list_issues(self, labels: Optional[str] = None, state: str = "open") -> List[Dict[str, Any]]:
        params = {"state": state, "per_page": 100}
        if labels:
            params["labels"] = labels
        return self.request("GET", "/issues", params=params)

    def create_issue(self, title: str, body: str = "", labels: Optional[List[str]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        return self.request("POST", "/issues", json=payload)

    def create_comment(self, issue_number: int, body: str) -> Dict[str, Any]:
        return self.request("POST", f"/issues/{issue_number}/comments", json={"body": body})

    def list_comments(self, issue_number: int) -> List[Dict[str, Any]]:
        return self.request("GET", f"/issues/{issue_number}/comments", params={"per_page": 100})

    def find_issue_by_title(self, title: str, labels: Optional[str] = None) -> Optional[Dict[str, Any]]:
        for issue in self.list_issues(labels=labels):
            if issue.get("title") == title:
                return issue
        return None
