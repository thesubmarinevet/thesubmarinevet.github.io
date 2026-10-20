/* Silent Service Trading — site helpers (no dependencies) */
(function () {
  'use strict';

  /* Live Stripe payment links. The ONLY place they're set on the site.
     Changing these changes where customers are charged — get approval first. */
  var BUY = {
    monthly:  'https://buy.stripe.com/28EaEWba9bwtcDM0x0gnK00',
    annual:   'https://buy.stripe.com/14A7sK0vvfMJ6fo3JcgnK01',
    lifetime: 'https://buy.stripe.com/8x2eVca65cAxavEfrUgnK02'
  };

  /* Old in-page anchors from the previous site → their new homes. */
  var path = location.pathname.replace(/index\.html$/, '');
  var hash = location.hash.toLowerCase();
  var moved = {
    '/#about': '/about/',
    '/#follow': '/about/#follow',
    '/#lexicon': '/',
    '/#silent-service': '/command-center/',
    '/#positioning': '/about/',
    '/command-center/#early-access': '/pricing/',
    '/command-center/#faq': '/support/#faq',
    '/command-center/#how': '/support/#getting-started'
  };
  var target = moved[path + hash];
  if (target && target !== path + hash) {
    if (target === '/') { history.replaceState(null, '', '/'); }
    else { location.replace(target); return; }
  }

  document.addEventListener('DOMContentLoaded', function () {
    /* checkout buttons */
    var links = document.querySelectorAll('[data-plan]');
    for (var i = 0; i < links.length; i++) {
      var url = BUY[links[i].getAttribute('data-plan')];
      if (url) links[i].setAttribute('href', url);
    }

    /* footer year */
    var y = document.querySelectorAll('[data-year]');
    for (var j = 0; j < y.length; j++) y[j].textContent = new Date().getFullYear();

    /* mobile menu */
    var btn = document.querySelector('.menu-btn');
    var nav = document.getElementById('site-nav');
    if (btn && nav) {
      btn.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && nav.classList.contains('open')) {
          nav.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          btn.focus();
        }
      });
    }
  });
})();
