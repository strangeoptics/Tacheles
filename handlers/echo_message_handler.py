from telegram import Update
from telegram.ext import MessageHandler, filters, ContextTypes

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

echo_message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
