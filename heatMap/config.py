import os

from dotenv import load_dotenv


load_dotenv()

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
WS_HOST = os.getenv('WS_HOST')
HOST = os.getenv('HOST')
