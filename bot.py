from dbase import check_db
from api import send_msg, send_photo, get_user_info, search, photos_get


def output_bot(event, find_user_info, offset):
    while offset < 1000:
        list_more_users = search(find_user_info, offset)
        while len(list_more_users) > 0:
            item_user_id = list_more_users.pop(-1)["id"]
            db_flag = check_db(event.user_id, item_user_id)
            if db_flag is False:
                photo_user_dict = photos_get(item_user_id)
                for item in photo_user_dict:
                    name = get_user_info(item_user_id)[3]
                    surname = get_user_info(item_user_id)[4]
                    link = get_user_info(item_user_id)[5]
                    send_msg(event.user_id, f"Имя: " + name + " Фамилия: " + surname + "\n" + link)
                    photo_data_owner_id = item["owner_id"]
                    photo_data_user_id = item["id"]
                    send_photo(event.user_id, f"photo{photo_data_owner_id}_{photo_data_user_id}")
            else:
                return
    else:
        send_msg(event.user_id, "Анкеты закончились")
