

import sqlite3

def get_my_cards() -> list:
    try:
        
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM card;")
        records =  cursor.fetchall()
        return records
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()

#print(get_my_cards())


