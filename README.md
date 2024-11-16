# 🤖 Socket Mode対応 Gemini SlackBot

SlackのSocket Modeを使用して、Google Gemini AIと連携してインテリジェントな応答を提供するSlackボットです。Block Kit形式による視覚的なフィードバックと堅牢なエラー処理を実装しています。

## ✨ 主な機能

- 🔌 **Socket Mode 統合**
  - セキュアなWebSocket接続
  - パブリックエンドポイント不要
  - リアルタイムなメッセージ処理

- 🧠 **Gemini AI 統合**
  - 高度な言語モデルによる応答
  - コンテキストを考慮した会話
  - 構造化された出力形式

- 📱 **Slack Block Kit UI**
  - リッチなメッセージフォーマット
  - リアクションによる視覚的フィードバック
  - スレッドサポート
  - ダイレクトメッセージ対応

- 🛡️ **堅牢なエラー処理**
  - 包括的なログ記録
  - 視覚的なエラーフィードバック
  - グレースフルな障害回復

## 🚀 必要条件

- Python 3.8以上
- Slackワークスペースの管理者権限
- Google Cloudアカウント（Gemini API用）
- 必要なAPIキー：
  - Slack Bot Token
  - Slack App Token
  - Gemini API Key

## 📦 インストール

1. **Replitでのセットアップ**
   - Replitでこのリポジトリをフォーク
   - Replit Secretsで環境変数を設定
   - 依存関係は自動的に処理されます

2. **手動インストール**
```bash
# 必要なPythonパッケージをインストール
pip install slack-bolt==1.18.0
pip install litellm==1.10.1
pip install python-dotenv==1.0.0
pip install loguru==0.7.2
```

3. **環境変数の設定**
```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token"
export GEMINI_API_KEY="your-gemini-api-key"
```

## 🔧 Slack Appの設定

1. [api.slack.com/apps](https://api.slack.com/apps)で新しいSlack Appを作成

2. **Socket Modeの有効化**
   - Basic Information → Socket Mode
   - Socket Modeを有効化
   - `connections:write`スコープを持つApp-Level Tokenを生成

3. **Bot Token Scopesの設定**
   - OAuth & Permissionsに移動
   - 以下のスコープを追加：
     - `app_mentions:read`
     - `chat:write`
     - `im:history`
     - `reactions:write`

4. **イベントの購読**
   - Event Subscriptionsセクションで：
     - `app_mention`を購読
     - `message.im`を購読

5. **アプリのインストール**
   - ワークスペースにインストール
   - Bot User OAuth Tokenをコピー

## 💻 使用方法

### ボットの実行

```bash
python main.py
```

### ボットとの対話

1. **チャンネルでのメンション**
```
@bot-name Pythonプログラミングについて教えて
```

2. **ダイレクトメッセージ**
- ボットとのDMを開く
- メッセージを直接入力

### 対話例

1. **基本的な質問**
```
ユーザー: @bot-name Pythonとは何ですか？
ボット: 🐍 **Pythonプログラミング言語**
```
Pythonは以下の特徴を持つ多目的高級プログラミング言語です：

✨ 主な特徴：
• シンプルで読みやすい文法
• 豊富な標準ライブラリ
• クロスプラットフォーム対応
• 動的型付け

🚀 一般的な用途：
• Web開発
• データサイエンス
• AI/ML
• 自動化
```

2. **コード例のリクエスト**
```
ユーザー: @bot-name PythonのHello worldの例を示して
ボット: 👋 **Python Hello World例**
```
シンプルなHello Worldプログラムはこちら：

```python
print("Hello, World!")
```

✨ よりインタラクティブな例：
```python
name = input("名前を入力してください: ")  # ユーザーに名前を尋ねる
print(f"こんにちは、{name}さん！")  # 挨拶を表示
```


## 📝 ログ

ログは`logs/slack_bot.log`に以下の形式で保存されます：
```
2024-11-16 10:00:00.123 | INFO     | bot:start | === Gemini Slack Bot 起動 ===
```

ログレベル：
- DEBUG: 詳細なデバッグ情報
- INFO: 一般的な操作情報
- ERROR: エラー状態と例外

## 🔒 セキュリティ考慮事項

1. **APIキー管理**
   - APIキーは環境変数で安全に保管
   - APIキーをバージョン管理に含めない
   - APIキーを定期的にローテーション

2. **アクセス制御**
   - ボットのインストールを特定のワークスペースに制限
   - 必要なOAuthスコープを最小限に
   - ボットの使用状況とアクセスパターンを監視

3. **データプライバシー**
   - メッセージはメモリ内でのみ処理
   - 会話データの永続的な保存なし
   - ワークスペースのデータ保持ポリシーに準拠

## 🛠️ トラブルシューティング

1. **ボットが応答しない場合**
   - 環境変数が正しく設定されているか確認
   - ログでエラーメッセージを確認
   - ボットがチャンネルに招待されているか確認
   - Socket Mode接続状態を確認

2. **APIエラー**
   - APIキーの権限を確認
   - レート制限を確認
   - ネットワーク接続を確認
   - Gemini APIクォータを確認

3. **メッセージフォーマットの問題**
   - Block Kitフォーマットを確認
   - メッセージ長の制限を確認
   - マークダウン構文を確認
   - 絵文字のサポートを確認

## 🚀 デプロイメント

### Replitでのデプロイメント（推奨）
1. ReplitでリポジトリをFork
2. Replit Secretsで環境変数を設定
3. "Run"をクリックしてボットを起動
4. 24/7運用のために"Always On"を有効化

### その他のデプロイメントオプション
1. **ローカルマシン**
   - 手動インストール手順に従う
   - screen/tmuxで永続的な実行
   - システムサービスのセットアップ（オプション）

2. **クラウドプラットフォーム**
   - サーバーレス関数としてデプロイ
   - コンテナオーケストレーションを使用
   - 自動スケーリングのセットアップ（オプション）

## 🛠️ 開発

### プロジェクト構造
```
├── src/
│   ├── __init__.py
│   ├── bot.py         # メインのボット実装
│   └── config.py      # 設定とログのセットアップ
├── logs/              # ログファイルディレクトリ
├── main.py           # アプリケーションのエントリーポイント
└── README.md
```

### 主要コンポーネント

1. **GeminiSlackBotクラス** (`src/bot.py`)
   - Slackイベントの処理
   - メッセージ処理の管理
   - Gemini AIとの統合

2. **設定** (`src/config.py`)
   - 環境変数の管理
   - ログ設定
   - システム設定

### エラー処理

ボットは複数層のエラー処理を実装：
1. 入力検証
2. APIエラー処理
3. レスポンスフォーマット検証
4. リアクションによる視覚的フィードバック

## 🤝 コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 変更をコミット
4. ブランチにプッシュ
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細はLICENSEファイルを参照してください。

## 🙏 謝辞

- [Slack Bolt for Python](https://slack.dev/bolt-python/concepts)
- [Google Gemini AI](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Slack Block Kit](https://api.slack.com/block-kit)
