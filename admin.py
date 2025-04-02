from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import database


async def admin_panel(update: Update, context: CallbackContext) -> int:
    if update.effective_user.id not in ADMIN_IDS:
        return ConversationHandler.END

    buttons = [['Добавить вопрос'], ['Статистика']]
    await update.message.reply_text(
        "Админ-панель:",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    )
    return GET_QUESTION_TEXT if update.message.text == 'Добавить вопрос' else ConversationHandler.END


async def add_question_start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите текст вопроса:")
    return GET_QUESTION_TEXT


async def get_question_text(update: Update, context: CallbackContext) -> int:
    context.user_data['new_question'] = {'text': update.message.text}
    await update.message.reply_text("Введите варианты ответов через запятую:")
    return GET_QUESTION_OPTIONS


async def get_question_options(update: Update, context: CallbackContext) -> int:
    options = [opt.strip() for opt in update.message.text.split(',')]
    question_text = context.user_data['new_question']['text']

    database.add_question(question_text, options)
    await update.message.reply_text("Вопрос добавлен!")
    return ConversationHandler.END


async def show_stats(update: Update, context: CallbackContext) -> None:
    stats = database.get_stats()
    if not stats:
        await update.message.reply_text("Нет данных для отображения")
        return

    response = "Статистика:\n\n"
    current_question = None

    for row in stats:
        if row[0] != current_question:
            response += f"Вопрос: {row[1]}\n"
            current_question = row[0]
        if row[2]:
            response += f"- {row[2]}: {row[3]}\n"

    await update.message.reply_text(response)