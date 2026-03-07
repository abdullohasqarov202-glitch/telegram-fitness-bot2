import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

ADMIN = "@Asqarov_0207"

users = {}

main_menu = [
    ["🏋️ Vazn olish", "🔥 Vazn yo‘qotish"],
    ["📅 7 kunlik ovqatlanish"],
    ["💎 Premium reja"]
]

keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    users[user.id] = {"step": "goal"}

    await update.message.reply_text(
        "👋 Salom!\n\n"
        "💪 Fitness yordamchi botiga xush kelibsiz!\n\n"
        "Maqsadingizni tanlang:",
        reply_markup=keyboard
    )

# MESSAGE HANDLER
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text

    if user.id not in users:
        users[user.id] = {"step": "goal"}

    step = users[user.id]["step"]

    # GOAL
    if text == "🏋️ Vazn olish":
        users[user.id]["goal"] = "gain"
        users[user.id]["step"] = "weight"
        await update.message.reply_text("⚖️ Vazningiz nechchi kg?")

    elif text == "🔥 Vazn yo‘qotish":
        users[user.id]["goal"] = "lose"
        users[user.id]["step"] = "weight"
        await update.message.reply_text("⚖️ Hozir vazningiz nechchi kg?")

    # WEIGHT
    elif step == "weight":
        users[user.id]["weight"] = text
        users[user.id]["step"] = "height"
        await update.message.reply_text("📏 Bo‘yingiz nechchi sm?")

    # HEIGHT
    elif step == "height":
        users[user.id]["height"] = text
        users[user.id]["step"] = "age"
        await update.message.reply_text("🎂 Yoshingiz nechchi?")

    # AGE
    elif step == "age":

        users[user.id]["age"] = text
        goal = users[user.id]["goal"]

        if goal == "gain":

            await update.message.reply_text(
                "🏋️ Vazn olish uchun tavsiya:\n\n"
                "🍳 Nonushta:\n"
                "Tuxum, suli bo‘tqa, banan, sut\n\n"
                "🍗 Tushlik:\n"
                "Guruch, tovuq go‘shti, sabzavot\n\n"
                "🥩 Kechki ovqat:\n"
                "Go‘sht, kartoshka, salat\n\n"
                "🥜 Snack:\n"
                "Yong‘oq, qatiq\n\n"
                "💧 Kuniga 3 litr suv iching"
            )

        else:

            await update.message.reply_text(
                "🔥 Vazn tashlash uchun tavsiya:\n\n"
                "🍳 Nonushta:\n"
                "2 ta tuxum, bodring, choy\n\n"
                "🥗 Tushlik:\n"
                "Tovuq, sabzavot salat\n\n"
                "🥗 Kechki ovqat:\n"
                "Sabzavot + baliq\n\n"
                "🍏 Snack:\n"
                "Olma yoki yogurt\n\n"
                "💧 Kuniga 2.5 litr suv iching"
            )

        users[user.id]["step"] = "done"

    # 7 KUNLIK OVQAT
    elif text == "📅 7 kunlik ovqatlanish":

        await update.message.reply_text(
            "📅 7 kunlik ovqatlanish rejasi\n\n"

            "1-kun\n"
            "🍳 Tuxum + suli\n"
            "🍗 Tovuq + guruch\n"
            "🥗 Salat\n\n"

            "2-kun\n"
            "🍳 Tuxum + non\n"
            "🥩 Go‘sht + kartoshka\n"
            "🥗 Salat\n\n"

            "3-kun\n"
            "🥣 Suli + banan\n"
            "🍗 Tovuq + makaron\n"
            "🥗 Sabzavot\n\n"

            "4-kun\n"
            "🍳 Tuxum\n"
            "🍗 Tovuq\n"
            "🥗 Salat\n\n"

            "5-kun\n"
            "🥣 Suli\n"
            "🥩 Go‘sht\n"
            "🥗 Sabzavot\n\n"

            "6-kun\n"
            "🍳 Tuxum\n"
            "🍗 Tovuq\n"
            "🥗 Salat\n\n"

            "7-kun\n"
            "🥣 Suli\n"
            "🥩 Go‘sht\n"
            "🥗 Sabzavot"
        )

    # PREMIUM
    elif text == "💎 Premium reja":

        await update.message.reply_text(
            "💎 PREMIUM REJA\n\n"
            "✔ Shaxsiy dieta\n"
            "✔ Kunlik menyu\n"
            "✔ Vazn nazorati\n"
            "✔ 30 kunlik plan\n\n"
            "💰 Narx: 20 000 so‘m / oy\n\n"
            f"To‘lov uchun admin: {ADMIN}"
        )

# ADMIN STATS
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username == "Asqarov_0207":

        total = len(users)

        await update.message.reply_text(
            f"📊 Bot statistikasi\n\n"
            f"👤 Foydalanuvchilar: {total}"
        )

# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
