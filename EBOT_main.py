from bs4 import BeautifulSoup
import requests as re
import pickle
import telebot
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))
OPTIONS = ['USD', '']
with open(os.path.join(FOLDER, "users", "id.txt"), "rb") as id_file:
    USERS = set(pickle.load(id_file))

#Сurrency search by specified filters
def view(charcode, data_req):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?{data_req=}"
    response = re.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    for currency in soup.find_all("charcode"):
        if currency.text == charcode:
            return currency.parent.value.text

ebot = telebot.TeleBot("1245576989:AAHF9AnQ_lHQ0LaGnTrYUSmpA29aQGGJLN8")


#Send the description of the bot to the user
command_start = ["start"]
@ebot.message_handler(commands=command_start)
@ebot.edited_message_handler(commands=command_start)
def start_message(message):
    with open(os.path.join(FOLDER, "messages", "startmessage.txt"), "r", encoding="utf-8") as start_message_string:
        ebot.reply_to(message, start_message_string.read())
        USERS.add(message.from_user.id)
    with open(os.path.join(FOLDER, "users", "id.txt"), "wb") as id_file:
        pickle.dump(USERS, id_file, 2)

#Send list of all possible currencies, currency denomination and currency code
command_c_list = ["currencylist"]
@ebot.message_handler(commands=command_c_list)
@ebot.edited_message_handler(commands=command_c_list)
def currency_list_message(message):
    with open(os.path.join(FOLDER, "messages", "list_of_currencies.txt"), "r", encoding="utf-8") as currency_list:
        ebot.reply_to(message, currency_list.read())

#Send instructions to the user
command_set_c = ["setcurrency"]
@ebot.message_handler(commands=command_set_c)
@ebot.edited_message_handler(commands=command_set_c)
def set_currency(message):
    with open(os.path.join(FOLDER, "messages", "setcurrency_message.txt"), "r", encoding="utf-8") as set_currency_string:
        ebot.reply_to(message, set_currency_string.read())

#Send view() to user
command_view = ["view"]
@ebot.message_handler(commands=command_view)
@ebot.edited_message_handler(commands=command_view)
def view_message(message):
    charcode, data_reg = OPTIONS
    reply_string = f'Текущий курс по {charcode} составляет {view(charcode, data_reg)} руб.'
    ebot.reply_to(message, reply_string)

#Recognize the currency code
reg_charcode = r"\b\w{3}\b"
@ebot.message_handler(regexp=reg_charcode)
@ebot.edited_message_handler(regexp=reg_charcode)
def currency_code_message(message):
    charcode = message.text
    OPTIONS[0] = charcode
    ebot.reply_to(message, f'Вы выбрали {message.text}.')

#Recognize the desired data
reg_data = r'\d\d/\d\d/\d{4}'
@ebot.message_handler(regexp=reg_data)
@ebot.edited_message_handler(regexp=reg_data)
def data_message(message):
    data = message.text
    OPTIONS[2] = data
    ebot.reply_to(message, f'Вы установили {data}.')

def sendler():
    charcode, data_reg = OPTIONS
    for id in USERS:
        ebot.send_message(id, f"На сегодня курс по {charcode} составляет {view(charcode, data_reg)}рублей")

sendler()

print(USERS)
ebot.polling()