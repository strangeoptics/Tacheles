import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from handlers import photo_message_handler, voice_message_handler, document_image_handler, ai_message_handler, all_message_handler, charakter_handler  # Import the charakter handler
from tacheles import tacheles  # Rename the shared instance

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)

print("Starting bot...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.message:
        await update.message.reply_text("Bin schon lange wach. Was ist los?")
    else:
        logging.warning("No update.message found in /start") 

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("You are so funny!")  

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tacheles.reset()
    await update.message.reply_text("Tacheles hat sich den Kopf gestoßen.")

async def log_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("History:\n %s", tacheles.get_message_history())

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = tacheles.users
    if users:
        user_list = "\n".join([f"{name}:  {description}\n" for name, description in users.items()])
        await update.message.reply_text(f"Users:\n{user_list}")
    else:
        await update.message.reply_text("No users found.")
    

def main() -> None:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        logging.error("TELEGRAM_TOKEN environment variable is not set.")
        return
    # Create the application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("reset", reset))  # Add reset handler
    application.add_handler(CommandHandler("history", log_history))  # Add the log_history handler
    application.add_handler(CommandHandler("listusers", list_users))  # Add the list_users handler
    application.add_handler(charakter_handler)  # Add charakter handler
    application.add_handler(ai_message_handler)
    application.add_handler(photo_message_handler)
    application.add_handler(voice_message_handler)
    application.add_handler(document_image_handler)
    application.add_handler(all_message_handler)  # Add all handler for text messages
   
    

    application.run_polling()

    print("polling...")


if __name__ == "__main__": 
    main()
