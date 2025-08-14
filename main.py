#!/usr/bin/env python3
"""
Comprehensive Telegram Bot with AI Assistant and Multiple Services
"""

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import (
    start_handler, help_handler, gemini_handler, youtube_handler,
    movie_handler, removebg_handler, vision_handler, text_handler
)
from config import Config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Start the bot"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("ai", gemini_handler))
    application.add_handler(CommandHandler("youtube", youtube_handler))
    application.add_handler(CommandHandler("movie", movie_handler))
    application.add_handler(CommandHandler("removebg", removebg_handler))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, vision_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Bot started successfully!")
    
    # Run the bot
    application.run_polling(allowed_updates=["message"])

if __name__ == '__main__':
    main()
