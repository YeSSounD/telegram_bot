from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
import sqlite3

# База данных для админов и статистики
def init_db():
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins 
                     (user_id INTEGER PRIMARY KEY, username TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats 
                     (user_id INTEGER, action TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав администратора")
        return
        
    keyboard = [
        ["/add_admin", "/list_admins"],
        ["/stats", "/broadcast"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Админ-панель:", reply_markup=reply_markup)

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Реализация добавления админа через reply или аргумент команды
    pass

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Показ статистики
    pass

def is_admin(user_id: int) -> bool:
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM admins WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def setup_admin_handlers(application):
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("add_admin", add_admin))
    application.add_handler(CommandHandler("stats", show_stats))

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Недостаточно прав")
        return

    try:
        new_admin_id = int(context.args[0])
        username = update.message.from_user.username
        
        conn = sqlite3.connect('bot_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO admins VALUES (?, ?)", 
                      (new_admin_id, username))
        conn.commit()
        conn.close()
        
        await update.message.reply_text(f"✅ Пользователь {username} добавлен в админы")
    except:
        await update.message.reply_text("Использование: /add_admin <user_id>")
        
async def log_action(user_id: int, action: str, details: str = ""):
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stats VALUES (?, ?, ?, datetime('now'))",
        (user_id, action, details)  # Теперь храним user_id, действие, детали и время
    )
    conn.commit()
    conn.close()

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
        
    conn = sqlite3.connect('bot_data.db')
    cursor = conn.cursor()
    
    # Статистика по командам
    cursor.execute("""SELECT action, COUNT(*) FROM stats 
                    GROUP BY action ORDER BY COUNT(*) DESC""")
    stats_text = "📊 Статистика:\n" + "\n".join(
        f"{row[0]}: {row[1]}" for row in cursor.fetchall()
    )
    
    # Количество админов
    cursor.execute("SELECT COUNT(*) FROM admins")
    stats_text += f"\n\n👑 Админов: {cursor.fetchone()[0]}"
    
    conn.close()
    await update.message.reply_text(stats_text)