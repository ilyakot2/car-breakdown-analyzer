from telegram import Update
from telegram.ext import ContextTypes
from states import CAR_BRAND

async def start(update: Update, context: ContextTypes):
    context.user_data.clear()
    await update.message.reply_text("Привет! Я помогу диагностировать неисправность вашего авто. 🛠")
    
    from handlers.car_selection import ask_car_brand
    return await ask_car_brand(update, context)

