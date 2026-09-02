import telebot, requests, re, sqlite3, datetime, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- CONFIG ----------
BOT_TOKEN = "8654008990:AAEbFOpj658dagBy92qIcvZDQd1mxhDkI50"  # नया टोकन
ADMIN_ID = 6936978343  # आपकी Chat ID

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

# ---------- LANGUAGE DICTIONARIES (All 6 languages) ----------
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
    'bn': {
        'lang': "🌐 ভাষা নির্বাচন করুন:",
        'welcome_premium': "💎 **প্রিমিয়াম প্রয়োজন**\n📅 প্ল্যান:\n• ১ দিন – ₹১০\n• ৫ দিন – ₹৩০\n• ১ সপ্তাহ – ₹৩৫\n• ১ মাস – ₹৭০",
        'buy_premium': "💳 প্রিমিয়াম কিনুন",
        'payment_info': "💳 **UPI দিয়ে পে করুন**\nUPI: `desi.hacker@ybl`\nপ্ল্যান: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 QR স্ক্যান করুন।",
        'already_premium': "🎉 আপনি ইতিমধ্যে প্রিমিয়াম!",
        'main_menu': "📱 **মেনু**",
        'search': "🔍 অনুসন্ধান",
        'premium': "💎 প্রিমিয়াম",
        'number': "📱 নম্বর",
        'vehicle': "🚗 গাড়ি",
        'vehicle_special': "🚘 গাড়ি স্পেশাল",
        'aadhaar': "🆔 আধার",
        'claim_btn': "🪙 Coin দাবি",
        'profile_btn': "👤 প্রোফাইল",
        'help_btn': "❓ সাহায্য",
        'about_btn': "ℹ️ তথ্য",
        'clear_btn': "🗑️ মুছুন",
        'back': "🔙 ফিরে",
        'owner': "👨‍💻 মালিক",
        'group': "🔗 গ্রুপ",
        'admin_only': "⚠️ আপনার অনুমতি নেই।",
        'stats_text': "📊 পরিসংখ্যান\n👥 মোট: {total}\n✅ সক্রিয়: {access}\n💎 প্রিমিয়াম: {premium}\n🪙 Coins: {coins}\n🔍 অনুসন্ধান: {searches}",
        'enter_number': "📱 ১০ অঙ্কের নম্বর দিন:",
        'enter_vehicle': "🚗 গাড়ির নম্বর দিন:",
        'enter_vehicle_special': "🚘 স্পেশালের জন্য গাড়ি:",
        'enter_aadhaar': "🆔 ১২ অঙ্কের আধার:",
        'coins_left': "🪙 {coins} coins বাকি",
        'premium_active': "💎 প্রিমিয়াম সক্রিয়",
        'not_premium': "❌ প্রিমিয়াম নয়।",
        'follow_insta': "📸 Insta ফলো",
        'visit_website': "🌐 ওয়েবসাইট",
        'get_coin': "🪙 ১টি FREE Coin পান",
        'coin_earned': "✅ ১টি FREE Coin পেলেন!",
        'already_done': "✅ আগেই করা!",
        'follow_visit_required': "⚠️ আগে Insta ফলো ও ওয়েবসাইট দেখুন।",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 প্রোফাইল\n🪙 Coins: {coins}\n💎 প্রিমিয়াম: {prem}\n🔍 অনুসন্ধান: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ আজ দাবি করেছেন!",
        'wt': "⏳ আনছি...",
        'nc': "❌ Coin নেই! দৈনিক ১টি FREE Coin দাবি করুন।",
        'pin_success': "📌 বার্তা পিন করা হয়েছে!",
        'pin_fail': "❌ পিন করতে ব্যর্থ। আমাকে পিন অনুমতি দিন।"
    },
    'mr': {
        'lang': "🌐 भाषा निवडा:",
        'welcome_premium': "💎 **प्रीमियम आवश्यक**\n📅 प्लान:\n• १ दिवस – ₹१०\n• ५ दिवस – ₹३०\n• १ आठवडा – ₹३५\n• १ महिना – ₹७०",
        'buy_premium': "💳 प्रीमियम खरेदी",
        'payment_info': "💳 **UPI द्वारा पैसे द्या**\nUPI: `desi.hacker@ybl`\nप्लान: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 QR स्कॅन करा.",
        'already_premium': "🎉 तुम्ही आधीच प्रीमियम आहात!",
        'main_menu': "📱 **मुख्य मेनू**",
        'search': "🔍 शोध",
        'premium': "💎 प्रीमियम",
        'number': "📱 क्रमांक",
        'vehicle': "🚗 वाहन",
        'vehicle_special': "🚘 वाहन स्पेशल",
        'aadhaar': "🆔 आधार",
        'claim_btn': "🪙 Coin मागा",
        'profile_btn': "👤 प्रोफाइल",
        'help_btn': "❓ मदत",
        'about_btn': "ℹ️ माहिती",
        'clear_btn': "🗑️ साफ करा",
        'back': "🔙 मागे",
        'owner': "👨‍💻 मालक",
        'group': "🔗 ग्रुप",
        'admin_only': "⚠️ तुम्हाला अधिकार नाही.",
        'stats_text': "📊 आकडेवारी\n👥 एकूण: {total}\n✅ सक्रिय: {access}\n💎 प्रीमियम: {premium}\n🪙 Coins: {coins}\n🔍 शोध: {searches}",
        'enter_number': "📱 १० अंकी क्रमांक पाठवा:",
        'enter_vehicle': "🚗 वाहन क्रमांक पाठवा:",
        'enter_vehicle_special': "🚘 स्पेशलसाठी वाहन:",
        'enter_aadhaar': "🆔 १२ अंकी आधार:",
        'coins_left': "🪙 {coins} coins शिल्लक",
        'premium_active': "💎 प्रीमियम सक्रिय",
        'not_premium': "❌ प्रीमियम नाही.",
        'follow_insta': "📸 Insta फॉलो करा",
        'visit_website': "🌐 वेबसाइट",
        'get_coin': "🪙 १ FREE Coin मिळवा",
        'coin_earned': "✅ १ FREE Coin मिळाला!",
        'already_done': "✅ आधीच केले!",
        'follow_visit_required': "⚠️ प्रथम Insta फॉलो व वेबसाइट पहा.",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 प्रोफाइल\n🪙 Coins: {coins}\n💎 प्रीमियम: {prem}\n🔍 शोध: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ आज मागितले!",
        'wt': "⏳ आणत आहे...",
        'nc': "❌ Coin नाही! दररोज १ FREE Coin मागा.",
        'pin_success': "📌 संदेश पिन केला!",
        'pin_fail': "❌ पिन करता आला नाही. मला पिन परवानगी द्या."
    },
    'ur': {
        'lang': "🌐 زبان منتخب کریں:",
        'welcome_premium': "💎 **پریمیم ضروری**\n📅 پلان:\n• ۱ دن – ₹۱۰\n• ۵ دن – ₹۳۰\n• ۱ ہفتہ – ₹۳۵\n• ۱ مہینہ – ₹۷۰",
        'buy_premium': "💳 پریمیم خریدیں",
        'payment_info': "💳 **UPI سے ادائیگی کریں**\nUPI: `desi.hacker@ybl`\nپلان: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 QR اسکین کریں۔",
        'already_premium': "🎉 آپ پہلے سے پریمیم ہیں!",
        'main_menu': "📱 **مین مینو**",
        'search': "🔍 تلاش",
        'premium': "💎 پریمیم",
        'number': "📱 نمبر",
        'vehicle': "🚗 گاڑی",
        'vehicle_special': "🚘 گاڑی سپیشل",
        'aadhaar': "🆔 آدھار",
        'claim_btn': "🪙 Coin کا دعوی",
        'profile_btn': "👤 پروفائل",
        'help_btn': "❓ مدد",
        'about_btn': "ℹ️ معلومات",
        'clear_btn': "🗑️ صاف کریں",
        'back': "🔙 واپس",
        'owner': "👨‍💻 مالک",
        'group': "🔗 گروپ",
        'admin_only': "⚠️ آپ مجاز نہیں۔",
        'stats_text': "📊 اعداد و شمار\n👥 کل: {total}\n✅ فعال: {access}\n💎 پریمیم: {premium}\n🪙 Coins: {coins}\n🔍 تلاش: {searches}",
        'enter_number': "📱 ۱۰ ہندسی نمبر بھیجیں:",
        'enter_vehicle': "🚗 گاڑی کا نمبر بھیجیں:",
        'enter_vehicle_special': "🚘 سپیشل کے لیے گاڑی:",
        'enter_aadhaar': "🆔 ۱۲ ہندسی آدھار:",
        'coins_left': "🪙 {coins} coins باقی",
        'premium_active': "💎 پریمیم فعال",
        'not_premium': "❌ پریمیم نہیں۔",
        'follow_insta': "📸 Insta فالو کریں",
        'visit_website': "🌐 ویب سائٹ",
        'get_coin': "🪙 ۱ FREE Coin حاصل کریں",
        'coin_earned': "✅ ۱ FREE Coin ملا!",
        'already_done': "✅ پہلے ہی کیا!",
        'follow_visit_required': "⚠️ پہلے Insta فالو اور ویب سائٹ وزٹ کریں۔",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 پروفائل\n🪙 Coins: {coins}\n💎 پریمیم: {prem}\n🔍 تلاش: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ آج دعوی کر چکے!",
        'wt': "⏳ لا رہا ہوں...",
        'nc': "❌ Coin نہیں! روزانہ ۱ FREE Coin حاصل کریں۔",
        'pin_success': "📌 پیغام پن کیا!",
        'pin_fail': "❌ پن نہیں کر سکا۔ مجھے پن کی اجازت دیں۔"
    },
    'ta': {
        'lang': "🌐 மொழியைத் தேர்ந்தெடுக்கவும்:",
        'welcome_premium': "💎 **பிரீமியம் தேவை**\n📅 திட்டங்கள்:\n• 1 நாள் – ₹10\n• 5 நாட்கள் – ₹30\n• 1 வாரம் – ₹35\n• 1 மாதம் – ₹70",
        'buy_premium': "💳 பிரீமியம் வாங்க",
        'payment_info': "💳 **UPI மூலம் செலுத்து**\nUPI: `desi.hacker@ybl`\nதிட்டங்கள்: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70\n📸 QR ஸ்கேன் செய்யவும்.",
        'already_premium': "🎉 நீங்கள் ஏற்கனவே பிரீமியம்!",
        'main_menu': "📱 **முதன்மை மெனு**",
        'search': "🔍 தேடு",
        'premium': "💎 பிரீமியம்",
        'number': "📱 எண்",
        'vehicle': "🚗 வாகனம்",
        'vehicle_special': "🚘 வாகனம் ஸ்பெஷல்",
        'aadhaar': "🆔 ஆதார்",
        'claim_btn': "🪙 Coin கோருக",
        'profile_btn': "👤 சுயவிவரம்",
        'help_btn': "❓ உதவி",
        'about_btn': "ℹ️ தகவல்",
        'clear_btn': "🗑️ அழி",
        'back': "🔙 பின்",
        'owner': "👨‍💻 உரிமையாளர்",
        'group': "🔗 குழு",
        'admin_only': "⚠️ உங்களுக்கு அனுமதி இல்லை.",
        'stats_text': "📊 புள்ளிவிவரங்கள்\n👥 மொத்தம்: {total}\n✅ செயலில்: {access}\n💎 பிரீமியம்: {premium}\n🪙 Coins: {coins}\n🔍 தேடல்கள்: {searches}",
        'enter_number': "📱 10 இலக்க எண்ணை அனுப்பவும்:",
        'enter_vehicle': "🚗 வாகன எண்ணை அனுப்பவும்:",
        'enter_vehicle_special': "🚘 ஸ்பெஷலுக்கான வாகனம்:",
        'enter_aadhaar': "🆔 12 இலக்க ஆதார்:",
        'coins_left': "🪙 {coins} coins மீதம்",
        'premium_active': "💎 பிரீமியம் செயலில்",
        'not_premium': "❌ பிரீமியம் இல்லை.",
        'follow_insta': "📸 Insta பின்தொடரவும்",
        'visit_website': "🌐 இணையதளம்",
        'get_coin': "🪙 1 FREE Coin பெற",
        'coin_earned': "✅ 1 FREE Coin கிடைத்தது!",
        'already_done': "✅ ஏற்கனவே செய்துவிட்டீர்கள்!",
        'follow_visit_required': "⚠️ முதலில் Insta பின்தொடரவும் & இணையதளத்தை பார்க்கவும்.",
        'help': "📖 /start, /menu, /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /contact, /clear, /language, /pin, /special",
        'profile': "👤 சுயவிவரம்\n🪙 Coins: {coins}\n💎 பிரீமியம்: {prem}\n🔍 தேடல்கள்: {searches}",
        'about': "🤖 OSINT v3.0\n👨‍💻 @Cyber_With_Ranjan",
        'al': "✅ இன்று கோரியுள்ளீர்கள்!",
        'wt': "⏳ பெற்று வருகிறது...",
        'nc': "❌ Coin இல்லை! தினமும் 1 FREE Coin பெறவும்.",
        'pin_success': "📌 செய்தி பொருத்தப்பட்டது!",
        'pin_fail': "❌ பொருத்த முடியவில்லை. எனக்கு பொருத்த அனுமதி கொடுக்கவும்."
    }
}

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

# ---------- API FUNCTIONS ----------
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

def fetch_number_special(phone):
    try:
        url = f"{NUMBER_SPECIAL_URL}?num={phone}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

# ---------- FORMAT ----------
def format_result(data, query, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    if is_aadhaar:
        if not data:
            return "`❌ No data`"
        if isinstance(data, dict):
            if 'status' in data and data['status'] == 'success' and 'data' in data:
                info = data['data']
            else:
                info = data
        else:
            info = {}
        if not info or not info.get('name'):
            return "`❌ No records`"
        name = info.get('name', 'N/A')
        father = info.get('father') or info.get('fname', 'N/A')
        aadhar = info.get('aadhaar') or info.get('aadhar', query)
        address = info.get('address') or info.get('addr', 'N/A')
        dob = info.get('dob') or info.get('DOB', 'N/A')
        gender = info.get('gender') or info.get('sex', 'N/A')
        phone = info.get('phone') or info.get('mobile', 'N/A')
        email = info.get('email') or info.get('mail', 'N/A')
        return f"""
`🆔 AADHAAR INTEL (NEW)
━━━━━━━━━━━━━━━━━━━━━
🆔 Aadhaar: {aadhar}
👤 Name: {name}
👨 Father: {father}
📅 DOB: {dob}
⚥ Gender: {gender}
🏠 Address: {address}
📱 Phone: {phone}
📧 Email: {email}
🔐 {OWNER}`
"""
    elif is_number_special:
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
`📱 NUMBER SPECIAL INTEL
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
    elif is_special:
        if not data or not data.get('reg_no'): return "`❌ Not found`"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"""
`🚘 VEHICLE SPECIAL
━━━━━━━━━━━━━━━━━━━━━
🚘 Number: {data.get('reg_no', 'N/A')}
👤 Owner: {i.get('ownerName', 'N/A')}
🚗 Class: {i.get('vehicle_class', 'N/A')}
⛽ Fuel: {i.get('fuel_type', 'N/A')}
🔧 Engine: {i.get('engine_no', 'N/A')}
🔩 Chassis: {i.get('chassis_no', 'N/A')}
📅 Reg Date: {i.get('reg_date', 'N/A')}
📋 Status: {i.get('status', 'N/A')}
🏭 Model: {i.get('maker_model', 'N/A')}
📅 Fitness Upto: {i.get('fitness_upto', 'N/A')}
🏢 Insurance: {i.get('insurance_company', 'N/A')}
📅 Insurance Upto: {i.get('insurance_upto', 'N/A')}
🔐 {OWNER}`
"""
    elif is_vehicle:
        if not data or not data.get('regNo'): return "`❌ Not found`"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"""
`🚗 VEHICLE INTEL
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
🔐 {OWNER}`
"""
    else:
        # Number info (new API)
        if not data:
            return "`❌ No data`"
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
`📱 NUMBER INTEL (NEW)
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

def format_json(data):
    return f"`{json.dumps(data, indent=2)}`"

def send_log(uid, un, nm, query, data, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False):
    try:
        if is_aadhaar:
            if not data: return
            if isinstance(data, dict):
                if 'status' in data and data['status'] == 'success' and 'data' in data:
                    info = data['data']
                else:
                    info = data
            else:
                info = {}
            bot.send_message(ADMIN_ID, f"🆔 AADHAAR LOG (NEW)\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n👤 {info.get('name','N/A')}")
        elif is_number_special:
            if not data or data.get('status')!='success': return
            info = data.get('data', {})
            bot.send_message(ADMIN_ID, f"📱 NUMBER SPECIAL LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n📱 {info.get('name','N/A')}")
        elif is_special:
            bot.send_message(ADMIN_ID, f"🚘 SPECIAL VEHICLE LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {data.get('reg_no','N/A')}")
        elif is_vehicle:
            i = data.get('response', {})
            bot.send_message(ADMIN_ID, f"🚗 VEHICLE LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n🚘 {i.get('vehicle','N/A')}")
        else:
            if not data: return
            if isinstance(data, dict):
                if 'result' in data and isinstance(data['result'], list) and data['result']:
                    i = data['result'][0]
                elif 'data' in data and isinstance(data['data'], dict):
                    i = data['data']
                else:
                    i = data
            else:
                i = {}
            bot.send_message(ADMIN_ID, f"📊 NUMBER LOG (NEW)\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n📱 {i.get('name','N/A')}")
    except: pass

# ---------- KEYBOARDS ----------
def premium_start_menu(l):
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton(L[l]['follow_insta'], url=INSTA))
    mk.add(InlineKeyboardButton(L[l]['visit_website'], url=WEBSITE))
    mk.add(InlineKeyboardButton(L[l]['get_coin'], callback_data="get_coin"))
    mk.add(InlineKeyboardButton(L[l]['buy_premium'], callback_data="buy_premium"))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan"))
    return mk

def main_menu(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("🔍 " + L[l]['search'], callback_data="search_menu"))
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="premium"))
    mk.add(InlineKeyboardButton("🪙 " + L[l]['claim_btn'], callback_data="claim"))
    mk.add(InlineKeyboardButton("👤 " + L[l]['profile_btn'], callback_data="profile"))
    mk.add(InlineKeyboardButton("❓ " + L[l]['help_btn'], callback_data="help"))
    mk.add(InlineKeyboardButton("ℹ️ " + L[l]['about_btn'], callback_data="about"))
    mk.add(InlineKeyboardButton("📢 Channel", url=CHANNEL))
    mk.add(InlineKeyboardButton("📞 Support", url=SUPPORT_GROUP))
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
    mk.add(InlineKeyboardButton("💎 " + L[l]['premium'], callback_data="premium"))
    mk.add(InlineKeyboardButton("🪙 " + L[l]['claim_btn'], callback_data="claim"))
    mk.add(InlineKeyboardButton(L[l]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton(L[l]['owner'], url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("📢 Channel", url=CHANNEL))
    mk.add(InlineKeyboardButton("📞 Support", url=SUPPORT_GROUP))
    return mk

def result_btn(query, lang, is_vehicle=False, is_special=False, is_aadhaar=False, is_number_special=False, message_id=None, is_group=False):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"json_{query}_{is_vehicle}_{is_special}_{is_aadhaar}_{is_number_special}"))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🗑️ " + L[lang]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton("🔙 " + L[lang]['back'], callback_data="main_menu"))
    if is_group and message_id:
        mk.add(InlineKeyboardButton("📌 Pin", callback_data=f"pin_{message_id}"))
    return mk

def premium_btn(l):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("💳 ₹10 - 1D", callback_data="pay_1day"),
        InlineKeyboardButton("💳 ₹30 - 5D", callback_data="pay_5days")
    )
    mk.add(
        InlineKeyboardButton("💳 ₹35 - 1W", callback_data="pay_7days"),
        InlineKeyboardButton("💳 ₹70 - 1M", callback_data="pay_30days")
    )
    mk.add(InlineKeyboardButton("📞 Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 " + L[l]['back'], callback_data="main_menu"))
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

# ---------- HANDLERS ----------
@bot.message_handler(commands=['start'])
def st(m):
    au(m.from_user.id, m.from_user.first_name or "", m.from_user.username or "")
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lc(c):
    l = c.data.split('_')[1]; sl(c.from_user.id, l)
    if ip(c.from_user.id):
        try: bot.edit_message_text(L[l]['main_menu'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
        except: bot.send_message(c.message.chat.id, L[l]['main_menu'], reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        caption = L[l]['welcome_premium']
        try:
            with open(QR_PATH, 'rb') as qr:
                bot.send_photo(c.message.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
                bot.delete_message(c.message.chat.id, c.message.message_id)
        except:
            bot.send_message(c.message.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "✅")

@bot.callback_query_handler(func=lambda c: c.data == "get_coin")
def get_coin_cb(c):
    l = gl(c.from_user.id)
    if check_both_done(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['already_done'], True); return
    mark_insta(c.from_user.id); mark_website(c.from_user.id)
    ga(c.from_user.id)
    coin = gc(c.from_user.id)
    bot.answer_callback_query(c.id, f"🪙 +1! Total: {coin}")
    bot.send_message(c.message.chat.id, L[l]['coin_earned'] + f"\n🪙 Total: {coin}\n\n📸 Now scan QR to buy premium!", reply_markup=premium_start_menu(l))
    payment_caption = L[l]['payment_info']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=payment_caption, parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, payment_caption, parse_mode='Markdown')
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_premium"))
    bot.send_message(c.message.chat.id, "📌 After payment, send screenshot to admin.", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "buy_premium")
def buy_premium_cb(c):
    l = gl(c.from_user.id)
    bot.send_message(c.message.chat.id, "💎 **Select your plan:**", reply_markup=premium_btn(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "💳 Plans")

@bot.callback_query_handler(func=lambda c: c.data.startswith('pay_'))
def pay_cb(c):
    l = gl(c.from_user.id)
    plan = c.data.split('_')[1]
    plan_map = {'1day':(1,'₹10'), '5days':(5,'₹30'), '7days':(7,'₹35'), '30days':(30,'₹70')}
    if plan not in plan_map: bot.answer_callback_query(c.id, "❌ Invalid", True); return
    days, amount = plan_map[plan]
    bot.answer_callback_query(c.id, f"💳 {amount} selected")
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=f"💳 **Pay {amount} for {days} day(s)**\n\nUPI: `desi.hacker@ybl`\n📸 Scan QR.\nAfter payment, send screenshot to @Cyber_With_Ranjan.\n✅ Admin will activate {days} days.", parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, f"💳 **Pay {amount} for {days} day(s)**\nUPI: `desi.hacker@ybl`\nAfter payment, send screenshot to @Cyber_With_Ranjan.", parse_mode='Markdown')
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📞 Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_premium"))
    bot.send_message(c.message.chat.id, "📌 After payment, send screenshot to admin.", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "back_to_premium")
def back_premium_cb(c):
    l = gl(c.from_user.id)
    caption = L[l]['welcome_premium']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔙")

@bot.callback_query_handler(func=lambda c: c.data == "claim")
def claim_cb(c):
    l = gl(c.from_user.id)
    if not ha(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['follow_visit_required'], True); return
    if adc(c.from_user.id):
        coins = gc(c.from_user.id)
        bot.answer_callback_query(c.id, "🪙 +1! Total: "+str(coins))
        bot.send_message(c.message.chat.id, "✅ +1 Coin!\n🪙 Total: "+str(coins), reply_markup=main_menu(l))
    else:
        bot.answer_callback_query(c.id, "❌ " + L[l]['al'], True)
        bot.send_message(c.message.chat.id, L[l]['al'])

@bot.callback_query_handler(func=lambda c: c.data == "premium")
def premium_cb(c):
    l = gl(c.from_user.id)
    if ip(c.from_user.id):
        bot.answer_callback_query(c.id, "💎 Already premium!", True); return
    caption = L[l]['welcome_premium']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "💎 Premium")

@bot.callback_query_handler(func=lambda c: c.data=="profile")
def profile_cb(c):
    uid = c.from_user.id; coins=gc(uid); prem="✅" if ip(uid) else "❌"; searches=0
    try: c.execute("SELECT searches FROM users WHERE user_id=?", (uid,)); r=c.fetchone(); searches=r[0] if r else 0
    except: pass
    l = gl(uid)
    bot.answer_callback_query(c.id, "👤 Profile")
    bot.send_message(c.message.chat.id, L[l]['profile'].format(coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="help")
def help_cb(c):
    l = gl(c.from_user.id)
    bot.answer_callback_query(c.id, "❓ Help")
    bot.send_message(c.message.chat.id, L[l]['help'], reply_markup=back_btn(l), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="about")
def about_cb(c):
    l = gl(c.from_user.id)
    bot.send_message(c.message.chat.id, L[l]['about'], reply_markup=back_btn(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "ℹ️ About")

@bot.callback_query_handler(func=lambda c: c.data=="clear")
def clear_cb(c):
    try:
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.answer_callback_query(c.id, "🗑️ Cleared!")
    except:
        bot.answer_callback_query(c.id, "❌ Can't clear!", True)

@bot.callback_query_handler(func=lambda c: c.data=="main_menu")
def main_menu_cb(c):
    l = gl(c.from_user.id)
    try:
        bot.edit_message_text(L[l]['main_menu'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, L[l]['main_menu'], reply_markup=main_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔙")

@bot.callback_query_handler(func=lambda c: c.data=="search_menu")
def search_menu_cb(c):
    l = gl(c.from_user.id)
    if not ip(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ Premium required!", True); return
    try:
        bot.edit_message_text("🔍 " + L[l]['search'], c.message.chat.id, c.message.message_id, reply_markup=search_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, "🔍 " + L[l]['search'], reply_markup=search_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data in ["info", "vehicle_info", "vehicle_special_info", "aadhaar_info"])
def info_cb(c):
    l = gl(c.from_user.id)
    if not ip(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ Premium required!", True); return
    is_vehicle = c.data == "vehicle_info"
    is_special = c.data == "vehicle_special_info"
    is_aadhaar = c.data == "aadhaar_info"
    if is_aadhaar:
        bot.send_message(c.message.chat.id, L[l]['enter_aadhaar'])
    elif is_special:
        bot.send_message(c.message.chat.id, L[l]['enter_vehicle_special'])
    elif is_vehicle:
        bot.send_message(c.message.chat.id, L[l]['enter_vehicle'])
    else:
        bot.send_message(c.message.chat.id, L[l]['enter_number'])
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data.startswith('json_'))
def json_cb(c):
    parts = c.data.split('_')[1:]
    q = parts[0]
    is_vehicle = parts[1] == 'True' if len(parts)>1 else False
    is_special = parts[2] == 'True' if len(parts)>2 else False
    is_aadhaar = parts[3] == 'True' if len(parts)>3 else False
    is_number_special = parts[4] == 'True' if len(parts)>4 else False
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
    if not d:
        bot.answer_callback_query(c.id, "❌", True); return
    bot.answer_callback_query(c.id, "📊 JSON")
    bot.send_message(c.message.chat.id, format_json(d), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith('pin_'))
def pin_callback(c):
    if c.from_user.id != ADMIN_ID:
        bot.answer_callback_query(c.id, "❌ " + L[gl(c.from_user.id)]['admin_only'], True)
        return
    message_id = int(c.data.split('_')[1])
    try:
        bot.pin_chat_message(c.message.chat.id, message_id)
        bot.answer_callback_query(c.id, "📌 Pinned!", show_alert=False)
        bot.send_message(c.message.chat.id, L[gl(c.from_user.id)]['pin_success'])
    except Exception as e:
        bot.answer_callback_query(c.id, "❌ " + L[gl(c.from_user.id)]['pin_fail'], True)
        bot.send_message(c.message.chat.id, f"❌ {L[gl(c.from_user.id)]['pin_fail']}")

@bot.message_handler(commands=['pin'])
def pin_command(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, L['en']['admin_only'])
        return
    if m.reply_to_message:
        try:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.message_id)
            bot.reply_to(m, "📌 Pinned!")
        except Exception as e:
            bot.reply_to(m, "❌ Failed to pin. Make me admin with pin permission.")
    else:
        bot.reply_to(m, "❌ Reply to a message with /pin to pin it.")

# ---------- PROCESS QUERY ----------
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

# ---------- COMMANDS ----------
@bot.message_handler(commands=['num','search'])
def nc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_number']); return
    process_query(m, p[1].strip(), False, False, False)

@bot.message_handler(commands=['vehicle','v'])
def vc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle']); return
    process_query(m, p[1].strip(), True, False, False)

@bot.message_handler(commands=['vehiclespecial','vs'])
def vsc(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle_special']); return
    process_query(m, p[1].strip(), False, True, False)

@bot.message_handler(commands=['aadhaar','aadhar'])
def acmd(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, L[gl(m.from_user.id)]['enter_aadhaar']); return
    process_query(m, p[1].strip(), False, False, True)

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
    process_query(m, phone, False, False, False, True)

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

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text))
def hn(m):
    if m.chat.type in ['group','supergroup']: return
    process_query(m, m.text.strip(), False, False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', m.text.upper()))
def vhn(m):
    if m.chat.type in ['group','supergroup']: return
    process_query(m, m.text.strip().upper(), True, False, False)

@bot.message_handler(func=lambda m: re.match(r'^\d{12}$', m.text))
def ahn(m):
    if m.chat.type in ['group','supergroup']: return
    process_query(m, m.text.strip(), False, False, True)

# ---------- GROUP HANDLERS ----------
@bot.message_handler(commands=['num'], chat_types=['group','supergroup'])
def gn(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /num 9661756498"); return
    process_query(m, p[1].strip(), False, False, False)

@bot.message_handler(commands=['vehicle'], chat_types=['group','supergroup'])
def gv(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /vehicle RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), True, False, False)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group','supergroup'])
def gvs(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /vehiclespecial RJ14CV0002"); return
    process_query(m, p[1].strip().upper(), False, True, False)

@bot.message_handler(commands=['aadhaar'], chat_types=['group','supergroup'])
def gaadhaar(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /aadhaar 962397300673"); return
    process_query(m, p[1].strip(), False, False, True)

@bot.message_handler(commands=['special'], chat_types=['group','supergroup'])
def gspecial(m):
    p=m.text.split()
    if len(p)<2: bot.reply_to(m, "❌ /special 9661756498"); return
    phone = p[1].strip()
    if not re.match(r'^\d{10}$', phone):
        bot.reply_to(m, "❌ Enter a valid 10-digit number.")
        return
    process_query(m, phone, False, False, False, True)

@bot.message_handler(func=lambda m: re.match(r'^\d{10}$', m.text), chat_types=['group','supergroup'])
def ghn(m):
    process_query(m, m.text.strip(), False, False, False)

@bot.message_handler(func=lambda m: re.match(r'^[A-Z]{2}\d{2}[A-Z]{0,2}\d{4}$', m.text.upper()), chat_types=['group','supergroup'])
def gvh(m):
    process_query(m, m.text.strip().upper(), True, False, False)

@bot.message_handler(func=lambda m: re.match(r'^\d{12}$', m.text), chat_types=['group','supergroup'])
def gahn(m):
    process_query(m, m.text.strip(), False, False, True)

@bot.message_handler(commands=['start','help'], chat_types=['group','supergroup'])
def gs(m):
    l = gl(m.from_user.id)
    bot.reply_to(m, "👋 /num 9661756498 | /vehicle RJ14CV0002 | /vehiclespecial RJ14CV0002 | /aadhaar 962397300673 | /special 9661756498\n🪙 1 FREE Coin/day = 1 Search!\n💎 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70", reply_markup=group_menu(l))

@bot.message_handler(commands=['menu'])
def me(m):
    l=gl(m.from_user.id)
    if m.chat.type in ['group','supergroup']:
        bot.send_message(m.chat.id, "📱 Menu", reply_markup=group_menu(l)); return
    if not ip(m.from_user.id):
        bot.send_message(m.chat.id, L[l]['welcome_premium'], reply_markup=premium_start_menu(l), parse_mode='Markdown'); return
    bot.send_message(m.chat.id, L[l]['main_menu'], reply_markup=main_menu(l), parse_mode='Markdown')

@bot.message_handler(commands=['claim'])
def cl2(m):
    l=gl(m.from_user.id)
    if not ha(m.from_user.id):
        bot.reply_to(m, L[l]['follow_visit_required'], reply_markup=premium_start_menu(l)); return
    if adc(m.from_user.id):
        coins=gc(m.from_user.id)
        bot.reply_to(m, f"✅ +1 Coin!\n🪙 Total: {coins}")
    else:
        bot.reply_to(m, L[l]['al'])

@bot.message_handler(commands=['premium'])
def pm(m):
    l=gl(m.from_user.id)
    if ip(m.from_user.id):
        bot.reply_to(m, L[l]['already_premium']); return
    caption = L[l]['welcome_premium']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(m.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(m.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')

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
    bot.send_message(m.chat.id, L['en']['lang'], reply_markup=lang_selection())

# ---------- ADMIN COMMANDS ----------
@bot.message_handler(commands=['addpremium'])
def ap2(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, days = m.text.split()
        if ap(int(uid), int(days)):
            bot.reply_to(m, f"✅ Premium added to {uid} for {days} days!")
            bot.send_message(int(uid), f"🎉 Premium activated for {days} days!\n✅ Now unlimited access!")
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
        bot.reply_to(m, f"✅ Added {coins} coins to {uid}")
        bot.send_message(int(uid), f"🪙 +{coins} coins added!")
    except: bot.reply_to(m, "❌ /addcoins [user_id] [coins]")

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT user_id, username, access, coins, premium FROM users LIMIT 20")
        users = c.fetchall()
        if not users: bot.reply_to(m, "No users.")
        text = "📋 Users:\n"
        for u in users:
            text += f"🆔 {u[0]} | {u[1]} | {'✅' if u[2] else '❌'} | 🪙{u[3]} | {'💎' if u[4] else ''}\n"
        bot.reply_to(m, text)
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
        l = gl(m.from_user.id)
        bot.reply_to(m, L[l]['stats_text'].format(total=total, access=access, premium=premium, coins=coins, searches=searches), parse_mode='Markdown')
    except: pass

@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id != ADMIN_ID: return
    msg = m.text.replace('/broadcast', '').strip()
    if not msg: bot.reply_to(m, "❌ /broadcast [message]"); return
    try:
        c.execute("SELECT user_id FROM users")
        users = c.fetchall()
        sent = 0
        for uid in users:
            try:
                bot.send_message(uid[0], "📢 **Announcement**\n\n" + msg, parse_mode='Markdown')
                sent += 1
            except: pass
        bot.reply_to(m, f"✅ Broadcast sent to {sent} users!")
    except Exception as e:
        bot.reply_to(m, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🔥 Hacker OSINT Bot v3.0 (Debug mode) Starting...")
    print(f"👨‍💻 {OWNER}")
    print("🪙 1 FREE Coin = 1 Search!")
    print("💎 Premium Plans: 1D ₹10, 5D ₹30, 1W ₹35, 1M ₹70")
    print("📌 Admin can pin messages in groups using /pin or the Pin button.")
    print("✅ Press Ctrl+C to stop")
    bot.infinity_polling()