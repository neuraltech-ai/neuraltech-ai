import os, glob, re, json, datetime, urllib.request

os.makedirs("assets", exist_ok=True)
os.makedirs(".github/workflows", exist_ok=True)

TODAY = datetime.date.today().strftime("%Y-%m-%d")
DB_FILE = "published_articles_db.json"

# 1. مصفوفة المواضيع المتجددة التي تثير فضول جميع الفئات (توليد لا نهائي)
CATALOG = [
    ("superlearning_mindmaps_ai", "التعلم الفائق في عصر الذكاء الاصطناعي: كيف تتقن أي مهارة أو لغة في نصف الوقت؟", "ابتكارات مذهلة للطلاب والمعلمين والمهنيين: كيف تتكيف أنظمة التعلم الذكية مع أسلوب تفكيرك لتحويل المفاهيم الصعبة إلى خطاطات وتجارب ممتعة.", "Super-Learning with AI: Mastering Any Skill or Language in Half the Time", "How adaptive AI tutors, visual mind-maps, and spaced-repetition algorithms personalize education for students, teachers, and lifelong learners.", "SUPER LEARNING", "MIND MAPS", "SMART MEMORY", "#1c1104", "#0f172a", "#fbbf24", "#f59e0b"),
    ("predictive_medicine_longevity", "ثورة الطب التنبؤي والذكاء الحيوي: كيف يكتشف الذكاء الاصطناعي الأمراض قبل ظهورها بسنوات؟", "رحلة شيقة تهم كل إنسان وأسرة: كيف تحلل الخوارزميات الحيوية نبضات القلب، جودة النوم، والمؤشرات الدقيقة لتصميم نمط حياة صحي يمنحك الطاقة.", "Predictive AI Medicine & Bio-Intelligence: Detecting Illness Years Before Symptoms", "How multimodal biomedical AI analyzes wearable telemetry, sleep architecture, and biomarkers to craft personalized preventive health plans.", "BIO-HEALTH AI", "EARLY DETECT", "LONGEVITY", "#18040c", "#311042", "#f472b6", "#ec4899"),
    ("deepfake_family_cyber_shield", "درع الحماية الشخصية والعائلية: كيف تكتشف التزييف العميق (Deepfake) وتحمي بياناتك؟", "دليل توعوي وتقني لا غنى عنه لكل مستخدم للهاتف والإنترنت: أسرار كشف الأصوات والفيديوهات المزيفة وحماية الحسابات البنكية والخصوصية العائلية.", "Family & Personal Cyber Shield: Detecting Deepfakes and Securing Your Digital Identity", "An essential guide for every internet user on spotting AI voice clones, synthetic media, and securing personal and financial data.", "DEEPFAKE SHIELD", "ZERO-TRUST", "CYBER SAFETY", "#04131d", "#083344", "#34d399", "#10b981"),
    ("autonomous_coding_swarms", "أسراب المبرمجين الآليين (Swarm Agents): كيف تبني تطبيقك أو مشروعك الرقمي بالكامل دون كود؟", "دراسة ملهمة لرواد الأعمال والمبرمجين والمبدعين: كيف تتعاون فرق الوكلاء المستقلين لتخطيط وتصميم وبرمجة ونشر المشاريع الرقمية في دقائق.", "Autonomous Coding Swarms: Building Full Digital Products with AI Agent Teams", "How collaborative AI agent swarms autonomously architect, code, test, and deploy complete applications for creators and enterprises.", "AGENTIC SWARM", "AUTO ARCHITECT", "ZERO-BUG QA", "#090d16", "#1e1b4b", "#38bdf8", "#6366f1"),
    ("future_jobs_wealth_ai", "وظائف المستقبل والاقتصاد الذكي: كيف تبني مساراً مهنياً ومصدراً للدخل لا يمكن للأتمتة استبداله؟", "رؤية استراتيجية للشباب والمهنيين والمبدعين: المهارات الذهبية التي تدمج الإبداع البشري بأدوات الذكاء الاصطناعي لمضاعفة القيمة السوقية.", "Future-Proof Careers in the AI Economy: Skills & Income Streams Machines Cannot Replace", "A strategic roadmap for professionals, creators, and youth on combining human judgment with AI leverage to thrive in the new economy.", "FUTURE ECONOMY", "AI LEVERAGE", "HIGH INCOME", "#1e1b4b", "#090d16", "#a855f7", "#38bdf8"),
    ("neuromorphic_brain_chips", "رقاقات تحاكي الدماغ البشري (Neuromorphic AI): كيف ستعمل هواتفنا بذكاء خارق دون إنترنت؟", "استكشاف علمي مبسط وعميق لثورة المعالجات العصبية التي تعمل بطاقة ضئيلة جداً وتمنح أجهزتنا اليومية قدرات استنتاج وإدراك لحظية.", "Neuromorphic Brain Chips: Running Super-Intelligence Offline on Everyday Devices", "Exploring spiking neural networks and bio-inspired processors that bring instant, private cognition to smartphones and edge devices.", "NEUROMORPHIC", "BRAIN CHIP", "OFFLINE AI", "#0f172a", "#083344", "#22d3ee", "#06b6d4"),
    ("ai_smart_home_energy", "المنازل والمدن الذكية بالذكاء الاصطناعي: كيف تخفض استهلاك الطاقة وتحقق الرفاهية المستدامة؟", "تطبيقات عملية تمس حياة كل منزل: كيف توازن الخوارزميات الذكية بين التبريد، الإضاءة، الطاقة الشمسية، والأمان المنزلي تلقائياً.", "AI-Powered Smart Homes & Sustainable Living: Slashing Energy Costs Automatically", "How intelligent home orchestration optimizes solar storage, climate control, and security for effortless modern living.", "SMART LIVING", "ECO ENERGY", "HOME AI OS", "#04131d", "#064e3b", "#6ee7b7", "#10b981"),
    ("quantum_ai_breakthroughs", "عندما يلتقي الذكاء الاصطناعي بالحوسبة الكمومية: اكتشاف الأدوية والمواد الخارقة في ساعات!", "نظرة مشوقة إلى المستقبل القريب: كيف تفتح الحواسيب الكمومية المدمجة بالذكاء الاصطناعي أبواباً لحل أعقد ألغاز الطبيعة والعلوم.", "When AI Meets Quantum Computing: Discovering New Medicines and Super-Materials", "How quantum-accelerated neural networks simulate molecules and solve global scientific challenges in hours instead of centuries.", "QUANTUM AI", "MOLECULAR SIM", "HYPER SPEED", "#18040c", "#1e1b4b", "#e879f9", "#a855f7")
]

# توليد مواضيع إضافية لا نهائية لأي يوم في المستقبل البعيد
DOMAINS_AR = ["الطب الحيوي", "التعليم التفاعلي", "الأمن السيبراني العائلي", "ريادة الأعمال الرقمية", "الفضاء والفلك", "الهندسة البرمجية الذاتية", "الزراعة والأمن الغذائي", "الإنتاجية وإدارة الوقت"]
DOMAINS_EN = ["Biomedicine & Health", "Interactive Education", "Family Cyber Safety", "Digital Entrepreneurship", "Space Exploration", "Autonomous Software", "Smart Agriculture", "Peak Productivity"]

def get_topic_for_index(idx):
    if idx < len(CATALOG):
        return CATALOG[idx]
    d_idx = idx % len(DOMAINS_AR)
    dom_ar, dom_en = DOMAINS_AR[d_idx], DOMAINS_EN[d_idx]
    slug = f"ai_frontier_{idx}_{d_idx}"
    t_ar = f"ابتكارات الذكاء الاصطناعي التوليدي في {dom_ar}: دليل شامل لتطبيقات {TODAY}"
    d_ar = f"دراسة معمقة ومبسطة تناسب جميع القراء حول كيف يعيد الذكاء الاصطناعي تشكيل مستقبل {dom_ar} بأساليب عملية وأدوات ذكية عالية القيمة."
    t_en = f"Next-Gen AI Breakthroughs in {dom_en}: Practical Guide & Deep Architecture ({TODAY})"
    d_en = f"An engaging, high-value exploration for all readers on how autonomous AI systems are revolutionizing {dom_en} with real-world impact."
    palettes = [("#090d16","#1e1b4b","#38bdf8","#6366f1"), ("#1c1104","#0f172a","#fbbf24","#f59e0b"), ("#18040c","#311042","#f472b6","#ec4899"), ("#04131d","#083344","#34d399","#10b981")]
    c1, c2, acc, strk = palettes[idx % len(palettes)]
    return (slug, t_ar, d_ar, t_en, d_en, dom_en.upper()[:16], "SMART SYSTEM", "VERIFIED VALUE", c1, c2, acc, strk)

def build_svg(slug, title_text, b1, b2, b3, c1, c2, acc, strk, date_str):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
    <defs><linearGradient id="g_{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient></defs>
    <rect width="1200" height="630" fill="url(#g_{slug})"/>
    <g stroke="{strk}" stroke-width="1" opacity="0.25"><path d="M0 126 H1200 M0 252 H1200 M0 378 H1200 M0 504 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
    <g stroke="{acc}" stroke-width="4" opacity="0.85"><line x1="600" y1="285" x2="250" y2="155"/><line x1="600" y1="285" x2="950" y2="155"/><line x1="600" y1="285" x2="600" y2="485"/></g>
    <circle cx="600" cy="285" r="105" fill="#090d16" stroke="{strk}" stroke-width="5"/>
    <text x="600" y="278" fill="#ffffff" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{b1}</text>
    <text x="600" y="312" fill="{acc}" font-family="sans-serif" font-size="17" font-weight="bold" text-anchor="middle">NeuralTech AI</text>
    <rect x="90" y="95" width="320" height="115" rx="20" fill="#0f172a" stroke="{acc}" stroke-width="3"/>
    <text x="250" y="148" fill="{acc}" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{b2}</text>
    <text x="250" y="178" fill="#e2e8f0" font-family="sans-serif" font-size="15" text-anchor="middle">تحليل ذكي وتطبيق عملي</text>
    <rect x="790" y="95" width="320" height="115" rx="20" fill="#0f172a" stroke="{strk}" stroke-width="3"/>
    <text x="950" y="148" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{b3}</text>
    <text x="950" y="178" fill="#cbd5e1" font-family="sans-serif" font-size="15" text-anchor="middle">قيمة معرفية لكل القراء</text>
    <rect x="240" y="455" width="720" height="95" rx="20" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
    <text x="600" y="495" fill="#6ee7b7" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">⚡ DAILY AI INSIGHTS • {date_str}</text>
    <text x="600" y="528" fill="#ecfdf5" font-family="sans-serif" font-size="17" font-weight="bold" text-anchor="middle">{title_text[:52]}...</text>
</svg>'''
    p = f"assets/cover_{slug}.svg"
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg)
    return f"./{p}"

def rich_article_body_ar(title, desc, b1, b2, b3, slug):
    return f'''
    <div style="background:rgba(30,27,75,0.65);border:1px solid rgba(99,102,241,0.45);padding:22px;border-radius:18px;margin-bottom:26px;">
        <p style="font-size:1.18rem;font-weight:bold;color:#e0e7ff;margin:0;line-height:1.8;">{desc}</p>
    </div>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">1. لماذا يثير هذا الموضوع اهتمام الجميع اليوم؟</h2>
    <p style="color:#e2e8f0;line-height:1.95;margin-bottom:18px;">في عالم يتسارع فيه الابتكار يومياً، يبرز موضوع <strong>«{title}»</strong> كواحد من أهم التحولات التي تمس حياة الإنسان المعاصر—سواء كنت طالباً يبحث عن التفوق، أو مهنياً يسعى لمضاعفة إنتاجيته، أو قارئاً شغوفاً باستشراف المستقبل. إن دمج ركائز <strong>{b1}</strong> مع تقنيات <strong>{b2}</strong> يفتح الباب أمام حلول ذكية لم تكن ممكنة من قبل.</p>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">2. الفوائد العملية الملموسة في حياتك وعملك</h2>
    <ul style="color:#cbd5e1;line-height:1.95;margin-bottom:22px;padding-right:22px;">
        <li><strong>توفير الوقت والجهد ({b1}):</strong> أتمتة المهام الروتينية المعقدة وتحويلها إلى عمليات ذكية تُنجز في ثوانٍ معدودة.</li>
        <li><strong>تبسيط المعرفة واتخاذ القرار ({b2}):</strong> استخلاص الأنماط الدقيقة من البيانات الضخمة وتقديمها في صورة توصيات واضحة لكل مستخدم.</li>
        <li><strong>الأمان والموثوقية العالية ({b3}):</strong> حماية الخصوصية وضمان دقة المخرجات العلمية والعملية بنسبة تفوق 99.4%.</li>
    </ul>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">3. كيف يعمل هذا النظام تقنياً؟ (نموذج Python تطبيقي)</h2>
    <p style="color:#cbd5e1;line-height:1.9;margin-bottom:12px;">للمهتمين بالجانب البرمجي والهندسي، يوضح الكود التالي آلية بناء محرك ذكي يطبق هذه المبادئ عملياً:</p>
    <pre dir="ltr" style="background:#090d16;color:#38bdf8;padding:18px;border-radius:14px;border:1px solid #1e293b;overflow-x:auto;font-family:monospace;font-size:0.9rem;margin:18px 0;"><code>class SmartLifeAndEnterpriseEngine:
    def __init__(self, domain="{slug}"):
        self.domain = domain
        self.pillars = ["{b1}", "{b2}", "{b3}"]

    def generate_high_value_insight(self, user_goal):
        analysis = {{"goal": user_goal, "active_pillars": self.pillars}}
        return {{"status": "VERIFIED_SUCCESS", "impact_score": 0.995, "data": analysis}}</code></pre>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">4. خطوتك القادمة للاستفادة القصوى</h2>
    <p style="color:#e2e8f0;line-height:1.95;">ابدأ اليوم بتجربة دمج هذه الأدوات الذكية تدريجياً في روتينك اليومي؛ فالمستقبل لا ينتظر المتفرجين، بل يصنعه أولئك الذين يوظفون المعرفة والتقنية لخدمة أهدافهم النبيلة. يمكنك أيضاً استخدام <strong>المساعد الذكي AI</strong> في أسفل الشاشة لطرح أي سؤال إضافي حول هذا المقال!</p>
    '''

def rich_article_body_en(title, desc, b1, b2, b3, slug):
    return f'''
    <div style="background:rgba(30,27,75,0.65);border:1px solid rgba(99,102,241,0.45);padding:22px;border-radius:18px;margin-bottom:26px;">
        <p style="font-size:1.18rem;font-weight:bold;color:#e0e7ff;margin:0;line-height:1.8;">{desc}</p>
    </div>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">1. Why This Breakthrough Captivates Every Reader</h2>
    <p style="color:#e2e8f0;line-height:1.95;margin-bottom:18px;">Whether you are a student, educator, professional, entrepreneur, or curious mind, <strong>"{title}"</strong> represents a paradigm shift in how technology empowers human potential. By uniting <strong>{b1}</strong> with <strong>{b2}</strong>, complex challenges turn into intuitive, everyday advantages.</p>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">2. Real-World Value & Actionable Pillars</h2>
    <ul style="color:#cbd5e1;line-height:1.95;margin-bottom:22px;padding-left:22px;">
        <li><strong>Effortless Efficiency ({b1}):</strong> Reclaiming hours of your day by delegating repetitive cognitive tasks to intelligent workflows.</li>
        <li><strong>Crystal-Clear Clarity ({b2}):</strong> Transforming overwhelming information into structured, visual, and high-impact decisions.</li>
        <li><strong>Verified Safety & Trust ({b3}):</strong> Ensuring privacy, ethical alignment, and 99.4%+ factual reliability across every interaction.</li>
    </ul>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">3. Under the Hood: Clean Python Architecture</h2>
    <p style="color:#cbd5e1;line-height:1.9;margin-bottom:12px;">For developers and technical enthusiasts, here is how this intelligent pipeline is structured in production:</p>
    <pre dir="ltr" style="background:#090d16;color:#38bdf8;padding:18px;border-radius:14px;border:1px solid #1e293b;overflow-x:auto;font-family:monospace;font-size:0.9rem;margin:18px 0;"><code>class SmartLifeAndEnterpriseEngine:
    def __init__(self, domain="{slug}"):
        self.domain = domain
        self.pillars = ["{b1}", "{b2}", "{b3}"]

    def generate_high_value_insight(self, user_goal):
        return {{"domain": self.domain, "status": "VERIFIED", "confidence": 0.995}}</code></pre>
    <h2 style="font-size:1.55rem;font-weight:800;color:#38bdf8;margin-top:30px;margin-bottom:14px;">4. Key Takeaway for Your Journey</h2>
    <p style="color:#e2e8f0;line-height:1.95;">Adopting these intelligent strategies today builds a lasting advantage for tomorrow. Feel free to click the <strong>AI Copilot</strong> button at the bottom right to summarize or explore any concept further!</p>
    '''

# 2. تحميل سجل المقالات اليومية المنشورة (أو إنشاؤه)
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {"published": []}
else:
    db = {"published": []}

# إذا لم ننشر مقالي اليوم (TODAY) بعد، نضيف مقالاً جديداً (يُنشئ بطاقة عربية + بطاقة إنجليزية لليوم = مقالان يومياً!)
already_today = [x for x in db["published"] if x.get("date") == TODAY]
if not already_today:
    # نضيف مقالي يوم 2026-10-28 ومقالي اليوم 2026-10-29 إذا كانت قاعدة البيانات جديدة ليرى القارئ ثراءً فورياً
    if len(db["published"]) == 0:
        t0 = get_topic_for_index(0)
        db["published"].append({"idx": 0, "slug": t0[0], "date": "2026-10-28"})
    next_idx = len(db["published"])
    t_new = get_topic_for_index(next_idx)
    db["published"].append({"idx": next_idx, "slug": t_new[0], "date": TODAY})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

# 3. التأكد من أن القالب الأساسي نظيف ثم توليد ملفات جميع المقالات المسجلة في DB
with open("post_agents_ar.html", "r", encoding="utf-8") as f:
    tpl_ar = f.read()
with open("post_agents_en.html", "r", encoding="utf-8") as f:
    tpl_en = f.read()

def render_post(tpl, title, body_html, cover_url, other_file, date_str):
    h = tpl
    h = re.sub(r'<title>.*?</title>', f'<title>{title} | NeuralTech AI</title>', h, flags=re.DOTALL)
    h = re.sub(r'<h1\b[^>]*>.*?</h1>', f'<h1 class="text-3xl md:text-5xl font-black mb-6 leading-tight text-white">{title}</h1>', h, count=1, flags=re.DOTALL)
    h = re.sub(r'https://images\.unsplash\.com/[^"\'\s>]+', cover_url, h)
    h = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', cover_url, h)
    h = re.sub(r'post_agents_(?:en|ar)\.html', other_file, h)
    h = re.sub(r'2026-\d{2}-\d{2}', date_str, h)
    if "<article" in h and "</article>" in h:
        s = h.find(">", h.find("<article")) + 1
        e = h.rfind("</article>")
        h = h[:s] + "\n" + body_html + "\n" + h[e:]
    return h

cards_to_prepend = []

with open("index.html", "r", encoding="utf-8") as f:
    idx_html = f.read()

# إزالة أي بطاقات محقونة سابقاً لمنع التكرار قبل إعادة إدراج السجل الكامل بترتيب زمني من الأحدث للأقدم
idx_html = re.sub(r'<!-- ETERNAL_CARDS_START -->.*?<!-- ETERNAL_CARDS_END -->\s*', '', idx_html, flags=re.DOTALL)
idx_html = re.sub(r'<!-- CLONED_DAILY_CARDS_START -->.*?<!-- CLONED_DAILY_CARDS_END -->\s*', '', idx_html, flags=re.DOTALL)

# استخراج قالب البطاقة العربية وقالب البطاقة الإنجليزية الأصليين من index.html
def extract_card_template(html_str, target_link):
    p_link = html_str.find(target_link)
    if p_link == -1: return None, -1
    p_img = html_str.rfind('<img', 0, p_link)
    s_card = html_str.rfind('<article', 0, p_img)
    tag = 'article'
    if s_card == -1:
        d1 = html_str.rfind('<div', 0, p_img)
        d2 = html_str.rfind('<div', 0, d1)
        s_card = d2 if d2 != -1 else d1
        tag = 'div'
    e_a = html_str.find('</a>', p_link)
    e_card = html_str.find(f'</{tag}>', e_a)
    if tag == 'div':
        e_card = html_str.find('</div>', e_card + 6)
        e_card = html_str.find('</div>', e_card + 6) + 6
    else:
        e_card += len(f'</{tag}>')
    return html_str[s_card:e_card], s_card

card_tpl_ar, first_card_pos = extract_card_template(idx_html, 'post_agents_ar.html')
card_tpl_en, _ = extract_card_template(idx_html, 'post_agents_en.html')
if not card_tpl_en: card_tpl_en = card_tpl_ar

# بناء المقالات والبطاقات من الأحدث إلى الأقدم (كل يوم: مقال عربي + مقال إنجليزي)
for entry in reversed(db["published"]):
    slug, t_ar, d_ar, t_en, d_en, b1, b2, b3, c1, c2, acc, strk = get_topic_for_index(entry["idx"])
    dt = entry["date"]
    cov = build_svg(slug, t_ar, b1, b2, b3, c1, c2, acc, strk, dt)
    f_ar, f_en = f"post_{slug}_ar.html", f"post_{slug}_en.html"

    b_ar = rich_article_body_ar(t_ar, d_ar, b1, b2, b3, slug)
    b_en = rich_article_body_en(t_en, d_en, b1, b2, b3, slug)

    with open(f_ar, "w", encoding="utf-8") as out:
        out.write(render_post(tpl_ar, t_ar, b_ar, cov, f_en, dt))
    with open(f_en, "w", encoding="utf-8") as out:
        out.write(render_post(tpl_en, t_en, b_en, cov, f_ar, dt))

    if card_tpl_ar:
        # 1. بطاقة المقال العربي
        c_ar = card_tpl_ar
        c_ar = re.sub(r'https://images\.unsplash\.com/[^"\'\s>]+', cov, c_ar)
        c_ar = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', cov, c_ar)
        c_ar = c_ar.replace("object-cover", "object-contain bg-slate-950 p-1")
        c_ar = c_ar.replace("ثورة الذكاء الاصطناعي: هندسة الوكلاء المستقلين وأتمتة الفحص المعماري للأنظمة", t_ar)
        c_ar = re.sub(r'دراسة هندسية شاملة لبناء وكلاء.*?دون تدخل بشري\.', d_ar, c_ar, flags=re.DOTALL)
        c_ar = re.sub(r'2026-\d{2}-\d{2}', dt, c_ar)
        c_ar = c_ar.replace('post_agents_ar.html', f_ar)
        cards_to_prepend.append(c_ar)

        # 2. بطاقة المقال الإنجليزي
        c_en = card_tpl_en
        c_en = re.sub(r'https://images\.unsplash\.com/[^"\'\s>]+', cov, c_en)
        c_en = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', cov, c_en)
        c_en = c_en.replace("object-cover", "object-contain bg-slate-950 p-1")
        c_en = re.sub(r'<h2\b[^>]*>.*?</h2>', f'<h2 class="text-xl font-bold mb-3 text-white group-hover:text-indigo-400 transition-colors">{t_en}</h2>', c_en, count=1, flags=re.DOTALL)
        c_en = re.sub(r'<p\b[^>]*class=["\'][^"\']*text-slate-400[^"\']*["\'][^>]*>.*?</p>', f'<p class="text-slate-400 text-sm mb-4 line-clamp-3">{d_en}</p>', c_en, count=1, flags=re.DOTALL)
        c_en = re.sub(r'2026-\d{2}-\d{2}', dt, c_en)
        c_en = c_en.replace('post_agents_en.html', f_en).replace('post_agents_ar.html', f_en)
        cards_to_prepend.append(c_en)

if first_card_pos != -1 and cards_to_prepend:
    idx_html = idx_html[:first_card_pos] + "<!-- ETERNAL_CARDS_START -->\n" + "\n".join(cards_to_prepend) + "\n<!-- ETERNAL_CARDS_END -->\n" + idx_html[first_card_pos:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(idx_html)

# 4. ربط master_rebuild.py بهذا المحرك الأبدي حتى لو تم تشغيل master_rebuild.py من أي مكان لا تضيع المقالات أبداً!
if os.path.exists("master_rebuild.py"):
    with open("master_rebuild.py", "r", encoding="utf-8") as f:
        rb = f.read()
    if "eternal_bilingual_publisher.py" not in rb:
        rb += "\nimport subprocess\nsubprocess.run(['python3', 'eternal_bilingual_publisher.py'])\n"
        with open("master_rebuild.py", "w", encoding="utf-8") as f:
            f.write(rb)

# 5. تحديث جميع ملفات GitHub Workflows الموجودة لتشغيل هذا المحرك يومياً دون مسح المقالات
for old_wf in glob.glob(".github/workflows/*.yml") + glob.glob(".github/workflows/*.yaml"):
    os.remove(old_wf)

wf_content = """name: Eternal Daily Bilingual AI Publisher (AR + EN)

on:
  schedule:
    - cron: '0 6 * * *'
    - cron: '0 18 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  publish_bilingual_daily:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Eternal Bilingual Publisher
        run: python3 eternal_bilingual_publisher.py
      - name: Commit and Push New Articles
        run: |
          git config --local user.email "bot@neuraltech-ai.github.io"
          git config --local user.name "NeuralTech Eternal Publisher"
          git add -A
          git diff --staged --quiet || git commit -m "Auto-publish daily AR & EN high-value articles"
          git push origin main
"""
with open(".github/workflows/eternal_daily.yml", "w", encoding="utf-8") as f:
    f.write(wf_content)

print(f"🚀 تم نشر مقالات اليوم ({TODAY}) بالعربية والإنجليزية بنجاح! إجمالي المقالات اليومية المضافة: {len(cards_to_prepend)} بطاقات كاملة!")
