from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler
from random import randint


async def start(update, context):
    await update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "В каком городе вы живёте?", reply_markup=ReplyKeyboardRemove())
    return 1


async def first_response(update, context):
    locality = update.message.text
    print(locality)
    if locality != '/skip':
        await update.message.reply_text(
            f"Какая погода в городе {locality}?")
    else:
        await update.message.reply_text(
            f"Какая погода у вас за окном?")
    return 2


async def second_response(update, context):
    weather = update.message.text
    await update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END



def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()