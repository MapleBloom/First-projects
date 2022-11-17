from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
env_path = Path('./venv')/'settings.env'
load_dotenv(dotenv_path=env_path)

DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
