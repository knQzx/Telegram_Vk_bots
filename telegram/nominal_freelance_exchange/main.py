import json
import random
import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot('2032759102:AAHdlvmMDN3d9sGZQNdEVqRXl3r5S5SEGzc')


@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['Меню 👉🏿'])
@bot.message_handler(content_types=['Назад 👉🏿'])
def get_command_start(message):
    """проверяем есть ли уже такие данные в бд"""
    conn = sqlite3.connect("nominal.sqlite")
    cursor = conn.cursor()
    res_1 = cursor.execute(
        f'''SELECT * FROM users WHERE id_tg="{message.from_user.id}"''').fetchone()
    res_2 = cursor.execute(
        f'''SELECT * FROM rating WHERE id_tg="{message.from_user.id}"''').fetchone()
    res_3 = cursor.execute(
        f'''SELECT my_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
    res_4 = cursor.execute(
        f'''SELECT completed_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
    if res_1 is None:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('English 🎃', 'Russian 🤖')
        bot.send_message(message.from_user.id, 'Choice your language', reply_markup=keyboard)
        bot.register_next_step_handler(message, send_privacy_policy)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_take = types.InlineKeyboardButton(text='Взять заказ', callback_data='take_order')
        key_my = types.InlineKeyboardButton(text='Мои заказы', callback_data='my_orders')
        key_rating = types.InlineKeyboardButton(text='Посмотреть историю рейтинга',
                                                callback_data='my_rating')
        keyboard.add(key_take, key_my)
        keyboard.add(key_rating)
        """
        считаем сколько заказов на бирже сейчас наших
        """
        print(res_3)
        if res_3 is None:
            my_orders_on_exchange = '0'
        else:
            my_orders_on_exchange = len(res_3)
        """
        считаем сколько заказов выполнено наших
        """
        print(res_4)
        if res_4 is None:
            my_completed_orders = '0'
        else:
            my_completed_orders = len(res_4)
        text = f'⚡️Здравствуйте, {res_1[2]} {res_1[1]} ⚡\n🔥Ваш рейтинг - {res_2[1]} ⭐\n' \
               f'🙀 Выполнено заказов - {my_completed_orders}\n' \
               f'🎃 Ваших заказов на бирже - {my_orders_on_exchange}\n' \
               f'🤯 Пользователей в данный момент на бирже - {random.randint(14, 49)}'
        bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Меню 👉🏿')
        keyboard.add('Написать в тех-поддержку 🤖')
        bot.send_message(message.from_user.id, 'Новых сообщений нет', reply_markup=keyboard)


"""
отправляем файл политики конфиденциальности
"""


def send_privacy_policy(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'English 🎃':
        keyboard.add('I do not accept ❌', 'I accept ✅')
        bot.send_document(message.from_user.id, open('en/privacy_policy.docx', 'rb'),
                          reply_markup=keyboard)
    elif message.text == 'Russian 🤖':
        keyboard.add('Не принимаю ❌', 'Принимаю ✅')
        bot.send_document(message.from_user.id, open('ru/privacy_policy.docx', 'rb'),
                          reply_markup=keyboard)


"""
поделиться телефоном
"""


def create_ask_phone(language):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if language == 'ru':
        key = types.KeyboardButton('Поделиться своим номером телефона ✅', request_contact=True)
        markup.add(key)
    elif language == 'en':
        key = types.KeyboardButton('Share my phone ✅', request_contact=True)
        markup.add(key)
    return markup


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Принимаю ✅':
        bot.send_message(message.from_user.id, 'Привет! Делись контактом :>',
                         reply_markup=create_ask_phone('ru'))
    elif message.text == 'I accept ✅':
        bot.send_message(message.from_user.id, 'Hi! Can you send me your contact? :>',
                         reply_markup=create_ask_phone('en'))
    elif message.text == 'Обжаловать рейтинг 🤖':
        """
        обжалования рейтинга
        """
        bot.send_message(message.from_user.id, 'Наш админ - @knQzx')
    elif message.text == 'Добавить заказ 🤖':
        global msge
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Web ⚡️', callback_data='th_1')
        key_2 = types.InlineKeyboardButton(text='Telegram боты 🖥', callback_data='th_2')
        key_3 = types.InlineKeyboardButton(text='Вк боты 🔥', callback_data='th_3')
        key_4 = types.InlineKeyboardButton(text='Скрипты 💻', callback_data='th_4')
        key_5 = types.InlineKeyboardButton(text='Взлом хакинг 💥', callback_data='th_5')
        key_6 = types.InlineKeyboardButton(text='Проекты для школы ✨', callback_data='th_6')
        keyboard.add(key_1, key_2)
        keyboard.add(key_3, key_4)
        keyboard.add(key_5, key_6)
        msge = bot.send_message(message.from_user.id, 'Выберите пожалуйста тему в которой будет '
                                                      'распологаться ваш заказ',
                                reply_markup=keyboard)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(f'Назад 👉🏿')
        bot.send_message(message.from_user.id, 'Если за вами будет замечен спам и флуд - '
                                               'вы будете забанены', reply_markup=keyboard)
    elif message.text == 'Удалить заказ 🎃':
        """
        полный алгоритм поиска темы и добавления в клавиатуру
        """
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT my_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        i = 1
        for theme in json_data:
            keyboard.add(f'Theme {i} - {theme}')
            i += 1
        keyboard.add(f'Назад 👉🏿')
        bot.send_message(message.from_user.id, 'Выбери тему', reply_markup=keyboard)
    elif message.text == 'Назад 👉🏿':
        """
        кнопка назад
        """
        get_command_start(message)
    elif 'Theme' in message.text:
        """
        полный алгоритм поиска заказа и добавления в клавиатуру
        """
        theme_mess = message.text.split(' - ')[1]
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT my_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for theme in json_data:
            if theme == theme_mess:
                for el in json_data[theme]:
                    for el_2 in el:
                        keyboard.add(f'Заказ {el_2} из темы {theme_mess}')
        keyboard.add('Назад 👉🏿')
        bot.send_message(message.from_user.id, 'Выбери заказ', reply_markup=keyboard)
    elif 'Заказ' in message.text and 'темы' in message.text:
        """
        полный алгоритм удаления заказа
        """
        order = ' '.join(message.text.split()[1:message.text.split().index('из')])
        theme_mess = ' '.join(message.text.split()[message.text.split().index('темы') + 1:])
        print(theme_mess, order)
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT my_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        list_del = []
        for i in range(len(json_data[theme_mess])):
            if list(json_data[theme_mess][i].items())[0][0] == order:
                list_del.append(list(json_data[theme_mess][i].items())[0][0])
        for i in range(len(json_data[theme_mess])):
            try:
                del json_data[theme_mess][i][list_del[0]]
            except BaseException:
                pass
        for el in json_data[theme_mess]:
            if el == {}:
                index_element_for_del = json_data[theme_mess].index(el)
                del json_data[theme_mess][index_element_for_del]
        cursor.execute(
            f'''UPDATE orders SET my_orders='{json.dumps(json_data)}'  WHERE id_tg="{message.from_user.id}"''')
        conn.commit()
        bot.send_message(message.from_user.id, 'Удалено.')
        get_command_start(message)
    elif message.text == 'Меню 👉🏿':
        get_command_start(message)
    elif message.text == 'Написать в тех-поддержку 🤖':
        bot.send_message(message.from_user.id, 'Наш админ - @knQzx')


# обработчик клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'my_rating':
        """
        берём из бд рейтинг чела
        """
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        res_2 = cursor.execute(
            f'''SELECT * FROM rating WHERE id_tg="{call.message.chat.id}"''').fetchone()
        history_rating = json.loads(res_2[2])
        text_rate_send = 'История вашего рейтинга:\n\n'
        for el in history_rating:
            if el == 'reg':
                text_rate_send += f'Дано ботом рейтинга - {history_rating[el]}\n'
            else:
                text_rate_send += f'Дано @{el} рейтинга - {history_rating[el]}\n'
        """
        проходимся по списку и высылаем данные
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Обжаловать рейтинг 🤖')
        keyboard.add('Назад 👉🏿')
        bot.send_message(call.message.chat.id, text_rate_send, reply_markup=keyboard)
    elif call.data == 'my_orders':
        """
        подключаемся к бд
        """
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT my_orders FROM orders WHERE id_tg="{call.message.chat.id}"''').fetchone()
        if f'{my_ord}' == 'None':
            bot.send_message(call.message.chat.id, f'Пользователь id{call.message.chat.id} '
                                                   f'не имеет на данный момент действующих заказов.')
        else:
            """
            кнопки удалить заказ и добавить заказ
            """
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add('Удалить заказ 🎃', 'Добавить заказ 🤖')
            keyboard.add('Назад 👉🏿')
            json_data = json.loads(my_ord[0])
            """
            подгружаем в формате json данные из бд чтобы отправить челу их
            """
            text = f'Заказы профиля id{call.message.chat.id}\n\n'
            for theme in json_data:
                text += f'Тема: {theme}\n\n'
                for el in json_data[theme]:
                    for el_2 in el:
                        text += f'Заказ: {el_2}\n'
                        text += f'Описание заказа: {el[el_2]["description"]}\n'
                        text += f'Дедлайн: {el[el_2]["dedline"]}\n'
                        text += f'Оплата: {el[el_2]["pay"]}\n'
                        for response in el[el_2]['responses']:
                            print(response)
                            text += f'Отклик: @{response} - {el[el_2]["responses"][response]}\n'
                    text += '\n'
            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)
    elif call.data in ['th_1', 'th_2', 'th_3', 'th_4', 'th_5', 'th_6']:
        if call.data == 'th_1':
            theme = 'Web ⚡️'
        elif call.data == 'th_2':
            theme = 'Telegram боты 🖥'
        elif call.data == 'th_3':
            theme = 'Вк боты 🔥'
        elif call.data == 'th_4':
            theme = 'Скрипты 💻'
        elif call.data == 'th_5':
            theme = 'Взлом хакинг 💥'
        elif call.data == 'th_6':
            theme = 'Проекты для школы ✨'
        bot.send_message(call.message.chat.id, 'Напишите пожалуйста название для вашего заказа')
        bot.register_next_step_handler(call.message, title_order, theme)


def title_order(message, theme):
    dict_ = {}
    if message.text == 'Назад 👉🏿':
        get_command_start(message)
    else:
        name_theme = [message.text, theme]
        dict_ = {message.text: {}}
        bot.send_message(message.chat.id, 'Напишите ваше описание к заказу')
        bot.register_next_step_handler(message, description_order, dict_, name_theme)


def description_order(message, dict_, name_theme):
    if message.text == 'Назад 👉🏿':
        get_command_start(message)
    else:
        name = name_theme[0]
        dict_[name]['description'] = message.text
        bot.send_message(message.chat.id, 'Напишите дедлайн для вашего заказа')
        bot.register_next_step_handler(message, dedline_order, dict_, name_theme)


def dedline_order(message, dict_, name_theme):
    if message.text == 'Назад 👉🏿':
        get_command_start(message)
    else:
        name = name_theme[0]
        dict_[name]['dedline'] = message.text
        bot.send_message(message.chat.id, 'Укажите цену, к примеру - 1000руб')
        bot.register_next_step_handler(message, pay_order, dict_, name_theme)


def pay_order(message, dict_, name_theme):
    if message.text == 'Назад 👉🏿':
        get_command_start(message)
    else:
        """
        полный алгоритм добавления заказа
        """
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT my_orders FROM orders WHERE id_tg="{message.from_user.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        #
        name = name_theme[0]
        dict_[name]['pay'] = message.text
        dict_[name]['responses'] = {}
        print(dict_)
        print(name_theme)
        """
        если это тема уже существует то просто добавляем в список
        """
        for themes in json_data:
            if themes == name_theme[1]:
                json_data[themes].append(dict_)
                """
                обновляем бд
                """
                cursor.execute(
                    f"""UPDATE orders 
                        SET my_orders='{json.dumps(json_data)}'
                        WHERE id_tg='{message.from_user.id}'""")
                conn.commit()
                bot.send_message(message.from_user.id, 'Добавлено')
                get_command_start(message)
                return
        """
        если этой темы ещё нет 
        то создаём новую и добавляем
        в неё данные
        """
        json_data[name_theme[1]] = [dict_]
        """
        обновляем бд
        """
        cursor.execute(
            f"""UPDATE orders 
                SET my_orders='{json.dumps(json_data)}'
                WHERE id_tg='{message.from_user.id}'""")
        conn.commit()
        bot.send_message(message.from_user.id, 'Добавлено')
        get_command_start(message)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    """проверяем есть ли уже такие данные в бд"""
    conn = sqlite3.connect("nominal.sqlite")
    cursor = conn.cursor()
    res = cursor.execute(f'''SELECT * FROM users WHERE id_tg="{message.from_user.id}"''').fetchone()
    """
    проверяем если запрос пустой, то есть None,
    то вставляем
    """
    if res is None:
        """
        пишем полученные данные в бд
        в дальнейшем для использования нами
        """
        conn = sqlite3.connect("nominal.sqlite")
        cursor = conn.cursor()
        name = message.contact.first_name.split()[1]
        surname = message.contact.first_name.split()[0]
        """
        вставляем теперь в бд рейтинга,
        и пишем что бот дал 4.8 изначально
        """
        rating_json = json.dumps({"reg": 4.8})
        cursor.execute(f"""INSERT INTO rating VALUES 
                            ('{message.from_user.id}', '4.8', '{rating_json}')
                        """)

        conn.commit()
        """
        добавили все данные
        """
    if str(message.contact.phone_number)[1] in ['7', '8'] or str(message.contact.phone_number)[
        0] in ['7', '8']:
        """
        делаем клавиатуру start
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Назад 👉🏿')
        bot.send_message(message.from_user.id,
                         f'Я получил твой контакт: {message.contact.phone_number}.'
                         f'Теперь у вас есть право пользоваться нашей биржей фриланса Nominal.',
                         reply_markup=keyboard)
        cursor.execute(f"""INSERT INTO users VALUES 
                            ('{message.from_user.id}', '{name}', '{surname}',
                             '{message.contact.phone_number}', '{message.from_user.username}', 'ru')
                        """)
        conn.commit()
    else:
        """
        делаем клавиатуру Назад 👉🏿
        """
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Назад 👉🏿')
        bot.send_message(message.from_user.id,
                         f'I get your contact: {message.contact.phone_number}.'
                         f'Now you have the right to use our Nominal freelance exchange.',
                         reply_markup=keyboard)
        cursor.execute(f"""INSERT INTO users VALUES 
                            ('{message.from_user.id}', '{name}', '{surname}',
                             '{message.contact.phone_number}', '{message.from_user.username}', 'en')
                        """)
        conn.commit()


bot.polling(none_stop=True, interval=0)
