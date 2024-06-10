import json
import random
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "app_db.db")
# Устанавливаем соединение с базой данных
# connection = sqlite3.connect(DB_FILE)
# cursor = connection.cursor()

# Формируем часть SQL-запроса для полей Drill
# drill_fields = ", ".join([f"Drill_{i} TEXT" for i in range(1, 438)])

# Создаем таблицу Users
# cursor.execute(f'''
# CREATE TABLE IF NOT EXISTS Users (
# tg_id INTEGER NOT NULL UNIQUE,
# first_name TEXT,
# username TEXT,
# global_points INTEGER,
# {drill_fields}
# )
# ''')

# Выполняем запрос ALTER TABLE
# try:
#     cursor.execute("ALTER TABLE Users ADD COLUMN global_points INTEGER;")
#     connection.commit()
#     print("Новый столбец успешно добавлен.")
# except sqlite3.OperationalError as e:
#     print("Ошибка:", e)


def create_connection(db_file=DB_FILE):
    """Создание подключения к базе данных SQLite"""

    conn = sqlite3.connect(db_file)
    return conn


def get_columns():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(Users)')
        columns = [row[1] for row in cursor.fetchall()]
        return columns


def add_columns(new_columns):
    with create_connection() as conn:
        cursor = conn.cursor()
        for column in new_columns:
            cursor.execute(f'ALTER TABLE Users ADD COLUMN {column} TEXT')
        conn.commit()


def get_user(tg_id):
    with create_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE tg_id = ?', (tg_id,))
        user = cursor.fetchone()
        if user:
            return user
        return None


def add_user(tg_id, first_name=None, username=None):
    with create_connection(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Users (tg_id, first_name, username)
        VALUES (?, ?, ?)
        ''', (tg_id, first_name, username))
        conn.commit()


def update_user(tg_id, first_name=None, username=None, global_points=None, data=None):
    with create_connection() as conn:
        cursor = conn.cursor()
        updates = []
        params = []

        if first_name is not None:
            updates.append("first_name = ?")
            params.append(first_name)
        if username is not None:
            updates.append("username = ?")
            params.append(username)
        if global_points is not None:
            updates.append("global_points = ?")
            params.append(global_points)

        if data is not None:
            for key, value in data.items():
                updates.append(f"{key} = ?")
                params.append(value)

        params.append(tg_id)
        query = f"UPDATE Users SET {', '.join(updates)} WHERE tg_id = ?"
        cursor.execute(query, params)
        # try:
        #     cursor.execute(query, params)
        # except sqlite3.OperationalError:
        #     return False
        conn.commit()
        return True


def delete_user(tg_id):
    with create_connection(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Users WHERE tg_id = ?', (tg_id,))
        conn.commit()


def get_exercise_data(conn, exercise):
    """Получение данных по названию упражнения"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT first_name, {exercise} FROM Users WHERE {exercise} IS NOT NULL ORDER BY {exercise} DESC ")
    rows = cursor.fetchall()
    return rows
