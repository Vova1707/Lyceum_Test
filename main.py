import vk_api
import os


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


def get_photos_from_album(vk_session, group_id, album_id):
    vk = vk_session.get_api()
    photos = vk.photos.get(
        owner_id=-group_id,
        album_id=album_id,
     )
    print(f"\nНайдено {photos['count']} фотографий в альбоме:")
    for i, photo in enumerate(photos['items'], 1):
        print(f"\nФото #{i}:")
        print(f"ID: {photo['id']}")
        print(f"Дата: {photo['date']}")
        or_ph = photo['orig_photo']
        print(f'{or_ph['height']}x{or_ph['width']}')
        print(f'URL: {or_ph['url']}')

    return photos['items']


def main():
    LOGIN, PASSWORD = 'kondrahinvov@yandex.ru', 'Konder12!'
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        auth_handler=auth_handler,
        captcha_handler=captcha_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    GROUP_ID = 230383848
    ALBUM_ID = 307208634
    photos = get_photos_from_album(vk_session, GROUP_ID, ALBUM_ID)


if __name__ == '__main__':
    main()