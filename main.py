import vk_api
import datetime


def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    # или код из приложения - генератора кодов
    key = input("Enter authentication code: ").strip()
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    LOGIN, PASSWORD = 'kondrahinvov@yandex.ru', 'Konder12!'
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()
    # Используем метод wall.get
    response = vk.friends.get(fields="bdate, city")
    if response['items']:
        for i in sorted(response['items'], key=lambda s: s['last_name']):
            stroka = f'Фамилия: {i['last_name']}'
            if 'bdate' in i.keys():
                stroka += f' ДР {i['bdate']}'
            print(stroka)


if __name__ == '__main__':
    main()
