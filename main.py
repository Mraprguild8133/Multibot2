#!/usr/bin/env python3
"""
Comprehensive Telegram Bot with AI Assistant and Multiple Services (Webhook Version)
"""
from flask import Flask, request, jsonify, render_template
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot.handlers import (
    start_handler, help_handler, gemini_handler, youtube_handler,
    movie_handler, removebg_handler, vision_handler, text_handler
)
from config import Config
import logging
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    """Status page"""
    return render_template('index.html', status="Bot is running")

async def post_init(application: Application) -> None:
    """Post initialization - set webhook"""
    webhook_url = Config.WEBHOOK_URL
    await application.bot.set_webhook(webhook_url)

def main():
    """Start the bot in webhook mode"""
    # Get bot token from environment
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
    application = Application.builder().token(bot_token).post_init(post_init).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("ai", gemini_handler))
    application.add_handler(CommandHandler("youtube", youtube_handler))
    application.add_handler(CommandHandler("movie", movie_handler))
    application.add_handler(CommandHandler("removebg", removebg_handler))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, vision_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # Flask route for webhook
    @app.route('/webhook', methods=['POST'])
    async def webhook():
        """Handle incoming updates"""
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.update_queue.put(update)
        return jsonify(success=True)

    # Run Flask app
    (port=5000)

if __name__ == '__main__':
    main()
