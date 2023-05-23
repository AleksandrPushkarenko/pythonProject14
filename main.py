from api import send_msg, longpoll, get_user_info
from vk_api.longpoll import VkEventType
from dbase import create_tables
from bot import output_bot
create_tables()
offset = 0

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() == "поиск" or event.text.lower() == "gjbcr":
            send_msg(event.user_id, "Нашли:")
            find_user_info = get_user_info(event.user_id)
            output_bot(event, find_user_info, offset)
            offset += 10
            if offset > 1000:
                send_msg(event.user_id, "Анкеты закончились")
                break
        else:
            send_msg(event.user_id, "Неверная команда")
