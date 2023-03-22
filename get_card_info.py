import requests
from config import WEBSCARD_TOKEN
WEBSCARD_HEADERS = {'Authorization': f'Bearer {WEBSCARD_TOKEN}'}

ENDPOINT_CARD_DETAIL = f'https://api.webscard.net/api/v1/cards/card/detail/sensitive?card_id='
def get_card_info(endpoint):
    response = requests.get(
        endpoint,
        headers=WEBSCARD_HEADERS,
        )
    return(response.json())




