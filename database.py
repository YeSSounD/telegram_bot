import sqlite3
from contextlib import closing

def init_db():
    """Инициализация базы данных"""
    with closing(sqlite3.connect('survey.db')) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            age INTEGER,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()