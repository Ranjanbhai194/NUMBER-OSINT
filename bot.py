import telebot, requests, re, sqlite3, datetime, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---------- CONFIG ----------
BOT_TOKEN = "8622116851:AAGFGCmwV6ijVGxEpLsVBW7LQbmZvqElmTk"
NUMBER_API_URL = "https://movements-invoice-amanda-victoria.trycloudflare.com/search/number"
API_KEY = "mysecretkey123"
VEHICLE_API_URL = "https://nitin-api-free-user-1k-spacial.vercel.app/api"
VEHICLE_SPECIAL_API_URL = "https://reseller-host.vercel.app/api/rc"
AADHAR_API_URL = "https://movements-invoice-amanda-victoria.trycloudflare.com/search/aadhar"
ADMIN_ID = 6936978343
OWNER = "@Cyber_With_Ranjan"
INSTA = "https://www.instagram.com/ranjan_bhai_194?igsh=ZTM2enVsNmt3MnJv"
WEBSITE = "https://cyberwithranjan.in"
GROUP = "https://t.me/cyberwithranjan"
CHANNEL = "https://t.me/cyberwithranjan"
SUPPORT_GROUP = "https://t.me/cyberwithranjan"

# QR Code image path (root folder)
QR_PATH = os.path.join(os.path.dirname(__file__), 'qr.png')

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, lang TEXT DEFAULT 'en', coins INTEGER DEFAULT 0, last_claim TEXT, access INTEGER DEFAULT 0, premium INTEGER DEFAULT 0, premium_expiry TEXT, searches INTEGER DEFAULT 0, insta_followed INTEGER DEFAULT 0, website_visited INTEGER DEFAULT 0)''')
conn.commit()

# ---------- ASCII BANNER ----------
BANNER = """
╔═══════════════════════════════════════════╗
║  ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗  ║
║  ████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗ ║
║  ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝ ║
║  ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗ ║
║  ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║ ║
║  ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ║
╠═══════════════════════════════════════════╣
║       🔥 OSINT ENGINE v3.0               ║
║       🛡️  CYBER WITH RANJAN              ║
╚═══════════════════════════════════════════╝
"""

# ---------- MULTI-LANGUAGE DICTIONARY ----------
L = {
    'en': {
        'lang': "🌐 Select Language:",
        'welcome_premium': "💎 **Premium Required**\n\nYou need a premium subscription to use this bot.\n\n📅 **Plans:**\n• 1 Week – ₹50\n• 1 Month – ₹100\n\n🎯 **Features:**\n📱 Number Info\n🆔 Aadhaar Info\n🚗 Vehicle Info (Normal & Special)\n\nClick below to buy premium.",
        'buy_premium': "💳 Buy Premium",
        'payment_info': "💳 **Pay via UPI**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **Plans:**\n• 1 Week – ₹50\n• 1 Month – ₹100\n\n📸 Scan QR code below or pay directly.\n\nAfter payment, send screenshot to @Cyber_With_Ranjan.\n\n✅ Admin will activate your premium.",
        'already_premium': "🎉 You are already a premium user!",
        'main_menu': "📱 **Main Menu**",
        'search': "🔍 Search",
        'premium': "💎 Premium",
        'account': "👤 Account",
        'info': "ℹ️ Info",
        'number': "📱 Number",
        'vehicle': "🚗 Vehicle",
        'vehicle_special': "🚘 Vehicle Special",
        'aadhaar': "🆔 Aadhaar",
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
        'coming_soon': "🚀 Coming Soon!",
        'admin_only': "⚠️ You are not authorized.",
        'broadcast_sent': "✅ Broadcast sent to all users!",
        'broadcast_fail': "❌ Failed to send broadcast.",
        'stats_text': "📊 **Bot Statistics**\n👥 Total Users: {total}\n✅ Active Users: {access}\n💎 Premium: {premium}\n🪙 Total Coins: {coins}\n🔍 Total Searches: {searches}",
        'enter_number': "📱 Send 10-digit number:",
        'enter_vehicle': "🚗 Send vehicle number (e.g., RJ14CV0002):",
        'enter_vehicle_special': "🚘 Send vehicle number for Special API:",
        'enter_aadhaar': "🆔 Send 12-digit Aadhaar number:",
        'result_ready': "✅ Result Ready!",
        'coins_left': "🪙 {coins} coins left",
        'premium_active': "💎 Premium Active",
        'not_premium': "❌ No premium access.",
        'thank_you': "🙏 Thank you for using Number OSINT Bot!",
        'follow_insta': "📸 Follow Instagram",
        'visit_website': "🌐 Visit Website",
        'get_coin': "🪙 Get 1 FREE Coin",
        'coin_earned': "✅ You earned 1 FREE Coin!",
        'already_done': "✅ You already completed this!",
        'follow_visit_required': "⚠️ First follow Instagram & visit Website to get 1 FREE Coin!",
        'help': "📖 **Commands**\n\n/start – Initialize\n/menu – Main console\n/num [number] – Phone intel\n/vehicle [number] – Vehicle intel (Normal)\n/vehiclespecial [number] – Vehicle intel (Special)\n/aadhaar [number] – Aadhaar intel\n/claim – Daily coin\n/premium – Premium plans\n/profile – Your stats\n/contact – Reach admin\n/clear – Clear chat\n/language – Change language",
        'profile': "👤 **Profile**\n🪙 Coins: {coins}\n💎 Premium: {prem}\n🔍 Searches: {searches}",
        'about': f"`🤖 **Number OSINT Bot**\n\nVersion 3.0\n👨‍💻 Developed by @Cyber_With_Ranjan\n\n🔹 Phone, Vehicle, Aadhaar intel\n🔹 Daily free coin system\n🔹 Premium plans for unlimited access\n🔹 Secure & Fast`",
        'al': "✅ Already claimed today! Come back tomorrow.",
        'wt': "⏳ Fetching intel...",
        'nc': "❌ No coins left! Claim daily 1 FREE Coin."
    },
    'hi': {
        'lang': "🌐 भाषा चुनें:",
        'welcome_premium': "💎 **प्रीमियम आवश्यक**\n\nइस बॉट का उपयोग करने के लिए प्रीमियम सब्सक्रिप्शन आवश्यक है।\n\n📅 **प्लान:**\n• 1 सप्ताह – ₹50\n• 1 महीना – ₹100\n\n🎯 **सुविधाएँ:**\n📱 नंबर जानकारी\n🆔 आधार जानकारी\n🚗 वाहन जानकारी (Normal & Special)\n\nप्रीमियम खरीदने के लिए नीचे क्लिक करें।",
        'buy_premium': "💳 प्रीमियम खरीदें",
        'payment_info': "💳 **UPI से भुगतान करें**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **प्लान:**\n• 1 सप्ताह – ₹50\n• 1 महीना – ₹100\n\n📸 नीचे QR code स्कैन करें या सीधे भुगतान करें।\n\nभुगतान के बाद @Cyber_With_Ranjan को स्क्रीनशॉट भेजें।\n\n✅ एडमिन आपका प्रीमियम सक्रिय करेगा।",
        'already_premium': "🎉 आप पहले से प्रीमियम उपयोगकर्ता हैं!",
        'main_menu': "📱 **मुख्य मेनू**",
        'search': "🔍 खोज",
        'premium': "💎 प्रीमियम",
        'account': "👤 खाता",
        'info': "ℹ️ जानकारी",
        'number': "📱 नंबर",
        'vehicle': "🚗 वाहन",
        'vehicle_special': "🚘 वाहन Special",
        'aadhaar': "🆔 आधार",
        'claim_btn': "🪙 दैनिक Coin",
        'profile_btn': "👤 प्रोफाइल",
        'help_btn': "❓ मदद",
        'about_btn': "ℹ️ जानकारी",
        'contact_btn': "📞 संपर्क",
        'support_btn': "📢 चैनल",
        'clear_btn': "🗑️ हिस्ट्री साफ",
        'back': "🔙 वापस",
        'owner': "👨‍💻 मालिक",
        'group': "🔗 ग्रुप",
        'coming_soon': "🚀 जल्द आ रहा!",
        'admin_only': "⚠️ आप अधिकृत नहीं।",
        'broadcast_sent': "✅ सभी को संदेश भेजा गया!",
        'broadcast_fail': "❌ संदेश भेजने में विफल।",
        'stats_text': "📊 **बॉट आँकड़े**\n👥 कुल: {total}\n✅ सक्रिय: {access}\n💎 प्रीमियम: {premium}\n🪙 कुल Coins: {coins}\n🔍 कुल खोज: {searches}",
        'enter_number': "📱 10 अंकों का नंबर भेजें:",
        'enter_vehicle': "🚗 वाहन नंबर भेजें (जैसे RJ14CV0002):",
        'enter_vehicle_special': "🚘 Special API के लिए वाहन नंबर:",
        'enter_aadhaar': "🆔 12 अंकों का आधार नंबर:",
        'result_ready': "✅ परिणाम तैयार!",
        'coins_left': "🪙 {coins} coins बचे",
        'premium_active': "💎 प्रीमियम सक्रिय",
        'not_premium': "❌ प्रीमियम नहीं।",
        'thank_you': "🙏 Number OSINT Bot का उपयोग करने के लिए धन्यवाद!",
        'follow_insta': "📸 इंस्टाग्राम फॉलो करें",
        'visit_website': "🌐 वेबसाइट विजिट करें",
        'get_coin': "🪙 1 FREE Coin पाएं",
        'coin_earned': "✅ आपको 1 FREE Coin मिला!",
        'already_done': "✅ आप पहले ही कर चुके हैं!",
        'follow_visit_required': "⚠️ पहले इंस्टाग्राम फॉलो करें और वेबसाइट विजिट करें!",
        'help': "📖 **कमांड्स**\n\n/start – आरंभ करें\n/menu – मुख्य मेनू\n/num [number] – फोन इंटेल\n/vehicle [number] – वाहन (Normal)\n/vehiclespecial [number] – वाहन (Special)\n/aadhaar [number] – आधार इंटेल\n/claim – दैनिक Coin\n/premium – प्रीमियम प्लान\n/profile – आपके आँकड़े\n/contact – एडमिन से संपर्क\n/clear – चैट साफ़ करें\n/language – भाषा बदलें",
        'profile': "👤 **प्रोफाइल**\n🪙 Coins: {coins}\n💎 प्रीमियम: {prem}\n🔍 खोज: {searches}",
        'about': f"`🤖 **Number OSINT Bot**\n\nVersion 3.0\n👨‍💻 विकसक: @Cyber_With_Ranjan\n\n🔹 फोन, वाहन, आधार इंटेल\n🔹 दैनिक मुफ्त Coin\n🔹 प्रीमियम – असीमित उपयोग\n🔹 सुरक्षित & तेज़`",
        'al': "✅ आज पहले ही ले लिए! कल आएं।",
        'wt': "⏳ इंटेल लाया जा रहा...",
        'nc': "❌ कोई Coin नहीं! रोजाना 1 FREE Coin लें।"
    },
    'bn': {'welcome_premium': "💎 **প্রিমিয়াম প্রয়োজন**\n\nএই বট ব্যবহার করতে প্রিমিয়াম সাবস্ক্রিপশন প্রয়োজন।\n\n📅 **প্ল্যান:**\n• ১ সপ্তাহ – ₹৫০\n• ১ মাস – ₹১০০\n\n🎯 **সুবিধা:**\n📱 নম্বর তথ্য\n🆔 আধার তথ্য\n🚗 যানবাহন তথ্য (Normal & Special)\n\nনীচে ক্লিক করে প্রিমিয়াম কিনুন।", 'buy_premium': "💳 প্রিমিয়াম কিনুন", 'payment_info': "💳 **UPI-তে পে করুন**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **প্ল্যান:**\n• ১ সপ্তাহ – ₹৫০\n• ১ মাস – ₹১০০\n\n📸 নীচে QR code স্ক্যান করুন বা সরাসরি পে করুন।\n\nপে করার পর @Cyber_With_Ranjan-কে স্ক্রিনশট পাঠান।\n\n✅ অ্যাডমিন আপনার প্রিমিয়াম সক্রিয় করবে।", 'already_premium': "🎉 আপনি ইতিমধ্যে প্রিমিয়াম ব্যবহারকারী!", 'main_menu': "📱 **মূল মেনু**", 'search': "🔍 অনুসন্ধান", 'premium': "💎 প্রিমিয়াম", 'account': "👤 অ্যাকাউন্ট", 'info': "ℹ️ তথ্য", 'number': "📱 নম্বর", 'vehicle': "🚗 যানবাহন", 'vehicle_special': "🚘 যানবাহন Special", 'aadhaar': "🆔 আধার", 'claim_btn': "🪙 দৈনিক Coin", 'profile_btn': "👤 প্রোফাইল", 'help_btn': "❓ সাহায্য", 'about_btn': "ℹ️ সম্পর্কে", 'contact_btn': "📞 যোগাযোগ", 'support_btn': "📢 চ্যানেল", 'clear_btn': "🗑️ ইতিহাস পরিষ্কার", 'back': "🔙 পিছনে", 'owner': "👨‍💻 মালিক", 'group': "🔗 গ্রুপ", 'coming_soon': "🚀 শীঘ্রই আসছে!", 'admin_only': "⚠️ আপনি অনুমোদিত নন।", 'broadcast_sent': "✅ সবাইকে বার্তা পাঠানো হয়েছে!", 'broadcast_fail': "❌ বার্তা পাঠাতে ব্যর্থ।", 'stats_text': "📊 **পরিসংখ্যান**\n👥 মোট: {total}\n✅ সক্রিয়: {access}\n💎 প্রিমিয়াম: {premium}\n🪙 মোট Coin: {coins}\n🔍 মোট অনুসন্ধান: {searches}", 'enter_number': "📱 ১০-অঙ্কের নম্বর পাঠান:", 'enter_vehicle': "🚗 যানবাহন নম্বর পাঠান (যেমন RJ14CV0002):", 'enter_vehicle_special': "🚘 Special API-র জন্য যানবাহন নম্বর:", 'enter_aadhaar': "🆔 ১২-অঙ্কের আধার নম্বর:", 'result_ready': "✅ ফলাফল প্রস্তুত!", 'coins_left': "🪙 {coins} coin বাকি", 'premium_active': "💎 প্রিমিয়াম সক্রিয়", 'not_premium': "❌ প্রিমিয়াম নেই।", 'thank_you': "🙏 Number OSINT Bot ব্যবহারের জন্য ধন্যবাদ!", 'follow_insta': "📸 ইনস্টাগ্রাম ফলো", 'visit_website': "🌐 ওয়েবসাইট ভিজিট", 'get_coin': "🪙 ১ FREE Coin নিন", 'coin_earned': "✅ আপনি ১ FREE Coin পেলেন!", 'already_done': "✅ আপনি ইতিমধ্যে করেছেন!", 'follow_visit_required': "⚠️ প্রথমে ইনস্টাগ্রাম ফলো করুন এবং ওয়েবসাইট ভিজিট করুন!", 'help': "📖 **কমান্ডসমূহ**\n\n/start – শুরু\n/menu – মেনু\n/num [number] – ফোন তথ্য\n/vehicle [number] – যানবাহন (Normal)\n/vehiclespecial [number] – যানবাহন (Special)\n/aadhaar [number] – আধার তথ্য\n/claim – দৈনিক Coin\n/premium – প্রিমিয়াম প্ল্যান\n/profile – প্রোফাইল\n/contact – অ্যাডমিনের সাথে যোগাযোগ\n/clear – চ্যাট পরিষ্কার\n/language – ভাষা পরিবর্তন", 'profile': "👤 **প্রোফাইল**\n🪙 Coins: {coins}\n💎 প্রিমিয়াম: {prem}\n🔍 অনুসন্ধান: {searches}", 'about': f"`🤖 **Number OSINT Bot**\n\nসংস্করণ 3.0\n👨‍💻 ডেভেলপার: @Cyber_With_Ranjan\n\n🔹 ফোন, যানবাহন, আধার তথ্য\n🔹 দৈনিক ফ্রি Coin\n🔹 প্রিমিয়াম – সীমাহীন ব্যবহার\n🔹 নিরাপদ & দ্রুত`", 'al': "✅ আজকে নিয়ে ফেলেছেন! আগামীকাল আসুন।", 'wt': "⏳ ইন্টেল আনা হচ্ছে...", 'nc': "❌ কোনো Coin নেই! দৈনিক ১ FREE Coin নিন।"},
    'mr': {'welcome_premium': "💎 **प्रीमियम आवश्यक**\n\nहा बॉट वापरण्यासाठी प्रीमियम सब्सक्रिप्शन आवश्यक आहे.\n\n📅 **प्लान:**\n• १ आठवडा – ₹५०\n• १ महिना – ₹१००\n\n🎯 **वैशिष्ट्ये:**\n📱 नंबर माहिती\n🆔 आधार माहिती\n🚗 वाहन माहिती (Normal & Special)\n\nप्रीमियम खरेदी करण्यासाठी खाली क्लिक करा.", 'buy_premium': "💳 प्रीमियम खरेदी", 'payment_info': "💳 **UPI द्वारे पैसे द्या**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **प्लान:**\n• १ आठवडा – ₹५०\n• १ महिना – ₹१००\n\n📸 खाली QR code स्कॅन करा किंवा थेट पैसे द्या.\n\nपैसे दिल्यानंतर @Cyber_With_Ranjan ला स्क्रीनशॉट पाठवा.\n\n✅ अ‍ॅडमिन तुमचा प्रीमियम सक्रिय करेल.", 'already_premium': "🎉 तुम्ही आधीच प्रीमियम आहात!", 'main_menu': "📱 **मुख्य मेनू**", 'search': "🔍 शोध", 'premium': "💎 प्रीमियम", 'account': "👤 खाते", 'info': "ℹ️ माहिती", 'number': "📱 नंबर", 'vehicle': "🚗 वाहन", 'vehicle_special': "🚘 वाहन Special", 'aadhaar': "🆔 आधार", 'claim_btn': "🪙 दैनिक Coin", 'profile_btn': "👤 प्रोफाइल", 'help_btn': "❓ मदत", 'about_btn': "ℹ️ माहिती", 'contact_btn': "📞 संपर्क", 'support_btn': "📢 चॅनेल", 'clear_btn': "🗑️ इतिहास साफ", 'back': "🔙 मागे", 'owner': "👨‍💻 मालक", 'group': "🔗 गट", 'coming_soon': "🚀 लवकरच!", 'admin_only': "⚠️ आपण अधिकृत नाही.", 'broadcast_sent': "✅ सर्वांना संदेश पाठवला!", 'broadcast_fail': "❌ संदेश पाठवता आला नाही.", 'stats_text': "📊 **आकडेवारी**\n👥 एकूण: {total}\n✅ सक्रिय: {access}\n💎 प्रीमियम: {premium}\n🪙 एकूण Coins: {coins}\n🔍 एकूण शोध: {searches}", 'enter_number': "📱 १०-अंकी नंबर पाठवा:", 'enter_vehicle': "🚗 वाहन नंबर पाठवा (जसे RJ14CV0002):", 'enter_vehicle_special': "🚘 Special API साठी वाहन नंबर:", 'enter_aadhaar': "🆔 १२-अंकी आधार नंबर:", 'result_ready': "✅ निकाल तयार!", 'coins_left': "🪙 {coins} coins शिल्लक", 'premium_active': "💎 प्रीमियम सक्रिय", 'not_premium': "❌ प्रीमियम नाही.", 'thank_you': "🙏 Number OSINT Bot वापरल्याबद्दल धन्यवाद!", 'follow_insta': "📸 इंस्टाग्राम फॉलो", 'visit_website': "🌐 वेबसाइट भेट", 'get_coin': "🪙 १ FREE Coin मिळवा", 'coin_earned': "✅ तुम्हाला १ FREE Coin मिळाला!", 'already_done': "✅ तुम्ही आधीच केले आहे!", 'follow_visit_required': "⚠️ प्रथम इंस्टाग्राम फॉलो करा आणि वेबसाइट भेट द्या!", 'help': "📖 **कमांड्स**\n\n/start – सुरू करा\n/menu – मुख्य मेनू\n/num [number] – फोन माहिती\n/vehicle [number] – वाहन (Normal)\n/vehiclespecial [number] – वाहन (Special)\n/aadhaar [number] – आधार माहिती\n/claim – दैनिक Coin\n/premium – प्रीमियम योजना\n/profile – प्रोफाइल\n/contact – प्रशासकाशी संपर्क\n/clear – चॅट साफ करा\n/language – भाषा बदला", 'profile': "👤 **प्रोफाइल**\n🪙 Coins: {coins}\n💎 प्रीमियम: {prem}\n🔍 शोध: {searches}", 'about': f"`🤖 **Number OSINT Bot**\n\nआवृत्ती 3.0\n👨‍💻 विकासक: @Cyber_With_Ranjan\n\n🔹 फोन, वाहन, आधार माहिती\n🔹 दैनिक मोफत Coin\n🔹 प्रीमियम – अमर्यादित वापर\n🔹 सुरक्षित & जलद`", 'al': "✅ आज आधीच घेतले! उद्या या.", 'wt': "⏳ इंटेल आणत आहे...", 'nc': "❌ Coin शिल्लक नाही! दररोज १ FREE Coin घ्या."},
    'ur': {'welcome_premium': "💎 **پریمیم درکار**\n\nاس بوٹ کو استعمال کرنے کے لیے پریمیم سبسکرپشن درکار ہے۔\n\n📅 **پلان:**\n• ۱ ہفتہ – ₹۵۰\n• ۱ مہینہ – ₹۱۰۰\n\n🎯 **خصوصیات:**\n📱 نمبر کی معلومات\n🆔 آدھار کی معلومات\n🚗 گاڑی کی معلومات (Normal & Special)\n\nپریمیم خریدنے کے لیے نیچے کلک کریں۔", 'buy_premium': "💳 پریمیم خریدیں", 'payment_info': "💳 **UPI سے ادائیگی کریں**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **پلان:**\n• ۱ ہفتہ – ₹۵۰\n• ۱ مہینہ – ₹۱۰۰\n\n📸 نیچے QR code اسکین کریں یا براہ راست ادائیگی کریں۔\n\nادائیگی کے بعد @Cyber_With_Ranjan کو اسکرین شاٹ بھیجیں۔\n\n✅ ایڈمن آپ کا پریمیم فعال کرے گا۔", 'already_premium': "🎉 آپ پہلے سے پریمیم صارف ہیں!", 'main_menu': "📱 **مین مینو**", 'search': "🔍 تلاش", 'premium': "💎 پریمیم", 'account': "👤 اکاؤنٹ", 'info': "ℹ️ معلومات", 'number': "📱 نمبر", 'vehicle': "🚗 گاڑی", 'vehicle_special': "🚘 گاڑی Special", 'aadhaar': "🆔 آدھار", 'claim_btn': "🪙 روزانہ Coin", 'profile_btn': "👤 پروفائل", 'help_btn': "❓ مدد", 'about_btn': "ℹ️ تعارف", 'contact_btn': "📞 رابطہ", 'support_btn': "📢 چینل", 'clear_btn': "🗑️ تاریخ صاف کریں", 'back': "🔙 واپس", 'owner': "👨‍💻 مالک", 'group': "🔗 گروپ", 'coming_soon': "🚀 جلد آ رہا ہے!", 'admin_only': "⚠️ آپ مجاز نہیں ہیں۔", 'broadcast_sent': "✅ تمام صارفین کو پیغام بھیج دیا!", 'broadcast_fail': "❌ پیغام بھیجنے میں ناکام۔", 'stats_text': "📊 **اعداد و شمار**\n👥 کل: {total}\n✅ فعال: {access}\n💎 پریمیم: {premium}\n🪙 کل Coins: {coins}\n🔍 کل تلاش: {searches}", 'enter_number': "📱 ۱۰ ہندسوں کا نمبر بھیجیں:", 'enter_vehicle': "🚗 گاڑی نمبر بھیجیں (جیسے RJ14CV0002):", 'enter_vehicle_special': "🚘 Special API کے لیے گاڑی نمبر:", 'enter_aadhaar': "🆔 ۱۲ ہندسوں کا آدھار نمبر:", 'result_ready': "✅ نتیجہ تیار!", 'coins_left': "🪙 {coins} coins باقی", 'premium_active': "💎 پریمیم فعال", 'not_premium': "❌ پریمیم نہیں۔", 'thank_you': "🙏 Number OSINT Bot استعمال کرنے کا شکریہ!", 'follow_insta': "📸 انسٹاگرام فالو", 'visit_website': "🌐 ویب سائٹ وزٹ", 'get_coin': "🪙 ۱ FREE Coin لیں", 'coin_earned': "✅ آپ کو ۱ FREE Coin ملا!", 'already_done': "✅ آپ پہلے ہی کر چکے ہیں!", 'follow_visit_required': "⚠️ پہلے انسٹاگرام فالو کریں اور ویب سائٹ وزٹ کریں!", 'help': "📖 **کمانڈز**\n\n/start – شروع کریں\n/menu – مین مینو\n/num [number] – فون معلومات\n/vehicle [number] – گاڑی (Normal)\n/vehiclespecial [number] – گاڑی (Special)\n/aadhaar [number] – آدھار معلومات\n/claim – روزانہ Coin\n/premium – پریمیم پلان\n/profile – پروفائل\n/contact – ایڈمن سے رابطہ\n/clear – چیٹ صاف کریں\n/language – زبان تبدیل کریں", 'profile': "👤 **پروفائل**\n🪙 Coins: {coins}\n💎 پریمیم: {prem}\n🔍 تلاش: {searches}", 'about': f"`🤖 **Number OSINT Bot**\n\nورژن 3.0\n👨‍💻 ڈویلپر: @Cyber_With_Ranjan\n\n🔹 فون، گاڑی، آدھار معلومات\n🔹 روزانہ مفت Coin\n🔹 پریمیم – لامحدود استعمال\n🔹 محفوظ & تیز`", 'al': "✅ آج پہلے ہی لے لیے! کل آئیں۔", 'wt': "⏳ انٹیل لایا جا رہا ہے...", 'nc': "❌ کوئی Coin نہیں! روزانہ ۱ FREE Coin لیں۔"},
    'ta': {'welcome_premium': "💎 **பிரீமியம் தேவை**\n\nஇந்த போட்டைப் பயன்படுத்த பிரீமியம் சந்தா தேவை.\n\n📅 **திட்டங்கள்:**\n• 1 வாரம் – ₹50\n• 1 மாதம் – ₹100\n\n🎯 **அம்சங்கள்:**\n📱 எண் தகவல்\n🆔 ஆதார் தகவல்\n🚗 வாகன தகவல் (Normal & Special)\n\nபிரீமியம் வாங்க கீழே கிளிக் செய்யவும்.", 'buy_premium': "💳 பிரீமியம் வாங்க", 'payment_info': "💳 **UPI மூலம் பணம் செலுத்த**\n\nUPI ID: `desi.hacker@ybl`\n\n📅 **திட்டங்கள்:**\n• 1 வாரம் – ₹50\n• 1 மாதம் – ₹100\n\n📸 கீழே QR code ஸ்கேன் செய்யவும் அல்லது நேரடியாக பணம் செலுத்தவும்.\n\nபணம் செலுத்திய பின் @Cyber_With_Ranjan-க்கு ஸ்கிரீன்ஷாட் அனுப்பவும்.\n\n✅ நிர்வாகி உங்கள் பிரீமியத்தை செயல்படுத்துவார்.", 'already_premium': "🎉 நீங்கள் ஏற்கனவே பிரீமியம் பயனர்!", 'main_menu': "📱 **முதன்மை மெனு**", 'search': "🔍 தேடல்", 'premium': "💎 பிரீமியம்", 'account': "👤 கணக்கு", 'info': "ℹ️ தகவல்", 'number': "📱 எண்", 'vehicle': "🚗 வாகனம்", 'vehicle_special': "🚘 வாகனம் Special", 'aadhaar': "🆔 ஆதார்", 'claim_btn': "🪙 தினசரி Coin", 'profile_btn': "👤 சுயவிவரம்", 'help_btn': "❓ உதவி", 'about_btn': "ℹ️ பற்றி", 'contact_btn': "📞 தொடர்பு", 'support_btn': "📢 சேனல்", 'clear_btn': "🗑️ வரலாற்றை அழி", 'back': "🔙 பின்", 'owner': "👨‍💻 உரிமையாளர்", 'group': "🔗 குழு", 'coming_soon': "🚀 விரைவில் வருகிறது!", 'admin_only': "⚠️ உங்களுக்கு அனுமதி இல்லை.", 'broadcast_sent': "✅ அனைவருக்கும் செய்தி அனுப்பப்பட்டது!", 'broadcast_fail': "❌ செய்தி அனுப்ப முடியவில்லை.", 'stats_text': "📊 **புள்ளிவிவரங்கள்**\n👥 மொத்தம்: {total}\n✅ செயலில்: {access}\n💎 பிரீமியம்: {premium}\n🪙 மொத்த Coins: {coins}\n🔍 மொத்த தேடல்கள்: {searches}", 'enter_number': "📱 10-இலக்க எண்ணை அனுப்பவும்:", 'enter_vehicle': "🚗 வாகன எண்ணை அனுப்பவும் (எ.கா. RJ14CV0002):", 'enter_vehicle_special': "🚘 Special API-க்கான வாகன எண்:", 'enter_aadhaar': "🆔 12-இலக்க ஆதார் எண்ணை அனுப்பவும்:", 'result_ready': "✅ முடிவு தயார்!", 'coins_left': "🪙 {coins} coins மீதம்", 'premium_active': "💎 பிரீமியம் செயலில்", 'not_premium': "❌ பிரீமியம் இல்லை.", 'thank_you': "🙏 Number OSINT Bot-ஐப் பயன்படுத்தியதற்கு நன்றி!", 'follow_insta': "📸 இன்ஸ்டாகிராம் பின்தொடர்", 'visit_website': "🌐 இணையதளம் பார்வையிடு", 'get_coin': "🪙 1 FREE Coin பெறு", 'coin_earned': "✅ நீங்கள் 1 FREE Coin பெற்றீர்கள்!", 'already_done': "✅ நீங்கள் ஏற்கனவே செய்துவிட்டீர்கள்!", 'follow_visit_required': "⚠️ முதலில் இன்ஸ்டாகிராம் பின்தொடர் & இணையதளம் பார்வையிடவும்!", 'help': "📖 **கட்டளைகள்**\n\n/start – தொடங்கவும்\n/menu – முதன்மை மெனு\n/num [number] – போன் தகவல்\n/vehicle [number] – வாகனம் (Normal)\n/vehiclespecial [number] – வாகனம் (Special)\n/aadhaar [number] – ஆதார் தகவல்\n/claim – தினசரி Coin\n/premium – பிரீமியம் திட்டம்\n/profile – சுயவிவரம்\n/contact – நிர்வாகியைத் தொடர்புகொள்ள\n/clear – அரட்டையை அழிக்கவும்\n/language – மொழியை மாற்றவும்", 'profile': "👤 **சுயவிவரம்**\n🪙 Coins: {coins}\n💎 பிரீமியம்: {prem}\n🔍 தேடல்கள்: {searches}", 'about': f"`🤖 **Number OSINT Bot**\n\nபதிப்பு 3.0\n👨‍💻 உருவாக்கியவர்: @Cyber_With_Ranjan\n\n🔹 போன், வாகனம், ஆதார் தகவல்கள்\n🔹 தினசரி இலவச Coin\n🔹 பிரீமியம் – வரம்பற்ற பயன்பாடு\n🔹 பாதுகாப்பான & வேகமான`", 'al': "✅ இன்று ஏற்கனவே பெற்றுவிட்டீர்கள்! நாளை வாருங்கள்.", 'wt': "⏳ தரவு பெறப்படுகிறது...", 'nc': "❌ Coin இல்லை! தினசரி 1 FREE Coin-ஐப் பெறுங்கள்。"}
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
        if r.status_code==200: return r.json()
        return None
    except: return None
def fetch_aadhaar(aadhaar_num):
    try:
        url = f"{AADHAR_API_URL}?aadhar={aadhaar_num}&key={API_KEY}"
        r=requests.get(url, timeout=10)
        if r.status_code==200: return r.json()
        return None
    except: return None

# ---------- FORMAT FUNCTIONS ----------
def format_result(data, query, is_vehicle=False, is_special=False, is_aadhaar=False):
    if is_aadhaar:
        if not data or data.get('status')!='success': return "`❌ No data found`"
        results = data.get('result', [])
        if not results: return "`❌ No records found`"
        info = results[0]; addr = info.get('address','N/A').replace('!',', ').strip()
        return f"""
`🆔 AADHAAR INTEL
━━━━━━━━━━━━━━━━━━━━━
🆔 Aadhaar: {info.get('aadhar', 'N/A')}
👤 Name: {info.get('name', 'N/A')}
👨 Father: {info.get('fname', 'N/A')}
📱 Number: {info.get('num', 'N/A')}
🏠 Address: {addr}
📡 Circle: {info.get('circle', 'N/A')}
📧 Email: {info.get('email', 'N/A')}
📞 Alt: {info.get('alt', 'N/A')}
📊 Total Records: {len(results)}
🔐 {OWNER}`
"""
    elif is_special:
        if not data or not data.get('reg_no'): return "`❌ Vehicle not found`"
        i = data.get('response', {}); rto = i.get('rtoData', {})
        return f"""
`🚘 VEHICLE SPECIAL INTEL
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
        if not data or not data.get('regNo'): return "`❌ Vehicle not found`"
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
        if not data or data.get('status')!='success': return "`❌ No data`"
        i=data['result'][0]; a=i.get('address','N/A').replace('!',', ')
        return f"""
`📱 NUMBER INTEL
━━━━━━━━━━━━━━━━━━━━━
📱 Number: {query}
👤 Name: {i.get('name','N/A')}
👨 Father: {i.get('fname','N/A')}
🆔 Aadhar: {i.get('aadhar','N/A')}
🏠 Address: {a}
📡 Circle: {i.get('circle','N/A')}
📧 Email: {i.get('email','N/A')}
📞 Alt: {i.get('alt','N/A')}
🔐 {OWNER}`
"""

def format_json(data):
    return f"`{json.dumps(data, indent=2)}`"

def send_log(uid, un, nm, query, data, is_vehicle=False, is_special=False, is_aadhaar=False):
    try:
        if is_aadhaar:
            if not data or data.get('status')!='success': return
            i=data['result'][0] if data.get('result') else {}
            bot.send_message(ADMIN_ID, f"🆔 AADHAAR LOG\n👤 @{un or 'N/A'} ({uid})\n🔍 {query}\n👤 {i.get('name','N/A')}")
        elif is_special:
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
def premium_start_menu(l):
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton(L[l]['follow_insta'], url=INSTA))
    mk.add(InlineKeyboardButton(L[l]['visit_website'], url=WEBSITE))
    mk.add(InlineKeyboardButton(L[l]['get_coin'], callback_data="get_coin"))
    mk.add(InlineKeyboardButton(L[l]['buy_premium'], callback_data="buy_premium"))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Cyber_With_Ranjan"))
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

def result_btn(query, lang, is_vehicle=False, is_special=False, is_aadhaar=False):
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(InlineKeyboardButton("📊 JSON", callback_data=f"json_{query}_{is_vehicle}_{is_special}_{is_aadhaar}"))
    mk.add(InlineKeyboardButton("🔗 Group", url=GROUP))
    mk.add(InlineKeyboardButton("👨‍💻 Owner", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🗑️ " + L[lang]['clear_btn'], callback_data="clear"))
    mk.add(InlineKeyboardButton("🔙 " + L[lang]['back'], callback_data="main_menu"))
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
        InlineKeyboardButton("🇧🇩 বাংলা", callback_data="lang_bn")
    )
    mk.add(
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
    l = c.data.split('_')[1]
    sl(c.from_user.id, l)
    if ip(c.from_user.id):
        try:
            bot.edit_message_text(L[l]['main_menu'], c.message.chat.id, c.message.message_id, reply_markup=main_menu(l), parse_mode='Markdown')
        except:
            bot.send_message(c.message.chat.id, L[l]['main_menu'], reply_markup=main_menu(l), parse_mode='Markdown')
    else:
        caption = L[l]['welcome_premium']
        try:
            with open(QR_PATH, 'rb') as qr:
                bot.send_photo(c.message.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
                bot.delete_message(c.message.chat.id, c.message.message_id)
        except:
            bot.send_message(c.message.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "✅")

# ---------- GET COIN + IMMEDIATE QR ----------
@bot.callback_query_handler(func=lambda c: c.data == "get_coin")
def get_coin_cb(c):
    l = gl(c.from_user.id)
    # Check if already done (both followed & visited)
    if check_both_done(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ " + L[l]['already_done'], True)
        return
    # Mark both done
    mark_insta(c.from_user.id)
    mark_website(c.from_user.id)
    # Grant access and coin
    ga(c.from_user.id)
    coin = gc(c.from_user.id)
    bot.answer_callback_query(c.id, f"🪙 +1 Coin! Total: {coin}")
    # Send coin earned message
    bot.send_message(c.message.chat.id, L[l]['coin_earned'] + f"\n🪙 Total: {coin}\n\n📸 Now scan QR to buy premium!", reply_markup=premium_start_menu(l))
    # Send QR code immediately for premium payment (with plans)
    payment_caption = L[l]['payment_info']  # includes plans now
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=payment_caption, parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, payment_caption, parse_mode='Markdown')
    # Also send contact button
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_premium"))
    bot.send_message(c.message.chat.id, "📌 After payment, send screenshot to admin.", reply_markup=mk)

# ---------- BUY PREMIUM (shows QR again) ----------
@bot.callback_query_handler(func=lambda c: c.data == "buy_premium")
def buy_premium_cb(c):
    l = gl(c.from_user.id)
    caption = L[l]['payment_info']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=caption, parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, caption, parse_mode='Markdown')
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("📞 Contact Admin", url="https://t.me/Cyber_With_Ranjan"))
    mk.add(InlineKeyboardButton("🔙 Back", callback_data="back_to_premium"))
    bot.send_message(c.message.chat.id, "📌 After payment, send screenshot to admin.", reply_markup=mk)
    bot.answer_callback_query(c.id, "💳 Payment Info")

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
        bot.answer_callback_query(c.id, "❌ " + L[l]['follow_visit_required'], True)
        return
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
        bot.answer_callback_query(c.id, "💎 You are already premium!", True)
        return
    caption = L[l]['welcome_premium']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(c.message.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "💎 Premium")

@bot.callback_query_handler(func=lambda c: c.data in ["pay_50","pay_100"])
def pay_cb(c):
    l = gl(c.from_user.id); a="₹50" if c.data=="pay_50" else "₹100"
    bot.answer_callback_query(c.id, "💳 " + a)
    bot.send_message(c.message.chat.id, f"💳 **Pay {a} on UPI:** `desi.hacker@ybl`\n📸 Send screenshot to @Cyber_With_Ranjan\n✅ Premium will be activated after verification!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data=="profile")
def profile_cb(c):
    uid = c.from_user.id
    coins = gc(uid); prem = "✅" if ip(uid) else "❌"
    searches = 0
    try:
        c.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
        r = c.fetchone(); searches = r[0] if r else 0
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
        bot.answer_callback_query(c.id, "❌ Premium required!", True)
        return
    try:
        bot.edit_message_text("🔍 " + L[l]['search'], c.message.chat.id, c.message.message_id, reply_markup=search_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(c.message.chat.id, "🔍 " + L[l]['search'], reply_markup=search_menu(l), parse_mode='Markdown')
    bot.answer_callback_query(c.id, "🔍")

@bot.callback_query_handler(func=lambda c: c.data in ["info", "vehicle_info", "vehicle_special_info", "aadhaar_info"])
def info_cb(c):
    l = gl(c.from_user.id)
    if not ip(c.from_user.id):
        bot.answer_callback_query(c.id, "❌ Premium required!", True)
        return
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
    is_vehicle = parts[1] == 'True' if len(parts) > 1 else False
    is_special = parts[2] == 'True' if len(parts) > 2 else False
    is_aadhaar = parts[3] == 'True' if len(parts) > 3 else False
    d = fetch_aadhaar(q) if is_aadhaar else (fetch_vehicle_special(q) if is_special else (fetch_vehicle(q) if is_vehicle else fetch_number(q)))
    if not d:
        bot.answer_callback_query(c.id, "❌", True); return
    bot.answer_callback_query(c.id, "📊 JSON")
    bot.send_message(c.message.chat.id, format_json(d), parse_mode='Markdown')

def process_query(m, q, is_vehicle=False, is_special=False, is_aadhaar=False):
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
    d = fetch_aadhaar(q) if is_aadhaar else (fetch_vehicle_special(q) if is_special else (fetch_vehicle(q) if is_vehicle else fetch_number(q)))
    if not d:
        try:
            bot.edit_message_text("❌ Error!", m.chat.id, msg.message_id)
        except:
            bot.send_message(m.chat.id, "❌ Error!")
        return
    send_log(m.from_user.id, m.from_user.username, m.from_user.first_name, q, d, is_vehicle, is_special, is_aadhaar)
    res = format_result(d, q, is_vehicle, is_special, is_aadhaar)
    try:
        bot.edit_message_text(f"{res}\n\n📊 JSON:\n{format_json(d)}", m.chat.id, msg.message_id, parse_mode='Markdown')
    except:
        bot.send_message(m.chat.id, f"{res}\n\n📊 JSON:\n{format_json(d)}", parse_mode='Markdown')
    coins_left = gc(m.from_user.id)
    status = f"🪙 {coins_left} coins" if not ip(m.from_user.id) else "💎 Premium"
    bot.send_message(m.chat.id, f"✅ Ready!\n{status}", reply_markup=result_btn(q, l, is_vehicle, is_special, is_aadhaar))

# ---------- COMMANDS ----------
@bot.message_handler(commands=['num','search'])
def nc(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, L[gl(m.from_user.id)]['enter_number'])
        return
    process_query(m, p[1].strip(), False, False, False)

@bot.message_handler(commands=['vehicle','v'])
def vc(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle'])
        return
    process_query(m, p[1].strip(), True, False, False)

@bot.message_handler(commands=['vehiclespecial','vs'])
def vsc(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, L[gl(m.from_user.id)]['enter_vehicle_special'])
        return
    process_query(m, p[1].strip(), False, True, False)

@bot.message_handler(commands=['aadhaar','aadhar'])
def acmd(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, L[gl(m.from_user.id)]['enter_aadhaar'])
        return
    process_query(m, p[1].strip(), False, False, True)

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
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, "❌ /num 9661756498")
        return
    process_query(m, p[1].strip(), False, False, False)

@bot.message_handler(commands=['vehicle'], chat_types=['group','supergroup'])
def gv(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, "❌ /vehicle RJ14CV0002")
        return
    process_query(m, p[1].strip().upper(), True, False, False)

@bot.message_handler(commands=['vehiclespecial'], chat_types=['group','supergroup'])
def gvs(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, "❌ /vehiclespecial RJ14CV0002")
        return
    process_query(m, p[1].strip().upper(), False, True, False)

@bot.message_handler(commands=['aadhaar'], chat_types=['group','supergroup'])
def gaadhaar(m):
    p = m.text.split()
    if len(p) < 2:
        bot.reply_to(m, "❌ /aadhaar 962397300673")
        return
    process_query(m, p[1].strip(), False, False, True)

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
    bot.reply_to(m, "👋 /num 9661756498 | /vehicle RJ14CV0002 | /vehiclespecial RJ14CV0002 | /aadhaar 962397300673\n🪙 1 FREE Coin/day = 1 Search!\n💎 1W ₹50 | 1M ₹100", reply_markup=group_menu(l))

@bot.message_handler(commands=['menu'])
def me(m):
    l = gl(m.from_user.id)
    if m.chat.type in ['group','supergroup']:
        bot.send_message(m.chat.id, "📱 Menu", reply_markup=group_menu(l))
        return
    if not ip(m.from_user.id):
        bot.send_message(m.chat.id, L[l]['welcome_premium'], reply_markup=premium_start_menu(l), parse_mode='Markdown')
        return
    bot.send_message(m.chat.id, L[l]['main_menu'], reply_markup=main_menu(l), parse_mode='Markdown')

@bot.message_handler(commands=['claim'])
def cl2(m):
    l = gl(m.from_user.id)
    if not ha(m.from_user.id):
        bot.reply_to(m, L[l]['follow_visit_required'], reply_markup=premium_start_menu(l))
        return
    if adc(m.from_user.id):
        coins = gc(m.from_user.id)
        bot.reply_to(m, f"✅ +1 Coin!\n🪙 Total: {coins}")
    else:
        bot.reply_to(m, L[l]['al'])

@bot.message_handler(commands=['premium'])
def pm(m):
    l = gl(m.from_user.id)
    if ip(m.from_user.id):
        bot.reply_to(m, L[l]['already_premium'])
        return
    caption = L[l]['welcome_premium']
    try:
        with open(QR_PATH, 'rb') as qr:
            bot.send_photo(m.chat.id, qr, caption=caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')
    except:
        bot.send_message(m.chat.id, caption, reply_markup=premium_start_menu(l), parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
def pr2(m):
    uid = m.from_user.id
    coins = gc(uid); prem = "✅" if ip(uid) else "❌"
    searches = 0
    try:
        c.execute("SELECT searches FROM users WHERE user_id=?", (uid,))
        r = c.fetchone(); searches = r[0] if r else 0
    except: pass
    l = gl(uid)
    bot.reply_to(m, L[l]['profile'].format(coins=coins, prem=prem, searches=searches), parse_mode='Markdown')

@bot.message_handler(commands=['contact'])
def ct(m):
    bot.reply_to(m, f"📞 {OWNER}\n🔗 {GROUP}")
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
    l = gl(m.from_user.id)
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
            bot.send_message(int(uid), f"🎉 Premium activated for {days} days!\n✅ Now you have unlimited access!")
    except:
        bot.reply_to(m, "❌ /addpremium [user_id] [days]")

@bot.message_handler(commands=['removepremium'])
def rp(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid = m.text.split()
        c.execute("UPDATE users SET premium=0, premium_expiry=NULL WHERE user_id=?", (int(uid),))
        conn.commit()
        bot.reply_to(m, f"✅ Removed premium from {uid}")
    except:
        bot.reply_to(m, "❌ /removepremium [user_id]")

@bot.message_handler(commands=['addcoins'])
def ac(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, coins = m.text.split()
        c.execute("UPDATE users SET coins=coins+? WHERE user_id=?", (int(coins), int(uid)))
        conn.commit()
        bot.reply_to(m, f"✅ +{coins} coins to {uid}")
    except:
        bot.reply_to(m, "❌ /addcoins [user_id] [coins]")

@bot.message_handler(commands=['users'])
def us(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        c.execute("SELECT user_id, username, access, coins, premium FROM users LIMIT 20")
        users = c.fetchall()
        if not users:
            bot.reply_to(m, "No users.")
            return
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
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, L['en']['admin_only'])
        return
    msg = m.text.replace('/broadcast', '').strip()
    if not msg:
        bot.reply_to(m, "❌ /broadcast [message]")
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
    print("🔥 Hacker OSINT Bot v3.0 Starting...")
    print(f"👨‍💻 {OWNER}")
    print("🪙 1 FREE Coin = 1 Search!")
    print("💎 1W ₹50 | 1M ₹100")
    print("✅ Commands: /num, /vehicle, /vehiclespecial, /aadhaar, /claim, /premium, /profile, /menu, /stats, /broadcast")
    print("✅ Press Ctrl+C to stop")
    bot.infinity_polling()