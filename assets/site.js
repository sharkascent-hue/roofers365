/* Roofers 365 — site behaviour and quote forms */
(function () {
  'use strict';

  var CFG = {
    formEndpoint: 'https://api.web3forms.com/submit',
    phone: '087 393 8096', tel: '+353873938096', whatsapp: '353873938096'
  };

  var root = document.documentElement.getAttribute('data-root') || '';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- mobile menu ---------- */
  var mnav = $('#mnav');
  $$('[data-menu]').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('data-menu') === 'open';
      mnav.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  });

  /* ---------- scroll animations ---------- */
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function mark(el, cls, d) {
    if (!el || el.closest('.hero')) return;
    el.classList.add('rv');
    if (cls) el.classList.add(cls);
    if (d) el.style.setProperty('--d', d + 's');
  }
  $$('.split').forEach(function (sp) {
    var flip = sp.classList.contains('flip');
    Array.prototype.forEach.call(sp.children, function (c, i) {
      if (c.classList.contains('media')) mark(c);
      else mark(c, (i === 0) !== flip ? 'rv-l' : 'rv-r');
    });
  });
  $$('.sec-head').forEach(function (el) { mark(el); });
  [['.grid', ''], ['.gal', 'rv-zoom'], ['.acols', ''], ['.faq', ''], ['.contact-list', 'rv-l'], ['.filters', '']].forEach(function (g) {
    $$(g[0]).forEach(function (box) {
      if (box.closest('.hero')) return;
      Array.prototype.forEach.call(box.children, function (c, i) {
        if (c.tagName === 'SCRIPT') return;
        mark(c, g[1], Math.min(i % 8, 7) * 0.09);
      });
    });
  });
  $$('.cta-band .wrap>*').forEach(function (c, i) { mark(c, i ? '' : 'rv-l', i * 0.15); });
  $$('.prose>*').forEach(function (c) { mark(c); });
  $$('.ftr .cols>*').forEach(function (c, i) { mark(c, '', i * 0.1); });
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
    $$('.rv').forEach(function (el) { io.observe(el); });
  } else { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }

  /* scroll progress bar + gentle hero parallax */
  var bar = document.createElement('div'); bar.className = 'prog'; document.body.appendChild(bar);
  var hbg = $('.hero .slides') || $('.hero .hero-bg'), big = $('.big365'), ticking = false;
  function onScroll() {
    var h = document.documentElement.scrollHeight - innerHeight, y = scrollY;
    bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (!reduce && y < innerHeight * 1.2) {
      if (hbg) hbg.style.translate = '0 ' + (y * 0.3) + 'px';
      if (big) big.style.translate = '0 ' + (y * -0.15) + 'px';
    }
    ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- quote forms ---------- */
  $$('form[data-quote]').forEach(function (f) {
    var msg = $('.fmsg', f), btn = $('button[type=submit]', f);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(f), bad = false;
      ['name', 'phone'].forEach(function (n) {
        var el = f.elements[n]; if (!el) return;
        var v = (el.value || '').trim();
        var ok = n === 'phone' ? v.replace(/\D/g, '').length >= 7 : v.length > 1;
        el.closest('.fld').classList.toggle('err', !ok); if (!ok) bad = true;
      });
      if (bad) { msg.className = 'fmsg bad'; msg.textContent = 'Please add your name and a phone number we can reach you on.'; return; }
      if (d.get('botcheck')) return;
      var em = f.elements.email;
      if (em && em.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())) {
        em.closest('.fld').classList.add('err'); msg.className = 'fmsg bad'; msg.textContent = 'That email address does not look right. Fix it or leave it blank.'; return;
      }
      if (em) em.closest('.fld').classList.remove('err');
      d.set('subject', 'New quote request: ' + (d.get('service') || 'Website enquiry') + ' (' + (d.get('area') || 'area not given') + ')');
      d.delete('botcheck');
      d.append('page', location.pathname);
      var t = 'Hi Roofers 365, I would like a quote.\nName: ' + d.get('name') + '\nPhone: ' + d.get('phone') +
        '\nArea: ' + (d.get('area') || '') + '\nService: ' + (d.get('service') || '') + '\n' + (d.get('message') || '');
      var fail = function () {
        btn.disabled = false; btn.innerHTML = label;
        msg.className = 'fmsg bad';
        msg.innerHTML = 'Sorry, that did not send. Please call <a href="tel:' + CFG.tel + '">' + CFG.phone + '</a> or <a target="_blank" rel="noopener" href="https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(t) + '">send it by WhatsApp</a>.';
      };
      var label = btn.innerHTML;
      if (!d.get('access_key')) { fail(); return; }
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(CFG.formEndpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: d })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok || !j.success) throw new Error(j.message || r.status); }); })
        .then(function () { location.href = root + 'thank-you/'; })
        .catch(fail);
    });
  });

  /* ---------- area checker ---------- */
  var ac = $('form[data-area]');
  if (ac) {
    var areas = JSON.parse($('#area-data').textContent), out = $('.acheck-out');
    var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]/g, '').trim(); };
    ac.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = norm(ac.elements.q.value); if (!q) return;
      var hit = null;
      Object.keys(areas).forEach(function (c) { areas[c].forEach(function (a) { if (!hit && (norm(a).indexOf(q) > -1 || q.indexOf(norm(a)) > -1)) hit = [a, c]; }); });
      if (!hit && /^(d(ublin)? ?\d{1,2}w?|dublin|kildare|meath|louth|co ?(dublin|kildare|meath|louth))$/.test(q)) hit = [ac.elements.q.value.trim(), 'our area'];
      if (hit) { out.className = 'acheck-out yes'; out.textContent = 'Yes, we cover ' + hit[0] + (hit[1] === 'our area' ? '' : ' (Co. ' + hit[1] + ')') + '. Call ' + CFG.phone + ' or request a free quote.'; }
      else { out.className = 'acheck-out no'; out.textContent = 'We may still cover you. We work across Dublin, Kildare, Meath and Louth, so ring ' + CFG.phone + ' and ask.'; }
    });
  }

  /* ---------- gallery filter + lightbox ---------- */
  $$('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      var c = b.getAttribute('data-f');
      $$('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      $$('.gal .gi').forEach(function (g) { g.hidden = !(c === 'all' || g.getAttribute('data-c') === c); });
    });
  });
  var lb = $('#lb');
  if (lb) {
    var items = [], idx = 0, img = $('img', lb), cap = $('p', lb);
    var show = function (i) {
      idx = (i + items.length) % items.length;
      img.src = items[idx].getAttribute('data-full'); img.alt = items[idx].getAttribute('data-cap') || '';
      cap.textContent = items[idx].getAttribute('data-cap') || '';
    };
    document.addEventListener('click', function (e) {
      var g = e.target.closest && e.target.closest('.gi');
      if (!g) return;
      items = $$('.gi', g.parentNode).filter(function (x) { return !x.hidden; });
      show(items.indexOf(g)); lb.classList.add('open');
    });
    var close = function () { lb.classList.remove('open'); img.src = ''; };
    $('.x', lb).addEventListener('click', close);
    $('.p', lb).addEventListener('click', function () { show(idx - 1); });
    $('.nx', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  var y = $('#yr'); if (y) y.textContent = new Date().getFullYear();
})();
