import os
import json
import logging
import urllib.request
import urllib.error

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

BASE_URL = "https://otcharts.com"


def api_request(endpoint, api_key):
    url = BASE_URL + endpoint

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "BlitzOTCBot/1.0",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Blitz OTC AI Signals!\n\n"
        "Bot: ONLINE\n"
        "Market data: NOT VERIFIED\n"
        "Trading signals: NOT ACTIVE\n\n"
        "Commands:\n"
        "/status - Check bot status\n"
        "/testdata - Test OTCharts connection"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 BLITZ OTC BOT\n\n"
        "Telegram: ONLINE\n"
        "OTCharts: NOT VERIFIED\n"
        "Signal engine: NOT ACTIVE\n\n"
        "Use /testdata to test the connection."
    )


async def testdata(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔄 Checking OTCharts account and market data..."
    )

    api_key = os.getenv("OTCHARTS_API_KEY")

    if not api_key:
        await update.message.reply_text(
            "❌ OTCharts API key is missing."
        )
        return

    try:
        usage = api_request("/v1/usage", api_key)

        await update.message.reply_text(
            "✅ API account reached!\n\n"
            f"Plan: {usage.get('planName', usage.get('plan', 'Unknown'))}\n"
            f"Books: {', '.join(usage.get('books', []))}\n"
            f"Requests used: "
            f"{usage.get('requests', {}).get('used', 'Unknown')}\n"
            f"Request allowance: "
            f"{usage.get('requests', {}).get('quota', 'Unknown')}"
        )

        candles = api_request(
            "/v1/candles?venue=iq&symbol=EURUSD-OTC&tf=60&limit=5",
            api_key
        )

        bars = candles.get("candles", [])

        if not bars:
            await update.message.reply_text(
                "⚠️ Connection reached, but no candles were returned."
            )
            return

        message = (
            "✅ MARKET DATA RECEIVED!\n\n"
            f"Symbol: {candles.get('symbol', 'Unknown')}\n"
            f"Candles received: {len(bars)}\n\n"
        )

        for bar in bars:
            message += (
                f"Open: {bar.get('open')}\n"
                f"High: {bar.get('high')}\n"
                f"Low: {bar.get('low')}\n"
                f"Close: {bar.get('close')}\n\n"
            )

        await update.message.reply_text(message[:3500])

    except urllib.error.HTTPError as error:
        details = error.read().decode(
            "utf-8", errors="replace"
        )

        await update.message.reply_text(
            f"❌ OTCharts error: {error.code}\n\n"
            f"{details[:1500]}"
        )

    except Exception as error:
        logger.exception("Connection test failed")

        await update.message.reply_text(
            "❌ Test failed: "
            f"{type(error).__name__}"
        )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing.")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("testdata", testdata))

    logger.info("Blitz OTC bot is starting.")

    app.run_polling()


if __name__ == "__main__":
    main()
