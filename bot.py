import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "BOT_TOKENINGIZ"

ADMIN_USERNAME = "Asqarov_0207"

users = {}
premium_users = set()

def is_admin(user):
    return user.username == ADMIN_USERNAME

def is_number(text):
    try:
        float(text)
        return True
    except:
        return False


main_menu = ReplyKeyboardMarkup([
["🏋️ Vazn olish", "🔥 Vazn yo‘qotish"],
["🍽 Ovqatlanish", "💪 Mashqlar"],
["💎 Premium"]
], resize_keyboard=True)

back_menu = ReplyKeyboardMarkup([["🔙 Ortga"]], resize_keyboard=True)

workout_menu = ReplyKeyboardMarkup([
["💪 Kunlik mashq", "📅 7 kunlik mashq"],
["🔙 Ortga"]
], resize_keyboard=True)

premium_menu = ReplyKeyboardMarkup([
["🥗 30 kunlik dieta", "🔥 Premium mashqlar"],
["🔙 Ortga"]
], resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    users[user_id] = {}

    await update.message.reply_text(
"""
👋 Salom!

Fitness botga xush kelibsiz.

Kerakli bo‘limni tanlang 👇
""",
reply_markup=main_menu
)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text
    user_id = user.id

    if user_id not in users:
        users[user_id] = {}

    # ORTGA
    if text == "🔙 Ortga":
        users[user_id] = {}
        await update.message.reply_text("Bosh menyu", reply_markup=main_menu)
        return

    # VAZN OLISH
    if text == "🏋️ Vazn olish":
        users[user_id] = {"goal":"gain","step":"weight"}
        await update.message.reply_text("⚖️ Vazningiz nechchi kg?", reply_markup=back_menu)
        return

    # VAZN YO‘QOTISH
    if text == "🔥 Vazn yo‘qotish":
        users[user_id] = {"goal":"lose","step":"weight"}
        await update.message.reply_text("⚖️ Hozir vazningiz nechchi kg?", reply_markup=back_menu)
        return


    # VAZN KIRITISH
    if users[user_id].get("step") == "weight":

        if not is_number(text):
            await update.message.reply_text("❌ Vaznni raqam bilan yozing\nMasalan: 70")
            return

        users[user_id]["weight"] = float(text)
        users[user_id]["step"] = "height"

        await update.message.reply_text("📏 Bo‘yingiz nechchi sm?")
        return


    # BO‘Y
    if users[user_id].get("step") == "height":

        if not is_number(text):
            await update.message.reply_text("❌ Bo‘yni raqam bilan yozing\nMasalan: 175")
            return

        users[user_id]["height"] = float(text)
        users[user_id]["step"] = "age"

        await update.message.reply_text("🎂 Yoshingiz nechchi?")
        return


    # YOSH
    if users[user_id].get("step") == "age":

        if not text.isdigit():
            await update.message.reply_text("❌ Yoshni raqam bilan yozing\nMasalan: 20")
            return

        age = int(text)
        weight = users[user_id]["weight"]
        height = users[user_id]["height"]

        calories = 10*weight + 6.25*height - 5*age + 5

        if users[user_id]["goal"] == "gain":
            calories += 400
        else:
            calories -= 400

        await update.message.reply_text(
f"""
📊 Sizga kerakli kunlik kaloriya

🔥 {int(calories)} kcal
"""
)

        await update.message.reply_text(
"""
🍽 KUNLIK OVQATLANISH

🍳 Nonushta
• 3 tuxum
• suli bo‘tqasi
• banan

🍗 Tushlik
• tovuq
• guruch
• salat

🥗 Kechki ovqat
• baliq yoki tovuq
• sabzavot

🥜 Tamaddi
• yong‘oq yoki yogurt
""",
reply_markup=main_menu
)

        users[user_id] = {}
        return


    # MASHQLAR
    if text == "💪 Mashqlar":
        await update.message.reply_text("💪 Mashqlar bo‘limi", reply_markup=workout_menu)
        return


    if text == "💪 Kunlik mashq":

        await update.message.reply_text(
"""
💪 BUGUNGI MASHQLAR

1️⃣ O‘tirib turish — 15 × 3
2️⃣ Push-up — 12 × 3
3️⃣ Qorin mashqi — 20 × 3
4️⃣ Turnik — 8 × 3
5️⃣ Plank — 60 soniya
"""
)
        return


    if text == "📅 7 kunlik mashq":

        await update.message.reply_text(
"""
📅 7 KUNLIK MASHQ

1-kun: Qo‘l
2-kun: Oyoq
3-kun: Qorin
4-kun: Dam
5-kun: Ko‘krak
6-kun: Kardio
7-kun: Yengil mashq
"""
)
        return


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
