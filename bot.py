import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN = "Asqarov_0207"
USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

users = load_users()
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    users.add(user.id)
    save_users(users)

    buttons = [["🏋️ Vazn olish", "🔥 Vazn yo‘qotish"]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Salom 👋\nMaqsadingizni tanlang:",
        reply_markup=keyboard
    )

async def users_count(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username != ADMIN:
        return

    await update.message.reply_text(f"👥 Bot userlari: {len(users)}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.username != ADMIN:
        return

    text = update.message.text.replace("/send ", "")

    for user_id in users:
        try:
            await context.bot.send_message(user_id, text)
        except:
            pass

    await update.message.reply_text("Xabar yuborildi ✅")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text

    if text == "🏋️ Vazn olish":

        user_data[user_id] = {"goal": "gain"}

        buttons = [["👨 Erkak", "👩 Ayol"]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

        await update.message.reply_text(
            "Jinsingizni tanlang:",
            reply_markup=keyboard
        )

    elif text == "🔥 Vazn yo‘qotish":

        user_data[user_id] = {"goal": "lose"}

        buttons = [["👨 Erkak", "👩 Ayol"]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

        await update.message.reply_text(
            "Jinsingizni tanlang:",
            reply_markup=keyboard
        )

    elif text in ["👨 Erkak", "👩 Ayol"]:

        user_data[user_id]["gender"] = text

        await update.message.reply_text("Vazningiz nechchi kg?")

    elif user_id in user_data and "weight" not in user_data[user_id]:

        user_data[user_id]["weight"] = float(text)

        await update.message.reply_text("Yoshingiz nechchi?")

    elif user_id in user_data and "age" not in user_data[user_id]:

        user_data[user_id]["age"] = int(text)

        await update.message.reply_text("Bo‘yingiz nechchi cm?")

    elif user_id in user_data and "height" not in user_data[user_id]:

        weight = user_data[user_id]["weight"]
        age = user_data[user_id]["age"]
        height = float(text)
        gender = user_data[user_id]["gender"]

        height_m = height / 100

        bmi = weight / (height_m ** 2)

        if gender == "👨 Erkak":
            calories = 10*weight + 6.25*height - 5*age + 5
        else:
            calories = 10*weight + 6.25*height - 5*age - 161

        water = weight * 0.035

        await update.message.reply_text(
            f"📊 BMI: {bmi:.1f}\n"
            f"🔥 Kunlik kaloriya: {int(calories)} kcal\n"
            f"💧 Kunlik suv normasi: {water:.1f} litr"
        )

        goal = user_data[user_id]["goal"]

        if goal == "gain":

            await update.message.reply_text(
                "💪 7 kunlik vazn olish dietasi:\n\n"
                "1-kun: tuxum, suli, guruch, tovuq\n"
                "2-kun: tuxum, makaron, mol go‘shti\n"
                "3-kun: suli, guruch, baliq\n"
                "4-kun: tuxum, kartoshka, tovuq\n"
                "5-kun: guruch, mol go‘shti, yogurt\n"
                "6-kun: suli, banan, baliq\n"
                "7-kun: tuxum, makaron, tovuq"
            )

        if goal == "lose":

            await update.message.reply_text(
                "🔥 7 kunlik ozish dietasi:\n\n"
                "1-kun: tuxum, sabzavot, salat\n"
                "2-kun: tovuq, sabzavot\n"
                "3-kun: baliq, bodring\n"
                "4-kun: tuxum, sabzavot\n"
                "5-kun: tovuq, salat\n"
                "6-kun: baliq, sabzavot\n"
                "7-kun: tuxum, salat"
            )

        await update.message.reply_text(
            "🏋️ 7 kunlik mashq rejasi:\n\n"
            "1-kun: Ko‘krak mashqlari\n"
            "2-kun: Oyoq mashqlari\n"
            "3-kun: Dam olish\n"
            "4-kun: Yelka mashqlari\n"
            "5-kun: Qo‘l mashqlari\n"
            "6-kun: Cardio\n"
            "7-kun: Dam olish"
        )

    else:

        await update.message.reply_text("Iltimos /start bosing")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users_count))
app.add_handler(CommandHandler("send", broadcast))
app.add_handler(MessageHandler(filters.TEXT, message))

app.run_polling()
