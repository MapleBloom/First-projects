import telebot

from config import *
from extentions import CryptoExchange, CryptoList


bot = telebot.TeleBot(TOKEN)   # Bot name Hi_Ululu


@bot.message_handler(commands=['start', 'help', ])
def helps(message: telebot.types.Message):
    text = 'Follow the pattern to get exchange rates: \n\namount  ticker-from  ticker-to\n\n' \
           'Get the available currency ticker list: \n /currency\n' \
           'Get the available crypto ticker list: \n /crypto'
    bot.reply_to(message, text)


@bot.message_handler(commands=['crypto', ])  # available crypto list
def cryptos(message: telebot.types.Message):
    bot.reply_to(message, CryptoList.list_available('crypto'))


@bot.message_handler(commands=['currency', ])  # available currency list
def currencies(message: telebot.types.Message):
    bot.reply_to(message, CryptoList.list_available('currency'))


@bot.message_handler(commands=['talk', ])  # just to talk
def talk(message: telebot.types.Message):
    text = f'Nice to hear you, dear {message.chat.username}, Ululu!\nWhats your favorite number?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, number_handler)


def number_handler(message: telebot.types.Message):
    num = int(message.text) * 11
    text = f'And mine is {str(num)[::-1]}, Ululu!\nWhats your favorite color?'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, color_handler, num)


def color_handler(message: telebot.types.Message, num):
    color = message.text.lower()
    text = f'Today is {color} day, Ululu!\nAnd I am tyred {num} times, bye!'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])  # currency converter
def exchange(message: telebot.types.Message):
    bot.send_message(message.chat.id, CryptoExchange.exchange(message))


bot.polling(none_stop=True)
