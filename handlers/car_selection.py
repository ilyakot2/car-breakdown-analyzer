from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from states import *
from handlers import utils

async def ask_car_brand(update: Update, context: ContextTypes):
    cars = utils.load_cars()
    brands = [car['brand'] for car in cars]
    markup = ReplyKeyboardMarkup([[b] for b in brands], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выберите марку авто:", reply_markup=markup)
    return CAR_MODEL

async def ask_car_model(update: Update, context: ContextTypes):
    brand = update.message.text
    context.user_data['brand'] = brand
    cars = utils.load_cars()
    car_data = next((c for c in cars if c['brand'] == brand), None)
    if not car_data:
        await update.message.reply_text('Марка не найдена')
        return CAR_MODEL

    models = [m['model'] for m in car_data['models']]
    markup = ReplyKeyboardMarkup([[m] for m in models], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите модель:', reply_markup=markup)
    return CAR_SYSTEM

async def ask_car_system(update: Update, context: ContextTypes):
    model = update.message.text
    context.user_data["car_model"] = model
    
    faults_data = utils.load_faults()
    
    # Получаем все системы из faults_database
    systems = []
    for system_key, system_data in faults_data.items():
        if system_key not in ["emergency_levels", "diy_levels", "complexity_levels"]:
            systems.append(system_data['title'])
    
    markup = ReplyKeyboardMarkup([[s] for s in systems], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Вы выбрали: {context.user_data['brand']} {model}\n\n"
        "Выберите систему автомобиля:",
        reply_markup=markup
    )
    return SHOW_FAULTS

async def handle_system_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    system_title = update.message.text
    context.user_data["system"] = system_title
    
    faults_data = utils.load_faults()
    
    # Находим выбранную систему
    selected_system = None
    for system_key, system_data in faults_data.items():
        if system_key not in ["emergency_levels", "diy_levels", "complexity_levels"]:
            if system_data['title'] == system_title:
                selected_system = system_data
                break
    
    if not selected_system:
        await update.message.reply_text("Система не найдена")
        return SHOW_FAULTS
    
    # Сохраняем доступные неисправности в user_data
    context.user_data["available_faults"] = selected_system['issues']
    
    # Формируем список симптомов для отображения
    symptoms = [f"{i+1}. {issue['symptom']}" for i, issue in enumerate(selected_system['issues'])]
    await update.message.reply_text(
        f"🔧 {system_title} - возможные неисправности:\n\n" + 
        "\n".join(symptoms) +
        "\n\nНапишите номер неисправности (например: 1)"
    )
    return FAULT_CHOICE

async def handle_fault_choice(update: Update, context: ContextTypes):
    try:
        choice = int(update.message.text) - 1
        issues = context.user_data["available_faults"]
        selected = issues[choice]
        context.user_data['fault_id'] = selected['id']
        
        # Формируем подробное сообщение о неисправности
        brief = (
            f"🔍 **{selected['symptom']}**\n\n"
            f"**Возможные причины:**\n" + "\n".join(f"• {c}" for c in selected["causes"][:3]) + "\n\n"
            f"**Решение:**\n" + "\n".join(f"• {s}" for s in selected["solutions"][:3]) + "\n\n"
            f"**Срочность:** {selected['emergency']}\n"
            f"**Сложность ремонта:** {selected['complexity']}\n"
            f"**Можно сделать самому:** {selected['can_diy']}"
        )
        
        await update.message.reply_text(brief, parse_mode="Markdown")
        
    except (ValueError, IndexError):
        await update.message.reply_text('Неверный номер. Попробуйте снова.')
        return FAULT_CHOICE
    
    # Переходим к обратной связи
    from handlers.feedback_handler import start_feedback
    return await start_feedback(update, context)

