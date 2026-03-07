import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

ADMIN_USERNAME = "Asqarov_0207"

user_data = {}
premium_users = set()

main_menu = ReplyKeyboardMarkup([
["🏋️ Vazn olish", "🔥 Vazn yo‘qotish"],
["🍽 Ovqatlanish", "🏋️ Workout"],
["💎 Premium", "📊 Statistika"]
], resize_keyboard=True)

back_menu = ReplyKeyboardMarkup([
["🔙 Ortga"]
], resize_keyboard=True)

diet_menu = ReplyKeyboardMarkup([
["🥗 7 kunlik ovqatlanish"],
["🔙 Ortga"]
], resize_keyboard=True)

workout_menu = ReplyKeyboardMarkup([
["💪 Kunlik workout", "📅 7 kunlik workout"],
["🔙 Ortga"]
], resize_keyboard=True)

premium_menu = ReplyKeyboardMarkup([
["🥗 30 kunlik dieta"],
["🔥 Premium workout"],
["🔙 Ortga"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
"""
👋 Salom!

Bu Fitness bot sizga yordam beradi:

🏋️ Vazn olish
🔥 Vazn yo‘qotish
🍽 Ovqatlanish rejasi
💪 Workout mashqlari

Boshlash uchun menyudan tanlang 👇
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
        user_data[user_id] = {"goal":"gain"}
        await update.message.reply_text("⚖️ Vazningiz nechchi kg?", reply_markup=back_menu)

    elif text == "🔥 Vazn yo‘qotish":
        user_data[user_id] = {"goal":"lose"}
        await update.message.reply_text("⚖️ Hozir vazningiz nechchi kg?", reply_markup=back_menu)

    elif user_id in user_data and "weight" not in user_data[user_id]:

        user_data[user_id]["weight"] = float(text)
        await update.message.reply_text("📏 Bo‘yingiz nechchi sm?")

    elif user_id in user_data and "height" not in user_data[user_id]:

        user_data[user_id]["height"] = float(text)
        await update.message.reply_text("🎂 Yoshingiz nechchi?")

    elif user_id in user_data and "age" not in user_data[user_id]:

        age = int(text)
        weight = user_data[user_id]["weight"]
        height = user_data[user_id]["height"]

        calories = 10*weight + 6.25*height - 5*age + 5

        if user_data[user_id]["goal"] == "gain":
            calories += 400
        else:
            calories -= 400

        await update.message.reply_text(
f"""
📊 Sizga kerakli kunlik kaloriya:

🔥 {int(calories)} kcal

Shu kaloriyani iste'mol qilsangiz maqsadingizga erishasiz.
""",
reply_markup=main_menu
)

    elif text == "🍽 Ovqatlanish":
        await update.message.reply_text(
"🥗 Ovqatlanish bo‘limi",
reply_markup=diet_menu
)

    elif text == "🥗 7 kunlik ovqatlanish":

        await update.message.reply_text(
"""
🥗 7 KUNLIK OVQATLANISH

1-kun
🍳 3 tuxum
🍗 Tovuq + guruch
🥗 Salat

2-kun
🥣 Suli
🍖 Go‘sht
🥗 Sabzavot

3-kun
🥚 2 tuxum
🍗 Tovuq
🥗 Salat

4-kun
🥣 Suli
🍖 Go‘sht
🥗 Sabzavot

5-kun
🥚 3 tuxum
🍗 Tovuq
🥗 Salat

6-kun
🥣 Suli
🍖 Go‘sht
🥗 Sabzavot

7-kun
🥚 Tuxum
🍗 Tovuq
🥗 Salat

💧 Kuniga 2-3 litr suv iching
"""
)

    elif text == "🏋️ Workout":

        await update.message.reply_text(
"💪 Workout bo‘limi",
reply_markup=workout_menu
)

    elif text == "💪 Kunlik workout":

        await update.message.reply_text(
"""
💪 BUGUNGI WORKOUT

1️⃣ O‘tirib turish (Squat) — 15 x 3
2️⃣ Push-up — 12 x 3
3️⃣ Press — 20 x 3
4️⃣ Turnik — 8 x 3
5️⃣ Plank — 60 soniya

🔥 Mashqdan oldin 5 minut razminka qiling
"""
)

    elif text == "📅 7 kunlik workout":

        await update.message.reply_text(
"""
📅 7 KUNLIK WORKOUT

1-kun
Push-up
Press

2-kun
Squat
Plank

3-kun
Turnik
Press

4-kun
Dam olish

5-kun
Push-up
Squat

6-kun
Press
Plank

7-kun
Yengil yugurish
"""
)

    elif text == "💎 Premium":

        if user_id in premium_users:

            await update.message.reply_text(
"""
💎 PREMIUM BO‘LIM

Maxsus fitness dasturlari
""",
reply_markup=premium_menu
)

        else:

            await update.message.reply_text(
f"""
❌ Bu premium bo‘lim

💰 Narx: 20 000 so‘m / oy

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
- tuxum
- suli
- banan

🍗 Tushlik
- tovuq
- guruch
- sabzavot

🥗 Kechki
- salat
- baliq

💧 3 litr suv
"""
)

    elif text == "🔥 Premium workout":

        if user_id in premium_users:

            await update.message.reply_text(
"""
🔥 PREMIUM WORKOUT

1️⃣ Push-up — 20x4
2️⃣ Squat — 25x4
3️⃣ Turnik — 12x4
4️⃣ Press — 30x4
5️⃣ Plank — 90s

Haftasiga 5 kun
"""
)

    elif text == "📊 Statistika":

        if user.username == ADMIN_USERNAME:

            await update.message.reply_text(
f"""
📊 BOT STATISTIKASI

👤 Foydalanuvchilar: {len(user_data)}
💎 Premium: {len(premium_users)}
"""
)

        else:
            await update.message.reply_text("❌ Bu admin bo‘lim")

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username == ADMIN_USERNAME:

        try:
            user_id = int(context.args[0])
            premium_users.add(user_id)

            await update.message.reply_text(
f"✅ {user_id} ga premium berildi"
)

        except:
            await update.message.reply_text("User ID yozing")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
