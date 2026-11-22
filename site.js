// Ressamım · küçük etkileşimler: sessiz otomatik oynatma, öğretmen sesi, vitrin sekmeleri, beliren bölümler.
(function () {
  var d = document, kok = d.documentElement;
  kok.classList.remove('js-yok');
  var azHareket = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var gozcu = 'IntersectionObserver' in window;

  // Üst çubuk: kaydırınca alt çizgi.
  var cubuk = d.querySelector('.cubuk');
  var kaydir = function () { if (cubuk) cubuk.classList.toggle('kaydi', window.scrollY > 8); };
  window.addEventListener('scroll', kaydir, { passive: true }); kaydir();

  // Videolar: görünürken sessiz oynar.
  function oynat(v) { if (!v.hidden && !azHareket) { var p = v.play(); if (p) p.catch(function () { v.controls = true; }); } }
  var videolar = d.querySelectorAll('video[data-oto]');
  videolar.forEach(function (v) {
    v.muted = true;
    if (azHareket) { v.controls = true; return; }
    if (gozcu) {
      new IntersectionObserver(function (g) { g.forEach(function (e) { e.isIntersecting ? oynat(v) : v.pause(); }); }, { threshold: 0.35 }).observe(v);
    } else { oynat(v); }
  });

  // Öğretmen sesi: dersi baştan sesli oynatır.
  d.querySelectorAll('[data-ses]').forEach(function (b) {
    var v = d.getElementById(b.getAttribute('data-ses'));
    var yazi = b.querySelector('.yazi');
    b.addEventListener('click', function () {
      var ac = v.muted;
      v.muted = !ac;
      if (ac) { v.currentTime = 0; var p = v.play(); if (p) p.catch(function () {}); }
      yazi.textContent = b.getAttribute(ac ? 'data-kapali' : 'data-acik');
      b.setAttribute('aria-pressed', ac ? 'true' : 'false');
    });
  });

  // Vitrin: sekme seçilince yanındaki telefonda o bölümün videosu oynar.
  var sekmeler = Array.prototype.slice.call(d.querySelectorAll('.sekme'));
  function sec(s, odak) {
    sekmeler.forEach(function (x) {
      var secili = x === s;
      x.setAttribute('aria-selected', secili ? 'true' : 'false');
      x.parentNode.classList.toggle('secili', secili);
      x.tabIndex = secili ? 0 : -1;
      var v = d.getElementById(x.getAttribute('aria-controls'));
      v.hidden = !secili;
      if (secili) { v.currentTime = 0; oynat(v); } else { v.pause(); }
    });
    if (odak) s.focus();
  }
  sekmeler.forEach(function (s, i) {
    s.addEventListener('click', function () { sec(s); });
    s.addEventListener('keydown', function (e) {
      var k = e.key, n = sekmeler.length, j = -1;
      if (k === 'ArrowDown' || k === 'ArrowRight') j = (i + 1) % n;
      if (k === 'ArrowUp' || k === 'ArrowLeft') j = (i - 1 + n) % n;
      if (k === 'Home') j = 0;
      if (k === 'End') j = n - 1;
      if (j >= 0) { e.preventDefault(); sec(sekmeler[j], true); }
    });
  });

  // Bölümler kaydırdıkça belirir.
  var belirler = d.querySelectorAll('.belir');
  if (gozcu && !azHareket) {
    var g = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('goster'); g.unobserve(e.target); } });
    }, { threshold: 0.12 });
    belirler.forEach(function (b) { g.observe(b); });
  } else { belirler.forEach(function (b) { b.classList.add('goster'); }); }

  // Dil menüsü: dışarı tıklayınca kapanır.
  var dil = d.querySelector('.dil');
  d.addEventListener('click', function (e) { if (dil && dil.open && !dil.contains(e.target)) dil.open = false; });
})();
