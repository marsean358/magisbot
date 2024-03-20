import sqlite3


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# SQL запрос для удаления таблицы
table_name = 'users'
query = f'DROP TABLE IF EXISTS {table_name}'

# Выполняем запрос
cursor.execute(query)
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, login TEXT, password TEXT)")
# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()