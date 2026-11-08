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

async def testdata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import urllib.request
    import urllib.error

    api_key = os.getenv("OTCHARTS_API_KEY")

    if not api_key:
        await update.message.reply_text("OTCharts API key is missing.")
        return

    url = url = "https://otcharts.com/v1/candles?venue=iq&symbol=EURUSD-OTC&tf=60&limit=5"

    request = urllib.request.Request(
        url,
    headers={
    "Authorization": f"Bearer {api_key}",
    "User-Agent": "BlitzOTCBot/1.0"
}
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = response.read().decode("utf-8")
            await update.message.reply_text(
                "OTCharts response:\n" + result[:2500]
            )
    except urllib.error.HTTPError as error:
        await update.message.reply_text(
            f"OTCharts HTTP error: {error.code}"
        )
    except Exception as error:
        await update.message.reply_text(
            f"Connection error: {type(error).__name__}"
        )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("testdata", testdata))

    print("Blitz OTC Telegram bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
