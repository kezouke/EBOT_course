from bs4 import BeautifulSoup
import requests
import telebot

#<span class="DFlfde SwHCTb" data-precision="2" data-value="77.579">77,58</span>
url = "https://www.google.com/search?q=dollar+in+rubles"
headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

response = requests.get(url, headers=headers)
content = response.text
soup = BeautifulSoup(content, 'lxml')

value = soup.find('span', attrs={"class": "DFlfde SwHCTb", "data-precision": "2"})
if value:
    course = value.text
#We got the current dollar exchange rate in rubles

ebot = telebot.TeleBot("1245576989:AAHF9AnQ_lHQ0LaGnTrYUSmpA29aQGGJLN8")

@ebot.message_handler(commands=['start'])
def start_message(message):
    start_message_string = 'ну здарова!!!!!!!!!!!!\nМой создатель решил назвать меня "нефтяная игла", но я предпочитаю назвывать себя  EBOT.\nТакие вот дела....'
    ebot.send_message(message.chat.id, start_message_string)


ebot.polling()

