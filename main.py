import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():
    vk_session = vk_api.VkApi(
        token='vk1.a.iWGJ7nURr_L_JftonlcwC-uZzusx6Kz56uVl_ba9W1rpT8kH_AwXEIOxuYKpC1MbZJdaieC2sx-4OANCe_TqEjWXJDKUz-qRha6PFhm49WQ0NQvz0VoMJU1RbPtdOMpUC4ArZqM1EdqSyFnojyQxAmvFQoUGLcwZN6lAwDHn3T6-uM_xx01AhuAa2FFyloLFD2ROX82bk-anrG0gfYz5rw')

    longpoll = VkBotLongPoll(vk_session, '230383848')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])

            vk = vk_session.get_api()

            ans_user = vk.users.get(user_id=event.obj.message['from_id'])[0]
            try:
                ans_name, ans_surname = ans_user['first_name'], ans_user['last_name']
            except Exception as e:
                ans_name, ans_surname = 'пользователь', ''

            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Привет {ans_name} {ans_surname}",
                             random_id=random.getrandbits(31))

if __name__ == '__main__':
    main()