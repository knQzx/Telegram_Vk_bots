import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def get_command_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('English 🎃', 'Russian 🤖')
    bot.send_message(message.from_user.id, 'Choice your language', reply_markup=keyboard)
    bot.register_next_step_handler(message, send_privacy_policy)


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


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    print(message.contact.phone_number)
    print(message.contact.first_name)
    print(message.contact.user_id)
    if str(message.contact.phone_number)[1] in ['7', '8']:
        bot.send_message(message.from_user.id,
                         f'Я получил твой контакт: {message.contact.phone_number}')
    else:
        bot.send_message(message.from_user.id,
                         f'I get your contact: {message.contact.phone_number}')


bot.polling(none_stop=True, interval=0)
