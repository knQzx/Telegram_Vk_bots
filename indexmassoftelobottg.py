import telebot

bot = telebot.TeleBot('токен')


def massa_tela(message):
    global msg
    try:
        msg = int(message.text)
        bot.send_message(message.from_user.id, f'Теперь введи пожалуйста свой рост в метрах через точку, пример - 1.75')
        bot.register_next_step_handler(message, rost_tela)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

def rost_tela(message):
    global msg12
    try:
        msg12 = float(message.text)
        bot.send_message(message.from_user.id, f'Теперь введи пожалуйста свой пол: "муж" или "жен" ')
        bot.register_next_step_handler(message, pol)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')


def pol(message):
    global msg20
    msg20 = message.text
    bot.send_message(message.from_user.id, f'Твой вес это {msg}, рост - {msg12}, и пол - {msg20}')
    IMT = msg / (msg12 * msg12)
    if IMT <= 16:
        bot.send_message(message.from_user.id, f'У тебя Недостаточная (дефицит) масса тела😅😅😅 Кушай больше')
    elif IMT >= 18.5 and IMT <= 25:
        bot.send_message(message.from_user.id, f'У тебя норма🥳🥳🥳')
    elif IMT >= 25 and IMT <= 30:
        bot.send_message(message.from_user.id, f'Избыточная масса тела (предожирение)😅😅😅 Надо кушать чуть меньше')
    elif IMT >= 30 and IMT <= 35:
        bot.send_message(message.from_user.id, f'Ожирение первой степени. Лол чел, давай ка снижай вес 😅')
    elif IMT >= 35 and IMT <= 40:
        bot.send_message(message.from_user.id, f'Ожирение второй степени. Ух ты, видимо любишь покушать, но надо худеть')
    elif IMT >= 40:
        bot.send_message(message.from_user.id, f'Ожирение третьей степени (морбидное), лол чел ты че такой жирный')



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Приветик😁\nТебя приветствует fitnessbot\nДелай всё что тебе говорят\nУдачки)🥳🥳🥳")
        bot.send_message(message.from_user.id, 'Введи свой вес')
        bot.register_next_step_handler(message, massa_tela)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
