from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from utils.get_token import BOT_TOKEN
from utils.get_inflation import handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bienvenido a Argentina con Datos!'
    )

async def inflation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requested_period = context.args[0]
        inflation_rate = handler(requested_period)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=inflation_rate
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Algo salió mal \U0001F61E por favor intente de nuevo.'
        )



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    inflation_handler = CommandHandler('inflacion', inflation)
    application.add_handler(inflation_handler)
    
    application.run_polling()
