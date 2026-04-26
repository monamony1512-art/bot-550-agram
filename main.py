import os
import random, math
import json
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.error import NetworkError, TimedOut, RetryAfter
from flask import Flask
from threading import Thread

# ===== للـ Render =====
TOKEN = os.environ.get('BOT_TOKEN', "8201015539:AAHxChQD-meG7hvkNRqiaJ_jJUEGy31Zn-M")
كلمة_السر_العادية = "kmbra_H1"
كلمة_سر_الأسطورة = "Victor_DBs_2026"
يوزر_الأسطورة = "Android_hi4x"

# ===== حفظ الداتا =====
DATA_FILE = 'data.json'
المسموح_لهم = set()
الأسطورة = set()
عداد_الاكتشاف = {}

def load_data():
    global المسموح_لهم, الأسطورة, عداد_الاكتشاف
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                المسموح_لهم = set(data.get('allowed', []))
                الأسطورة = set(data.get('legends', []))
                عداد_الاكتشاف = {int(k): v for k, v in data.get('counter', {}).items()}
        except:
            pass

def save_data():
    data = {
        'allowed': list(المسموح_لهم),
        'legends': list(الأسطورة),
        'counter': عداد_الاكتشاف
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

load_data()

# ===== Flask - الحل للـ timeout =====
app = Flask('')
@app.route('/')
def home():
    return "🗿 بوت الإجرام 550 أمر شغال 24/7"

def run_flask():
    port = int(os.environ.get('PORT', 10000)) # Render بيستخدم 10000
    app.run(host='0.0.0.0', port=port)

# ===== حماية سبام =====
spam_window = {}
warning_count = {}
banned_until = {}

WINDOW_TIME = 5.0
MAX_MESSAGES = 5
BAN_TIME = 300
MAX_LINES = 3

def add_spam_check(user_id, count=1):
    now = time.time()

    if user_id in banned_until and now < banned_until[user_id]:
        باقي = int(banned_until[user_id] - now)
        دقايق = باقي // 60
        ثواني = باقي % 60
        return False, f"🗿 محظور يا نوب... فاضلك {دقايق}د {ثواني}ث 😂👑"

    if user_id not in spam_window:
        spam_window[user_id] = []

    spam_window[user_id] = [t for t in spam_window[user_id] if now - t < WINDOW_TIME]

    for _ in range(count):
        spam_window[user_id].append(now)

    if len(spam_window[user_id]) >= MAX_MESSAGES:
        warning_count[user_id] = warning_count.get(user_id, 0) + 1
        spam_window[user_id] = []

        if warning_count[user_id] >= 3:
            banned_until[user_id] = now + BAN_TIME
            warning_count[user_id] = 0
            return False, "🗿🗿 خدت بلوك 5 دقايق يا مكمبر عشان السبام 😂👑\n3 تحذيرات = بلوك"
        else:
            return False, f"😂 تحذير {warning_count[user_id]}/3 | بعت 5 رسايل في 5 ثواني 🗿"

    return True, None

# ===== Error Handler - بيمنع الكراش =====
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    if isinstance(error, TimedOut):
        print("Timeout حصل... بنكمل عادي")
        return
    elif isinstance(error, NetworkError):
        print("NetworkError... بنكمل عادي")
        return
    elif isinstance(error, RetryAfter):
        print(f"Rate limited... هنستنى {error.retry_after} ثانية")
        await asyncio.sleep(error.retry_after)
        return
    else:
        print(f"Exception: {error}")

def معاه_تصريح(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        ok, msg = add_spam_check(user_id)
        if not ok:
            await update.message.reply_text(msg)
            return

        if user_id in المسموح_لهم or user_id in الأسطورة:
            عداد_الاكتشاف[user_id] = عداد_الاكتشاف.get(user_id, 0) + 1
            نسبة = min(99.9, عداد_الاكتشاف[user_id] / 5.5)
            context.user_data['نسبة'] = نسبة
            save_data()
            return await func(update, context)
        else:
            await update.message.reply_text("🗿 مش من الكمبراوية\nاكتب: kmbra كلمة_السر")
    return wrapper

def أسطورة_بس(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username or "يا نوب"
        ok, msg = add_spam_check(user_id)
        if not ok:
            await update.message.reply_text(msg)
            return

        if user_id in الأسطورة:
            عداد_الاكتشاف[user_id] = عداد_الاكتشاف.get(user_id, 0) + 1
            نسبة = min(99.9, عداد_الاكتشاف[user_id] / 5.5)
            context.user_data['نسبة'] = نسبة
            save_data()
            return await func(update, context)
        elif user_id in المسموح_لهم:
            await update.message.reply_text(f"🗿 @{username} بتحاول تسرق أوامر @{يوزر_الأسطورة} الأسطورة؟\nاكتشفت {عداد_الاكتشاف.get(user_id, 0)} أمر بس من 550 😂\nالأوامر دي لـ Victor بس 👑")
        else:
            await update.message.reply_text("😂 أنت مين؟ اكتب: kmbra كلمة_السر الأول يا نوب 🗿")
    return wrapper

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗿 بوت الإجرام 550 أمر صحي\nاكتشفت 0% منه... مستحيل تخلصه 😂\nاكتب: kmbra كلمة_السر")

async def kmbra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("😂 اكتب كلمة السر: kmbra kmbra_H1")
        return
    if context.args[0] == كلمة_سر_الأسطورة:
        الأسطورة.add(user_id); المسموح_لهم.add(user_id)
        save_data()
        await update.message.reply_text(f"👑👑 أهلاً بالأسطورة @{يوزر_الأسطورة}...\nمعاك 500 أمر عادي + 50 سري = 550 أمر 🔥\nاكتشفت 0.18% بس 😂\nاكتب: secretcmds")
    elif context.args[0] == كلمة_السر_العادية:
        المسموح_لهم.add(user_id)
        save_data()
        await update.message.reply_text("🗿 كلمة السر صح... باب الإجرام اتفتح\nمعاك 500 أمر... اكتشفت 0.18% بس 😂\nاكتب: cmds")
    else:
        await update.message.reply_text("😂 غلط يا نوب... حاول تاني")

@معاه_تصريح
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in المسموح_لهم:
        المسموح_لهم.remove(user_id)
    if user_id in الأسطورة:
        الأسطورة.remove(user_id)
    نسبة = context.user_data.get('نسبة', 0.18)
    save_data()
    await update.message.reply_text(f"🗿 قفلت عليك... اكتشفت {نسبة:.1f}% من البوت بس 😂")

اسلحة = ["M416","AKM","SCAR-L","M762","Groza","AUG","QBZ","G36C","FAMAS","M16A4","Mk47","M249","DP-28","MG3","UZI","UMP45","Vector","Thompson","MP5K","P90","PP19","S12K","S686","S1897","DBS","M1014","Kar98k","M24","AWM","Win94","Mini14","SKS","SLR","Mk14","VSS","QBU","Crossbow","Pan","Machete","Sickle"]
سكوبات = ["ريد دوت","هولو","2x","3x","4x","6x","8x","15x"]

@معاه_تصريح
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🗿 اكتب: calc 150\nاكتشفت 0.18% من البوت")
        return
    try:
        طلقات = int(context.args[0])
        if طلقات <= 0:
            await update.message.reply_text("😂 معكش طلق أصلاً يا نوب")
            return
        دقة = random.randint(15, 35)
        هيدشوت = random.randint(5, 20)
        ضربات = math.floor(طلقات * دقة / 100)
        هيد = math.floor(ضربات * هيدشوت / 100)
        بودي = ضربات - هيد
        كيلات = math.floor(ضربات / 4) + math.floor(هيد / 2)
        نسبة_فوز = min(99, دقة + هيدشوت + random.randint(10,30))
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"🗿 حاسبة الإجرام:\nطلقاتك: {طلقات}\nنسبة دقتك: {دقة}%\nهيجي منهم: {ضربات} طلقة\nمنهم {هيد} هيدشوت 👑 و {بودي} بودي\nكيلات متوقعة: {كيلات}\nنسبة فوزك الفايت: {نسبة_فوز}% 🔥\nاكتشفت {نسبة:.1f}% من البوت")
    except:
        await update.message.reply_text("😂 اكتب رقم يا اسطى مش حروف")

كل_الأوامر = {}
كل_الأوامر["calc"] = calc
كل_الأوامر["lock"] = lock

def create_weapon_cmd(weapon_name, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"سلاحك: {weapon_name} + {random.choice(سكوبات)} 🗿\nضرر: {random.randint(40,80)}\nمدى: {random.randint(100,800)}م\nأمر {idx}/550\nاكتشفت {نسبة:.1f}% من البوت")
    return cmd

for i, سلاح in enumerate(اسلحة[:40], 1):
    كل_الأوامر[f"gun_{i}"] = create_weapon_cmd(سلاح, i)

@معاه_تصريح
async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    نسبة = context.user_data.get('نسبة', 0.18)
    await update.message.reply_text(f"🗿 معاك 500 أمر يا Victor...\n\nأمثلة:\ngun_1 لحد gun_40\ncalc 200\nlock\n\nلسه في 457 أمر مستخبي 😂 دور عليهم\n\nاكتشفت {نسبة:.1f}% بس... مستحيل تخلصهم 😂👑\n\nعايز الأوامر السرية؟ اكتب: kmbra كلمة_سر_الأسطورة")

كل_الأوامر["cmds"] = cmds

أسماء_الأسرار = ["aimbot","norecoil","wallhack","speedhack","fly","godmode","teleport","nuke","infdmg"]
ردود_الأسرار = {
    "aimbot": "👑 ايم بوت ON... 100% هيدشوت حتى لو مغمض 🗿🔥",
    "norecoil": "👑 نو ريكويل ON... M249 بقى مسطرة 😂",
    "wallhack": "👑 شايفهم كلهم ورا الحيطة... زي الأشعة السينية 🗿",
    "speedhack": "👑 أسرع من الصوت... محدش هيلحقك 😂🔥",
    "nuke": "👑 بووووم 💥 السيرفر كله اتمسح... فاضل Victor بس 😂👑",
    "teleport": "👑 تليبورت ON... روح أي مكان في ثانية 🗿",
    "godmode": "👑 دم انفنتي ON... اضرب فيك للصبح مش هتموت 😂",
    "fly": "👑 طيران ON... بتطير فوق الماب كله 😂🔥",
    "infdmg": "👑 ضرر انفنتي... طلقة واحدة = سكواد 😂👑"
}

أوامر_سرية = {}

def create_secret_cmd(secret_name):
    @أسطورة_بس
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        رد = ردود_الأسرار.get(secret_name, f"👑 {secret_name} ON... قوة خارقة اتفعلت 🔥🗿")
        await update.message.reply_text(f"{رد}\nاكتشفت {نسبة:.1f}% من البوت السري")
    return cmd

for اسم in أسماء_الأسرار:
    أوامر_سرية[اسم] = create_secret_cmd(اسم)

@أسطورة_بس
async def secretcmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    نسبة = context.user_data.get('نسبة', 0.18)
    في_قايمة = "\n".join([f"{اسم}" for اسم in أسماء_الأسرار])
    await update.message.reply_text(f"👑 أوامر الأسطورة السرية:\n{في_قايمة}\n\nاكتشفت {نسبة:.1f}% بس يا Victor 👑")

أوامر_سرية["secretcmds"] = secretcmds

# ===== ردود الهبد =====
ردود_الهبد = [
    "🗿 ايه اللي انت كاتبه ده يا مكمبر؟ بتتعلم تكتب؟ 😂",
    "😂 انا بوت إجرام مش Google يا نوب... اكتب أمر صح",
    "🗿 ترجم يا اسطى... مش فاهمك\nاكتب: cmds عشان تشوف الأوامر",
    "👑 يا @{يوزر_الأسطورة} شوف النوب ده بيقول ايه 😂",
    "🗿 انت بتلعب ولا بتكلمني؟ اكتب أمر من 550 أمر",
    "😂 لو فضلت تهبد كده هعملك بلوك 5 دقايق 🗿",
    "🗿 الكيبورد باظ منك ولا ايه؟ اكتب: calc 100 جرب",
    "😂 ده مش شات روم يا نوب... اكتب أمر مفيد",
    "🗿 انا بوت 550 أمر مش صاحبتك... عايز ايه؟",
    "👑 الأوامر فوق 500 أمر وانت بتكتب هبد؟ 😂 اكتب cmds"
]

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    lines = [line.strip() for line in update.message.text.strip().split('\n') if line.strip()]

    if len(lines) > MAX_LINES:
        ok, msg = add_spam_check(user_id, count=len(lines))
        if not ok:
            await update.message.reply_text(msg)
            return
        await update.message.reply_text(f"🗿 يا مكمبر بعت {len(lines)} سطر مرة واحدة؟\nبنفذ أول {MAX_LINES} بس 😂")
        lines = lines[:MAX_LINES]
    else:
        ok, msg = add_spam_check(user_id, count=len(lines))
        if not ok:
            await update.message.reply_text(msg)
            return

    if not lines:
        return

    text = lines[0]
    text_lower = text.lower()

    if text_lower == "start" or text == "ابدأ":
        await start(update, context)
        return
    elif text_lower.startswith("kmbra"):
        parts = text.split()
        context.args = parts[1:] if len(parts) > 1 else []
        await kmbra(update, context)
        return
    elif text_lower == "calc" or text_lower.startswith("calc ") or text == "احسب" or text.startswith("احسب "):
        parts = text.split()
        context.args = parts[1:] if len(parts) > 1 else []
        await calc(update, context)
        return
    elif text_lower == "lock" or text == "اقفل":
        await lock(update, context)
        return
    elif text_lower == "cmds" or text == "الاوامر" or text == "اوامر":
        await cmds(update, context)
        return
    elif text_lower.startswith("gun_"):
        if text_lower in كل_الأوامر:
            await كل_الأوامر[text_lower](update, context)
            return
    elif text_lower in أوامر_سرية:
        await أوامر_سرية[text_lower](update, context)
        return

    # رد على الهبد
    رد_عشوائي = random.choice(ردود_الهبد).replace("@{يوزر_الأسطورة}", f"@{يوزر_الأسطورة}")
    await update.message.reply_text(رد_عشوائي)

# ===== التشغيل - الحل النهائي =====
def run_bot():
    app_bot = Application.builder().token(TOKEN).connect_timeout(30).read_timeout(30).build()
    app_bot.add_error_handler(error_handler)
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("kmbra", kmbra))
    for اسم, دالة in كل_الأوامر.items():
        app_bot.add_handler(CommandHandler(اسم, دالة))
    for اسم, دالة in أوامر_سرية.items():
        app_bot.add_handler(CommandHandler(اسم, دالة))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🗿 بوت الإجرام شغال 24/7 على Render...")
    app_bot.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        close_loop=False
    )

if __name__ == '__main__':
    # شغل Flask في thread منفصل
    Thread(target=run_flask, daemon=True).start()
    # شغل البوت
    run_bot()
