import logging
import os
from telegram import Update
import telegram
from telegram.ext import MessageHandler, filters, ContextTypes
from tacheles import tacheles  # Rename the shared instance

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        logging.warning("No update.message found in /ai")
        return

    user_message = update.message.text.strip()
    user_info = update.message.from_user
    user_name = user_info.username or f"{user_info.first_name} {user_info.last_name}".strip()
    chat_id = update.effective_chat.id

    logging.info(f"Message from user: {user_name}")
    logging.info(f"AI command received: {user_message}")

    tacheles.set_chat_id(chat_id)
    tacheles.update_message_history(user_name, user_message)

    response_text = tacheles.generate_response(user_name, user_message)
    if response_text:
        logging.info(f"AI response: {response_text}")
        await sende_nachricht_an_gruppe(response_text)
        tacheles.update_message_history("tacheles", response_text)
    else:
        logging.error("Failed to generate AI response.")


async def all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        logging.warning("No update.message found in all handler.")
        return

    user_message = update.message.text.strip()
    user_info = update.message.from_user
    user_name = user_info.username or f"{user_info.first_name} {user_info.last_name}".strip()

    logging.info(f"Message from user: {user_name}: {user_message}")

    tacheles.set_chat_id(update.effective_chat.id)
    tacheles.update_message_history(user_name, user_message)

    if tacheles.should_respond(user_name, user_message):
        logging.info(f"Bot decided to respond to the message from {user_name}.")
        response_text = tacheles.generate_response(user_name, user_message)
        if response_text:
            logging.info(f"AI response: {response_text}")
            await sende_nachricht_an_gruppe(response_text)
            tacheles.update_message_history("tacheles", response_text)
        else:
            logging.error("Failed to generate AI response.")
    else:
        logging.info(f"Bot decided not to respond to the message from {user_name}.")

async def sende_nachricht_an_gruppe(nachricht):
    """Send a message to a Telegram group."""
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    try:
        chat_id = tacheles.get_chat_id()
        await bot.send_message(chat_id=chat_id, text=nachricht)
        logging.info(f"Message successfully sent to group {chat_id}: {nachricht}")
    except telegram.error.TelegramError as e:
        logging.error(f"Error sending message: {e}")

ai_message_handler = MessageHandler(filters.Regex(r"^/ai\b"), ai)
all_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, all)
