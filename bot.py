import telebot, requests, re, sqlite3, datetime, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- CONFIG ----------
BOT_TOKEN = "8622116851:AAGFGCmwV6ijVGxEpLsVBW7LQbmZvqElmTk"  # नया टोकन
ADMIN_ID = 6936978343

# APIs को स्वैप कर दिया गया है
NUMBER_API_URL = "https://anurixx-gift-number.vercel.app/api"          # अब /num इसका उपयोग करेगा (Special)
NUMBER_SPECIAL_URL = "https://num-info-redzone.susxbunny.workers.dev/api"  # अब /special इसका उपयोग करेगा (Normal)

# बाकी APIs वही
AADHAAR_API_URL = "https://leak-osint-redzone.vercel.app/api"
AADHAAR_API_KEY = "REDZONE"
VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"

# Normal Number API के लिए key (अब SPECIAL_URL में यह key काम आएगी)
NUMBER_API_KEY = "redzone@12"

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

# ---------- LANGUAGE DICTIONARIES (All 6 languages) ----------
# (सभी भाषाएँ पहले की तरह – स्पेस बचाने के लिए यहाँ केवल अंग्रेज़ी और हिंदी दिखा रहा हूँ, लेकिन आपके पास सभी 6 होंगी)
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
    },
    'bn': { ... },  # पूरी डिक्शनरी आपके पास है, यहाँ स्पेस बचाने के लिए छोड़ रहा हूँ
    'mr': { ... },
    'ur': { ... },
    'ta': { ... }
}
# (अन्य भाषाओं को अपने मूल कोड से कॉपी करें)

# ---------- HELPERS ----------
def gl(i):
    try: c.execute("SELECT lang FROM users WHERE user_id=?", (i,)); r=c.fetchone(); return r[0] if r else 'en'
    except: return 'en'
def sl(i,l):
    try: c.execute("UPDATE users SET lang=? WHERE user_id=?", (l, i)); conn.commit()
    except: pass
def au(i,n,u=""):
    try: c.execute("INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?,?,?)", (i,n,u)); conn.commit()
    except: pass
def ha(i):
    if i==ADMIN_ID: return True
    try: c.execute("SELECT access FROM users WHERE user_id=?", (i,)); r=c.fetchone(); return r and r[0]==1
    except: return False
def ga(i):
    try: c.execute("UPDATE users SET access=1, coins=1 WHERE user_id=?", (i,)); conn.commit()
    except: pass
def gc(i):
    try: c.execute("SELECT coins FROM users WHERE user_id=?", (i,)); r=c.fetchone(); return r[0] if r else 0
    except: return 0
def dc(i):
    if ip(i): return True
    try:
        coins=gc(i)
        if coins<=0: return False
        c.execute("UPDATE users SET coins=coins-1, searches=searches+1 WHERE user_id=?", (i,)); conn.commit(); return True
    except: return False
def adc(i):
    try:
        t=datetime.datetime.now().date().isoformat()
        c.execute("SELECT last_claim FROM users WHERE user_id=?", (i,)); r=c.fetchone()
        if r and r[0]==t: return False
        c.execute("UPDATE users SET coins=coins+1, last_claim=? WHERE user_id=?", (t, i)); conn.commit(); return True
    except: return False
def ip(i):
    if i==ADMIN_ID: return True
    try:
        c.execute("SELECT premium, premium_expiry FROM users WHERE user_id=?", (i,)); r=c.fetchone()
        if not r or r[0]==0: return False
        if r[1]:
            if datetime.datetime.fromisoformat(r[1]) > datetime.datetime.now(): return True
            else: c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (i,)); conn.commit(); return False
        return True
    except: return False
def ap(i,d=30):
    try:
        e=(datetime.datetime.now()+datetime.timedelta(days=d)).isoformat()
        c.execute("UPDATE users SET premium=1, premium_expiry=?, access=1 WHERE user_id=?", (e, i))
        conn.commit(); return True
    except: return False
def mark_insta(i):
    try: c.execute("UPDATE users SET insta_followed=1 WHERE user_id=?", (i,)); conn.commit(); return True
    except: return False
def mark_website(i):
    try: c.execute("UPDATE users SET website_visited=1 WHERE user_id=?", (i,)); conn.commit(); return True
    except: return False
def check_both_done(i):
    try: c.execute("SELECT insta_followed, website_visited FROM users WHERE user_id=?", (i,)); r=c.fetchone(); return r and r[0]==1 and r[1]==1
    except: return False
def get_total_searches():
    try: c.execute("SELECT SUM(searches) FROM users"); r=c.fetchone(); return r[0] if r and r[0] else 0
    except: return 0

# ---------- API FUNCTIONS (स्वैप किए गए) ----------
def fetch_number(num):
    """अब यह Special API को कॉल करता है (क्योंकि URL बदला है)"""
    try:
        url = f"{NUMBER_API_URL}?num={num}"  # Special API को key की ज़रूरत नहीं
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def fetch_number_special(phone):
    """अब यह Normal API को कॉल करता है (क्योंकि URL बदला है)"""
    try:
        url = f"{NUMBER_SPECIAL_URL}?key={NUMBER_API_KEY}&number={phone}"  # Normal API key के साथ
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

def fetch_vehicle(vehicle_num):
    try:
        url = f"{VEHICLE_API_URL}?type=vehicle&search={vehicle_num.upper()}"
        r=requests.get(url, timeout=10)
        if r.status_code==200:
            data = r.json()
            if data.get('regNo'): return data
        return None
    except: return None

def fetch_vehicle_special(vehicle_num):
    try:
        url = f"{VEHICLE_SPECIAL_API_URL}?number={vehicle_num.upper()}"
        r=requests.get(url, timeout=10)
        if r.status_code==200: return r.json()
        return None
    except: return None

# ---------- FORMAT ----------
def format_result(data, query, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    if is_aadhaar:
        # ... (पहले जैसा)
        pass
    elif is_number_special:
        # अब यह Normal API का response handle करेगा (क्योंकि हमने स्वैप किया)
        if not data:
            return "`❌ No data`"
        # Normal API का फॉर्मेट: {result: [...]} या सीधा object
        if isinstance(data, dict):
            if 'result' in data and isinstance(data['result'], list) and data['result']:
                info = data['result'][0]
            elif 'data' in data and isinstance(data['data'], dict):
                info = data['data']
            else:
                info = data
        else:
            info = {}
        if not info or not info.get('name'):
            return "`❌ No records`"
        name = info.get('name', 'N/A')
        father = info.get('fname') or info.get('father', 'N/A')
        aadhar = info.get('aadhar') or info.get('aadhaar', 'N/A')
        address = info.get('address') or info.get('addr', 'N/A')
        circle = info.get('circle') or info.get('operator', 'N/A')
        email = info.get('email') or info.get('mail', 'N/A')
        alt = info.get('alt') or info.get('alternate', 'N/A')
        return f"""
`📱 NUMBER INTEL (Normal API via /special)
━━━━━━━━━━━━━━━━━━━━━
📱 Number: {query}
👤 Name: {name}
👨 Father: {father}
🆔 Aadhar: {aadhar}
🏠 Address: {address}
📡 Circle: {circle}
📧 Email: {email}
📞 Alt: {alt}
🔐 {OWNER}`
"""
    elif is_vehicle:
        # ... (पहले जैसा)
        pass
    elif is_special:
        # ... (पहले जैसा)
        pass
    else:
        # अब यह Special API का response handle करेगा (क्योंकि हमने स्वैप किया)
        if not data or data.get('status') != 'success':
            return "`❌ No data`"
        info = data.get('data', {})
        if not info:
            return "`❌ No records`"
        name = info.get('name', 'N/A')
        phone = info.get('phone', query)
        address = info.get('address', 'N/A')
        circle = info.get('circle', 'N/A')
        alt = info.get('alt', 'N/A')
        email = info.get('email', 'N/A')
        aadhar = info.get('aadhar', 'N/A')
        return f"""
`📱 NUMBER SPECIAL INTEL (via /num)
━━━━━━━━━━━━━━━━━━━━━
📱 Number: {phone}
👤 Name: {name}
🆔 Aadhar: {aadhar}
🏠 Address: {address}
📡 Circle: {circle}
📧 Email: {email}
📞 Alt: {alt}
🔐 {OWNER}`
"""

def format_json(data):
    return f"`{json.dumps(data, indent=2)}`"

def send_log(uid, un, nm, query, data, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    # ... (पहले जैसा – कोई बदलाव नहीं)
    pass

# ---------- KEYBOARDS ----------
# (सभी keyboard functions पहले जैसे हैं – यहाँ नहीं दोहरा रहा)

# ---------- HANDLERS ----------
# (सभी handlers पहले जैसे – सिर्फ process_query में बदलाव)

def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    l = gl(m.from_user.id)
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
        d = fetch_number_special(q)   # /special अब Normal API का उपयोग करेगा
    else:
        d = fetch_number(q)           # /num अब Special API का उपयोग करेगा
    
    # DEBUG: Admin को raw response
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

# ---------- COMMANDS ----------
@bot.message_handler(commands=['num','search'])
def nc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip(), False, False, False, False)  # is_number_special=False

@bot.message_handler(commands=['special','s'])
def special_cmd(m):
    p=m.text.split()
    if len(p)<2:
        bot.reply_to(m, "❌ /special 9661756498 (10-digit number)")
        return
    phone = p[1].strip()
    if not re.match(r'^\d{10}$', phone):
        bot.reply_to(m, "❌ Enter a valid 10-digit number.")
        return
    process_query(m, phone, False, False, False, True)  # is_number_special=True

# ---------- बाकी सभी handlers (vehicle, aadhaar, admin commands, etc.) पहले जैसे हैं ----------
# (कृपया अपने पूरे कोड में ये सभी शामिल करें – मैंने सिर्फ मुख्य बदलाव दिखाए हैं)

if __name__ == "__main__":
    print("🔥 Hacker OSINT Bot v3.0 (Swapped APIs) Starting...")
    print(f"👨‍💻 {OWNER}")
    print("✅ /num → Special API, /special → Normal API")
    bot.infinity_polling()