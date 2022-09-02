import telebot
import requests
import json


class ExchangeException(Exception):
    pass


TOKEN = "5630158132:AAE0WiU_GZYBkiruDl28Rt5vFbEaZOGFwFA"
bot = telebot.TeleBot(TOKEN)

currencies_dict = {
    'bitcoin': 'btc',
    'ethereum': 'eth',
    'dollar': 'usd',
    }


@bot.message_handler(commands=['start', 'help'])
def helps(message: telebot.types.Message):
    text = 'Follow the pattern to start: \namount currency-from currency-to'
    text1 = 'To get the list of available currencies: /currencies'
    bot.reply_to(message, f'{text}\n{text1}')


@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message):
    text = 'Enter for available currencies:'
    for c, n in currencies_dict.items():
        text = '\n'.join((text, f'{n} for {c}'))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def exchange(message: telebot.types.Message):
    mes = message.text.upper().split(' ')
    if len(mes) > 3:
        raise ExchangeException('Too many parameters - 3 expected')
    elif len(mes) < 3:
        raise ExchangeException('Not enough parameters - 3 expected')
    amount, from_cur, to_cur = mes
    try:
        amount = float(amount)
    except ValueError:
        raise ExchangeException('First parameter should be a number')
    if from_cur.lower() in currencies_dict.keys():
        from_cur = currencies_dict[from_cur.lower()].upper()
    if to_cur.lower() in currencies_dict.keys():
        to_cur = currencies_dict[to_cur.lower()].upper()
    if from_cur.lower() not in currencies_dict.values() or to_cur.lower() not in currencies_dict.values():
        raise ExchangeException('Entered currency is not available')
    if from_cur == to_cur:
        raise ExchangeException('Nothing to exchange - different currencies expected')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={from_cur}&tsyms={to_cur}')
    rate = json.loads(r.content)[to_cur]
    cost = amount * rate
    i = 2
    while round(cost, i) == 0:
        i += 1
    text = f'{amount} {from_cur} costs {round(cost, i + 3)} {to_cur}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
