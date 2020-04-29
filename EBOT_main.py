from bs4 import BeautifulSoup
from threading import Thread
from datetime import date
import requests as re
import pickle
import telebot
import os
import time
import schedule


def store(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f, 2)


def fetch(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(FOLDER, "users", "users.json")
DATE_PATH = os.path.join(FOLDER, "users", "date_file.json")
DATA = fetch(DATA_PATH)
DATE = fetch(DATE_PATH)


# Сurrency search by specified filters
def view(charcode, date_req):

    if date_req in DATE:
        content = DATE[date_req]
    else:
        
        url = r"http://www.cbr.ru/scripts/XML_daily.asp?"
        response = re.get(url, params={"date_req": date_req})
        content = response.text
        DATE[date_req] = content
        store(DATE_PATH, DATE)

    soup = BeautifulSoup(content, 'lxml')

    for currency in soup.find_all("charcode"):
        if currency.text == charcode:
            return currency.parent.value.text


ebot = telebot.TeleBot("1245576989:AAHF9AnQ_lHQ0LaGnTrYUSmpA29aQGGJLN8")


# Send the description of the bot to the user
command_start = ["start"]
@ebot.message_handler(commands=command_start)
@ebot.edited_message_handler(commands=command_start)
def start_message(message):
    with open(os.path.join(FOLDER, "messages", "startmessage.txt"), "r", encoding="utf-8") as start_message_string:
        ebot.reply_to(message, start_message_string.read())
    DATA[message.from_user.id] = 'USD'
    store(DATA_PATH, DATA)


# The meaning of the commands with their description
command_help = ["help"]
@ebot.message_handler(commands=command_help)
@ebot.edited_message_handler(commands=command_help)
def help_message(message):
    with open(os.path.join(FOLDER, "messages", "help.txt"), "r", encoding="utf-8") as help_message_string:
        ebot.reply_to(message, help_message_string.read())


# Stop sending currency
command_start = ["stopsending"]
@ebot.message_handler(commands=command_start)
@ebot.edited_message_handler(commands=command_start)
def stop(message):
    id = message.from_user.id
    if id in DATA:
        DATA.pop(id)
        store(DATA_PATH, DATA)
        ebot.reply_to(message, "Вы отписались от рассылки. Отправьте мне /start и я снова буду присылать сообщения")
    else:
        ebot.reply_to(message, "Вы уже отписались от рассылки")


# Send list of all possible currencies, currency denomination and currency code
command_c_list = ["currencylist"]
@ebot.message_handler(commands=command_c_list)
@ebot.edited_message_handler(commands=command_c_list)
def currency_list_message(message):
    with open(os.path.join(FOLDER, "messages", "list_of_currencies.txt"), "r", encoding="utf-8") as currency_list:
        ebot.reply_to(message, currency_list.read())


# Send instructions to the user
command_set_c = ["setcurrency"]
@ebot.message_handler(commands=command_set_c)
@ebot.edited_message_handler(commands=command_set_c)
def set_currency(message):
    with open(os.path.join(FOLDER, "messages", "setcurrency_message.txt"), "r", encoding="utf-8") as set_currency_string:
        ebot.reply_to(message, set_currency_string.read())


# Send view() to user
command_view = ["view"]
@ebot.message_handler(commands=command_view)
@ebot.edited_message_handler(commands=command_view)
def view_message(message):
    id = message.from_user.id
    if id in DATA:
        charcode = DATA[id]
        reply_string = f'Текущий курс по {charcode} составляет {view(charcode, None)} руб.'
        ebot.reply_to(message, reply_string)
    else:
        ebot.reply_to(message, "Вы должны написать /start, для того, чтобы использовать эту функци")


# Recognize the currency code
reg_charcode = r"\b\w{3}\b"
@ebot.message_handler(regexp=reg_charcode)
@ebot.edited_message_handler(regexp=reg_charcode)
def currency_code_message(message):
    charcode = message.text
    if view(charcode, None):
        ebot.reply_to(message, f'Вы выбрали {charcode}.')
        DATA[message.from_user.id] = charcode
        store(DATA_PATH, DATA)
    else:
        ebot.reply_to(message, f'К сожалению {charcode} не существует. Возможно вам следует ознакомится с /currencylist')


# Recognize the desired data
reg_data = r'\d\d/\d\d/\d{4}'
@ebot.message_handler(regexp=reg_data)
@ebot.edited_message_handler(regexp=reg_data)
def data_message(message):
    id = message.from_user.id
    if id in DATA:
        charcode = DATA[id]
        date = message.text
        if view(charcode, date):
            ebot.reply_to(message, f'Курс на {date} по {charcode} составляет {view(charcode, date)} руб.')
        else:
            ebot.reply_to(message, f"К сожаллению у нас нет информации для {charcode} на {date}")
    else:
        ebot.reply_to(message, "Вы должны написать /start, для того, чтобы использовать эту функци")


def sendler(data_reg=None):
    if date_req is None:
        today = date.today()
        date_req = today.strftime("%d/%m/%Y")

    print(date_req)
    print('WE SEND')
    
    for id in DATA:
        charcode = DATA[id]
        ebot.send_message(id, f"Доброе утро! На сегодня курс по {charcode} составляет {view(charcode, data_reg)} руб.")


schedule.every().day.at("10:30").do(sendler)


def send():
    while True:
        schedule.run_pending()
        time.sleep(1)


t = Thread(target=send, name="Scheduling", daemon=True)
t.start()

ebot.polling()
