import sqlite3

import requests
from conf import WEBSCARD_TOKEN


WEBSCARD_HEADERS = {'Authorization': f'Bearer {WEBSCARD_TOKEN}'}


def get_my_cards(tg_id):
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE user_id = {tg_id};")
        records = cursor.fetchone()
        return records
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()


def get_card_info(endpoint):
    response = requests.get(
        endpoint,
        headers=WEBSCARD_HEADERS,
        )
    return response.json()
