import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import requests
from io import BytesIO


def map(main_coords, add_params=None):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={main_coords[0]},{main_coords[1]}&spn=0.18,0.18&l=map"
    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)
    return BytesIO(response.content)


def get_coord(adress):
    server_address = "http://geocode-maps.yandex.ru/1.x/?"
    api_key = "8013b162-6b42-4997-9691-77b7074026e0"
    geocode = adress
    geocoder_request = f"{server_address}apikey={api_key}&geocode={geocode}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"
        ]
        toponym_coodrinates = toponym["Point"]["pos"]
        return float(toponym_coodrinates.split()[0]), float(
            toponym_coodrinates.split()[1]
        )
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def main():
    vk_session = vk_api.VkApi(
        token="vk1.a.iWGJ7nURr_L_JftonlcwC-uZzusx6Kz56uVl_ba9W1rpT8kH_AwXEIOxuYKpC1MbZJdaieC2sx-4OANCe_TqEjWXJDKUz-qRha6PFhm49WQ0NQvz0VoMJU1RbPtdOMpUC4ArZqM1EdqSyFnojyQxAmvFQoUGLcwZN6lAwDHn3T6-uM_xx01AhuAa2FFyloLFD2ROX82bk-anrG0gfYz5rw"
    )

    longpoll = VkBotLongPoll(vk_session, "230383848")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print("Новое сообщение:")
            print("Для меня от:", event.obj.message["from_id"])
            print("Текст:", event.obj.message["text"])

            vk = vk_session.get_api()

            ans_user = vk.users.get(user_id=event.obj.message["from_id"])[0]
            try:
                ans_name, ans_surname = ans_user["first_name"], ans_user["last_name"]
            except Exception as e:
                ans_name, ans_surname = "пользователь", ""
            try:
                main_coords = get_coord(event.obj.message["text"])
                map_image = map(main_coords)
                upload = vk_api.VkUpload(vk_session)
                photo = upload.photo_messages(map_image)[0]
                attachment = f"photo{photo['owner_id']}_{photo['id']}"
                vk.messages.send(
                    user_id=event.obj.message["from_id"],
                    message=f"{ans_name} {ans_surname} вот что я нашёл",
                    random_id=random.getrandbits(31),
                    attachment=attachment,
                )
            except Exception as e:
                vk.messages.send(
                    user_id=event.obj.message["from_id"],
                    message=f"{ans_name} {ans_surname} введи корректное название",
                    random_id=random.getrandbits(31),
                )
                print(e)


if __name__ == "__main__":
    main()
