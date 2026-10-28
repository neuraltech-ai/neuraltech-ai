import os, glob, re, datetime, hashlib

os.makedirs("assets", exist_ok=True)
os.makedirs(".github/workflows", exist_ok=True)

TODAY = datetime.date.today().strftime("%Y-%m-%d")

# 1. بنك موسع من المقالات الهندسية العميقة للنشر اليومي المتجدد
DAILY_ARTICLES_BANK = [
    {
        "slug": "deepseek_r1_reasoning",
        "title_ar": "معمارية الاستدلال العميق (Chain-of-Thought) في نماذج الجيل القادم وتطبيقاتها المؤسسية",
        "desc_ar": "تحليل هندسي شامل لآليات التفكير المتسلسل والتعلم المعزز (RL) لبناء نماذج قادرة على حل المعضلات البرمجية والرياضية المعقدة ذاتياً.",
        "title_en": "Deep Reasoning Architectures (Chain-of-Thought) & Reinforcement Learning at Scale",
        "desc_en": "An enterprise engineering deep-dive into multi-step reasoning, self-verification loops, and reinforcement learning for autonomous code synthesis.",
        "read_time": "8",
        "badge_1": "REINFORCEMENT RL",
        "badge_2": "CHAIN OF THOUGHT",
        "badge_3": "SELF-VERIFICATION",
        "color_1": "#0f172a", "color_2": "#1e1b4b", "accent": "#38bdf8", "stroke": "#6366f1",
        "code_sample": """class DeepReasoningEngine:
    def __init__(self, verifier_model):
        self.verifier = verifier_model
        self.thought_trace = []

    def solve_with_reflection(self, problem_statement):
        for step in range(1, 5):
            hypothesis = self.generate_thought_step(problem_statement, self.thought_trace)
            score = self.verifier.evaluate_logic(hypothesis)
            self.thought_trace.append({"step": step, "hypothesis": hypothesis, "confidence": score})
            if score >= 0.96:
                return self.compile_final_solution(self.thought_trace)
        return self.fallback_safe_response()"""
    },
    {
        "slug": "agentic_mesh_enterprise",
        "title_ar": "شبكات الوكلاء المترابطة (Agentic Mesh): كيف تتخاطب الأنظمة الذكية عبر بروتوكول MCP؟",
        "desc_ar": "دراسة تطبيقية لبناء بنية تحتية موزعة تسمح لعشرات الوكلاء المستقلين بتبادل السياق والأدوات بأمان فائق وزمن استجابة لحظي.",
        "title_en": "Enterprise Agentic Mesh: Standardized Context Protocols (MCP) for Multi-Agent Systems",
        "desc_en": "Designing distributed low-latency communication fabrics allowing specialized AI agents to securely share memory, tools, and execution state.",
        "read_time": "6",
        "badge_1": "MCP PROTOCOL",
        "badge_2": "AGENTIC MESH",
        "badge_3": "ZERO-LATENCY SYNC",
        "color_1": "#04131d", "color_2": "#083344", "accent": "#22d3ee", "stroke": "#10b981",
        "code_sample": """class AgenticMeshRouter:
    def __init__(self):
        self.registry = {}

    def register_node(self, agent_id, capabilities):
        self.registry[agent_id] = {"caps": capabilities, "status": "ACTIVE"}

    def dispatch_task(self, intent, context_vector):
        for agent_id, meta in self.registry.items():
            if intent in meta["caps"]:
                return {"routed_to": agent_id, "protocol": "MCP-v2", "state": "SYNCED"}"""
    },
    {
        "slug": "llm_finops_optimization",
        "title_ar": "هندسة ضغط النماذج وتقليل تكاليف الاستدلال السحابي بنسبة 80% عبر التوجيه الذكي",
        "desc_ar": "استراتيجيات عملية لدمج التكميم الرقمي (Quantization AWQ) مع التخزين الدلالي المؤقت (Semantic Caching) لتشغيل الأنظمة الضخمة بكفاءة قصوى.",
        "title_en": "LLM Inference Optimization: Semantic Caching, Speculative Decoding & 4-Bit Quantization",
        "desc_en": "Production techniques to slash GPU inference latency and cloud costs by 80% while preserving 99.2% accuracy across enterprise workloads.",
        "read_time": "7",
        "badge_1": "SEMANTIC CACHE",
        "badge_2": "AWQ QUANTIZATION",
        "badge_3": "SPECULATIVE DECODING",
        "color_1": "#18040c", "color_2": "#311042", "accent": "#f472b6", "stroke": "#a855f7",
        "code_sample": """class SemanticCacheRouter:
    def __init__(self, similarity_threshold=0.93):
        self.threshold = similarity_threshold
        self.vector_cache = {}

    def query_or_infer(self, prompt_embedding, llm_callable):
        for cached_emb, response in self.vector_cache.items():
            if self.cosine_sim(prompt_embedding, cached_emb) >= self.threshold:
                return {"source": "SEMANTIC_CACHE_HIT", "latency_ms": 4, "data": response}
        fresh = llm_callable(prompt_embedding)
        self.vector_cache[prompt_embedding] = fresh
        return {"source": "LLM_INFERENCE", "latency_ms": 420, "data": fresh}"""
    },
    {
        "slug": "graphrag_knowledge_systems",
        "title_ar": "الجيل الجديد من الاسترجاع المعرفي (GraphRAG): دمج الرسوم البيانية المعرفية مع المتجهات",
        "desc_ar": "كيف تتفوق معمارية GraphRAG على البحث المتجهي التقليدي في ربط العلاقات المعقدة واستنتاج الحقائق المخفية عبر آلاف الوثائق المؤسسية.",
        "title_en": "Next-Gen GraphRAG: Combining Knowledge Graphs with Dense Vector Retrieval",
        "desc_en": "Overcoming the limitations of naive vector similarity by mapping entities, edges, and hierarchical communities for multi-hop reasoning.",
        "read_time": "9",
        "badge_1": "KNOWLEDGE GRAPH",
        "badge_2": "MULTI-HOP QUERY",
        "badge_3": "HYBRID VECTOR DB",
        "color_1": "#1c1104", "color_2": "#0f172a", "accent": "#fbbf24", "stroke": "#f59e0b",
        "code_sample": """class HybridGraphRAG:
    def retrieve_multi_hop(self, entity_query, graph_db, vector_db):
        subgraph = graph_db.traverse_neighbors(entity_query, max_depth=2)
        dense_hits = vector_db.search(entity_query, top_k=5)
        return self.merge_and_rerank(subgraph, dense_hits)"""
    }
]

# 2. دالة توليد الغلاف الهندسي المخصص (SVG) لأي مقال جديد
def build_custom_svg(item):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">
    <defs>
        <linearGradient id="bg_{item['slug']}" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="{item['color_1']}"/>
            <stop offset="100%" stop-color="{item['color_2']}"/>
        </linearGradient>
    </defs>
    <rect width="1200" height="630" fill="url(#bg_{item['slug']})"/>
    <g stroke="{item['stroke']}" stroke-width="1" opacity="0.25">
        <path d="M0 126 H1200 M0 252 H1200 M0 378 H1200 M0 504 H1200"/>
        <path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/>
    </g>
    <g stroke="{item['accent']}" stroke-width="4" opacity="0.8">
        <line x1="600" y1="290" x2="250" y2="160"/>
        <line x1="600" y1="290" x2="950" y2="160"/>
        <line x1="600" y1="290" x2="600" y2="490"/>
    </g>
    <circle cx="600" cy="290" r="105" fill="#090d16" stroke="{item['stroke']}" stroke-width="5"/>
    <text x="600" y="280" fill="#ffffff" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">{item['badge_2']}</text>
    <text x="600" y="315" fill="{item['accent']}" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">NeuralTech Core</text>
    <rect x="90" y="95" width="320" height="120" rx="20" fill="#0f172a" stroke="{item['accent']}" stroke-width="3"/>
    <text x="250" y="150" fill="{item['accent']}" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{item['badge_1']}</text>
    <text x="250" y="182" fill="#e2e8f0" font-family="sans-serif" font-size="16" text-anchor="middle">طبقة التحليل والمعالجة الفورية</text>
    <rect x="790" y="95" width="320" height="120" rx="20" fill="#0f172a" stroke="{item['stroke']}" stroke-width="3"/>
    <text x="950" y="150" fill="#c084fc" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">{item['badge_3']}</text>
    <text x="950" y="182" fill="#e2e8f0" font-family="sans-serif" font-size="16" text-anchor="middle">التدقيق الذاتي وضمان الموثوقية</text>
    <rect x="350" y="455" width="500" height="100" rx="20" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
    <text x="600" y="500" fill="#6ee7b7" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">✓ ENTERPRISE PRODUCTION READY</text>
    <text x="600" y="532" fill="#ecfdf5" font-family="sans-serif" font-size="17" text-anchor="middle">{item['title_ar'][:48]}...</text>
</svg>"""
    svg_path = f"assets/cover_{item['slug']}.svg"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    return f"./{svg_path}"

# 3. اختيار مقال جديد لم يُنشر بعد في الصفحة الرئيسية
with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

chosen_article = None
for candidate in DAILY_ARTICLES_BANK:
    if f"post_{candidate['slug']}_ar.html" not in index_html:
        chosen_article = candidate
        break

if not chosen_article:
    # إذا نُشرت كلها، نولّد مقالاً دورياً برقم تاريخ اليوم
    idx = datetime.date.today().toordinal() % len(DAILY_ARTICLES_BANK)
    base = dict(DAILY_ARTICLES_BANK[idx])
    base["slug"] = f"{base['slug']}_{datetime.date.today().strftime('%m%d')}"
    chosen_article = base

cover_rel = build_custom_svg(chosen_article)
ar_file = f"post_{chosen_article['slug']}_ar.html"
en_file = f"post_{chosen_article['slug']}_en.html"

# 4. استخدام أحد المقالات الحالية كقالب متكامل لضمان نفس التصميم والهيدر والمساعد الذكي 100%
template_ar = "post_agents_ar.html" if os.path.exists("post_agents_ar.html") else glob.glob("post_*_ar.html")[0]
with open(template_ar, "r", encoding="utf-8") as f:
    base_post_html = f.read()

new_article_body_ar = f"""
<article class="prose prose-invert max-w-none space-y-6 text-slate-200 leading-relaxed">
    <div class="p-6 rounded-2xl bg-indigo-950/40 border border-indigo-500/30 my-6">
        <p class="text-lg font-semibold text-indigo-200">{chosen_article['desc_ar']}</p>
    </div>
    <h2 class="text-2xl font-bold text-cyan-400 mt-8">1. المعمارية الهندسية والتحديات التشغيلية</h2>
    <p>في بيئات الإنتاج الحديثة، لم يعد كافياً الاعتماد على الاستدعاءات التقليدية للنماذج اللغوية؛ بل يتطلب الاستقرار المؤسسي بناء طبقات تحكم ذكية تضمن الدقة (Accuracy) وتمنع الهلوسة وتقلل زمن الاستجابة إلى أجزاء من الثانية.</p>
    <h2 class="text-2xl font-bold text-cyan-400 mt-8">2. النموذج البرمجي التطبيقي (Production Python Architecture)</h2>
    <pre class="bg-slate-950 p-5 rounded-xl border border-slate-800 overflow-x-auto text-sm text-cyan-300" dir="ltr"><code>{chosen_article['code_sample']}</code></pre>
    <h2 class="text-2xl font-bold text-cyan-400 mt-8">3. معايير الموثوقية والأداء القياسي</h2>
    <ul class="list-disc list-inside space-y-2 text-slate-300">
        <li><strong>التحقق الذاتي المستمر:</strong> فحص مخرجات كل مرحلة برمجياً قبل تمريرها للمستخدم النهائي.</li>
        <li><strong>الاستمرارية الصفرية (Zero-Downtime):</strong> التبديل التلقائي بين النماذج السحابية والمحرك المحلي عند ذروة الضغط.</li>
        <li><strong>الحوكمة والأمان:</strong> عزل السياق الحساس وتطبيق معايير الحماية القياسية في كل طلب.</li>
    </ul>
</article>
"""

post_ar_html = base_post_html
post_ar_html = re.sub(r'<title>.*?</title>', f'<title>{chosen_article["title_ar"]} | NeuralTech AI</title>', post_ar_html, flags=re.DOTALL)
post_ar_html = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1 class="text-3xl md:text-4xl font-extrabold text-white leading-tight mb-4">{chosen_article["title_ar"]}</h1>', post_ar_html, count=1, flags=re.DOTALL)
post_ar_html = re.sub(r'\./assets/cover_[a-zA-Z0-9_]+\.svg', cover_rel, post_ar_html)
post_ar_html = post_ar_html.replace("post_agents_en.html", en_file)
post_ar_html = re.sub(r'<article[^>]*>.*?</article>', new_article_body_ar, post_ar_html, count=1, flags=re.DOTALL)

with open(ar_file, "w", encoding="utf-8") as f:
    f.write(post_ar_html)
with open(en_file, "w", encoding="utf-8") as f:
    f.write(post_ar_html.replace(chosen_article["title_ar"], chosen_article["title_en"]).replace(chosen_article["desc_ar"], chosen_article["desc_en"]))

print(f"✅ تم توليد مقال اليوم الجديد: {ar_file}")

# 5. إدراج بطاقة المقال الجديد في قمة الصفحة الرئيسية (index.html) وتحديث تاريخ أحدث مقال إلى اليوم
new_card_html = f"""
<!-- DAILY_AUTO_CARD_{chosen_article['slug']} -->
<div class="bg-slate-900/90 rounded-3xl overflow-hidden border border-slate-800/80 shadow-2xl hover:border-indigo-500/50 transition-all duration-300 flex flex-col mb-8">
    <div class="relative h-56 overflow-hidden bg-slate-950">
        <img src="{cover_rel}" alt="{chosen_article['title_ar']}" class="w-full h-full object-contain bg-slate-950 p-1">
    </div>
    <div class="p-6 flex-1 flex flex-col justify-between" dir="rtl">
        <div>
            <div class="flex justify-between items-center mb-4">
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-indigo-950 text-indigo-300 border border-indigo-700/40">تقنية (AR)</span>
                <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-700/40">✓ Audited</span>
            </div>
            <h2 class="text-2xl font-extrabold text-white mb-3 leading-snug">{chosen_article['title_ar']}</h2>
            <p class="text-slate-400 text-sm leading-relaxed mb-6">{chosen_article['desc_ar']}</p>
        </div>
        <div class="pt-4 border-t border-slate-800/80 flex justify-between items-center text-xs text-slate-400">
            <span>📅 {TODAY} • ⏱️ وقت القراءة: {chosen_article['read_time']} دقائق</span>
            <a href="./{ar_file}" class="text-indigo-400 hover:text-indigo-300 font-bold text-sm">اقرأ المقال ←</a>
        </div>
    </div>
</div>
"""

if f"DAILY_AUTO_CARD_{chosen_article['slug']}" not in index_html:
    # ندرج البطاقة الجديدة مباشرة قبل أول بطاقة مقال موجودة في index.html
    first_card_match = re.search(r'(<(?:article|div)\b[^>]*>\s*<(?:div|a)\b[^>]*>\s*<img\b[^>]*cover_)', index_html)
    if first_card_match:
        insert_pos = first_card_match.start()
        index_html = index_html[:insert_pos] + new_card_html + "\n" + index_html[insert_pos:]
    else:
        index_html = re.sub(r'(<main[^>]*>)', r'\1\n' + new_card_html, index_html, count=1)

# 6. الإزالة الجذرية للزر القديم المكرر (✨ NeuralTech AI) من الكود المصدري لجميع الصفحات!
KILL_LEGACY_BTN_SCRIPT = """<script>
(function() {
    function nukeLegacyButtons() {
        document.querySelectorAll('button, a, div').forEach(function(el) {
            if (el.id === 'nt-copilot-btn' || el.closest('#nt-copilot-panel') || el.closest('header') || el.closest('nav')) return;
            var txt = (el.innerText || '').trim();
            if ((txt === 'NeuralTech AI ✨' || txt === '✨ NeuralTech AI' || (txt.indexOf('NeuralTech AI') !== -1 && txt.indexOf('✨') !== -1)) && el.children.length <= 2) {
                el.remove();
            }
        });
    }
    nukeLegacyButtons();
    window.addEventListener('DOMContentLoaded', nukeLegacyButtons);
    setTimeout(nukeLegacyButtons, 300);
    setTimeout(nukeLegacyButtons, 1000);
})();
</script>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

for fname in sorted(glob.glob("*.html")):
    with open(fname, "r", encoding="utf-8") as f:
        h = f.read()

    # حذف أي زر HTML ثابت يحتوي على NeuralTech AI و ✨ مباشرة من الكود
    h = re.sub(r'<button\b[^>]*>(?:(?!</button>).)*?(?:✨\s*NeuralTech AI|NeuralTech AI\s*✨)(?:(?!</button>).)*?</button>', '', h, flags=re.DOTALL)

    if "function nukeLegacyButtons()" not in h:
        h = h.replace("</body>", KILL_LEGACY_BTN_SCRIPT + "\n</body>")

    with open(fname, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"🧹 تم تطهير {fname} من الزر القديم نهائياً وتحديث المحتوى!")

# 7. إنشاء GitHub Actions Workflow ليعمل تلقائياً كل يوم في الساعة 08:00 صباحاً دون تدخل منك
workflow_yaml = """name: Daily Autonomous AI Blog Publisher

on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  publish_daily_post:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Generate and publish daily enterprise AI article
        run: |
          python3 ultimate_daily_automation.py

      - name: Commit and push new daily article
        run: |
          git config --local user.email "bot@neuraltech-ai.github.io"
          git config --local user.name "NeuralTech Autonomous Publisher"
          git add .
          git diff --staged --quiet || git commit -m "Auto-publish daily AI engineering article"
          git push origin main
"""

with open(".github/workflows/daily_publish.yml", "w", encoding="utf-8") as f:
    f.write(workflow_yaml)

print("🚀 تم تفعيل النشر اليومي التلقائي عبر GitHub Actions (.github/workflows/daily_publish.yml) بنجاح!")
