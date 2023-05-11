from api import send_msg, longpoll, send_photo, get_user_info, search, photos_get
from dbase import check_db, create_tables
from vk_api.longpoll import VkEventType
offset = 0
create_tables()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() == "поиск" or event.text.lower() == "gjbcr":
            send_msg(event.user_id, "Нашли:")
            find_user_info = get_user_info(event.user_id)
            offset += 10
            while offset < 1000:
                list_more_users = search(find_user_info, offset)
                while len(list_more_users) > 0:
                    item_user_id = list_more_users.pop(-1)["id"]
                    check_db(event.user_id, item_user_id)
                    photo_user_dict = photos_get(item_user_id)
                    for item in photo_user_dict:
                        photo_data_owner_id = item["owner_id"]
                        photo_data_user_id = item["id"]
                        send_photo(event.chat_id, f"photo{photo_data_owner_id}_{photo_data_user_id}")
            else:
                print("Анкеты закончились")
        else:
            send_msg(event.user_id, "Неверная команда")