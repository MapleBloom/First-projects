from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
env_path = Path('./venv')/'settings.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

all_dict = {
    'btc': 'bitcoin',
    'eth': 'ethereum',
    'usd': 'dollar',
    'rur': 'ruble',
    'eur': 'euro',
    }
currency_list = ['rur', 'eur', 'usd']
crypto_list = ['btc', 'eth', 'usd']
