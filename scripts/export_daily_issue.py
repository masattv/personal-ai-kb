import os
from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv
from github_api import GitHubClient


def sanitize_comment(body: str) -> str:
    body = body.strip()
    if not body:
        return ""
    return body


def main() -> None:
    load_dotenv()

    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    target_date = os.getenv("TARGET_DATE") or date.today().isoformat()
    title = f"daily: {target_date}"

    client = GitHubClient(owner=owner, repo=repo, token=token)
    issue = client.find_issue_by_title(title, labels="daily")

    if not issue:
        print(f"No daily issue found: {title}")
        return

    comments = client.list_comments(issue["number"])

    dt = datetime.fromisoformat(target_date)
    out_dir = Path("blog") / f"{dt.year:04d}" / f"{dt.month:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{target_date}.md"

    lines = []
    lines.append(f"# {target_date}")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append(f"- Issue: #{issue['number']}")
    lines.append(f"- URL: {issue.get('html_url', '')}")
    lines.append("")
    lines.append("## Logs")
    lines.append("")

    if not comments:
        lines.append("_No comments yet._")
    else:
        for comment in comments:
            created_at = comment.get("created_at", "")
            user = comment.get("user", {}).get("login", "unknown")
            body = sanitize_comment(comment.get("body", ""))
            if not body:
                continue
            lines.append(f"### {created_at} by {user}")
            lines.append("")
            lines.append(body)
            lines.append("")

    lines.append("## AI Summary")
    lines.append("")
    lines.append("> TODO: Run AI organization workflow.")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Exported: {out_path}")


if __name__ == "__main__":
    main()
