import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

ADMIN = "Asqarov_0207"

users = {}
premium_users = set()
weights = {}

menu = [
["🏋️ Vazn olish","🔥 Vazn yo‘qotish"],
["📊 BMI hisoblash","⚖️ Vazn yozish"],
["📅 7 kunlik ovqat","🏋️ Workout"],
["💎 Premium dieta"]
]

keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    users[user.id] = {"step":"menu"}

    await update.message.reply_text(

"💪 FITNESS BOT\n"
"━━━━━━━━━━━━━━\n"
"Sog‘lom hayot uchun yordamchi bot\n\n"

"Bot sizga yordam beradi:\n"
"🥗 dieta\n"
"📊 BMI\n"
"🏋️ workout\n"
"⚖️ vazn nazorat\n\n"

"Kerakli menyuni tanlang 👇",

reply_markup=keyboard
)

# MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text

    if user.id not in users:
        users[user.id]={"step":"menu"}

    step = users[user.id]["step"]

# VAZN OLISH
    if text == "🏋️ Vazn olish":

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
        height=users[user.id]["height"]/100

        bmi=weight/(height*height)
        water=weight*0.035

        await update.message.reply_text(

f"📊 Sizning BMI: {round(bmi,1)}\n"
f"💧 Kunlik suv: {round(water,1)} L\n\n"

)

        if users[user.id]["goal"]=="gain":

            await update.message.reply_text(

"🏋️ VAZN OLISH DIETA\n\n"

"🍳 Nonushta\n"
"Tuxum + suli + banan\n\n"

"🍗 Tushlik\n"
"Guruch + tovuq + salat\n\n"

"🥩 Kechki ovqat\n"
"Go‘sht + kartoshka\n\n"

"🥜 Snack\n"
"Yong‘oq + yogurt"

)

        else:

            await update.message.reply_text(

"🔥 VAZN TASHLASH DIETA\n\n"

"🍳 Nonushta\n"
"2 tuxum + sabzavot\n\n"

"🥗 Tushlik\n"
"Tovuq + salat\n\n"

"🐟 Kechki ovqat\n"
"Baliq + sabzavot\n\n"

"🍏 Snack\n"
"Olma"

)

        users[user.id]["step"]="menu"

# BMI
    elif text == "📊 BMI hisoblash":

        users[user.id]["step"]="bmi_weight"

        await update.message.reply_text(
"⚖️ Vazningiz nechchi kg?"
)

    elif step == "bmi_weight":

        users[user.id]["bmi_w"]=float(text)
        users[user.id]["step"]="bmi_height"

        await update.message.reply_text(
"📏 Bo‘yingiz nechchi sm?"
)

    elif step == "bmi_height":

        w=users[user.id]["bmi_w"]
        h=float(text)/100

        bmi=w/(h*h)

        await update.message.reply_text(
f"📊 BMI: {round(bmi,1)}"
)

        users[user.id]["step"]="menu"

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

"📅 7 KUNLIK OVQAT\n\n"

"1️⃣ Tuxum + suli\n"
"2️⃣ Tovuq + guruch\n"
"3️⃣ Go‘sht + sabzavot\n"
"4️⃣ Tuxum + non\n"
"5️⃣ Tovuq + makaron\n"
"6️⃣ Go‘sht + kartoshka\n"
"7️⃣ Baliq + salat"

)

# WORKOUT
    elif text == "🏋️ Workout":

        await update.message.reply_text(

"🏋️ HAFTALIK WORKOUT\n\n"

"1️⃣ Push-up 20\n"
"2️⃣ Squat 30\n"
"3️⃣ Plank 30 sec\n"
"4️⃣ Running 10 min"

)

# PREMIUM
    elif text == "💎 Premium dieta":

        if user.id in premium_users:

            await update.message.reply_text(

"💎 PREMIUM DIETA\n\n"

"🥗 30 kunlik maxsus dieta\n\n"

"🍳 Nonushta\n"
"Tuxum + suli + meva\n\n"

"🍗 Tushlik\n"
"Guruch + tovuq\n\n"

"🥩 Kechki ovqat\n"
"Go‘sht + sabzavot\n\n"

"💧 Kuniga 3L suv\n"
"🏋️ Haftasiga 4 workout"

)

        else:

            await update.message.reply_text(

"❌ Bu premium bo‘lim\n\n"

"💰 Narx: 20 000 so‘m / oy\n\n"

"Premium olish uchun\n"
"@Asqarov_0207"

)

# ADMIN PREMIUM
async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username==ADMIN:

        user_id=int(context.args[0])
        premium_users.add(user_id)

        await update.message.reply_text("✅ Premium berildi")

# ADMIN STATS
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username==ADMIN:

        await update.message.reply_text(

f"📊 BOT STATISTIKA\n\n"
f"👤 Userlar: {len(users)}\n"
f"💎 Premium: {len(premium_users)}\n"
f"⚖️ Vazn yozganlar: {len(weights)}"

)

# ID
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
f"Sizning ID: {update.message.from_user.id}"
)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("stats",stats))
app.add_handler(CommandHandler("premium",premium))
app.add_handler(CommandHandler("id",myid))
app.add_handler(MessageHandler(filters.TEXT,message))

app.run_polling()
