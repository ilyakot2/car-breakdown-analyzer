from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv
import os

from db_system.config import global_init
from handlers.start_handler import start
from handlers.car_selection import ask_car_brand, ask_car_model, ask_car_system, handle_system_selection, handle_fault_choice
from handlers.feedback_handler import handle_helpful, handle_accurate, handle_comment, skip_comment
from states import *

load_dotenv()

def main():
    global_init('feedback_db')

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Ошибка: BOT_TOKEN не задан в .env")

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
       	    states={
       	    CAR_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_brand)],
       	    CAR_MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_model)],
       	    CAR_SYSTEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_car_system)],
       	    SHOW_FAULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_system_selection)],
       	    FAULT_CHOICE: [MessageHandler(filters.Regex(r'^\d+$'), handle_fault_choice)],
       	    FEEDBACK_HELPFUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_helpful)],
            FEEDBACK_ACCURATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_accurate)],
            FEEDBACK_COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment),
                CommandHandler("skip", skip_comment)
            ],
        },
        fallbacks=[CommandHandler("start", start)],  # Добавляем возможность перезапуска
    )


    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()

