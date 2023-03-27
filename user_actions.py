import sqlite3


def user_to_db(tg_id):
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO bot_user\
                  (telegram_id, user_status) VALUES ({tg_id}, 'new_user');")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()


def check_user(tg_id):
    try:
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
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()


def check_status(tg_id):
    try:
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
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()


def update_status(tg_id):
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE bot_user SET\
                user_status='has_card' WHERE telegram_id='{tg_id}'")
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
