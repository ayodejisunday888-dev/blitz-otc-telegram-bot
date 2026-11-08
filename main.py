import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Blitz OTC AI Signals! 📊\n\n"
        "Your Telegram bot is running.\n"
        "Use /status to check its connection.\n\n"
        "Market data is not connected yet, so no trading "
        "signals will be generated."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Status: ONLINE\n"
        "📊 Market Data: NOT CONNECTED\n"
        "🔔 Trading Signals: NOT ACTIVE\n\n"
        "We will activate signals only after testing "
        "a compatible and reliable market data source."
    )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Blitz OTC Telegram bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
