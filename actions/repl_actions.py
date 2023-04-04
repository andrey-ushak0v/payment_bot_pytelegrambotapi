import sqlite3

from loger_conf import logger


def repl_to_db(message, pay_type, tg_id):
    try:
        logger.info(f'сохранение хэша пополнения у юзера {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO replenishment\
                (transaction_hash, payment_type, user_id)\
                  VALUES ('{message}', '{pay_type}', '{tg_id}');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'хэш юзера {tg_id} не сохранился {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def check_repl(tg_id, hhash):
    try:
        logger.info(f'получение последнего хэша \
                    оплаты юзера из бд с id - {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT transaction_hash FROM replenishment\
                  WHERE transaction_hash='{hhash}';"
            )
        record = cursor.fetchone()
        if record is None:
            return record
        return record[0]
    except sqlite3.Error as error:
        logger.error(f'ошибка получения хэша\
                      юзера из бд с id - {tg_id} {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()
