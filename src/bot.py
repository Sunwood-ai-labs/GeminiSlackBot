from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import litellm
import json
from loguru import logger
from .schemas import RESPONSE_SCHEMA, SYSTEM_PROMPT

class GeminiSlackBot:
    def __init__(self, bot_token: str, app_token: str):
        """Initialize the Slack bot with Socket Mode"""
        logger.info("Socket Mode GeminiSlackBotの初期化を開始")
        
        self.app = App(token=bot_token)
        self.setup_handlers()
        self.handler = SocketModeHandler(self.app, app_token)
        
        logger.info("ボットの初期化が完了")

    def setup_handlers(self):
        """Set up event handlers for the bot"""
        @self.app.event("app_mention")
        def handle_mention(event, say):
            """Handle mentions in channels"""
            logger.info(f"メンション受信: {event['text']}")
            self._process_message(event, say)

        @self.app.event("message")
        def handle_message(event, say):
            """Handle direct messages"""
            if event.get("channel_type") == "im":
                logger.info(f"DM受信: {event['text']}")
                self._process_message(event, say)

    def _process_message(self, event, say):
        """Process incoming messages and generate responses"""
        try:
            channel = event["channel"]
            thread_ts = event.get("thread_ts", event["ts"])
            user_message = event["text"]

            # Remove mention if present
            if "<@" in user_message:
                user_message = user_message.split(">", 1)[1].strip()

            logger.debug(f"処理するメッセージ: {user_message}")

            # Add processing reaction
            self.app.client.reactions_add(
                channel=channel,
                timestamp=thread_ts,
                name="hourglass_flowing_sand"
            )

            # Get Gemini response
            response_data = self._get_gemini_response(user_message)

            # Send response
            say(
                blocks=response_data["blocks"],
                text="新しいメッセージ",
                thread_ts=thread_ts
            )

            # Update reactions
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

    def _get_gemini_response(self, user_message: str) -> dict:
        """Get response from Gemini AI"""
        logger.info(f"Geminiへのリクエスト: {user_message[:100]}...")
        try:
            response = litellm.completion(
                model="gemini/gemini-1.5-flash-latest",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
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
        """Start the bot"""
        logger.info("Socket Modeでボットを起動")
        self.handler.start()
