import json
import random
import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot('ТОКЕН')


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
        text = f'⚡️Здравствуйте, {res_1[2]} {res_1[1]} ⚡\n🔥Ваш рейтинг - {res_2[1]} ⭐\n🙀 Выполнено заказов - {my_completed_orders}\n🎃 Ваших заказов на бирже - {my_orders_on_exchange}\n🤯 Пользователей в данный момент на бирже - {random.randint(14, 49)}'
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
        order = message.text.split()[1]
        theme_mess = message.text.split()[4]
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
        bot.send_message(message.from_user.id, 'Успешно удалена тема.')
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
                        text += f'Дедлайн: {el[el_2]["dedline"]}\n'
                        text += f'Оплата: {el[el_2]["pay"]}\n'
                        for response in el[el_2]['responses']:
                            print(response)
                            text += f'Отклик: @{response} - {el[el_2]["responses"][response]}\n'
                    text += '\n'
            bot.send_message(call.message.chat.id, text, reply_markup=keyboard)


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
