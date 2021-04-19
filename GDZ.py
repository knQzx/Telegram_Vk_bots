import telebot


bot = telebot.TeleBot('TOKEN')



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет\nесли вводишь английский то вводи номер страницы\nесли русский. алгебру или геометрию то упражнения")
        bot.send_message(message.from_user.id, 'пишешь к примеру "русский 43" или "английский 93"')
    elif 'англ' in message.text.lower():
        try:
            s = message.text.split()
            urll = f'https://gdz.ru/class-8/english/reshebnik-spotlight-8-angliyskiy-v-fokuse-vaulina-yu-e/{s[1]}-s/'
            bot.send_message(message.from_user.id, urll)
        except:
            bot.send_message(message.from_user.id, 'ты чето ввел не так')
    elif 'русск' in message.text.lower():
        try:
            s = message.text.split()
            urll = f'https://gdz.ru/class-8/russkii_yazik/trostencova-8/{s[1]}-nom/'
            bot.send_message(message.from_user.id, urll)
        except:
            bot.send_message(message.from_user.id, 'ты чето ввел не так')
    elif 'алге' in message.text.lower():
        try:
            s = message.text.split()
            urll = f'https://gdz.ru/class-8/algebra/makarychev-8/{s[1]}-nom/'
            bot.send_message(message.from_user.id, urll)
        except:
            bot.send_message(message.from_user.id, 'ты чето ввел не так')
    elif 'геом' in message.text.lower():
        try:
            s = message.text.split()
            urll = f'https://gdz.ru/class-8/geometria/atanasyan-8/{s[1]}-task/'
            bot.send_message(message.from_user.id, urll)
        except:
            bot.send_message(message.from_user.id, 'ты чето ввел не так')



bot.polling(none_stop=True, interval=0)
