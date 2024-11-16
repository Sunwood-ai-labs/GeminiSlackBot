# 🤖 Socket Mode対応 Gemini SlackBot

このノートブックでは、SlackのSocket Modeを使用してGemini 1.5 Flash搭載のSlackボットを作成します。

## 📚 1. 必要なライブラリのインストール

```python
!pip install slack_bolt litellm python-dotenv loguru
```

## 🔑 2. 環境設定

```python
import os
from dotenv import load_dotenv
from loguru import logger
import sys
from pathlib import Path

from google.colab import userdata


# 環境変数の読み込み
load_dotenv()

# Slack設定
SLACK_BOT_TOKEN = userdata.get('SLACK_BOT_TOKEN')    # xoxb-で始まるトークン
SLACK_APP_TOKEN = userdata.get('SLACK_APP_TOKEN')   # xapp-で始まるトークン

# Gemini API Key
os.environ["GEMINI_API_KEY"] = userdata.get('GEMINI_API_KEY')

# ログ設定
def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "slack_bot.log"

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>"
    )

    logger.remove()
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )
    logger.add(
        log_file,
        format=log_format,
        level="DEBUG",
        rotation="1 day"
    )

setup_logger()
```

## 📝 3. 応答スキーマの定義

```python
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "blocks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "text": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "text": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
}
```

## 🤖 4. ボットクラスの実装

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import litellm
import json

class GeminiSlackBot:
    def __init__(self, bot_token, app_token):
        logger.info("Socket Mode GeminiSlackBotの初期化を開始")

        # Boltアプリケーションの初期化
        self.app = App(token=bot_token)

        # イベントハンドラーの設定
        self.setup_handlers()

        # Socket Modeハンドラーの初期化
        self.handler = SocketModeHandler(self.app, app_token)

        logger.info("ボットの初期化が完了")

    def setup_handlers(self):
        """イベントハンドラーの設定"""
        # メンションされた時の処理
        @self.app.event("app_mention")
        def handle_mention(event, say):
            logger.info(f"メンション受信: {event['text']}")
            self._process_message(event, say)

        # DMの処理
        @self.app.event("message")
        def handle_message(event, say):
            # DMの場合のみ処理
            if event.get("channel_type") == "im":
                logger.info(f"DM受信: {event['text']}")
                self._process_message(event, say)

    def _process_message(self, event, say):
        """メッセージ処理のメインロジック"""
        try:
            channel = event["channel"]
            thread_ts = event.get("thread_ts", event["ts"])
            user_message = event["text"]

            # メンションの場合、ボットIDを削除
            if "<@" in user_message:
                user_message = user_message.split(">", 1)[1].strip()

            logger.debug(f"処理するメッセージ: {user_message}")

            # 処理中リアクション
            self.app.client.reactions_add(
                channel=channel,
                timestamp=thread_ts,
                name="hourglass_flowing_sand"
            )

            # Geminiから応答を取得
            response_data = self._get_gemini_response(user_message)

            # 応答を送信
            say(
                blocks=response_data["blocks"],
                text="新しいメッセージ",
                thread_ts=thread_ts
            )

            # リアクションの更新
            self.app.client.reactions_remove(
                channel=channel,
                timestamp=thread_ts,
                name="hourglass_flowing_sand"
            )
            self.app.client.reactions_add(
                channel=channel,
                timestamp=thread_ts,
                name="white_check_mark"
            )

        except Exception as e:
            logger.exception(f"メッセージ処理エラー: {str(e)}")
            say(
                text="申し訳ありません。エラーが発生しました。",
                thread_ts=thread_ts
            )
            self.app.client.reactions_add(
                channel=channel,
                timestamp=thread_ts,
                name="x"
            )

    def _get_gemini_response(self, user_message):
        """Geminiから応答を取得"""
        logger.info(f"Geminiへのリクエスト: {user_message[:100]}...")
        try:
            response = litellm.completion(
                model="gemini/gemini-1.5-flash-latest",
                # model="gemini/gemini-1.5-flash-8b",
                # model="gemini/gemini-exp-1114",
                messages=[
                    {
                        "role": "system",
                        "content": """あなたは親切なアシスタントです。
                        メッセージに対して、分かりやすく構造化された形で応答してください。
                        可能な限り絵文字を使用し、情報を見やすく提示してください。"""
                    },
                    {"role": "user", "content": user_message}
                ],
                response_format={
                    "type": "json_object",
                    "response_schema": RESPONSE_SCHEMA
                }
            )

            logger.debug("Geminiからの応答を受信")
            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            logger.error(f"Gemini APIエラー: {str(e)}")
            return {
                "blocks": [{
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🙇 申し訳ありません。エラーが発生しました。"
                    }
                }]
            }

    def start(self):
        """ボットを起動"""
        logger.info("Socket Modeでボットを起動")
        self.handler.start()
```

## 🚀 5. 実行コード

```python
if __name__ == "__main__":
    # 環境変数のチェック
    if not all([SLACK_BOT_TOKEN, SLACK_APP_TOKEN, os.environ.get("GEMINI_API_KEY")]):
        logger.error("必要な環境変数が設定されていません。")
        sys.exit(1)

    try:
        logger.info("=== Gemini Slack Bot 起動 ===")

        # ボットのインスタンス作成と起動
        bot = GeminiSlackBot(SLACK_BOT_TOKEN, SLACK_APP_TOKEN)
        bot.start()

    except Exception as e:
        logger.exception("起動時エラー発生")
        sys.exit(1)
```

## 📌 セットアップ手順

1. **Slack App の設定**
   - [Slack API](https://api.slack.com/apps) で新しいアプリを作成
   - Basic Information → Socket Mode を有効化
   - Basic Information → App-Level Tokens から新しいトークンを生成
     - `connections:write` スコープを付与
   - OAuth & Permissions で以下のスコープを追加:
     - `app_mentions:read`
     - `chat:write`
     - `im:history`
     - `reactions:write`
   - Event Subscriptions は設定不要（Socket Mode使用のため）
   - Events タブで以下のイベントを購読:
     - `app_mention`
     - `message.im`

2. **環境変数の設定**
   ```bash
   export SLACK_BOT_TOKEN="xoxb-your-bot-token"
   export SLACK_APP_TOKEN="xapp-your-app-token"
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

3. **アプリのインストール**
   - Slack ワークスペースにアプリをインストール
   - 使用したいチャンネルにアプリを追加

## 📝 使用例

1. **メンションでの利用**
   ```
   @あなたのボット こんにちは
   ```

2. **DMでの利用**
   - ボットとのDMで直接メッセージを送信

## 🔍 ログの確認

ログは `logs/slack_bot.log` に保存され、以下のような形式で出力されます：

```log
2024-11-16 10:00:00.123 | INFO     | __main__:start | === Gemini Slack Bot 起動 ===
2024-11-16 10:00:00.234 | INFO     | bot:setup | Socket Modeでボットを起動
2024-11-16 10:00:10.456 | INFO     | bot:handle_mention | メンション受信: こんにちは
```

## 📚 主な特徴

1. **Socket Mode対応**
   - パブリックエンドポイント不要
   - セキュアな接続
   - リアルタイムな応答

2. **構造化された応答**
   - Slack Block Kit形式
   - 絵文字を使用した視覚的な改善
   - メタデータのサポート

3. **エラーハンドリング**
   - 詳細なログ記録
   - リアクションによる状態表示
   - グレースフルな失敗処理

4. **非同期処理**
   - 効率的なメッセージ処理
   - レスポンスの遅延を最小化

注意: このコードを実行する前に、必要な環境変数が正しく設定されていることを確認してください。
