import json
import random
import sqlite3

import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start(message):
    text = """Васап! 🤩 
Я — бот 🤯, умею:
- показывать меню 😜
- принимать доставку и самовывоз 🙄
"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('🍴 Меню', '🛒 Корзина')
    keyboard.add('📜 Заказы', '❓ FAQ')
    keyboard.add('📞 Контакты')
    """
    проверяем есть ли этот 
    пользователь в бд и если
    его нету, то добавляем вместе со словарями
    """
    conn = sqlite3.connect("shop.sqlite")
    cursor = conn.cursor()
    my_ord = cursor.execute(
        f'''SELECT * FROM shop_table WHERE id_tg="{message.from_user.id}"''').fetchone()
    if my_ord is None:
        pizza = json.dumps(
            {'pizza_1': '0', 'pizza_2': '0', 'pizza_3': '0', 'pizza_4': '0', 'pizza_5': '0'})
        desert = json.dumps(
            {'desert_1': '0', 'desert_2': '0', 'desert_3': '0', 'desert_4': '0', 'desert_5': '0'})
        nadrink = json.dumps(
            {'nadrinks_1': '0', 'nadrinks_2': '0', 'nadrinks_3': '0', 'nadrinks_4': '0',
             'nadrinks_5': '0'})
        burger = json.dumps({'burgers_1': '0', 'burgers_2': '0', 'burgers_3': '0', 'burgers_4': '0',
                             'burgers_5': '0'})
        sql = f"""INSERT INTO shop_table(id_tg, pizzas, burgers, deserts, nadrinks) 
            VALUES ('{message.from_user.id}', '{pizza}', '{desert}', '{nadrink}', '{burger}')"""
        cursor.execute(sql)
        conn.commit()
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text_response(message):
    global msg_for_back
    msg_for_back = message
    if message.text == '🍴 Меню':
        keyboard = types.InlineKeyboardMarkup()
        key_pizza = types.InlineKeyboardButton(text='Пицца 🍕 (5)', callback_data='key_pizza')
        key_desert = types.InlineKeyboardButton(text='Десерты 🥐 (5)', callback_data='key_desert')
        key_nadrinks = types.InlineKeyboardButton(text='Напитки б/а 🥤 (5)',
                                                  callback_data='key_nadrinks')
        key_beer = types.InlineKeyboardButton(text='Бургеры 🍔 (5)', callback_data='key_burger')
        keyboard.add(key_pizza, key_beer)
        keyboard.add(key_desert, key_nadrinks)

        bot.send_message(message.from_user.id, 'Выбирай', reply_markup=keyboard)
    elif message.text == '🛒 Корзина':
        """
        запрос к бд
        """
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT * FROM shop_table WHERE id_tg="{message.from_user.id}"''').fetchone()
        sp = []
        sum = 0
        for el in my_ord[1:]:
            json_data = json.loads(el)
            for el in json_data:
                if json_data[el] != '0':
                    if 'pizza' in el:
                        text = \
                        open(f'pizzas/descriptions/pizza_{el.split("_")[1]}', mode='r').readlines()[
                            0].rstrip()
                        sp.append(
                            f'{text}\n{json_data[el]} шт. x 560 руб. = {int(json_data[el]) * 560} руб.\n\n')
                        sum += int(json_data[el]) * 560
                    elif 'burgers' in el:
                        text = open(f'burgers/descriptions/burger_{el.split("_")[1]}',
                                    mode='r').readlines()[0].rstrip()
                        sp.append(
                            f'{text}\n{json_data[el]} шт. x 180 руб. = {int(json_data[el]) * 180} руб.\n\n')
                        sum += int(json_data[el]) * 180
                    elif 'desert' in el:
                        print(el, json_data[el])
                        text = open(f'desserts/descriptions/desert_{el.split("_")[1]}',
                                    mode='r').readlines()[0].rstrip()
                        sp.append(
                            f'{text}\n{json_data[el]} шт. x 150 руб. = {int(json_data[el]) * 150} руб.\n\n')
                        sum += int(json_data[el]) * 150
                    elif 'nadrinks' in el:
                        print(el, json_data[el])
                        text = open(f'non-alcoholic drinks/descriptions/nadrink_{el.split("_")[1]}',
                                    mode='r').readlines()[0].rstrip()
                        sp.append(
                            f'{text}\n{json_data[el]} шт. x 110 руб. = {int(json_data[el]) * 110} руб.\n\n')
                        sum += int(json_data[el]) * 110
        text_ = 'Корзина\n___________\n\n'
        for el in sp:
            text_ += el
        text_ += f'___________\n\nИтоговая сумма - {sum}'
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Купить', callback_data='th_1')
        key_2 = types.InlineKeyboardButton(text='Очистить корзину', callback_data='th_2')
        keyboard.add(key_1, key_2)
        bot.send_message(message.from_user.id, text_, reply_markup=keyboard)


number = 1
msg_id = int


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global number, msg_id
    if call.data == 'th_1':
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        pizza = json.dumps(
            {'pizza_1': '0', 'pizza_2': '0', 'pizza_3': '0', 'pizza_4': '0', 'pizza_5': '0'})
        desert = json.dumps(
            {'desert_1': '0', 'desert_2': '0', 'desert_3': '0', 'desert_4': '0', 'desert_5': '0'})
        nadrink = json.dumps(
            {'nadrinks_1': '0', 'nadrinks_2': '0', 'nadrinks_3': '0', 'nadrinks_4': '0',
             'nadrinks_5': '0'})
        burger = json.dumps({'burgers_1': '0', 'burgers_2': '0', 'burgers_3': '0', 'burgers_4': '0',
                             'burgers_5': '0'})
        cursor.execute(
            f"""UPDATE shop_table
                SET pizzas='{pizza}', deserts='{desert}', nadrinks='{nadrink}', burgers='{burger}'
                WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        bot.send_message(call.message.chat.id,
                         f'Ваш уникальный номер заказа - {random.randint(1111111, 999999999)}')
    elif call.data == 'th_2':
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        pizza = json.dumps(
            {'pizza_1': '0', 'pizza_2': '0', 'pizza_3': '0', 'pizza_4': '0', 'pizza_5': '0'})
        desert = json.dumps(
            {'desert_1': '0', 'desert_2': '0', 'desert_3': '0', 'desert_4': '0', 'desert_5': '0'})
        nadrink = json.dumps(
            {'nadrinks_1': '0', 'nadrinks_2': '0', 'nadrinks_3': '0', 'nadrinks_4': '0',
             'nadrinks_5': '0'})
        burger = json.dumps({'burgers_1': '0', 'burgers_2': '0', 'burgers_3': '0', 'burgers_4': '0',
                             'burgers_5': '0'})
        cursor.execute(
            f"""UPDATE shop_table
                        SET pizzas='{pizza}', deserts='{desert}', nadrinks='{nadrink}', burgers='{burger}'
                        WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        bot.send_message(call.message.chat.id, f'Корзина очищена.')
    """
    пиццы
    """
    if call.data == 'key_pizza':
        keyboard = types.InlineKeyboardMarkup()
        number = 1
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 560 руб.',
                                                    callback_data='key_buy_pizza_1')
        key_left = types.InlineKeyboardButton(text='⬅️', callback_data=f'key_pizza_left_5')
        key_number = types.InlineKeyboardButton(text='1/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️', callback_data='key_pizza_right_2')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'pizzas/descriptions/pizza_{number}', mode='r').read()
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open('pizzas/photos/pizza_1.jpg', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_pizza_right' in call.data:
        number += 1
        if number == 6:
            number = 1
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 560 руб.',
                                                    callback_data=f'key_buy_pizza_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_pizza_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_pizza_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'pizzas/descriptions/pizza_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id,
                       caption=text_caption,
                       photo=open(f'pizzas/photos/pizza_{number}.jpg', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_pizza_left' in call.data:
        number -= 1
        if number == 0:
            number = 5
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 560 руб.',
                                                    callback_data=f'key_buy_pizza_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_pizza_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_pizza_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'pizzas/descriptions/pizza_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open(f'pizzas/photos/pizza_{number}.jpg', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    """
    десерты
    """
    if call.data == 'key_desert':
        keyboard = types.InlineKeyboardMarkup()
        number = 1
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 150 руб.',
                                                    callback_data='key_buy_desert_1')
        key_left = types.InlineKeyboardButton(text='⬅️', callback_data=f'key_desert_left_5')
        key_number = types.InlineKeyboardButton(text='1/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️', callback_data='key_desert_right_2')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'desserts/descriptions/desert_{number}', mode='r').read()
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open('desserts/photos/desert_1.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_desert_right' in call.data:
        number += 1
        if number == 6:
            number = 1
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 150 руб.',
                                                    callback_data=f'key_buy_desert_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_desert_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_desert_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'desserts/descriptions/desert_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id,
                       caption=text_caption,
                       photo=open(f'desserts/photos/desert_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_desert_left' in call.data:
        number -= 1
        if number == 0:
            number = 5
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 150 руб.',
                                                    callback_data=f'key_buy_desert_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_desert_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_desert_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'desserts/descriptions/desert_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open(f'desserts/photos/desert_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    """
    безалкогольные напитки
    """
    if call.data == 'key_nadrinks':
        keyboard = types.InlineKeyboardMarkup()
        number = 1
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 110 руб.',
                                                    callback_data='key_buy_nadrinks_1')
        key_left = types.InlineKeyboardButton(text='⬅️', callback_data=f'key_nadrinks_left_5')
        key_number = types.InlineKeyboardButton(text='1/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️', callback_data='key_nadrinks_right_2')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'non-alcoholic drinks/descriptions/nadrink_{number}', mode='r').read()
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open('non-alcoholic drinks/photos/nadrink_1.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_nadrinks_right' in call.data:
        number += 1
        if number == 6:
            number = 1
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 110 руб.',
                                                    callback_data=f'key_buy_nadrinks_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_nadrinks_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_nadrinks_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'non-alcoholic drinks/descriptions/nadrink_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id,
                       caption=text_caption,
                       photo=open(f'non-alcoholic drinks/photos/nadrink_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_nadrinks_left' in call.data:
        number -= 1
        if number == 0:
            number = 5
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 110 руб.',
                                                    callback_data=f'key_buy_nadrinks_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_nadrinks_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_nadrinks_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'non-alcoholic drinks/descriptions/nadrink_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open(f'non-alcoholic drinks/photos/nadrink_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    """
    бургеры
    """
    if call.data == 'key_burger':
        keyboard = types.InlineKeyboardMarkup()
        number = 1
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 180 руб.',
                                                    callback_data='key_buy_burgers_1')
        key_left = types.InlineKeyboardButton(text='⬅️', callback_data=f'key_burger_left_5')
        key_number = types.InlineKeyboardButton(text='1/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️', callback_data='key_burger_right_2')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'burgers/descriptions/burger_{number}', mode='r').read()
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open('burgers/photos/burger_1.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_burger_right' in call.data:
        number += 1
        if number == 6:
            number = 1
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 180 руб.',
                                                    callback_data=f'key_buy_burgers_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_burger_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_burger_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'burgers/descriptions/burger_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id,
                       caption=text_caption,
                       photo=open(f'burgers/photos/burger_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    elif 'key_burger_left' in call.data:
        number -= 1
        if number == 0:
            number = 5
        keyboard = types.InlineKeyboardMarkup()
        key_add_basket = types.InlineKeyboardButton(text='В корзину - 180 руб.',
                                                    callback_data=f'key_buy_burgers_{number}')
        key_left = types.InlineKeyboardButton(text='⬅️',
                                              callback_data=f'key_burger_left_{number - 1}')
        key_number = types.InlineKeyboardButton(text=f'{number}/5', callback_data='key_number')
        key_right = types.InlineKeyboardButton(text='➡️',
                                               callback_data=f'key_burger_right_{number + 1}')
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='key_back_menu')
        keyboard.add(key_add_basket)
        keyboard.add(key_left, key_number, key_right)
        keyboard.add(key_back)
        text_caption = open(f'burgers/descriptions/burger_{number}', mode='r').read()
        bot.delete_message(call.message.chat.id, msg_id + 1)
        bot.send_photo(call.message.chat.id, caption=text_caption,
                       photo=open(f'burgers/photos/burger_{number}.png', mode='rb'),
                       reply_markup=keyboard)
        msg_id = call.message.id
    """
    обработка добавления кнпоок
    """
    if 'key_buy_burgers' in call.data:
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT burgers FROM shop_table WHERE id_tg="{call.message.chat.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        ks = int(call.data.split('_')[3])
        json_data[f'burgers_{ks}'] = str(int(json_data[f'burgers_{ks}']) + 1)
        cursor.execute(
            f"""UPDATE shop_table 
                SET burgers = '{json.dumps(json_data)}'
                WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        document = open(f'burgers/descriptions/burger_{ks}').readlines()
        name_burger = document[0].rstrip()
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=f'{name_burger} добавлен в корзину')
    elif 'key_buy_nadrinks' in call.data:
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT nadrinks FROM shop_table WHERE id_tg="{call.message.chat.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        ks = int(call.data.split('_')[3])
        json_data[f'nadrinks_{ks}'] = str(int(json_data[f'nadrinks_{ks}']) + 1)
        cursor.execute(
            f"""UPDATE shop_table 
                SET nadrinks = '{json.dumps(json_data)}'
                WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        document = open(f'non-alcoholic drinks/descriptions/nadrink_{ks}').readlines()
        name_drink = document[0].rstrip()
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=f'{name_drink} добавлен в корзину')
    elif 'key_buy_desert' in call.data:
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT deserts FROM shop_table WHERE id_tg="{call.message.chat.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        ks = int(call.data.split('_')[3])
        json_data[f'desert_{ks}'] = str(int(json_data[f'desert_{ks}']) + 1)
        cursor.execute(
            f"""UPDATE shop_table 
                SET deserts = '{json.dumps(json_data)}'
                WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        document = open(f'desserts/descriptions/desert_{ks}').readlines()
        name_desert = document[0].rstrip()
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=f'{name_desert} добавлен в корзину')
    elif 'key_buy_pizza' in call.data:
        conn = sqlite3.connect("shop.sqlite")
        cursor = conn.cursor()
        my_ord = cursor.execute(
            f'''SELECT pizzas FROM shop_table WHERE id_tg="{call.message.chat.id}"''').fetchone()
        json_data = json.loads(my_ord[0])
        ks = int(call.data.split('_')[3])
        json_data[f'pizza_{ks}'] = str(int(json_data[f'pizza_{ks}']) + 1)
        cursor.execute(
            f"""UPDATE shop_table  
                SET pizzas = '{json.dumps(json_data)}'
                WHERE id_tg='{call.message.chat.id}'""")
        conn.commit()
        ks = int(call.data.split('_')[3])
        document = open(f'pizzas/descriptions/pizza_{ks}').readlines()
        name_pizza = document[0].rstrip()
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=f'{name_pizza} добавлен в корзину')
    """
    обратно в меню
    """
    if call.data == 'key_back_menu':
        text_response(msg_for_back)


bot.polling(none_stop=True, interval=0)
