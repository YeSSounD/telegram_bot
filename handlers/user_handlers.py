from config import BOT_TOKEN, ADMIN_IDS


from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    Application
)
from telegram.constants import ParseMode
from utils.keyboards import get_gender_keyboard, get_yes_no_keyboard 
# Состояния ConversationHandler
AGE, GENDER, Q1, Q2 = range(4)  # Добавили Q1 и Q2

# Сначала объявляем все асинхронные функции
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text("👋 Привет! Используй /survey для опроса")

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало опроса"""
    await update.message.reply_text(
        "📝 Опрос начался!\n\n"
        "1. Введите ваш возраст (12-100):"
    )
    return AGE

async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка возраста"""
    try:
        age = int(update.message.text)
        if not 12 <= age <= 100:
            raise ValueError
            
        context.user_data['age'] = age
        await update.message.reply_text(
            "2. Выберите ваш пол:",
            reply_markup=get_gender_keyboard()
        )
        return GENDER
        
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите корректный возраст (12-100)")
        return AGE


async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "cancel":
        await query.edit_message_text("Опрос отменен")
        return ConversationHandler.END
    
    context.user_data['gender'] = "Мужской" if query.data == "male" else "Женский"
    
    # Переходим к первому новому вопросу
    await query.edit_message_text(
        "❄️ Вопрос 1/2:\n"
        "Можно ли включать кондиционер зимой?",
        reply_markup=get_yes_no_keyboard()
    )
    return Q1  # Переходим к следующему состоянию


async def handle_question1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "back":
        # Возврат к предыдущему вопросу
        await query.edit_message_text(
            "2. Выберите ваш пол:",
            reply_markup=get_gender_keyboard()
        )
        return GENDER
    
    context.user_data['q1'] = query.data == "yes"  # Сохраняем ответ (True/False)
    
    await query.edit_message_text(
        "🌬️ Вопрос 2/2:\n"
        "В кабинете душно, появится ли свежий воздух если включить кондиционер?",
        reply_markup=get_yes_no_keyboard()
    )
    return Q2

async def handle_question2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "back":
        await query.edit_message_text(
            "❄️ Вопрос 1/2:\nМожно ли включать кондиционер зимой?",
            reply_markup=get_yes_no_keyboard()
        )
        return Q1
    
    # Сохраняем ответ
    context.user_data['q2'] = query.data == "yes"
    
    # Формируем сообщение для пользователя
    await query.edit_message_text(
        "✅ Спасибо! Ваши ответы отправлены администратору",
        reply_markup=None
    )
    
    # Формируем сообщение для админа
    answers = {
        'yes': '✅ Да',
        'no': '❌ Нет'
    }
    
    admin_message = (
        "📊 <b>Новые ответы:</b>\n\n"
        f"👤 Пользователь: @{query.from_user.username or 'без username'}\n"
        f"🆔 ID: {query.from_user.id}\n\n"
        f"▪️ Возраст: {context.user_data['age']}\n"
        f"▪️ Пол: {context.user_data['gender']}\n"
        f"▪️ Кондиционер зимой: {answers['yes' if context.user_data['q1'] else 'no']}\n"
        f"▪️ Свежий воздух: {answers['yes' if context.user_data['q2'] else 'no']}"
    )
    
    # Отправляем сообщение админу
    for admin_id in Config.ADMIN_IDS:
        await context.bot.send_message(
            chat_id=admin_id,
            text=admin_message,
            parse_mode="HTML"
    )
    
    # Отправляем сообщение всем админам
    for admin_id in Config.ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message,
                parse_mode="HTML"
            )
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение админу {admin_id}: {e}")
    
    return ConversationHandler.END


# Затем объявляем функцию setup
def setup_user_handlers(application: Application):
    application.add_handler(CommandHandler("start", start))
    
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('survey', start_survey)],
            states={
                AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)],
                GENDER: [CallbackQueryHandler(handle_gender)],
                Q1: [CallbackQueryHandler(handle_question1)],
                Q2: [CallbackQueryHandler(handle_question2)]
            },
            fallbacks=[],
            per_message=False
        )
    )