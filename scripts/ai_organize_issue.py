"""
knowledge-candidateラベル付きIssueをAIでMarkdown化するための拡張口です。

現時点では安全のため、AI API呼び出しは未実装のスタブにしています。
OpenAI / Claude / Gemini のどれを使うか決めたあと、このファイルに実装します。
"""

import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv
from github_api import GitHubClient


def build_markdown_from_issue(issue: dict) -> str:
    title = issue.get("title", "Untitled")
    body = issue.get("body", "")
    url = issue.get("html_url", "")
    today = date.today().isoformat()

    return f"""---
title: "{title}"
category: "ideas"
tags:
  - knowledge-candidate
created: "{today}"
source: "{url}"
---

# 概要

TODO: AIで要約する。

# 元メモ

{body}

# 次にやること

- [ ] 内容を整理する
- [ ] category/tagsを見直す
- [ ] 関連ノートをリンクする
"""


def main() -> None:
    load_dotenv()

    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    client = GitHubClient(owner=owner, repo=repo, token=token)
    issues = client.list_issues(labels="knowledge-candidate")

    out_dir = Path("knowledge/ideas")
    out_dir.mkdir(parents=True, exist_ok=True)

    for issue in issues:
        number = issue["number"]
        slug = f"issue-{number}"
        out_path = out_dir / f"{slug}.md"
        if out_path.exists():
            print(f"Skip existing: {out_path}")
            continue
        out_path.write_text(build_markdown_from_issue(issue), encoding="utf-8")
        print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
