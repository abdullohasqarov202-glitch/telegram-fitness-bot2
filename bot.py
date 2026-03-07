import telebot
from telebot import types

TOKEN = "BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

ADMIN_USERNAME = "Asqarov_0207"

users = set()
state = {}

# START
@bot.message_handler(commands=['start'])
def start(message):

    users.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔥 Vazn yo'qotish")
    markup.add("🍽 Ovqatlanish", "💪 Mashqlar")

    bot.send_message(
        message.chat.id,
        "👋 MYFIT BOT ga xush kelibsiz\nKerakli bo‘limni tanlang:",
        reply_markup=markup
    )


# VAZN YO'QOTISH
@bot.message_handler(func=lambda m: m.text == "🔥 Vazn yo'qotish")
def ask_weight(message):

    state[message.chat.id] = "weight"

    bot.send_message(
        message.chat.id,
        "⚖ Hozir vazningiz nechchi kg?"
    )


# VAZN QABUL QILISH
@bot.message_handler(func=lambda m: state.get(m.chat.id) == "weight")
def get_weight(message):

    if message.text.isdigit():

        weight = int(message.text)
        calories = weight * 24

        bot.send_message(
            message.chat.id,
            f"✅ Vazningiz: {weight} kg\n"
            f"🔥 Kunlik taxminiy kaloriya: {calories} kcal"
        )

        state[message.chat.id] = None

    else:

        bot.send_message(
            message.chat.id,
            "❌ Vaznni raqam bilan yozing\nMasalan: 70"
        )


# OVQATLANISH
@bot.message_handler(func=lambda m: m.text == "🍽 Ovqatlanish")
def food(message):

    text = """
🍽 Kunlik ovqatlanish

🥞 Nonushta
• 3 tuxum
• suli bo‘tqasi
• banan

🍗 Tushlik
• tovuq go‘shti
• guruch
• sabzavot salati

🥗 Kechki ovqat
• baliq yoki tovuq
• sabzavot

🥜 Tamaddi
• yong‘oq yoki yogurt

💧 Kuniga 2-3 litr suv iching
"""

    bot.send_message(message.chat.id, text)


# MASHQLAR
@bot.message_handler(func=lambda m: m.text == "💪 Mashqlar")
def workout(message):

    text = """
💪 Kunlik workout

1️⃣ O‘tirib turish — 3x15
2️⃣ Otjimaniya — 3x10
3️⃣ Press — 3x20
4️⃣ Plank — 30 soniya x3
5️⃣ Yugurish — 10 daqiqa

🔥 Har kuni bajaring!
"""

    bot.send_message(message.chat.id, text)


# ADMIN PANEL
@bot.message_handler(commands=['admin'])
def admin_panel(message):

    if message.from_user.username == ADMIN_USERNAME:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📢 Xabar yuborish")

        bot.send_message(
            message.chat.id,
            "👑 Admin panel",
            reply_markup=markup
        )


# XABAR YUBORISH BOSHLASH
@bot.message_handler(func=lambda m: m.text == "📢 Xabar yuborish")
def broadcast_start(message):

    if message.from_user.username == ADMIN_USERNAME:

        state[message.chat.id] = "broadcast"

        bot.send_message(
            message.chat.id,
            "📨 Hamma userlarga yuboriladigan xabarni yozing"
        )


# XABAR YUBORISH
@bot.message_handler(func=lambda m: state.get(m.chat.id) == "broadcast")
def broadcast_send(message):

    if message.from_user.username == ADMIN_USERNAME:

        for user in users:
            try:
                bot.send_message(user, message.text)
            except:
                pass

        bot.send_message(message.chat.id, "✅ Xabar hammaga yuborildi")

        state[message.chat.id] = None


print("Bot ishga tushdi...")
bot.infinity_polling()
