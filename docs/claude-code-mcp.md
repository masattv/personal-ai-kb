# Claude Code / MCP連携案

## 役割分担

```text
GitHub = データ本体
GitHub Actions = 定期処理
Claude Code = 整理・変換・レビュー
MCP = 外部ツール接続
Obsidian = 閲覧
```

## Claude Codeにやらせること

- Issueを整理してMarkdown化
- blog/から週次レビューを作成
- knowledge/の重複を統合
- タグの揺れを修正
- 古いIssueを棚卸し
- READMEやindexを更新

## 例プロンプト

```text
knowledge-candidateラベルのIssueを読み、
knowledge/配下に整理済みMarkdownとして保存してください。
カテゴリは tech/work/life/money/health/ideas から選び、
YAML frontmatterを付けてください。
```

## MCPでやるとよいこと

- GitHub repo参照
- ファイル横断検索
- ローカルObsidian vault参照
- 必要ならブラウザ検索
- 必要ならカレンダーやタスク管理との接続

## MCPでやらない方がいいこと

- 毎回のスマホメモ入力
- 単純なIssue作成
- daily comment追加

単純な入力はGitHub APIの方が安定します。
