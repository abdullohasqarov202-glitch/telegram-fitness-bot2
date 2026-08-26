import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# =========================
# 🔑 BOT TOKEN
# =========================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN topilmadi!")


# =========================
# 📢 MAJBURIY KANAL
# =========================

CHANNEL_USERNAME = "@SENING_KANALING"


# =========================
# 👤 FOYDALANUVCHILAR
# =========================

users = {}


# =========================
# 🎛 4 TA ASOSIY TUGMA
# =========================

main_menu = [
    ["❓ Savol berish", "📚 Savollar"],
    ["👤 Profilim", "ℹ️ Yordam"]
]

keyboard = ReplyKeyboardMarkup(
    main_menu,
    resize_keyboard=True
)


# =========================
# 🔍 KANALGA OBUNANI TEKSHIRISH
# =========================

async def check_subscription(bot, user_id):

    try:
        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as e:
        print("❌ Obunani tekshirish xatosi:", e)
        return False


# =========================
# 📢 OBUNA TUGMASI
# =========================

def subscription_keyboard():

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Kanalga obuna bo‘lish",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Obunani tekshirish",
                callback_data="check_subscription"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# 🚀 START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    users[user.id] = {
        "name": user.first_name
    }

    subscribed = await check_subscription(
        context.bot,
        user.id
    )

    # OBUNA YO‘Q
    if not subscribed:

        await update.message.reply_text(
            f"👋 Salom, <b>{user.first_name}</b>!\n\n"
            "🤖 <b>Savol-javob botiga xush kelibsiz!</b>\n\n"
            "Botdan foydalanish uchun avval "
            "kanalimizga obuna bo‘ling 👇\n\n"
            "📢 Kanalga obuna bo‘lish majburiy.\n\n"
            "Obuna bo‘lgach, "
            "«✅ Obunani tekshirish» tugmasini bosing.",
            parse_mode="HTML",
            reply_markup=subscription_keyboard()
        )

        return

    # OBUNA BOR
    await update.message.reply_text(
        f"👋 Salom, <b>{user.first_name}</b>!\n\n"
        "🤖 <b>Savol-javob botiga xush kelibsiz!</b>\n\n"
        "Kerakli bo‘limni tanlang 👇",
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =========================
# ✅ OBUNANI TEKSHIRISH
# =========================

async def check_subscription_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    user = query.from_user

    subscribed = await check_subscription(
        context.bot,
        user.id
    )

    if subscribed:

        await query.answer(
            "✅ Obuna tasdiqlandi!"
        )

        try:
            await query.message.delete()
        except:
            pass

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                f"🎉 <b>Obuna tasdiqlandi!</b>\n\n"
                f"👋 Salom, <b>{user.first_name}</b>!\n\n"
                "🤖 Endi botdan foydalanishingiz mumkin.\n\n"
                "Kerakli bo‘limni tanlang 👇"
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )

    else:

        await query.answer(
            "❌ Avval kanalga obuna bo‘ling!",
            show_alert=True
        )


# =========================
# ❓ SAVOL BERISH
# =========================

async def ask_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not await check_subscription(
        context.bot,
        user.id
    ):

        await update.message.reply_text(
            "🚫 Avval kanalga obuna bo‘ling!",
            reply_markup=subscription_keyboard()
        )

        return

    await update.message.reply_text(
        "❓ <b>Savol berish</b>\n\n"
        "Savolingizni yozib yuboring 👇",
        parse_mode="HTML"
    )


# =========================
# 📚 SAVOLLAR
# =========================

async def questions(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📚 <b>Ko‘p beriladigan savollar</b>\n\n"
        "1️⃣ Bot qanday ishlaydi?\n"
        "2️⃣ Savolga qanday javob olaman?\n"
        "3️⃣ Botdan foydalanish bepulmi?",
        parse_mode="HTML"
    )


# =========================
# 👤 PROFIL
# =========================

async def profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    username = (
        f"@{user.username}"
        if user.username
        else "Username yo‘q"
    )

    await update.message.reply_text(
        "👤 <b>Profilim</b>\n\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"👤 Ism: {user.first_name}\n"
        f"🔗 Username: {username}",
        parse_mode="HTML"
    )


# =========================
# ℹ️ YORDAM
# =========================

async def help_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "ℹ️ <b>Yordam</b>\n\n"
        "❓ Savol berish — savolingizni yuborish.\n"
        "📚 Savollar — ko‘p beriladigan savollar.\n"
        "👤 Profilim — profilingizni ko‘rish.\n\n"
        "Botdan foydalanish uchun kanalga "
        "obuna bo‘lish talab qilinadi.",
        parse_mode="HTML"
    )


# =========================
# 💬 MATNLARNI QABUL QILISH
# =========================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    if text == "❓ Savol berish":

        await ask_question(
            update,
            context
        )

    elif text == "📚 Savollar":

        await questions(
            update,
            context
        )

    elif text == "👤 Profilim":

        await profile(
            update,
            context
        )

    elif text == "ℹ️ Yordam":

        await help_button(
            update,
            context
        )

    else:

        await update.message.reply_text(
            "🤔 Iltimos, menyudagi tugmalardan birini tanlang 👇",
            reply_markup=keyboard
        )


# =========================
# ▶️ BOTNI ISHGA TUSHIRISH
# =========================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # START
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # OBUNANI TEKSHIRISH
    app.add_handler(
        CallbackQueryHandler(
            check_subscription_callback,
            pattern="^check_subscription$"
        )
    )

    # MATNLAR
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("🤖 Bot ishga tushdi...")

    app.run_polling()


# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    main()
