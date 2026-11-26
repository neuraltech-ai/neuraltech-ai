#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeuralTech Daily Publisher v2 — بوت النشر اليومي الحقيقي لموقع نيورال تك
=========================================================================
في كل تشغيل:
  1) إذا نُشر مقال اليوم يتوقف بهدوء (إلا مع NT_FORCE=1).
  2) يختار مجالاً بالتناوب ويطلب من الذكاء الاصطناعي موضوعاً جديداً لم يُنشر من قبل.
  3) يكتب المقال بالعربية ثم نسخته الإنجليزية:
       - Gemini إذا وُجد السر GEMINI_API_KEY (أفضل جودة للعربية)
       - وإلا Pollinations المجاني بلا مفتاح (احتياطي تلقائي أيضاً إذا فشل Gemini)
  4) ينشئ post_<slug>_ar.html و post_<slug>_en.html وغلاف SVG، ويضيف البطاقتين أعلى index.html.
  5) يسجّل المقال في data/articles_db.json بتاريخه الحقيقي. لا يغيّر تواريخ أو محتوى المقالات القديمة.
  6) يستبدل نافذة الدردشة القديمة في كل صفحات الموقع بـ nt-chat.js (آمن، يتكرر بلا ضرر).
إذا فشل التوليد يخرج برمز 1، فيظهر ❌ في GitHub Actions وتصلك رسالة بريد بدل الفشل الصامت.

تشغيل محلي (مثلاً في Termux داخل مجلد المستودع):
    python3 daily_publisher.py             # نشر مقال اليوم
    python3 daily_publisher.py --migrate   # تحديث نافذة الدردشة في الصفحات فقط
لا يحتاج أي مكتبة خارجية (المكتبة القياسية فقط).
"""
import ast
import datetime as dt
import glob
import hashlib
import html
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, "data", "articles_db.json")
INDEX_PATH = os.path.join(ROOT, "index.html")
COVERS_DIR = os.path.join(ROOT, "assets", "covers")
CHAT_TAG = '<script src="nt-chat.js" defer></script>'
STORE_URL = "https://payhip.com/Youstor"
SITE_URL = os.environ.get("SITE_URL", "https://neuraltech-ai.github.io/neuraltech-ai/").rstrip("/") + "/"
TZ_NAME = os.environ.get("NT_TZ", "Africa/Casablanca")
FORCE = os.environ.get("NT_FORCE", "").strip().lower() in ("1", "true", "yes")

# يقبل حتى 3 مفاتيح Gemini (أسرار GitHub: GEMINI_API_KEY و GEMINI2 و GEMINI3)؛ إذا نفدت حصة مفتاح ينتقل للتالي
_KEY_SOURCES = {"GEMINI_API_KEY": "GEMINI_API_KEY", "GEMINI_API_KEY_2": "GEMINI2", "GEMINI_API_KEY_3": "GEMINI3"}
KEY_NAMES = {}
for _env, _name in _KEY_SOURCES.items():
    _k = os.environ.get(_env, "").strip()
    if _k and _k not in KEY_NAMES:
        KEY_NAMES[_k] = _name
for _i, _k in enumerate(k.strip() for k in os.environ.get("GEMINI_API_KEYS", "").split(",")):
    if _k and _k not in KEY_NAMES:
        KEY_NAMES[_k] = f"GEMINI_API_KEYS[{_i + 1}]"
GEMINI_KEYS = list(KEY_NAMES)
GEMINI_KEY = GEMINI_KEYS[0] if GEMINI_KEYS else ""
GEMINI_URL = os.environ.get("NT_GEMINI_URL", "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions")
GEMINI_MODELS = list(dict.fromkeys(m for m in [
    os.environ.get("GEMINI_MODEL", "").strip(),
    "gemini-3.8-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-2.5-flash",
] if m))
POLL_URL = os.environ.get("NT_POLL_URL", "https://text.pollinations.ai/openai")
POLL_KEY = os.environ.get("POLLINATIONS_API_KEY", "").strip()
POLL_MODEL = os.environ.get("POLLINATIONS_MODEL", "openai")
POLL_GAP = float(os.environ.get("NT_POLL_GAP", "32"))  # الحد المجاني: طلب واحد كل ~30 ثانية

# (الاسم العربي، الاسم الإنجليزي، رمز الغلاف) — يتناوب البوت عليها يومياً
CATEGORIES = [
    ("نماذج اللغة والاستدلال", "LLMs & Reasoning", "🧠"),
    ("الوكلاء الأذكياء", "AI Agents", "🤖"),
    ("هندسة البرمجيات بالذكاء الاصطناعي", "AI Software Engineering", "💻"),
    ("تحليل البيانات", "Data Analytics", "📊"),
    ("الأمن السيبراني", "Cybersecurity", "🛡️"),
    ("التعليم الذكي", "AI in Education", "🎓"),
    ("الرؤية الحاسوبية", "Computer Vision", "👁️"),
    ("البحث الدلالي وأنظمة RAG", "RAG & Semantic Search", "🔎"),
    ("الذكاء الاصطناعي على الأجهزة", "On-Device & Edge AI", "📱"),
    ("الأتمتة والإنتاجية", "Automation & Productivity", "⚙️"),
    ("الذكاء الاصطناعي في الصحة", "AI in Healthcare", "🩺"),
    ("أخلاقيات وحوكمة الذكاء الاصطناعي", "AI Ethics & Governance", "⚖️"),
]

AR_RE = re.compile(r"[؀-ۿ]")


def log(msg):
    print(msg, flush=True)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.replace(tmp, path)


def today_str():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(TZ_NAME)).strftime("%Y-%m-%d")
    except Exception:
        return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


# ───────────────────────────── الاتصال بالنماذج ─────────────────────────────
class ApiError(Exception):
    def __init__(self, status, msg, retry_after=None):
        super().__init__(f"HTTP {status}: {str(msg)[:300]}")
        self.status = status
        self.retry_after = retry_after


def post_json(url, payload, headers=None, timeout=240):
    h = {"Content-Type": "application/json", "User-Agent": "NeuralTech-Publisher/2.0"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        ra = e.headers.get("Retry-After") if e.headers else None
        try:
            ra = float(ra) if ra else None
        except ValueError:
            ra = None
        raise ApiError(e.code, body, ra)
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise ApiError(0, e)


def content_from(body):
    s = body.strip()
    if s.startswith("{"):
        try:
            j = json.loads(s)
        except json.JSONDecodeError:
            return s
        if isinstance(j, dict) and j.get("error"):
            raise ApiError(502, json.dumps(j["error"], ensure_ascii=False))
        if isinstance(j, dict) and j.get("choices"):
            c = j["choices"][0].get("message", {}).get("content") or j["choices"][0].get("text") or ""
            if isinstance(c, list):
                c = "".join(x.get("text", "") for x in c if isinstance(x, dict))
            return c
    return s


def _model_missing(e):
    t = str(e).lower()
    return e.status == 404 or "not found" in t or "is not supported" in t or "unknown model" in t


_missing_models = set()
_bad_keys = set()


def _key_problem(e):
    t = str(e).lower()
    return e.status in (401, 403) or (e.status == 400 and ("api key" in t or "api_key" in t))


def _call_gemini_key(key, messages, want_json, more_keys):
    headers = {"Authorization": f"Bearer {key}"}
    last = None
    for model in [m for m in GEMINI_MODELS if m not in _missing_models]:
        payload = {"model": model, "messages": messages, "temperature": 0.7, "reasoning_effort": "low"}
        if want_json:
            payload["response_format"] = {"type": "json_object"}
        attempt = 0
        while attempt < 4:
            attempt += 1
            try:
                out = content_from(post_json(GEMINI_URL, payload, headers))
                log(f"   ✓ Gemini ({model})")
                return out, model
            except ApiError as e:
                last = e
                if _key_problem(e):
                    raise
                if _model_missing(e):
                    log(f"   ↪ النموذج {model} غير متاح، أجرّب التالي")
                    _missing_models.add(model)
                    break
                if e.status == 400 and ("reasoning_effort" in payload or "response_format" in payload):
                    dropped = "reasoning_effort" if "reasoning_effort" in payload else "response_format"
                    payload.pop(dropped)
                    log(f"   ↪ إعادة بدون {dropped}")
                    attempt -= 1
                    continue
                if e.status == 429 and more_keys:
                    raise  # حصة هذا المفتاح نفدت: ننتقل للمفتاح التالي فوراً
                if e.status in (0, 408, 429) or e.status >= 500:
                    wait = min(e.retry_after or 15 * attempt, 90)
                    log(f"   ⚠️ Gemini: {e} — إعادة بعد {wait:.0f}ث ({attempt}/4)")
                    time.sleep(wait)
                    continue
                raise
    raise last or ApiError(503, "لا يوجد نموذج Gemini متاح")


def call_gemini(messages, want_json):
    keys = [k for k in GEMINI_KEYS if k not in _bad_keys]
    last = None
    for i, key in enumerate(keys):
        try:
            return _call_gemini_key(key, messages, want_json, more_keys=i + 1 < len(keys))
        except ApiError as e:
            last = e
            if _key_problem(e) or e.status == 429:
                _bad_keys.add(key)
                why = "نفدت حصته" if e.status == 429 else "غير صالح"
                log(f"   ↪ المفتاح {KEY_NAMES[key]} {why} (HTTP {e.status})" + ("، أجرّب المفتاح التالي" if i + 1 < len(keys) else ""))
                continue
            raise
    raise last or ApiError(503, "لا يوجد مفتاح Gemini صالح")


_last_poll = 0.0


def call_pollinations(messages, want_json):
    global _last_poll
    payload = {"model": POLL_MODEL, "messages": messages, "temperature": 0.7, "max_tokens": 4000}
    if want_json:
        payload["response_format"] = {"type": "json_object"}
    headers = {"Authorization": f"Bearer {POLL_KEY}"} if POLL_KEY else {}
    for attempt in range(1, 7):
        gap = POLL_GAP - (time.time() - _last_poll)
        if _last_poll and gap > 0:
            log(f"   ⏳ انتظار {gap:.0f}ث (حد Pollinations المجاني)")
            time.sleep(gap)
        _last_poll = time.time()
        try:
            out = content_from(post_json(POLL_URL, payload, headers))
            log(f"   ✓ Pollinations ({POLL_MODEL})")
            return out
        except ApiError as e:
            if e.status == 400 and ("response_format" in payload or "max_tokens" in payload):
                dropped = "response_format" if "response_format" in payload else "max_tokens"
                payload.pop(dropped)
                log(f"   ↪ إعادة بدون {dropped}")
                continue
            if e.status in (0, 402, 408, 425, 429) or e.status >= 500:
                wait = min(e.retry_after or (POLL_GAP if e.status in (402, 429) else 10 * attempt), 120)
                log(f"   ⚠️ Pollinations: {e} — إعادة بعد {wait:.0f}ث ({attempt}/6)")
                time.sleep(wait)
                _last_poll = time.time() - POLL_GAP  # انتظرنا للتو
                continue
            raise
    raise ApiError(503, "Pollinations: نفدت المحاولات")


_gemini_disabled = False


def chat(messages, want_json=True):
    global _gemini_disabled
    if GEMINI_KEY and not _gemini_disabled:
        try:
            out, model = call_gemini(messages, want_json)
            return out, f"gemini:{model}"
        except ApiError as e:
            _gemini_disabled = True
            log(f"⚠️ فشل Gemini ({e}). سأكمل عبر Pollinations المجاني…")
    return call_pollinations(messages, want_json), f"pollinations:{POLL_MODEL}"


def gemini_chat(messages, want_json=True):
    """Gemini فقط (للتوليد دفعة واحدة)؛ عند الفشل نتحول للتوليد على أجزاء."""
    global _gemini_disabled
    try:
        out, model = call_gemini(messages, want_json)
        return out, f"gemini:{model}"
    except ApiError:
        _gemini_disabled = True
        raise


# ───────────────────────────── التحقق من المقال ─────────────────────────────
def extract_json(text):
    s = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", str(text or "").strip())
    a, b = s.find("{"), s.rfind("}")
    if a == -1 or b <= a:
        raise ValueError("لا يوجد JSON في الرد")
    chunk = s[a:b + 1]
    try:
        return json.loads(chunk, strict=False)
    except json.JSONDecodeError:
        return json.loads(re.sub(r",\s*([}\]])", r"\1", chunk), strict=False)


def as_text(x):
    return re.sub(r"\s+", " ", str(x or "")).strip()


def validate_article(d, lang):
    if not isinstance(d, dict):
        return None, ["not an object"]
    out = {
        "title": as_text(d.get("title"))[:160],
        "description": as_text(d.get("description"))[:260],
        "tag": as_text(d.get("tag"))[:40],
        "takeaways": [as_text(t) for t in (d.get("takeaways") or []) if as_text(t)][:6],
        "code_explanation": as_text(d.get("code_explanation"))[:700],
    }
    secs = []
    for s in d.get("sections") or []:
        if not isinstance(s, dict):
            continue
        ps = s.get("paragraphs")
        if isinstance(ps, str):
            ps = re.split(r"\n\s*\n", ps)
        ps = [as_text(p) for p in (ps or []) if as_text(p)]
        h = as_text(s.get("heading"))
        if h and ps:
            secs.append({"heading": h[:140], "paragraphs": ps[:5]})
    out["sections"] = secs[:7]

    code = d.get("code") or ""
    if isinstance(code, dict):
        code = code.get("content") or code.get("code") or ""
    code = re.sub(r"^\s*```[\w+-]*\s*\n|\n?\s*```\s*$", "", str(code)).strip("\n")
    out["code"] = ""
    if code.strip():
        try:
            ast.parse(code)
            out["code"] = code[:6000]
        except SyntaxError as e:
            log(f"   ⚠️ الكود لا يجتاز ast.parse ({e.msg}) — سيُحذف من هذه النسخة")

    words = sum(len(p.split()) for s in secs for p in s["paragraphs"])
    out["words"] = words
    errs = []
    if len(out["title"]) < 12:
        errs.append("العنوان قصير")
    if lang == "ar" and not AR_RE.search(out["title"]):
        errs.append("العنوان ليس عربياً")
    if lang == "en" and AR_RE.search(out["title"] + out["description"]):
        errs.append("النسخة الإنجليزية تحتوي نصاً عربياً")
    if len(out["description"]) < 30:
        errs.append("الوصف قصير")
    if len(out["takeaways"]) < 3:
        errs.append("النقاط أقل من 3")
    if len(secs) < 3:
        errs.append("الأقسام أقل من 3")
    if words < 300:
        errs.append(f"المقال قصير ({words} كلمة)")
    return out, errs


def norm_title(t):
    t = re.sub(r"[ً-ٟـ]", "", str(t).lower())
    t = re.sub(r"[إأآٱ]", "ا", t).replace("ة", "ه").replace("ى", "ي")
    return set(w for w in re.split(r"[^0-9a-z؀-ۿ]+", t) if len(w) > 2)


def similar_title(title, titles):
    a = norm_title(title)
    for t in titles:
        b = norm_title(t)
        if a and b and len(a & b) / len(a | b) >= 0.7:
            return t
    return None


def make_slug(raw, existing):
    s = re.sub(r"[^a-z0-9]+", "_", str(raw or "").lower()).strip("_")
    s = "_".join(s.split("_")[:6])[:60].strip("_")
    if len(s) < 4:
        s = "article_" + dt.datetime.now().strftime("%Y%m%d")
    base, n = s, 2
    while s in existing or os.path.exists(os.path.join(ROOT, f"post_{s}_ar.html")):
        s = f"{base}_{n}"
        n += 1
    return s


def read_minutes(art):
    lines = art["code"].count("\n") + 1 if art["code"] else 0
    return max(3, round(art["words"] / 170 + lines / 40))


# ───────────────────────────── التوجيهات (Prompts) ─────────────────────────────
def prompt_ar(cat, titles):
    avoid = "\n".join(f"- {t}" for t in titles[-60:]) or "- (لا يوجد)"
    system = ("أنت كاتب تقني محترف ومحرر علمي دقيق لموقع «نيورال تك» العربي المتخصص في الذكاء الاصطناعي والبرمجة. "
              "تكتب بعربية فصحى سلسة وواضحة، وتعيد دائماً كائن JSON صالحاً فقط دون أي نص قبله أو بعده.")
    user = f"""اكتب مقالاً تقنياً أصيلاً في مجال: «{cat[0]}» ({cat[1]}).

اختر موضوعاً محدداً وعملياً يهم المطورين والمتعلمين العرب، ويختلف بوضوح عن هذه المقالات المنشورة سابقاً:
{avoid}

الشروط:
- من 700 إلى 1000 كلمة موزعة على 4 أو 5 أقسام، في كل قسم فقرتان أو ثلاث.
- الدقة أولاً: لا تخترع إحصاءات أو نسباً مئوية أو أسماء دراسات أو أخباراً وأحداثاً بتواريخ محددة. ركّز على مفاهيم وتقنيات راسخة وتطبيقات عملية. إن ذكرت مكتبة أو أداة فلتكن حقيقية ومعروفة.
- لا مبالغات تسويقية مثل «دقة 100%» أو «ثورة غير مسبوقة».
- مثال كود بايثون قصير (15 إلى 45 سطراً) يعمل بالمكتبة القياسية فقط، بتعليقات عربية، ويمكن تشغيله مباشرة.
- اكتب المصطلح الإنجليزي المهم بين قوسين بعد المصطلح العربي عند أول ذكر.

أعد JSON فقط بهذه البنية:
{{
  "slug": "english_words_with_underscores (3-6 words)",
  "tag": "وسم قصير من كلمة أو كلمتين",
  "title": "عنوان جذاب ودقيق",
  "description": "وصف من جملة أو جملتين (أقل من 200 حرف)",
  "takeaways": ["نقطة 1", "نقطة 2", "نقطة 3", "نقطة 4"],
  "sections": [{{"heading": "عنوان القسم", "paragraphs": ["فقرة", "فقرة"]}}],
  "code": "كود بايثون كامل",
  "code_explanation": "جملتان تشرحان ما يفعله الكود"
}}"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def prompt_en(ar):
    src = json.dumps({k: ar[k] for k in ("tag", "title", "description", "takeaways", "sections", "code", "code_explanation")},
                     ensure_ascii=False)
    system = ("You are a senior technical writer for NeuralTech AI. You write clear, accurate, natural English "
              "and always return a single valid JSON object only, with no text before or after it.")
    user = f"""Create the English edition of this Arabic article. Adapt it naturally for English readers (not word-for-word), keep the same facts, structure and section order, and translate the code comments to English while keeping the code behaviour identical. Do not add statistics or claims that are not in the source.

Arabic article (JSON):
{src}

Return JSON only:
{{"tag": "...", "title": "...", "description": "... (under 200 chars)", "takeaways": ["..."], "sections": [{{"heading": "...", "paragraphs": ["..."]}}], "code": "...", "code_explanation": "..."}}"""
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def generate_single(cat, titles):
    """المقال كاملاً في طلب واحد (Gemini) — أسرع وأكثر تماسكاً."""
    ar = None
    provider = ""
    for attempt in range(1, 4):
        log(f"📝 كتابة المقال العربي (محاولة {attempt}/3) — المجال: {cat[0]}")
        raw, provider = gemini_chat(prompt_ar(cat, titles), True)
        try:
            data = extract_json(raw)
            art, errs = validate_article(data, "ar")
            if errs:
                raise ValueError("، ".join(errs))
            dup = similar_title(art["title"], titles)
            if dup:
                raise ValueError(f"العنوان قريب جداً من مقال سابق: {dup}")
            art["slug_hint"] = data.get("slug") or ""
            ar = art
            break
        except Exception as e:
            log(f"   ⚠️ رد غير صالح: {e} (طول الرد {len(raw)} حرفاً)")
    if not ar:
        raise RuntimeError("تعذّر الحصول على مقال عربي صالح بعد 3 محاولات")

    en = None
    for attempt in range(1, 4):
        log(f"🌍 كتابة النسخة الإنجليزية (محاولة {attempt}/3)")
        raw, _ = gemini_chat(prompt_en(ar), True)
        try:
            art, errs = validate_article(extract_json(raw), "en")
            if errs:
                raise ValueError(", ".join(errs))
            if not art["code"] and ar["code"]:
                art["code"] = ar["code"]
            en = art
            break
        except Exception as e:
            log(f"   ⚠️ رد غير صالح: {e} (طول الرد {len(raw)} حرفاً)")
    if not en:
        raise RuntimeError("تعذّر الحصول على نسخة إنجليزية صالحة بعد 3 محاولات")
    return ar, en, provider



# ─────────── التوليد على أجزاء (للخدمة المجانية التي تقطع الردود الطويلة) ───────────
SYSTEM_AR = "أنت كاتب تقني محترف ومحرر علمي دقيق لموقع «نيورال تك» العربي المتخصص في الذكاء الاصطناعي والبرمجة. تكتب بعربية فصحى سلسة وواضحة."
SYSTEM_EN = "You are a senior technical writer for NeuralTech AI. You write clear, accurate, natural English."


def prompt_outline_ar(cat, titles, n):
    avoid = "\n".join(f"- {t}" for t in titles[-60:]) or "- (لا يوجد)"
    user = f"""نخطط لمقال تقني أصيل في مجال: «{cat[0]}» ({cat[1]}).
اختر موضوعاً محدداً وعملياً يهم المطورين والمتعلمين العرب، ويختلف بوضوح عن هذه المقالات المنشورة سابقاً:
{avoid}

أعد مخطط المقال فقط (لا تكتب المقال نفسه) بصيغة JSON مختصرة:
{{
  "slug": "english_words_with_underscores (3-6 words)",
  "tag": "وسم من كلمة أو كلمتين",
  "title": "عنوان جذاب ودقيق",
  "description": "وصف من جملة واحدة (أقل من 180 حرفاً)",
  "takeaways": ["4 نقاط، كل نقطة أقل من 15 كلمة"],
  "sections": ["{n} عناوين أقسام مرتبة منطقياً"]
}}
لا تخترع إحصاءات أو أخباراً بتواريخ محددة، ولا مبالغات تسويقية. أعد JSON فقط."""
    return [{"role": "system", "content": SYSTEM_AR}, {"role": "user", "content": user}]


def prompt_section_ar(o, heading, i):
    order = "، ".join(f"«{h}»" for h in o["sections"])
    last = i == len(o["sections"]) - 1
    user = f"""نكتب مقالاً بعنوان «{o['title']}» ({o['description']}).
أقسام المقال بالترتيب: {order}.

اكتب الآن القسم رقم {i + 1} فقط: «{heading}».
- فقرتان أو ثلاث، بين 130 و200 كلمة إجمالاً.
- نص عادي فقط: بدون عنوان، بدون Markdown، بدون قوائم. افصل بين الفقرات بسطر فارغ.
- الدقة أولاً: لا إحصاءات مخترعة ولا أسماء دراسات أو أخبار بتواريخ. اكتب المصطلح الإنجليزي بين قوسين عند أول ذكر.
- {'هذا القسم الأخير، فاختمه بخلاصة عملية قصيرة.' if last else 'لا تكتب خاتمة للمقال، ولا تتناول موضوعات الأقسام الأخرى.'}"""
    return [{"role": "system", "content": SYSTEM_AR}, {"role": "user", "content": user}]


def prompt_code_ar(o):
    user = f"""اكتب مثال كود بايثون قصيراً (15 إلى 35 سطراً) يوضح فكرة مقال «{o['title']}».
- يعمل بالمكتبة القياسية فقط ويمكن تشغيله مباشرة، مع تعليقات عربية قصيرة.
أعد الكود داخل كتلة ```python ثم سطراً واحداً بعدها يبدأ بـ «الشرح:» من جملة أو جملتين."""
    return [{"role": "system", "content": SYSTEM_AR}, {"role": "user", "content": user}]


def prompt_outline_en(ar):
    src = json.dumps({"tag": ar["tag"], "title": ar["title"], "description": ar["description"],
                      "takeaways": ar["takeaways"], "sections": [x["heading"] for x in ar["sections"]]}, ensure_ascii=False)
    user = f"""Translate this Arabic article outline into natural English for the English edition of NeuralTech AI. Keep the same number and order of items.
{src}
Return JSON only: {{"tag": "...", "title": "...", "description": "...", "takeaways": ["..."], "sections": ["..."]}}"""
    return [{"role": "system", "content": SYSTEM_EN}, {"role": "user", "content": user}]


def prompt_section_en(title_en, heading_en, paras_ar):
    body = "\n\n".join(paras_ar)
    user = f"""Translate this section of the article "{title_en}" into natural, clear English. Adapt rather than translate word-for-word, keep every fact and add nothing.
Section: "{heading_en}"

{body}

Return plain text only: no heading, no Markdown, paragraphs separated by a blank line."""
    return [{"role": "system", "content": SYSTEM_EN}, {"role": "user", "content": user}]


def prompt_code_en(code):
    user = f"""Translate only the comments and printed strings in this Python code to English. Do not change the logic.
```python
{code}
```
Return the code in a ```python block, then one line starting with "Explanation:" (one or two sentences)."""
    return [{"role": "system", "content": SYSTEM_EN}, {"role": "user", "content": user}]


def trim_to_sentence(t):
    t = str(t or "").rstrip()
    if not t or t[-1] in ".!?؟…»\")":
        return t
    ends = [m.end() for m in re.finditer(r"[.!?؟…]", t)]
    return t[:ends[-1]] if ends and ends[-1] > len(t) * 0.5 else t


def to_paragraphs(raw, heading=""):
    t = re.sub(r"^\s*```\w*\s*|\s*```\s*$", "", str(raw or "").strip())
    lines = []
    for line in t.splitlines():
        x = line.strip()
        if re.match(r"^#{1,6}\s", x):
            continue
        if heading and as_text(x.strip("*_ ").rstrip(":：")) == as_text(heading):
            continue
        lines.append(re.sub(r"^[-*•]\s+", "", x))
    t = trim_to_sentence("\n".join(lines).strip())
    paras = [as_text(p) for p in re.split(r"\n\s*\n", t) if as_text(p)]
    if len(paras) == 1:
        paras = [as_text(p) for p in t.split("\n") if as_text(p)] or paras
    return paras[:5]


def parse_code(raw):
    s = str(raw or "")
    m = re.search(r"```(?:python|py)?[^\n]*\n(.*?)```", s, re.S)
    code, rest = (m.group(1), s[m.end():]) if m else ("", "")
    expl = ""
    mm = re.search(r"(?:الشرح|Explanation)\s*[:：]\s*(.+)", rest, re.S)
    if mm:
        expl = trim_to_sentence(as_text(mm.group(1)))[:400]
    code = code.strip("\n")
    try:
        ast.parse(code)
    except SyntaxError:
        code = ""
    return code, expl


def check_outline(d, lang, n_min=3):
    if not isinstance(d, dict):
        raise ValueError("الرد ليس كائن JSON")
    secs = []
    for x in d.get("sections") or []:
        h = x if isinstance(x, str) else (x.get("heading") if isinstance(x, dict) else "")
        if as_text(h):
            secs.append(as_text(h)[:140])
    o = {"slug": as_text(d.get("slug")), "title": as_text(d.get("title"))[:160],
         "description": as_text(d.get("description"))[:260], "tag": as_text(d.get("tag"))[:40],
         "takeaways": [as_text(t) for t in (d.get("takeaways") or []) if as_text(t)][:6], "sections": secs[:6]}
    errs = []
    if len(o["title"]) < 12:
        errs.append("العنوان قصير")
    if lang == "ar" and not AR_RE.search(o["title"]):
        errs.append("العنوان ليس عربياً")
    if lang == "en" and AR_RE.search(o["title"] + o["description"] + " ".join(secs)):
        errs.append("المخطط الإنجليزي يحتوي نصاً عربياً")
    if len(o["description"]) < 30:
        errs.append("الوصف قصير")
    if len(o["takeaways"]) < 3:
        errs.append("النقاط أقل من 3")
    if len(secs) < n_min:
        errs.append("الأقسام أقل من 3")
    if errs:
        raise ValueError("، ".join(errs))
    return o


def generate_chunked(cat, titles):
    log("🧩 توليد المقال على أجزاء قصيرة (الخدمة المجانية تقطع الردود الطويلة)")
    provider, o = "", None
    for attempt in range(1, 4):
        log(f"📝 مخطط المقال العربي (محاولة {attempt}/3) — المجال: {cat[0]}")
        raw, provider = chat(prompt_outline_ar(cat, titles, 4), True)
        try:
            cand = check_outline(extract_json(raw), "ar")
            dup = similar_title(cand["title"], titles)
            if dup:
                raise ValueError(f"العنوان قريب جداً من مقال سابق: {dup}")
            o = cand
            break
        except Exception as e:
            log(f"   ⚠️ رد غير صالح: {e} (طول الرد {len(raw)} حرفاً)")
    if not o:
        raise RuntimeError("تعذّر الحصول على مخطط عربي صالح بعد 3 محاولات")
    log(f"   ↳ «{o['title']}»")

    secs = []
    for i, h in enumerate(o["sections"]):
        for attempt in (1, 2):
            log(f"✍️ القسم {i + 1}/{len(o['sections'])}: {h}")
            raw, _ = chat(prompt_section_ar(o, h, i), False)
            paras = to_paragraphs(raw, h)
            n = len(" ".join(paras).split())
            if n >= 50 and AR_RE.search(" ".join(paras)):
                secs.append({"heading": h, "paragraphs": paras})
                break
            log(f"   ⚠️ القسم قصير أو غير عربي ({n} كلمة)")
    if len(secs) < 3:
        raise RuntimeError("حصلت على أقل من 3 أقسام صالحة")

    code, expl = "", ""
    log("🐍 مثال الكود")
    try:
        code, expl = parse_code(chat(prompt_code_ar(o), False)[0])
        if not code:
            log("   ⚠️ لم يصل كود صالح — سيُنشر المقال بدون كود")
    except ApiError as e:
        log(f"   ⚠️ تعذّر توليد الكود ({e}) — سيُنشر المقال بدون كود")
    ar, errs = validate_article(dict(o, sections=secs, code=code, code_explanation=expl), "ar")
    if errs:
        raise RuntimeError("المقال العربي غير مكتمل: " + "، ".join(errs))
    ar["slug_hint"] = o["slug"]

    eo = None
    for attempt in range(1, 4):
        log(f"🌍 مخطط النسخة الإنجليزية (محاولة {attempt}/3)")
        raw, _ = chat(prompt_outline_en(ar), True)
        try:
            cand = check_outline(extract_json(raw), "en")
            if len(cand["sections"]) < len(ar["sections"]):
                raise ValueError("عدد الأقسام لا يطابق النسخة العربية")
            eo = cand
            break
        except Exception as e:
            log(f"   ⚠️ رد غير صالح: {e} (طول الرد {len(raw)} حرفاً)")
    if not eo:
        raise RuntimeError("تعذّر الحصول على مخطط إنجليزي صالح بعد 3 محاولات")

    en_secs = []
    for i, sec in enumerate(ar["sections"]):
        h = eo["sections"][i]
        for attempt in (1, 2):
            log(f"🌍 ترجمة القسم {i + 1}/{len(ar['sections'])}")
            raw, _ = chat(prompt_section_en(eo["title"], h, sec["paragraphs"]), False)
            paras = to_paragraphs(raw, h)
            n = len(" ".join(paras).split())
            if n >= 50 and not AR_RE.search(" ".join(paras)):
                en_secs.append({"heading": h, "paragraphs": paras})
                break
            log(f"   ⚠️ الترجمة قصيرة أو فيها عربية ({n} كلمة)")
    if len(en_secs) < 3:
        raise RuntimeError("حصلت على أقل من 3 أقسام إنجليزية صالحة")

    en_code, en_expl = ar["code"], ""
    if ar["code"]:
        log("🐍 ترجمة تعليقات الكود")
        try:
            c, x = parse_code(chat(prompt_code_en(ar["code"]), False)[0])
            if c:
                en_code, en_expl = c, x
        except ApiError as e:
            log(f"   ⚠️ تعذّرت ترجمة الكود ({e}) — سأستعمل الكود العربي")
    en, errs = validate_article(dict(eo, sections=en_secs, code=en_code, code_explanation=en_expl), "en")
    if errs:
        raise RuntimeError("النسخة الإنجليزية غير مكتملة: " + ", ".join(errs))
    return ar, en, provider


def generate_pair(cat, titles):
    if GEMINI_KEY:
        try:
            return generate_single(cat, titles)
        except Exception as e:
            log(f"⚠️ لم ينجح التوليد دفعة واحدة ({e}). أنتقل للتوليد على أجزاء…")
    return generate_chunked(cat, titles)


# ───────────────────────────── توليد الصفحات ─────────────────────────────
EXTRA_CSS = """
        .post-meta { color: var(--text-muted); font-size: 14px; margin: 4px 0 6px; }
        .post-content code { background: var(--bg-elevated); padding: 1px 6px; border-radius: 5px; direction: ltr; unicode-bidi: isolate; font-size: .9em; }
        .post-content strong { color: var(--heading-color); }
        .ai-note { margin-top: 28px; padding: 12px 16px; border-radius: 12px; background: var(--bg-elevated); border: 1px dashed var(--card-border); color: var(--text-muted); font-size: 13.5px; line-height: 1.8; }
"""

FALLBACK_CSS = """<style>
        :root { --bg-main:#0b1120; --bg-card:#151f32; --bg-elevated:#1e293b; --card-border:#26354d; --text-main:#f8fafc; --text-muted:#94a3b8; --heading-color:#60a5fa; --accent:#3b82f6; --badge-bg:rgba(16,185,129,.12); --badge-text:#10b981; --tag-bg:rgba(59,130,246,.14); --tag-text:#60a5fa; --code-bg:#070b14; }
        body.light-mode { --bg-main:#f1f5f9; --bg-card:#fff; --bg-elevated:#f8fafc; --card-border:#e2e8f0; --text-main:#0f172a; --text-muted:#475569; --heading-color:#1d4ed8; --accent:#2563eb; }
        * { box-sizing: border-box; } body { background: var(--bg-main); color: var(--text-main); font-family: system-ui, sans-serif; margin: 0; line-height: 1.75; }
        header { background: var(--bg-card); padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--card-border); }
        .brand-title { font-size: 19px; font-weight: 800; color: var(--heading-color); text-decoration: none; }
        .header-actions { display: flex; gap: 10px; align-items: center; }
        .btn-nav, .theme-btn { background: var(--bg-elevated); color: var(--text-main); border: 1px solid var(--card-border); padding: 7px 13px; border-radius: 12px; text-decoration: none; cursor: pointer; }
        .post-container { max-width: 820px; margin: 22px auto; padding: 0 16px; } .post-card { background: var(--bg-card); border: 1px solid var(--card-border); border-radius: 18px; padding: 24px; }
        .post-hero { width: 100%; height: auto; border-radius: 14px; margin-bottom: 20px; } .post-h1 { font-size: 25px; color: var(--heading-color); }
        .card-meta-top { display: flex; justify-content: space-between; gap: 8px; } .tag-pill, .audit-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; background: var(--tag-bg); color: var(--tag-text); }
        .takeaways-box { background: rgba(59,130,246,.08); border-inline-start: 4px solid var(--accent); border-radius: 12px; padding: 18px 20px; margin: 22px 0; }
        .post-content h2 { color: var(--heading-color); font-size: 20px; } .code-wrapper { position: relative; } .copy-btn { position: absolute; top: 10px; right: 10px; }
        pre { background: var(--code-bg); color: #38bdf8; padding: 18px; border-radius: 12px; overflow-x: auto; direction: ltr; text-align: left; }
        footer { text-align: center; padding: 28px 16px; color: var(--text-muted); border-top: 1px solid var(--card-border); margin-top: 40px; } footer a { color: var(--heading-color); }
    </style>"""

SITE_JS = """<script>
function toggleThemeMode(){document.body.classList.toggle('light-mode');var l=document.body.classList.contains('light-mode');try{localStorage.setItem('nt_theme',l?'light':'dark');}catch(e){}var b=document.getElementById('theme-toggle-btn');if(b)b.textContent=l?'🌙':'☀️';}
(function(){try{if(localStorage.getItem('nt_theme')==='light'){document.body.classList.add('light-mode');var b=document.getElementById('theme-toggle-btn');if(b)b.textContent='🌙';}}catch(e){}})();
function copyArticleCode(btn){var c=btn.parentElement.querySelector('code');if(!c||!navigator.clipboard)return;navigator.clipboard.writeText(c.innerText).then(function(){var o=btn.textContent;btn.textContent='Copied ✓';setTimeout(function(){btn.textContent=o;},1500);});}
</script>"""


def site_style():
    try:
        m = re.search(r"<style>.*?</style>", read(INDEX_PATH), re.S)
        if m:
            return m.group(0).replace("</style>", EXTRA_CSS + "    </style>")
    except OSError:
        pass
    return FALLBACK_CSS.replace("</style>", EXTRA_CSS + "    </style>")


def fmt_inline(t):
    e = html.escape(t, quote=False)
    e = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", e)
    return re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", e)


def minutes_label(n, ar):
    if not ar:
        return f"{n} min read"
    return f"وقت القراءة: {n} {'دقائق' if 3 <= n <= 10 else 'دقيقة'}"


def render_post(a, lang, slug, date, style):
    ar = lang == "ar"
    other = f"post_{slug}_{'en' if ar else 'ar'}.html"
    fn = f"post_{slug}_{lang}.html"
    t, d = html.escape(a["title"]), html.escape(a["description"])
    L = {
        "switch": "🌐 English" if ar else "🌐 العربية",
        "home": "🏠 الرئيسية" if ar else "🏠 Home",
        "theme": "تبديل المظهر" if ar else "Toggle theme",
        "badge": "✍️ كُتب بمساعدة الذكاء الاصطناعي" if ar else "✍️ Written with AI assistance",
        "tk": "💡 أبرز النقاط" if ar else "💡 Key takeaways",
        "code": "🐍 مثال عملي بلغة بايثون" if ar else "🐍 Hands-on Python example",
        "note": ("كُتب هذا المقال آلياً بالذكاء الاصطناعي ضمن النشر اليومي لموقع نيورال تك، وقد يحتوي أخطاء. "
                 "جرّب الكود وتحقق منه قبل استعماله في مشاريعك، ويمكنك سؤال المساعد ✨ عن أي جزء." if ar else
                 "This article was generated with AI as part of NeuralTech's daily publishing and may contain mistakes. "
                 "Test the code before using it in your projects — and ask the ✨ assistant about any part."),
        "store": "المتجر الرقمي" if ar else "Digital Store",
    }
    tk = "\n".join(f"            <li>{fmt_inline(x)}</li>" for x in a["takeaways"])
    body = []
    for s in a["sections"]:
        body.append(f"            <h2>{fmt_inline(s['heading'])}</h2>")
        body.extend(f"            <p>{fmt_inline(p)}</p>" for p in s["paragraphs"])
    code_html = ""
    if a["code"]:
        expl = f"\n            <p>{fmt_inline(a['code_explanation'])}</p>" if a["code_explanation"] else ""
        code_html = f"""
        <div class="post-content">
            <h2>{L['code']}</h2>{expl}
        </div>
        <div class="code-wrapper">
            <button class="copy-btn" onclick="copyArticleCode(this)">Copy</button>
            <pre><code>{html.escape(a['code'])}</code></pre>
        </div>"""
    year = date[:4]
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if ar else 'ltr'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t} | {'نيورال تك' if ar else 'NeuralTech AI'}</title>
    <meta name="description" content="{d}">
    <link rel="canonical" href="{SITE_URL}{fn}">
    <link rel="alternate" hreflang="ar" href="{SITE_URL}post_{slug}_ar.html">
    <link rel="alternate" hreflang="en" href="{SITE_URL}post_{slug}_en.html">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{t}">
    <meta property="og:description" content="{d}">
    <meta property="og:url" content="{SITE_URL}{fn}">
    <meta property="article:published_time" content="{date}">
    {style}
</head>
<body>

<header>
    <a href="index.html" class="brand-title">
        <span>⚡ نيورال تك |</span>
        <span>NeuralTech AI</span>
    </a>
    <div class="header-actions">
        <a href="{other}" class="btn-nav">{L['switch']}</a>
        <a href="index.html" class="btn-nav">{L['home']}</a>
        <button id="theme-toggle-btn" class="theme-btn" onclick="toggleThemeMode()" title="{L['theme']}">☀️</button>
    </div>
</header>

<div class="post-container">
    <article class="post-card">
        <img src="assets/covers/{slug}.svg" alt="{t}" class="post-hero" width="1200" height="630">
        <div class="card-meta-top">
            <span class="tag-pill">{html.escape(a['tag'])}</span>
            <span class="audit-badge">{L['badge']}</span>
        </div>
        <h1 class="post-h1">{t}</h1>
        <div class="post-meta">📅 <time datetime="{date}">{date}</time> • ⏱️ {minutes_label(a['read_minutes'], ar)}</div>
        <div class="takeaways-box">
            <h3>{L['tk']}</h3>
            <ul>
{tk}
            </ul>
        </div>
        <div class="post-content">
{chr(10).join(body)}
        </div>{code_html}
        <div class="ai-note">{L['note']}</div>
    </article>
</div>

<footer>
    © {year} نيورال تك | NeuralTech AI — <a href="{STORE_URL}" target="_blank" rel="noopener">{L['store']}</a>
</footer>

{SITE_JS}
{CHAT_TAG}
</body>
</html>
"""


PALETTES = [("#1d4ed8", "#7c3aed"), ("#0f766e", "#2563eb"), ("#9333ea", "#db2777"),
            ("#0369a1", "#10b981"), ("#b45309", "#dc2626"), ("#4338ca", "#0891b2")]


def cover_svg(slug, cat):
    h = int(hashlib.sha256(slug.encode()).hexdigest(), 16)
    rnd = random.Random(h)
    c1, c2 = PALETTES[h % len(PALETTES)]
    nodes = [(rnd.randint(30, 1170), rnd.randint(30, 600)) for _ in range(24)]
    lines = "".join(
        f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}"/>'
        for i, (x, y) in enumerate(nodes) for (x2, y2) in nodes[i + 1:]
        if (x - x2) ** 2 + (y - y2) ** 2 < 230 ** 2)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{rnd.choice([3, 4, 5, 7])}"/>' for x, y in nodes)
    ar_name, en_name, emoji = cat
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<radialGradient id="r" cx=".8" cy=".15" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="630" fill="#0b1120"/><rect width="1200" height="630" fill="url(#g)" opacity=".92"/><rect width="1200" height="630" fill="url(#r)"/>
<g stroke="#fff" stroke-opacity=".16" stroke-width="1.5">{lines}</g><g fill="#fff" fill-opacity=".5">{dots}</g>
<text x="600" y="295" text-anchor="middle" font-size="150" font-family="Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif">{emoji}</text>
<text x="600" y="415" text-anchor="middle" direction="rtl" font-size="48" font-weight="800" fill="#fff" font-family="system-ui,Segoe UI,Tahoma,sans-serif">{html.escape(ar_name)}</text>
<text x="600" y="472" text-anchor="middle" font-size="26" font-weight="600" fill="#fff" fill-opacity=".8" letter-spacing="3" font-family="system-ui,Segoe UI,Arial,sans-serif">{html.escape(en_name.upper())}</text>
<text x="1165" y="600" text-anchor="end" font-size="22" fill="#fff" fill-opacity=".7" font-family="system-ui,Arial,sans-serif">⚡ NeuralTech AI</text>
</svg>
"""


# ───────────────────────────── الصفحة الرئيسية ─────────────────────────────
START, END = "<!-- NT_AUTO_CARDS_START -->", "<!-- NT_AUTO_CARDS_END -->"


def card_html(rec, lang):
    a, slug, ar = rec[lang], rec["slug"], lang == "ar"
    href = f"post_{slug}_{lang}.html"
    attrs = f'data-lang="{lang}"' + ("" if ar else ' dir="ltr" style="display: none;"')
    t = html.escape(a["title"])
    return f"""        <div class="article-card" {attrs}>
            <a href="{href}"><img src="assets/covers/{slug}.svg" alt="{t}" class="card-thumb" loading="lazy"></a>
            <div class="card-body">
                <div class="card-meta-top">
                    <span class="tag-pill">{html.escape(a['tag'])}</span>
                    <span class="audit-badge">{'🆕 جديد' if ar else '🆕 New'}</span>
                </div>
                <h2 class="card-title">{t}</h2>
                <p class="card-desc">{html.escape(a['description'])}</p>
                <div class="card-footer">
                    <span>📅 {rec['date']} • ⏱️ {minutes_label(a['read_minutes'], ar)}</span>
                    <a href="{href}" class="read-link">{'اقرأ المقال ←' if ar else 'Read Article →'}</a>
                </div>
            </div>
        </div>"""


def update_index(db):
    idx = read(INDEX_PATH)
    recs = sorted(db["articles"], key=lambda r: (r["date"], r.get("created", "")), reverse=True)
    block = "\n".join([START] + [card_html(r, "ar") for r in recs] + [card_html(r, "en") for r in recs] + ["        " + END])
    if START in idx and END in idx:
        idx = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block.strip(), idx, count=1, flags=re.S)
    else:
        m = re.search(r'<div class="grid-cards"[^>]*>', idx)
        if not m:
            raise RuntimeError('لم أجد <div class="grid-cards"> في index.html')
        idx = idx[:m.end()] + "\n        " + block.strip() + "\n" + idx[m.end():]
    write(INDEX_PATH, idx)


def collect_titles(db):
    titles = []
    try:
        titles += [html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
                   for t in re.findall(r'<h2 class="card-title">(.*?)</h2>', read(INDEX_PATH), re.S)]
    except OSError:
        pass
    for r in db["articles"]:
        titles += [r["ar"]["title"], r["en"]["title"]]
    return list(dict.fromkeys(t for t in titles if t))


# ───────────────────────────── ترحيل نافذة الدردشة ─────────────────────────────
OLD_ENGINE_RE = re.compile(r"<!--\s*NeuralTech Hyper-Interactive Conversational Engine[^>]*-->\s*<script>.*?</script>\s*", re.S)


def remove_old_widget(s):
    i = s.find('<div id="nt-ai-wrapper"')
    if i == -1:
        return s
    depth = 0
    for m in re.finditer(r"<div\b|</div\s*>", s[i:]):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            end = i + m.end()
            if "nt-ai-window" in s[i:end] and end - i < 40000:
                return s[:i] + s[end:].lstrip("\n")
            return s
    return s


def migrate_file(path):
    s = read(path)
    orig = s
    s = remove_old_widget(s)
    m = OLD_ENGINE_RE.search(s)
    if m and ("__ntGetSmartReply" in m.group(0) or "pollinations" in m.group(0)):
        s = s[:m.start()] + s[m.end():]
    if "nt-chat.js" not in s:
        k = s.lower().rfind("</body>")
        if k != -1:
            s = s[:k] + CHAT_TAG + "\n" + s[k:]
    if s != orig:
        write(path, s)
        return True
    return False


def migrate_all():
    return sum(1 for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))) if migrate_file(p))


# ───────────────────────────── قاعدة البيانات ─────────────────────────────
def load_db():
    try:
        db = json.loads(read(DB_PATH))
        if isinstance(db, dict) and isinstance(db.get("articles"), list):
            return db
    except (OSError, json.JSONDecodeError):
        pass
    return {"version": 2, "articles": []}


def save_db(db):
    write(DB_PATH, json.dumps(db, ensure_ascii=False, indent=2) + "\n")


# ───────────────────────────── التشغيل ─────────────────────────────
def main():
    os.chdir(ROOT)
    if "--migrate" in sys.argv[1:]:
        log(f"✅ تم تحديث نافذة الدردشة في {migrate_all()} صفحة")
        return 0
    if not os.path.exists(INDEX_PATH):
        log("❌ لم أجد index.html — شغّل السكربت من جذر المستودع")
        return 1
    if not os.path.exists(os.path.join(ROOT, "nt-chat.js")):
        log("⚠️ nt-chat.js غير موجود في جذر المستودع؛ أضفه لتظهر نافذة الدردشة.")

    db = load_db()
    today = today_str()
    if not FORCE and any(r.get("date") == today for r in db["articles"]):
        log(f"ℹ️ مقال اليوم ({today}) منشور مسبقاً — لا جديد.")
        n = migrate_all()
        if n:
            log(f"🔁 حُدّثت نافذة الدردشة في {n} صفحة")
        return 0

    cat = CATEGORIES[len(db["articles"]) % len(CATEGORIES)]
    log(f"🚀 النشر اليومي {today} — المزوّد: " + (f"Gemini ({'، '.join(KEY_NAMES.values())})" if GEMINI_KEYS else "Pollinations (مجاني) — لم أجد أي مفتاح Gemini"))
    try:
        ar, en, provider = generate_pair(cat, collect_titles(db))
    except Exception as e:
        log(f"❌ فشل توليد مقال اليوم: {e}")
        log("   سيحاول التشغيل المجدول التالي مجدداً. للتشغيل الآن: Actions ← Run workflow")
        return 1

    slug = make_slug(ar.get("slug_hint") or en["title"], {r["slug"] for r in db["articles"]})
    ar["read_minutes"] = read_minutes(ar)
    en["read_minutes"] = read_minutes(en)
    for a in (ar, en):
        if not a["tag"]:
            a["tag"] = cat[0] if a is ar else cat[1]

    style = site_style()
    write(os.path.join(COVERS_DIR, f"{slug}.svg"), cover_svg(slug, cat))
    write(os.path.join(ROOT, f"post_{slug}_ar.html"), render_post(ar, "ar", slug, today, style))
    write(os.path.join(ROOT, f"post_{slug}_en.html"), render_post(en, "en", slug, today, style))

    db["articles"].append({
        "slug": slug, "date": today,
        "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "category": cat[1], "provider": provider,
        "ar": {k: ar[k] for k in ("title", "description", "tag", "read_minutes")},
        "en": {k: en[k] for k in ("title", "description", "tag", "read_minutes")},
    })
    save_db(db)
    update_index(db)
    n = migrate_all()
    log(f"✅ نُشر: {ar['title']}")
    log(f"   ↳ post_{slug}_ar.html + post_{slug}_en.html ({ar['words']} / {en['words']} كلمة، عبر {provider})")
    if n:
        log(f"🔁 حُدّثت نافذة الدردشة في {n} صفحة")
    return 0


if __name__ == "__main__":
    sys.exit(main())
