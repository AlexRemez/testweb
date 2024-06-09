import sqlite3
DB_FILE = "app_db.db"
# Устанавливаем соединение с базой данных
connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

# Формируем часть SQL-запроса для полей Drill
drill_fields = ", ".join([f"Drill_{i} TEXT" for i in range(1, 438)])

# Создаем таблицу Users
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS Users (
tg_id INTEGER NOT NULL UNIQUE,
first_name TEXT,
username TEXT,
{drill_fields}
)
''')


def create_connection(db_file):
    """Создание подключения к базе данных SQLite"""

    conn = sqlite3.connect(db_file)
    return conn


def get_exercise_data(conn, exercise):
    """Получение данных по названию упражнения"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT first_name, {exercise} FROM Users WHERE {exercise} IS NOT NULL")
    rows = cursor.fetchall()
    return rows

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()