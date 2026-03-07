import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN = "Asqarov_0207"

users = {}
premium_users = set()
weights = {}

# ASOSIY MENU
menu = ReplyKeyboardMarkup([
["🏋️ Vazn olish","🔥 Vazn yo‘qotish"],
["🔥 Kaloriya hisoblash","⚖️ Vazn yozish"],
["📅 7 kunlik ovqat","🏋️ Workout"],
["💎 Premium","🔙 Ortga"]
], resize_keyboard=True)

# PREMIUM MENU
premium_menu = ReplyKeyboardMarkup([
["🥗 30 kunlik dieta"],
["🏋️ Premium workout"],
["🔙 Ortga"]
], resize_keyboard=True)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    users[user.id] = {"step":"menu"}

    await update.message.reply_text(

"""💪 FITNESS BOT
━━━━━━━━━━━━━━━

Sog‘lom hayot uchun yordamchi bot

Bot sizga yordam beradi:
🥗 dieta reja
🔥 kaloriya hisoblash
🏋️ workout
⚖️ vazn nazorati

Kerakli menyuni tanlang 👇
""",

reply_markup=menu
)

# MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text

    if user.id not in users:
        users[user.id]={"step":"menu"}

    step = users[user.id]["step"]

# ORTGA
    if text == "🔙 Ortga":

        users[user.id]["step"]="menu"

        await update.message.reply_text(
        "🏠 Asosiy menyu",
        reply_markup=menu
        )

# VAZN OLISH
    elif text == "🏋️ Vazn olish":

        users[user.id]["goal"]="gain"
        users[user.id]["step"]="weight"

        await update.message.reply_text(
        "⚖️ Vazningiz nechchi kg?"
        )

# OZISH
    elif text == "🔥 Vazn yo‘qotish":

        users[user.id]["goal"]="lose"
        users[user.id]["step"]="weight"

        await update.message.reply_text(
        "⚖️ Hozir vazningiz nechchi kg?"
        )

# VAZN
    elif step == "weight":

        users[user.id]["weight"]=float(text)
        users[user.id]["step"]="height"

        await update.message.reply_text(
        "📏 Bo‘yingiz nechchi sm?"
        )

# BOY
    elif step == "height":

        users[user.id]["height"]=float(text)
        users[user.id]["step"]="age"

        await update.message.reply_text(
        "🎂 Yoshingiz nechchi?"
        )

# AGE
    elif step == "age":

        users[user.id]["age"]=int(text)

        weight=users[user.id]["weight"]
        height=users[user.id]["height"]
        age=users[user.id]["age"]

        calories=10*weight+6.25*height-5*age+5
        water=weight*0.035

        await update.message.reply_text(

f"""🔥 Kunlik kaloriya: {round(calories)} kcal
💧 Kunlik suv: {round(water,1)} L

Quyidagi dieta sizga mos 👇
"""
)

        if users[user.id]["goal"]=="gain":

            await update.message.reply_text(

"""🏋️ VAZN OLISH DIETA

🍳 Nonushta
Tuxum + suli + banan

🍗 Tushlik
Guruch + tovuq

🥩 Kechki ovqat
Go‘sht + kartoshka

🥜 Snack
Yong‘oq + yogurt
"""
)

        else:

            await update.message.reply_text(

"""🔥 VAZN YO‘QOTISH DIETA

🍳 Nonushta
2 tuxum + sabzavot

🥗 Tushlik
Tovuq + salat

🐟 Kechki ovqat
Baliq + sabzavot

🍏 Snack
Olma
"""
)

        users[user.id]["step"]="menu"

# KALORIYA
    elif text == "🔥 Kaloriya hisoblash":

        users[user.id]["step"]="weight"

        await update.message.reply_text(
        "⚖️ Vazningiz nechchi kg?"
        )

# VAZN YOZISH
    elif text == "⚖️ Vazn yozish":

        users[user.id]["step"]="save_weight"

        await update.message.reply_text(
        "Bugungi vazningiz nechchi kg?"
        )

    elif step == "save_weight":

        weights[user.id]=text

        await update.message.reply_text(
        f"✅ Vazn saqlandi: {text} kg"
        )

        users[user.id]["step"]="menu"

# 7 KUNLIK OVQAT
    elif text == "📅 7 kunlik ovqat":

        await update.message.reply_text(

"""📅 7 KUNLIK OVQAT

1️⃣ Tuxum + suli
2️⃣ Tovuq + guruch
3️⃣ Go‘sht + sabzavot
4️⃣ Tuxum + non
5️⃣ Tovuq + makaron
6️⃣ Go‘sht + kartoshka
7️⃣ Baliq + salat
"""
)

# WORKOUT
    elif text == "🏋️ Workout":

        await update.message.reply_text(

"""🏋️ HAFTALIK WORKOUT

1️⃣ Push-up 20
2️⃣ Squat 30
3️⃣ Plank 30 sec
4️⃣ Running 10 min
"""
)

# PREMIUM
    elif text == "💎 Premium":

        if user.id in premium_users:

            await update.message.reply_text(
            "💎 PREMIUM BO‘LIM",
            reply_markup=premium_menu
            )

        else:

            await update.message.reply_text(

"""❌ Bu premium bo‘lim

💰 Narx: 20 000 so‘m / oy

Premium olish uchun:
@Asqarov_0207
"""
)

# 30 KUNLIK DIETA
    elif text == "🥗 30 kunlik dieta":

        if user.id in premium_users:

            diet="🥗 30 KUNLIK DIETA\n\n"

            for i in range(1,31):

                diet+=(
f"""📅 {i}-kun
🍳 Nonushta: tuxum + suli
🍗 Tushlik: guruch + tovuq
🥗 Kechki ovqat: sabzavot + baliq

"""
)

            await update.message.reply_text(diet)

        else:

            await update.message.reply_text("❌ Premium kerak")

# PREMIUM WORKOUT
    elif text == "🏋️ Premium workout":

        if user.id in premium_users:

            await update.message.reply_text(

"""🏋️ PREMIUM WORKOUT

1-kun
Push-up 25
Squat 40
Plank 40 sec

2-kun
Pull-up 10
Running 15 min

3-kun
Dam olish
"""
)

        else:

            await update.message.reply_text("❌ Premium kerak")


# ADMIN PREMIUM BERISH
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username==ADMIN:

        user_id=int(context.args[0])
        premium_users.add(user_id)

        await update.message.reply_text("✅ Premium berildi")

# ADMIN STATS
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username==ADMIN:

        await update.message.reply_text(

f"""📊 BOT STATISTIKA

👤 Userlar: {len(users)}
💎 Premium: {len(premium_users)}
⚖️ Vazn yozganlar: {len(weights)}
"""
)

# ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
f"Sizning ID: {update.message.from_user.id}"
)

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("stats",stats))
app.add_handler(CommandHandler("premium",premium))
app.add_handler(CommandHandler("id",myid))
app.add_handler(MessageHandler(filters.TEXT,message))

app.run_polling()
