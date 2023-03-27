import sqlite3


def repl_to_db(message, tg_id):
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO replenishment\
            (transaction_hash, user_id) VALUES ('{message}', '{tg_id}');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
