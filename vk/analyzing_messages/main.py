import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3
from collections import Counter
from vk_api.utils import get_random_id
import re

vk_session = vk_api.VkApi(
    token='VK TOKEN')
vk = vk_session.get_api()

longpol = VkLongPoll(vk_session)

try:
    for event in longpol.listen():
        k = False
        try:
            print(event.chat_id)
            k = True
        except BaseException as e:
            print(e)
        if k is True and event.type == VkEventType.MESSAGE_NEW and event.chat_id == 33 and '!stat' in event.text:
            id = event.text.split()[1].split('|')[0].replace('[', '').replace('id', '')
            '''
            подключаемся к базе данных
            '''
            conn = sqlite3.connect("vk_db.sqlite")
            cursor = conn.cursor()
            '''
            запрос в базу данных на поиск такого id
            '''
            sql = f"""
                    SELECT * FROM messages
                    WHERE id = '{id}'
            """
            res = cursor.execute(sql).fetchall()
            dict_recurring_msgs = {}
            for el in res:
                dict_recurring_msgs[el[1]] = int(el[2])
            dict_recurring_msgs = sorted(dict_recurring_msgs.items(), key=lambda x: x[1])
            dict_recurring_msgs = dict(dict_recurring_msgs)
            x = Counter(dict_recurring_msgs)
            list_recurring_msgs = x.most_common()
            list_msg = []
            k = 1
            for el in list_recurring_msgs:
                if k <= 7:
                    list_msg.append(f'{el[0]} - {el[1]}')
                    k += 1
            if len(list_msg) != 0:
                text = f'Статистика на id{id}:\n\n' + '\n'.join(list_msg)
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=get_random_id(),
                    message=text
                )
            else:
                vk.messages.send(
                    chat_id=event.chat_id,
                    random_id=get_random_id(),
                    message=f'Статистика на id{id} на данный момент отсутствует'
                )
        elif k is True and event.type == VkEventType.MESSAGE_NEW and event.chat_id == 33 and '!all_stat' in event.text:
            '''
                    подключаемся к базе данных
                    '''
            conn = sqlite3.connect("vk_db.sqlite")
            cursor = conn.cursor()
            '''
            запрос в базу данных на поиск такого id
            '''
            sql = f"""SELECT * FROM messages"""
            res = cursor.execute(sql).fetchall()
            dict_recurring_msgs = {}
            for el in res:
                dict_recurring_msgs[el[1]] = int(el[2])
            dict_recurring_msgs = sorted(dict_recurring_msgs.items(), key=lambda x: x[1])
            dict_recurring_msgs = dict(dict_recurring_msgs)
            x = Counter(dict_recurring_msgs)
            list_recurring_msgs = x.most_common()
            list_msg = []
            k = 1
            for el in list_recurring_msgs:
                if k <= 7:
                    list_msg.append(f'{el[0]} - {el[1]}')
                    k += 1
            text = f'Статистика на всех:\n\n' + '\n'.join(list_msg)
            vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message=text
            )
        elif k is True and event.type == VkEventType.MESSAGE_NEW and event.chat_id == 33 and 'Статистика на' not in event.text and '!stat' not in event.text and '!all_stat' not in event.text:
            '''
            подключаемся к базе данных
            '''
            conn = sqlite3.connect("vk_db.sqlite")
            cursor = conn.cursor()
            '''
            запрос в базу данных на поиск такого id
            '''
            text = re.sub('[^a-zа-яё-]', ' ', event.text, flags=re.IGNORECASE)
            text = text.strip('-')
            for el in text.split():
                print(el)
                sql = f"""
                SELECT * FROM messages
                WHERE id = '{event.user_id}' AND message = '{el}'
                """
                res = cursor.execute(sql).fetchall()
                '''
                проверяем если уже есть такое,
                то делаем просто += 1
                '''
                if len(res) != 0:
                    sql = f"""
                            UPDATE messages
                            SET amount_mess = '{str(int(res[0][2]) + 1)}'
                            WHERE id = '{event.user_id}' AND message = '{el}'
                            """
                    cursor.execute(sql)
                    conn.commit()
                else:
                    sql = f"""
                            INSERT INTO messages
                            VALUES ('{event.user_id}', '{el}', '{str(1)}')
                            """
                    cursor.execute(sql)
                    conn.commit()
except BaseException:
    pass
