/*!
 * NeuralTech Chat v2 — نافذة الدردشة التفاعلية لموقع نيورال تك
 * ------------------------------------------------------------------
 * التركيب: ضع هذا الملف في جذر المستودع، ثم أضف قبل </body> في كل صفحة:
 *     <script src="nt-chat.js" defer></script>
 * (اختياري، لردود فورية بلا انتظار) بعد إنشاء الخادم الوسيط worker.js ضع رابطه في DEFAULT_PROXY أدناه.
 *
 * - يجرب: الخادم الوسيط (إن وُجد) ← Pollinations المجاني ← إجابة محلية من نص المقال.
 * - يعيد المحاولة تلقائياً عند الازدحام مع عدّاد تنازلي، فلا "يتوقف" أبداً.
 * - يقرأ المقال الحالي (العنوان، النقاط، المحتوى، الكود) وقائمة مقالات الموقع.
 */
(function () {
  'use strict';
  // (اختياري) بعد إنشاء الخادم الوسيط worker.js على Cloudflare ضع رابطه هنا لردود فورية:
  var DEFAULT_PROXY = '';   // مثال: 'https://neuraltech-chat.اسمك.workers.dev'
  if (window.__NTC_LOADED__) return;
  window.__NTC_LOADED__ = true;

  var SCRIPT = document.currentScript;
  var CFG = Object.assign({
    proxyUrl: (SCRIPT && SCRIPT.getAttribute('data-proxy')) || DEFAULT_PROXY,
    pollinationsOpenAI: 'https://text.pollinations.ai/openai',
    pollinationsClassic: 'https://text.pollinations.ai/',
    pollinationsModel: 'openai',
    requestTimeout: 75,   // ثوانٍ بلا أي استجابة قبل اعتبار الطلب فاشلاً
    maxWaitPerTry: 45,    // أقصى انتظار بين محاولتين
    totalBudget: 120,     // بعد هذه المدة نعرض إجابة محلية من المقال
    maxStored: 40,        // عدد الرسائل المحفوظة لكل صفحة
    sendHistory: 10       // عدد الرسائل السابقة المرسلة للنموذج
  }, window.NTC_CONFIG || {});

  var IS_EN = /^en/i.test(document.documentElement.lang || '') || /_en\.html?$/i.test(location.pathname);
  var DIR = IS_EN ? 'ltr' : 'rtl';

  var T = IS_EN ? {
    fab: 'Ask the assistant', title: 'NeuralTech Assistant', ready: 'Ready', thinking: 'Thinking…',
    writing: 'Writing…', switching: 'Trying another server…',
    waiting: function (s) { return 'Server busy — retrying in ' + s + 's'; },
    placeholder: 'Type your question… (Enter to send)', send: 'Send', stop: 'Stop',
    newChat: 'New chat', close: 'Close', copy: 'Copy', copied: 'Copied ✓', retry: 'Retry',
    ctx: 'About:', disclaimer: 'Answers are AI-generated and may contain mistakes.',
    welcomePost: function (t) { return 'Hi 👋 I\'m the **NeuralTech Assistant** (an AI assistant). I\'ve read **"' + t + '"** — I can summarize it, explain the code, give examples, or quiz you. Where shall we start?'; },
    welcomeHome: 'Hi 👋 I\'m the **NeuralTech Assistant**. Tell me what you\'re interested in and I\'ll point you to the right article — or ask me any tech question.',
    chipsPost: ['💡 Summarize this article', '🧪 Give me a practical example', '❓ Quiz me on it', '📚 Suggest a related article'],
    chipCode: '🐍 Explain the code step by step',
    chipsHome: ['🔎 What are the latest articles?', '🎯 Suggest an article for beginners', '🤖 What are AI agents?'],
    askSel: '✨ Ask about this', selPrompt: function (s) { return 'Explain this passage from the article in simple terms:\n> ' + s; },
    nudge: '👋 Questions about this article? Ask me!',
    stopped: '_(stopped)_', takeaways: 'Key points',
    localIntro: '⚠️ The AI service is busy right now, so I searched this page directly:',
    localNone: '⚠️ The AI service is busy right now and I couldn\'t find a close match on this page.',
    localArticles: 'Articles that may help:', localSummary: 'Key points of the article:',
    localRetry: 'Tap **Retry** in a moment for a full answer.'
  } : {
    fab: 'اسأل المساعد', title: 'مساعد نيورال تك', ready: 'جاهز للإجابة', thinking: 'يفكّر…',
    writing: 'يكتب…', switching: 'أجرّب خادماً آخر…',
    waiting: function (s) { return 'الخدمة مزدحمة، أعيد المحاولة خلال ' + s + ' ث'; },
    placeholder: 'اكتب سؤالك… (Enter للإرسال)', send: 'إرسال', stop: 'إيقاف',
    newChat: 'محادثة جديدة', close: 'إغلاق', copy: 'نسخ', copied: 'تم النسخ ✓', retry: 'إعادة المحاولة',
    ctx: 'نتحدث عن:', disclaimer: 'الردود مولّدة بالذكاء الاصطناعي وقد تحتوي أخطاء.',
    welcomePost: function (t) { return 'أهلاً بك 👋 أنا **مساعد نيورال تك** (مساعد ذكاء اصطناعي). قرأت مقال **«' + t + '»** ويمكنني تلخيصه، أو شرح الكود، أو إعطاؤك أمثلة، أو اختبار فهمك. بماذا نبدأ؟'; },
    welcomeHome: 'أهلاً بك 👋 أنا **مساعد نيورال تك**. أخبرني بما يهمّك وسأقترح عليك المقال المناسب، أو اسألني أي سؤال تقني.',
    chipsPost: ['💡 لخّص لي المقال', '🧪 أعطني مثالاً عملياً', '❓ اختبرني بسؤال عن المقال', '📚 اقترح مقالاً مشابهاً'],
    chipCode: '🐍 اشرح الكود خطوة بخطوة',
    chipsHome: ['🔎 ما أحدث المقالات؟', '🎯 اقترح مقالاً للمبتدئين', '🤖 ما هم الوكلاء الأذكياء؟'],
    askSel: '✨ اسأل عن هذا', selPrompt: function (s) { return 'اشرح لي هذا المقطع من المقال بأسلوب بسيط:\n> ' + s; },
    nudge: '👋 عندك سؤال عن المقال؟ اسألني!',
    stopped: '_(أُوقف الرد)_', takeaways: 'أبرز النقاط',
    localIntro: '⚠️ خدمة الذكاء الاصطناعي مزدحمة الآن، فبحثت لك داخل الصفحة مباشرة:',
    localNone: '⚠️ خدمة الذكاء الاصطناعي مزدحمة الآن ولم أجد في هذه الصفحة ما يطابق سؤالك بدقة.',
    localArticles: 'مقالات قد تفيدك:', localSummary: 'أبرز نقاط المقال:',
    localRetry: 'اضغط **إعادة المحاولة** بعد قليل للحصول على إجابة كاملة.'
  };

  var state = {
    open: false, busy: false, controller: null, history: [], ctx: null, articles: null,
    key: 'ntc_v2_' + location.pathname, partial: '', anim: 0, built: false
  };

  /* ------------------------------ أدوات عامة ------------------------------ */
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function clean(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function abortErr() { var e = new Error('aborted'); e.name = 'AbortError'; return e; }
  function isAbort(e) { return e && (e.name === 'AbortError'); }
  function reducedMotion() { return window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function isMobile() { return window.matchMedia && matchMedia('(max-width: 640px)').matches; }
  function load() {
    try { var d = JSON.parse(localStorage.getItem(state.key) || 'null'); if (d && Array.isArray(d.h)) state.history = d.h; } catch (e) { }
  }
  function save() {
    try { localStorage.setItem(state.key, JSON.stringify({ h: state.history.slice(-CFG.maxStored) })); } catch (e) { }
  }

  /* --------------------------- سياق الصفحة والمقالات --------------------------- */
  function getContext() {
    if (state.ctx) return state.ctx;
    var h1 = document.querySelector('.post-h1') || document.querySelector('article h1, main h1, h1');
    var post = document.querySelector('.post-content');
    var takeaways = qsa('.takeaways-box li').map(function (el) { return clean(el.textContent); }).filter(Boolean);
    var passages = [], section = '';
    if (post) qsa('h2, h3, p, li', post).forEach(function (el) {
      var t = clean(el.textContent); if (!t) return;
      if (/^H[23]$/.test(el.tagName)) { section = t; passages.push({ t: t, h: 1 }); }
      else passages.push({ t: t, s: section });
    });
    takeaways.forEach(function (t) { passages.push({ t: t, s: T.takeaways }); });
    var codeEl = document.querySelector('.post-card pre code, .post-content pre code, .code-wrapper code');
    state.ctx = {
      isPost: !!(post || document.querySelector('.post-card')),
      title: h1 ? clean(h1.textContent) : document.title,
      takeaways: takeaways, passages: passages,
      code: codeEl ? codeEl.textContent.trim() : '',
      body: post ? clean(post.textContent) : ''
    };
    return state.ctx;
  }

  function parseCards(doc) {
    var lang = IS_EN ? 'en' : 'ar', here = location.pathname.split('/').pop(), out = [];
    qsa('.article-card', doc).forEach(function (card) {
      if ((card.getAttribute('data-lang') || 'ar') !== lang) return;
      var a = card.querySelector('a[href]'), t = card.querySelector('.card-title'), d = card.querySelector('.card-desc');
      if (!a || !t) return;
      var href = a.getAttribute('href');
      if (!href || href === here) return;
      out.push({ t: clean(t.textContent), d: clean(d ? d.textContent : '').slice(0, 160), u: href });
    });
    return out.slice(0, 30);
  }

  var articlesPromise = null;
  function ensureArticles() {
    if (state.articles) return Promise.resolve(state.articles);
    var fromDom = parseCards(document);
    if (fromDom.length) { state.articles = fromDom; return Promise.resolve(fromDom); }
    try {
      var c = JSON.parse(sessionStorage.getItem('ntc_articles_v2_' + (IS_EN ? 'en' : 'ar')) || 'null');
      if (c && c.length) { state.articles = c; return Promise.resolve(c); }
    } catch (e) { }
    if (!articlesPromise) {
      articlesPromise = fetch('index.html', { cache: 'no-cache' })
        .then(function (r) { return r.ok ? r.text() : ''; })
        .then(function (html) {
          var list = html ? parseCards(new DOMParser().parseFromString(html, 'text/html')) : [];
          state.articles = list;
          try { sessionStorage.setItem('ntc_articles_v2_' + (IS_EN ? 'en' : 'ar'), JSON.stringify(list)); } catch (e) { }
          return list;
        })
        .catch(function () { state.articles = []; return []; });
    }
    return articlesPromise;
  }

  function systemPrompt() {
    var ctx = getContext();
    var arts = (state.articles || []).slice(0, 24).map(function (a) { return '- [' + a.t + '](' + a.u + '): ' + a.d; }).join('\n');
    var p = [];
    if (IS_EN) {
      p.push('You are the "NeuralTech Assistant", an AI assistant on NeuralTech AI, a bilingual (Arabic/English) tech articles website.');
      p.push('Rules:\n- Reply in the visitor\'s language (English by default), clear and friendly.\n- Be concise and interactive: 2–6 sentences or a short list, unless the visitor asks for detail.\n- Rely first on the article below. If the question goes beyond it, answer from general knowledge and say so.\n- Never invent numbers, sources or links. When suggesting articles, use only links from "Site articles", formatted [Title](link).\n- If asked for a quiz, ask ONE multiple-choice question, wait for the answer, then grade it.\n- If asked who you are: you are an AI assistant, not a human.\n- Use light Markdown: **bold**, `code`, lists, ``` code blocks.\n- End EVERY reply with one final line containing three short follow-up questions the visitor could ask, exactly in this format:\n<<short question | short question | short question>>');
      if (ctx.isPost) p.push('[Current article]\nTitle: ' + ctx.title +
        (ctx.takeaways.length ? '\nKey points:\n- ' + ctx.takeaways.join('\n- ') : '') +
        (ctx.body ? '\nContent (excerpt):\n' + ctx.body.slice(0, 3500) : '') +
        (ctx.code ? '\nAttached code:\n```\n' + ctx.code.slice(0, 1800) + '\n```' : ''));
      else p.push('[Current page]\nThe homepage. Help the visitor pick the right article for their interest.');
      if (arts) p.push('[Site articles]\n' + arts);
    } else {
      p.push('أنت «مساعد نيورال تك»، مساعد ذكاء اصطناعي داخل موقع نيورال تك (NeuralTech AI) للمقالات التقنية بالعربية والإنجليزية.');
      p.push('قواعد الرد:\n- أجب بلغة الزائر (العربية افتراضياً) بأسلوب واضح وودود.\n- كن مختصراً وتفاعلياً: من 2 إلى 6 جمل أو قائمة قصيرة، إلا إذا طلب الزائر التفصيل.\n- اعتمد أولاً على محتوى المقال أدناه. إن كان السؤال خارج المقال فأجب من معرفتك العامة وقل ذلك بوضوح.\n- لا تخترع أرقاماً أو مصادر أو روابط. عند اقتراح مقال استعمل فقط الروابط الموجودة في «مقالات الموقع» بصيغة [العنوان](الرابط).\n- إذا طلب الزائر اختباراً فاطرح سؤالاً واحداً متعدد الخيارات، وانتظر إجابته ثم صحّحها.\n- إن سُئلت عن هويتك فأنت مساعد ذكاء اصطناعي ولست إنساناً.\n- استعمل Markdown بسيطاً: **غامق**، `كود`، قوائم، وكتل ``` للكود.\n- اختم كل رد بسطر أخير فيه ثلاثة أسئلة متابعة قصيرة قد يطرحها الزائر، بهذا الشكل بالضبط:\n<<سؤال قصير | سؤال قصير | سؤال قصير>>');
      if (ctx.isPost) p.push('[المقال الحالي]\nالعنوان: ' + ctx.title +
        (ctx.takeaways.length ? '\nأبرز النقاط:\n- ' + ctx.takeaways.join('\n- ') : '') +
        (ctx.body ? '\nالمحتوى (مقتطف):\n' + ctx.body.slice(0, 3500) : '') +
        (ctx.code ? '\nالكود المرفق:\n```\n' + ctx.code.slice(0, 1800) + '\n```' : ''));
      else p.push('[الصفحة الحالية]\nالصفحة الرئيسية للموقع. ساعد الزائر على اختيار المقال المناسب لاهتمامه.');
      if (arts) p.push('[مقالات الموقع]\n' + arts);
    }
    return p.join('\n\n');
  }

  function buildMessages() {
    var hist = state.history.filter(function (m) { return !m.local; }).slice(-CFG.sendHistory);
    while (hist.length && hist[0].role !== 'user') hist.shift();
    var msgs = [{ role: 'system', content: systemPrompt() }];
    hist.forEach(function (m) {
      msgs.push({ role: m.role, content: m.role === 'assistant' ? splitSuggestions(m.content).text : m.content });
    });
    return msgs;
  }

  /* ------------------------------ الاتصال بالنماذج ------------------------------ */
  var PROVIDERS = [];
  if (CFG.proxyUrl) PROVIDERS.push({ id: 'proxy', url: CFG.proxyUrl, build: function (m) { return { messages: m, stream: true }; } });
  PROVIDERS.push({ id: 'poll', url: CFG.pollinationsOpenAI, build: function (m) { return { model: CFG.pollinationsModel, messages: m }; } });
  PROVIDERS.push({ id: 'poll-classic', url: CFG.pollinationsClassic, onlyAfterHardError: true, build: function (m) { return { model: CFG.pollinationsModel, messages: m }; } });

  function parseRetryAfter(v) {
    if (!v) return null;
    var n = parseFloat(v);
    if (!isNaN(n)) return n;
    var d = Date.parse(v);
    return isNaN(d) ? null : Math.max(0, (d - Date.now()) / 1000);
  }

  function cleanReply(t) {
    return String(t || '')
      .replace(/\n*-{3,}\s*\n+[^\n]*(?:🌸\s*Ad\s*🌸|Powered by Pollinations|Support Pollinations)[\s\S]*$/i, '')
      .replace(/🌸\s*Ad\s*🌸[\s\S]*$/i, '')
      .replace(/^\s*assistant\s*:\s*/i, '')
      .trim();
  }

  function extractText(raw) {
    var s = String(raw || '').trim();
    if (s.charAt(0) === '{') {
      var j = null;
      try { j = JSON.parse(s); } catch (e) { j = null; }
      if (j) {
        if (j.error) {
          var msg = typeof j.error === 'string' ? j.error : (j.error.message || 'error');
          var er = new Error(msg); er.status = /(rate|limit|queue|quota|tier|busy)/i.test(msg) ? 429 : 502; throw er;
        }
        var c = j.choices && j.choices[0];
        var out = c ? (c.message ? c.message.content : c.text) : (j.content || j.text || j.response || '');
        if (Array.isArray(out)) out = out.map(function (x) { return x.text || ''; }).join('');
        return out || '';
      }
    }
    if (s.length < 400 && /(free limit|1 reply every|rate limit|too many requests|queue full)/i.test(s)) {
      var e2 = new Error(s.slice(0, 120)); e2.status = 429; throw e2;
    }
    return s;
  }

  function readSSE(body, onDelta, touch) {
    var reader = body.getReader(), dec = new TextDecoder(), buf = '', acc = '';
    function pump() {
      return reader.read().then(function (r) {
        if (r.done) return acc;
        touch();
        buf += dec.decode(r.value, { stream: true });
        var lines = buf.split(/\r?\n/); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          var line = lines[i].trim();
          if (line.indexOf('data:') !== 0) continue;
          var data = line.slice(5).trim();
          if (!data) continue;
          if (data === '[DONE]') return acc;
          var j; try { j = JSON.parse(data); } catch (e) { continue; }
          if (j.error) {
            var m = j.error.message || 'stream error', er = new Error(m);
            er.status = /(rate|quota|limit|exhaust)/i.test(m) ? 429 : 502; throw er;
          }
          var c = j.choices && j.choices[0];
          var d = c ? ((c.delta && c.delta.content) || (c.message && c.message.content) || c.text || '') : '';
          if (d) { acc += d; onDelta(acc, false); }
        }
        return pump();
      });
    }
    return pump().catch(function (e) {
      if (e && e.status) throw e;
      if (acc.length > 80) return acc;   // انقطع البث بعد جزء مفيد: نحتفظ به
      throw e;
    });
  }

  function callProvider(p, messages, signal, onDelta) {
    var ctrl = new AbortController(), timedOut = false, timer = null;
    function touch() {
      clearTimeout(timer);
      timer = setTimeout(function () { timedOut = true; ctrl.abort(); }, CFG.requestTimeout * 1000);
    }
    function onUserAbort() { ctrl.abort(); }
    if (signal.aborted) return Promise.reject(abortErr());
    signal.addEventListener('abort', onUserAbort, { once: true });
    touch();
    function done() { clearTimeout(timer); signal.removeEventListener('abort', onUserAbort); }
    function normalize(e) {
      if (signal.aborted) return abortErr();
      if (e && e.status !== undefined) return e;
      var er = new Error(timedOut ? 'timeout' : 'network'); er.status = 0; return er;
    }
    return fetch(p.url, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(p.build(messages)), signal: ctrl.signal
    }).then(function (res) {
      if (!res.ok) {
        var er = new Error('HTTP ' + res.status); er.status = res.status;
        er.retryAfter = parseRetryAfter(res.headers.get('Retry-After'));
        throw er;
      }
      var ct = (res.headers.get('Content-Type') || '').toLowerCase();
      if (ct.indexOf('event-stream') > -1 && res.body && res.body.getReader) {
        return readSSE(res.body, onDelta, touch).then(cleanReply);
      }
      return res.text().then(function (raw) {
        var txt = cleanReply(extractText(raw));
        if (txt) onDelta(txt, true);
        return txt;
      });
    }).then(function (txt) {
      if (signal.aborted) throw abortErr();
      if (!txt || txt.length < 2) { var er = new Error('empty'); er.status = 0; throw er; }
      done(); return txt;
    }).catch(function (e) { done(); throw normalize(e); });
  }

  function sleepCountdown(secs, signal, onTick) {
    return new Promise(function (resolve, reject) {
      var left = Math.max(1, Math.ceil(secs));
      onTick(left);
      var iv = setInterval(function () {
        left--;
        if (left <= 0) { clearInterval(iv); resolve(); } else onTick(left);
      }, 1000);
      signal.addEventListener('abort', function () { clearInterval(iv); reject(abortErr()); }, { once: true });
    });
  }

  function generate(messages, hooks) {
    var start = Date.now(), lastErr = null, prevHard = false;
    var pi = 0, attempt = 0;
    function elapsed() { return (Date.now() - start) / 1000; }
    function nextProvider() {
      pi++; attempt = 0;
      while (pi < PROVIDERS.length && PROVIDERS[pi].onlyAfterHardError && !prevHard) pi++;
      if (pi >= PROVIDERS.length || elapsed() > CFG.totalBudget) return Promise.reject(lastErr || new Error('failed'));
      hooks.status('switching');
      return tryOnce();
    }
    function tryOnce() {
      attempt++;
      hooks.status('thinking');
      return callProvider(PROVIDERS[pi], messages, hooks.signal, hooks.delta).catch(function (e) {
        if (isAbort(e) || hooks.signal.aborted) throw abortErr();
        lastErr = e;
        var st = e.status || 0;
        var retriable = st === 0 || st === 402 || st === 408 || st === 425 || st === 429 || st >= 500;
        prevHard = !retriable || st === 0;   // خطأ شبكة/CORS: جرّب المسار الكلاسيكي أيضاً
        if (!retriable) return nextProvider();
        var wait = (e.retryAfter != null) ? e.retryAfter : Math.min(4 * Math.pow(2, attempt - 1), 20) + Math.random() * 1.5;
        wait = Math.min(Math.max(wait, 1), CFG.maxWaitPerTry);
        if (attempt >= 4 || elapsed() + wait > CFG.totalBudget) return nextProvider();
        return sleepCountdown(wait, hooks.signal, function (left) { hooks.status('waiting', left); }).then(tryOnce);
      });
    }
    return tryOnce();
  }

  /* ---------------------- إجابة محلية عند تعذّر الاتصال تماماً ---------------------- */
  var STOP = {};
  ('ما ماذا كيف هل لماذا متى اين في من على الى عن هذا هذه ذلك تلك التي الذي هو هي انا انت لي لك مع او ثم كل بعض اشرح وضح اريد ممكن يمكن ' +
    'what how why when where which who the a an is are was does do did can could explain this that these those with for and or of to in on about me my you your please').split(' ')
    .forEach(function (w) { STOP[w] = 1; });
  function norm(s) {
    return String(s || '').toLowerCase()
      .replace(/[ً-ٰٟـ]/g, '')
      .replace(/[إأآٱ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه').replace(/ؤ/g, 'و').replace(/ئ/g, 'ي');
  }
  function tokens(s) {
    return norm(s).split(/[^0-9a-z؀-ۿ]+/).map(function (w) {
      return w.replace(/^(وال|بال|كال|فال|لل|ال)(?=..)/, '');
    }).filter(function (w) { return w.length >= 3 && !STOP[w]; });
  }
  function localAnswer(q) {
    var ctx = getContext(), terms = tokens(q), L = [];
    if (/(لخص|لخّص|ملخص|تلخيص|اختصار|summar|tl;?dr|key points)/i.test(q) && ctx.takeaways.length) {
      L.push(T.localIntro, '', '**' + T.localSummary + '**');
      ctx.takeaways.forEach(function (t) { L.push('- ' + t); });
    } else {
      var hits = ctx.passages.map(function (p) {
        var n = norm(p.t), sc = 0;
        terms.forEach(function (w) { if (n.indexOf(w) > -1) sc += p.h ? 0.6 : 1; });
        return { p: p, sc: sc };
      }).filter(function (x) { return x.sc > 0 && !x.p.h; })
        .sort(function (a, b) { return b.sc - a.sc; }).slice(0, 2);
      if (hits.length) {
        L.push(T.localIntro, '');
        hits.forEach(function (x) {
          L.push('> ' + (x.p.t.length > 420 ? x.p.t.slice(0, 420) + '…' : x.p.t), '');
        });
      } else L.push(T.localNone);
    }
    var arts = (state.articles || []).map(function (a) {
      var n = norm(a.t + ' ' + a.d), sc = 0;
      terms.forEach(function (w) { if (n.indexOf(w) > -1) sc++; });
      return { a: a, sc: sc };
    }).filter(function (x) { return x.sc > 0; }).sort(function (x, y) { return y.sc - x.sc; }).slice(0, 3);
    if (arts.length) {
      L.push('', '**' + T.localArticles + '**');
      arts.forEach(function (x) { L.push('- [' + x.a.t + '](' + x.a.u + ')'); });
    }
    L.push('', T.localRetry);
    return L.join('\n');
  }

  /* ------------------------------ عرض Markdown بأمان ------------------------------ */
  function splitSuggestions(t) {
    var s = String(t || ''), sugg = [];
    var m = s.match(/<<([^<>]{2,500})>>?\s*$/);
    if (m) {
      sugg = m[1].split('|').map(function (x) { return x.trim().replace(/^[-•*\d.)\s]+/, ''); })
        .filter(function (x) { return x.length > 1 && x.length < 90; }).slice(0, 3);
      s = s.slice(0, m.index);
    }
    s = s.replace(/<<[^>]*$/, '');   // جزء غير مكتمل أثناء البث
    return { text: s.trim(), suggestions: sugg };
  }

  function inline(s) {
    var codes = [];
    var e = esc(s).replace(/`([^`\n]+)`/g, function (_, c) { codes.push(c); return '\u0000' + (codes.length - 1) + '\u0000'; });
    e = e.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    e = e.replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,!?؟،:]|$)/g, '$1<em>$2</em>');
    e = e.replace(/(^|[\s(])_([^_\n]+)_(?=[\s).,!?؟،:]|$)/g, '$1<em>$2</em>');
    e = e.replace(/\[([^\]\n]+)\]\(([^)\s]+)\)/g, function (_, label, url) {
      var u = url.replace(/&amp;/g, '&');
      if (!/^(https?:\/\/|[\w./-]+\.html?(#[\w-]*)?$)/i.test(u)) return label;
      var ext = /^https?:/i.test(u) && u.indexOf(location.host) === -1;
      return '<a href="' + esc(u) + '"' + (ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + label + '</a>';
    });
    return e.replace(/\u0000(\d+)\u0000/g, function (_, i) { return '<code>' + codes[+i] + '</code>'; });
  }

  function renderBlocks(text) {
    var html = '', list = null, para = [], quote = [];
    function flushPara() { if (para.length) { html += '<p>' + inline(para.join('\n')).replace(/\n/g, '<br>') + '</p>'; para = []; } }
    function flushList() { if (list) { html += '</' + list + '>'; list = null; } }
    function flushQuote() { if (quote.length) { html += '<blockquote>' + inline(quote.join('\n')).replace(/\n/g, '<br>') + '</blockquote>'; quote = []; } }
    text.split('\n').forEach(function (line) {
      var m;
      if (/^\s*$/.test(line)) { flushPara(); flushList(); flushQuote(); return; }
      if ((m = line.match(/^\s*>\s?(.*)$/))) { flushPara(); flushList(); quote.push(m[1]); return; }
      flushQuote();
      if ((m = line.match(/^\s*#{1,6}\s+(.*)$/))) { flushPara(); flushList(); html += '<p class="ntc-h">' + inline(m[1]) + '</p>'; return; }
      if ((m = line.match(/^\s*(?:[-*•]|\d+[.)])\s+(.*)$/))) {
        flushPara();
        var type = /^\s*\d/.test(line) ? 'ol' : 'ul';
        if (list !== type) { flushList(); html += '<' + type + '>'; list = type; }
        html += '<li>' + inline(m[1]) + '</li>'; return;
      }
      flushList(); para.push(line);
    });
    flushPara(); flushList(); flushQuote();
    return html;
  }

  function renderMarkdown(src) {
    var parts = String(src || '').split('```'), out = '';
    for (var i = 0; i < parts.length; i++) {
      if (i % 2 === 1) {
        var code = parts[i], nl = code.indexOf('\n'), lang = '';
        if (nl > -1 && /^[\w+#.-]{0,20}$/.test(code.slice(0, nl).trim())) { lang = code.slice(0, nl).trim(); code = code.slice(nl + 1); }
        out += '<div class="ntc-code"><div class="ntc-code-bar"><span>' + esc(lang || 'code') +
          '</span><button type="button" class="ntc-copy-code">' + T.copy + '</button></div><pre dir="ltr"><code>' +
          esc(code.replace(/\n$/, '')) + '</code></pre></div>';
      } else out += renderBlocks(parts[i]);
    }
    return out;
  }

  /* ------------------------------ الواجهة ------------------------------ */
  var CSS = [
    '#nt-ai-wrapper{display:none!important}',
    '#ntc-root{--ntc-bg:var(--bg-card,#151f32);--ntc-elev:var(--bg-elevated,#1e293b);--ntc-border:var(--card-border,#26354d);--ntc-text:var(--text-main,#f8fafc);--ntc-muted:var(--text-muted,#94a3b8);--ntc-accent:var(--accent,#3b82f6);--ntc-head:var(--heading-color,#60a5fa);font-family:inherit;line-height:1.6;color:var(--ntc-text)}',
    '#ntc-root *{box-sizing:border-box}',
    '#ntc-root button{font-family:inherit}',
    '#ntc-fab{position:fixed;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:2147483000;display:inline-flex;align-items:center;justify-content:center;gap:8px;height:52px;padding:0 18px;border-radius:26px;border:1px solid rgba(255,255,255,.14);background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:700;font-size:14px;cursor:pointer;box-shadow:0 10px 28px rgba(37,99,235,.42);transition:transform .2s,box-shadow .2s,opacity .2s}',
    '#ntc-root[dir=rtl] #ntc-fab{left:16px}#ntc-root[dir=ltr] #ntc-fab{right:16px}',
    '#ntc-fab:hover{transform:translateY(-2px);box-shadow:0 14px 34px rgba(37,99,235,.55)}',
    '#ntc-fab .ntc-fab-ico{font-size:19px;line-height:1}',
    '#ntc-fab.ntc-unread::after{content:"";position:absolute;top:6px;inset-inline-end:6px;width:11px;height:11px;border-radius:50%;background:#10b981;border:2px solid #fff}',
    '#ntc-root.ntc-open #ntc-fab{opacity:0;pointer-events:none;transform:scale(.85)}',
    '#ntc-panel{position:fixed;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:2147483001;width:390px;max-width:calc(100vw - 32px);height:min(620px,calc(100vh - 40px));display:flex;flex-direction:column;background:var(--ntc-bg);border:1px solid var(--ntc-border);border-radius:18px;box-shadow:0 24px 60px rgba(0,0,0,.45);overflow:hidden;animation:ntc-pop .22s ease-out}',
    '#ntc-root[dir=rtl] #ntc-panel{left:16px;transform-origin:bottom left}#ntc-root[dir=ltr] #ntc-panel{right:16px;transform-origin:bottom right}',
    '#ntc-panel[hidden]{display:none}',
    '@keyframes ntc-pop{from{opacity:0;transform:translateY(12px) scale(.97)}to{opacity:1;transform:none}}',
    '.ntc-head{display:flex;align-items:center;gap:10px;padding:12px 14px;background:var(--ntc-elev);border-bottom:1px solid var(--ntc-border)}',
    '.ntc-avatar{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-size:19px;flex:none}',
    '.ntc-meta{flex:1;min-width:0}',
    '.ntc-title{font-weight:800;font-size:15px;color:var(--ntc-head);line-height:1.3}',
    '.ntc-status{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ntc-muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.ntc-dot{width:8px;height:8px;border-radius:50%;background:#10b981;flex:none;box-shadow:0 0 6px #10b981}',
    '.ntc-dot.ntc-busy{background:var(--ntc-accent);box-shadow:0 0 6px var(--ntc-accent);animation:ntc-pulse 1s infinite}',
    '.ntc-dot.ntc-wait{background:#f59e0b;box-shadow:0 0 6px #f59e0b}',
    '@keyframes ntc-pulse{50%{opacity:.35}}',
    '.ntc-icon-btn{width:34px;height:34px;border-radius:10px;border:1px solid var(--ntc-border);background:transparent;color:var(--ntc-muted);cursor:pointer;display:grid;place-items:center;font-size:15px;flex:none}',
    '.ntc-icon-btn:hover{color:var(--ntc-text);background:var(--ntc-bg)}',
    '.ntc-ctx{padding:7px 14px;font-size:12px;color:var(--ntc-muted);border-bottom:1px solid var(--ntc-border);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.ntc-ctx b{color:var(--ntc-text);font-weight:600}',
    '.ntc-msgs{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:12px;overscroll-behavior:contain;scroll-behavior:smooth}',
    '.ntc-msg{display:flex;flex-direction:column;max-width:90%;animation:ntc-in .18s ease-out}',
    '@keyframes ntc-in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}',
    '.ntc-user{align-self:flex-end}.ntc-bot{align-self:flex-start}',
    '.ntc-bubble{padding:10px 13px;border-radius:14px;font-size:14.5px;line-height:1.75;overflow-wrap:anywhere}',
    '.ntc-bot .ntc-bubble{background:var(--ntc-elev);border:1px solid var(--ntc-border);color:var(--ntc-text);border-start-start-radius:4px}',
    '.ntc-user .ntc-bubble{background:var(--ntc-accent);color:#fff;border-start-end-radius:4px;white-space:pre-wrap}',
    '.ntc-bubble p{margin:0 0 .55em}.ntc-bubble p:last-child{margin-bottom:0}',
    '.ntc-bubble .ntc-h{font-weight:800;color:var(--ntc-head)}',
    '.ntc-bubble ul,.ntc-bubble ol{margin:.2em 0 .6em;padding-inline-start:1.3em}.ntc-bubble li{margin:.15em 0}',
    '.ntc-bubble a{color:var(--ntc-head);font-weight:700;text-decoration:underline;text-underline-offset:3px}',
    '.ntc-user .ntc-bubble a{color:#fff}',
    '.ntc-bubble code{background:rgba(127,127,127,.2);padding:1px 6px;border-radius:5px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.88em;direction:ltr;unicode-bidi:isolate}',
    '.ntc-bubble strong{color:var(--ntc-head)}.ntc-user .ntc-bubble strong{color:#fff}',
    '.ntc-bubble blockquote{margin:.3em 0 .6em;padding:6px 10px;border-inline-start:3px solid var(--ntc-accent);background:rgba(59,130,246,.08);border-radius:6px;color:var(--ntc-text)}',
    '.ntc-code{margin:.5em 0;border-radius:10px;overflow:hidden;border:1px solid #334155;background:#070b14}',
    '.ntc-code-bar{display:flex;justify-content:space-between;align-items:center;padding:4px 10px;background:#111a2e;color:#94a3b8;font-size:11.5px;direction:ltr}',
    '.ntc-code-bar button{background:none;border:1px solid #334155;color:#cbd5e1;border-radius:6px;padding:1px 8px;font-size:11px;cursor:pointer}',
    '.ntc-code pre{margin:0;padding:10px 12px;overflow-x:auto;text-align:left;color:#e2e8f0;font-size:12.5px;line-height:1.55}',
    '.ntc-code pre code{background:none;padding:0;font-size:inherit}',
    '.ntc-tools{display:flex;gap:4px;margin-top:4px}',
    '.ntc-tools button{background:none;border:none;color:var(--ntc-muted);font-size:12px;padding:3px 7px;border-radius:7px;cursor:pointer}',
    '.ntc-tools button:hover{background:var(--ntc-elev);color:var(--ntc-text)}',
    '.ntc-typing{display:inline-flex;gap:4px;vertical-align:middle;margin-inline-end:6px}',
    '.ntc-typing i{width:7px;height:7px;border-radius:50%;background:var(--ntc-head);animation:ntc-bounce 1.2s infinite}',
    '.ntc-typing i:nth-child(2){animation-delay:.15s}.ntc-typing i:nth-child(3){animation-delay:.3s}',
    '@keyframes ntc-bounce{0%,60%,100%{transform:translateY(0);opacity:.45}30%{transform:translateY(-5px);opacity:1}}',
    '.ntc-typing-label{font-size:12.5px;color:var(--ntc-muted)}',
    '.ntc-caret{display:inline-block;width:7px;height:1em;background:var(--ntc-head);vertical-align:-2px;margin-inline-start:2px;animation:ntc-pulse .8s infinite}',
    '.ntc-chips{display:flex;gap:6px;padding:8px 12px;overflow-x:auto;border-top:1px solid var(--ntc-border);scrollbar-width:none}',
    '.ntc-chips::-webkit-scrollbar{display:none}',
    '.ntc-chips:empty{display:none}',
    '.ntc-chip{flex:none;background:rgba(59,130,246,.12);color:var(--ntc-head);border:1px solid rgba(59,130,246,.35);border-radius:18px;padding:6px 12px;font-size:12.5px;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s}',
    '.ntc-chip:hover{background:var(--ntc-accent);color:#fff}',
    '.ntc-form{display:flex;align-items:flex-end;gap:8px;padding:10px 12px;border-top:1px solid var(--ntc-border);background:var(--ntc-elev)}',
    '.ntc-form textarea{flex:1;resize:none;min-height:42px;max-height:120px;padding:10px 12px;border-radius:12px;border:1px solid var(--ntc-border);background:var(--ntc-bg);color:var(--ntc-text);font:inherit;font-size:16px;line-height:1.45;outline:none}',
    '.ntc-form textarea:focus{border-color:var(--ntc-accent)}',
    '.ntc-send{width:42px;height:42px;border-radius:12px;border:none;background:var(--ntc-accent);color:#fff;cursor:pointer;display:grid;place-items:center;flex:none}',
    '.ntc-send svg{width:19px;height:19px}',
    '#ntc-root[dir=rtl] .ntc-send svg{transform:scaleX(-1)}',
    '.ntc-send.ntc-stop{background:#ef4444}',
    '.ntc-foot{padding:4px 12px 8px;font-size:10.5px;color:var(--ntc-muted);text-align:center;background:var(--ntc-elev)}',
    '#ntc-ask{position:fixed;z-index:2147483002;padding:8px 14px;border-radius:20px;border:none;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:700;font-size:13px;box-shadow:0 8px 22px rgba(0,0,0,.35);cursor:pointer;transform:translateX(-50%)}',
    '#ntc-ask[hidden],#ntc-nudge[hidden]{display:none}',
    '#ntc-nudge{position:fixed;bottom:calc(78px + env(safe-area-inset-bottom,0px));z-index:2147483000;max-width:250px;padding:10px 32px 10px 12px;border-radius:14px;background:var(--ntc-bg);border:1px solid var(--ntc-border);color:var(--ntc-text);font-size:13px;box-shadow:0 10px 26px rgba(0,0,0,.35);cursor:pointer;animation:ntc-in .25s ease-out}',
    '#ntc-root[dir=rtl] #ntc-nudge{left:16px;padding:10px 12px 10px 32px}#ntc-root[dir=ltr] #ntc-nudge{right:16px}',
    '#ntc-nudge button{position:absolute;top:6px;inset-inline-end:6px;background:none;border:none;color:var(--ntc-muted);cursor:pointer;font-size:13px}',
    '@media (max-width:640px){',
    '#ntc-fab{width:54px;height:54px;padding:0;border-radius:50%}#ntc-fab .ntc-fab-label{display:none}#ntc-fab .ntc-fab-ico{font-size:22px}',
    '#ntc-root[dir] #ntc-panel{left:0;right:0;top:0;bottom:0;width:100%;max-width:none;height:100%;border-radius:0;border:none;animation:ntc-in .2s ease-out}',
    '#ntc-root[dir] #ntc-nudge{bottom:calc(82px + env(safe-area-inset-bottom,0px))}',
    '.ntc-msg{max-width:94%}',
    '}',
    'html.ntc-lock,html.ntc-lock body{overflow:hidden!important}',
    '@media (prefers-reduced-motion:reduce){#ntc-root *{animation:none!important;transition:none!important}}'
  ].join('\n');

  var ICON_SEND = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.4 20.4 21 12 3.4 3.6l-.1 6.5L15 12 3.3 13.9z"/></svg>';
  var ICON_STOP = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';

  var el = {};
  function build() {
    if (state.built) return;
    state.built = true;
    var st = document.createElement('style'); st.id = 'ntc-style'; st.textContent = CSS;
    document.head.appendChild(st);

    var root = document.createElement('div');
    root.id = 'ntc-root'; root.setAttribute('dir', DIR); root.setAttribute('lang', IS_EN ? 'en' : 'ar');
    var ctx = getContext();
    root.innerHTML =
      '<button id="ntc-fab" type="button" aria-label="' + esc(T.fab) + '" aria-expanded="false" aria-controls="ntc-panel">' +
      '<span class="ntc-fab-ico">✨</span><span class="ntc-fab-label">' + esc(T.fab) + '</span></button>' +
      '<div id="ntc-nudge" hidden role="status"><span></span><button type="button" aria-label="' + esc(T.close) + '">✕</button></div>' +
      '<section id="ntc-panel" hidden role="dialog" aria-label="' + esc(T.title) + '">' +
      '<div class="ntc-head"><div class="ntc-avatar" aria-hidden="true">✨</div>' +
      '<div class="ntc-meta"><div class="ntc-title">' + esc(T.title) + '</div>' +
      '<div class="ntc-status"><span class="ntc-dot"></span><span class="ntc-status-text">' + esc(T.ready) + '</span></div></div>' +
      '<button type="button" class="ntc-icon-btn" data-act="new" title="' + esc(T.newChat) + '" aria-label="' + esc(T.newChat) + '">↺</button>' +
      '<button type="button" class="ntc-icon-btn" data-act="close" title="' + esc(T.close) + '" aria-label="' + esc(T.close) + '">✕</button></div>' +
      (ctx.isPost ? '<div class="ntc-ctx">📄 ' + esc(T.ctx) + ' <b>' + esc(ctx.title) + '</b></div>' : '') +
      '<div class="ntc-msgs" aria-live="polite"></div>' +
      '<div class="ntc-chips"></div>' +
      '<form class="ntc-form"><textarea rows="1" placeholder="' + esc(T.placeholder) + '" aria-label="' + esc(T.placeholder) + '" maxlength="2000"></textarea>' +
      '<button type="submit" class="ntc-send" aria-label="' + esc(T.send) + '">' + ICON_SEND + '</button></form>' +
      '<div class="ntc-foot">' + esc(T.disclaimer) + '</div></section>' +
      '<button id="ntc-ask" type="button" hidden>' + esc(T.askSel) + '</button>';
    document.body.appendChild(root);

    el.root = root;
    el.fab = root.querySelector('#ntc-fab');
    el.panel = root.querySelector('#ntc-panel');
    el.msgs = root.querySelector('.ntc-msgs');
    el.chips = root.querySelector('.ntc-chips');
    el.form = root.querySelector('.ntc-form');
    el.input = root.querySelector('textarea');
    el.send = root.querySelector('.ntc-send');
    el.dot = root.querySelector('.ntc-dot');
    el.status = root.querySelector('.ntc-status-text');
    el.ask = root.querySelector('#ntc-ask');
    el.nudge = root.querySelector('#ntc-nudge');

    el.fab.addEventListener('click', function () { state.open ? close() : open(); });
    root.querySelector('[data-act=close]').addEventListener('click', close);
    root.querySelector('[data-act=new]').addEventListener('click', newChat);
    el.form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (state.busy) { stop(); return; }
      var v = el.input.value; el.input.value = ''; autosize(); send(v);
    });
    el.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && !isMobile()) { e.preventDefault(); el.form.requestSubmit ? el.form.requestSubmit() : el.form.dispatchEvent(new Event('submit', { cancelable: true })); }
    });
    el.input.addEventListener('input', autosize);
    el.chips.addEventListener('click', function (e) {
      var b = e.target.closest('.ntc-chip'); if (b && !state.busy) send(b.getAttribute('data-q'));
    });
    el.msgs.addEventListener('click', onMsgsClick);
    el.nudge.addEventListener('click', function (e) {
      el.nudge.hidden = true;
      if (!e.target.closest('button')) open();
    });
    el.ask.addEventListener('mousedown', function (e) { e.preventDefault(); });
    el.ask.addEventListener('click', function () {
      var txt = el.ask.getAttribute('data-sel') || '';
      el.ask.hidden = true;
      if (txt) { open(); send(T.selPrompt(txt)); }
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && state.open) close(); });
    document.addEventListener('selectionchange', debounce(onSelection, 250));
    if (window.visualViewport) {
      visualViewport.addEventListener('resize', fitViewport);
      visualViewport.addEventListener('scroll', fitViewport);
    }
  }

  function debounce(fn, ms) { var t; return function () { clearTimeout(t); t = setTimeout(fn, ms); }; }

  function fitViewport() {
    if (!state.open || !isMobile() || !window.visualViewport) { if (el.panel) { el.panel.style.height = ''; el.panel.style.top = ''; } return; }
    el.panel.style.height = visualViewport.height + 'px';
    el.panel.style.top = visualViewport.offsetTop + 'px';
    scrollBottom(true);
  }

  function autosize() {
    el.input.style.height = 'auto';
    el.input.style.height = Math.min(el.input.scrollHeight, 120) + 'px';
  }

  function setStatus(kind, n) {
    el.dot.className = 'ntc-dot' + (kind === 'waiting' ? ' ntc-wait' : (kind === 'ready' ? '' : ' ntc-busy'));
    var label = kind === 'waiting' ? T.waiting(n) : (T[kind] || T.ready);
    el.status.textContent = label;
    var tl = el.msgs.querySelector('.ntc-pending .ntc-typing-label');
    if (tl) tl.textContent = label;
  }

  function setBusy(b) {
    state.busy = b;
    el.send.classList.toggle('ntc-stop', b);
    el.send.innerHTML = b ? ICON_STOP : ICON_SEND;
    el.send.setAttribute('aria-label', b ? T.stop : T.send);
    if (!b) setStatus('ready');
  }

  function nearBottom() { return el.msgs.scrollHeight - el.msgs.scrollTop - el.msgs.clientHeight < 90; }
  function scrollBottom(force) { if (force || nearBottom()) el.msgs.scrollTop = el.msgs.scrollHeight; }

  function msgNode(role) {
    var w = document.createElement('div');
    w.className = 'ntc-msg ' + (role === 'user' ? 'ntc-user' : 'ntc-bot');
    w.innerHTML = '<div class="ntc-bubble"></div>';
    el.msgs.appendChild(w);
    return w;
  }

  function addTools(node, idx, isLast) {
    var tools = document.createElement('div');
    tools.className = 'ntc-tools';
    tools.innerHTML = '<button type="button" class="ntc-copy" data-i="' + idx + '">📋 ' + esc(T.copy) + '</button>' +
      (isLast ? '<button type="button" class="ntc-retry">↻ ' + esc(T.retry) + '</button>' : '');
    node.appendChild(tools);
  }

  function renderBot(node, raw, partial) {
    var s = splitSuggestions(raw);
    node.querySelector('.ntc-bubble').innerHTML = renderMarkdown(s.text) + (partial ? '<span class="ntc-caret"></span>' : '');
  }

  function contextChips() {
    var ctx = getContext();
    if (!ctx.isPost) return T.chipsHome.slice();
    var c = T.chipsPost.slice();
    if (ctx.code) c.splice(1, 0, T.chipCode);
    return c;
  }

  function setChips(list) {
    el.chips.innerHTML = (list || []).map(function (q) {
      return '<button type="button" class="ntc-chip" data-q="' + esc(q) + '">' + esc(q) + '</button>';
    }).join('');
    el.chips.scrollLeft = 0;
  }

  function renderAll() {
    el.msgs.innerHTML = '';
    var ctx = getContext();
    var w = msgNode('bot');
    w.querySelector('.ntc-bubble').innerHTML = renderMarkdown(ctx.isPost ? T.welcomePost(ctx.title) : T.welcomeHome);
    var lastBot = -1;
    state.history.forEach(function (m, i) { if (m.role === 'assistant') lastBot = i; });
    state.history.forEach(function (m, i) {
      var n = msgNode(m.role === 'user' ? 'user' : 'bot');
      if (m.role === 'user') n.querySelector('.ntc-bubble').textContent = m.content;
      else { renderBot(n, m.content, false); addTools(n, i, i === lastBot && i === state.history.length - 1); }
    });
    var last = state.history[state.history.length - 1];
    if (last && last.role === 'assistant') {
      var sg = splitSuggestions(last.content).suggestions;
      setChips(sg.length ? sg : contextChips().slice(0, 3));
    } else setChips(contextChips());
    scrollBottom(true);
  }

  function onMsgsClick(e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.classList.contains('ntc-copy-code')) {
      copyText(b.closest('.ntc-code').querySelector('code').textContent, b);
    } else if (b.classList.contains('ntc-copy')) {
      var m = state.history[+b.getAttribute('data-i')];
      if (m) copyText(splitSuggestions(m.content).text, b);
    } else if (b.classList.contains('ntc-retry')) {
      regenerate();
    }
  }

  function copyText(txt, btn) {
    var old = btn.innerHTML;
    function ok() { btn.textContent = T.copied; setTimeout(function () { btn.innerHTML = old; }, 1400); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, function () { });
    else {
      var ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); ok(); } catch (e) { } document.body.removeChild(ta);
    }
  }

  function typewriter(node, full) {
    return new Promise(function (resolve) {
      if (reducedMotion() || full.length < 40) { renderBot(node, full, false); resolve(); return; }
      var i = 0, step = Math.max(3, Math.ceil(full.length / 80));
      node.addEventListener('click', function skip() { i = full.length; }, { once: true });
      (function tick() {
        i = Math.min(full.length, i + step);
        renderBot(node, full.slice(0, i), i < full.length);
        scrollBottom();
        if (i < full.length) state.anim = requestAnimationFrame(tick); else resolve();
      })();
    });
  }

  /* ------------------------------ منطق المحادثة ------------------------------ */
  function send(text) {
    text = String(text || '').trim();
    if (!text || state.busy) return;
    if (!state.open) open();
    state.history.push({ role: 'user', content: text.slice(0, 2000) });
    save();
    var lastTools = el.msgs.querySelector('.ntc-retry'); if (lastTools) lastTools.remove();
    var n = msgNode('user'); n.querySelector('.ntc-bubble').textContent = text;
    scrollBottom(true);
    runAssistant();
  }

  function regenerate() {
    if (state.busy) return;
    while (state.history.length && state.history[state.history.length - 1].role === 'assistant') state.history.pop();
    var last = state.history[state.history.length - 1];
    if (!last || last.role !== 'user') return;
    save(); renderAll(); runAssistant();
  }

  function runAssistant() {
    setBusy(true);
    setChips([]);
    state.partial = '';
    var node = msgNode('bot');
    node.classList.add('ntc-pending');
    node.querySelector('.ntc-bubble').innerHTML = '<span class="ntc-typing"><i></i><i></i><i></i></span><span class="ntc-typing-label">' + esc(T.thinking) + '</span>';
    scrollBottom(true);
    var ctrl = new AbortController(); state.controller = ctrl;
    var fullText = null, streamed = false, raf = 0, done = false;

    var hooks = {
      signal: ctrl.signal,
      status: function (kind, n) { if (!streamed) setStatus(kind, n); },
      delta: function (txt, isFull) {
        state.partial = txt;
        if (isFull) { fullText = txt; return; }
        if (!streamed) { streamed = true; node.classList.remove('ntc-pending'); setStatus('writing'); }
        if (!raf && !done) raf = requestAnimationFrame(function () { raf = 0; if (!done) { renderBot(node, state.partial, true); scrollBottom(); } });
      }
    };

    ensureArticles().then(function () {
      return generate(buildMessages(), hooks);
    }).then(function (reply) {
      done = true;
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      node.classList.remove('ntc-pending');
      setStatus('writing');
      return (fullText && !streamed ? typewriter(node, reply) : Promise.resolve(renderBot(node, reply, false))).then(function () { return reply; });
    }).then(function (reply) {
      finish(node, reply, false);
    }).catch(function (e) {
      done = true;
      if (raf) cancelAnimationFrame(raf);
      node.classList.remove('ntc-pending');
      if (isAbort(e)) {
        if (state.partial && state.partial.length > 10) finish(node, splitSuggestions(state.partial).text + '\n\n' + T.stopped, false);
        else { node.remove(); setBusy(false); setChips(contextChips()); }
        return;
      }
      if (window.console) console.warn('[NeuralTech Chat]', e && (e.message || e));
      finish(node, localAnswer(lastUserText()), true);
    });
  }

  function lastUserText() {
    for (var i = state.history.length - 1; i >= 0; i--) if (state.history[i].role === 'user') return state.history[i].content;
    return '';
  }

  function finish(node, content, isLocal) {
    renderBot(node, content, false);
    state.history.push(isLocal ? { role: 'assistant', content: content, local: true } : { role: 'assistant', content: content });
    save();
    addTools(node, state.history.length - 1, true);
    var sg = splitSuggestions(content).suggestions;
    setChips(sg.length ? sg : contextChips().slice(0, 3));
    setBusy(false);
    state.controller = null;
    if (!state.open) el.fab.classList.add('ntc-unread');
    scrollBottom();
  }

  function stop() { if (state.controller) state.controller.abort(); }

  function newChat() {
    stop();
    state.history = []; save();
    renderAll();
    if (!isMobile()) el.input.focus();
  }

  function open() {
    build();
    if (state.open) return;
    state.open = true;
    el.panel.hidden = false;
    el.root.classList.add('ntc-open');
    el.fab.setAttribute('aria-expanded', 'true');
    el.fab.classList.remove('ntc-unread');
    el.nudge.hidden = true;
    try { sessionStorage.setItem('ntc_seen', '1'); } catch (e) { }
    if (isMobile()) document.documentElement.classList.add('ntc-lock');
    if (!el.msgs.childElementCount) renderAll();
    fitViewport();
    scrollBottom(true);
    ensureArticles();
    if (!isMobile()) setTimeout(function () { el.input.focus(); }, 60);
  }

  function close() {
    if (!state.open) return;
    state.open = false;
    el.panel.hidden = true;
    el.root.classList.remove('ntc-open');
    el.fab.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('ntc-lock');
    el.panel.style.height = ''; el.panel.style.top = '';
    el.fab.focus({ preventScroll: true });
  }

  /* ---------------------- "اسأل عن هذا" عند تحديد نص في المقال ---------------------- */
  function onSelection() {
    if (!el.ask) return;
    var sel = window.getSelection ? window.getSelection() : null;
    var txt = sel ? clean(sel.toString()) : '';
    var node = sel && sel.anchorNode ? (sel.anchorNode.nodeType === 1 ? sel.anchorNode : sel.anchorNode.parentElement) : null;
    var inArticle = node && node.closest && node.closest('.post-card, .post-content, .takeaways-box, article') && !node.closest('#ntc-root');
    if (!inArticle || txt.length < 6 || txt.length > 700 || sel.rangeCount === 0) { el.ask.hidden = true; return; }
    el.ask.setAttribute('data-sel', txt);
    if (isMobile()) {
      el.ask.style.left = '50%'; el.ask.style.top = ''; el.ask.style.bottom = 'calc(84px + env(safe-area-inset-bottom,0px))';
    } else {
      var r = sel.getRangeAt(0).getBoundingClientRect();
      var top = r.bottom + 10; if (top > window.innerHeight - 50) top = Math.max(10, r.top - 46);
      el.ask.style.bottom = ''; el.ask.style.top = top + 'px';
      el.ask.style.left = Math.min(window.innerWidth - 90, Math.max(90, r.left + r.width / 2)) + 'px';
    }
    el.ask.hidden = false;
  }

  /* ------------------------------ التهيئة ------------------------------ */
  function init() {
    load();
    build();
    if (state.history.length && state.history[state.history.length - 1].role === 'user') {
      // آخر سؤال بقي بلا رد (أُغلقت الصفحة أثناء التوليد): نزيله كي لا يربك السياق
      state.history.pop(); save();
    }
    var ctx = getContext();
    var seen = false; try { seen = !!sessionStorage.getItem('ntc_seen'); } catch (e) { }
    if (ctx.isPost && !seen) {
      setTimeout(function () {
        if (state.open || seen) return;
        el.nudge.querySelector('span').textContent = T.nudge;
        el.nudge.hidden = false;
        try { sessionStorage.setItem('ntc_seen', '1'); } catch (e) { }
        setTimeout(function () { el.nudge.hidden = true; }, 9000);
      }, 9000);
    }
  }

  // واجهة عامة + توافق مع صندوق التعليقات القديم (submitArticleComment)
  window.NTChat = {
    open: open, close: close,
    ask: function (q) { open(); send(q); }
  };
  window.__ntGetSmartReply = function (text) {
    var ctrl = new AbortController();
    return ensureArticles().then(function () {
      return generate([{ role: 'system', content: systemPrompt() }, { role: 'user', content: String(text || '').slice(0, 2000) }],
        { signal: ctrl.signal, status: function () { }, delta: function () { } });
    }).then(function (r) { return splitSuggestions(r).text; }, function () { return localAnswer(text); });
  };
  window.__ntCraftReply = function (text) { return localAnswer(text); };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
