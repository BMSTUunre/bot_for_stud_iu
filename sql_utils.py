from os import getenv
from dotenv import load_dotenv
import  sqlite3


load_dotenv(dotenv_path=".env")
DATA_BASE_PATH = getenv('DATA_BASE_PATH')  # берем api токен из .env


def check_user_in_bd(tg_user_id: int):
    """
    Просто лезет в БД и тырит строки, где tg_user_id подходит
    """
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()

            cursor.execute(f'''SELECT * FROM users WHERE tg_user_id = {tg_user_id}''')
            records = cursor.fetchall()

        return records

    except Exception as exp:
        print(exp)
        return exp


def user_by_user_name(user_name: str):
    """
        Просто лезет в БД и тырит строки, где user_name подходит
    """
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()

            cursor.execute(f"""SELECT * FROM users WHERE user_name = '{user_name}'""")
            records = cursor.fetchall()

        return records

    except Exception as exp:
        print(exp)
        return exp


def check_history_in_db(tg_user_id: int):
    """
        Просто лезет в БД и тырит строки, где tg_user_id совпадает
    """
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()

            cursor.execute(f'''SELECT * FROM points_history WHERE tg_user_id = {tg_user_id}''')
            records = cursor.fetchall()

        return records

    except Exception as exp:
        print(exp)
        return exp


def add_user_in_db(tg_user_id: int, tg_username: str, user_name: str, user_group: str):
    """
            Просто лезет в БД и добавляет нового пользователя
    """
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()
            cursor.execute(f'''INSERT INTO users VAlUES 
            ({tg_user_id}, '{tg_username}', '{user_name}', '{user_group}', 0, 0, 0)''')

    except Exception as exp:
        print(exp)
        return exp


def make_user_admin(tg_user_id: int):
    """
        Просто лезет в БД и дает пользователю права админа
    """
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()
            cursor.execute(f''' UPDATE users SET is_admin = 1 WHERE tg_user_id = {tg_user_id}''')

    except Exception as exp:
        print(exp)
        return exp


def add_points_to_user(tg_member_id: int, tech_points_delta: int, art_points_delta: int,
                       tg_admin_name: str, datetime: str):
    try:
        with sqlite3.connect(DATA_BASE_PATH) as connect:
            cursor = connect.cursor()

            cursor.execute(f'''SELECT tech_points, art_points FROM users WHERE tg_user_id = {tg_member_id}''')
            records = cursor.fetchall()

            tech, art = records[0][0] + tech_points_delta, records[0][1] + art_points_delta

            cursor.execute(f'''UPDATE users SET tech_points = {tech}, art_points = {art} WHERE tg_user_id = {tg_member_id}''')
            cursor.execute(f"""INSERT INTO points_history VAlUES 
                            ({tg_member_id}, {tech_points_delta}, {art_points_delta}, '@{tg_admin_name}', '{datetime}')""")

    except Exception as exp:
        print(exp)
        return exp


if __name__ == '__main__':
    with sqlite3.connect(DATA_BASE_PATH) as connect:
        cursor = connect.cursor()
        # CREATE TABLE users (tg_user_id INTEGER, tg_username TEXT, user_name TEXT, user_group TEXT, tech_points INTEGER, art_points INTEGER, is_admin INTEGER)
        # CREATE TABLE points_history (tg_user_id INTEGER, tech_points_delta INTEGER, art_points_delta INTEGER, admin_tg_username TEXT, datetime TEXT)


        # INSERT INTO users VAlUES (1, 'a', 'А А', 'ИУ0-00', 0, 0, 0)
        # SELECT * FROM points_history WHERE tg_user_id = 1
        # DELETE FROM users WHERE tg_user_id = 321138226
        # cursor.execute('DELETE FROM users WHERE tg_user_id = 321138226')
        cursor.execute("DELETE FROM points_history")

