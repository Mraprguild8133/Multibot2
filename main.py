#!/usr/bin/env python3
"""
Telegram Bot with Webhook for Render.com Deployment
"""

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handlers (simplified for example)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Bot is alive!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def post_init(application: Application) -> None:
    """Initialize webhook on Render"""
    webhook_url = f"https://{os.getenv('RENDER_SERVICE_NAME')}.onrender.com/telegram"
    await application.bot.set_webhook(webhook_url)

def main():
    """Start the bot in webhook mode for Render.com"""
    # Get configurations
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    # Create application
    application = Application.builder().token(bot_token).post_init(post_init).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Webhook configuration for Render
    port = int(os.getenv("PORT", 5000))
    webhook_url = f"https://{os.getenv('RENDER_SERVICE_NAME')}.onrender.com/telegram"
    
    logger.info(f"Starting webhook on port {port} with URL: {webhook_url}")
    
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=webhook_url,
        secret_token=os.getenv("WEBHOOK_SECRET"),
    )

if __name__ == '__main__':
    main()
