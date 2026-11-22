/* Silent Service Trading — site helpers (no dependencies) */
(function () {
  'use strict';

  /* Live Stripe payment links (launch 2026 prices: $49 / $500 / $1,999). The ONLY place they're set on the site.
     Changing these changes where customers are charged — get approval first. */
  var BUY = {
    monthly:  'https://buy.stripe.com/6oU4gydih0RP6fo1B4gnK03',
    annual:   'https://buy.stripe.com/3cI3cucedasp9rAgvYgnK04',
    lifetime: 'https://buy.stripe.com/4gM7sKdihbwt33ca7AgnK05',
    nyopen:   'https://buy.stripe.com/fZuaEW4LL8kh33c1B4gnK06'      /* NYOpen $39.99 / month → /automation/thanks/ */
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
      if (url) {
        links[i].setAttribute('href', url);
        /* Checkout opens in a new tab so the pricing page stays open behind it:
           closing the checkout tab is the "cancel". Payment links have no cancel URL. */
        links[i].setAttribute('target', '_blank');
        links[i].setAttribute('rel', 'noopener');
      }
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

  /* Screenshots: click (or Enter / Space) opens the image full screen; click, Esc or × closes it. */
  var zooms = document.querySelectorAll('.zoom');
  if (zooms.length) {
    var box = null, big = null, opener = null;
    var build = function () {
      box = document.createElement('dialog');
      box.className = 'lightbox';
      box.setAttribute('aria-label', 'Enlarged screenshot');
      var close = document.createElement('button');
      close.type = 'button';
      close.className = 'lightbox-close';
      close.setAttribute('aria-label', 'Close');
      close.textContent = '\u00D7';
      big = document.createElement('img');
      big.className = 'lightbox-img';
      box.appendChild(close);
      box.appendChild(big);
      document.body.appendChild(box);
      box.addEventListener('click', function () { box.close(); });          // anywhere, image included, closes
      box.addEventListener('close', function () {
        document.documentElement.classList.remove('lightbox-open');
        if (opener) opener.focus();
      });
    };
    for (var z = 0; z < zooms.length; z++) {
      zooms[z].addEventListener('click', function () {
        var img = this.querySelector('img');
        if (!img) return;
        if (!box) build();
        opener = this;
        big.src = img.currentSrc || img.src;
        big.alt = img.alt;
        if (typeof box.showModal === 'function') {
          document.documentElement.classList.add('lightbox-open');
          box.showModal();
        } else {
          window.open(big.src, '_blank', 'noopener');                        // very old browsers: open the image
        }
      });
    }
  }
})();
