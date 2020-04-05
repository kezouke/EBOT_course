from bs4 import BeautifulSoup
import requests as re
import telebot

options = ['USD', '']

def view(charcode, data_req):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?{data_req=}"
    response = re.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')

    for currency in soup.find_all("CharCode"):
        if currency.text == charcode:
            return currency.parent.value.text

ebot = telebot.TeleBot("1245576989:AAHF9AnQ_lHQ0LaGnTrYUSmpA29aQGGJLN8")
@ebot.message_handler(commands=["start"])
def start_message(message):
    with open("startmessage.txt", "r", encoding="utf-8") as start_message_string:
        ebot.reply_to(message, start_message_string.read())

@ebot.message_handler(commands=["currencylist"])
def currency_list_message(message):
    with open("list_of_currencies.txt", "r", encoding="utf-8") as currency_list:
        ebot.reply_to(message, currency_list.read())

@ebot.message_handler(commands=["setcurrency"])
def set_currency(message):
    with open("setcurrency_message.txt", "r", encoding="utf-8") as set_currency_string:
        ebot.reply_to(message, set_currency_string.read())

@ebot.message_handler(regexp=r"\b\w{3}\b")
def currency_code_message(message):
    charcode = message.text
    options.append(charcode)
    data_string = "Вы можете отправить интересующую вас дату при желании(по умолчанию стоит сегодняшняя дата).\nДля этого отправьте дату в формате ДД/ММ/ГГГГ"
    ebot.reply_to(message, f'Вы выбрали {message.text}.' + data_string)

@ebot.message_handler(regexp=r'\d\d/\d\d/\d{4}')
def data_message(message):
    data = message.text
    options.append(data)
    ebot.reply_to(message, f'Вы установили {data}.')


ebot.polling()