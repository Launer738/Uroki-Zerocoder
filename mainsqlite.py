import sqlite3
import os

# Путь к базе рядом с этим скриптом (чтобы example.db всегда был в папке проекта)
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "example.db")

# Подключение к базе (файл создаётся, если его нет)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создание простой таблицы
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
""")

# Вставка одной записи
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Иван", 25))

# Добавить ещё одну запись (просто ещё один execute с другими данными)
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Мария", 30))

# Добавить несколько записей сразу (executemany)
cursor.executemany(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    [("Петр", 22), ("Анна", 28), ("Сергей", 35)]
)

# Сохранение изменений
conn.commit()

# Чтение данных
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print(f"Записей в таблице: {len(rows)}")
for row in rows:
    print(row)

conn.close()
print("Готово. База:", db_path)
