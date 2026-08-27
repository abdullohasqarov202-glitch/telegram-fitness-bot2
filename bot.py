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
        "1️⃣  🛡️ PROFESSIONAL SERVER & CYBER SECURITY XIZMATLARI

Serveringiz, VPS, Cloud yoki korporativ infratuzilmangizni professional darajada himoyalashni istaysizmi?

Biz serverlarni audit qilish, zaifliklarni aniqlash, konfiguratsiyani kuchaytirish va monitoring tizimlarini yo‘lga qo‘yish bo‘yicha xizmat ko‘rsatamiz.

🔐 ASOSIY XIZMATLAR

🔹 Server Security Audit — 500 000 so‘mdan
🔹 Linux/Windows Server Hardening — 1 000 000 so‘mdan
🔹 VPS Security — 800 000 so‘mdan
🔹 Firewall sozlash — 500 000 so‘mdan
🔹 SSH/RDP Security — 500 000 so‘mdan
🔹 Web Server Security (Apache/Nginx/IIS) — 1 000 000 so‘mdan
🔹 SSL/TLS Security — 400 000 so‘mdan
🔹 Backup & Recovery tizimi — 1 000 000 so‘mdan
🔹 Server Monitoring — 1 500 000 so‘mdan

🔥 KUCHLIROQ XIZMATLAR

🔸 Vulnerability Assessment — 2 000 000 so‘mdan
Server va xizmatlardagi xavfsizlik zaifliklarini aniqlash.

🔸 Web Application Security Audit — 3 000 000 so‘mdan
Web-ilovadagi xavfsizlik muammolarini tekshirish.

🔸 Penetration Testing — 5 000 000 so‘mdan
Faqat mijozning yozma ruxsati bilan nazorat ostidagi xavfsizlik testi.

🔸 External Infrastructure Pentest — 7 000 000 so‘mdan
Internetga ochiq serverlar, domenlar va xizmatlarning xavfsizlik testi.

🔸 Internal Network Security Audit — 8 000 000 so‘mdan
Ichki tarmoq, serverlar, foydalanuvchi huquqlari va konfiguratsiyalarni audit qilish.

🔸 Active Directory Security Audit — 10 000 000 so‘mdan
Korporativ Windows/AD infratuzilmasining xavfsizlik holatini tekshirish.

🔸 Red Team Assessment — 15 000 000 so‘mdan
Kompaniyaning real hujum ssenariylariga chidamliligini tekshirish. Faqat rasmiy ruxsat asosida.

🔸 SOC / SIEM Monitoring Setup — 10 000 000 so‘mdan
Loglarni yig‘ish, tahlil qilish, alertlar va xavfsizlik monitoringini tashkil qilish.

🔸 Incident Response — 5 000 000 so‘mdan
Server yoki infratuzilmada xavfsizlik hodisasi yuz berganda tekshirish, sababini aniqlash va tiklash.

🔸 Digital Forensics — 8 000 000 so‘mdan
Xavfsizlik hodisasidan keyingi texnik tekshiruv va dalillarni tahlil qilish.

💎 ENTERPRISE SECURITY

🏢 Katta kompaniyalar uchun:

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

💰 Enterprise loyihalar: 20 000 000 – 100 000 000+ so‘m

Narx infratuzilma hajmi, serverlar soni, IP manzillar, domenlar, xodimlar soni va ish hajmiga qarab individual belgilanadi.

⚠️ Eslatma: Pentest, Red Team va boshqa hujum simulyatsiyalari faqat tizim egasining rasmiy yozma ruxsati bilan amalga oshiriladi.

🔒 SERVERINGIZNI HUJUMDAN KEYIN EMAS, HUJUMDAN OLDIN HIMOYALANG!

📩 Xizmat buyurtma qilish uchun Telegram orqali murojaat qiling.
[27.08.2026 13:25] Syber: Ha, bor. Agar Telegram kanal uchun qimmatroq xizmatlar ham tushunarli ko‘rinsin desangiz, xizmatni “nima qilinadi + kimga kerak + taxminiy narx” shaklida yozgan yaxshi.

🛡️ SERVER VA KIBERXAVFSIZLIK XIZMATLARI

Serveringizni shunchaki ishlatib qo‘yish emas, uni hujumlarga chidamli va nazorat qilinadigan holatga keltirish kerak.

Biz Linux, Windows, VPS, Web-server va korporativ tarmoqlar xavfsizligi bo‘yicha professional xizmatlar ko‘rsatamiz.

━━━━━━━━━━━━━━
🔰 1. SERVER SECURITY AUDIT
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

📌 Yakunda aniqlangan muammolar va ularni bartaraf etish bo‘yicha hisobot beriladi.

━━━━━━━━━━━━━━
🔐 2. SERVER HARDENING
💰 1 000 000 – 5 000 000 so‘m

Server xavfsizligi kuchaytiriladi:

• Keraksiz servislar o‘chiriladi
• Firewall sozlanadi
• SSH/RDP himoyalanadi
• Kuchli autentifikatsiya sozlanadi
• Foydalanuvchi huquqlari tartibga keltiriladi
• Yangilanishlar sozlanadi
• Loglash kuchaytiriladi

📌 Maqsad — serverning hujum yuzasini kamaytirish.

━━━━━━━━━━━━━━
🌐 3. WEB-SERVER SECURITY
💰 1 500 000 – 5 000 000 so‘m

Apache / Nginx / IIS serverlari tekshiriladi.

• Web-server konfiguratsiyasi
• SSL/TLS
• HTTP security headers
• Keraksiz endpointlar
• Fayl va katalog huquqlari
• Web-server loglari
• Xavfsizlik sozlamalari

━━━━━━━━━━━━━━
💻 4. WEB APPLICATION SECURITY AUDIT
💰 3 000 000 – 15 000 000 so‘m

Sayt yoki web-ilovaning xavfsizligi tekshiriladi.

Tekshiriladigan yo‘nalishlar:

• Authentication
• Authorization
• Session Security
• Access Control
• Input Validation
• API Security
• Xavfli konfiguratsiyalar
• OWASP Top 10 yo‘nalishlari

📌 Yakunda zaifliklar darajasi va tuzatish bo‘yicha tavsiyalar beriladi.

━━━━━━━━━━━━━━
🎯 5. VULNERABILITY ASSESSMENT
💰 2 000 000 – 10 000 000 so‘m

Infratuzilmadagi ma’lum xavfsizlik zaifliklari aniqlanadi.

Natijada:

🔴 Critical
🟠 High
🟡 Medium
🟢 Low

darajasida risklar ajratiladi.

━━━━━━━━━━━━━━
🧪 6. PENETRATION TEST
💰 5 000 000 – 30 000 000+ so‘m

Rasmiy ruxsat asosida tizim xavfsizligi nazorat ostida sinovdan o‘tkaziladi.

Tekshirilishi mumkin:

• External infrastructure
• Internal network
• Web application
• API
• Serverlar
• Wi-Fi infratuzilmasi

📄 Yakunda professional hisobot tayyorlanadi.

━━━━━━━━━━━━━━
🏢 7. INTERNAL NETWORK SECURITY AUDIT
💰 8 000 000 – 30 000 000+ so‘m

Kompaniyaning ichki tarmog‘i tekshiriladi.

• Router
• Switch
• Server
• Workstation
• VLAN
• Firewall
• User permissions
• Network segmentation

📌 Maqsad — ichki tarmoqdagi xavflarni aniqlash.

━━━━━━━━━━━━━━
🪟 8. ACTIVE DIRECTORY SECURITY AUDIT
💰 10 000 000 – 40 000 000+ so‘m

Windows korporativ infratuzilmasi xavfsizligi tekshiriladi.

• Domain konfiguratsiyasi
• Administrator huquqlari
• Group Policy
• Account security
• Privilege management
• Keraksiz huquqlar
• AD xavfsizlik sozlamalari

━━━━━━━━━━━━━━
☁️ 9. CLOUD SECURITY AUDIT
💰 10 000 000 – 50 000 000+ so‘m

Cloud infratuzilmasi xavfsizligi tekshiriladi.

• Serverlar
• Storage
• IAM
• Network
• Access permissions
• Security configurations
• Logging
• Backup

━━━━━━━━━━━━━━
🚨 10. INCIDENT RESPONSE
💰 5 000 000 – 30 000 000+ so‘m

Agar serverga buzib kirilgan yoki shubhali faoliyat aniqlangan bo‘lsa:

1️⃣ Hodisa aniqlanadi
2️⃣ Tizim tekshiriladi
3️⃣ Shubhali faoliyat tahlil qilinadi
4️⃣ Zararlangan qismlar aniqlanadi
5️⃣ Xavf bartaraf qilinadi
6️⃣ Server tiklanadi
7️⃣ Qayta hujumning oldi olinadi

━━━━━━━━━━━━━━
🔎 11. DIGITAL FORENSICS
💰 8 000 000 – 50 000 000+ so‘m

Xavfsizlik hodisasidan keyin texnik tekshiruv:

• Loglar
• Tizim izlari
• Fayllar
• Jarayonlar
• Account faoliyati
• Tarmoq faoliyati

tahlil qilinadi.

━━━━━━━━━━━━━━
🎯 12. RED TEAM ASSESSMENT
💰 15 000 000 – 100 000 000+ so‘m

Kompaniyaning real hujumlarga qanchalik tayyor ekanligi tekshiriladi.

Bu oddiy pentestdan kengroq bo‘lib, tashkilotning:

• Texnik himoyasi
• Monitoring tizimi
• Xodimlar tayyorgarligi
• Detection & Response jarayonlari

baholanadi.
[27.08.2026 13:25] Syber: ⚠️ Faqat rasmiy yozma ruxsat bilan.

━━━━━━━━━━━━━━
👁️ 13. SIEM / SOC MONITORING
💰 10 000 000 – 100 000 000+ so‘m

Server va tarmoqlardan xavfsizlik loglari yig‘iladi va monitoring qilinadi.

🚨 Shubhali hodisalar aniqlansa alert yuboriladi.

24/7 monitoring ham alohida tashkil qilinishi mumkin.

━━━━━━━━━━━━━━
💾 14. BACKUP & DISASTER RECOVERY
💰 3 000 000 – 30 000 000+ so‘m

Serverdagi muhim ma’lumotlarni yo‘qotib qo‘ymaslik uchun:

• Avtomatik backup
• Off-site backup
• Backup encryption
• Recovery testing
• Disaster Recovery rejasi

tashkil qilinadi.

━━━━━━━━━━━━━━
📊 15. SECURITY CONSULTING
💰 1 000 000 so‘m / sessiyadan

Kompaniyangiz uchun:

• Xavfsizlik strategiyasi
• Risklarni baholash
• Server arxitekturasi
• Network Security
• Access Control
• Backup siyosati
• Security Policy

bo‘yicha maslahat va texnik reja ishlab chiqiladi.

━━━━━━━━━━━━━━
💎 ENTERPRISE SECURITY PACKAGE

💰 20 000 000 – 150 000 000+ so‘m

Katta kompaniyalar uchun kompleks xizmat:

✅ Server Audit
✅ Network Audit
✅ Web Security
✅ AD Security
✅ Cloud Security
✅ Vulnerability Assessment
✅ Penetration Testing
✅ SIEM/SOC
✅ Backup & Recovery
✅ Incident Response rejasi
✅ Security Report
✅ Risk Assessment

📌 Yakuniy narx infratuzilma hajmi va ish ko‘lamiga qarab belgilanadi.

━━━━━━━━━━━━━━

🔒 XAVFSIZLIK — FAQAT ANTIVIRUS O‘RNATISH EMAS.

To‘g‘ri himoya — server, tarmoq, dastur, foydalanuvchi va monitoringni birgalikda nazorat qilishdir.

📩 Serveringiz xavfsizligini tekshirtirish uchun murojaat qiling.

⚠️ Barcha xavfsizlik testlari faqat tizim egasining rasmiy ruxsati bilan amalga oshiriladi. 1\\n"
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
