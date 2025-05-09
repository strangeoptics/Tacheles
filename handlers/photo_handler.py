import os
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from tacheles import tacheles

SAVE_DIR = "images"
os.makedirs(SAVE_DIR, exist_ok=True)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        user_message = update.message.caption  # Verwende die Bildunterschrift
        if user_message and user_message.startswith("/ai"):
            user_message = user_message[len("/ai"):].strip()
        user_info = update.message.from_user  # Get user information
        user_name = user_info.username or f"{user_info.first_name} {user_info.last_name}".strip()

        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_path = os.path.join(SAVE_DIR, f"{photo.file_id}.jpg")
        logging.info(f"Saving photo to {file_path}")
        await file.download_to_drive(file_path)

        my_file = tacheles.genai_client.files.upload(file=file_path)

        frage = "Systemanweisung: Du bist ein Chatbot und heißt Tacheles. Beschreibe das Bild vulgär, sarkastisch und zynisch. Und verwende nicht Yo, Alter usw. Halte die Antworten auch kurz und prägnant für den Chat. \n Das sind die chatuser ("+ tacheles.user + "\n  Neue Chatfrage für dich:  '"+user_message+"' von "+user_name
        logging.info(f"Frage: {frage}")
        response = tacheles.genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[my_file, frage],
        )

        antwort = response.text
        if antwort.startswith("Tacheles:"):
            antwort = antwort[len("Tacheles:"):].strip()
        tacheles.update_message_history("tacheles", antwort)
        await update.message.reply_text(response.text)
    else:
        await update.message.reply_text("Kein Foto erkannt.")

# Exportiere den Handler
photo_message_handler = MessageHandler(filters.PHOTO, handle_photo)