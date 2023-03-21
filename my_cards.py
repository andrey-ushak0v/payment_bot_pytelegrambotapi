#import requests

import sqlite3

def get_my_cards() -> list:
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM card;")
        records =  cursor.fetchall()
        result = []
        for record in records:
            info = f'id вашей карты {record[2]} - {record[0]}'
            result.append(info)
        return result
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
#print(get_my_cards())

