import sqlite3

from loger_conf import logger


def user_to_db(tg_id):
    try:
        logger.info(f'добавление юзера {tg_id} в бд')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO bot_user\
                  (telegram_id, user_status) VALUES ({tg_id}, 'new_user');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ошибка добавления юзера {tg_id} в бд {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def check_user(tg_id):
    try:
        logger.info(f'получение id юзера из бд с id - {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT telegram_id FROM bot_user WHERE telegram_id={tg_id};"
            )
        record = cursor.fetchone()
        if record is None:
            return record
        return record[0]
    except sqlite3.Error as error:
        logger.error(f'ошибка получения id юзера из бд с id - {tg_id} {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def check_status(tg_id):
    try:
        logger.info(f'получение статуса у юзера {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT user_status FROM bot_user WHERE telegram_id={tg_id};"
            )
        record = cursor.fetchone()
        if record is None:
            return record
        return record[0]
    except sqlite3.Error as error:
        logger.error(f'ошибка получения статуса у юзера {tg_id} {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def update_status(tg_id, status):
    try:
        logger.info(f'изменение статуса у юзера {tg_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE bot_user SET\
                user_status='{status}' WHERE telegram_id='{tg_id}'")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.info(f' ошибка изменения статуса у юзера {tg_id} {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()
