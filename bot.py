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

CHANNEL_USERNAME = "@moonsecurityy"


# =========================
# 👤 FOYDALANUVCHILAR
# =========================

users = {}


# =========================
# 🎛 2 TA ASOSIY TUGMA
# =========================

main_menu = [
    ["🛠 Xizmatlar", "👤 Admin"]
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
            "🤖 <b> Moon Securty botiga xush kelibsiz!</b>\n\n"
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
        "🤖 <b>Moon Securty botiga xush kelibsiz!</b>\n\n"
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
# 🛠 XIZMATLAR
# =========================

async def services(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # 👇 SHU JOYNI KEYIN O‘ZING TO‘LDIRASAN

    
    await update.message.reply_text(
        "🛠 <b>Xizmatlar</b>\n\n"
        "\n\n"
        "1️⃣ Xizmat 1\n"
        "2️⃣ Xizmat 2\n"
        "3️⃣ Xizmat 3\n\n"
        "📌 Ma'lumotlar tez orada qo‘shiladi.",
        parse_mode="HTML"
    )


# =========================
# 👤 ADMIN
# =========================

async def admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # 👇 SHU JOYNI KEYIN O‘ZING TO‘LDIRASAN

    await update.message.reply_text(
        "👤 <b>Admin</b>\n\n"
        "Admin bilan bog‘lanish uchun:\n\n"
        "📩 Admin: @Moonnadmin\n\n"
        "📱 Nomwer: 90 629 19 12 ",
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

    # 🛠 XIZMATLAR
    if text == "🛠 Xizmatlar":

        await services(
            update,
            context
        )

    # 👤 ADMIN
    elif text == "👤 Admin":

        await admin(
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
