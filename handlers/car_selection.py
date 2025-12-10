from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from states import CAR_MODEL, SHOW_FAULTS, FEEDBACK_HELPFUL
from handlers import utils

async def ask_car_brand(update: Update, context: ContextTypes):
    cars = utils.load_cars()
    brands = [car['brand'] for car in cars]
    markup = ReplyKeyboardMarkup([[b] for b in brands], one_time_keyboard=True,resize_keyboard=True)
    await update.message.reply_text("Выберите марку авто:", reply_markup=markup)
    return CAR_MODEL

async def ask_car_model(update: Update, context: ContextTypes):
    brand = update.message.text
    context.user_data['brand'] = brand
    cars = utils.load_cars()
    car_data = next((c for c in cars if c['brand'] == brand), None)
    if not car_data:
        await update.message.reply_text('Марка не найдена')
        return await ask_car_model(update, context)

    models = [m['model'] for m in car_data['models']]
    markup = ReplyKeyboardMarkup([[m] for m in models], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите модель:', reply_markup=markup)
    return SHOW_FAULTS


async def handle_fault_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    model = update.message.text
    context.user_data["car_model"] = model

    faults_data = utils.load_faults()
    engine_issues = faults_data["engine_system"]["issues"]
    context.user_data["available_faults"] = engine_issues

    symptoms = [f"{i+1}. {issue['symptom']}" for i, issue in enumerate(engine_issues)]
    await update.message.reply_text(
        "Выберите неисправность:\n" + "\n".join(symptoms) +
        "\n\nНапишите номер (например, 1)."
    )
    return SHOW_FAULTS

async def handle_fault_choice(update: Update, context: ContextTypes):
    try:
        choice = int(update.message.text) - 1
        issues = context.user_data["available_faults"]
        selected = issues[choice]
        context.user_data['fault_id'] = selected['id']
    except (ValueError, IndexError):
        await update.message.reply_text('Неверный номер. Попробуйте снова.')
        return SHOW_FAULTS

    brief = f"❗️ {selected['symptom']}\n\nРешение:\n" + "\n".join(f"• {s}" for s in selected["solutions"][:2])
    await update.message.reply_text(brief)

    from feedback_handler import start_feedback
    return await start_feedback(update, context)


