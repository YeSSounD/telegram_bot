from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
   #Кнопки тестов
def get_gender_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚹 Мужской", callback_data="male"),
         InlineKeyboardButton("🚺 Женский", callback_data="female")],
        [InlineKeyboardButton("❌ Отменить", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_yes_no_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="yes"),
         InlineKeyboardButton("❌ Нет", callback_data="no")],
        [InlineKeyboardButton("↩️ Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_keyboard():
    """Клавиатура для админ-панели"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("📩 Рассылка", callback_data="broadcast")]
    ])