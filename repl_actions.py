import sqlite3

from loger_conf import logger


def repl_to_db(message, tg_id):
    try:
        logger.info(f'сохранение хэша пополнения у юзера {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO replenishment\
            (transaction_hash, user_id) VALUES ('{message}', '{tg_id}');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'хэш юзера {tg_id} не сохранился {error}  ')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()
