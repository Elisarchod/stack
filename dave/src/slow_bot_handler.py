#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import os
import logging
import requests
import random
from telegram import ForceReply, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

QBTORRENT_URL = "http://192.168.1.250:15080/api/v2/torrents/info?filter=completed"

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(rf"Hi {user.mention_html()}!", reply_markup=ForceReply(selective=True), )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    

    emojis = ['😊', '😂', '🥰', '🤔', '😢', '🎉', '🌟', '🔥', '🌈', '🍀']
    emoji = random.choice(emojis)
    await update.message.reply_text(f"Help! {emoji} {update.effective_user.mention_html()}!")


async def ask_ollma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    payload = {
        "model":  "phi3:3.8b",
        "prompt": update.message.text,
        "format": "json",
        "stream": False}

    # # Make the POST request
    response = requests.post(os.environ['OLLMA_URL'], json=payload)
    if response.status_code == 200:
        logger.info(f"API Response: {response.text}")
        await update.message.reply_text(response.json()['response'])
    else:
        response.raise_for_status()
        logger.error(f"Failed to fetch data from the API. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        logger.error(f"Request Headers: {response.request.headers}")
        await update.message.reply_text("Failed to fetch data from the API.")

async def completed_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch completed torrents."""
    response = requests.get(QBTORRENT_URL)
    if response.status_code == 200:
        sample_responses = random.sample([i.get('name') for i in response.json()], 3)
        await update.message.reply_text(f"API Response: {sample_responses}")
    else:
        response.raise_for_status()
        logger.error(f"Failed to fetch data from the API. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        logger.error(f"Request Headers: {response.request.headers}")
        await update.message.reply_text("Failed to fetch data from the API.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    logger.info(f"User: {update.effective_user.username} - Message: {update.message.text} \U0001F60A")
    await update.message.reply_text(update.message.text)


def main() -> None:
    
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    
    application = Application.builder().token(os.environ['BOT_TOKEN']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("torts", completed_torrents))
    application.add_handler(CommandHandler("ollma", ask_ollma))
    
    # add buttun for command

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
