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
import json
import os

from utils.get_token import BOT_TOKEN


FEEDBACK = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Bienvenido a Argentina con Datos!'
    )

async def inflation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        requested_period = context.args[0]
        
        client = boto3.client('lambda', region_name='us-west-2')
        
        response = client.invoke(
            FunctionName=os.environ['LAMBDA_INFLATION'],
            InvocationType='RequestResponse',
            Payload=json.dumps({'date': requested_period})
        )

        inflation_rate = json.loads(response['Payload'].read())['inflation_rate']

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=inflation_rate
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Algo salió mal \U0001F61E por favor intente de nuevo.'
        )

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
    
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler('comentario', feedback)],
        states={
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(feedback_handler)
    
    application.run_polling()
