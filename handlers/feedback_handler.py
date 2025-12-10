from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from db_system.config import create_session
from db_system.models import Feedback
from states import *


async def start_feedback(update: Update, context: ContextTypes):
    await update.message.reply_text(
        "❓ Помогло ли решение?",
        reply_markup=ReplyKeyboardMarkup([["✅ Да", "❌ Нет"]], one_time_keyboard=True, resize_keyboard=True)
    )
    return FEEDBACK_HELPFUL

async def handle_helpful(update: Update, context: ContextTypes):
    context.user_data["was_helpful"] = (update.message.text == "✅ Да")
    await update.message.reply_text(
        "🔍 Симптом описан точно?",
        reply_markup=ReplyKeyboardMarkup([["✅ Да", "❌ Нет"]], one_time_keyboard=True, resize_keyboard=True)
    )
    return FEEDBACK_ACCURATE

async def handle_accurate(update: Update, context: ContextTypes):
    context.user_data["symptom_accurate"] = (update.message.text == "✅ Да")
    await update.message.reply_text(
        "💬 Оставьте комментарий или нажмите /skip",
        reply_markup=ReplyKeyboardRemove()
    )
    return FEEDBACK_COMMENT

async def handle_comment(update: Update, context: ContextTypes):
    context.user_data["comment"] = update.message.text
    await save_and_finish(update, context)
    return FEEDBACK_COMMENT

async def skip_comment(update: Update, context: ContextTypes):
    context.user_data["comment"] = None
    await save_and_finish(update, context)
    return FEEDBACK_COMMENT

async def save_and_finish(update: Update, context: ContextTypes):
    session = create_session()
    try:
        feedback = Feedback(
            user_id=update.effective_user.id,
            fault_id=context.user_data.get("fault_id"),
            car_brand=context.user_data.get("car_brand"),
            car_model=context.user_data.get("car_model"),
            was_helpful=context.user_data.get("was_helpful"),
            symptom_accurate=context.user_data.get("symptom_accurate"),
            comment=context.user_data.get("comment")
        )
        session.add(feedback)
        session.commit()
        await  update.message.reply_text('Спасибо за отзыв! 🙏')
    except Exception as e:
        session.rollback()
        await update.message.reply_text('Ошибка сохранения')
    finally:
        session.close()
