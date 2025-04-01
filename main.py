import telebot
from telebot import types

TOKEN = "7716499994:AAEhPROF0AxgMpXAaTG1i9cucYTNDTOWoxM"
ADMIN_ID = "1226264539"

bot = telebot.TeleBot(TOKEN)
user_data = {}

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📍 Manzil")
    btn2 = types.KeyboardButton("🗉 Vakansiya")
    markup.add(btn1, btn2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    text = "Bu botda siz Istanbul 24 open marketiga ishga joylashish uchun ariza topshirasiz."
    bot.send_message(message.chat.id, text, reply_markup=start_menu())

@bot.message_handler(func=lambda message: message.text == "🗉 Vakansiya")
def show_vacancies(message):
    text = "Vakansiya ma'lumotlari..."
    bot.send_message(message.chat.id, text)
    ask_position(message)

def ask_position(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Sotuvchi", "Kassir", "Farrosh", "Yuk tushuruvchi"]
    for btn in buttons:
        markup.add(types.KeyboardButton(btn))
    bot.send_message(message.chat.id, "Qaysi lavozimda ishlashni xohlaysiz?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_job_type)

def ask_job_type(message):
    user_data[message.chat.id] = {"lavozim": message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Doimiy", "Vaqtinchalik")
    bot.send_message(message.chat.id, "Siz qanday ish izlayapsiz?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_schedule)

def ask_schedule(message):
    user_data[message.chat.id]["ish_turi"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("08:00-20:00", "20:00-08:00", "Kelishib olamiz")
    bot.send_message(message.chat.id, "Qaysi ish grafigida ishlashni xohlaysiz?", reply_markup=markup)
    bot.register_next_step_handler(message, ask_gender)

def ask_gender(message):
    user_data[message.chat.id]["ish_grafik"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Erkak", "Ayol")
    bot.send_message(message.chat.id, "Jinsingizni tanlang:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    user_data[message.chat.id]["jins"] = message.text
    bot.send_message(message.chat.id, "Ism, familiyangizni kiriting:")
    bot.register_next_step_handler(message, ask_phone)

def ask_phone(message):
    user_data[message.chat.id]["fio"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)
    markup.add(button)
    bot.send_message(message.chat.id, "Telefon raqamingizni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(message, ask_photo)

def ask_photo(message):
    if message.contact:
        user_data[message.chat.id]["telefon"] = message.contact.phone_number
        bot.send_message(message.chat.id, "Iltimos, o‘zingizning fotosuratingizni yuboring:")
        bot.register_next_step_handler(message, ask_comment)
    else:
        bot.send_message(message.chat.id, "Iltimos, telefon raqamingizni pastdagi tugma orqali yuboring!")
        bot.register_next_step_handler(message, ask_phone)

def ask_comment(message):
    if message.photo:
        user_data[message.chat.id]["photo"] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "O‘zingiz haqingizda qisqacha yozing:")
        bot.register_next_step_handler(message, confirm_application)
    else:
        bot.send_message(message.chat.id, "Iltimos, fotosuratingizni yuboring!")
        bot.register_next_step_handler(message, ask_photo)

def confirm_application(message):
    user_data[message.chat.id]["izoh"] = message.text
    data = user_data[message.chat.id]
    summary = f"""📋 Anketa ma'lumotlari:
    🛠 Lavozim: {data['lavozim']}
    ⏳ Ish turi: {data['ish_turi']}
    🕒 Grafik: {data['ish_grafik']}
    🧑‍💼 Jins: {data['jins']}
    📛 F.I.Sh: {data['fio']}
    📞 Telefon: {data['telefon']}
    📝 Izoh: {data['izoh']}"""
    
    bot.send_message(message.chat.id, summary)
    bot.send_photo(ADMIN_ID, data["photo"], caption=summary)
    bot.send_message(message.chat.id, "✅ Anketangiz yuborildi!")

bot.polling(none_stop=True)
