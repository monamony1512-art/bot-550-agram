import os
import random, math
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
كلمة_السر_العادية = "كمبرة_H1"
كلمة_سر_الأسطورة = "Victor_DBs_فوشك_2026_👑"

المسموح_لهم = set()
الأسطورة = set()
عداد_الاكتشاف = {}

# سيرفر وهمي
app = Flask('')
@app.route('/')
def home(): return "🗿 بوت الإجرام 550 أمر شغال"
def run(): app.run(host='0.0.0.0',port=8080)
def keep_alive(): Thread(target=run).start()

# ========== الحماية + عداد ==========
def معاه_تصريح(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id in المسموح_لهم or user_id in الأسطورة:
            عداد_الاكتشاف[user_id] = عداد_الاكتشاف.get(user_id, 0) + 1
            نسبة = min(99.9, عداد_الاكتشاف[user_id] / 5.5)
            context.user_data['نسبة'] = نسبة
            return await func(update, context)
        else:
            await update.message.reply_text("🗿 مش من الكمبراوية\n/كمبر كلمة_السر")
    return wrapper

def أسطورة_بس(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        username = update.effective_user.username or "يا نوب"
        if user_id in الأسطورة:
            عداد_الاكتشاف[user_id] = عداد_الاكتشاف.get(user_id, 0) + 1
            نسبة = min(99.9, عداد_الاكتشاف[user_id] / 5.5)
            context.user_data['نسبة'] = نسبة
            return await func(update, context)
        elif user_id in المسموح_لهم:
            await update.message.reply_text(f"🗿 @{username} بتحاول تسرق أوامر الأسطورة؟\nاكتشفت {عداد_الاكتشاف.get(user_id, 0)} أمر بس من 550 😂\nالأوامر دي لـ Victor بس 👑")
        else:
            await update.message.reply_text("😂 أنت مين؟ روح /كمبر كلمة_السر الأول يا نوب 🗿")
    return wrapper

# ========== الدخول ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗿 بوت الإجرام 550 أمر صحي\nاكتشفت 0% منه... مستحيل تخلصه 😂\nاكتب: /كمبر كلمة_السر")

async def كمبر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("😂 اكتب كلمة السر: /كمبر كمبرة_H1")
        return
    if context.args[0] == كلمة_سر_الأسطورة:
        الأسطورة.add(user_id); المسموح_لهم.add(user_id)
        await update.message.reply_text("👑👑 أهلاً بالأسطورة Victor...\nمعاك 500 أمر عادي + 50 سري = 550 أمر 🔥\nاكتشفت 0.18% بس 😂\n/أوامر_الأسطورة")
    elif context.args[0] == كلمة_السر_العادية:
        المسموح_لهم.add(user_id)
        await update.message.reply_text("🗿 كلمة السر صح... باب الإجرام اتفتح\nمعاك 500 أمر... اكتشفت 0.18% بس 😂\n/اوامر")
    else:
        await update.message.reply_text("😂 غلط يا نوب... حاول تاني")

@معاه_تصريح
async def قفل(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in المسموح_لهم: المسموح_لهم.remove(user_id)
    if user_id in الأسطورة: الأسطورة.remove(user_id)
    نسبة = context.user_data.get('نسبة', 0.18)
    await update.message.reply_text(f"🗿 قفلت عليك... اكتشفت {نسبة:.1f}% من البوت بس 😂")

# ========== داتا ==========
اسلحة = ["M416","AKM","SCAR-L","M762","Groza","AUG","QBZ","G36C","FAMAS","M16A4","Mk47","M249","DP-28","MG3","UZI","UMP45","Vector","Thompson","MP5K","P90","PP19","S12K","S686","S1897","DBS","M1014","Kar98k","M24","AWM","Win94","Mini14","SKS","SLR","Mk14","VSS","QBU","Crossbow","Pan","Machete","Sickle"]
سكوبات = ["ريد دوت","هولو","2x","3x","4x","6x","8x","15x"]
دروبات = ["Pochinki","Military Base","School","Rozhok","Yasnaya","Georgopol","Mylta Power","Novorepnoye","Sosnovka","Primorsk","Severny","Lipovka","Stalber","Zharki","Hospital","Mansion","Prison","Shelter","Farm","Ruins","Cave","Quarry","Crater Field","Water Town","Bootcamp","Paradise Resort","Tambang","Kampong","Ha Tinh","Train Station","Ruins","Cave","Quarry","Mylta","Novorepnoye"]
عربيات = ["UAZ مفتوح","UAZ مقفل","داسيا","بجي","بيك أب","شاحنة","تروسيكل","موتوسيكل","باجي","زحافة","جيت سكي","قارب","توك توك","دباب","ميرادو","كوبيه","لادا","لونا بارك","هامر","دبابة"]
خطط = ["كمبر طرف الزون","راش بيت واحد","سبليت بوش","كمبر برج","فايت مفتوح","بوش بعربيات","سموك وهيل","نيد ورش","كمبر بريدج","اقطع الزون","هولد هاي جراوند","لو روتيت","بيت كامب","تريد كيلات","فول سكواد بوش"]
نصايح = ["متضربش غير وانت متأكد","الهيدشوت يكسب","الكمبرة حياة","الصوت أهم من الشوف","ثالث الزون أفضل مكان","متخليش ضهرك مكشوف","سموك قبل اللوت","نيد قبل البوش","ريفايف في كفر","متجريش في المفتوح","اعمل Peek صح","خلي معاك سموكين","المقلاة بتصد","اشرب انرجي قبل الفايت","متكمبرش في النص","رابع الزون أخطر مكان","الهاي جراوند يكسب","متخشش بيت مقفول بابه","عد الطلق قبل الرش","غير مكانك بعد كل كيل"]

# ========== حاسبة الطلق الأساسية ==========
@معاه_تصريح
async def حاسبة_الطلق(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🗿 اكتب: /حاسبة_الطلق 150\nاكتشفت 0.18% من البوت")
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

# ========== مولد الـ 500 أمر ==========
كل_الأوامر = {}
كل_الأوامر["حاسبة_الطلق"] = حاسبة_الطلق
كل_الأوامر["قفل"] = قفل

# 1. أوامر الأسلحة 40
def create_weapon_cmd(weapon_name, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"سلاحك: {weapon_name} + {random.choice(سكوبات)} 🗿\nضرر: {random.randint(40,80)}\nمدى: {random.randint(100,800)}م\nأمر {idx}/550\nاكتشفت {نسبة:.1f}% من البوت")
    return cmd

for i, سلاح in enumerate(اسلحة[:40], 1):
    كل_الأوامر[f"سلاح_{i}"] = create_weapon_cmd(سلاح, i)

# 2. أوامر الدروب 35
def create_drop_cmd(drop_name, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        لوت = random.choice(["غني 🔥","فقير 😂","متوسط","مولع 🔥","آمن 🗿"])
        await update.message.reply_text(f"انزل: {drop_name} 🗿\nحالة اللوت: {لوت}\nنسبة الخطر: {random.randint(1,100)}%\nنسبة اللاعبين: {random.randint(1,20)}/100\nأمر {40+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i, دروب in enumerate(دروبات[:35], 1):
    كل_الأوامر[f"دروب_{i}"] = create_drop_cmd(دروب, i)

# 3. أوامر العربيات 20
def create_car_cmd(car_name, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"اركب: {car_name} 🗿\nسرعة: {random.randint(80,130)} كم\nبنزين: {random.randint(20,100)}%\nدروع: {random.randint(0,100)}%\nأمر {75+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i, عربية in enumerate(عربيات[:20], 1):
    كل_الأوامر[f"عربية_{i}"] = create_car_cmd(عربية, i)

# 4. أوامر الخطط 15
def create_plan_cmd(plan_name, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"الخطة: {plan_name} 🗿\nنسبة النجاح: {random.randint(50,95)}%\nصعوبة: {random.choice(['سهلة','متوسطة','صعبة','انتحارية 😂'])}\nأمر {95+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i, خطة in enumerate(خطط[:15], 1):
    كل_الأوامر[f"خطة_{i}"] = create_plan_cmd(خطة, i)

# 5. أوامر النصايح 20
def create_tip_cmd(tip_text, idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"👑 نصيحة Ace H1 رقم {idx}:\n{tip_text}\n\nمستوى الأهمية: {random.randint(1,10)}/10\nأمر {110+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i, نصيحة in enumerate(نصايح[:20], 1):
    كل_الأوامر[f"نصيحة_{i}"] = create_tip_cmd(نصيحة, i)

# 6. حاسبات 49 زيادة
def create_calc_cmd(idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        base = random.randint(50,500) * idx
        نتيجة = base * random.uniform(0.5, 1.5)
        نسبة = context.user_data.get('نسبة', 0.18)
        await update.message.reply_text(f"🗿 حاسبة {idx}:\nالرقم الأساسي: {base}\nالنتيجة: {نتيجة:.0f}\nنسبة الدقة: {random.randint(60,99)}%\nمعامل الخطورة: {random.uniform(0.1,2):.2f}\nأمر {130+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i in range(1,50):
    كل_الأوامر[f"حاسبة_{i}"] = create_calc_cmd(i)

# 7. معلومات 100
معلومات_ببجي = [
    "الـ AWM بتشيل خوذة لفل 3 بطلقة واحدة 🗿","المقلاة بتصد رصاصة AWM 😂","الزون بتقفل كل 2-5 دقايق",
    "أسرع عربية هي الداسيا","الـ M249 فيه 100 طلقة","الريدزون قطرها 200 متر تقريباً",
    "تقدر تشيل 2 سلاح أساسي بس","الهيلث الكامل 100","البوست بيوصل 100","الـ DBS أقوى شوتجن",
    "الـ VSS فيه سكوب 4x ثابت","المولوتوف بيحرق 10 ثواني","السموك بيفضل 40 ثانية","الستن بتعمي 5 ثواني",
    "الفلير بيجيب دروب مخصوص","الـ 8x مش بيركب على كل الأسلحة","الـ Crossbow صامت تماماً","الـ UZI أسرع معدل اطلاق"
]
def create_info_cmd(idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        معلومة = معلومات_ببجي[idx % len(معلومات_ببجي)]
        await update.message.reply_text(f"{معلومة}\n\nمعلومة رقم {idx}/500 🗿\nمستوى الندرة: {random.randint(1,5)}/5\nأمر {179+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i in range(1,101):
    كل_الأوامر[f"معلومة_{i}"] = create_info_cmd(i)

# 8. تحديات 50
تحديات_قايمة = ["فوز جيم بمسدس بس 😂","جيب 10 كيل بـ Crossbow","كمبر الجيم كله واكسب","العب بدون هيل","فوز جيم بسيارة بس","جيب 5 كيل بالمقلاة","العب بدون سكوب","فوز وانت لابس لفل 1 بس","جيب 15 كيل","العب بدون درع","فوز بدون ما تلوت","جيب Win بضرر أقل من 500","العب منظور أول بس","فوز بيد واحدة 😂"]
def create_challenge_cmd(idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        تحدي = تحديات_قايمة[idx % len(تحديات_قايمة)]
        await update.message.reply_text(f"👑 تحدي {idx}:\n{تحدي}\n\nمكافأة: {random.randint(100,5000)} نقطة إجرام\nصعوبة: {random.randint(1,10)}/10\nأمر {279+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i in range(1,51):
    كل_الأوامر[f"تحدي_{i}"] = create_challenge_cmd(i)

# 9. رانك 50
رانكات_قايمة = ["برونز V","برونز IV","برونز III","برونز II","برونز I","سيلفر V","سيلفر IV","سيلفر III","سيلفر II","سيلفر I","جولد V","جولد IV","جولد III","جولد II","جولد I","بلاتينيوم V","بلاتينيوم IV","بلاتينيوم III","بلاتينيوم II","بلاتينيوم I","دايموند V","دايموند IV","دايموند III","دايموند II","دايموند I","كراون V","كراون IV","كراون III","كراون II","كراون I","Ace","Ace Master","Ace Dominator","Conqueror"]
def create_rank_cmd(idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        رانك = رانكات_قايمة[idx % len(رانكات_قايمة)]
        await update.message.reply_text(f"🗿 رانك {idx}:\nالرانك: {رانك}\nK/D: {random.uniform(0.5,20):.2f}\nماتشات: {random.randint(10,10000)}\nتوب10: {random.randint(5,95)}%\nضرر/جيم: {random.randint(100,2000)}\nأمر {329+idx}/550\nاكتشفت {نسبة:.1f}%")
    return cmd

for i in range(1,51):
    كل_الأوامر[f"رانك_{i}"] = create_rank_cmd(i)

# 10. أوامر عشوائية 121
ردود_عشوائية = ["Victor عمك 👑","الكمبرة حياة 🗿","رش ومتفكرش 🔥","الهيدشوت مفتاح الفوز","اقفل الباب وراك 😂","سموك قبل اللوت","الصوت أهم من الشوف","ثالث الزون = جيم مضمون","الهاي جراوند يكسب","عد الطلق قبل الرش","غير مكانك بعد كل كيل","المقلاة بتصد كل حاجة","الفيرست ايد = 75% هيل","الانرجي درينك = 40 بوست","الباندج = 10% هيل","المدكيت = 100% هيل","الـ AWM ون شوت ون كيل","الـ M416 ملك الثبات"]
def create_random_cmd(idx):
    @معاه_تصريح
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        رد = ردود_عشوائية[idx % len(ردود_عشوائية)]
        await update.message.reply_text(f"{رد}\n\nأمر رقم {idx}/500\nقوة الإجرام: {random.randint(1,100)}%\nأمر {379+idx}/550\nاكتشفت {نسبة:.1f}%... لسه بدري 😂")
    return cmd

for i in range(1,122):
    كل_الأوامر[f"أمر_{i}"] = create_random_cmd(i)

# أمر عرض كل الأوامر
@معاه_تصريح
async def اوامر(update: Update, context: ContextTypes.DEFAULT_TYPE):
    نسبة = context.user_data.get('نسبة', 0.18)
    await update.message.reply_text(f"🗿 معاك 500 أمر يا Victor...\n\nأمثلة:\n/سلاح_1 لحد /سلاح_40\n/دروب_1 لحد /دروب_35\n/عربية_1 لحد /عربية_20\n/خطة_1 لحد /خطة_15\n/نصيحة_1 لحد /نصيحة_20\n/حاسبة_الطلق 200\n/حاسبة_1 لحد /حاسبة_49\n/معلومة_1 لحد /معلومة_100\n/تحدي_1 لحد /تحدي_50\n/رانك_1 لحد /رانك_50\n/أمر_1 لحد /أمر_121\n\nاكتشفت {نسبة:.1f}% بس... مستحيل تخلصهم 😂👑\n\nعايز الأوامر السرية؟ /كمبر كلمة_سر_الأسطورة")

كل_الأوامر["اوامر"] = اوامر

# ========== 50 أمر سري 👑 ==========
أسماء_الأسرار = ["ايم_بوت","نو_ريكويل","وول_هاك","سبيد_هاك","سكوب_حراري","كشف_اماكن","طيران","اختفاء","تليبورت","دم_انفنتي","رصاص_انفنتي","ريفايف_فوري","درع_انفنتي","دروب_ليك_بس","لوت_خرافي","طيارة_خاصة","عربية_مدرعة","دبابة","هليكوبتر","قنبلة_نووية","ليزر","تجميد_زمن","قلب_زون","نسبة_فوز_100","باند_سيرفر","طرد_كل_النوبات","اضافة_كمبراوي","ترقية_لفل_100","سكن_ذهبي","ايموجي_تاج","صوت_فيكتور","منع_الريبورت","فلوس_انفنتي","شدات_انفنتي","فتح_كل_السكنات","قتل_بضربة","جدار_حماية","رادار_كامل","سموك_شفاف","مقلاة_ذهبية","بوت_يغني","بوت_يرقص","بوت_يبعت_ميمز","بوت_يسب_النوبات","تحكم_في_الزون","تحكم_في_الطقس","تحكم_في_الوقت","نسخ_نفسك","استدعاء_تيم","قفل_السيرفر"]

ردود_الأسرار = {
    "ايم_بوت": "👑 ايم بوت ON... 100% هيدشوت حتى لو مغمض 🗿🔥",
    "نو_ريكويل": "👑 نو ريكويل ON... M249 بقى مسطرة 😂",
    "وول_هاك": "👑 شايفهم كلهم ورا الحيطة... زي الأشعة السينية 🗿",
    "سبيد_هاك": "👑 أسرع من الصوت... محدش هيلحقك 😂🔥",
    "قنبلة_نووية": "👑 بووووم 💥 السيرفر كله اتمسح... فاضل Victor بس 😂👑",
    "تليبورت": "👑 تليبورت ON... روح أي مكان في ثانية 🗿",
    "نسخ_نفسك": "👑 بقى فيه 4 Victor في الماب... السكواد كله أنت 😂👑",
    "دم_انفنتي": "👑 دم انفنتي ON... اضرب فيك للصبح مش هتموت 😂",
    "رصاص_انفنتي": "👑 رصاص انفنتي... رش براحتك يا ملك 🔥",
    "طيران": "👑 طيران ON... بتطير فوق الماب كله 😂🔥",
    "اختفاء": "👑 اختفاء ON... محدش شايفك بس أنت شايفهم 🗿",
    "نسبة_فوز_100": "👑 نسبة فوزك: 100%... الجيم خلصان قبل ما يبدأ 😂👑",
    "باند_سيرفر": "👑 تم تبنيد كل السيرفر... فاضل Victor بس 🗿😂",
    "قفل_السيرفر": "👑 قفلت السيرفر... محدش هيعرف يلعب غيرك 😂👑"
}

أوامر_سرية = {}
def create_secret_cmd(secret_name):
    @أسطورة_بس
    async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        نسبة = context.user_data.get('نسبة', 0.18)
        رد = ردود_الأسرار.get(secret_name, f"👑 {secret_name} ON... قوة خارقة اتفعلت 🔥🗿")
        await update.message.reply_text(f"{رد}\nأمر سري {أسماء_الأسرار.index(secret_name)+1}/50\nاكتشفت {نسبة:.1f}% من البوت السري")
    return cmd

for اسم in أسماء_الأسرار:
    أوامر_سرية[اسم] = create_secret_cmd(اسم)

# أوامر خاصة بالأسطورة
@أسطورة_بس
async def طرد_نوب(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = context.args[0] if context.args else "@نوب"
    نسبة = context.user_data.get('نسبة', 0.18)
    await update.message.reply_text(f"👑 تم طرد {user}... مش من مستوانا 😂\nاكتشفت {نسبة:.1f}%")

@أسطورة_بس
async def اضافة_كمبراوي(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = context.args[0] if context.args else "@جديد"
    نسبة = context.user_data.get('نسبة', 0.18)
    await update.message.reply_text(f"👑 تم إضافة {user} للكمبراوية... أهلاً 🗿\nاكتشفت {نسبة:.1f}%")

@أسطورة_بس
async def أوامر_الأسطورة(update: Update, context: ContextTypes.DEFAULT_TYPE):
    نسبة = context.user_data.get('نسبة', 0.18)
    قايمة = "\n".join([f"/{اسم}" for اسم in أسماء_الأسرار[:25]])
    await update.message.reply_text(f"👑 أوامر الأسطورة 50 أمر سري:\n{قايمة}\n...و25 كمان 😂\n\nاكتشفت {نسبة:.1f}% بس يا Victor 👑")

أوامر_سرية["طرد_نوب"] = طرد_نوب
أوامر_سرية["اضافة_كمبراوي"] = اضافة_كمبراوي
أوامر_سرية["أوامر_الأسطورة"] = أوامر_الأسطورة

# ========== التشغيل ==========
def main():
    app_bot = Application.builder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("كمبر", كمبر))

    # نضيف الـ 500 أمر عادي
    for اسم, دالة in كل_الأوامر.items():
        app_bot.add_handler(CommandHandler(اسم, دالة))

    # نضيف الـ 50 أمر سري
    for اسم, دالة in أوامر_سرية.items():
        app_bot.add_handler(CommandHandler(اسم, دالة))

    keep_alive()
    print("🗿 بوت الإجرام 550 أمر شغال... محدش هيخلصه")
    app_bot.run_polling()

if __name__ == '__main__':
    main()
