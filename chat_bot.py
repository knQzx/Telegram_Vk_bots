import telebot
import random
import datetime
from telebot import types

bot = telebot.TeleBot('TOKEN')

ggusers = []

users = []




@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global users
    print(message.text)
    if message.chat.id not in ggusers:
        if message.text == "привет" or message.text == "Привет":
            k = f'Username - @{message.from_user.username}, id - {message.chat.id}'
            if k not in users:
                users.append(f'Username - @{message.from_user.username}, id - {message.chat.id}')
            bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
            keyboard = types.InlineKeyboardMarkup()
            key_ad1 = types.InlineKeyboardButton(text='задать вопрос администратору', callback_data='ad1')
            keyboard.add(key_ad1)
            key_ad2 = types.InlineKeyboardButton(text='начать общение по id', callback_data='ad2')
            keyboard.add(key_ad2)
            key_ad3 = types.InlineKeyboardButton(text='узнать свой id', callback_data='ad3')
            keyboard.add(key_ad3)
            key_ad4 = types.InlineKeyboardButton(text='помощь', callback_data='ad4')
            keyboard.add(key_ad4)
            bot.send_message(message.from_user.id, text='Выбери нужную тебе функцию', reply_markup=keyboard)
        elif message.text == "/help" or message.text == "помощь":
            bot.send_message(message.from_user.id, "Напиши привет")
        elif message.text == 'check users':
            bot.send_message(message.from_user.id, f"{users}")
        elif message.text == 'бан юзеру' and message.chat.id == 763258583:
            bot.send_message(message.from_user.id, f'Введи id user:')
            bot.register_next_step_handler(message, banuser)
        elif message.text == 'разблокировка' and message.chat.id == 763258583:
            bot.send_message(message.from_user.id, "Введи id юзера:")
            bot.register_next_step_handler(message, razblokuser)
        elif message.text == 'посмотреть забаненных' and message.chat.id == 763258583:
            bot.send_message(message.from_user.id, f'Вот - {ggusers}')
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    else:
        bot.send_message(message.from_user.id, "Извини но ты забанен в данной системе")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print(vars(call))
    if call.data == "ad1":
        bot.send_message(call.message.chat.id, "Пиши свой вопрос:")
        bot.register_next_step_handler(call.message, regstr_new_question)
    elif call.data == "ad2":
        bot.send_message(call.message.chat.id, "Введи id user:")
        bot.register_next_step_handler(call.message, regstr_new_rty)
    elif call.data == "ad3":
        bot.send_message(call.message.chat.id, f"Твой id - {call.message.chat.id}")
    elif call.data == "ad4":
        bot.send_message(call.message.chat.id, "Напиши /help.")




def razblokuser(message):
    try:
        n = int(message.text)
        ggusers.remove(n)
        bot.send_message(message.from_user.id, 'Успех')
    except:
        bot.send_message(message.from_user.id, 'Что то пошло не так')


def banuser(message):
    global ggusers
    try:
        ss = int(message.text)
        if ss != 763258583:
            ggusers.append(ss)
            bot.send_message(message.from_user.id, 'Юзер заблокан')
        else:
            bot.send_message(message.from_user.id, 'Так он админ')
    except:
        bot.send_message(message.from_user.id,'Шо то не так')



def regstr_new_question(message):
    body = f'Text message: {message.text}\n------------\nName user - @{message.from_user.username}\nUser id - {message.chat.id}\nDate send message - {str(datetime.datetime.now())}'
    bot.send_message(763258583, body)
    bot.send_message(message.chat.id, '@' + str(message.from_user.username) + ',' + ' я получил сообщение и очень скоро на него отвечу :)')

def regstr_new_rty(message):
    global r
    try:
        r = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Проверьте правильность ввода id')
    bot.send_message(message.chat.id, 'Выбери "аноним" или "официально"')
    bot.register_next_step_handler(message, regstr_vid)


def regstr_vid(message):
    gg = message.text
    if gg == 'аноним':
        bot.send_message(message.chat.id, 'Ты выбрал анонимно\nНапиши текст сообщения')
        bot.register_next_step_handler(message, regstr_new_text333)
    elif gg == 'официально':
        bot.send_message(message.chat.id, 'Ты выбрал официально\nНапиши текст сообщения')
        bot.register_next_step_handler(message, regstr_new_text)


def regstr_new_text(message):
    tt = message.text
    msg = (f'From user: {message.chat.id}\n'
           f'Text message: {tt}\n'
           f'Name user - @{message.from_user.username}\n'
           f'Date send message - {str(datetime.datetime.now())}')
    try:
        bot.send_message(r, msg)
        bot.send_message(message.chat.id, 'Ну вроде всё хорошо')
    except:
        bot.send_message(message.chat.id, 'Проверьте правильность ввода id')
        bot.register_next_step_handler(message, get_text_messages)


def regstr_new_text333(message):
    tt = message.text
    msg = (f'From user: Аноним\n'
           f'Text message: {tt}')
    try:
        bot.send_message(r, msg)
        bot.send_message(message.chat.id, 'Ну вроде всё хорошо')
    except:
        bot.send_message(message.chat.id, 'Проверьте правильность ввода id')
        bot.register_next_step_handler(message, get_text_messages)


bot.polling(none_stop=True, interval=0)
