from config import BOT_TOKEN, ADMIN_IDS

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверяем, что команду вызвал админ"""
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("👨‍💻 Добро пожаловать в админ-панель!")
    else:
        await update.message.reply_text("⛔ У вас нет прав доступа!")