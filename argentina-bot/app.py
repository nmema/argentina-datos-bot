from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from utils.get_token import BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bienvenido a Argentina con Datos!'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()