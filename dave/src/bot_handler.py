import os
import random
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT, COMMAND
from enum import Enum

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_ENDPOINT = os.getenv('OLLMA_URL')
QBTORRENT_URL = "http://192.168.1.205:15080/api/v2/torrents"

class CallbackData(Enum):
    ASK_LLAMA = 'ask_llama'
    HELP = 'help'
    COMPLETED_TORRENTS = 'completed_torrents'

emojis = ['😀', '😂', '🤖', '😎', '🔥', '🌈', '🚀', '🎉', '💡', '📚']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command from user %s", update.effective_user.id)
    keyboard = [
        [
            InlineKeyboardButton("Ask llama", callback_data=CallbackData.ASK_LLAMA.value),
            InlineKeyboardButton("Help", callback_data=CallbackData.HELP.value),
            InlineKeyboardButton("Completed torrents", callback_data=CallbackData.COMPLETED_TORRENTS.value),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    logger.info("Button clicked with data: %s", query.data)

    if query.data == CallbackData.ASK_LLAMA.value:
        await query.edit_message_text(text="You chose to ask llama. Please enter the text:")
        context.user_data['awaiting_text'] = True
    elif query.data == CallbackData.HELP.value:
        random_emoji = random.choice(emojis)
        await query.edit_message_text(text=f"Help message {random_emoji}")
    elif query.data == CallbackData.COMPLETED_TORRENTS.value:
        await query.edit_message_text(text="Fetching completed torrents...")
        await completed_torrents(update, context)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_text'):
        user_input = update.message.text
        await process_llama_request(update.message, context, user_input)
        context.user_data['awaiting_text'] = False

async def process_llama_request(message, context, user_input):
    chat_id = message.chat_id
    request_payload = {
        "model":  "phi3:3.8b",
        "prompt": user_input,
        "format": "json",
        "stream": False}
    try:
        response = requests.post(API_ENDPOINT, json=request_payload)
        if response.status_code == 200:
            response_json = response.json()
            response_text = response_json.get("response", "")
            await context.bot.send_message(chat_id=chat_id, text=response_text)
        else:
            logger.error("Failed to stream response from API. Status code: %s, Response: %s", response.status_code, response.text)
            await context.bot.send_message(chat_id=chat_id, text="Failed to stream response from API.")
    except requests.exceptions.RequestException as e:
        logger.error("An error occurred while processing the LLM request: %s", e)
        await context.bot.send_message(chat_id=chat_id, text=f"An error occurred: {e}")

async def completed_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetch completed torrents."""
    try:
        response = requests.get(QBTORRENT_URL)
        if response.status_code == 200:
            sample_responses = random.sample([i.get('name') for i in response.json()], 3)
            logger.error("sample_responses")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"API Response: {sample_responses}")
        else:
            logger.error("Failed to fetch data from the API. Status code: %s", response.status_code)
            logger.error("Response: %s", response.text)
            logger.error("Request Headers: %s", response.request.headers)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to fetch data from the API.")
    except requests.exceptions.RequestException as e:
        logger.error("An error occurred while fetching completed torrents: %s", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {e}")

def main() -> None:
    logger.info("Starting bot application")
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(TEXT & ~COMMAND, message_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
