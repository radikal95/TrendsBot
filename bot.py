# -*- coding:utf-8 -*-
import requests
import config
import telebot
from telebot import types


MAILGUN_API_KEY = 'key-90629ec43738c8cbe97a6f98fc03bd26'
MAILGUN_SANDBOX_URL = 'https://api.mailgun.net/v3/sandbox1eb6b7c1a60c4220a1350c50b13e870a.mailgun.org/messages'
SEND_FROM_MAILGUN = '<radushin.arseny@yandex.ru>'
SEND_TO_MAILGUN = '<radushin.arseny@yandex.ru>'
bot = telebot.TeleBot(config.token)

@bot.message_handler(regexp='/senddata')
def send_complex_message(message):
    #filepath = (bot.get_file(message.document.file_id))
    #f_url = ('https://api.telegram.org/file/bot' + config.token + '/' + str(filepath.file_path))
    #name = str(message.chat.last_name + " " + message.chat.first_name + ".txt")
    #urllib.request.urlretrieve(f_url, name)
    url = 'https://api.mailgun.net/v3/sandbox1eb6b7c1a60c4220a1350c50b13e870a.mailgun.org/messages'
    auth = ('api', MAILGUN_API_KEY)
    files = [("attachment", ("text1.txt", open("TrendsBot/text1.txt", "rb").read())),
             ("attachment", ("text2.txt", open("TrendsBot/text2.txt", "rb").read())),
             ("attachment", ("text3.txt", open("TrendsBot/text3.txt", "rb").read())),
             ("attachment", ("text4.txt", open("TrendsBot/text4.txt", "rb").read())),
             ("attachment", ("text5.txt", open("TrendsBot/text5.txt", "rb").read()))]
    data = {
        'from': 'radushin.arseny@yandex.ru',
        'to': 'radushin.arseny@yandex.ru',
        'subject': 'Data from Telegram Bot',
        'text': '',
        "html": "<html>HTML version of the body</html>"
    }
    response = requests.post(url, auth=auth, data=data, files=files)
    response.raise_for_status()
    bot.send_message(message.chat.id, "Данные успешно переданы")
    pass

@bot.message_handler(regexp='/start')
def default_test(message):
    if message.chat.id not in config.users:
        config.users.append(message.chat.id)
        config.waiting.append(False)
        config.name_waiting.append(False)
        config.path.append('')
        config.name.append('')
        bot.send_message(message.chat.id,
                         "Добрый день! Добро пожаловать в бот стратегического семинара МегаФон. Для обратной связи следуйте подсказкам бота. Для начала введите Ваши имя и фамилию")
    else:
        config.path[config.users.index(message.chat.id)] = ''
        bot.send_message(message.chat.id,
                         "С возвращением! Это бот стратегического семинара МегаФон. Для обратной связи следуйте подсказкам бота. Для начала введите Ваши имя и фамилию")


    config.name_waiting[config.users.index(message.chat.id)] = True
    config.waiting[config.users.index(message.chat.id)] = True
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message.chat.id not in config.users:
        config.users.append(call.message.chat.id)
        config.waiting.append(False)
        config.path.append('')
    if call.message:
        if call.data == "1":
            config.waiting[config.users.index(call.message.chat.id)]=True
            config.path[config.users.index(call.message.chat.id)] = 'text1.txt'
            bot.send_message(call.message.chat.id, "Увидели в тренде новую возможность для нас - опишите её")
        if call.data == "2":
            config.waiting[config.users.index(call.message.chat.id)] = True
            config.path[config.users.index(call.message.chat.id)] = 'text2.txt'
            bot.send_message(call.message.chat.id, "Увидели в тренде угрозу / риск для нас - опишите её")
        if call.data == "3":
            config.waiting[config.users.index(call.message.chat.id)] = True
            config.path[config.users.index(call.message.chat.id)] = 'text3.txt'
            bot.send_message(call.message.chat.id, "Увидели в потребности новую возможность для нас - опишите её")
        if call.data == "4":
            config.waiting[config.users.index(call.message.chat.id)] = True
            config.path[config.users.index(call.message.chat.id)] = 'text4.txt'
            bot.send_message(call.message.chat.id, "Увидели в потребности угрозу / риск для нас - опишите её ")
        if call.data == "5":
            config.waiting[config.users.index(call.message.chat.id)] = True
            config.path[config.users.index(call.message.chat.id)] = 'text5.txt'
            bot.send_message(call.message.chat.id, "Какие-то ещё комментарии - я слушаю")

pass


@bot.message_handler(content_types='text')
def default_test(message):
    if message.chat.id not in config.users:
        config.users.append(message.chat.id)
        config.waiting.append(False)
        config.name_waiting.append(False)
        config.path.append('')
        config.name.append('')


    if config.waiting[config.users.index(message.chat.id)] == False:
        bot.send_message(message.chat.id, "Cначала выберите нужный пункт меню")

    if config.waiting[config.users.index(message.chat.id)]  and config.name_waiting[config.users.index(message.chat.id)] == False:
        f = open(config.path[config.users.index(message.chat.id)],'a', encoding='utf-8')
        f.write(message.chat.first_name+' '+message.chat.last_name+' known as ' + config.name[config.users.index(message.chat.id)]+' said: '+message.text + '\n')
        f.close()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        url_button = types.InlineKeyboardButton(text="1. Тренд - новая возможность             ", callback_data=1)
        url_button1 = types.InlineKeyboardButton(text="2. Тренд - угроза/риск", callback_data=2)
        url_button2 = types.InlineKeyboardButton(text="3. Потребность - новая возможность", callback_data=3)
        url_button3 = types.InlineKeyboardButton(text="4. Потребность - угроза/риск", callback_data=4)
        url_button4 = types.InlineKeyboardButton(text="5. Прочее", callback_data=5)
        keyboard.add(url_button, url_button1, url_button2, url_button3, url_button4)
        bot.send_message(message.chat.id, "Окей, принято", reply_markup=keyboard)
        config.waiting[config.users.index(message.chat.id)] = False
        config.path[config.users.index(message.chat.id)] = ''


    if config.waiting[config.users.index(message.chat.id)] and config.name_waiting[config.users.index(message.chat.id)]:
        config.name[config.users.index(message.chat.id)] = message.text

        bot.send_message(message.chat.id, "Окей, " + message.text + ', принято!')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        url_button = types.InlineKeyboardButton(text="1. Тренд - новая возможность             ", callback_data=1)
        url_button1 = types.InlineKeyboardButton(text="2. Тренд - угроза/риск", callback_data=2)
        url_button2 = types.InlineKeyboardButton(text="3. Потребность - новая возможность", callback_data=3)
        url_button3 = types.InlineKeyboardButton(text="4. Потребность - угроза/риск", callback_data=4)
        url_button4 = types.InlineKeyboardButton(text="5. Прочее", callback_data=5)
        keyboard.add(url_button, url_button1, url_button2, url_button3, url_button4)
        bot.send_message(message.chat.id, "Для обратной связи следуйте подсказкам бота.", reply_markup=keyboard)
        config.name_waiting[config.users.index(message.chat.id)] = False
        config.waiting[config.users.index(message.chat.id)] = False
        config.path[config.users.index(message.chat.id)] = ''

    pass



if "a" == "a":
    bot.polling(none_stop=True)



