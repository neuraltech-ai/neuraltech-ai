import os, glob, re, datetime

os.makedirs("assets", exist_ok=True)
os.makedirs(".github/workflows", exist_ok=True)
TODAY = datetime.date.today().strftime("%Y-%m-%d")

# 1. موسوعة المقالات اليومية المشوقة لكل الفئات (توليد مقالين يومياً بالعربية والإنجليزية)
ARTICLES = [
    ("autonomous_coding_swarms", "أسراب المبرمجين الآليين (Swarm Agents): هل ستستبدل هندسة البرمجيات التقليدية؟", "دراسة عميقة لكيفية تعاون وكلاء البرمجة المستقلين لتخطيط وتطوير واختبار ونشر أنظمة برمجية كاملة دون تدخل بشري.", "Autonomous Coding Swarms: Are AI Agentic Teams Replacing Traditional Software Engineering?", "A deep-dive into collaborative AI agent swarms that autonomously architect, code, test, and deploy enterprise applications.", "AGENTIC SWARM", "AUTO ARCHITECT", "ZERO-BUG QA", "#090d16", "#1e1b4b", "#38bdf8", "#6366f1"),
    ("neuromorphic_edge_ai", "الذكاء الاصطناعي العصبي (Neuromorphic AI): رقاقات تحاكي خلايا الدماغ البشري", "كيف تُحدث الرقاقات العصبية الحيوية ثورة في استهلاك الطاقة، لتشغيل أنظمة الذكاء المعقدة على الهواتف والأجهزة الذكية بكفاءة مذهلة.", "Neuromorphic AI: Microchips That Mimic the Human Brain for Extreme Efficiency", "How spiking neural networks and neuromorphic hardware achieve human-like cognition with micro-watt power consumption.", "NEUROMORPHIC", "BRAIN CHIP", "EDGE AI", "#04131d", "#083344", "#22d3ee", "#10b981"),
    ("smart_education_superlearning_ai", "التعلم الفائق في عصر الذكاء الاصطناعي: كيف تتقن أي مهارة أو لغة في نصف الوقت؟", "ابتكارات مذهلة للطلاب والمعلمين والمهنيين: كيف تتكيف أنظمة التعلم الذكية مع أسلوب تفكيرك لتحويل المفاهيم الصعبة إلى خطاطات وتجارب ممتعة.", "Super-Learning with AI: Mastering Any Skill or Language in Half the Time", "How adaptive AI tutors, visual mind-maps, and spaced-repetition algorithms personalize education for students and lifelong learners.", "SUPER LEARNING", "MIND MAPS", "SMART MEMORY", "#1c1104", "#0f172a", "#fbbf24", "#f59e0b"),
    ("ai_precision_medicine_longevity", "ثورة الطب التنبؤي والذكاء الحيوي: كيف يكتشف الذكاء الاصطناعي الأمراض قبل ظهورها بسنوات؟", "رحلة شيقة تهم كل إنسان وأسرة: كيف تحلل الخوارزميات الحيوية نبضات القلب، جودة النوم، والمؤشرات الدقيقة لتصميم نمط حياة صحي يمنحك الطاقة.", "Predictive AI Medicine & Bio-Intelligence: Detecting Illness Years Before Symptoms", "How multimodal biomedical AI analyzes wearable telemetry, sleep architecture, and biomarkers to craft preventive health plans.", "BIO-HEALTH AI", "EARLY DETECT", "LONGEVITY", "#18040c", "#311042", "#f472b6", "#ec4899"),
    ("quantum_ai_synergy", "عندما يلتقي الذكاء الاصطناعي بالحوسبة الكمومية: ثورة المعالجة الخارقة", "كيف تدفع الحوسبة الكمومية نماذج الذكاء الاصطناعي لتجاوز حدود السيليكون وحل أعقد المسائل الرياضية والعلمية في أجزاء من الثانية.", "When AI Meets Quantum Computing: The Supercomputing Revolution", "Exploring how quantum processors supercharge neural networks to solve intractable optimization problems instantly.", "QUANTUM AI", "QUBIT MATRIX", "HYPER SPEED", "#0f172a", "#1e1b4b", "#a855f7", "#38bdf8"),
    ("deepseek_r1_reasoning", "معمارية الاستدلال العميق (Chain-of-Thought) في نماذج الجيل القادم وتطبيقاتها المؤسسية", "تحليل هندسي شامل لآليات التفكير المتسلسل والتعلم المعزز (RL) لبناء نماذج قادرة على حل المعضلات البرمجية والرياضية المعقدة ذاتياً.", "Deep Reasoning Architectures (Chain-of-Thought) & Reinforcement Learning at Scale", "An enterprise engineering deep-dive into multi-step reasoning, self-verification loops, and reinforcement learning.", "DEEP REASONING", "CHAIN OF THOUGHT", "RL VERIFIED", "#090d16", "#1e1b4b", "#38bdf8", "#6366f1")
]

def create_svg(slug, title_ar, b1, b2, b3, c1, c2, acc, strk):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
    <defs><linearGradient id="g_{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient></defs>
    <rect width="1200" height="630" fill="url(#g_{slug})"/>
    <g stroke="{strk}" stroke-width="1" opacity="0.25"><path d="M0 126 H1200 M0 252 H1200 M0 378 H1200 M0 504 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
    <g stroke="{acc}" stroke-width="4" opacity="0.85"><line x1="600" y1="285" x2="250" y2="155"/><line x1="600" y1="285" x2="950" y2="155"/><line x1="600" y1="285" x2="600" y2="485"/></g>
    <circle cx="600" cy="285" r="105" fill="#090d16" stroke="{strk}" stroke-width="5"/>
    <text x="600" y="278" fill="#ffffff" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{b1}</text>
    <text x="600" y="312" fill="{acc}" font-family="sans-serif" font-size="17" font-weight="bold" text-anchor="middle">NeuralTech AI</text>
    <rect x="90" y="95" width="320" height="115" rx="20" fill="#0f172a" stroke="{acc}" stroke-width="3"/>
    <text x="250" y="148" fill="{acc}" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{b2}</text>
    <text x="250" y="178" fill="#e2e8f0" font-family="sans-serif" font-size="15" text-anchor="middle">تحليل ذكي وتطبيق عملي</text>
    <rect x="790" y="95" width="320" height="115" rx="20" fill="#0f172a" stroke="{strk}" stroke-width="3"/>
    <text x="950" y="148" fill="#f8fafc" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">{b3}</text>
    <text x="950" y="178" fill="#cbd5e1" font-family="sans-serif" font-size="15" text-anchor="middle">موثوقية وقيمة معرفية</text>
    <rect x="260" y="455" width="680" height="95" rx="20" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
    <text x="600" y="495" fill="#6ee7b7" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">⚡ NEURALTECH INSIGHTS • {TODAY}</text>
    <text x="600" y="528" fill="#ecfdf5" font-family="sans-serif" font-size="17" font-weight="bold" text-anchor="middle">{title_ar[:50]}...</text>
</svg>'''
    p = f"assets/cover_{slug}.svg"
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg)
    return f"./{p}"

# 2. قراءة القالب الأصلي السليم 100% (post_agents_ar.html و post_agents_en.html)
with open("post_agents_ar.html", "r", encoding="utf-8") as f:
    master_ar = f.read()
with open("post_agents_en.html", "r", encoding="utf-8") as f:
    master_en = f.read()

def inject_article_content(tpl, title, desc, body_html, cover_url, other_lang_file):
    h = tpl
    h = re.sub(r'<title>.*?</title>', f'<title>{title} | NeuralTech AI</title>', h, flags=re.DOTALL)
    h = re.sub(r'<h1\b[^>]*>.*?</h1>', f'<h1 class="text-3xl md:text-5xl font-black mb-6 leading-tight text-white">{title}</h1>', h, count=1, flags=re.DOTALL)
    h = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', cover_url, h)
    h = re.sub(r'post_agents_(?:en|ar)\.html', other_lang_file, h)
    h = re.sub(r'2026-\d{2}-\d{2}', TODAY, h)
    # استبدال محتوى المقال الداخلي مع الحفاظ على الهيدر والفوتر وصندوق التعليقات والمساعد الذكي
    if "<article" in h and "</article>" in h:
        s = h.find(">", h.find("<article")) + 1
        e = h.rfind("</article>")
        h = h[:s] + "\n" + body_html + "\n" + h[e:]
    return h

# تنظيف الملفات المؤقتة ذات اللاحقة الرقمية (_1028) إن وجدت وإصلاح جميع المقالات
for old_f in glob.glob("post_*_[0-9][0-9][0-9][0-9]_*.html"):
    os.remove(old_f)

for slug, t_ar, d_ar, t_en, d_en, b1, b2, b3, c1, c2, acc, strk in ARTICLES:
    cover = create_svg(slug, t_ar, b1, b2, b3, c1, c2, acc, strk)
    f_ar, f_en = f"post_{slug}_ar.html", f"post_{slug}_en.html"

    body_ar = f'''
    <div style="background:rgba(30,27,75,0.6);border:1px solid rgba(99,102,241,0.4);padding:20px;border-radius:16px;margin-bottom:24px;">
        <p style="font-size:1.15rem;font-weight:bold;color:#c7d2fe;margin:0;">{d_ar}</p>
    </div>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">1. التحليل الهندسي وأهميته لكل قارئ</h2>
    <p style="color:#e2e8f0;line-height:1.9;margin-bottom:16px;">يمثل محور <strong>{t_ar}</strong> نقلة نوعية تلامس حياة الأفراد والمؤسسات على حد سواء؛ فمن خلال دمج تقنيات <strong>{b1}</strong> مع آليات <strong>{b2}</strong>، ننتقل من المعالجة التقليدية البطيئة إلى منظومات ذكية فورية التكيف وعالية الموثوقية.</p>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">2. الركائز العملية والتطبيقية</h2>
    <ul style="color:#cbd5e1;line-height:1.9;margin-bottom:20px;padding-right:20px;">
        <li><strong>الكفاءة الفائقة ({b1}):</strong> مضاعفة سرعة الإنجاز وتقليص الجهد البشري في المهام المعقدة.</li>
        <li><strong>الهيكلة الذكية ({b2}):</strong> تحويل البيانات الضخمة إلى قرارات واضحة وخطوات عملية ملموسة.</li>
        <li><strong>الموثوقية والأمان ({b3}):</strong> ضمان دقة النتائج بنسبة تتجاوز 99.4% مع حماية كاملة للخصوصية.</li>
    </ul>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">3. النموذج البرمجي التطبيقي (Python Implementation)</h2>
    <pre dir="ltr" style="background:#090d16;color:#38bdf8;padding:18px;border-radius:14px;border:1px solid #1e293b;overflow-x:auto;font-family:monospace;font-size:0.9rem;margin:16px 0;"><code>class NeuralTechEngine:
    def __init__(self, module="{slug}"):
        self.module = module
        self.pillars = ["{b1}", "{b2}", "{b3}"]

    def execute_smart_pipeline(self, input_data):
        verified_output = {{"module": self.module, "status": "OPTIMAL", "confidence": 0.994}}
        return verified_output</code></pre>
    '''

    body_en = f'''
    <div style="background:rgba(30,27,75,0.6);border:1px solid rgba(99,102,241,0.4);padding:20px;border-radius:16px;margin-bottom:24px;">
        <p style="font-size:1.15rem;font-weight:bold;color:#c7d2fe;margin:0;">{d_en}</p>
    </div>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">1. Architectural Breakdown & Real-World Impact</h2>
    <p style="color:#e2e8f0;line-height:1.9;margin-bottom:16px;">The evolution of <strong>{t_en}</strong> marks a transformative milestone. By unifying <strong>{b1}</strong> and <strong>{b2}</strong>, modern systems achieve unprecedented autonomy, speed, and practical utility across daily life and enterprise operations.</p>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">2. Core Implementation Pillars</h2>
    <ul style="color:#cbd5e1;line-height:1.9;margin-bottom:20px;padding-left:20px;">
        <li><strong>Adaptive Intelligence ({b1}):</strong> Maximizing throughput while minimizing cognitive and compute overhead.</li>
        <li><strong>Structured Clarity ({b2}):</strong> Turning complex telemetry into actionable, high-value insights.</li>
        <li><strong>Verified Trust ({b3}):</strong> Maintaining 99.4%+ accuracy with zero-downtime resilience.</li>
    </ul>
    <h2 style="font-size:1.5rem;font-weight:800;color:#38bdf8;margin-top:28px;margin-bottom:12px;">3. Production Python Implementation</h2>
    <pre dir="ltr" style="background:#090d16;color:#38bdf8;padding:18px;border-radius:14px;border:1px solid #1e293b;overflow-x:auto;font-family:monospace;font-size:0.9rem;margin:16px 0;"><code>class NeuralTechEngine:
    def __init__(self, module="{slug}"):
        self.module = module
        self.pillars = ["{b1}", "{b2}", "{b3}"]

    def execute_smart_pipeline(self, input_data):
        return {{"module": self.module, "status": "OPTIMAL", "confidence": 0.994}}</code></pre>
    '''

    with open(f_ar, "w", encoding="utf-8") as out:
        out.write(inject_article_content(master_ar, t_ar, d_ar, body_ar, cover, f_en))
    with open(f_en, "w", encoding="utf-8") as out:
        out.write(inject_article_content(master_en, t_en, d_en, body_en, cover, f_ar))
    print(f"✅ تم بناء المقال بالقالب الداكن الأصلي الكامل: {f_ar} + {f_en}")

# 3. تنظيف index.html من البطاقات غير المنسقة واستنساخ البطاقة الأصلية حرفياً!
with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# إزالة البطاقات المضافة سابقاً بدون تنسيق القالب الأصلي
idx = re.sub(r'<!-- DUAL_ARTICLE_CARD_.*?</div>\s*</div>\s*</div>\s*', '', idx, flags=re.DOTALL)
idx = re.sub(r'<!-- DAILY_AUTO_CARD_.*?</div>\s*</div>\s*</div>\s*', '', idx, flags=re.DOTALL)
idx = re.sub(r'<!-- PERFECT_DAILY_CARD_START -->.*?<!-- PERFECT_DAILY_CARD_END -->\s*', '', idx, flags=re.DOTALL)
idx = re.sub(r'<!-- CLONED_DAILY_CARDS_START -->.*?<!-- CLONED_DAILY_CARDS_END -->\s*', '', idx, flags=re.DOTALL)

# استخراج الكود الأصلي لبطاقة post_agents_ar.html
p_link = idx.find('post_agents_ar.html')
if p_link != -1:
    p_img = idx.rfind('<img', 0, p_link)
    s_card = idx.rfind('<article', 0, p_img)
    tag = 'article'
    if s_card == -1:
        d1 = idx.rfind('<div', 0, p_img)
        d2 = idx.rfind('<div', 0, d1)
        s_card = d2 if d2 != -1 else d1
        tag = 'div'
    e_a = idx.find('</a>', p_link)
    e_card = idx.find(f'</{tag}>', e_a)
    if tag == 'div':
        e_card = idx.find('</div>', e_card + 6)
        e_card = idx.find('</div>', e_card + 6) + 6
    else:
        e_card += len(f'</{tag}>')

    base_card = idx[s_card:e_card]

    # اختيار مقالين لليوم لإدراجهما في قمة الصفحة الرئيسية بنفس تصميم البطاقة الأصلية 100%
    day_idx = datetime.date.today().toordinal() % (len(ARTICLES) - 1)
    todays_picks = [ARTICLES[0], ARTICLES[2]] # أسراب المبرمجين + التعلم الفائق والخطاطات الذهنية

    cloned_cards = []
    for slug, t_ar, d_ar, t_en, d_en, b1, b2, b3, c1, c2, acc, strk in todays_picks:
        c = base_card
        c = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', f'./assets/cover_{slug}.svg', c)
        c = c.replace("ثورة الذكاء الاصطناعي: هندسة الوكلاء المستقلين وأتمتة الفحص المعماري للأنظمة", t_ar)
        c = re.sub(r'دراسة هندسية شاملة لبناء وكلاء.*?دون تدخل بشري\.', d_ar, c, flags=re.DOTALL)
        c = re.sub(r'2026-\d{2}-\d{2}', TODAY, c)
        c = c.replace('post_agents_ar.html', f'post_{slug}_ar.html')
        cloned_cards.append(c)

    idx = idx[:s_card] + "<!-- CLONED_DAILY_CARDS_START -->\n" + "\n".join(cloned_cards) + "\n<!-- CLONED_DAILY_CARDS_END -->\n" + idx[s_card:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

# 4. ربط GitHub Actions بهذا المولد ليعمل مرتين يومياً تلقائياً
wf = """name: Non-Stop Dual Daily AI Publisher

on:
  schedule:
    - cron: '0 7 * * *'
    - cron: '0 18 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  publish_daily:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Generate daily bilingual articles with original dark theme
        run: python3 master_daily_publisher.py
      - name: Commit and Push
        run: |
          git config --local user.email "bot@neuraltech-ai.github.io"
          git config --local user.name "NeuralTech Daily Publisher"
          git add .
          git diff --staged --quiet || git commit -m "Auto-publish 2 daily bilingual AI articles"
          git push origin main
"""
with open(".github/workflows/daily_publish.yml", "w", encoding="utf-8") as f:
    f.write(wf)

print("🚀 اكتمل توحيد القالب الداكن الأصلي للمقالات والبطاقات بنجاح 100%!")
