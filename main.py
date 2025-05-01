from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from datetime import datetime

# Удалить клаву: reply_markup=ReplyKeyboardRemove()
async def echo(update, context):
    await update.message.reply_text(f'Я получил сообщение- "{update.message.text}"')


from telegram.ext import CommandHandler



async def start(update, context):
    print(context.args)

    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        reply_markup=markup
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


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    if context.args and len(context.args) == 1:
        try:
            TIMER = int(context.args[0])
            chat_id = update.effective_message.chat_id
            job_removed = remove_job_if_exists(str(chat_id), context)
            context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

            text = f'Таймер сработает {TIMER} секунд!'
            if job_removed:
                text += ' Стараый таймер удален.'
            await update.effective_message.reply_text(text)
        except ValueError:
            await update.message.reply_text("Неккоректно указано время")
    else:
        print(context.args)
        await update.message.reply_text("Укажите секунды для таймера")


async def task(context):
    await context.bot.send_message(context.job.chat_id, text='Таймер!')


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("date", date_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset_timer", unset))
    application.add_handler(text_handler)
    application.run_polling()



reply_keyboard = [['/start', '/help'],
                  ['/date', '/time'],
                  #['/set', '/unset']
                  ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

if __name__ == '__main__':
    main()