import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# Verzeichnis zum Speichern
VOICE_DIR = "voices"
os.makedirs(VOICE_DIR, exist_ok=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    if voice:
        file = await context.bot.get_file(voice.file_id)
        file_path = os.path.join(VOICE_DIR, f"{voice.file_id}.ogg")
        await file.download_to_drive(file_path)
        await update.message.reply_text("Sprachnachricht gespeichert.")
    else:
        await update.message.reply_text("Keine Sprachnachricht erkannt.")

# Exportierter Handler
voice_message_handler = MessageHandler(filters.VOICE, handle_voice)