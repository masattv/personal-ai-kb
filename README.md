<<<<<<< HEAD
# personal-ai-kb
=======
# personal-ai-kb

GitHubを中心にした個人AIナレッジベースです。

## 目的

- スマホから雑にメモ・タスク・アイデアをGitHubへ入れる
- GitHub IssueをInboxとして使う
- daily issueのコメントを日次Markdownに変換する
- AIで雑メモを整理して `knowledge/` に蓄積する
- Claude Code / MCP / Obsidian / VS Code から参照しやすくする

## 全体像

```text
スマホ入力
  ↓
GitHub Issue / daily issue comment
  ↓
GitHub Actions
  ↓
Markdown化 / AI整形
  ↓
knowledge/ に蓄積
  ↓
Claude Code / MCP / Obsidian / GitHub検索で参照
```

## ディレクトリ構成

```text
personal-ai-kb/
├── inbox/                 # 一時メモ・未整理
├── blog/                  # 日次ログ
├── knowledge/             # 整理済みナレッジ
│   ├── tech/
│   ├── work/
│   ├── life/
│   ├── money/
│   ├── health/
│   └── ideas/
├── tasks/                 # タスク・レビュー
├── templates/             # Issue / daily / knowledgeテンプレート
├── scripts/               # 自動化スクリプト
├── docs/                  # 運用メモ
└── .github/workflows/     # GitHub Actions
```

## 最初にやること

### 1. GitHubで新規repoを作る

おすすめ名：

```text
personal-ai-kb
```

Private repo 推奨です。

### 2. このZIPを展開してpushする

```bash
unzip personal-ai-kb.zip
cd personal-ai-kb

git init
git add .
git commit -m "Initial personal AI knowledge base"
git branch -M main
git remote add origin git@github.com:<YOUR_NAME>/personal-ai-kb.git
git push -u origin main
```

HTTPSの場合：

```bash
git remote add origin https://github.com/<YOUR_NAME>/personal-ai-kb.git
git push -u origin main
```

### 3. GitHub Actions Secretsを設定する

GitHub repoの  
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

最低限：

```text
PERSONAL_AI_KB_TOKEN
```

これはGitHub Personal Access Tokenです。Issueの読み書きとrepoへのcommitに使います。

AI整形まで使う場合は、どれか1つを追加します。

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
```

## 運用ルール

```text
Issue = 雑に入れる場所
daily issue comment = 日々のメモ
blog/ = 日次ログ
knowledge/ = 整理済みナレッジ
Claude Code = 整理・レビュー係
MCP = 高度な外部ツール連携
```

## MVPでできること

- 今日のdaily issueを作る
- daily issueのコメントをMarkdownへ出力する
- knowledge-candidateラベル付きIssueを整理対象にする
- 将来のAI整形スクリプトを差し込める

## 詳細

- セットアップ: [`docs/setup.md`](docs/setup.md)
- 運用方法: [`docs/operation.md`](docs/operation.md)
- スマホ入力案: [`docs/mobile-input.md`](docs/mobile-input.md)
- Claude Code / MCP連携案: [`docs/claude-code-mcp.md`](docs/claude-code-mcp.md)
>>>>>>> a40553a (Initial personal AI knowledge base)
