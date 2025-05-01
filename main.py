from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from random import choice


poems = [
    ['Я помню чудное мгновенье:',
    'Передо мной явилась ты,',
    'Как мимолетное виденье,',
    'Как гений чистой красоты.',
     ],

    [
    'Буря мглою небо кроет,',
    'Вихри снежные крутя;',
    'То, как зверь, она завоет,',
    'То заплачет, как дитя.',
     ],
]

user_data = {}


async def start(update, context):
    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        del user_data[user_id]

    user_data[user_id] = {
        "state": "awaiting_line",
        "poem": choice(poems),
        "current_line_index": 1,
    }

    first_line = user_data[user_id]["poem"][0]
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-литератор давай зачитаем с тобой стихотворение!"
        f"Я начну:\n{first_line}",
        reply_markup=markup
    )

async def stop(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        del user_data[user_id]
        await update.message.reply_text('Стоп игра')
    else:
        await update.message.reply_text("Начните сначала с /start.")



async def suphler(update, context):
    user_id = update.message.from_user.id

    if user_id in user_data:
        current_index = user_data[user_id]["current_line_index"]
        return_text = ''
        if user_data[user_id]["poem"][current_index] == update.message.text:
            next_index = current_index + 1
            if len(user_data[user_id]["poem"]) - 1 <= next_index:
                if len(user_data[user_id]["poem"]) - 1 == next_index:
                    return_text += f'Последняя строка:\n{user_data[user_id]["poem"][next_index]}\n'

                return_text += 'Конец стиха. Нажмите на старт чтобы начать заново'
                del user_data[user_id]
            else:
                return_text += f'{user_data[user_id]["poem"][next_index]}'
                user_data[user_id]["current_line_index"] = next_index + 1
        else:
            return_text += '\nнет, не так\n'
            print(user_data[user_id]["poem"][current_index])
            return_text += f'Начинается с {user_data[user_id]["poem"][current_index][0: len(user_data[user_id]["poem"][current_index]) // 2]}...'
        await update.message.reply_text(return_text)
    else:
        await update.message.reply_text("Начните сначала с /start.")



def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, suphler)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()