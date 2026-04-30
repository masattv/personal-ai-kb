import os
from datetime import date
from dotenv import load_dotenv
from github_api import GitHubClient


def main() -> None:
    load_dotenv()

    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    today = os.getenv("TARGET_DATE") or date.today().isoformat()
    title = f"daily: {today}"

    client = GitHubClient(owner=owner, repo=repo, token=token)
    existing = client.find_issue_by_title(title, labels="daily")
    if existing:
        print(f"Daily issue already exists: #{existing['number']} {title}")
        return

    body = f"""# {today}

今日のメモをコメントで追加してください。

## 使い方

- スマホからコメント追加
- 気づき、作業ログ、タスク、アイデアを雑に書く
- 後でGitHub ActionsがMarkdown化する
"""

    issue = client.create_issue(title=title, body=body, labels=["daily"])
    print(f"Created daily issue: #{issue['number']} {title}")


if __name__ == "__main__":
    main()
