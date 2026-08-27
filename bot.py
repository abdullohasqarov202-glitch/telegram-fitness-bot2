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


# =========================================================
# 🔑 BOT TOKENI
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi!")


# =========================================================
# 📢 MAJBURIY KANAL
# =========================================================

CHANNEL_USERNAME = "@moonsecurityy"


# =========================================================
# 👥 FOYDALANUVCHILAR
# =========================================================

users = {}


# =========================================================
# 🎛 ASOSIY MENYU
# =========================================================

main_menu = [
    ["📚 Xizmatlar", "👤 Admin"]
]

keyboard = ReplyKeyboardMarkup(
    main_menu,
    resize_keyboard=True
)


# =========================================================
# 🔍 KANALGA OBUNANI TEKSHIRISH
# =========================================================

async def check_subscription(bot, user_id):

    try:

        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as e:

        print("Obunani tekshirish xatosi:", e)

        return False


# =========================================================
# 📢 OBUNA TUGMALARI
# =========================================================

def subscription_keyboard():

    buttons = [

        [
            InlineKeyboardButton(
                "📢 Kanalga obuna bo‘lish",
                url="https://t.me/moonsecurityy"
            )
        ],

        [
            InlineKeyboardButton(
                "✅ Obunani tekshirish",
                callback_data="check_subscription"
            )
        ]

    ]

    return InlineKeyboardMarkup(buttons)


# =========================================================
# 🚀 START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    users[user.id] = {
        "name": user.first_name,
        "username": user.username
    }

    subscribed = await check_subscription(
        context.bot,
        user.id
    )

    # -----------------------------------------------------
    # OBUNA YO'Q
    # -----------------------------------------------------

    if not subscribed:

        await update.message.reply_text(

            f"👋 Salom, {user.first_name}!\n\n"

            "🤖 <b>Moon Security</b> xizmatlar botiga "
            "xush kelibsiz!\n\n"

            "Botdan foydalanish uchun avval "
            "kanalimizga obuna bo‘ling.\n\n"

            "📢 <b>Majburiy obuna</b>\n\n"

            "Kanalga obuna bo‘lgach, "
            "«✅ Obunani tekshirish» tugmasini bosing 👇",

            parse_mode="HTML",

            reply_markup=subscription_keyboard()
        )

        return


    # -----------------------------------------------------
    # OBUNA BOR
    # -----------------------------------------------------

    await update.message.reply_text(

        f"👋 Salom, <b>{user.first_name}</b>!\n\n"

        "🛡 <b>Moon Security</b> botiga xush kelibsiz!\n\n"

        "🔐 Kiberxavfsizlik va server xavfsizligi "
        "xizmatlaridan foydalanishingiz mumkin.\n\n"

        "Kerakli bo‘limni tanlang 👇",

        parse_mode="HTML",

        reply_markup=keyboard
    )


# =========================================================
# ✅ OBUNANI TEKSHIRISH
# =========================================================

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

        except Exception:

            pass

        await context.bot.send_message(

            chat_id=query.message.chat_id,

            text=(

                f"🎉 <b>Obuna tasdiqlandi!</b>\n\n"

                f"👋 Salom, <b>{user.first_name}</b>!\n\n"

                "🛡 Endi botdan foydalanishingiz mumkin.\n\n"

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


# =========================================================
# 📚 XIZMATLAR
# =========================================================

async def services(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # Avval obunani tekshiramiz

    if not await check_subscription(
        context.bot,
        update.effective_user.id
    ):

        await update.message.reply_text(

            "🚫 Avval kanalga obuna bo‘ling!",

            reply_markup=subscription_keyboard()
        )

        return


    text = """

🔐 <b>MOON SECURITY XIZMATLARI</b>

━━━━━━━━━━━━━━━━━━

🔰 <b>1. SERVER SECURITY AUDIT</b>

💰 500 000 – 2 000 000 so‘m

Serveringiz tekshiriladi:

• Ochiq portlar
• Ishlayotgan servislar
• SSH/RDP sozlamalari
• Foydalanuvchi huquqlari
• Firewall
• Eski dasturlar
• Zaif konfiguratsiyalar
• Loglar


━━━━━━━━━━━━━━━━━━

🔐 <b>2. SERVER HARDENING</b>

💰 1 000 000 – 5 000 000 so‘m

Server xavfsizligi kuchaytiriladi:

• Keraksiz servislar o‘chiriladi
• Firewall sozlanadi
• SSH/RDP himoyalanadi
• Foydalanuvchi huquqlari tartibga keltiriladi
• Yangilanishlar sozlanadi
• Loglash kuchaytiriladi


━━━━━━━━━━━━━━━━━━

🌐 <b>3. WEB-SERVER SECURITY</b>

💰 1 500 000 – 5 000 000 so‘m

Apache / Nginx / IIS serverlari tekshiriladi.

• Web-server konfiguratsiyasi
• SSL/TLS
• HTTP security headers
• Keraksiz endpointlar
• Fayl va katalog huquqlari
• Web-server loglari
• Xavfsizlik sozlamalari
• Kuchli autentifikatsiya
• Foydalanuvchi huquqlari
• Yangilanishlar
• Loglash


━━━━━━━━━━━━━━━━━━

🔸 <b>4. VULNERABILITY ASSESSMENT</b>

💰 2 000 000 so‘mdan

Server va xizmatlardagi xavfsizlik zaifliklarini aniqlash.


━━━━━━━━━━━━━━━━━━

🔸 <b>5. WEB APPLICATION SECURITY AUDIT</b>

💰 3 000 000 so‘mdan

Web-ilovadagi xavfsizlik muammolarini tekshirish.


━━━━━━━━━━━━━━━━━━

🔸 <b>6. PENETRATION TESTING</b>

💰 5 000 000 so‘mdan

Faqat mijozning yozma ruxsati bilan nazorat ostidagi xavfsizlik testi.


━━━━━━━━━━━━━━━━━━

🔸 <b>7. EXTERNAL INFRASTRUCTURE PENTEST</b>

💰 7 000 000 so‘mdan

Internetga ochiq serverlar, domenlar va xizmatlarning xavfsizlik testi.


━━━━━━━━━━━━━━━━━━

🔸 <b>8. INTERNAL NETWORK SECURITY AUDIT</b>

💰 8 000 000 so‘mdan

Ichki tarmoq, serverlar, foydalanuvchi huquqlari va konfiguratsiyalarni audit qilish.


━━━━━━━━━━━━━━━━━━

🔸 <b>9. ACTIVE DIRECTORY SECURITY AUDIT</b>

💰 10 000 000 so‘mdan

Korporativ Windows/AD infratuzilmasining xavfsizlik holatini tekshirish.


━━━━━━━━━━━━━━━━━━

🔸 <b>10. RED TEAM ASSESSMENT</b>

💰 15 000 000 so‘mdan

Kompaniyaning real hujum ssenariylariga chidamliligini tekshirish.

⚠️ Faqat rasmiy ruxsat asosida.


━━━━━━━━━━━━━━━━━━

🔸 <b>11. SOC / SIEM MONITORING SETUP</b>

💰 10 000 000 so‘mdan

Loglarni yig‘ish, tahlil qilish, alertlar va xavfsizlik monitoringini tashkil qilish.


━━━━━━━━━━━━━━━━━━

🔸 <b>12. INCIDENT RESPONSE</b>

💰 5 000 000 so‘mdan

Server yoki infratuzilmada xavfsizlik hodisasi yuz berganda tekshirish, sababini aniqlash va tiklash.


━━━━━━━━━━━━━━━━━━

🔸 <b>13. DIGITAL FORENSICS</b>

💰 8 000 000 so‘mdan

Xavfsizlik hodisasidan keyingi texnik tekshiruv va dalillarni tahlil qilish.


━━━━━━━━━━━━━━━━━━

🏢 <b>KATTA KOMPANIYALAR UCHUN</b>

• Bir nechta serverlarni kompleks audit qilish
• Cloud Security Audit
• Network Security Assessment
• Active Directory Security
• SIEM/SOC integratsiyasi
• 24/7 monitoring
• Incident Response
• Vulnerability Management
• Security Policy ishlab chiqish
• Risk Assessment
• Red Team / Purple Team mashg‘ulotlari


━━━━━━━━━━━━━━━━━━

💰 <b>ENTERPRISE LOYIHALAR</b>

20 000 000 – 100 000 000+ so‘m

Narx infratuzilma hajmi, serverlar soni,
IP manzillar, domenlar, xodimlar soni
va ish hajmiga qarab individual belgilanadi.

━━━━━━━━━━━━━━━━━━

📩 Batafsil ma’lumot uchun:
👤 Admin bilan bog‘laning @Moonnadmin
"""

    await update.message.reply_text(

        text,

        parse_mode="HTML",

        reply_markup=keyboard
    )


# =========================================================
# 👤 ADMIN
# =========================================================

async def admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not await check_subscription(
        context.bot,
        update.effective_user.id
    ):

        await update.message.reply_text(

            "🚫 Avval kanalga obuna bo‘ling!",

            reply_markup=subscription_keyboard()
        )

        return


    await update.message.reply_text(

        "👤 <b>ADMIN BILAN BOG‘LANISH</b>\n\n"

        "📩 Xizmatlar bo‘yicha murojaat qilish uchun "
        "admin bilan bog‘laning.\n\n"

        "🛡 Server Security\n"
        "🌐 Web Security\n"
        "🔐 Pentest\n"
        "🏢 Enterprise Security\n\n"

        "👇 Admin bilan bog‘lanish:",

        parse_mode="HTML",

        reply_markup=InlineKeyboardMarkup([

            [
                InlineKeyboardButton(
                    "👤 Admin bilan bog‘lanish",
                    url="https://t.me/Asqarov_0207"
                )
            ]

        ])
    )


# =========================================================
# 💬 MATNLARNI QABUL QILISH
# =========================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text


    # XIZMATLAR

    if text == "📚 Xizmatlar":

        await services(
            update,
            context
        )

        return


    # ADMIN

    if text == "👤 Admin":

        await admin(
            update,
            context
        )

        return


    # BOSHQA MATN

    await update.message.reply_text(

        "🤔 Iltimos, menyudagi tugmalardan birini tanlang 👇",

        reply_markup=keyboard
    )


# =========================================================
# ▶️ BOTNI ISHGA TUSHIRISH
# =========================================================

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


    print("Bot ishga tushdi...")


    app.run_polling()


# =========================================================
# 🚀 RUN
# =========================================================

if __name__ == "__main__":
    main()
