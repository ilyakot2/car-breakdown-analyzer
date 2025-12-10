from telegram import Update
from telegram.ext import ContextTypes
from .car_selection import ask_car_brand

async def start(update: Update, context: ContextTypes):
    await update.message.reply_text("Привет! Я помогу диагностировать неисправность вашего авто. 🛠️")
    return await ask_car_brand(update, context)
