import telebot
from telebot import types
import requests as r
import os
import time

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


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id, 'Вы выбираете валюту из списка. Мы пришлём Вам курс к рублю на дату')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    currency_dict = get_currency(API_KEY, currency)[1]

    for cur in currency_dict:
        if cur != 'RUB':
            markup.add(types.InlineKeyboardButton(cur, callback_data=cur))

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


def start_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(15)  # Задержка перед перезапуском


if __name__ == "__main__":
    start_bot()
