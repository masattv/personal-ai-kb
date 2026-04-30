# 運用方法

## 基本ルール

```text
Issue = 雑に入れる
daily issue comment = 今日のログ
blog/ = 日次Markdown
knowledge/ = 整理済みナレッジ
```

## daily issue

毎日1つ、以下のようなIssueを作ります。

```text
daily: 2026-04-28
```

ラベル：

```text
daily
```

そのIssueにコメントとして、スマホやPCからメモを追加します。

例：

```md
仕事でMTGの伝え方に悩んだ。要点を先に言う練習が必要。
```

## Markdown出力

GitHub Actionsの `Export Daily Issue` を実行すると、daily issueのコメントを日次Markdownへ変換します。

出力先：

```text
blog/YYYY/MM/YYYY-MM-DD.md
```

## ナレッジ化

Issueに以下のラベルを付けます。

```text
knowledge-candidate
```

将来的に `scripts/ai_organize_issue.py` がこのIssueを読み、以下にMarkdown化します。

```text
knowledge/<category>/<slug>.md
```

## 週次レビュー

週末に `blog/` と `knowledge/` をClaude Codeに読ませて、以下を作る想定です。

```text
tasks/reviews/weekly-YYYY-WW.md
```
