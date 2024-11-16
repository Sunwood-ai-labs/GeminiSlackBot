from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import litellm
from loguru import logger

class GeminiSlackBot:
    def __init__(self, bot_token: str, app_token: str):
        """Initialize the Slack bot with Socket Mode"""
        logger.info("Socket Mode GeminiSlackBotの初期化を開始")
        
        self.app = App(token=bot_token)
        self.setup_handlers()
        self.handler = SocketModeHandler(self.app, app_token)
        
        logger.info("ボットの初期化が完了")

    SYSTEM_PROMPT = """あなたは親切なアシスタントです。
メッセージに対して、分かりやすく構造化された形で応答してください。
可能な限り絵文字を使用し、情報を見やすく提示してください。"""

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
        channel = event["channel"]
        thread_ts = event.get("thread_ts", event["ts"])
        
        try:
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
                text=response_data["blocks"][0]["text"]["text"],  # Fallback text
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
            error_text = "🙇 申し訳ありません。エラーが発生しました。"
            say(
                text=error_text,
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
                        "content": self.SYSTEM_PROMPT
                    },
                    {"role": "user", "content": user_message}
                ]
            )

            logger.debug("Geminiからの応答を受信")
            
            # Handle the response content safely
            try:
                content = response.choices[0].message.content
            except AttributeError:
                # If the response structure is different, try alternate access methods
                content = getattr(response, 'text', None) or response.get('choices', [{}])[0].get('text', '')
                if not content:
                    raise ValueError("Unable to extract content from Gemini response")
            
            # Format the response as a Slack block
            return {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": content
                        }
                    }
                ]
            }

        except Exception as e:
            logger.error(f"Gemini APIエラー: {str(e)}")
            return {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "🙇 申し訳ありません。エラーが発生しました。"
                        }
                    }
                ]
            }

    def start(self):
        """Start the bot"""
        logger.info("Socket Modeでボットを起動")
        self.handler.start()
