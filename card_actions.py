import sqlite3


import requests
from conf import WEBSCARD_TOKEN
from loger_conf import logger

WEBSCARD_HEADERS = {'Authorization': f'Bearer {WEBSCARD_TOKEN}'}


def get_my_cards(tg_id):
    try:
        logger.info(f'получение карты bp бд юзером {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE user_id = {tg_id};")
        records = cursor.fetchone()
        return records
    except sqlite3.Error as error:
        logger.error(f'юзер {tg_id} не получил карту из бд {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def get_card_info(endpoint):
    try:
        response = requests.get(
            endpoint,
            headers=WEBSCARD_HEADERS,
            )
        if response.status_code != 200:
            logger.error('ошибка эндпоинта')
            raise Exception('Эндпоинт недоступен')
        return response.json()
    except requests.exceptions.RequestException:
        logger.error('сетевая ошибка')
        raise Exception('ошибка сети', exc_info=True)
