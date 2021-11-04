import hashlib
import random
import telebot
from telebot import types
from make_html import make_html

bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start', 'info'])
def send_description_bot(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Сделать QR-код😋')
    keyboard.add('Профиль🎃')
    text = f'Привет 👋👋👋! Этот бот может помочь тебе не делать ' \
           f'вакцинацию и также свободно гулять по тц и общественным местам' \
           f'без qr кода. От тебя понадобятся только 3 первые буквы фамилии, имя, ' \
           f'и отчества. Вот так - К. Р. Н. Также понадобится:\n- твой год рождения в полном формате\n- первые 2 цифры паспорта и последние 3(если хочешь, можешь написать любые 5 цифр, это ни на что не влияет, просто если проверят твой паспорт и там будет несовпадение..))'
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


dannye = []


@bot.message_handler(content_types=['text'])
def send_text(message):
    global dannye
    if message.text == 'Сделать QR-код😋':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Назад🎃')
        bot.send_message(message.from_user.id, 'Напиши нам первую букву фамилии, имя и отчества,'
                                               'а так же год рождения в полном формате и первые 2 цифры паспорта'
                                               'и последние 3. Если хочешь, можешь написать рандомные 5 цифр. \n\n'
                                               'В ФОРМАТЕ: К. Р. Н. 01.01.2000 12512',
                         reply_markup=keyboard)
    elif message.text == 'Назад🎃':
        bot.send_message(message.from_user.id, 'Вы вернулись назад')
        send_description_bot(message)
    elif message.text == 'Да😺':
        bot.send_message(message.from_user.id, 'Делаю...')
        fio = dannye[0].split('. ')
        FIO = fio[:3]
        res = fio[3:][0].split(' ')
        date = res[0]
        passport = res[1]
        Hash_object_id = hashlib.md5(
            f'{random.randint(0, 1212121212121)}'.encode('utf-8')).hexdigest()
        result = make_html(FIO, date, passport, Hash_object_id)
        bot.send_message(message.from_user.id,
                         f'Твой сайт с данными (может не загружаться, надо подождать минут 5) - {result[0]}')
        bot.send_photo(message.from_user.id, photo=open(f'{result[1]}', 'rb'))
        bot.send_message(message.from_user.id, 'Вы вернулись назад')
        send_description_bot(message)
    elif message.text == 'Неа😿':
        dannye = []
        bot.send_message(message.from_user.id, 'Возвращаю в главное меню...')
        send_description_bot(message)
    else:
        dannye.append(message.text)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add('Да😺', 'Неа😿')
        bot.send_message(message.from_user.id, f'{message.text} - перепроверь, точно верно?',
                         reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
