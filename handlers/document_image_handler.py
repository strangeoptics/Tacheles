import os
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# Verzeichnis zum Speichern
DOC_IMAGE_DIR = "images"
os.makedirs(DOC_IMAGE_DIR, exist_ok=True)

async def handle_document_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    # Sicherstellen, dass es ein Bild ist
    if document.mime_type and document.mime_type.startswith("image/"):
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(DOC_IMAGE_DIR, document.file_name)
        await file.download_to_drive(file_path)
        await update.message.reply_text(f"Bild gespeichert: {file_path}")
    else:
        await update.message.reply_text("Dies scheint kein Bild zu sein.")

# Exportierter Handler
document_image_handler = MessageHandler(filters.Document.IMAGE, handle_document_image)