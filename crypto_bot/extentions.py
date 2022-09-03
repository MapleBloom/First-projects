import telebot
import requests
import json
from config import crypto_list, currency_list, all_dict


class ExchangeException(Exception):
    pass


class CryptoList:
    @staticmethod
    def list_available(c_type: str) -> str:
        # Return list of available tickers
        c_list = []
        if c_type == 'crypto':
            c_list = crypto_list
        elif c_type == 'currency':
            c_list = currency_list
        text = f'Enter for available {c_type}:'
        for c in c_list:
            text = '\n'.join((text, f'{c} for {all_dict[c]}'))
        return text


class Precision:
    @staticmethod
    def adjust_precision(c: float) -> str:
        # If c is too small adjust precision
        p = 2
        while round(c, p - 2) == 0:
            p += 1
        return f'{c:.{p}f}'


class CryptoExchange:
    @staticmethod
    def get_crypto_rate(a: float, from_c: str, to_c: str) -> str:
        # Take exchange rates for crypto from API
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?'
                         f'fsym={from_c.upper()}&tsyms={to_c.upper()}')
        rate = json.loads(r.content)[to_c.upper()]
        cost = a * rate
        return f'{a} {from_c} costs {Precision.adjust_precision(cost)} {to_c}'

    @staticmethod
    def get_curr_rate(a: float, from_c: str, to_c: str) -> str:
        # Take exchange rates for currency from API
        r = requests.get(f'https://www.cbr-xml-daily.ru/daily_json.js')
        rates = json.loads(r.content)
        from_r = 1 if from_c == 'rur' else rates['Valute'][from_c.upper()]['Value']
        to_r = 1 if to_c == 'rur' else rates['Valute'][to_c.upper()]['Value']
        cost = a * from_r / to_r
        return f'{a} {from_c} costs {Precision.adjust_precision(cost)} {to_c}'

    @staticmethod
    def exchange(message: telebot.types.Message) -> str:
        mes = message.text.lower().split()
        # Get amount and currencies from message, return decision or exceptions
        try:
            if len(mes) > 3:
                raise ExchangeException('Too many parameters - 3 expected')
            elif len(mes) < 3:
                raise ExchangeException('Not enough parameters - 3 expected')
            amount, from_cur, to_cur = mes
            try:
                amount = float(amount.replace(',', '.'))
            except ValueError:
                raise ExchangeException('First parameter should be a number')
            # Abbreviate to ticker in case of full currency name
            if from_cur in all_dict.values():
                from_cur = [c for c, v in all_dict.items() if v == from_cur][0]
            if to_cur in all_dict.values():
                to_cur = [c for c, v in all_dict.items() if v == to_cur][0]
            if from_cur == to_cur:
                raise ExchangeException('Nothing to exchange - different currencies expected')
            # Work with crypto or with currency
            if from_cur in crypto_list:
                if to_cur in crypto_list:
                    return CryptoExchange.get_crypto_rate(amount, from_cur, to_cur)
                elif from_cur != 'usd':
                    raise ExchangeException(f'Entered crypto "{to_cur}" is not available')
            if from_cur in currency_list:
                if to_cur in currency_list:
                    return CryptoExchange.get_curr_rate(amount, from_cur, to_cur)
                else:
                    raise ExchangeException(f'Entered currency {to_cur} is not available')
            else:
                raise ExchangeException(f'Entered ticker "{from_cur}" is not available')
        except ExchangeException as e:
            return f'{e}\nTry once more'
        except Exception as e:
            return f'Something goes wrong\n{e}\nTry a bit later'
