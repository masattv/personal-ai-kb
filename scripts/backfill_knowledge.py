"""
backfill_knowledge.py
=====================
Rescue existing issues that have the ``routed-knowledge`` label but were never
converted to a Markdown file in ``knowledge/``.

Run manually via workflow_dispatch or on the command line:

    python scripts/backfill_knowledge.py
"""

import base64
import json
import os
import re
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from github_api import GitHubClient

load_dotenv()

JST = timezone(timedelta(hours=9))


# ---------------------------------------------------------------------------
# Helpers (shared logic with route_issue.py)
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a URL-safe slug (ASCII alphanumeric + hyphens)."""
    safe = "".join(c if c.isalnum() else "-" for c in text.lower())
    safe = "-".join(part for part in safe.split("-") if part)
    return safe[:80] or "untitled"


def create_knowledge_markdown(issue: dict, routed: dict) -> str:
    """Generate a Markdown document with frontmatter for a knowledge item."""
    created_at = issue.get("created_at", "")
    if created_at:
        # Convert ISO 8601 UTC to JST display string
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        dt_jst = dt.astimezone(JST)
        created_str = dt_jst.strftime("%Y-%m-%d %H:%M:%S %z")
    else:
        created_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S %z")

    title = routed.get("title") or issue.get("title", "")
    description = routed.get("description", "")
    reason = routed.get("reason", "")
    issue_number = issue["number"]
    issue_url = issue.get("html_url", "")

    return f"""---
title: "{title}"
type: knowledge
source: github_issue
issue_number: {issue_number}
created_at: "{created_str}"
tags:
  - knowledge
---

# {title}

## 内容

{description}

## ルーティング理由

{reason}

## 元Issue

- #{issue_number}
- {issue_url}
"""


def create_repo_file(client: GitHubClient, path: str, content: str, message: str) -> None:
    """Create a file in the repository via the GitHub Contents API."""
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    client.request(
        "PUT",
        f"/contents/{path}",
        json={
            "message": message,
            "content": encoded,
        },
    )


def repo_file_exists(client: GitHubClient, path: str) -> bool:
    """Return True if the file already exists in the repository."""
    try:
        client.request("GET", f"/contents/{path}")
        return True
    except RuntimeError:
        return False


def set_issue_labels(client: GitHubClient, issue_number: int, labels: list[str]) -> None:
    client.request(
        "PATCH",
        f"/issues/{issue_number}",
        json={"labels": labels},
    )


# ---------------------------------------------------------------------------
# Extract routing result from issue comments
# ---------------------------------------------------------------------------

_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def extract_routing_result(comments: list[dict]) -> dict | None:
    """Find the first ``AI routing result`` comment and parse its JSON."""
    for comment in comments:
        body = comment.get("body", "")
        if "AI routing result" not in body:
            continue
        m = _JSON_BLOCK_RE.search(body)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    client = GitHubClient(owner, repo, token)

    issues = client.list_issues(labels="routed-knowledge")

    if not issues:
        print("No routed-knowledge issues found.")
        return

    created = 0
    skipped = 0

    for issue in issues:
        number = issue["number"]
        labels = [label["name"] for label in issue.get("labels", [])]

        # Skip if already backfilled
        if "backfilled-knowledge" in labels:
            print(f"Skip issue #{number}: already backfilled")
            skipped += 1
            continue

        # Extract routing result from comments
        comments = client.list_comments(number)
        routed = extract_routing_result(comments)

        if not routed:
            print(f"Skip issue #{number}: routing result not found in comments")
            skipped += 1
            continue

        # Determine file path
        title = routed.get("title") or issue.get("title", "")
        slug = slugify(title)
        date_prefix = issue.get("created_at", "")[:10] or datetime.now(JST).strftime("%Y-%m-%d")
        path = f"knowledge/{date_prefix}-{slug}.md"

        # Skip if file already exists
        if repo_file_exists(client, path):
            print(f"Skip issue #{number}: file already exists at {path}")
            skipped += 1
            continue

        # Create knowledge Markdown
        md = create_knowledge_markdown(issue, routed)

        create_repo_file(
            client,
            path,
            md,
            f"Backfill knowledge from issue #{number}",
        )

        # Add backfilled label (keep existing labels)
        set_issue_labels(client, number, labels + ["backfilled-knowledge"])

        print(f"Created knowledge file: {path} (issue #{number})")
        created += 1

    print(f"\nBackfill complete: {created} created, {skipped} skipped")


if __name__ == "__main__":
    main()
