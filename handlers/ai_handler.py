import logging
import os
from telegram import Update
import telegram
from telegram.ext import MessageHandler, filters, ContextTypes
from tacheles import tacheles  # Rename the shared instance

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user_message = update.message.text
        user_info = update.message.from_user  # Get user information
        user_name = user_info.username or f"{user_info.first_name} {user_info.last_name}".strip()
        chat_id = update.effective_chat.id
        print(f"Die Chat-ID dieser Gruppe ist: {chat_id}")

        logging.info(f"Message from user: {user_name} ")
                     
        if user_message.startswith("/ai"):
            user_message = user_message[len("/ai"):].strip()
        logging.info(f"AI command received: {user_message}")
        
        # Set chat_id using the setter method
        tacheles.set_chat_id(chat_id)
        
        # Update message history
        tacheles.update_message_history(user_name, user_message)
        
        # Generate content using Tacheles
        response_text = tacheles.generate_response(user_name, user_message)
        if response_text:
            logging.info(f"AI response: {response_text}")
            # Send the response back to the user
            #await update.message.reply_text(response_text)
            await sende_nachricht_an_gruppe(response_text)
            tacheles.update_message_history("tacheles", response_text)
        else:
            logging.error("Failed to generate AI response.")
    else:
        logging.warning("No update.message found in /ai")


async def all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info(f"Received a message in all handler.")
    user_message = update.message.text
    user_info = update.message.from_user  # Get user information
    tacheles.set_chat_id(update.effective_chat.id)
    
    user_name = user_info.username or f"{user_info.first_name} {user_info.last_name}".strip()
    logging.info(f"Message from user: {user_name}: {user_message}")
    tacheles.update_message_history(user_name, user_message)
    #await sende_nachricht_an_gruppe("nachricht")
    response = tacheles.genai_client.models.generate_content(
                model="gemini-2.0-flash", #model="gemini-2.0-flash",
                contents=f"Systemanweisung: Du bist ein Chatbot und heißt Tacheles. Antworte nur auf Chatnachrichten die an dich gerichtet sind oder die eine allgemeine Frage sind. Würdest du auf die Chatnachricht vom {user_name} antworten: '{user_message}'? Antworte mit 'ja' oder 'nein'."
            )
    logging.info(f"AI response: {response.text}")
    if response.text.strip().lower() == "ja":
        response_text = tacheles.generate_response(user_name, user_message)
        if response_text:
            logging.info(f"AI response: {response_text}")
            # Send the response back to the user
            #await update.message.reply_text(response_text)
            await sende_nachricht_an_gruppe(response_text)
            tacheles.update_message_history("tacheles", response_text)
        else:
            logging.error("Failed to generate AI response.")

async def sende_nachricht_an_gruppe(nachricht):
    """Sendet eine Nachricht an eine Telegram-Gruppe."""
    bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
    try:
        chat_id = tacheles.get_chat_id()  # Call the method to get the chat ID
        await bot.send_message(chat_id=chat_id, text=nachricht)
        print(f"Nachricht erfolgreich an Gruppe {chat_id} gesendet: {nachricht}")
    except telegram.error.TelegramError as e:
        print(f"Fehler beim Senden der Nachricht: {e}")   


ai_message_handler = MessageHandler(filters.Regex(r"^/ai\b"), ai)
all_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, all)
