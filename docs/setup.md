# セットアップ手順

## 1. GitHub repo作成

GitHubで新規repoを作成します。

おすすめ：

```text
personal-ai-kb
```

Private repo推奨です。

## 2. ZIPを展開してpush

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

## 3. GitHub Tokenを作成

Fine-grained Personal Access Token推奨です。

必要な権限目安：

- Repository contents: Read and write
- Issues: Read and write
- Metadata: Read-only

## 4. Actions Secretsを設定

GitHub repoの以下から設定します。

```text
Settings
  → Secrets and variables
  → Actions
  → New repository secret
```

追加するSecret：

```text
PERSONAL_AI_KB_TOKEN
```

AI整形を有効にする場合：

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
```

## 5. Actionsを手動実行

GitHubのActionsタブから以下を手動実行します。

```text
Create Daily Issue
Export Daily Issue
```

最初は `workflow_dispatch` で手動実行して、問題なければスケジュール運用に移します。
