import telebot
from telebot import types
import requests as r
import os

API_KEY = os.environ.get('API_TOKEN')
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
currency = 'RUB'


def get_currency(API_KEY, currency: str):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}?"
    responce = r.get(url)
    data = responce.json()
    currency_dict = data['conversion_rates'].keys()
    return (data, currency_dict)


currency_dict = get_currency(API_KEY, currency)[1]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    currency_dict = get_currency(API_KEY, currency)[1]

    for cur in currency_dict:
        if cur != 'RUB':
            markup.add(types.InlineKeyboardButton(cur, callback_data=cur))
    # markup.add(types.InlineKeyboardButton("USD", callback_data="USD"))
    # markup.add(types.InlineKeyboardButton("EUR", callback_data="EUR"))
    # markup.add(types.InlineKeyboardButton("GBP", callback_data="GBP"))
    # markup.add(types.InlineKeyboardButton("JPY", callback_data="JPY"))
    # Добавьте больше валют, если необходимо

    bot.send_message(message.chat.id, "Выберите валюту:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    selected_currency = call.data
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currency}?"
    response = r.get(url)
    if response.status_code == 200:
        data = response.json()
        rates = data['conversion_rates']
        date = data['time_last_update_utc'].split(' +')[0]
        rate = rates.get(selected_currency, 'Неизвестная валюта')
        bot.send_message(call.message.chat.id,
                         f"Курс на {date}: {selected_currency}: {rate} к RUB")
    else:
        bot.send_message(call.message.chat.id, "Ошибка получения курса валют.")


bot.polling()
