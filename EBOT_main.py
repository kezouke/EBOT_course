from bs4 import BeautifulSoup
import requests
import telebot

ebot = telebot.TeleBot("1245576989:AAHF9AnQ_lHQ0LaGnTrYUSmpA29aQGGJLN8")

@ebot.message_handler(commands=["start"])
def start_message(message):
    with open("startmessage.txt", "r", encoding="utf-8") as start_message_string:
        ebot.reply_to(message, start_message_string.read())


ebot.polling(timeout=60)

