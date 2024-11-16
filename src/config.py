import os
from pathlib import Path
import sys
from loguru import logger

def setup_logger():
    """Configure logging settings for the application"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "slack_bot.log"

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
        "<level>{message}</level>"
    )

    # Remove default logger
    logger.remove()
    
    # Add stdout handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )
    
    # Add file handler
    logger.add(
        log_file,
        format=log_format,
        level="DEBUG",
        rotation="1 day"
    )

def load_environment():
    """Load and validate environment variables"""
    required_vars = {
        "SLACK_BOT_TOKEN": os.environ.get("SLACK_BOT_TOKEN"),
        "SLACK_APP_TOKEN": os.environ.get("SLACK_APP_TOKEN"),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY")
    }

    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

    # Set Gemini API key in environment
    os.environ["GEMINI_API_KEY"] = required_vars["GEMINI_API_KEY"]
    
    return required_vars
