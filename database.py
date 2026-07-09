import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

conn.commit()


def save_user(name):
    cursor.execute(
        "INSERT INTO users(name) VALUES(?)",
        (name,)
    )
    conn.commit()


def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()