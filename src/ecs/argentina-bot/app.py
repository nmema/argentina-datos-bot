from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes, 
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

import boto3
import datetime
import os

from utils.get_token import BOT_TOKEN
from utils.lambda_invoke import get_data


FEEDBACK = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Bienvenido a Argentina con Datos!'
    text = """
¡Bienvenido al bot Argentina con Datos!\n
Un acercamiento de la información hacia las personas, realizando consultas a [Datos Argentina](https://www.datos.gob.ar/)\n
    """
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='markdown'
    )

async def inflation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requested_period = context.args[0]

        data = get_data(
            lambda_name='LAMBDA_INFLATION',
            payload={'date': requested_period}
        )
        inflation_rate = data['inflation_rate']

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=inflation_rate
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Algo salió mal \U0001F61E por favor intente de nuevo.'
        )

async def change_rates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requested_period = context.args[0]

        data = get_data(
            lambda_name='LAMBDA_CHANGE_RATES',
            payload={'date': requested_period}
        )
        change_rates = data['change_rates']
        
        if len(change_rates) == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='No hay información para el período solicitado.'
            )
        else:
            message = ''
            for k, v in change_rates.items():
                change_rate_string = f'{k:5} : $ {v:.2f}\n'
                message += change_rate_string
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'```\n{message}```',
                parse_mode='markdown'
            )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Algo salió mal \U0001F61E por favor intente de nuevo.'
        )

async def emae(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requested_period = context.args[0]
        
        data = get_data(
            lambda_name='LAMBDA_EMAE',
            payload={'date': requested_period}
        )

        emae_info = data['emae']

        if len(emae_info) == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='No hay información para el período solicitado.'
            )
        else:
            message = ''
            for k, v in emae_info.items():
                change_rate_string = f'{k:18} : {v:.3f}\n'
                message += change_rate_string
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'```\n{message}```',
                parse_mode='markdown'
            )
        
    except:
        pass

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Este Bot se encuentra en desarrollo!\n\n"
        "Dejame tu comentario de que te pareció la experiencia, "
        "y de nuevas funcionalidades que te gustaria ver.\n"
        "A mí gustaria tener nuevos comandos \U0001F60E"
    )
    return FEEDBACK

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_id = user['id']
    chat_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    message = update.message.text
    
    try:
        client = boto3.client('dynamodb', region_name='us-west-2')
        client.put_item(
            TableName=os.environ['DYNAMODB_FEEDBACK'],
            Item={
                'user_id': {'N': str(user_id)},
                'chat_date': {'S': chat_date},
                'message': {'S': message}
            }
        )
        
        await update.message.reply_text(
            'Listo! Muchas gracias por tu comentario \U0001F929'
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Algo salió mal \U0001F61E por favor intente de nuevo.'
        )
        
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Comentario cancelado."
    )

    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    inflation_handler = CommandHandler('inflacion', inflation)
    application.add_handler(inflation_handler)
    
    change_rates_handler = CommandHandler('tiposdecambio', change_rates)
    application.add_handler(change_rates_handler)
    
    emae_handler = CommandHandler('emae', emae)
    application.add_handler(emae_handler)
    
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler('comentario', feedback)],
        states={
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(feedback_handler)
    
    application.run_polling()
