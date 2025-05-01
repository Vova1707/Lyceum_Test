from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from random import randint


async def start(update, context):
    reply_keyboard = [['Вход']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-Экскурсовот!",
        reply_markup=markup
    )


async def exs(update, context):
    zals = {'Зал 1': ([['Зал 2', 'Выход']], 'декорации первого зала'),
            'Зал 2': ([['Зал 3']], 'что-то из второго зала'),
            'Зал 3': ([['Зал 1', 'Зал 4']], 'штуки из третьего зала'),
            'Зал 4': ([['Зал 1']], 'мега интересное из четвёртого зала'),
    }
    text = update.message.text
    if text == 'Вход':
        text = 'Зал 1'

    markup = ReplyKeyboardMarkup(zals[text][0], one_time_keyboard=False)
    await update.message.reply_text(
        "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб! "
        f"В данном зале представлено {zals[text][1]}."
        " Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!",
        reply_markup=markup
    )



def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^(Выход)$"), start))

    application.add_handler(MessageHandler(filters.Regex(
        '^(Зал 1|Зал 2|Зал 3|Зал 4|Вход)$'), exs))
    application.run_polling()


if __name__ == '__main__':
    main()