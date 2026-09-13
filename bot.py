import telebot, requests, re, sqlite3, datetime, json, os, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = "8622116851:AAGFGCmwV6ijVGxEpLsVBW7LQbmZvqElmTk"
ADMIN_ID = 6936978343

NUMBER_API_URL = "https://anurixx-gift-number.vercel.app/api"
NUMBER_SPECIAL_URL = "https://num-info-redzone.susxbunny.workers.dev/api"
NUMBER_API_KEY = "paid_key@REDZONE21"
AADHAAR_API_URL = "https://leak-osint-redzone.vercel.app/api"
AADHAAR_API_KEY = "REDZONE"
VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"

OWNER = "@Cyber_With_Ranjan"
INSTA = "https://www.instagram.com/ranjan_bhai_194?igsh=ZTM2enVsNmt3MnJv"
WEBSITE = "https://cyberwithranjan.in"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
SUPPORT_GROUP = "https://t.me/cyberwithranjan"
UPI_ID = "desi.hacker@ybl"

QR_PATH = os.path.join(os.path.dirname(__file__), 'qr.png')
bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT, first_name TEXT,
    lang TEXT DEFAULT 'en',
    coins INTEGER DEFAULT 0,
    last_claim TEXT,
    access INTEGER DEFAULT 0,
    premium INTEGER DEFAULT 0,
    premium_expiry TEXT,
    searches INTEGER DEFAULT 0,
    insta_followed INTEGER DEFAULT 0,
    website_visited INTEGER DEFAULT 0
)''')
conn.commit()

# ==================== LANGUAGES ====================
L = {
    'en': {'lang': "🌐 **Select Language:**", 'welcome': "🎁 **Welcome to OSINT Bot!**\n\n🪙 **FREE Daily Coin**\n• Claim 1 coin every day for FREE\n• 1 Coin = 1 Search\n\n💎 **Premium Plans**\n• 1 Day – ₹10\n• 1 Week – ₹60\n• 1 Month – ₹101\n\n📸 Scan QR below to buy premium\n👇 Or claim your FREE coin now!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 Buy Premium", 'already_claimed': "✅ Aaj ka coin already claim kar chuke ho!\n\n⏰ Kal phir aana", 'coin_claimed': "🎉 **Congratulations!**\n\n🪙 You got 1 FREE Coin!\n🪙 Total Coins: {coins}\n\n✅ Now you can search any info!", 'main_menu': "📱 **Main Menu**", 'search': "🔍 Search", 'premium': "💎 Premium", 'number': "📱 Number", 'vehicle': "🚗 Vehicle", 'vehicle_special': "🚘 Vehicle Special", 'aadhaar': "🆔 Aadhaar", 'profile_btn': "👤 Profile", 'help_btn': "❓ Help", 'about_btn': "ℹ️ About", 'clear_btn': "🗑️ Clear", 'back': "🔙 Back", 'owner': "👨‍💻 Owner", 'admin_only': "⚠️ Not authorized.", 'enter_number': "📱 Send 10-digit number:", 'enter_vehicle': "🚗 Send vehicle number:", 'enter_vehicle_special': "🚘 Send vehicle for Special:", 'enter_aadhaar': "🆔 Send 12-digit Aadhaar:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **Profile**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 Premium: {prem}\n🔍 Searches: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ No coins! Claim daily 1 FREE coin.", 'stats_text': "📊 Stats\n👥 Total: {total}\n💎 Premium: {premium}\n🪙 Coins: {coins}\n🔍 Searches: {searches}"},
    'hi': {'lang': "🌐 **भाषा चुनें:**", 'welcome': "🎁 **OSINT Bot में स्वागत है!**\n\n🪙 **FREE Daily Coin**\n• रोज 1 FREE Coin claim करें\n• 1 Coin = 1 Search\n\n💎 **प्रीमियम प्लान**\n• 1 दिन – ₹10\n• 1 सप्ताह – ₹60\n• 1 महीना – ₹101\n\n📸 QR स्कैन करके premium खरीदें\n👇 या अभी FREE coin claim करें!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरीदें", 'already_claimed': "✅ आज का coin already claim कर चुके हो!\n\n⏰ कल फिर आना", 'coin_claimed': "🎉 **बधाई हो!**\n\n🪙 आपको 1 FREE Coin मिला!\n🪙 Total Coins: {coins}\n\n✅ अब आप कोई भी info search कर सकते हैं!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 खोज", 'premium': "💎 प्रीमियम", 'number': "📱 नंबर", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Special", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदद", 'about_btn': "ℹ️ जानकारी", 'clear_btn': "🗑️ साफ करें", 'back': "🔙 वापस", 'owner': "👨‍💻 मालिक", 'admin_only': "⚠️ अधिकृत नहीं।", 'enter_number': "📱 10 अंकों का नंबर भेजें:", 'enter_vehicle': "🚗 वाहन नंबर भेजें:", 'enter_vehicle_special': "🚘 Special वाहन:", 'enter_aadhaar': "🆔 12 अंकों का आधार:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नहीं! रोज 1 FREE coin claim करें।", 'stats_text': "📊 आँकड़े\n👥 कुल: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 खोज: {searches}"},
    'bn': {'lang': "🌐 **ভাষা নির্বাচন করুন:**", 'welcome': "🎁 **OSINT Bot এ স্বাগতম!**\n\n🪙 **FREE Daily Coin**\n• প্রতিদিন ১টি FREE Coin\n• ১ Coin = ১ Search\n\n💎 **প্রিমিয়াম প্ল্যান**\n• ১ দিন – ₹১০\n• ১ সপ্তাহ – ₹৬০\n• ১ মাস – ₹১০১\n\n📸 QR স্ক্যান করুন\n👇 অথবা FREE coin claim করুন!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 প্রিমিয়াম কিনুন", 'already_claimed': "✅ আজকের coin ইতিমধ্যে claim করেছেন!\n\n⏰ কাল আবার আসুন", 'coin_claimed': "🎉 **অভিনন্দন!**\n\n🪙 ১টি FREE Coin পেয়েছেন!\n🪙 Total Coins: {coins}\n\n✅ এখন যেকোনো info search করুন!", 'main_menu': "📱 **মেনু**", 'search': "🔍 অনুসন্ধান", 'premium': "💎 প্রিমিয়াম", 'number': "📱 নম্বর", 'vehicle': "🚗 গাড়ি", 'vehicle_special': "🚘 গাড়ি স্পেশাল", 'aadhaar': "🆔 আধার", 'profile_btn': "👤 প্রোফাইল", 'help_btn': "❓ সাহায্য", 'about_btn': "ℹ️ তথ্য", 'clear_btn': "🗑️ মুছুন", 'back': "🔙 ফিরে", 'owner': "👨‍💻 মালিক", 'admin_only': "⚠️ অনুমতি নেই।", 'enter_number': "📱 ১০ অঙ্কের নম্বর:", 'enter_vehicle': "🚗 গাড়ির নম্বর:", 'enter_vehicle_special': "🚘 স্পেশাল গাড়ি:", 'enter_aadhaar': "🆔 ১২ অঙ্কের আধার:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **প্রোফাইল**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 প্রিমিয়াম: {prem}\n🔍 অনুসন্ধান: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin নেই! দৈনিক ১ FREE coin নিন।", 'stats_text': "📊 পরিসংখ্যান\n👥 মোট: {total}\n💎 প্রিমিয়াম: {premium}\n🪙 Coins: {coins}\n🔍 অনুসন্ধান: {searches}"},
    'mr': {'lang': "🌐 **भाषा निवडा:**", 'welcome': "🎁 **OSINT Bot मध्ये स्वागत!**\n\n🪙 **FREE Daily Coin**\n• रोज १ FREE Coin\n• १ Coin = १ Search\n\n💎 **प्रीमियम प्लान**\n• १ दिवस – ₹१०\n• १ आठवडा – ₹६०\n• १ महिना – ₹१०१\n\n📸 QR स्कॅन करा\n👇 किंवा FREE coin claim करा!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरेदी", 'already_claimed': "✅ आजचा coin आधीच claim केला!\n\n⏰ उद्या पुन्हा या", 'coin_claimed': "🎉 **अभिनंदन!**\n\n🪙 १ FREE Coin मिळाला!\n🪙 Total Coins: {coins}\n\n✅ आता कोणतीही info शोधा!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 शोध", 'premium': "💎 प्रीमियम", 'number': "📱 क्रमांक", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन स्पेशल", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदत", 'about_btn': "ℹ️ माहिती", 'clear_btn': "🗑️ साफ करा", 'back': "🔙 मागे", 'owner': "👨‍💻 मालक", 'admin_only': "⚠️ अधिकार नाही.", 'enter_number': "📱 १० अंकी क्रमांक:", 'enter_vehicle': "🚗 वाहन क्रमांक:", 'enter_vehicle_special': "🚘 स्पेशल वाहन:", 'enter_aadhaar': "🆔 १२ अंकी आधार:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 शोध: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नाही! रोज १ FREE coin.", 'stats_text': "📊 आकडेवारी\n👥 एकूण: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 शोध: {searches}"},
    'ur': {'lang': "🌐 **زبان منتخب کریں:**", 'welcome': "🎁 **OSINT Bot میں خوش آمدید!**\n\n🪙 **FREE Daily Coin**\n• روزانہ ۱ FREE Coin\n• ۱ Coin = ۱ Search\n\n💎 **پریمیم پلان**\n• ۱ دن – ₹۱۰\n• ۱ ہفتہ – ₹۶۰\n• ۱ مہینہ – ₹۱۰۱\n\n📸 QR اسکین کریں\n👇 یا FREE coin claim کریں!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 پریمیم خریدیں", 'already_claimed': "✅ آج کا coin پہلے claim کر چکے!\n\n⏰ کل پھر آئیں", 'coin_claimed': "🎉 **مبارک ہو!**\n\n🪙 ۱ FREE Coin ملا!\n🪙 Total Coins: {coins}\n\n✅ اب کوئی بھی info search کریں!", 'main_menu': "📱 **مین مینو**", 'search': "🔍 تلاش", 'premium': "💎 پریمیم", 'number': "📱 نمبر", 'vehicle': "🚗 گاڑی", 'vehicle_special': "🚘 گاڑی سپیشل", 'aadhaar': "🆔 آدھار", 'profile_btn': "👤 پروفائل", 'help_btn': "❓ مدد", 'about_btn': "ℹ️ معلومات", 'clear_btn': "🗑️ صاف", 'back': "🔙 واپس", 'owner': "👨‍💻 مالک", 'admin_only': "⚠️ مجاز نہیں۔", 'enter_number': "📱 ۱۰ ہندسی نمبر:", 'enter_vehicle': "🚗 گاڑی نمبر:", 'enter_vehicle_special': "🚘 سپیشل گاڑی:", 'enter_aadhaar': "🆔 ۱۲ ہندسی آدھار:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **پروفائل**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 پریمیم: {prem}\n🔍 تلاش: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin نہیں! روزانہ ۱ FREE coin لیں۔", 'stats_text': "📊 اعداد\n👥 کل: {total}\n💎 پریمیم: {premium}\n🪙 Coins: {coins}\n🔍 تلاش: {searches}"},
    'ta': {'lang': "🌐 **மொழியைத் தேர்ந்தெடுக்கவும்:**", 'welcome': "🎁 **OSINT Bot க்கு வரவேற்கிறோம்!**\n\n🪙 **FREE Daily Coin**\n• தினமும் 1 FREE Coin\n• 1 Coin = 1 Search\n\n💎 **பிரீமியம் திட்டம்**\n• 1 நாள் – ₹10\n• 1 வாரம் – ₹60\n• 1 மாதம் – ₹101\n\n📸 QR ஸ்கேன் செய்யவும்\n👇 அல்லது FREE coin claim செய்யுங்கள்!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 பிரீமியம் வாங்க", 'already_claimed': "✅ இன்றைய coin ஏற்கனவே claim! \n\n⏰ நாளை மீண்டும் வாருங்கள்", 'coin_claimed': "🎉 **வாழ்த்துக்கள்!**\n\n🪙 1 FREE Coin கிடைத்தது!\n🪙 Total Coins: {coins}\n\n✅ இப்போது எந்த info search செய்யுங்கள்!", 'main_menu': "📱 **மெனு**", 'search': "🔍 தேடு", 'premium': "💎 பிரீமியம்", 'number': "📱 எண்", 'vehicle': "🚗 வாகனம்", 'vehicle_special': "🚘 வாகனம் ஸ்பெஷல்", 'aadhaar': "🆔 ஆதார்", 'profile_btn': "👤 சுயவிவரம்", 'help_btn': "❓ உதவி", 'about_btn': "ℹ️ தகவல்", 'clear_btn': "🗑️ அழி", 'back': "🔙 பின்", 'owner': "👨‍💻 உரிமை", 'admin_only': "⚠️ அனுமதி இல்லை.", 'enter_number': "📱 10 இலக்க எண்:", 'enter_vehicle': "🚗 வாகன எண்:", 'enter_vehicle_special': "🚘 ஸ்பெஷல் வாகனம்:", 'enter_aadhaar': "🆔 12 இலக்க ஆதார்:", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **சுயவிவரம்**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 பிரீமியம்: {prem}\n🔍 தேடல்: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin இல்லை! தினமும் 1 FREE coin.", 'stats_text': "📊 புள்ளி\n👥 மொத்தம்: {total}\n💎 பிரீமியம்: {premium}\n🪙 Coins: {coins}\n🔍 தேடல்: {searches}"}
}

# ==================== HELPERS ====================
def gl(i):
    try:
        c.execute("SELECT lang FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        return r[0] if r else 'en'
    except: return 'en'

def sl(i, l):
    try:
        c.execute("UPDATE users SET lang=? WHERE user_id=?", (l, i)); conn.commit()
    except: pass

def ensure_user(i, name="User", un=""):
    try:
        c.execute("INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?, ?, ?)", (i, name, un))
        conn.commit()
    except: pass

def au(i, n, u=""):
    ensure_user(i, n, u)

def gc(i):
    try:
        c.execute("SELECT coins FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        return r[0] if r else 0
    except: return 0

def dc(i):
    try:
        if ip(i):
            c.execute("UPDATE users SET searches=searches+1 WHERE user_id=?", (i,)); conn.commit()
            return True
        coins = gc(i)
        if coins <= 0: return False
        c.execute("UPDATE users SET coins=coins-1, searches=searches+1 WHERE user_id=?", (i,)); conn.commit()
        return True
    except: return False

def claim_daily_coin(i):
    try:
        ensure_user(i)
        t = datetime.datetime.now().date().isoformat()
        c.execute("SELECT last_claim FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        if r and r[0] == t: return False
        c.execute("UPDATE users SET coins=coins+1, last_claim=?, access=1 WHERE user_id=?", (t, i))
        conn.commit()
        return True
    except: return False

def ip(i):
    if i == ADMIN_ID: return True
    try:
        c.execute("SELECT premium, premium_expiry FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        if not r or r[0] == 0: return False
        if r[1]:
            try:
                if datetime.datetime.fromisoformat(r[1]) > datetime.datetime.now(): return True
            except: return True
            c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (i,)); conn.commit()
            return False
        return True
    except: return False

def ap(i, d=30):
    try:
        ensure_user(i, "Admin_Added")
        e = (datetime.datetime.now() + datetime.timedelta(days=d)).isoformat()
        c.execute("UPDATE users SET premium=1, premium_expiry=?, access=1 WHERE user_id=?", (e, i))
        conn.commit()
        return True
    except: return False

def add_coins_db(i, coins):
    try:
        ensure_user(i, "Admin_Added")
        c.execute("UPDATE users SET coins=coins+? WHERE user_id=?", (coins, i))
        conn.commit()
        return gc(i)
    except: return 0

def get_total_searches():
    try:
        c.execute("SELECT SUM(searches) FROM users"); r = c.fetchone()
        return r[0] if r and r[0] else 0
    except: return 0

# ==================== GREEN HACKER LOADING ====================
def hacker_loading(chat_id, msg_id, query, search_type='NUMBER'):
    spinners = ["◐", "◓", "◑", "◒"]
    frames = [
        (10, "⚡", "SYSTEM BOOT",       "boot --kernel=dark",       "IPv6 : 192.***.***.7"),
        (20, "🔌", "VPN TUNNEL",        "vpn connect tor_node7",    "Proxy : ACTIVE ✔"),
        (30, "🛡️", "FIREWALL BYPASS",  "iptables -F --silent",     "Shield: DOWN ⚠️"),
        (40, "🔐", "HASH CRACKING",     "hashcat -m 0 -a 3",        "Hash  : CRACKED 🔓"),
        (50, "💾", "DATABASE ACCESS",   "sqlmap --dump --root",     "DB    : ROOT ✔"),
        (60, "🟢", "RECORD EXTRACT",    "SELECT * FROM users",      f"Target: {query}"),
        (70, "🔓", "AES DECRYPTION",    "openssl aes-256-cbc -d",   "Key   : FOUND 🔑"),
        (80, "📡", "DATA TRANSFER",     "wget --mirror --no-check", "Speed : 2.4 GB/s"),
        (90, "🎯", "IDENTITY MATCH",    "facematch --deep --ai",    "Match : 99.8% 🎯"),
        (100, "✅", "ACCESS GRANTED",   "root@hacker:~$ SUCCESS",   "SYSTEM: COMPLETE")
    ]
    for idx, (percent, icon, status, cmd, extra) in enumerate(frames):
        filled = percent // 10
        bar = "🟩" * filled + "⬛" * (10 - filled)
        spin = spinners[idx % 4]
        try:
            bot.edit_message_text(
                f"`╔══════════════════════════════╗`\n"
                f"`║  🟢 HACKER TERMINAL v3.0     ║`\n"
                f"`║  💚 SECURE • ANONYMOUS • FAST║`\n"
                f"`╚══════════════════════════════╝`\n"
                f"`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`💚 SYS  ▶ ONLINE    | VPN ▶ ACTIVE`\n"
                f"`💚 ENC  ▶ AES-256 ✔ | TOR ▶ NODE-7`\n"
                f"`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`{spin} LOADING...`\n"
                f"{bar} `{percent}%`\n"
                f"`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`{icon} {status}`\n"
                f"` $ {cmd}`\n"
                f"` 📌 {extra}`\n"
                f"`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🎯 TARGET : {query}`\n"
                f"`📡 METHOD : {search_type}`\n"
                f"`🔒 STATUS : SCANNING...`\n"
                f"`⚡ UPTIME : 00:00:{idx+1:02d}`",
                chat_id, msg_id, parse_mode='Markdown'
            )
            time.sleep(0.5)
        except: pass

# ==================== API FUNCTIONS ====================
def fetch_number(num):
    try:
        r = requests.get(f"{NUMBER_API_URL}?num={num}", timeout=10)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_number_special(phone):
    try:
        r = requests.get(f"{NUMBER_SPECIAL_URL}?key={NUMBER_API_KEY}&number={phone}", timeout=10)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_aadhaar(aadhaar_num):
    try:
        r = requests.get(f"{AADHAAR_API_URL}?key={AADHAAR_API_KEY}&aadhaar={aadhaar_num}", timeout=10)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_vehicle(vehicle_num):
    try:
        r = requests.get(f"{VEHICLE_API_URL}?type=vehicle&search={vehicle_num.upper()}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('regNo'): return data
        return None
    except: return None

def fetch_vehicle_special(vehicle_num):
    try:
        r = requests.get(f"{VEHICLE_SPECIAL_API_URL}?number={vehicle_num.upper()}", timeout=10)
        if r.status_code == 200: return r.json()
        return None
    except: return None

# ==================== FORMAT RESULT ====================
def format_result(data, query, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    if is_aadhaar:
        if not data: return "`❌ No data`"
        if isinstance(data, dict):
            info = data['data'] if ('status' in data and data['status'] == 'success' and 'data' in data) else data
        else: info = {}
        if not info or not info.get('name'): return "`❌ No records`"
        return f"`🆔 AADHAAR INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🆔 Aadhaar: {info.get('aadhaar') or info.get('aadhar', query)}`\n`👤 Name: {info.get('name', 'N/A')}`\n`👨 Father: {info.get('father') or info.get('fname', 'N/A')}`\n`📅 DOB: {info.get('dob') or info.get('DOB', 'N/A')}`\n`⚥ Gender: {info.get('gender') or info.get('sex', 'N/A')}`\n`🏠 Address: {info.get('address') or info.get('addr', 'N/A')}`\n`📱 Phone: {info.get('phone') or info.get('mobile', 'N/A')}`\n`📧 Email: {info.get('email') or info.get('mail', 'N/A')}`\n`🔐 {OWNER}`"
    elif is_number_special:
        if not data: return "`❌ No data`"
        if isinstance(data, dict):
            if 'result' in data and isinstance(data['result'], list) and data['result']: info = data['result'][0]
            elif 'data' in data and isinstance(data['data'], dict): info = data['data']
            else: info = data
        else: info = {}
        if not info or not info.get('name'): return "`❌ No records`"
        return f"`📱 NUMBER INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`📱 Number: {query}`\n`👤 Name: {info.get('name', 'N/A')}`\n`👨 Father: {info.get('fname') or info.get('father', 'N/A')}`\n`🆔 Aadhar: {info.get('aadhar') or info.get('aadhaar', 'N/A')}`\n`🏠 Address: {info.get('address') or info.get('addr', 'N/A')}`\n`📡 Circle: {info.get('circle') or info.get('operator', 'N/A')}`\n`📧 Email: {info.get('email') or info.get('mail', 'N/A')}`\n`📞 Alt: {info.get('alt') or info.get('alternate', 'N/A')}`\n`🔐 {OWNER}`"
    elif is_special:
        if not data or not data.get('reg_no'): return "`❌ Not found`"
        i = data.get('response', {})
        return f"`🚘 VEHICLE SPECIAL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🚘 Number: {data.get('reg_no', 'N/A')}`\n`👤 Owner: {i.get('ownerName', 'N/A')}`\n`🚗 Class: {i.get('vehicle_class', 'N/A')}`\n`⛽ Fuel: {i.get('fuel_type', 'N/A')}`\n`🔧 Engine: {i.get('engine_no', 'N/A')}`\n`🔩 Chassis: {i.get('chassis_no', 'N/A')}`\n`📅 Reg Date: {i.get('reg_date', 'N/A')}`\n`📋 Status: {i.get('status', 'N/A')}`\n`🏭 Model: {i.get('maker_model', 'N/A')}`\n`📅 Fitness: {i.get('fitness_upto', 'N/A')}`\n`🏢 Insurance: {i.get('insurance_company', 'N/A')}`\n`📅 Ins Upto: {i.get('insurance_upto', 'N/A')}`\n`🔐 {OWNER}`"
    elif is_vehicle:
        if not data or not data.get('regNo'): return "`❌ Not found`"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"`🚗 VEHICLE INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🚘 Number: {data.get('regNo', 'N/A')}`\n`👤 Owner: {i.get('ownerName', 'N/A')}`\n`🏭 Company: {i.get('manufacturer', 'N/A')}`\n`🚗 Model: {i.get('vehicle', 'N/A')}`\n`📅 Reg Date: {i.get('regDate', 'N/A')}`\n`🏢 RTO: {rto.get('rtoCode', 'N/A')}`\n`📋 Status: {'✅' if i.get('status') == '100' else '❌'}`\n`🏠 Address: {i.get('presentAddress', 'N/A')}`\n`📱 Owner: {data.get('owner', 'N/A')}`\n`🔐 {OWNER}`"
    else:
        if not data or data.get('status') != 'success': return "`❌ No data`"
        info = data.get('data', {})
        if not info: return "`❌ No records`"
        return f"`📱 NUMBER SPECIAL INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`📱 Number: {info.get('phone', query)}`\n`👤 Name: {info.get('name', 'N/A')}`\n`🆔 Aadhar: {info.get('aadhar', 'N/A')}`\n`🏠 Address: {info.get('address', 'N/A')}`\n`📡 Circle: {info.get('circle', 'N/A')}`\n`📧 Email: {info.get('email', 'N/A')}`\n`📞 Alt: {info.get('alt', 'N/A')}`\n`🔐 {OWNER}`"

def send_log(uid, un, query, data, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    try:
        if is_aadhaar:
            if not data: return
            info = data.get('data', data) if isinstance(data, dict) else {}
            bot.send_message(ADMIN_ID, f"🆔 AADHAAR LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n👤 {info.get('name', 'N/A')}")
        elif is_number_special:
            if not data: return
            if isinstance(data, dict):
                if 'result' in data and isinstance(data['result'], list) and data['result']: i = data['result'][0]
                elif 'data' in data and isinstance(data['data'], dict): i = data['data']
                else: i = data
            else: i = {}
            bot.send_message(ADMIN_ID, f"📊 NUMBER NORMAL LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n📱 {i.get('name', 'N/A')}")
        elif is_special:
            bot.send_message(ADMIN_ID, f"🚘 SPECIAL LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {data.get('reg_no', 'N/A')}")
        elif is_vehicle:
            i = data.get('response', {})
            bot.send_message(ADMIN_ID, f"🚗 VEHICLE LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {i.get('vehicle', 'N/A')}")
        else:
            if not data or data.get('status') != 'success': return
            info = data.get('data', {})
            bot.send_message(ADMIN_ID, f"📊 NUMBER SPECIAL LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n📱 {info.get('name', 'N/A')}")
    except: pass

# ==================== KEYBOARDS ====================
def welcome_kb(l):
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton("🎁 FREE Daily Coin Claim", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("💳 Buy Premium", callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Cyber_With_Ranjan"))
    return mk

def premium_plans_kb(l):
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton("💳 1 Day – ₹10", callback_data="pay_1day"))
    mk.add(InlineKeyboardButton("💳 1 Week – ₹60", callback_data="pay_7days"))
    mk.add(InlineKeyboardButton("💳 1 Month – ₹101", callback_data="pay_30days"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_welcome"))
    return mk

def main_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🔍 " + L[l]['search'], callback_data="search_menu"))
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🎁 Claim Coin", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("👤 " + L[l]['profile_btn'], callback_data="profile"))
    mk.add(InlineKeyboardButton("❓ " + L[l]['help_btn'], callback_data="help"))
    mk.add(InlineKeyboardButton("ℹ️ " + L[l]['about_btn'], callback_data="about"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton("📢 Channel", url=CHANNEL))
    mk.add(InlineKeyboardButton(L[l]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan"))
    return mk

def search_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton(L[l]['number'], callback_data="info"),
        InlineKeyboardButton(L[l]['vehicle'], callback_data="vehicle_info"),
        InlineKeyboardButton(L[l]['vehicle_special'], callback_data="vehicle_special_info"),
        InlineKeyboardButton(L[l]['aadhaar'], callback_data="aadhaar_info")
    )
    mk.add(InlineKeyboardButton(L[l]['back'], callback_data="main_menu"))
    return mk

def group_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton(L[l]['number'], callback_data="info"),
        InlineKeyboardButton(L[l]['vehicle'], callback_data="vehicle_info"),
        InlineKeyboardButton(L[l]['vehicle_special'], callback_data="vehicle_special_info"),
        InlineKeyboardButton(L[l]['aadhaar'], callback_data="aadhaar_info")
    )
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🎁 Claim Coin", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan"))
    return mk

def result_btn(query, lang, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False, message_id=None, is_group=False):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"json_{query}_{is_vehicle}_{is_special}_{is_aadhaar}_{is_number_special}"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🗑️ " + L[lang]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton("🔙 " + L[lang]['back'], callback_data="main_menu"))
    if is_group and message_id:
        mk.add(InlineKeyboardButton("📌 Pin", callback_data=f"pin_{message_id}"))
    return mk

def back_btn(l):
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🔙 " + L[l]['back'], callback_data="main_menu"))
    return mk

def lang_selection():
    mk = InlineKeyboardMarkup(row_width=3)
    mk.add(
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"),
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn"),
        InlineKeyboardButton("🇮🇳 मराठी", callback_data="lang_mr"),
        InlineKeyboardButton("🇵🇰 اُردو", callback_data="lang_ur"),
        InlineKeyboardButton("🇮🇳 தமிழ்", callback_data="lang_ta")
    )
    return mk

def send_welcome_with_qr(chat_id, l, edit_message_id=None):
    caption = L[l]['welcome']
    kb = welcome_kb(l)
    try:
        with open(QR_PATH, 'rb') as qr:
            if edit_message_id:
                try: bot.delete_message(chat_id, edit_message_id)
                except: pass
            bot.send_photo(chat_id, qr, caption=caption, reply_markup=kb, parse_mode='Markdown')
    except:
        bot.send_message(chat_id, caption, reply_markup=kb, parse_mode='Markdown')

# ==================== LANGUAGE ====================
@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lc(c):
    l = c.data.split('_')[1]
    sl(c.from_user.id, l)
    ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    send_welcome_with_qr(c.message.chat.id, l)
    bot.answer_callback_query(c.id, "✅")

# ==================== CLAIM COIN ====================
@bot.callback_query_handler(func=lambda c: c.data == "claim_coin")
def claim_coin_cb(c):
    l = gl(c.from_user.id)
    ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
    if claim_daily_coin(c.from_user.id):
        coins = gc(c.from_user.id)
        bot.answer_callback_query(c.id, f"🎉 +1 Coin! Total: {coins}")
        bot.send_message(c.message.chat.id, L[l]['coin_claimed'].format(coins=coins), reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        bot.answer_callback_query(c.id, "❌ Aaj ka already claim!", True)
        bot.send_message(c.message.chat.id, L[l]['already_claimed'], reply_markup=main_menu(l))

# ==================== PREMIUM ====================
@bot.callback_query_handler(func=lambda c: c.data == "show_premium")
def show_premium_cb(c):
    l = gl(c.from_user.id)
    if ip(c.from_user.id):
        bot.answer_callback_query(c.id, "💎 Already Premium!", True); return
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "💎 Plans")

@bot.callback_query_handler(func=lambda c: c.data == "back_to_welcome")
def back_welcome_cb(c):
    l = gl(c.from_user.id)
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    send_welcome_with_qr(c.message.chat.id, l)
    bot.answer_callback_query(c.id, "🔙")

@bot.callback_query_handler(func=lambda c: c.data.startswith('pay_'))
def pay_cb(c):
    l = gl(c.from_user.id)
    plan = c.data.split('_')[1]
    plan_map = {'1day': (1, '₹10'), '7days': (7, '₹60'), '30days': (30, '₹101')}
    if plan not in plan_map:
        bot.answer_callback_query(c.id, "❌ Invalid", True); return
    days, amount = plan_map[plan]
    bot.answer_callback_query(c.id, f"💳 {amount}")
    text = (f"💳 **Payment Details**\n\n📦 Plan: {days} Days\n💰 Amount: {amount}\n🏦 UPI: `{UPI_ID}`\n\n"
            f"📸 Scan QR & pay {amount}\n📤 Send screenshot to @Cyber_With_Ranjan\n\n✅ Premium will be activated within 5 mins!")
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=text, parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, text, parse_mode='Markdown')
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="show_premium"))
    bot.send_message(c.message.chat.id, "📌 After payment, send screenshot to admin.", reply_markup=mk)

# ==================== PROFILE ====================
@bot.callback_query_handler(func=lambda cb: cb.data == "profile")
def profile_cb(cb):
    uid = cb.from_user.id
    ensure_user(uid, cb.from_user.first_name or "User", cb.from_user.username or "")
    coins = gc(uid)
    prem = "✅ Active" if ip(uid) else "❌ Inactive"
    searches = 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
        r = cur.fetchone()
        searches = r[0] if r else 0
    except: pass
    l = gl(uid)
    bot.answer_callback_query(cb.id, "👤 Profile")
    bot.send_message(cb.message.chat.id, L[l]['profile'].format(uid=uid, coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data == "help")
def help_cb(c):
    l = gl(c.from_user.id)
    bot.answer_callback_query(c.id, "❓")
    bot.send_message(c.message.chat.id, L[l]['help'], reply_markup=back_btn(l), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data == "about")
def about_cb(c):
    l = gl(c.from_user.id)
    bot.send_message(c.message.chat.id, L[l]['about'] + f"\n🌐 {WEBSITE}", reply_markup=back_btn(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "ℹ️")

@bot.callback_query_handler(func=lambda c: c.data == "clear")
def clear_cb(c):
    try:
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.answer_callback_query(c.id, "🗑️ Cleared!")
    except: bot.answer_callback_query(c.id, "❌ Can't clear!", True)

@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def main_menu_cb(c):
    l = gl(c.from_user.id)
    coins = gc(c.from_user.id)
    if ip(c.from_user.id):
        text = f"{L[l]['main_menu']}\n\n💎 **Premium** — Unlimited Access"
    else:
        text = f"{L[l]['main_menu']}\n\n🪙 **Coins:** {coins}\n_1 Coin = 1 Search_"
    try:
        bot.edit_message_text(text, c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, text, reply_markup=main_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔙")

@bot.callback_query_handler(func=lambda c: c.data == "search_menu")
def search_menu_cb(c):
    l = gl(c.from_user.id)
    coins_info = ""
    if not ip(c.from_user.id):
        coins = gc(c.from_user.id)
        coins_info = f"\n\n🪙 Coins Left: **{coins}**"
    try:
        bot.edit_message_text("🔍 " + L[l]['search'] + coins_info, c.message.chat.id, c.message.message_id, reply_markup=search_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, "🔍 " + L[l]['search'] + coins_info, reply_markup=search_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data in ["info", "vehicle_info", "vehicle_special_info", "aadhaar_info"])
def info_cb(c):
    l = gl(c.from_user.id)
    if not ip(c.from_user.id):
        coins = gc(c.from_user.id)
        if coins <= 0:
            bot.answer_callback_query(c.id, "❌ No coins! Claim FREE coin", True)
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("🎁 Claim 1 FREE Coin", callback_data="claim_coin"))
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            bot.send_message(c.message.chat.id,
                "❌ **No Coins Left!**\n\n🎁 Claim 1 FREE Coin daily\n🪙 1 Coin = 1 Search\n\n💎 Or Buy Premium:\n• 1 Day – ₹10\n• 1 Week – ₹60\n• 1 Month – ₹101",
                reply_markup=mk, parse_mode='Markdown')
            return
    if c.data == "aadhaar_info": bot.send_message(c.message.chat.id, L[l]['enter_aadhaar'])
    elif c.data == "vehicle_special_info": bot.send_message(c.message.chat.id, L[l]['enter_vehicle_special'])
    elif c.data == "vehicle_info": bot.send_message(c.message.chat.id, L[l]['enter_vehicle'])
    else: bot.send_message(c.message.chat.id, L[l]['enter_number'])
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data.startswith('json_'))
def json_cb(c):
    parts = c.data.split('_')[1:]
    if len(parts) < 1:
        bot.answer_callback_query(c.id, "❌", True); return
    q = parts[0]
    is_vehicle = parts[1] == 'True' if len(parts) > 1 else False
    is_special = parts[2] == 'True' if len(parts) > 2 else False
    is_aadhaar = parts[3] == 'True' if len(parts) > 3 else False
    is_number_special = parts[4] == 'True' if len(parts) > 4 else False
    if is_aadhaar: d = fetch_aadhaar(q)
    elif is_special: d = fetch_vehicle_special(q)
    elif is_vehicle: d = fetch_vehicle(q)
    elif is_number_special: d = fetch_number_special(q)
    else: d = fetch_number(q)
    if not d:
        bot.answer_callback_query(c.id, "❌", True); return
    bot.answer_callback_query(c.id, "📊")
    try:
        jtext = json.dumps(d, indent=2, ensure_ascii=False)
        if len(jtext) > 3800: jtext = jtext[:3800] + "\n... (truncated)"
        bot.send_message(c.message.chat.id, f"`📊 JSON OUTPUT\n\n{jtext}`", parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, f"📊 JSON:\n`{str(d)[:3500]}`", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith('pin_'))
def pin_callback(c):
    if c.from_user.id != ADMIN_ID:
        bot.answer_callback_query(c.id, "❌ Admin only", True); return
    try:
        message_id = int(c.data.split('_')[1])
        bot.pin_chat_message(c.message.chat.id, message_id)
        bot.answer_callback_query(c.id, "📌 Pinned!", show_alert=False)
        bot.send_message(c.message.chat.id, "📌 Message Pinned!")
    except: bot.answer_callback_query(c.id, "❌ Pin failed!", True)

# ==================== PROCESS QUERY ====================
def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    l = gl(m.from_user.id)
    ensure_user(m.from_user.id, m.from_user.first_name or "User", m.from_user.username or "")
    is_premium_user = ip(m.from_user.id)

    if not is_premium_user:
        coins = gc(m.from_user.id)
        if coins <= 0:
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("🎁 Claim 1 FREE Coin", callback_data="claim_coin"))
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            bot.reply_to(m,
                "❌ **No Coins Left!**\n\n🎁 Claim 1 FREE Coin daily\n🪙 1 Coin = 1 Search\n\n💎 Or Buy Premium:\n• 1 Day – ₹10\n• 1 Week – ₹60\n• 1 Month – ₹101",
                reply_markup=mk, parse_mode='Markdown')
            return
        if not dc(m.from_user.id):
            bot.reply_to(m, L[l]['nc'], reply_markup=main_menu(l))
            return

    if is_aadhaar: stype = "AADHAAR"
    elif is_special: stype = "VEHICLE SPECIAL"
    elif is_vehicle: stype = "VEHICLE"
    elif is_number_special: stype = "NUMBER NORMAL"
    else: stype = "NUMBER SPECIAL"

    if is_aadhaar: d = fetch_aadhaar(q)
    elif is_special: d = fetch_vehicle_special(q)
    elif is_vehicle: d = fetch_vehicle(q)
    elif is_number_special: d = fetch_number_special(q)
    else: d = fetch_number(q)

    if m.from_user.id == ADMIN_ID:
        try: bot.send_message(ADMIN_ID, f"🔍 **RAW API** `{q}`:\n```json\n{json.dumps(d, indent=2)}\n```", parse_mode='Markdown')
        except: pass

    try: msg = bot.reply_to(m, "`💻 INITIALIZING...`", parse_mode='Markdown')
    except: msg = bot.reply_to(m, "💻 INITIALIZING...")

    try: hacker_loading(m.chat.id, msg.message_id, q, stype)
    except: pass

    if not d:
        try: bot.edit_message_text(f"`❌ ACCESS DENIED`\n\n`> Target: {q}`\n`> Reason: No data / API error`", m.chat.id, msg.message_id, parse_mode='Markdown')
        except: bot.send_message(m.chat.id, "❌ API returned empty or error.")
        return

    send_log(m.from_user.id, m.from_user.username, q, d, is_vehicle, is_special, is_aadhaar, is_number_special)
    res = format_result(d, q, is_vehicle, is_special, is_aadhaar, is_number_special)

    try:
        bot.edit_message_text(
            f"`╔══════════════════════════════╗`\n"
            f"`║  💚 ACCESS GRANTED SUCCESS 💚║`\n"
            f"`║  🎯 DATA EXTRACTED           ║`\n"
            f"`╚══════════════════════════════╝`\n"
            f"`🎯 TARGET : {q}`\n"
            f"`🔒 STATUS : ✅ DECRYPTED`\n"
            f"{res}",
            m.chat.id, msg.message_id, parse_mode='Markdown'
        )
        is_group = m.chat.type in ['group', 'supergroup']
        markup = result_btn(q, l, is_vehicle, is_special, is_aadhaar, is_number_special, msg.message_id if is_group else None, is_group)
        bot.edit_message_reply_markup(m.chat.id, msg.message_id, reply_markup=markup)
    except Exception as e:
        bot.send_message(m.chat.id, f"Error: {e}")
        return

    try:
        jtext = json.dumps(d, indent=2, ensure_ascii=False)
        if len(jtext) > 3600: jtext = jtext[:3600] + "\n... (truncated)"
        bot.send_message(m.chat.id, f"`📊 JSON OUTPUT for {q}`\n\n```json\n{jtext}\n```", parse_mode='Markdown')
    except:
        try: bot.send_message(m.chat.id, f"📊 JSON:\n`{str(d)[:3500]}`", parse_mode='Markdown')
        except: pass

    if not is_premium_user and m.chat.type == 'private':
        coins_left = gc(m.from_user.id)
        if coins_left > 0:
            bot.send_message(m.chat.id, f"🪙 **Coins Left: {coins_left}**", parse_mode='Markdown')
        else:
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("🎁 Claim 1 FREE Coin", callback_data="claim_coin"))
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            bot.send_message(m.chat.id,
                "🪙 **Coins Left: 0**\n\n🎁 Claim FREE coin daily or\n💎 Buy Premium for unlimited!",
                reply_markup=mk, parse_mode='Markdown')

# ==================== START ====================
@bot.message_handler(commands=['start'], chat_types=['private'])
def st(m):
    au(m.from_user.id, m.from_user.first_name or "", m.from_user.username or "")
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection(), parse_mode='Markdown')

@bot.message_handler(commands=['myid', 'id', 'whoami'])
def myid_cmd(m):
    uid = m.from_user.id
    un = m.from_user.username or "N/A"
    fn = m.from_user.first_name or "N/A"
    ensure_user(uid, fn, un)
    bot.reply_to(m, f"🆔 **Your Telegram Info**\n\n👤 Name: {fn}\n📛 Username: @{un}\n🆔 **User ID:** `{uid}`\n\n📌 Send this ID to admin to get Premium or Coins.", parse_mode='Markdown')

# ==================== SEARCH (PRIVATE) ====================
@bot.message_handler(commands=['num', 'search'], chat_types=['private'])
def nc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip(), False, False, False, False)

@bot.message_handler(commands=['vehicle', 'v'], chat_types=['private'])
def vc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle']); return
    process_query(m, p[1].strip(), True, False, False)

@bot.message_handler(commands=['vehiclespecial', 'vs'], chat_types=['private'])
def vsc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle_special']); return
    process_query(m, p[1].strip(), False, True, False)

@bot.message_handler(commands=['aadhaar', 'aadhar'], chat_types=['private'])
def acmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_aadhaar']); return
    process_query(m, p[1].strip(), False, False, True)

@bot.message_handler(commands=['special', 's'], chat_types=['private'])
def special_cmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /special 9661756498 (10-digit)"); return
    phone = p[1].strip()
    if not re.match(r'^\d{10}$', phone): bot.reply_to(m, "❌ Enter a valid 10-digit number."); return
    process_query(m, phone, False, False, False, True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text or ''), chat_types=['private'])
def hn(m): process_query(m, m.text.strip(), False, False, False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', (m.text or '').upper()), chat_types=['private'])
def vhn(m): process_query(m, m.text.strip().upper(), True, False, False)

@bot.message_handler(func=lambda m: re.match(r'^\d{12}$', m.text or ''), chat_types=['private'])
def ahn(m): process_query(m, m.text.strip(), False, False, True)

# ==================== SEARCH (GROUP) ====================
@bot.message_handler(commands=['num'], chat_types=['group', 'supergroup'])
def gn(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /num 9661756498"); return
    process_query(m, p[1].strip(), False, False, False, False)

@bot.message_handler(commands=['vehicle'], chat_types=['group', 'supergroup'])
def gv(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /vehicle RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), True, False, False)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group', 'supergroup'])
def gvs(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /vehiclespecial RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), False, True, False)

@bot.message_handler(commands=['aadhaar'], chat_types=['group', 'supergroup'])
def gaadhaar(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /aadhaar 962397300673"); return
    process_query(m, p[1].strip(), False, False, True)

@bot.message_handler(commands=['special'], chat_types=['group', 'supergroup'])
def gspecial(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /special 9661756498"); return
    phone = p[1].strip()
    if not re.match(r'^\d{10}$', phone): bot.reply_to(m, "❌ Enter a valid 10-digit number."); return
    process_query(m, phone, False, False, False, True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text or ''), chat_types=['group', 'supergroup'])
def ghn(m): process_query(m, m.text.strip(), False, False, False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', (m.text or '').upper()), chat_types=['group', 'supergroup'])
def gvh(m): process_query(m, m.text.strip().upper(), True, False, False)

@bot.message_handler(func=lambda m: re.match(r'^\d{12}$', m.text or ''), chat_types=['group', 'supergroup'])
def gahn(m): process_query(m, m.text.strip(), False, False, True)

@bot.message_handler(commands=['start', 'help'], chat_types=['group', 'supergroup'])
def gs(m):
    l = gl(m.from_user.id)
    bot.reply_to(m, "👋 /num 9661756498 | /vehicle RJ14CV0002 | /vehiclespecial RJ14CV0002 | /aadhaar 962397300673 | /special 9661756498\n🪙 1 FREE Coin/day = 1 Search!\n💎 1D ₹10, 1W ₹60, 1M ₹101\n🌐 cyberwithranjan.in", reply_markup=group_menu(l))

# ==================== GENERAL ====================
@bot.message_handler(commands=['menu'])
def me(m):
    l = gl(m.from_user.id)
    if m.chat.type in ['group', 'supergroup']:
        bot.send_message(m.chat.id, "📱 Menu", reply_markup=group_menu(l)); return
    coins = gc(m.from_user.id)
    status = "💎 **Premium** — Unlimited Access" if ip(m.from_user.id) else f"🪙 **Coins:** {coins}\n_1 Coin = 1 Search_"
    bot.send_message(m.chat.id, f"{L[l]['main_menu']}\n\n{status}", reply_markup=main_menu(l), parse_mode='Markdown')

@bot.message_handler(commands=['claim'])
def cl2(m):
    l = gl(m.from_user.id)
    if claim_daily_coin(m.from_user.id):
        coins = gc(m.from_user.id)
        bot.reply_to(m, L[l]['coin_claimed'].format(coins=coins), parse_mode='Markdown')
    else:
        bot.reply_to(m, L[l]['already_claimed'])

@bot.message_handler(commands=['premium'])
def pm(m):
    l = gl(m.from_user.id)
    if ip(m.from_user.id):
        bot.reply_to(m, "🎉 You are already premium!"); return
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(m.chat.id, qr, caption=L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')
    except:
        bot.send_message(m.chat.id, L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
def pr2(m):
    uid = m.from_user.id
    ensure_user(uid, m.from_user.first_name or "User", m.from_user.username or "")
    coins = gc(uid)
    prem = "✅ Active" if ip(uid) else "❌ Inactive"
    searches = 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
        r = cur.fetchone()
        searches = r[0] if r else 0
    except: pass
    l = gl(uid)
    bot.reply_to(m, L[l]['profile'].format(uid=uid, coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.message_handler(commands=['contact'])
def ct(m): bot.reply_to(m, f"📞 {OWNER}\n🔗 {GROUP}\n🌐 {WEBSITE}")

@bot.message_handler(commands=['clear'])
def clear_cmd(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
        bot.reply_to(m, "🗑️ Cleared!")
    except: bot.reply_to(m, "❌ Can't clear!")

@bot.message_handler(commands=['help'], chat_types=['private'])
def hp(m):
    l = gl(m.from_user.id)
    bot.reply_to(m, L[l]['help'], parse_mode='Markdown')

@bot.message_handler(commands=['language', 'lang'])
def lg(m):
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection())

@bot.message_handler(commands=['website', 'site'])
def wsite(m):
    bot.reply_to(m, f"🌐 **Official Website**\n\n👉 {WEBSITE}",
                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 Visit cyberwithranjan.in", url=WEBSITE)),
                 parse_mode='Markdown')

@bot.message_handler(commands=['pin'])
def pin_command(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, L['en']['admin_only']); return
    if m.reply_to_message:
        try:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
            bot.reply_to(m, "📌 Pinned!")
        except: bot.reply_to(m, "❌ Pin failed. Make me admin.")
    else: bot.reply_to(m, "❌ Reply to a message with /pin")

# ==================== ADMIN ====================
@bot.message_handler(commands=['addpremium'])
def ap2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = m.text.split()
        uid_int = int(uid); days_int = int(days)
        if ap(uid_int, days_int):
            bot.reply_to(m, f"✅ **Premium Added**\n\n🆔 User ID: `{uid_int}`\n📅 Days: {days_int}\n💎 Status: Unlimited Access", parse_mode='Markdown')
            try:
                bot.send_message(uid_int, f"🎉 **Premium Activated!**\n\n⏰ Duration: {days_int} days\n✅ Unlimited searches unlocked!\n\n🔍 Now send any number to search!", parse_mode='Markdown')
            except: pass
    except:
        bot.reply_to(m, "❌ Use: `/addpremium [user_id] [days]`", parse_mode='Markdown')

@bot.message_handler(commands=['removepremium'])
def rp(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (int(uid),)); conn.commit()
        bot.reply_to(m, f"✅ Removed premium from `{uid}`", parse_mode='Markdown')
    except: bot.reply_to(m, "❌ /removepremium [uid]")

@bot.message_handler(commands=['addcoins'])
def ac(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, coins = m.text.split()
        uid_int = int(uid); coins_int = int(coins)
        new_coins = add_coins_db(uid_int, coins_int)
        bot.reply_to(m, f"✅ **Coins Added**\n\n🆔 User ID: `{uid_int}`\n🪙 Added: {coins_int}\n🪙 Total now: **{new_coins}**", parse_mode='Markdown')
        try:
            bot.send_message(uid_int, f"🪙 **+{coins_int} Coins Added!**\n\n🪙 Total Coins: **{new_coins}**\n\n✅ Now you can search {new_coins} times!", parse_mode='Markdown')
        except: pass
    except:
        bot.reply_to(m, "❌ Use: `/addcoins [user_id] [coins]`", parse_mode='Markdown')

@bot.message_handler(commands=['userinfo'])
def userinfo_cmd(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        uid_int = int(uid)
        cur = conn.cursor()
        cur.execute("SELECT user_id, first_name, username, coins, premium, premium_expiry, searches FROM users WHERE user_id=?", (uid_int,))
        r = cur.fetchone()
        if not r:
            bot.reply_to(m, f"❌ User `{uid_int}` not in DB.\nAsk user `/myid` first!", parse_mode='Markdown'); return
        prem_status = "✅ YES" if ip(uid_int) else "❌ NO"
        bot.reply_to(m, f"👤 **User Info**\n\n🆔 ID: `{r[0]}`\n👤 Name: {r[1]}\n📛 Username: @{r[2] or 'N/A'}\n🪙 Coins: **{r[3]}**\n💎 Premium: {prem_status}\n📅 Expiry: {r[5] or 'N/A'}\n🔍 Searches: {r[6]}", parse_mode='Markdown')
    except: bot.reply_to(m, "❌ Use: `/userinfo [user_id]`", parse_mode='Markdown')

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT user_id, username, coins, premium FROM users ORDER BY user_id DESC LIMIT 20")
        users = c.fetchall()
        if not users: bot.reply_to(m, "No users."); return
        text = "📋 **Last 20 Users:**\n\n"
        for u in users:
            text += f"🆔 `{u[0]}` | @{u[1] or 'N/A'} | 🪙{u[2]} | {'💎' if u[3] else ''}\n"
        bot.reply_to(m, text, parse_mode='Markdown')
    except: pass

@bot.message_handler(commands=['stats'])
def st2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT COUNT(*) FROM users"); total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE access=1"); access = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE premium=1"); premium = c.fetchone()[0]
        c.execute("SELECT SUM(coins) FROM users"); coins = c.fetchone()[0] or 0
        searches = get_total_searches()
        bot.reply_to(m, L[gl(m.from_user.id)]['stats_text'].format(total=total, access=access, premium=premium, coins=coins, searches=searches), parse_mode='Markdown')
    except: pass

@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id != ADMIN_ID: return
    msg = m.text.replace('/broadcast', '').strip()
    if not msg: bot.reply_to(m, "❌ /broadcast [message]"); return
    try:
        c.execute("SELECT user_id FROM users"); users = c.fetchall()
        sent = 0
        for uid in users:
            try:
                bot.send_message(uid[0], "📢 **Announcement**\n\n" + msg, parse_mode='Markdown')
                sent += 1
            except: pass
        bot.reply_to(m, f"✅ Broadcast sent to {sent} users!")
    except Exception as e: bot.reply_to(m, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['testapi'])
def test_api(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "❌ Admin only."); return
    parts = m.text.split()
    if len(parts) < 3: bot.reply_to(m, "❌ /testapi num 9876543210"); return
    typ = parts[1].lower(); val = parts[2].strip()
    if typ == "num": data = fetch_number(val)
    elif typ == "aadhaar": data = fetch_aadhaar(val)
    else: bot.reply_to(m, "❌ Use 'num' or 'aadhaar'"); return
    if data: bot.reply_to(m, f"✅ **Response:**\n```json\n{json.dumps(data, indent=2)}\n```", parse_mode='Markdown')
    else: bot.reply_to(m, "❌ No data or error.")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("=" * 55)
    print("🔥 HACKER OSINT BOT v3.0 — PROFESSIONAL")
    print("=" * 55)
    print(f"👨‍💻 Owner: {OWNER}")
    print(f"🌐 Website: {WEBSITE}")
    print("-" * 55)
    print("✅ Flow: /start → Language → QR + Free Coin → Search")
    print("✅ 1 FREE Coin/Day → 1 Search")
    print("✅ Premium: 1D ₹10 | 1W ₹60 | 1M ₹101")
    print("✅ Admin: /addpremium + /addcoins (auto-create user)")
    print("✅ Premium = Unlimited Search")
    print("✅ Green Hacker Loading Animation")
    print("=" * 55)
    bot.infinity_polling()