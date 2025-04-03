import sqlite3

conn = sqlite3.connect('bot_data.db')
cursor = conn.cursor()
cursor.execute("INSERT OR IGNORE INTO admins VALUES (?, ?)", 
              (ВАШ_TELEGRAM_ID, "ВАШ_НИК"))
conn.commit()
conn.close()
print("Первый админ добавлен!")