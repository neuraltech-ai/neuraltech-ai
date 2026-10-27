import os, glob, re, hashlib

os.makedirs("assets", exist_ok=True)

# 1. الأغلفة الهندسية الأربعة المصممة خصيصاً للمقالات الأساسية
BASE_COVERS = {
    "agents": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
        <defs>
            <linearGradient id="bgA" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#090d16"/><stop offset="50%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/></linearGradient>
            <linearGradient id="nodeA" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#a855f7"/></linearGradient>
        </defs>
        <rect width="1200" height="630" fill="url(#bgA)"/>
        <g stroke="#312e81" stroke-width="1" opacity="0.4"><path d="M0 105 H1200 M0 210 H1200 M0 315 H1200 M0 420 H1200 M0 525 H1200"/><path d="M200 0 V630 M400 0 V630 M600 0 V630 M800 0 V630 M1000 0 V630"/></g>
        <g stroke="#818cf8" stroke-width="4" opacity="0.85"><line x1="600" y1="300" x2="260" y2="150"/><line x1="600" y1="300" x2="940" y2="150"/><line x1="600" y1="300" x2="260" y2="470"/><line x1="600" y1="300" x2="940" y2="470"/></g>
        <circle cx="600" cy="300" r="105" fill="#1e1b4b" stroke="url(#nodeA)" stroke-width="5"/>
        <text x="600" y="285" fill="#ffffff" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">ORCHESTRATOR</text>
        <text x="600" y="318" fill="#a5b4fc" font-family="sans-serif" font-size="19" font-weight="bold" text-anchor="middle">الوكيل المنسق الذكي</text>
        <text x="600" y="345" fill="#38bdf8" font-family="monospace" font-size="15" text-anchor="middle">[ReAct + Memory]</text>
        <rect x="110" y="85" width="300" height="120" rx="20" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
        <text x="260" y="132" fill="#38bdf8" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">AST Code Auditor</text>
        <text x="260" y="165" fill="#e2e8f0" font-family="sans-serif" font-size="18" text-anchor="middle">فحص أشجار الإعراب البرمجية</text>
        <rect x="790" y="85" width="300" height="120" rx="20" fill="#0f172a" stroke="#a855f7" stroke-width="3"/>
        <text x="940" y="132" fill="#c084fc" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Autonomous Planner</text>
        <text x="940" y="165" fill="#e2e8f0" font-family="sans-serif" font-size="18" text-anchor="middle">التخطيط الذاتي وتقسيم المهام</text>
        <rect x="110" y="410" width="300" height="120" rx="20" fill="#0f172a" stroke="#10b981" stroke-width="3"/>
        <text x="260" y="457" fill="#34d399" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Tool &amp; API Runner</text>
        <text x="260" y="490" fill="#e2e8f0" font-family="sans-serif" font-size="18" text-anchor="middle">تنفيذ الأدوات والأكواد آلياً</text>
        <rect x="790" y="410" width="300" height="120" rx="20" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
        <text x="940" y="457" fill="#fbbf24" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">Critic &amp; Verifier</text>
        <text x="940" y="490" fill="#e2e8f0" font-family="sans-serif" font-size="18" text-anchor="middle">التدقيق الذاتي وتصحيح المسار</text>
        <rect x="320" y="555" width="560" height="48" rx="24" fill="#312e81" opacity="0.85"/>
        <text x="600" y="586" fill="#ffffff" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">AUTONOMOUS MULTI-AGENT ARCHITECTURE</text>
    </svg>""",

    "rag": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
        <defs><linearGradient id="bgR" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#04131d"/><stop offset="50%" stop-color="#083344"/><stop offset="100%" stop-color="#0f172a"/></linearGradient></defs>
        <rect width="1200" height="630" fill="url(#bgR)"/>
        <g stroke="#155e75" stroke-width="1" opacity="0.35"><path d="M0 120 H1200 M0 240 H1200 M0 360 H1200 M0 480 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
        <rect x="280" y="40" width="640" height="54" rx="27" fill="#0e7490" opacity="0.75"/>
        <text x="600" y="74" fill="#ecfeff" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">HYBRID RAG &amp; VECTOR RETRIEVAL ENGINE</text>
        <rect x="70" y="170" width="270" height="290" rx="22" fill="#0f172a" stroke="#38bdf8" stroke-width="3"/>
        <text x="205" y="225" fill="#38bdf8" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">1. Vector Embeddings</text>
        <text x="205" y="260" fill="#cbd5e1" font-family="sans-serif" font-size="18" text-anchor="middle">تقطيع وتضمين الوثائق</text>
        <text x="205" y="315" fill="#22d3ee" font-family="monospace" font-size="16" text-anchor="middle">[0.042, -0.891, 0.512]</text>
        <text x="205" y="350" fill="#22d3ee" font-family="monospace" font-size="16" text-anchor="middle">[0.731,  0.128, -0.34]</text>
        <text x="205" y="405" fill="#94a3b8" font-family="sans-serif" font-size="16" text-anchor="middle">Semantic Chunking</text>
        <path d="M345 315 L445 315" stroke="#22d3ee" stroke-width="5"/><polygon points="445,303 468,315 445,327" fill="#22d3ee"/>
        <rect x="470" y="150" width="280" height="330" rx="24" fill="#164e63" stroke="#06b6d4" stroke-width="4"/>
        <text x="610" y="210" fill="#67e8f9" font-family="sans-serif" font-size="23" font-weight="bold" text-anchor="middle">2. Hybrid Search</text>
        <text x="610" y="245" fill="#ffffff" font-family="sans-serif" font-size="19" font-weight="bold" text-anchor="middle">Vector DB + BM25</text>
        <rect x="500" y="275" width="220" height="75" rx="14" fill="#083344" stroke="#22d3ee" stroke-width="2"/>
        <text x="610" y="308" fill="#a5f3fc" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">Cross-Encoder</text>
        <text x="610" y="335" fill="#cbd5e1" font-family="sans-serif" font-size="15" text-anchor="middle">إعادة ترتيب النتائج الأدق</text>
        <text x="610" y="415" fill="#cffafe" font-family="sans-serif" font-size="18" text-anchor="middle">استرجاع فائق الدقة</text>
        <path d="M755 315 L855 315" stroke="#a855f7" stroke-width="5"/><polygon points="855,303 878,315 855,327" fill="#a855f7"/>
        <rect x="880" y="170" width="260" height="290" rx="22" fill="#1e1b4b" stroke="#a855f7" stroke-width="3"/>
        <text x="1010" y="225" fill="#e879f9" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">3. Grounded LLM</text>
        <text x="1010" y="265" fill="#f8fafc" font-family="sans-serif" font-size="19" font-weight="bold" text-anchor="middle">توليد موثق بالمصادر</text>
        <rect x="915" y="300" width="190" height="55" rx="12" fill="#065f46" stroke="#10b981" stroke-width="2"/>
        <text x="1010" y="334" fill="#a7f3d0" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">✓ 0% Hallucination</text>
        <text x="1010" y="405" fill="#cbd5e1" font-family="sans-serif" font-size="17" text-anchor="middle">إجابات دقيقة بلا هلوسة</text>
    </svg>""",

    "security": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
        <defs><linearGradient id="bgS" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#18040c"/><stop offset="50%" stop-color="#3b071e"/><stop offset="100%" stop-color="#0f172a"/></linearGradient></defs>
        <rect width="1200" height="630" fill="url(#bgS)"/>
        <g stroke="#881337" stroke-width="1" opacity="0.35"><path d="M0 120 H1200 M0 240 H1200 M0 360 H1200 M0 480 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
        <rect x="70" y="185" width="290" height="260" rx="20" fill="#4c0519" stroke="#f43f5e" stroke-width="3"/>
        <text x="215" y="240" fill="#fb7185" font-family="sans-serif" font-size="23" font-weight="bold" text-anchor="middle">⚠ Prompt Injection</text>
        <text x="215" y="280" fill="#fecdd3" font-family="sans-serif" font-size="19" text-anchor="middle">هجمات حقن الأوامر الخبيثة</text>
        <text x="215" y="335" fill="#fda4af" font-family="monospace" font-size="16" text-anchor="middle">Jailbreak / PII Leak</text>
        <text x="215" y="385" fill="#f43f5e" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">[BLOCKED BY GUARDRAIL]</text>
        <path d="M365 315 L445 315" stroke="#f43f5e" stroke-width="5" stroke-dasharray="10,6"/>
        <polygon points="600,95 755,165 755,345 600,520 445,345 445,165" fill="#0f172a" stroke="#10b981" stroke-width="5"/>
        <text x="600" y="245" fill="#34d399" font-family="sans-serif" font-size="25" font-weight="bold" text-anchor="middle">AI FIREWALL</text>
        <text x="600" y="285" fill="#ffffff" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">جدار حماية النماذج</text>
        <text x="600" y="325" fill="#a7f3d0" font-family="sans-serif" font-size="17" text-anchor="middle">NeMo &amp; Llama Guardrails</text>
        <text x="600" y="365" fill="#38bdf8" font-family="monospace" font-size="16" text-anchor="middle">Zero-Trust Sandbox</text>
        <path d="M760 315 L845 315" stroke="#10b981" stroke-width="5"/>
        <rect x="850" y="185" width="280" height="260" rx="20" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
        <text x="990" y="245" fill="#6ee7b7" font-family="sans-serif" font-size="23" font-weight="bold" text-anchor="middle">🔒 Secured LLM</text>
        <text x="990" y="285" fill="#ecfdf5" font-family="sans-serif" font-size="19" font-weight="bold" text-anchor="middle">نموذج معزول وآمن 100%</text>
        <text x="990" y="335" fill="#a7f3d0" font-family="sans-serif" font-size="17" text-anchor="middle">تشفير وحجب البيانات الحساسة</text>
        <text x="990" y="380" fill="#34d399" font-family="monospace" font-size="16" text-anchor="middle">OWASP LLM Compliant</text>
        <rect x="310" y="555" width="580" height="46" rx="23" fill="#881337" opacity="0.85"/>
        <text x="600" y="585" fill="#ffffff" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">ADVERSARIAL AI SECURITY &amp; GUARDRAILS</text>
    </svg>""",

    "triage": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
        <defs><linearGradient id="bgT" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1c1104"/><stop offset="50%" stop-color="#3b2106"/><stop offset="100%" stop-color="#0f172a"/></linearGradient></defs>
        <rect width="1200" height="630" fill="url(#bgT)"/>
        <g stroke="#78350f" stroke-width="1" opacity="0.35"><path d="M0 120 H1200 M0 240 H1200 M0 360 H1200 M0 480 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
        <rect x="270" y="40" width="660" height="52" rx="26" fill="#92400e" opacity="0.85"/>
        <text x="600" y="73" fill="#fef3c7" font-family="sans-serif" font-size="21" font-weight="bold" text-anchor="middle">REAL-TIME AI SMART TRIAGE &amp; PRIORITY MATRIX</text>
        <rect x="80" y="175" width="360" height="290" rx="22" fill="#0f172a" stroke="#f59e0b" stroke-width="4"/>
        <text x="260" y="235" fill="#fbbf24" font-family="sans-serif" font-size="24" font-weight="bold" text-anchor="middle">AI Triage Classifier</text>
        <text x="260" y="275" fill="#ffffff" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle">محرك الفرز وتقييم الخطورة</text>
        <polyline points="115,345 180,345 205,295 235,395 265,315 290,365 315,345 405,345" fill="none" stroke="#10b981" stroke-width="4"/>
        <text x="260" y="425" fill="#38bdf8" font-family="monospace" font-size="17" text-anchor="middle">Latency: 12ms | Confidence: 99.4%</text>
        <path d="M440 240 L570 175 M440 320 L570 320 M440 400 L570 465" stroke="#fbbf24" stroke-width="4"/>
        <rect x="575" y="120" width="540" height="105" rx="18" fill="#4c0519" stroke="#f43f5e" stroke-width="3"/>
        <text x="845" y="165" fill="#fda4af" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">🚨 P1 CRITICAL — أولوية قصوى فورية</text>
        <text x="845" y="200" fill="#fecdd3" font-family="sans-serif" font-size="17" text-anchor="middle">تصعيد فوري للخبير المختص + استجابة طوارئ لحظية</text>
        <rect x="575" y="265" width="540" height="105" rx="18" fill="#451a03" stroke="#f59e0b" stroke-width="3"/>
        <text x="845" y="310" fill="#fcd34d" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">⚡ P2 HIGH — معالجة هجينة سريعة</text>
        <text x="845" y="345" fill="#fef3c7" font-family="sans-serif" font-size="17" text-anchor="middle">تحليل استباقي مدعوم بالذكاء الاصطناعي وتوصية فورية</text>
        <rect x="575" y="410" width="540" height="105" rx="18" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
        <text x="845" y="455" fill="#6ee7b7" font-family="sans-serif" font-size="22" font-weight="bold" text-anchor="middle">✓ P3 ROUTINE — أتمتة ذاتية كاملة</text>
        <text x="845" y="490" fill="#a7f3d0" font-family="sans-serif" font-size="17" text-anchor="middle">حل آلي فوري دون إشغال الطاقم البشري (Zero-Queue)</text>
    </svg>"""
}

for k, v in BASE_COVERS.items():
    with open(f"assets/cover_{k}.svg", "w", encoding="utf-8") as f:
        f.write(v.strip())

# 2. مولّد أوتوماتيكي لأي مقال مستقبلي جديد يقرأ عنوان المقال ويرسم غلافه الهندسي فوراً
def generate_custom_svg_for_new_post(slug, title_text):
    clean_title = re.sub(r'<[^>]+>', '', title_text).strip()
    short_title = clean_title[:55] + ("..." if len(clean_title) > 55 else "")
    h = int(hashlib.md5(slug.encode()).hexdigest()[:6], 16)
    palettes = [
        ("#0f172a", "#1e1b4b", "#6366f1", "#38bdf8"),
        ("#04131d", "#083344", "#06b6d4", "#10b981"),
        ("#18040c", "#311042", "#ec4899", "#a855f7"),
        ("#1c1104", "#0f172a", "#f59e0b", "#38bdf8")
    ]
    c1, c2, acc1, acc2 = palettes[h % len(palettes)]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="100%" height="100%">
        <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c2}"/></linearGradient></defs>
        <rect width="1200" height="630" fill="url(#bg)"/>
        <g stroke="{acc1}" stroke-width="1" opacity="0.25"><path d="M0 126 H1200 M0 252 H1200 M0 378 H1200 M0 504 H1200"/><path d="M240 0 V630 M480 0 V630 M720 0 V630 M960 0 V630"/></g>
        <rect x="90" y="110" width="1020" height="410" rx="28" fill="#090d16" fill-opacity="0.82" stroke="{acc1}" stroke-width="3"/>
        <text x="600" y="210" fill="{acc2}" font-family="monospace" font-size="22" font-weight="bold" text-anchor="middle">⚡ NEURALTECH AI ARCHITECTURE</text>
        <text x="600" y="315" fill="#ffffff" font-family="sans-serif" font-size="30" font-weight="bold" text-anchor="middle">{short_title}</text>
        <rect x="420" y="395" width="360" height="52" rx="26" fill="{acc1}" fill-opacity="0.25" stroke="{acc2}" stroke-width="2"/>
        <text x="600" y="428" fill="#e2e8f0" font-family="sans-serif" font-size="19" font-weight="bold" text-anchor="middle">ENTERPRISE TECHNICAL DEEP-DIVE</text>
    </svg>"""
    out_path = f"assets/cover_{slug}.svg"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg.strip())
    return f"./{out_path}"

def detect_topic(text):
    s = text.lower()
    if any(k in s for k in ["post_agents", "الوكلاء", "وكلاء", "autonomous", "multi-agent", "ast"]):
        return "./assets/cover_agents.svg"
    if any(k in s for k in ["post_rag", "الاسترجاع", "استرجاع", "متجه", "vector", "rag", "hallucination", "هلوسة"]):
        return "./assets/cover_rag.svg"
    if any(k in s for k in ["post_security", "أمن", "الأمن", "حماية", "اختراق", "حقن", "security", "injection", "guardrail", "firewall"]):
        return "./assets/cover_security.svg"
    if any(k in s for k in ["post_triage", "الفرز", "فرز", "أولويات", "طوارئ", "triage", "severity", "escalation"]):
        return "./assets/cover_triage.svg"
    return None

# 3. فحص وتحديث جميع صفحات المقالات الحالية والمستقبلية
for fname in sorted(glob.glob("*.html")):
    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()

    if fname != "index.html":
        cover_url = detect_topic(fname)
        if not cover_url:
            m_title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL) or re.search(r'<title>(.*?)</title>', html, re.DOTALL)
            t_text = m_title.group(1) if m_title else fname
            slug = os.path.splitext(fname)[0]
            cover_url = generate_custom_svg_for_new_post(slug, t_text)
        html = re.sub(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'][^>]*>)', lambda m: m.group(1) + cover_url + m.group(3), html)
    else:
        pos = 0
        out = []
        for m in re.finditer(r'<img\b[^>]*?\bsrc=["\']([^"\']+)["\'][^>]*>', html):
            start, end = m.span()
            out.append(html[pos:start])
            window = html[max(0, start - 300):min(len(html), end + 900)]
            cover_url = detect_topic(window)
            if not cover_url:
                m_link = re.search(r'href=["\'](post_[^"\']+\.html)["\']', window)
                if m_link:
                    slug = os.path.splitext(m_link.group(1))[0]
                    cover_url = f"./assets/cover_{slug}.svg"
            img_tag = m.group(0)
            if cover_url:
                img_tag = re.sub(r'\bsrc=["\'][^"\']+["\']', f'src="{cover_url}"', img_tag)
            out.append(img_tag)
            pos = end
        out.append(html[pos:])
        html = "".join(out)

    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)

# 4. ربط المولّد أوتوماتيكياً بملف master_rebuild.py وأي workflow مستقبلي
if os.path.exists("master_rebuild.py"):
    with open("master_rebuild.py", "r", encoding="utf-8") as f:
        rb = f.read()
    if "auto_cover_engine" not in rb:
        rb += "\n\n# توليد وربط الأغلفة الهندسية أوتوماتيكياً بعد كل بناء\nimport subprocess\nsubprocess.run(['python3', 'auto_cover_engine.py'])\n"
        with open("master_rebuild.py", "w", encoding="utf-8") as f:
            f.write(rb)
        print("🔗 تم ربط المولّد الأوتوماتيكي بـ master_rebuild.py بنجاح!")

print("✅ تم توليد وربط جميع الأغلفة الهندسية الأوتوماتيكية بنجاح 100%!")
