import requests

from config import WEBSCARD_TOKEN

WEBSCARD_HEADERS = {'Authorization': f'Bearer {WEBSCARD_TOKEN}'}


def get_card_info(endpoint):
    response = requests.get(
        endpoint,
        headers=WEBSCARD_HEADERS,
        )
    return response.json()
