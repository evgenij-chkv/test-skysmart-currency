import os
import telebot
import requests
from bs4 import BeautifulSoup
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
    s = requests.Session()
    s.headers = {
        'cookie': 'swp_token=1529318441:da348e5038f36f4e22e839d6e317852a:c8fe351689c07b18b38cf1bb7e6604ff',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    r = s.get('https://www.cbr.ru/currency_base/daily/')
    soup = BeautifulSoup(r.text, 'html.parser')
    button = soup.find('button', {'class': 'datepicker-filter_button'}) 
    button_text = ''
    if button:
        button_text = button.text
    return parse(currency, r.text), button_text








bot.polling()
