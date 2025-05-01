from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
import json
from random import choice


user_data = {}


async def start(update, context):
    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    user_id = update.message.from_user.id

    user_data[user_id] = {
        'right': 0,
    }

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-Тест отправь файл с тестом!",
        reply_markup=markup
    )

async def stop(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        del user_data[user_id]
        await update.message.reply_text('Стоп игра')
    else:
        await update.message.reply_text("Начните сначала с /start.")


async def test(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        if 'test' in user_data[user_id].keys():

            if not 'answers' in user_data[user_id].keys():
                user_data[user_id]["answers"] = list(user_data[user_id]['test'].keys())

            if user_data[user_id]['answers']:
                text = ''
                if not 'question' in user_data[user_id] or not user_data[user_id]["question"]:
                    user_data[user_id]["question"] = choice(user_data[user_id]['answers'])
                    text += user_data[user_id]['test'][user_data[user_id]["question"]]['question']

                else:
                    if user_data[user_id]['test'][user_data[user_id]["question"]]['response'] != update.message.text:
                        text = 'Неверно'
                    else:
                        text = 'Правильно'
                        user_data[user_id]["right"] += 1

                    del user_data[user_id]['answers'][user_data[user_id]['answers'].index(user_data[user_id]["question"])]
                    if not user_data[user_id]['answers']:
                        user_data[user_id]["question"] = None
                        text += f'\nТест пройден {user_data[user_id]["right"]}/{len(list(user_data[user_id]['test'].keys()))}'
                    else:
                        user_data[user_id]["question"] = choice(user_data[user_id]['answers'])
                        text += f'\n{user_data[user_id]['test'][user_data[user_id]["question"]]['question']}'
                await update.message.reply_text(text)
            else:
                await update.message.reply_text("Тест пройден. Начните сначала с /start. ")
        else:
            await update.message.reply_text("Отправьте JSON файл сначала")
    else:
        await update.message.reply_text("Начните сначала с /start.")


'''            if not user_data[user_id]["answers"]:
                await update.message.reply_text("Тест пройден, начните заново - /start")
            else:'''


async def load_test_from_json(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        try:
            file = await update.message.document.get_file()
            file_content = await file.download_as_bytearray()
            test_data = json.loads(file_content.decode('utf-8'))
            user_data[user_id]["test"] = test_data["test"]
            await update.message.reply_text("JSON файл загружен. Отправьте /test чтобы начать.")
        except (ValueError, KeyError, AttributeError):
            await update.message.reply_text("Неверный формат JSON файла. Пожалуйста, загрузите файл в нужном формате.")
    else:
        await update.message.reply_text("Начните сначала с /start.")



def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("test", test))
    application.add_handler(MessageHandler(filters.Document.ALL, load_test_from_json))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, test)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()