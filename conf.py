import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
WEBSCARD_TOKEN = str(os.getenv('WEBSCARD_TOKEN'))
ENDPOINT_CARD_DETAIL = str(os.getenv('ENDPOINT_CARD_DETAIL'))
ENDPOINT_CARD_BALANCE = str(os.getenv('ENDPOINT_CARD_BALANCE'))
