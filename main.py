# Done! Congratulations on your new bot. You will find it at t.me/skysmart_currency_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 5206778605:AAF1G-dYOWhNYVUhCHM8g9GpYVQp3yo2ePc
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
import os
import telebot
import requests
from bs4 import BeautifulSoup
# TOKEN = '5206778605:AAF1G-dYOWhNYVUhCHM8g9GpYVQp3yo2ePc'
TOKEN = os.environ.get('BOT_TOKEN')
keys = telebot.types.ReplyKeyboardMarkup(True, True)
keys.row('Курс USD', 'Курс EUR')
keys.row('Курс UAH', 'Курс GBP')
keys.row('Курс JPY', 'Курс CNY')
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, "Этот бот позволяет получить информацию о текущем курсе валют.")
    bot.send_message(message.chat.id, 'Выбери валюту: ', reply_markup=keys)
    # print(message.text)
@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Курс USD':
        value, date = get_currency('USD')
        bot.send_message(message.chat.id, f'Курс доллара: {value} рублей на {date}')
    elif message.text == 'Курс EUR':
        value, date = get_currency('EUR')
        bot.send_message(message.chat.id, f'Курс евро: {value} рублей на {date}')
    elif message.text == 'Курс UAH':
        value, date = get_currency('UAH')
        bot.send_message(message.chat.id, f'Курс гривны: {value} рублей на {date}')
    elif message.text == 'Курс JPY':
        value, date = get_currency('JPY')
        bot.send_message(message.chat.id, f'Курс японской йены: {value} рублей на {date}')
    elif message.text == 'Курс GBP':
        value, date = get_currency('GBP')
        bot.send_message(message.chat.id, f'Курс фунта стерлингов: {value} рублей на {date}')
    elif message.text == 'Курс CNY':
        value, date = get_currency('CNY')
        bot.send_message(message.chat.id, f'Курс китайского юаня: {value} рублей на {date}')
def parse(currency, html_text):
    pos = html_text.find(currency)
    if pos == -1:
        return 'Неизвестная валюта!'
    trpos = html_text.find('</tr>', pos)
    if trpos == -1:
        return 'Не найден tr'
    tdpos_end = html_text.rfind('</td>', pos, trpos)
    if tdpos_end == -1:
        return 'Не найден tdpos_end'
    tdpos_begin = html_text.rfind('>', pos, tdpos_end)
    if tdpos_begin == -1:
        return 'Не найден tdpos_begin'
    return html_text[tdpos_begin + 1: tdpos_end]


def get_currency(currency):
    r = requests.get('https://www.cbr.ru/currency_base/daily/')
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r, r.text)
    button = soup.find('button', {'class': 'datepicker-filter_button'}) 
    button_text = ''
    if button:
        button_text = button.text
    return parse(currency, r.text), button_text








bot.polling()
