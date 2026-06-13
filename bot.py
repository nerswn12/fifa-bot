from flask import Flask, send_file
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import json
import os

BOT_TOKEN = os.environ.get("8980488374:AAFQHLYKY072189JUSSoyEZOY33nscQm6kU")
ADMIN_ID = 6062006736

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"stream":"https://example.com/live.m3u8"}, f)

def get_stream():
    with open(DATA_FILE,"r") as f:
        return json.load(f)["stream"]

def set_stream(url):
    with open(DATA_FILE,"w") as f:
        json.dump({"stream":url}, f)

app_web = Flask(__name__)

@app_web.route("/")
def player():
    return send_file("player.html")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    site_url = os.environ.get("SITE_URL")

    keyboard = [[
        InlineKeyboardButton(
            "⚽ FIFA Match",
            url=site_url
        )
    ]]

    await update.message.reply_text(
        "Select Match",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def setlink(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "/setlink https://example.com/live.m3u8"
        )
        return

    url = context.args[0]
    set_stream(url)

    await update.message.reply_text("✅ Stream Updated")

telegram_app = Application.builder().token(BOT_TOKEN).build()

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("setlink", setlink))

import threading

def run_bot():
    telegram_app.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
