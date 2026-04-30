# スマホ入力案

## 方針

スマホ入力はMCP中心にしない方が安定します。

おすすめは以下です。

```text
スマホ
  → GitHub REST API
  → Issue作成 / daily issueコメント追加
```

## 入力導線

### 1. タスク登録

```text
入力: 音声 or テキスト
保存先: GitHub Issue
ラベル: task, inbox
```

### 2. 日次メモ登録

```text
入力: 音声 or テキスト
保存先: 今日のdaily issueコメント
ラベル: daily
```

### 3. ナレッジ候補登録

```text
入力: 雑メモ
保存先: GitHub Issue
ラベル: knowledge-candidate
```

## iPhoneショートカットでやること

GitHub REST APIを叩きます。

- Issue作成
- Issue検索
- Issueコメント追加

必要なもの：

```text
GitHub Token
repo owner
repo name
```

## Androidの場合

以下のどれかが現実的です。

- HTTP Request系アプリ
- Tasker
- 自作の超軽量Webフォーム
- GitHub Mobileで直接Issue作成

## 注意

スマホ側にAI APIキーを置かない方が安全です。

```text
スマホではGitHubに保存するだけ
AI整形はGitHub Actions側で実行
```
