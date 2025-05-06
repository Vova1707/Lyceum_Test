import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import wikipedia
from warnings import filterwarnings

# Игнорируем предупреждение BeautifulSoup
filterwarnings("ignore", category=UserWarning, module="wikipedia")


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.iWGJ7nURr_L_JftonlcwC-uZzusx6Kz56uVl_ba9W1rpT8kH_AwXEIOxuYKpC1MbZJdaieC2sx-4OANCe_TqEjWXJDKUz-qRha6PFhm49WQ0NQvz0VoMJU1RbPtdOMpUC4ArZqM1EdqSyFnojyQxAmvFQoUGLcwZN6lAwDHn3T6-uM_xx01AhuAa2FFyloLFD2ROX82bk-anrG0gfYz5rw')

    longpoll = VkBotLongPoll(vk_session, 230383848)  # ID без кавычек
    vk = vk_session.get_api()

    print("Бот запущен и ожидает сообщений...")

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            user_id = msg['from_id']
            text = msg['text']

            print(f'Новое сообщение от {user_id}: {text}')

            try:
                user_info = vk.users.get(user_ids=user_id)[0]
                full_name = f"{user_info['first_name']} {user_info['last_name']}"
            except Exception:
                full_name = "пользователь"
            if text.strip().endswith('?'):
                query = text.strip()[:-1]
                try:
                    page = wikipedia.page(query, auto_suggest=False)
                    summary = page.summary[:1000]
                    response = f"{summary}\n\nПодробнее: {page.url}"
                except wikipedia.exceptions.DisambiguationError as e:
                    options = "\n• ".join(e.options[:5])
                    response = f"Уточните запрос. Возможные варианты:\n• {options}"
                except wikipedia.exceptions.PageError:
                    response = "Не удалось найти информацию по вашему запросу."
                except Exception as e:
                    response = f"Произошла ошибка: {str(e)}"
            else:
                response = f"{full_name}, поставьте знак вопроса в конце сообщения, чтобы я мог ответить."

            vk.messages.send(
                user_id=user_id,
                message=response,
                random_id=random.getrandbits(31)
            )


if __name__ == '__main__':
    wikipedia.set_lang("ru")
    main()