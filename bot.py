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
       # ============================================================
# TUZATILGAN KOD — 3 ta xabar, har biri alohida o'zgaruvchida
# Har bir qator \n bilan ajratilgan, hammasi bir qatorli
# string literal ichida — shuning uchun sintaksis xatosi bo'lmaydi.
# ============================================================

MESSAGE_1 = (
    "1️⃣ 🔹 Server Security Audit — 500 000 so'mdan\n"
    "🔹 Linux/Windows Server Hardening — 1 000 000 so'mdan\n"
    "🔹 VPS Security — 800 000 so'mdan\n"
    "🔹 Firewall sozlash — 500 000 so'mdan\n"
    "🔹 SSH/RDP Security — 500 000 so'mdan\n"
    "🔹 Web Server Security (Apache/Nginx/IIS) — 1 000 000 so'mdan\n"
    "🔹 SSL/TLS Security — 400 000 so'mdan\n"
    "🔹 Backup & Recovery tizimi — 1 000 000 so'mdan\n"
    "🔹 Server Monitoring — 1 500 000 so'mdan\n\n"
    "🔸 Vulnerability Assessment — 2 000 000 so'mdan\n"
    "Server va xizmatlardagi xavfsizlik zaifliklarini aniqlash.\n"
    "🔸 Web Application Security Audit — 3 000 000 so'mdan\n"
    "Web-ilovadagi xavfsizlik muammolarini tekshirish.\n"
    "🔸 Penetration Testing — 5 000 000 so'mdan\n"
    "Faqat mijozning yozma ruxsati bilan nazorat ostidagi xavfsizlik testi.\n"
    "🔸 External Infrastructure Pentest — 7 000 000 so'mdan\n"
    "Internetga ochiq serverlar, domenlar va xizmatlarning xavfsizlik testi.\n"
    "🔸 Internal Network Security Audit — 8 000 000 so'mdan\n"
    "Ichki tarmoq, serverlar, foydalanuvchi huquqlari va konfiguratsiyalarni audit qilish.\n"
    "🔸 Active Directory Security Audit — 10 000 000 so'mdan\n"
    "Korporativ Windows/AD infratuzilmasining xavfsizlik holatini tekshirish.\n"
    "🔸 Red Team Assessment — 15 000 000 so'mdan\n"
    "Kompaniyaning real hujum ssenariylariga chidamliligini tekshirish. Faqat rasmiy ruxsat asosida.\n"
    "🔸 SOC / SIEM Monitoring Setup — 10 000 000 so'mdan\n"
    "Loglarni yig'ish, tahlil qilish, alertlar va xavfsizlik monitoringini tashkil qilish.\n"
    "🔸 Incident Response — 5 000 000 so'mdan\n"
    "Server yoki infratuzilmada xavfsizlik hodisasi yuz berganda tekshirish, sababini aniqlash va tiklash.\n"
    "🔸 Digital Forensics — 8 000 000 so'mdan\n"
    "Xavfsizlik hodisasidan keyingi texnik tekshiruv va dalillarni tahlil qilish.\n"
)

MESSAGE_2 = (
    "2️⃣ 1. SERVER SECURITY AUDIT\n"
    "💰 500 000 – 2 000 000 so'm\n"
    "Serveringiz tekshiriladi:\n"
    "• Ochiq portlar\n"
    "• Ishlayotgan servislar\n"
    "• SSH/RDP sozlamalari\n"
    "• Foydalanuvchi huquqlari\n"
    "• Firewall\n"
    "• Eski dasturlar\n"
    "• Zaif konfiguratsiyalar\n"
    "• Loglar\n\n"
    "🔐 2. SERVER HARDENING\n"
    "💰 1 000 000 – 5 000 000 so'm\n"
    "Server xavfsizligi kuchaytiriladi:\n"
    "• Keraksiz servislar o'chiriladi\n"
    "• Firewall sozlanadi\n"
    "• SSH/RDP himoyalanadi\n"
    "🌐 3. WEB-SERVER SECURITY\n"
    "💰 1 500 000 – 5 000 000 so'm\n"
    "Apache / Nginx / IIS serverlari tekshiriladi.\n"
    "• Web-server konfiguratsiyasi\n"
    "• SSL/TLS\n"
    "• HTTP security headers\n"
    "• Keraksiz endpointlar\n"
    "• Fayl va katalog huquqlari\n"
    "• Web-server loglari\n"
    "• Xavfsizlik sozlamalari\n"
    "• Kuchli autentifikatsiya sozlanadi\n"
    "• Foydalanuvchi huquqlari tartibga keltiriladi\n"
    "• Yangilanishlar sozlanadi\n"
    "• Loglash kuchaytiriladi\n"
)

MESSAGE_3 = (
    "3️⃣ 🏢 Katta kompaniyalar uchun:\n"
    "• Bir nechta serverlarni kompleks audit qilish\n"
    "• Cloud Security Audit\n"
    "• Network Security Assessment\n"
    "• Active Directory Security\n"
    "• SIEM/SOC integratsiyasi\n"
    "• 24/7 monitoring\n"
    "• Incident Response\n"
    "• Vulnerability Management\n"
    "• Security Policy ishlab chiqish\n"
    "• Risk Assessment\n"
    "• Red Team / Purple Team mashg'ulotlari\n"
    "💰 Enterprise loyihalar: 20 000 000 – 100 000 000+ so'm\n"
    "Narx infratuzilma hajmi, serverlar soni, IP manzillar, domenlar, xodimlar soni va ish hajmiga qarab individual belgilanadi.\n\n"
)

# ============================================================
# Botda ishlatish:
# ============================================================
#
# async def send_services(update, context):
#     await update.message.reply_text(MESSAGE_1)
#     await update.message.reply_text(MESSAGE_2)
#     await update.message.reply_text(MESSAGE_3)
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
        "📱 Nomer: 90 629 19 12 ",
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
