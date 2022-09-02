import telebot
from config import TOKEN
from extentions import CryptoExchange, CryptoList


bot = telebot.TeleBot(TOKEN)   # Bot name Hi_Ululu


@bot.message_handler(commands=['start', 'help', ])
def helps(message: telebot.types.Message):
    text = 'Follow the pattern to get exchange rates: \namount ticker-from ticker-to\n' \
           'Get the available currency ticker list: \n /currency\n' \
           'Get the available crypto ticker list: \n /crypto'
    bot.reply_to(message, text)


@bot.message_handler(commands=['crypto', ])  # available crypto list
def cryptos(message: telebot.types.Message):
    bot.reply_to(message, CryptoList.list_available('crypto'))


@bot.message_handler(commands=['currency', ])  # available currency list
def currencies(message: telebot.types.Message):
    bot.reply_to(message, CryptoList.list_available('currency'))


@bot.message_handler(content_types=['text', ])  # currency converter
def exchange(message: telebot.types.Message):
    bot.send_message(message.chat.id, CryptoExchange.exchange(message))


bot.polling(none_stop=True)
