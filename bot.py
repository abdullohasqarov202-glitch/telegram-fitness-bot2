import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

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

Bu fitness bot sizga yordam beradi:

🏋️ Vazn olish
🔥 Vazn yo‘qotish
🍽 Ovqatlanish
💪 Mashqlar

Menyudan tanlang 👇
""",
reply_markup=main_menu
)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text
    user_id = user.id

    if text == "🔙 Ortga":
        await update.message.reply_text("Bosh menyu", reply_markup=main_menu)


    elif text == "🏋️ Vazn olish":
        users[user_id] = {"goal":"gain"}
        await update.message.reply_text("⚖️ Vazningiz nechchi kg?", reply_markup=back_menu)


    elif text == "🔥 Vazn yo‘qotish":
        users[user_id] = {"goal":"lose"}
        await update.message.reply_text("⚖️ Hozir vazningiz nechchi kg?", reply_markup=back_menu)


    elif user_id in users and "weight" not in users[user_id]:

        if not is_number(text):
            await update.message.reply_text("❌ Vaznni raqam bilan yozing\nMasalan: 70")
            return

        users[user_id]["weight"] = float(text)
        await update.message.reply_text("📏 Bo‘yingiz nechchi sm?")


    elif user_id in users and "height" not in users[user_id]:

        if not is_number(text):
            await update.message.reply_text("❌ Bo‘yni raqam bilan yozing\nMasalan: 175")
            return

        users[user_id]["height"] = float(text)
        await update.message.reply_text("🎂 Yoshingiz nechchi?")


    elif user_id in users and "age" not in users[user_id]:

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
📊 Sizga kerakli kunlik kaloriya:

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
• tovuq go‘shti
• guruch
• sabzavot salati

🥗 Kechki ovqat
• baliq yoki tovuq
• sabzavot

🥜 Tamaddi
• yong‘oq yoki yogurt

💧 Kuniga 2-3 litr suv iching
""",
reply_markup=main_menu
)


    elif text == "💪 Mashqlar":

        await update.message.reply_text("💪 Mashqlar bo‘limi", reply_markup=workout_menu)


    elif text == "💪 Kunlik mashq":

        await update.message.reply_text(
"""
💪 BUGUNGI MASHQLAR

1️⃣ O‘tirib turish — 15 × 3

2️⃣ Qo‘l bilan yerga tayangan holda ko‘tarilish — 12 × 3

3️⃣ Qorin mashqi — 20 × 3

4️⃣ Turnikda tortilish — 8 × 3

5️⃣ Planka — 60 soniya
"""
)


    elif text == "📅 7 kunlik mashq":

        await update.message.reply_text(
"""
📅 7 KUNLIK MASHQ

1-kun
Qo‘l mashqlari
Qorin mashqi

2-kun
O‘tirib turish
Yugurish

3-kun
Turnik
Qorin mashqi

4-kun
Dam olish

5-kun
O‘tirib turish
Qo‘l mashqlari

6-kun
Yugurish
Qorin mashqi

7-kun
Yengil mashqlar
"""
)


    elif text == "💎 Premium":

        if user_id in premium_users:

            await update.message.reply_text(
"💎 Premium menyu",
reply_markup=premium_menu
)

        else:

            await update.message.reply_text(
f"""
❌ Bu premium bo‘lim

💰 Narxi: 20 000 so‘m / oy

Premium olish uchun yozing:
@{ADMIN_USERNAME}
"""
)


    elif text == "🥗 30 kunlik dieta":

        if user_id in premium_users:

            await update.message.reply_text(
"""
🥗 30 KUNLIK DIETA

Har kuni:

🍳 Nonushta
tuxum + suli

🍗 Tushlik
tovuq + guruch

🥗 Kechki
salat + baliq

💧 3 litr suv
"""
)


    elif text == "🔥 Premium mashqlar":

        if user_id in premium_users:

            await update.message.reply_text(
"""
🔥 PREMIUM MASHQLAR

1️⃣ O‘tirib turish — 25 × 4

2️⃣ Qo‘l bilan ko‘tarilish — 20 × 4

3️⃣ Turnik — 12 × 4

4️⃣ Qorin mashqi — 30 × 4

5️⃣ Planka — 90 soniya
"""
)


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.message.from_user):
        await update.message.reply_text("❌ Siz admin emassiz")
        return

    try:
        user_id = int(context.args[0])
        premium_users.add(user_id)

        await update.message.reply_text("✅ Premium berildi")

    except:
        await update.message.reply_text("User ID yozing")


async def reklama(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.message.from_user):
        return

    text = " ".join(context.args)

    for user_id in users:

        try:
            await context.bot.send_message(user_id, text)
        except:
            pass

    await update.message.reply_text("✅ Xabar yuborildi")


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.message.from_user):
        return

    await update.message.reply_text(
f"""
📊 BOT STATISTIKASI

👤 Foydalanuvchilar: {len(users)}
💎 Premium userlar: {len(premium_users)}
"""
)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("reklama", reklama))
app.add_handler(CommandHandler("stat", stat))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
