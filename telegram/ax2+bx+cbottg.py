import telebot
import math

bot = telebot.TeleBot('token')


def massa_tela(message):
    global a
    try:
        a = int(message.text)
        bot.send_message(message.from_user.id, f'Теперь введи пожалуйста b')
        bot.register_next_step_handler(message, rost_tela)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')


def rost_tela(message):
    global b
    try:
        b = int(message.text)
        bot.send_message(message.from_user.id, f'Теперь введи пожалуйста - c')
        bot.register_next_step_handler(message, re)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')


def re(message):
    global c
    global Discriminant
    c = int(message.text)
    Discriminant = (b ** 2) - 4 * a * c
    if Discriminant <= 0:
        bot.send_message(message.from_user.id, 'Дискриминант меньше нуля, дальнейший счёт мы не можем продолжить')
    else:
        bot.send_message(message.from_user.id, f'Discriminant = {Discriminant}')
        bot.send_message(message.from_user.id, f'X1 = {(-b - math.sqrt((b ** 2) - 4 * a * c)) / 2}')
        bot.send_message(message.from_user.id, f'X2 = {(-b + math.sqrt((b ** 2) - 4 * a * c)) / 2}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Приветик😁")
        bot.send_message(message.from_user.id, 'Введи - a')
        bot.register_next_step_handler(message, massa_tela)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
