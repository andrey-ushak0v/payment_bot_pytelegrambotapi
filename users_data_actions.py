import sqlite3

from loger_conf import logger


def user_name_to_db(name, tg_id):
    try:
        logger.info(f'добавление имени \
                    {name} из пспорта от юзера {tg_id} в бд')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO pasport_name\
                  (p_name, user_id) VALUES ('{name}', {tg_id});")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ошибка добавления имени юзера {tg_id} в бд {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()


def user_p_num_to_db(p_number, tg_id):
    try:
        logger.info(f'добавление номера паспорта\
                     {p_number} из пспорта от юзера {tg_id} в бд')
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO pasport_number\
                  (p_number, user_id) VALUES ({p_number}, {tg_id});")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ошибка добавления поспорта юзера {tg_id} в бд {error}')
        return ("Ошибка при работе с SQLite")
    finally:
        if conn:
            conn.close()
    



