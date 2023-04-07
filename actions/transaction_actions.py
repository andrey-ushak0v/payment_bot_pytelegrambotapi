import sqlite3

from loger_conf import logger


def transaction_to_db(
        tr_id,
        tr_amount,
        tr_status,
        tr_type,
        id_card,
        ):
    try:
        logger.info(f'сохранение данных транзакции {tr_id} в бд')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO transactions \
                (transaction_id, transaction_amount,\
                      transaction_status, transaction_type,\
                          id_card) VALUES ('{tr_id}', '{tr_amount}',\
                              '{tr_status}', '{tr_type}', '{id_card}');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'данные транзакции {tr_id} не сохранились {error} ')
        return (f"Ошибка при работе с SQLite {error}")
    finally:
        if conn:
            conn.close()


def check_transaction_owner(card_id):
    try:
        logger.info(f'получение владельца карты юзера {card_id}')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT user_id FROM card WHERE card_id='{card_id}';"
            )
        record = cursor.fetchone()
        if record is None:
            return record
        return record[0]
    except sqlite3.Error as error:
        logger.error(f'ошибка получения владельца карты {card_id} {error}')
        return (f"Ошибка при работе с SQLite {error}")
    finally:
        if conn:
            conn.close()
