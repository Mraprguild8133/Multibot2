#!/usr/bin/env python3
"""
Telegram Bot with Webhook - Fixed Version for Render.com
"""

import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Enable verbose logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    await update.message.reply_text('🚀 Bot is working! Send me a message.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message"""
    logger.info(f"Received message: {update.message.text}")
    await update.message.reply_text(f"You said: {update.message.text}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

async def set_webhook(app: Application):
    """Configure webhook on startup"""
    webhook_url = f"https://{os.getenv('RENDER_SERVICE_NAME')}.onrender.com/telegram"
    await app.bot.set_webhook(
        webhook_url,
        secret_token=os.getenv("WEBHOOK_SECRET"),
        drop_pending_updates=True
    )
    logger.info(f"Webhook set to: {webhook_url}")

def main():
    """Start the bot"""
    # Verify essential config
    if not (token := os.getenv("TELEGRAM_BOT_TOKEN")):
        logger.error("Missing TELEGRAM_BOT_TOKEN")
        return
    if not (service_name := os.getenv("RENDER_SERVICE_NAME")):
        logger.error("Missing RENDER_SERVICE_NAME")
        return

    # Create and configure application
    app = Application.builder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    # Webhook configuration
    port = int(os.environ.get("PORT", 5000))
    webhook_url = f"https://{service_name}.onrender.com/telegram"
    
    logger.info("Starting webhook...")
    
    # Run with webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=webhook_url,
        secret_token=os.getenv("WEBHOOK_SECRET"),
        ssl_context=None,  # Render handles SSL
    )

if __name__ == '__main__':
    main()
