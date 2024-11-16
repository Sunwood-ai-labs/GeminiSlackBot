import sys
from loguru import logger
from src.config import setup_logger, load_environment
from src.bot import GeminiSlackBot

def main():
    """Main entry point for the Slack bot application"""
    try:
        # Setup logging
        setup_logger()
        logger.info("=== Gemini Slack Bot 起動 ===")

        # Load environment variables
        env_vars = load_environment()

        # Create and start bot
        bot = GeminiSlackBot(
            bot_token=env_vars["SLACK_BOT_TOKEN"],
            app_token=env_vars["SLACK_APP_TOKEN"]
        )
        bot.start()

    except Exception as e:
        logger.exception("起動時エラー発生")
        sys.exit(1)

if __name__ == "__main__":
    main()
