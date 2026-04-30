import os
import json
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from github_api import GitHubClient

load_dotenv()

JST = timezone(timedelta(hours=9))

SYSTEM_PROMPT = """
あなたは個人メモを分類するルーターです。
入力メモを calendar / task / knowledge のどれかに分類してください。

必ずJSONだけを返してください。

形式:
{
  "type": "calendar" | "task" | "knowledge",
  "title": "...",
  "description": "...",
  "start": "YYYY-MM-DDTHH:MM:SS+09:00",
  "end": "YYYY-MM-DDTHH:MM:SS+09:00",
  "due": "YYYY-MM-DDT00:00:00.000Z",
  "reason": "..."
}

ルール:
- 日時が明確な予定は calendar
- 締切ややることは task
- 学び、考え、調査メモ、アイデアは knowledge
- calendarの場合、endが不明ならstartの1時間後
- taskの場合、期限が不明ならdueは空文字
- knowledgeの場合、start/end/dueは空文字
"""


def call_openai(text: str) -> dict:
    now = datetime.now(JST).isoformat()

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT + f"\n現在日時: {now}"},
            {"role": "user", "content": text},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    res.raise_for_status()
    return json.loads(res.json()["choices"][0]["message"]["content"])


def send_to_gas(data: dict) -> None:
    data["secret"] = os.environ["GAS_SECRET"]

    res = requests.post(
        os.environ["GAS_WEBHOOK_URL"],
        json=data,
        timeout=30,
    )
    res.raise_for_status()
    print(res.text)


def main():
    owner = os.getenv("GITHUB_OWNER") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[0]
    repo = os.getenv("GITHUB_REPO") or os.getenv("GITHUB_REPOSITORY", "/").split("/")[-1]
    token = os.getenv("GITHUB_TOKEN") or os.getenv("PERSONAL_AI_KB_TOKEN")

    client = GitHubClient(owner, repo, token)

    issues = client.list_issues(labels="inbox")

    for issue in issues:
        number = issue["number"]
        title = issue.get("title", "")
        body = issue.get("body", "")
        text = f"{title}\n\n{body}"

        routed = call_openai(text)

        if routed["type"] in ["calendar", "task"]:
            send_to_gas(routed)
            client.create_comment(
                number,
                "AI routed to Google:\n\n```json\n"
                + json.dumps(routed, ensure_ascii=False, indent=2)
                + "\n```"
            )

        else:
            client.create_comment(
                number,
                "AI routed to knowledge:\n\n```json\n"
                + json.dumps(routed, ensure_ascii=False, indent=2)
                + "\n```"
            )


if __name__ == "__main__":
    main()