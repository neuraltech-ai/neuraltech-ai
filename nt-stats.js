/*!
 * NeuralTech Stats — عدّاد زيارات حقيقي لموقع نيورال تك (عبر GoatCounter المجاني)
 * ------------------------------------------------------------------------------
 * 1) سجّل مجاناً في https://www.goatcounter.com واختر رمزاً لموقعك (مثلاً neuraltech).
 * 2) في إعدادات الموقع هناك فعّل: «Allow adding visitor counts on your website».
 * 3) ضع الرمز في السطر التالي ثم ادفع التغيير. قبل ذلك لا يظهر أي عدّاد (لا أرقام وهمية).
 */
(function () {
  'use strict';
  var GOATCOUNTER = '';   // مثال: 'neuraltech'

  if (window.__NTS_LOADED__) return;
  window.__NTS_LOADED__ = true;

  function boxes() { return Array.prototype.slice.call(document.querySelectorAll('#nt-stats')); }

  // بقايا العدّاد القديم إن وُجدت في صفحة لم تُحدَّث: نخفيها بدل عرض أرقام غير حقيقية
  var oldA = document.getElementById('nt-active-users');
  if (oldA) {
    var pill = oldA.closest('.telemetry-pill');
    if (pill) pill.style.display = 'none';
  }

  if (!GOATCOUNTER) return;
  var base = 'https://' + GOATCOUNTER + '.goatcounter.com';

  // تسجيل الزيارة (GoatCounter لا يستعمل كوكيز ولا يتتبع الزائر بين المواقع)
  if (!document.querySelector('script[data-goatcounter]')) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://gc.zgo.at/count.js';
    s.setAttribute('data-goatcounter', base + '/count');
    document.head.appendChild(s);
  }

  var list = boxes();
  if (!list.length) return;
  var css = document.createElement('style');
  css.textContent = '#nt-stats{flex-wrap:wrap;row-gap:2px;margin:6px 0}#nt-stats span{white-space:nowrap}';
  document.head.appendChild(css);
  var isEn = /^en/i.test(document.documentElement.lang || '') || /_en\.html?$/i.test(location.pathname);
  var isPost = !!document.querySelector('.post-card, .post-content');

  function get(path) {
    return fetch(base + '/counter/' + path + '.json', { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }
  function esc(x) { return String(x).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  Promise.all([isPost ? get(encodeURIComponent(location.pathname)) : Promise.resolve(null), get('TOTAL')]).then(function (res) {
    var page = res[0] && res[0].count, total = res[1] && res[1].count;
    if (!page && !total) return;
    var parts = [];
    if (page) parts.push('<span>👁️ ' + (isEn ? 'Article views: ' : 'مشاهدات المقال: ') + '<b>' + esc(page) + '</b></span>');
    if (total) parts.push('<span>📈 ' + (isEn ? 'Total site visits: ' : 'إجمالي زيارات الموقع: ') + '<b>' + esc(total) + '</b></span>');
    list.forEach(function (b) { b.innerHTML = parts.join('<span>•</span>'); b.style.display = ''; });
  });
})();
