import os
import sys
from datetime import date
from dotenv import load_dotenv
from github_api import GitHubClient


def main() -> None:
    load_dotenv()

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/add_daily_comment.py 'comment text'")

    comment = sys.argv[1]
    target_date = os.getenv("TARGET_DATE") or date.today().isoformat()
    title = f"daily: {target_date}"

    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    client = GitHubClient(owner=owner, repo=repo, token=token)
    issue = client.find_issue_by_title(title, labels="daily")
    if not issue:
        issue = client.create_issue(
            title=title,
            body=f"# {target_date}\n\n今日のメモをコメントで追加してください。",
            labels=["daily"],
        )

    client.create_comment(issue["number"], comment)
    print(f"Added comment to #{issue['number']} {title}")


if __name__ == "__main__":
    main()
