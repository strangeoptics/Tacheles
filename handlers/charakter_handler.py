import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from tacheles import tacheles  # Rename the shared instance

async def charakter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /charakter command and sends a response to the user.
    """
    
    user_message = update.message.text
    user_message = user_message[len("/character"):].strip()
    logging.info("Received a message in charakter handler." + user_message)
    tacheles.set_character(user_message)  # Use Tacheles to update character
    logging.info(f"Updated character: {tacheles.get_character()}")
    await update.message.reply_text("Character updated.")

charakter_handler = CommandHandler("character", charakter)