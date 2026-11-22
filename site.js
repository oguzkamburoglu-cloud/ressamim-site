// Videolar görününce sessiz oynar, ekrandan çıkınca durur. "Sesi aç" öğretmeni baştan dinletir.
(function () {
  var azHareket = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var videolar = document.querySelectorAll('video[data-oto]');

  videolar.forEach(function (v) {
    v.muted = true;
    if (azHareket) { v.controls = true; return; }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (g) {
        g.forEach(function (e) {
          if (e.isIntersecting) { v.play().catch(function () { v.controls = true; }); } else { v.pause(); }
        });
      }, { threshold: 0.4 }).observe(v);
    } else {
      v.play().catch(function () { v.controls = true; });
    }
  });

  document.querySelectorAll('[data-ses]').forEach(function (d) {
    var v = document.getElementById(d.getAttribute('data-ses'));
    var acik = d.getAttribute('data-acik'), kapali = d.getAttribute('data-kapali');
    d.addEventListener('click', function () {
      var ac = v.muted;
      v.muted = !ac;
      if (ac) { v.currentTime = 0; v.play().catch(function () {}); }
      d.querySelector('span').textContent = ac ? kapali : acik;
      d.setAttribute('aria-pressed', ac ? 'true' : 'false');
    });
  });
})();
