import telebot, requests, re, sqlite3, datetime, json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- CONFIG ----------
BOT_TOKEN = "8622116851:AAGFGCmwV6ijVGxEpLsVBW7LQbmZvqElmTk"
NUMBER_API_URL = "https://movements-invoice-amanda-victoria.trycloudflare.com/search/number"
API_KEY = "mysecretkey123"
VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"
ADMIN_ID = 6936978343
OWNER = "@Cyber_With_Ranjan"
INSTA = "https://www.instagram.com/ranjan_bhai_194"
WEBSITE = "https://cyberwithranjanbhai.attackerhydra.workers.dev/"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
SUPPORT_GROUP = "https://t.me/cyberwithranjan"

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, lang TEXT DEFAULT 'en', coins INTEGER DEFAULT 0, last_claim TEXT, access INTEGER DEFAULT 0, premium INTEGER DEFAULT 0, premium_expiry TEXT, searches INTEGER DEFAULT 0, insta_followed INTEGER DEFAULT 0, website_visited INTEGER DEFAULT 0)''')
conn.commit()

# ---------- LANGUAGE ----------
L = {
    'en': {
        'welcome': "👋 Welcome to **Number OSINT Bot**!\n\n🔍 Get info from Phone, Vehicle (Normal & Special).\n🪙 1 FREE Coin daily = 1 Search!\n💎 Premium: Unlimited searches.",
        'lang': "🌐 Select Language:",
        'if': "📸 Follow Insta",
        'wv': "🌐 Visit Website",
        'gc': "🪙 Claim Coin",
        'p': "💎 **Premium Plans**\n\n📅 1 Week – ₹50\n📅 1 Month – ₹80\n\n💳 UPI: `desi.hacker@ybl`\n📸 Pay & send screenshot to @Cyber_With_Ranjan",
        'd': "✅ Follow & Visit first!",
        't': "✅ Access Granted! You got 1 FREE Coin!",
        'nc': "❌ No coins left!\n🪙 Claim your daily 1 FREE Coin.",
        'al': "✅ Already claimed today! Come back tomorrow.",
        'wt': "⏳ Fetching data...",
        'about': "🤖 **Number OSINT Bot**\n\nVersion 2.0\n👨‍💻 Developed by @Cyber_With_Ranjan\n\n🔹 Get details from phone numbers, vehicle numbers.\n🔹 Daily free coin system.\n🔹 Premium plans for unlimited access.\n🔹 Support: @Cyber_With_Ranjan",
        'help': "📖 **Commands**\n\n/start – Start bot\n/menu – Main menu\n/num [number] – Phone number info\n/vehicle [number] – Vehicle info (Normal)\n/vehiclespecial [number] – Vehicle info (Special)\n/claim – Claim daily 1 coin\n/premium – Premium plans\n/profile – Your profile\n/contact – Contact admin\n/clear – Clear chat history\n/language – Change language",
        'profile': "👤 **Profile**\n🪙 Coins: {coins}\n💎 Premium: {prem}\n🔍 Searches: {searches}",
        'search': "🔍 Search",
        'premium': "💎 Premium",
        'account': "👤 Account",
        'info': "ℹ️ Info",
        'number': "📱 Number",
        'vehicle': "🚗 Vehicle",
        'vehicle_special': "🚘 Vehicle Special",
        'claim_btn': "🪙 Claim Daily Coin",
        'profile_btn': "👤 Profile",
        'help_btn': "❓ Help",
        'about_btn': "ℹ️ About",
        'contact_btn': "📞 Contact",
        'support_btn': "📢 Channel",
        'clear_btn': "🗑️ Clear History",
        'back': "🔙 Back",
        'owner': "👨‍💻 Owner",
        'group': "🔗 Group",
        'coming_soon': "🚀 This feature is coming soon!",
        'admin_only': "⚠️ You are not authorized to use this command.",
        'broadcast_sent': "✅ Broadcast sent to all users!",
        'broadcast_fail': "❌ Failed to send broadcast.",
        'stats_text': "📊 **Bot Statistics**\n👥 Total Users: {total}\n✅ Active Users (access): {access}\n💎 Premium Users: {premium}\n🪙 Total Coins: {coins}\n🔍 Total Searches: {searches}",
        'enter_number': "📱 Send 10-digit number:",
        'enter_vehicle': "🚗 Send vehicle number (e.g., RJ14CV0002):",
        'enter_vehicle_special': "🚘 Send vehicle number for Special API:",
        'result_ready': "✅ Result Ready!",
        'coins_left': "🪙 {coins} coins left",
        'premium_active': "💎 Premium Active",
        'not_premium': "❌ No premium access.",
        'thank_you': "🙏 Thank you for using Number OSINT Bot!"
    },
    'hi': {
        'welcome': "👋 **Number OSINT Bot** में स्वागत है!\n\n🔍 फोन, वाहन (Normal & Special) से जानकारी पाएं।\n🪙 रोजाना 1 FREE Coin = 1 Search!\n💎 Premium: असीमित खोज।",
        'lang': "🌐 भाषा चुनें:",
        'if': "📸 Insta फॉलो",
        'wv': "🌐 वेबसाइट",
        'gc': "🪙 Coin लें",
        'p': "💎 **प्रीमियम प्लान**\n\n📅 1 सप्ताह – ₹50\n📅 1 महीना – ₹80\n\n💳 UPI: `desi.hacker@ybl`\n📸 भुगतान करें और @Cyber_With_Ranjan को स्क्रीनशॉट भेजें",
        'd': "✅ पहले फॉलो और विजिट करें!",
        't': "✅ एक्सेस मिल गया! आपको 1 FREE Coin मिला!",
        'nc': "❌ कोई Coin नहीं!\n🪙 रोजाना 1 FREE Coin लें।",
        'al': "✅ आज पहले ही ले लिए! कल आएं।",
        'wt': "⏳ डेटा लाया जा रहा...",
        'about': "🤖 **Number OSINT Bot**\n\nVersion 2.0\n👨‍💻 विकसक: @Cyber_With_Ranjan\n\n🔹 फोन नंबर, वाहन नंबर से जानकारी\n🔹 रोजाना फ्री Coin सिस्टम\n🔹 Premium प्लान – असीमित उपयोग\n🔹 सहायता: @Cyber_With_Ranjan",
        'help': "📖 **कमांड्स**\n\n/start – बॉट शुरू करें\n/menu – मुख्य मेनू\n/num [number] – फोन नंबर जानकारी\n/vehicle [number] – वाहन जानकारी (Normal)\n/vehiclespecial [number] – वाहन जानकारी (Special)\n/claim – रोजाना 1 Coin लें\n/premium – प्रीमियम प्लान\n/profile – प्रोफाइल\n/contact – संपर्क करें\n/clear – चैट साफ करें\n/language – भाषा बदलें",
        'profile': "👤 **प्रोफाइल**\n🪙 Coins: {coins}\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}",
        'search': "🔍 खोज",
        'premium': "💎 प्रीमियम",
        'account': "👤 खाता",
        'info': "ℹ️ जानकारी",
        'number': "📱 नंबर",
        'vehicle': "🚗 वाहन",
        'vehicle_special': "🚘 वाहन Special",
        'claim_btn': "🪙 रोजाना Coin",
        'profile_btn': "👤 प्रोफाइल",
        'help_btn': "❓ मदद",
        'about_btn': "ℹ️ जानकारी",
        'contact_btn': "📞 संपर्क",
        'support_btn': "📢 चैनल",
        'clear_btn': "🗑️ हिस्ट्री साफ करें",
        'back': "🔙 वापस",
        'owner': "👨‍💻 मालिक",
        'group': "🔗 ग्रुप",
        'coming_soon': "🚀 यह सुविधा जल्द आ रही है!",
        'admin_only': "⚠️ आप इस कमांड का उपयोग नहीं कर सकते।",
        'broadcast_sent': "✅ सभी उपयोगकर्ताओं को संदेश भेजा गया!",
        'broadcast_fail': "❌ संदेश भेजने में विफल।",
        'stats_text': "📊 **बॉट आँकड़े**\n👥 कुल उपयोगकर्ता: {total}\n✅ सक्रिय (access): {access}\n💎 प्रीमियम: {premium}\n🪙 कुल Coins: {coins}\n🔍 कुल खोज: {searches}",
        'enter_number': "📱 10 अंकों का नंबर भेजें:",
        'enter_vehicle': "🚗 वाहन नंबर भेजें (जैसे RJ14CV0002):",
        'enter_vehicle_special': "🚘 Special API के लिए वाहन नंबर भेजें:",
        'result_ready': "✅ परिणाम तैयार!",
        'coins_left': "🪙 {coins} coins बचे",
        'premium_active': "💎 प्रीमियम सक्रिय",
        'not_premium': "❌ प्रीमियम नहीं।",
        'thank_you': "🙏 Number OSINT Bot का उपयोग करने के लिए धन्यवाद!"
    }
}

# ---------- DATABASE HELPERS ----------
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
        conn.commit()
        return True
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

# ---------- API FUNCTIONS ----------
def fetch_number(num):
    try:
        r=requests.get(f"{NUMBER_API_URL}?number={num}&key={API_KEY}", timeout=10)
        return r.json() if r.status_code==200 else None
    except: return None

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
        if r.status_code==200:
            return r.json()
        return None
    except:
        return None

# ---------- FORMAT FUNCTIONS ----------
def format_result(data, num, is_vehicle=False, is_special=False):
    if is_special:
        if not data or not data.get('reg_no'):
            return "❌ Vehicle not found"
        return f"""
🚘 **Vehicle Special Details**
━━━━━━━━━━━━━━━━━━━━━
🚘 Number: {data.get('reg_no', 'N/A')}
👤 Owner: {data.get('owner_name', 'N/A')}
🚗 Class: {data.get('vehicle_class', 'N/A')}
⛽ Fuel: {data.get('fuel_type', 'N/A')}
🔧 Engine: {data.get('engine_no', 'N/A')}
🔩 Chassis: {data.get('chassis_no', 'N/A')}
📅 Reg Date: {data.get('reg_date', 'N/A')}
📋 Status: {data.get('status', 'N/A')}
🏭 Model: {data.get('maker_model', 'N/A')}
📅 Fitness Upto: {data.get('fitness_upto', 'N/A')}
🏢 Insurance: {data.get('insurance_company', 'N/A')}
📅 Insurance Upto: {data.get('insurance_upto', 'N/A')}
🔐 {OWNER}
"""
    elif is_vehicle:
        if not data or not data.get('regNo'): return "❌ Vehicle not found"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"""
🚗 **Vehicle Details**
━━━━━━━━━━━━━━━━━━━━━
🚘 Number: {data.get('regNo', 'N/A')}
👤 Owner: {i.get('ownerName', 'N/A')}
🏭 Company: {i.get('manufacturer', 'N/A')}
🚗 Model: {i.get('vehicle', 'N/A')}
📅 Reg Date: {i.get('regDate', 'N/A')}
🏢 RTO: {rto.get('rtoCode', 'N/A')}
📋 Status: {'✅' if i.get('status')=='100' else '❌'}
🏠 Address: {i.get('presentAddress', 'N/A')}
📱 Owner: {data.get('owner', 'N/A')}
🔐 {OWNER}
"""
    else:
        if not data or data.get('status')!='success': return "❌ No data"
        i=data['result'][0]; a=i.get('address','N/A').replace('!',', ')
        return f"""
📱 **Number Details**
━━━━━━━━━━━━━━━━━━━━━
📱 Number: {num}
👤 Name: {i.get('name','N/A')}
👨 Father: {i.get('fname','N/A')}
🆔 Aadhar: {i.get('aadhar','N/A')}
🏠 Address: {a}
📡 Circle: {i.get('circle','N/A')}
📧 Email: {i.get('email','N/A')}
📞 Alt: {i.get('alt','N/A')}
🔐 {OWNER}
"""

def format_json(data):
    return json.dumps(data, indent=2)

def send_log(uid, un, nm, query, data, is_vehicle=False, is_special=False):
    try:
        if is_special:
            bot.send_message(ADMIN_ID, f"🚘 SPECIAL VEHICLE LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {data.get('reg_no','N/A')}")
        elif is_vehicle:
            i = data.get('response', {})
            bot.send_message(ADMIN_ID, f"🚗 VEHICLE LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {i.get('vehicle','N/A')}")
        else:
            if not data or data.get('status')!='success': return
            i=data['result'][0]
            bot.send_message(ADMIN_ID, f"📊 NUMBER LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n📱 {i.get('name','N/A')}")
    except: pass

# ---------- KEYBOARDS ----------
def start_btn(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton(L[l]['if'], callback_data="insta_done"),
        InlineKeyboardButton(L[l]['wv'], callback_data="website_done")
    )
    mk.add(InlineKeyboardButton(L[l]['gc'], callback_data="claim"))
    mk.add(InlineKeyboardButton(L[l]['group'], url=GROUP))
    return mk

def main_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🔍 " + L[l]['search'], callback_data="search_menu"))
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="premium"))
    mk.add(InlineKeyboardButton("🪙 " + L[l]['claim_btn'], callback_data="claim"))
    mk.add(InlineKeyboardButton("👤 " + L[l]['profile_btn'], callback_data="profile"))
    mk.add(InlineKeyboardButton("❓ " + L[l]['help_btn'], callback_data="help"))
    mk.add(InlineKeyboardButton("ℹ️ " + L[l]['about_btn'], callback_data="about"))
    mk.add(
        InlineKeyboardButton("📢 Channel", url=CHANNEL),
        InlineKeyboardButton("📞 Support", url=SUPPORT_GROUP)
    )
    mk.add(
        InlineKeyboardButton(L[l]['clear_btn'], callback_data="clear"),
        InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan")
    )
    return mk

def search_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton(L[l]['number'], callback_data="info"),
        InlineKeyboardButton(L[l]['vehicle'], callback_data="vehicle_info"),
        InlineKeyboardButton(L[l]['vehicle_special'], callback_data="vehicle_special_info")
    )
    mk.add(InlineKeyboardButton(L[l]['back'], callback_data="main_menu"))
    return mk

def group_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton(L[l]['number'], callback_data="info"),
        InlineKeyboardButton(L[l]['vehicle'], callback_data="vehicle_info"),
        InlineKeyboardButton(L[l]['vehicle_special'], callback_data="vehicle_special_info")
    )
    mk.add(
        InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="premium"),
        InlineKeyboardButton("🪙 " + L[l]['claim_btn'], callback_data="claim")
    )
    mk.add(
        InlineKeyboardButton(L[l]['clear_btn'], callback_data="clear"),
        InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan")
    )
    mk.add(
        InlineKeyboardButton("📢 Channel", url=CHANNEL),
        InlineKeyboardButton("📞 Support", url=SUPPORT_GROUP)
    )
    return mk

def result_btn(query, lang, is_vehicle=False, is_special=False):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"json_{query}_{is_vehicle}_{is_special}"))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🗑️ " + L[lang]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton("🔙 " + L[lang]['back'], callback_data="main_menu"))
    return mk

def premium_btn(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("💳 ₹50 - 1W", callback_data="pay_50"),
        InlineKeyboardButton("💳 ₹80 - 1M", callback_data="pay_80")
    )
    mk.add(
        InlineKeyboardButton("📞 Admin", url="https://t.me/Cyber_With_Ranjan"),
        InlineKeyboardButton("🔙 " + L[l]['back'], callback_data="main_menu")
    )
    return mk

def back_btn(l):
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🔙 " + L[l]['back'], callback_data="main_menu"))
    return mk

# ---------- HANDLERS ----------
@bot.message_handler(commands=['start'])
def st(m):
    au(m.from_user.id, m.from_user.first_name or "", m.from_user.username or "")
    mk=InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"))
    mk.add(InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"))
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lc(c):
    l=c.data.split('_')[1]; sl(c.from_user.id, l)
    if ha(c.from_user.id):
        try: bot.edit_message_text(L[l]['welcome'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
        except: bot.send_message(c.message.chat.id, L[l]['welcome'], reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        try: bot.edit_message_text("👋 " + L[l]['welcome'].split('\n')[0] + "\n\n📌 " + L[l]['d'], c.message.chat.id, c.message.message_id, reply_markup=start_btn(l), parse_mode='Markdown')
        except: bot.send_message(c.message.chat.id, "👋 " + L[l]['welcome'].split('\n')[0] + "\n\n📌 " + L[l]['d'], reply_markup=start_btn(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "✅")

@bot.callback_query_handler(func=lambda c: c.data in ["insta_done","website_done"])
def fcb(c):
    if c.data=="insta_done": mark_insta(c.from_user.id)
    else: mark_website(c.from_user.id)
    l=gl(c.from_user.id)
    if check_both_done(c.from_user.id):
        ga(c.from_user.id)
        bot.answer_callback_query(c.id, "✅ +1 Coin!")
        try: bot.edit_message_text("✅ " + L[l]['t'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
        except: bot.send_message(c.message.chat.id, "✅ " + L[l]['t'], reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        bot.answer_callback_query(c.id, "✅ Done!")

@bot.callback_query_handler(func=lambda c: c.data=="claim")
def claim_cb(c):
    l=gl(c.from_user.id)
    if not ha(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['d'], True)
        return
    if adc(c.from_user.id):
        coins=gc(c.from_user.id)
        bot.answer_callback_query(c.id, "🪙 +1! Total: "+str(coins))
        bot.send_message(c.message.chat.id, "✅ +1 Coin!\n🪙 Total: "+str(coins), reply_markup=main_menu(l))
    else:
        bot.answer_callback_query(c.id, "❌ " + L[l]['al'], True)
        bot.send_message(c.message.chat.id, L[l]['al'])

@bot.callback_query_handler(func=lambda c: c.data=="premium")
def premium_cb(c):
    l=gl(c.from_user.id)
    bot.answer_callback_query(c.id, "💎 Premium")
    bot.send_message(c.message.chat.id, L[l]['p'], reply_markup=premium_btn(l), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data in ["pay_50","pay_80"])
def pay_cb(c):
    l=gl(c.from_user.id); a="₹50" if c.data=="pay_50" else "₹80"
    bot.answer_callback_query(c.id, "💳 " + a)
    bot.send_message(c.message.chat.id, f"💳 **Pay {a} on UPI:** `desi.hacker@ybl`\n📸 Send screenshot to @Cyber_With_Ranjan\n✅ Premium will be activated after verification!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="profile")
def profile_cb(c):
    uid=c.from_user.id; coins=gc(uid); prem="✅" if ip(uid) else "❌"; searches=0
    try: c.execute("SELECT searches FROM users WHERE user_id=?", (uid,)); r=c.fetchone(); searches=r[0] if r else 0
    except: pass
    l=gl(uid)
    bot.answer_callback_query(c.id, "👤 Profile")
    bot.send_message(c.message.chat.id, L[l]['profile'].format(coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="help")
def help_cb(c):
    l=gl(c.from_user.id)
    bot.answer_callback_query(c.id, "❓ Help")
    bot.send_message(c.message.chat.id, L[l]['help'], reply_markup=back_btn(l), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="about")
def about_cb(c):
    l=gl(c.from_user.id)
    bot.answer_callback_query(c.id, "ℹ️ About")
    bot.send_message(c.message.chat.id, L[l]['about'], reply_markup=back_btn(l), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="clear")
def clear_cb(c):
    try:
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.answer_callback_query(c.id, "🗑️ Cleared!")
        bot.send_message(c.message.chat.id, "✅ Chat history cleared!")
    except:
        bot.answer_callback_query(c.id, "❌ Can't clear!", True)

@bot.callback_query_handler(func=lambda c: c.data=="main_menu")
def main_menu_cb(c):
    l=gl(c.from_user.id)
    try: bot.edit_message_text(L[l]['welcome'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
    except: bot.send_message(c.message.chat.id, L[l]['welcome'], reply_markup=main_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔙")

@bot.callback_query_handler(func=lambda c: c.data=="search_menu")
def search_menu_cb(c):
    l=gl(c.from_user.id)
    try: bot.edit_message_text("🔍 " + L[l]['search'], c.message.chat.id, c.message.message_id, reply_markup=search_menu(l), parse_mode='Markdown')
    except: bot.send_message(c.message.chat.id, "🔍 " + L[l]['search'], reply_markup=search_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data in ["info", "vehicle_info", "vehicle_special_info"])
def info_cb(c):
    l=gl(c.from_user.id)
    is_vehicle = c.data == "vehicle_info"
    is_special = c.data == "vehicle_special_info"
    if not ha(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['d'], True)
        bot.send_message(c.message.chat.id, "📌 " + L[l]['d'], reply_markup=start_btn(l)); return
    coins=gc(c.from_user.id)
    if coins<=0 and not ip(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['nc'], True)
        bot.send_message(c.message.chat.id, L[l]['nc'], reply_markup=main_menu(l)); return
    bot.answer_callback_query(c.id, f"🪙 {coins} coins left")
    if is_special:
        bot.send_message(c.message.chat.id, L[l]['enter_vehicle_special'])
    elif is_vehicle:
        bot.send_message(c.message.chat.id, L[l]['enter_vehicle'])
    else:
        bot.send_message(c.message.chat.id, L[l]['enter_number'])

@bot.callback_query_handler(func=lambda c: c.data.startswith('json_'))
def json_cb(c):
    parts=c.data.split('_')[1:]
    q=parts[0]
    is_vehicle = parts[1] == 'True' if len(parts) > 1 else False
    is_special = parts[2] == 'True' if len(parts) > 2 else False
    if is_special:
        d=fetch_vehicle_special(q)
    elif is_vehicle:
        d=fetch_vehicle(q)
    else:
        d=fetch_number(q)
    if not d:
        bot.answer_callback_query(c.id, "❌", True); return
    bot.answer_callback_query(c.id, "📊 JSON")
    bot.send_message(c.message.chat.id, f"📊 JSON:\n{format_json(d)}")

def process_query(m, q, is_vehicle=False, is_special=False):
    l=gl(m.from_user.id)
    if not ha(m.from_user.id):
        bot.reply_to(m, "📌 " + L[l]['d'], reply_markup=start_btn(l)); return
    if not ip(m.from_user.id):
        coins=gc(m.from_user.id)
        if coins<=0:
            bot.reply_to(m, L[l]['nc'], reply_markup=main_menu(l)); return
        if not dc(m.from_user.id):
            bot.reply_to(m, L[l]['nc'], reply_markup=main_menu(l)); return
    msg=bot.reply_to(m, L[l]['wt'])
    if is_special:
        d=fetch_vehicle_special(q)
    elif is_vehicle:
        d=fetch_vehicle(q)
    else:
        d=fetch_number(q)
    if not d:
        try: bot.edit_message_text("❌ Error!", m.chat.id, msg.message_id)
        except: bot.send_message(m.chat.id, "❌ Error!")
        return
    send_log(m.from_user.id, m.from_user.username, m.from_user.first_name, q, d, is_vehicle, is_special)
    res=format_result(d, q, is_vehicle, is_special)
    try: bot.edit_message_text(f"{res}\n\n📊 JSON:\n{format_json(d)}", m.chat.id, msg.message_id)
    except: bot.send_message(m.chat.id, f"{res}\n\n📊 JSON:\n{format_json(d)}")
    coins_left=gc(m.from_user.id)
    status = f"🪙 {coins_left} coins" if not ip(m.from_user.id) else "💎 Premium"
    bot.send_message(m.chat.id, f"✅ Ready!\n{status}", reply_markup=result_btn(q, l, is_vehicle, is_special))

@bot.message_handler(commands=['num','search'])
def nc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip(), False, False)

@bot.message_handler(commands=['vehicle','v'])
def vc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle']); return
    process_query(m, p[1].strip(), True, False)

@bot.message_handler(commands=['vehiclespecial','vs'])
def vsc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle_special']); return
    process_query(m, p[1].strip(), False, True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text))
def hn(m):
    if m.chat.type in ['group','supergroup']: return
    process_query(m, m.text.strip(), False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', m.text.upper()))
def vhn(m):
    if m.chat.type in ['group','supergroup']: return
    process_query(m, m.text.strip().upper(), True, False)

# ----- GROUP HANDLERS -----
@bot.message_handler(commands=['num'], chat_types=['group','supergroup'])
def gn(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /num 9661756498"); return
    process_query(m, p[1].strip(), False, False)

@bot.message_handler(commands=['vehicle'], chat_types=['group','supergroup'])
def gv(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /vehicle RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), True, False)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group','supergroup'])
def gvs(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /vehiclespecial RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), False, True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text), chat_types=['group','supergroup'])
def ghn(m):
    process_query(m, m.text.strip(), False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', m.text.upper()), chat_types=['group','supergroup'])
def gvh(m):
    process_query(m, m.text.strip().upper(), True, False)

@bot.message_handler(commands=['start','help'], chat_types=['group','supergroup'])
def gs(m):
    l=gl(m.from_user.id)
    bot.reply_to(m, "👋 /num 9661756498 | /vehicle RJ14CV0002 | /vehiclespecial RJ14CV0002\n🪙 1 FREE Coin/day = 1 Search!\n💎 1W ₹50 | 1M ₹80", reply_markup=group_menu(l))

@bot.message_handler(commands=['menu'])
def me(m):
    l=gl(m.from_user.id)
    if m.chat.type in ['group','supergroup']:
        bot.send_message(m.chat.id, "📱 Menu", reply_markup=group_menu(l))
        return
    if not ha(m.from_user.id):
        bot.send_message(m.chat.id, "📌 " + L[l]['d'], reply_markup=start_btn(l))
        return
    bot.send_message(m.chat.id, L[l]['welcome'], reply_markup=main_menu(l), parse_mode='Markdown')

@bot.message_handler(commands=['claim'])
def cl2(m):
    l=gl(m.from_user.id)
    if not ha(m.from_user.id):
        bot.reply_to(m, "📌 " + L[l]['d'], reply_markup=start_btn(l)); return
    if adc(m.from_user.id):
        coins=gc(m.from_user.id)
        bot.reply_to(m, f"✅ +1 Coin!\n🪙 Total: {coins}")
    else:
        bot.reply_to(m, L[l]['al'])

@bot.message_handler(commands=['premium'])
def pm(m):
    l=gl(m.from_user.id)
    bot.reply_to(m, L[l]['p'], reply_markup=premium_btn(l), parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
def pr2(m):
    uid=m.from_user.id; coins=gc(uid); prem="✅" if ip(uid) else "❌"; searches=0
    try: c.execute("SELECT searches FROM users WHERE user_id=?", (uid,)); r=c.fetchone(); searches=r[0] if r else 0
    except: pass
    l=gl(uid)
    bot.reply_to(m, L[l]['profile'].format(coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.message_handler(commands=['contact'])
def ct(m): bot.reply_to(m, f"📞 {OWNER}\n🔗 {GROUP}")

@bot.message_handler(commands=['clear'])
def clear_cmd(m):
    try:
        bot.delete_message(m.chat.id, m.message_id)
        bot.reply_to(m, "🗑️ Cleared!")
    except:
        bot.reply_to(m, "❌ Can't clear!")

@bot.message_handler(commands=['help'])
def hp(m):
    if m.chat.type in ['group','supergroup']: return
    l=gl(m.from_user.id)
    bot.reply_to(m, L[l]['help'], parse_mode='Markdown')

@bot.message_handler(commands=['language','lang'])
def lg(m):
    mk=InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")); mk.add(InlineKeyboardButton("🇮🇳 हिन्दी", callback_data="lang_hi"))
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=mk)

# ---------- ADMIN COMMANDS ----------
@bot.message_handler(commands=['addpremium'])
def ap2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = m.text.split()
        if ap(int(uid), int(days)):
            bot.reply_to(m, f"✅ Premium added to {uid} for {days} days!")
            bot.send_message(int(uid), f"🎉 Premium activated for {days} days!\n✅ Now you have unlimited access!")
    except: bot.reply_to(m, "❌ /addpremium [user_id] [days]")

@bot.message_handler(commands=['removepremium'])
def rp(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (int(uid),)); conn.commit()
        bot.reply_to(m, f"✅ Removed premium from {uid}")
    except: bot.reply_to(m, "❌ /removepremium [user_id]")

@bot.message_handler(commands=['addcoins'])
def ac(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, coins = m.text.split()
        c.execute("UPDATE users SET coins=coins+? WHERE user_id=?", (int(coins), int(uid))); conn.commit()
        bot.reply_to(m, f"✅ +{coins} coins to {uid}")
    except: bot.reply_to(m, "❌ /addcoins [user_id] [coins]")

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT user_id, username, access, coins, premium FROM users LIMIT 20")
        users=c.fetchall()
        if not users: bot.reply_to(m, "No users."); return
        text="📋 Users:\n"
        for u in users: text += f"🆔 {u[0]} | {u[1]} | {'✅' if u[2] else '❌'} | 🪙{u[3]} | {'💎' if u[4] else ''}\n"
        bot.reply_to(m, text)
    except: pass

@bot.message_handler(commands=['stats'])
def st2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT COUNT(*) FROM users"); total=c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE access=1"); access=c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM users WHERE premium=1"); premium=c.fetchone()[0]
        c.execute("SELECT SUM(coins) FROM users"); coins=c.fetchone()[0] or 0
        searches=get_total_searches()
        l=gl(m.from_user.id)
        bot.reply_to(m, L[l]['stats_text'].format(total=total, access=access, premium=premium, coins=coins, searches=searches), parse_mode='Markdown')
    except: pass

@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, L['en']['admin_only'])
        return
    msg = m.text.replace('/broadcast', '').strip()
    if not msg:
        bot.reply_to(m, "❌ Please provide a message: /broadcast Hello everyone!")
        return
    try:
        c.execute("SELECT user_id FROM users")
        users = c.fetchall()
        sent = 0
        for uid in users:
            try:
                bot.send_message(uid[0], "📢 **Announcement**\n\n" + msg, parse_mode='Markdown')
                sent += 1
            except:
                pass
        bot.reply_to(m, f"✅ Broadcast sent to {sent} users!")
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🤖 Professional Number OSINT Bot Running...")
    print(f"👨‍💻 {OWNER}")
    print("🪙 1 FREE Coin/day = 1 Search!")
    print("💎 1W ₹50 | 1M ₹80")
    print("✅ Commands: /num, /vehicle, /vehiclespecial, /claim, /premium, /profile, /menu, /stats, /broadcast")
    print("✅ Press Ctrl+C to stop")
    bot.infinity_polling()