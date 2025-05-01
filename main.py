import aiohttp
from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler


user_data = {}

async def geocoder(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        try:
            geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
            response = await get_response(geocoder_uri, params={
                "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
                "format": "json",
                "geocode": update.message.text
            })

            toponym = response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            ll = toponym["Point"]["pos"].split()
            static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll[0]},{ll[1]}&spn=0.18,0.18&pt={ll[0]},{ll[1]}&l=map"
            await context.bot.send_photo(
                update.message.chat_id,
                static_api_request,
                caption=f"Вот что нашёл по запросу: {update.message.text}"
            )
        except:
            await update.message.reply_text("Ошибка: Введите корректно запрос")
    else:
        await update.message.reply_text("Начните сначала с /start.")


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def start(update, context):
    reply_keyboard = [['/start', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    user_id = update.message.from_user.id

    user_data[user_id] = {
        'right': 0,
    }

    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-Геокодер отправь мне название города, а я выведу карту этого объекта!",
        reply_markup=markup
    )

async def stop(update, context):
    user_id = update.message.from_user.id
    if user_id in user_data.keys():
        del user_data[user_id]
        await update.message.reply_text('Стоп игра')
    else:
        await update.message.reply_text("Начните сначала с /start.")


def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, geocoder)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()