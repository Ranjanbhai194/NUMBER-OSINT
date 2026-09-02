import telebot, requests, re, sqlite3, datetime, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- CONFIG ----------
BOT_TOKEN = "8654008990:AAEbFOpj658dagBy92qIcvZDQd1mxhDkI50"
ADMIN_ID = 6936978343

NUMBER_API_URL = "https://num-info-redzone.susxbunny.workers.dev/api"
NUMBER_API_KEY = "redzone@12"

AADHAAR_API_URL = "https://leak-osint-redzone.vercel.app/api"
AADHAAR_API_KEY = "REDZONE"

VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"
NUMBER_SPECIAL_URL = "https://anurixx-gift-number.vercel.app/api"

OWNER = "@Cyber_With_Ranjan"
INSTA = "https://www.instagram.com/ranjan_bhai_194?igsh=ZTM2enVsNmt3MnJv"
WEBSITE = "https://cyberwithranjan.in"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
SUPPORT_GROUP = "https://t.me/cyberwithranjan"

QR_PATH = os.path.join(os.path.dirname(__file__), 'qr.png')
bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, lang TEXT DEFAULT 'en', coins INTEGER DEFAULT 0, last_claim TEXT, access INTEGER DEFAULT 0, premium INTEGER DEFAULT 0, premium_expiry TEXT, searches INTEGER DEFAULT 0, insta_followed INTEGER DEFAULT 0, website_visited INTEGER DEFAULT 0)''')
conn.commit()

# ---------- LANGUAGE DICTIONARIES (full as before) ----------
# (I've included only English and Hindi to save space, but you can keep all 6 languages)
L = {
    'en': {
        'lang': "🌐 Select Language:",
        'welcome_premium': "💎 **Premium Required**\n\n📅 Plans:\n• 1 Day – ₹10\n• 5 Days – ₹30\n• 1 Week – ₹35\n• 1 Month – ₹70\n\n🎯 Features:\n📱 Number\n🆔 Aadhaar\n🚗 Vehicle (Normal & Special)",
        'buy_premium': "💳 Buy Premium",
        'payment_info': "💳 **Pay via UPI**\nUPI: `desi.hacker@ybl`\n📅 Plans: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 Scan QR below.\nAfter payment, send screenshot to @Cyber_With_Ranjan.",
        'already_premium': "🎉 You are already premium!",
        'main_menu': "📱 **Main Menu**",
        'search': "🔍 Search",
        'premium': "💎 Premium",
        'number': "📱 Number",
        'vehicle': "🚗 Vehicle",
        'vehicle_special': "🚘 Vehicle Special",
        'aadhaar': "🆔 Aadhaar",
        'claim_btn': "🪙 Claim Coin",
        'profile_btn': "👤 Profile",
        'help_btn': "❓ Help",
        'about_btn': "ℹ️ About",
        'clear_btn': "🗑️ Clear",
        'back': "🔙 Back",
        'owner': "👨‍💻 Owner",
        'group': "🔗 Group",
        'admin_only': "⚠️ You are not authorized.",
        'stats_text': "📊 Stats\n👥 Total: {total}\n✅ Active: {access}\n💎 Premium: {premium}\n🪙 Coins: {coins}\n🔍 Searches: {searches}",
        'enter_number': "📱 Send 10-digit number:",
        'enter_vehicle': "🚗 Send vehicle number:",
        'enter_vehicle_special': "🚘 Send vehicle for Special:",
        'enter_aadhaar': "🆔 Send 12-digit Aadhaar:",
        'coins_left': "🪙 {coins} coins left",
        'premium_active': "💎 Premium Active",
        'not_premium': "❌ No premium access.",
        'follow_insta': "📸 Follow Insta",
        'visit_website': "🌐 Visit Website",
        'get_coin': "🪙 Get 1 FREE Coin",
        'coin_earned': "✅ You earned 1 FREE Coin!",
        'already_done': "✅ Already done!",
        'follow_visit_required': "⚠️ First follow Insta & visit Website.",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 Profile\n🪙 Coins: {coins}\n💎 Premium: {prem}\n🔍 Searches: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ Already claimed today!",
        'wt': "⏳ Fetching...",
        'nc': "❌ No coins! Claim daily 1 FREE Coin.",
        'pin_success': "📌 Message pinned!",
        'pin_fail': "❌ Failed to pin. Make me admin with pin permission."
    },
    'hi': {
        'lang': "🌐 भाषा चुनें:",
        'welcome_premium': "💎 **प्रीमियम आवश्यक**\n📅 प्लान:\n• 1 दिन – ₹10\n• 5 दिन – ₹30\n• 1 सप्ताह – ₹35\n• 1 महीना – ₹70",
        'buy_premium': "💳 प्रीमियम खरीदें",
        'payment_info': "💳 **UPI से भुगतान करें**\nUPI: `desi.hacker@ybl`\nप्लान: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 QR स्कैन करें।",
        'already_premium': "🎉 आप पहले से प्रीमियम हैं!",
        'main_menu': "📱 **मुख्य मेनू**",
        'search': "🔍 खोज",
        'premium': "💎 प्रीमियम",
        'number': "📱 नंबर",
        'vehicle': "🚗 वाहन",
        'vehicle_special': "🚘 वाहन Special",
        'aadhaar': "🆔 आधार",
        'claim_btn': "🪙 Coin लें",
        'profile_btn': "👤 प्रोफाइल",
        'help_btn': "❓ मदद",
        'about_btn': "ℹ️ जानकारी",
        'clear_btn': "🗑️ साफ करें",
        'back': "🔙 वापस",
        'owner': "👨‍💻 मालिक",
        'group': "🔗 ग्रुप",
        'admin_only': "⚠️ आप अधिकृत नहीं।",
        'stats_text': "📊 आँकड़े\n👥 कुल: {total}\n✅ सक्रिय: {access}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 खोज: {searches}",
        'enter_number': "📱 10 अंकों का नंबर भेजें:",
        'enter_vehicle': "🚗 वाहन नंबर भेजें:",
        'enter_vehicle_special': "🚘 Special के लिए वाहन:",
        'enter_aadhaar': "🆔 12 अंकों का आधार:",
        'coins_left': "🪙 {coins} coins बचे",
        'premium_active': "💎 प्रीमियम सक्रिय",
        'not_premium': "❌ प्रीमियम नहीं।",
        'follow_insta': "📸 Insta फॉलो",
        'visit_website': "🌐 वेबसाइट",
        'get_coin': "🪙 1 FREE Coin पाएं",
        'coin_earned': "✅ 1 FREE Coin मिला!",
        'already_done': "✅ पहले ही किया!",
        'follow_visit_required': "⚠️ पहले Insta फॉलो और वेबसाइट विजिट करें।",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 प्रोफाइल\n🪙 Coins: {coins}\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ आज ले लिए!",
        'wt': "⏳ लाया जा रहा...",
        'nc': "❌ कोई Coin नहीं! रोजाना 1 FREE Coin लें।",
        'pin_success': "📌 संदेश पिन किया!",
        'pin_fail': "❌ पिन नहीं कर सका। मुझे पिन अनुमति दें।"
    }
}
# Add other languages (bn, mr, ur, ta) as per your original code

# ---------- HELPERS (unchanged) ----------
# ... (all helper functions remain the same, copy from previous code)

# ---------- API FUNCTIONS with debug logging for admin ----------
def fetch_number(num):
    try:
        url = f"{NUMBER_API_URL}?key={NUMBER_API_KEY}&number={num}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def fetch_aadhaar(aadhaar_num):
    try:
        url = f"{AADHAAR_API_URL}?key={AADHAAR_API_KEY}&aadhaar={aadhaar_num}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# ---------- PROCESS QUERY with debug for admin ----------
def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    l = gl(m.from_user.id)
    # Admin gets unlimited free, but we still deduct coins only if not admin
    if not ip(m.from_user.id):
        coins = gc(m.from_user.id)
        if coins <= 0:
            bot.reply_to(m, L[l]['nc'], reply_markup=premium_start_menu(l))
            return
        if not dc(m.from_user.id):
            bot.reply_to(m, L[l]['nc'], reply_markup=main_menu(l))
            return
    msg = bot.reply_to(m, L[l]['wt'])
    if is_aadhaar:
        d = fetch_aadhaar(q)
    elif is_special:
        d = fetch_vehicle_special(q)
    elif is_vehicle:
        d = fetch_vehicle(q)
    elif is_number_special:
        d = fetch_number_special(q)
    else:
        d = fetch_number(q)
    
    # DEBUG: If user is admin, send raw response to admin chat
    if m.from_user.id == ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, f"🔍 **RAW API RESPONSE** for `{q}`:\n```json\n{json.dumps(d, indent=2)}\n```", parse_mode='Markdown')
        except:
            pass

    if not d:
        try:
            bot.edit_message_text("❌ API returned empty or error. Check raw response in admin chat.", m.chat.id, msg.message_id)
        except:
            bot.send_message(m.chat.id, "❌ API returned empty or error. Check raw response in admin chat.")
        return

    send_log(m.from_user.id, m.from_user.username, m.from_user.first_name, q, d, is_vehicle, is_special, is_aadhaar, is_number_special)
    res = format_result(d, q, is_vehicle, is_special, is_aadhaar, is_number_special)
    try:
        bot.edit_message_text(res, m.chat.id, msg.message_id, parse_mode='Markdown')
        is_group = m.chat.type in ['group', 'supergroup']
        markup = result_btn(q, l, is_vehicle, is_special, is_aadhaar, is_number_special, msg.message_id if is_group else None, is_group)
        bot.edit_message_reply_markup(m.chat.id, msg.message_id, reply_markup=markup)
    except Exception as e:
        bot.send_message(m.chat.id, f"Error: {e}")

# ---------- NEW ADMIN COMMAND: /testapi ----------
@bot.message_handler(commands=['testapi'])
def test_api(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, "❌ Admin only.")
        return
    parts = m.text.split()
    if len(parts) < 3:
        bot.reply_to(m, "❌ /testapi num 9876543210  or  /testapi aadhaar 123412341234")
        return
    typ = parts[1].lower()
    val = parts[2].strip()
    if typ == "num":
        data = fetch_number(val)
    elif typ == "aadhaar":
        data = fetch_aadhaar(val)
    else:
        bot.reply_to(m, "❌ Use 'num' or 'aadhaar'")
        return
    if data:
        bot.reply_to(m, f"✅ **Response:**\n```json\n{json.dumps(data, indent=2)}\n```", parse_mode='Markdown')
    else:
        bot.reply_to(m, "❌ No data or error from API.")

# ---------- The rest of your handlers (unchanged) ----------
# (include all previous callback handlers, admin commands, etc.)

if __name__ == "__main__":
    print("🔥 Hacker OSINT Bot v3.0 (Debug mode) Starting...")
    print(f"👨‍💻 {OWNER}")
    print("✅ Admin will receive raw API responses for debugging.")
    bot.infinity_polling()