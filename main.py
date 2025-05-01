from telegram.ext import Application
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler


user_data = {}


async def start(update, context):
    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    user_id = update.message.from_user.id

    user_data[user_id] = {}

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-Тест отправь файл с тестом!",
        reply_markup=markup
    )

async def stop(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        del user_data[user_id]
        await update.message.reply_text('Стоп')
    else:
        await update.message.reply_text("Начните сначала с /start.")

def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling()


if __name__ == '__main__':
    main()