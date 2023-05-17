import vk_api
from vk_api.longpoll import VkLongPoll
import requests
from vk_api.exceptions import ApiError
from config import token_bot, token_vk

vk_session = vk_api.VkApi(token=token_bot)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
vk_tok = vk_api.VkApi(token=token_vk)


def send_msg(user_id, message):
    vk.messages.send(user_id=user_id, message=message, random_id=0)


def send_photo(user_id, attachment):
    vk.messages.send(user_id=user_id, attachment=attachment, random_id=0)


def get_user_info(user_id):
    url = "https://api.vk.com/method/users.get"
    params = {
        "access_token": token_vk,
        "user_ids": user_id,
        "v": "5.131",
        "fields": "bdate, sex, city, relation"
    }
    res = requests.get(url, params).json()
    age = 2023 - int(res["response"][0]["bdate"].split(".")[2])
    city_id = 1
    sex = res["response"][0]["sex"]
    name = res["response"][0]["first_name"]
    surname = res["response"][0]["last_name"]
    link = f"https://vk.com/id" + str(user_id)
    if sex == 2:
        sex = 1
    return city_id, age, sex, name, surname, link


def search(user_info_tuple: tuple, offset):
    try:
        profiles = vk_tok.method("users.search",
                                 {"city_id": user_info_tuple[0],
                                  "age_from": user_info_tuple[1],
                                  "age_to": user_info_tuple[1],
                                  "sex": user_info_tuple[2],
                                  "count": 10,
                                  "offset": offset
                                  })
    except ApiError:
        return
    profiles = profiles["items"]
    user_id_list = []
    for profile in profiles:
        if not profile["is_closed"]:
            user_id_list.append({"name": profile["first_name"] + " " + profile["last_name"],
                                 "id": profile["id"]
                                 })
    return user_id_list


def photos_get(user_id):
    photos = vk_tok.method("photos.get",
                           {"album_id": "profile",
                            "owner_id": user_id,
                            "extended": 1
                            }
                           )
    try:
        photos = photos["items"]
        user_photo_list_to_sort = []
        for _ in range(len(photos)):
            summ = photos[_]["likes"]["count"] + photos[_]["comments"]["count"]
            user_photo_list_to_sort.append({"owner_id": photos[_]["owner_id"], "id": photos[_]["id"], "likes": summ})
        user_photo_list_to_sort.sort(key=lambda dictionary: dictionary["likes"])
        user_photo_list_to_sort.reverse()
    except KeyError:
        return
    user_photo_list = []
    for num, photo in enumerate(user_photo_list_to_sort):
        user_photo_list.append({"owner_id": photo["owner_id"],
                                "id": photo["id"]
                                })
        if num == 3:
            break
    return user_photo_list
