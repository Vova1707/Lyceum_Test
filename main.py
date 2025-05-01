from telegram.ext import Application, MessageHandler, filters

from datetime import datetime


async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение- "{update.message.text}"')


from telegram.ext import CommandHandler



async def start(update, context):

    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def date_command(update, context):
    dt = datetime.now()
    res = dt.strftime('%Y-%m-%d')
    await update.message.reply_text(f"Сегодня {res}")


async def time_command(update, context):
    dt = datetime.now().time()
    res = dt.strftime('%H часов %M минут %S секунд')
    await update.message.reply_text(f"Сейчас {res}")


def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()