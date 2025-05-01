from telegram.ext import Application, MessageHandler, filters
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler
from random import randint


async def start(update, context):
    reply_keyboard = [['/dice ', '/timer', '/help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я Бот-помощник для игр!",
        reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


async def diсe(update, context):
    reply_keyboard = [['кинуть один шестигранный кубик', 'кинуть 2 шестигранных кубика одновременно'],
                      ['кинуть 20-гранный кубик', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Такс бросаем кубик выберите одну из команд", reply_markup=markup)


async def broke_kybik(update, context):
    text = update.message.text
    if text == 'кинуть один шестигранный кубик':
        await update.message.reply_text(f"Выпало {randint(1, 6)}")
    elif text == 'кинуть 20-гранный кубик':
        await update.message.reply_text(f"Выпало {randint(1, 20)}")
    elif text == 'кинуть 2 шестигранных кубика одновременно':
        await update.message.reply_text(f"Выпало {randint(1, 6)} и {randint(1, 6)}")


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    tm = {'30 секунд': 30, '1 минута': 60, '5 минут': 300}
    TIMER = tm[update.message.text]
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = f'засек {update.message.text}'
    if job_removed:
        text += ' Стараый таймер удален.'
    reply_keyboard = [['/close']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.effective_message.reply_text(text, reply_markup=markup)


async def task(context):
    time_in_sec = context.job.data
    time_str = {30: '30 секунд', 60: '1 минута', 300: '5 минут'}[time_in_sec]
    await context.bot.send_message(context.job.chat_id, text=f'{time_str} истекло')


async def close(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def timer(update, context):
    reply_keyboard = [['30 секунд', '1 минута'],
                      ['5 минут', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Такс ставим таймер выберите одну из команд", reply_markup=markup)




def main():
    application = Application.builder().token('7227875074:AAEoDFAWXsjZCYkHqMx2RnhTMcgJKzI55gU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dice", diсe))
    application.add_handler(CommandHandler("close", close))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(MessageHandler(filters.Regex(
        '^(кинуть один шестигранный кубик|кинуть 2 шестигранных кубика одновременно|кинуть 20-гранный кубик)$'),
                                           broke_kybik))
    application.add_handler(MessageHandler(filters.Regex(
        '^(30 секунд|5 минут|1 минута)$'),
                                           set_timer))
    application.add_handler(MessageHandler(filters.Regex('^(вернуться назад)$'), start))
    application.run_polling()


if __name__ == '__main__':
    main()