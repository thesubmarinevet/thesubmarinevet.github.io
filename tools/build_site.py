#!/usr/bin/env python3
"""Generates the static pages for silentservicetrading.com.
Output is plain HTML committed to the repo; GitHub Pages serves it as-is."""
import json, sys, os

ROOT = sys.argv[1]
SITE = "https://silentservicetrading.com"
EMAIL = "thesubmarineveteran@gmail.com"

import hashlib as _hl, os as _os
def _asset_v():
    h=_hl.sha256()
    for f in ("assets/site.css","assets/site.js"):
        h.update(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", f),"rb").read())
    return h.hexdigest()[:8]
ASSET_V=_asset_v()   # changes whenever site.css / site.js change, so browsers fetch the new copy

LOGO = """<svg class="logo-mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
  <path d="M14 2 H50 L62 14 V50 L50 62 H14 L2 50 V14 Z" fill="#0E0F0C" stroke="#5C6352" stroke-width="2"/>
  <circle cx="32" cy="32" r="21" fill="#17140A" stroke="#F2A900" stroke-opacity="0.45" stroke-width="2.5"/>
  <circle cx="32" cy="32" r="12" fill="none" stroke="#F2A900" stroke-opacity="0.45" stroke-width="2.5"/>
  <path d="M32 11 V53 M11 32 H53" stroke="#F2A900" stroke-opacity="0.25" stroke-width="1.5"/>
  <path d="M32 32 L32 11 A21 21 0 0 1 50.2 21.5 Z" fill="#F2A900" fill-opacity="0.28"/>
  <path d="M32 32 L50.2 21.5" stroke="#F2A900" stroke-width="3.5" stroke-linecap="square"/>
  <rect x="38" y="16" width="5" height="5" fill="#F2A900"/>
</svg>"""

ICONS = {
 "trade": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 17l5-5 4 4 7-8"/><path d="M15 8h5v5"/></svg>',
 "monitor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="M7 12l2.5-3 2.5 2 4-4"/></svg>',
 "plan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6h16M4 12h10M4 18h7"/><circle cx="18" cy="16" r="3"/><path d="M20.2 18.2L22 20"/></svg>',
 "review": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5"/><path d="M9 13h7M9 17h5"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/></svg>',
 "pc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></svg>',
 "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5L16 9.5"/></svg>',
 "nt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19V5l16 14V5"/></svg>',
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>',
}

NAV = [("Home", "/"), ("Features", "/command-center/"), ("Automation", "/automation/"), ("Pricing", "/pricing/"), ("About", "/about/"), ("Support", "/support/")]

DISCLAIMER = ("Silent Service Trading is a software tool, not financial advice. Futures trading involves substantial risk of loss and is not "
              "suitable for every investor. You are responsible for every order placed on your accounts and for following your broker's and "
              "prop firm's rules, including rules on trade copiers and automated trading. Past or hypothetical performance does not guarantee "
              "future results. Test on simulation accounts first.")

def head(title, desc, path, noindex=False, extra=""):
    url = SITE + path
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1220">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Silent Service Trading">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;650;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ASSET_V}">
<script src="/assets/site.js?v={ASSET_V}" defer></script>
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(active):
    links = []
    for name, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        links.append(f'      <a href="{href}"{cur}>{name}</a>')
    links = "\n".join(links)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Silent Service Trading — home">
      {LOGO}
      <span class="logo-text"><strong>Silent Service Trading</strong><span>by The Submarine Vet</span></span>
    </a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
{links}
    </nav>
  </div>
</header>
"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo" href="/" aria-label="Silent Service Trading — home">{LOGO}<span class="logo-text"><strong>Silent Service Trading</strong><span>by The Submarine Vet</span></span></a>
        <p>SST: the risk, copier and journal workspace for NinjaTrader&nbsp;8. Trade, monitor and review every account you run.</p>
      </div>
      <div class="foot-col">
        <h2>Product</h2>
        <ul>
          <li><a href="/command-center/">Features</a></li>
          <li><a href="/automation/">Automation</a></li>
          <li><a href="/command-center/#requirements">Requirements</a></li>
          <li><a href="/pricing/">Pricing</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h2>Company</h2>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/about/#follow">Follow</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h2>Support</h2>
        <ul>
          <li><a href="/support/#getting-started">Getting started</a></li>
          <li><a href="/support/#faq">FAQ</a></li>
          <li><a href="mailto:{EMAIL}">Email support</a></li>
        </ul>
      </div>
    </div>
    <p class="disclaimer">{DISCLAIMER}</p>
    <p class="disclaimer">NinjaTrader is a registered trademark of NinjaTrader Group, LLC. Silent Service Trading is not affiliated with or endorsed by NinjaTrader or any prop firm.</p>
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> The Submarine Vet · Silent Service Trading</span>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</footer>
</body>
</html>
"""

def shot(label, file_hint, alt, bar="Silent Service Trading", eager=False):
    # Real screenshot when /assets/img/<name>.webp exists, otherwise a placeholder frame.
    name = file_hint.rsplit(".", 1)[0]
    img = os.path.join(ROOT, "assets", "img", name + ".webp")
    if os.path.exists(img):
        from PIL import Image
        w, h = Image.open(img).size
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return f"""<figure class="shot shot-real">
  <button class="zoom" type="button" aria-label="Enlarge image: {alt}">
    <img src="/assets/img/{name}.webp" alt="{alt}" width="{w}" height="{h}" {load} decoding="async">
    <span class="zoom-hint" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4M11 8v6M8 11h6"/></svg>Click to enlarge</span>
  </button>
</figure>"""
    return f"""<figure class="shot">
  <div class="shot-bar" aria-hidden="true"><i></i><i></i><i></i><span>{bar}</span></div>
  <!-- SCREENSHOT TO ADD: /assets/img/{name}.webp (1600 px wide, Sim accounts or names blurred) -->
  <div class="shot-placeholder" role="img" aria-label="{alt} (screenshot coming soon)">
    <strong>{label}</strong>
    <span>Screenshot coming soon</span>
  </div>
</figure>"""

def page(path, title, desc, active, body, noindex=False, extra=""):
    out = head(title, desc, path, noindex, extra) + header(active) + '<main id="main">\n' + body + "\n</main>\n" + FOOTER
    dest = os.path.join(ROOT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w").write(out)
    print("wrote", dest)

def badge(kind):
    return {"a": '<span class="badge badge-available">Available</span>',
            "t": '<span class="badge badge-early">In testing</span>',
            "p": '<span class="badge badge-planned">Planned</span>'}[kind]

def feature(title, text, kind):
    return f'<div class="feature"><h3>{title} {badge(kind)}</h3><p>{text}</p></div>'

# ------------------------------------------------------------------ HOME
ld = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Organization", "name": "Silent Service Trading", "url": SITE + "/",
     "parentOrganization": {"@type": "Organization", "name": "The Submarine Vet"},
     "email": EMAIL,
     "sameAs": ["https://x.com/thesubmarinevet", "https://www.youtube.com/@SilentServiceTrading", "https://www.instagram.com/silentservicetrading",
                "https://www.facebook.com/thesubmarinevet", "https://www.tiktok.com/@silentservicetrading", "https://www.threads.net/@silentservicetrading",
                "https://www.tradingview.com/u/thesubmarinevet/"]},
    {"@type": "SoftwareApplication", "name": "Silent Service Trading", "applicationCategory": "FinanceApplication",
     "operatingSystem": "Windows (NinjaTrader 8)", "url": SITE + "/command-center/",
     "offers": [
       {"@type": "Offer", "name": "Monthly", "price": "49.00", "priceCurrency": "USD", "url": SITE + "/pricing/"},
       {"@type": "Offer", "name": "Annual", "price": "500.00", "priceCurrency": "USD", "url": SITE + "/pricing/"},
       {"@type": "Offer", "name": "Lifetime", "price": "1999.00", "priceCurrency": "USD", "url": SITE + "/pricing/"}]}
  ]}
home_ld = '<script type="application/ld+json">' + json.dumps(ld, separators=(",", ":")) + "</script>\n"

pillars = [
 ("trade", "Trade", "Order entry, trims, ATM templates, drag-out stops and targets, and a trade copier that sizes every follower on its own terms.", "/command-center/#trade"),
 ("monitor", "Monitor", "Every account's day at a glance, prop-firm limits and micro caps enforced automatically, and a block on hedging across one firm's accounts.", "/command-center/#monitor"),
 ("plan", "Plan", "Market Read with the levels intraday traders draw by hand, chart tabs and side-by-side charts, and playbooks that alert.", "/command-center/#plan"),
 ("review", "Review", "A trade journal that records itself, net of each firm's fees, with a P&amp;L calendar, per-account views and an equity curve.", "/command-center/#review"),
]
pill_html = "\n".join(f'''      <a class="card" href="{h}">
        <div class="icon">{ICONS[i]}</div>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="more">Explore {t.lower()} &rarr;</span>
      </a>''' for i, t, d, h in pillars)

home = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Silent Service Trading (SST) for NinjaTrader&nbsp;8</p>
      <h1>Command Your Trading.<br><span class="accent">Stay in Control.</span></h1>
      <p class="lead">One integrated NinjaTrader&nbsp;8 workspace for managing trading accounts, monitoring positions, following playbooks, and reviewing performance.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/pricing/">See pricing</a>
        <a class="btn btn-secondary" href="/command-center/">Take the tour</a>
      </div>
      <p class="hero-note">Now available · Runs inside NinjaTrader on your own PC</p>
    </div>
    <div>
{shot("SST workspace", "cc-workspace.png", "SST View Screen: a 5-minute MNQ chart with session, pivot and POC levels beside the Trade Console", eager=True)}
    </div>
  </div>
</section>

<section class="strip" aria-label="Highlights">
  <div class="wrap">
    <ul>
      <li>{ICONS['nt']}Built for NinjaTrader&nbsp;8</li>
      <li>{ICONS['pc']}Runs locally — your logins stay on your PC</li>
      <li>{ICONS['shield']}Prop-firm limits and same-firm hedge checks per account</li>
      <li>{ICONS['hand']}You place every trade</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">One workspace</p>
      <h2>Everything a multi-account trader juggles, in one window.</h2>
      <p>SST brings the four jobs of an active trading day together, so you stop switching between tabs, spreadsheets and dashboards.</p>
    </div>
    <div class="grid-4">
{pill_html}
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Walkthrough</p>
      <h2>How a session runs in SST.</h2>
    </div>

    <div class="row">
      <div>
        <h3>Enter, manage and copy trades from one console.</h3>
        <p>Place the trade once. SST copies it to your follower accounts, each with its own size and limits, and keeps every bracket on the instrument it was placed on.</p>
        <ul class="checks">
          <li>Buy, sell, reverse, close and trim ¼ or ½ in one click</li>
          <li>Use your own NinjaTrader ATM templates</li>
          <li>Copy minis as micros, with contract caps per account</li>
          <li>Step-down rotation: one follower at a time takes the trade</li>
          <li>FLATTEN ALL ACCOUNTS when you need everything closed now</li>
        </ul>
      </div>
{shot("Trade copier", "cc-trade.png", "Copier tab: a lead account copied to several follower accounts, each with its own size, lock and limits (group and account names blurred)")}
    </div>

    <div class="row flip">
      <div>
        <h3>Watch every account, and let the rules enforce themselves.</h3>
        <p>Enter each prop account's limits once. When an account reaches its daily loss or drawdown limit, SST locks it and flattens it — even if you're not watching.</p>
        <ul class="checks">
          <li>Day P&amp;L and balance for every account, sortable</li>
          <li>Drawdown, daily limits and consistency per account</li>
          <li>Max micros per account, enforced on every order</li>
          <li>Blocks a trade that would hedge two accounts at the same firm</li>
        </ul>
      </div>
{shot("Prop-firm rules", "cc-monitor.png", "Prop Rules tab: stage, drawdown, daily limits, room left and status for every account (account names blurred)")}
    </div>

    <div class="row">
      <div>
        <h3>Plan the session, then review it.</h3>
        <p>Market Read puts the day's key levels on the chart. After the close, the journal has already recorded every trade, so review starts with the facts.</p>
        <ul class="checks">
          <li>Prior day, session and opening-range levels, VWAP and POC</li>
          <li>Playbooks that alert and mark the chart — never place orders</li>
          <li>P&amp;L net of fees, a monthly P&amp;L calendar and an equity curve</li>
        </ul>
      </div>
{shot("Trade journal", "cc-plan-review.png", "P&amp;L calendar: net result, trades and wins / losses for each day, with weekly totals (sample data)")}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap founder">
    <div class="founder-mark" aria-hidden="true">
      <svg viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="88" fill="none" stroke="#5B8DB8" stroke-opacity=".18" stroke-width="2"/>
        <circle cx="100" cy="100" r="62" fill="none" stroke="#5B8DB8" stroke-opacity=".32" stroke-width="2"/>
        <circle cx="100" cy="100" r="36" fill="none" stroke="#5B8DB8" stroke-opacity=".55" stroke-width="2"/>
        <path d="M100 100 L162 48" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
        <circle cx="100" cy="100" r="6" fill="#38BDF8"/>
      </svg>
    </div>
    <div>
      <p class="eyebrow">The founder</p>
      <h2>Built by a submarine veteran who trades.</h2>
      <p>On a submarine, you don't steer by feel. You read your instruments, follow procedure and keep the boat inside its limits through long, quiet stretches and sudden ones.</p>
      <p>SST was built by The Submarine Vet for his own futures trading on NinjaTrader — the tool he wanted when running several funded accounts at once. Now it is Silent Service Trading's first product, with more tools to follow.</p>
      <blockquote class="quote">Instruments over instinct.</blockquote>
      <p style="margin-top:24px"><a href="/about/">Read the story &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Pricing</p>
      <h2>Launch pricing.</h2>
      <p>Monthly, annual, or a limited lifetime license. Launch prices are offered through December&nbsp;31, 2026.</p>
    </div>
    <div class="grid-3">
      <div class="card"><h3>Monthly</h3><p class="price">$49<small>/ month</small></p><p class="price-note">Cancel anytime.</p></div>
      <div class="card"><h3>Annual</h3><p class="price">$500<small>/ year</small></p><p class="price-note">$41.67 a month — save $88 (15%).</p></div>
      <div class="card"><h3>Lifetime</h3><p class="price">$1,999<small>once</small></p><p class="price-note">First 25 seats. Includes every automated strategy and playbook.</p></div>
    </div>
    <div class="btn-row" style="justify-content:center;margin-top:32px"><a class="btn btn-primary" href="/pricing/">Compare plans</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <h2>Take command of every account.</h2>
      <p>Set it up on simulation accounts, test your copier group and rules, and go live when you trust it.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/pricing/">Get SST</a>
        <a class="btn btn-secondary" href="/support/#getting-started">How setup works</a>
      </div>
    </div>
  </div>
</section>"""

page("/", "Silent Service Trading (SST) — risk and copier workspace for NinjaTrader 8",
     "Silent Service Trading (SST) for NinjaTrader 8: trade copier, prop-firm rules, Trade Console and a self-filling trade journal for traders running several accounts.",
     "/", home, extra=home_ld)

# ------------------------------------------------------------------ COMMAND CENTER
trade = [
 ("Trade Console", "Buy and sell at market or limit with stop-loss and take-profit in ticks. Reverse, close and cancel from the same panel. Buttons never move — status messages appear below them, so a click always lands where you aim. Remembers the account you trade.", "a"),
 ("Drag-out stop and target", "In a trade with no stop or target? Drag the SL or TP chip off the position line; the preview shows the price and the P&amp;L there. Release to place it — the two cancel each other.", "a"),
 ("One-click trims", "Trim ¼ or ½ of a position in one click, rounded to the nearest contract and always leaving at least one open.", "a"),
 ("ATM integration", "Pick any of your NinjaTrader ATM strategy templates from the console. Brackets and ATM orders stay on the instrument they were placed on, even after you switch to another.", "a"),
 ("Trade copier", "Trade one lead account and copy to followers, each with its own multiplier, maximum contracts and daily loss / profit lock. Copy minis as micros (NQ → MNQ, ES → MES and more). Followers are kept in line with their real positions, and locked followers still follow the lead out of a trade.", "a"),
 ("Flatten all accounts", "One click turns the copier off, cancels every working order and closes every position on every account — and logs what each account held.", "a"),
 ("Step-down rotation", "One follower takes each trade until it reaches its target or loss limit, then the next account takes over, with working exit orders on the follower.", "a"),
 ("Same-firm hedge protection", "A new trade is held back when another account at the same firm holds the opposite side of the same market (NQ and MNQ count as one). Closing a position always goes through. On by default; switch it off in Settings.", "a"),
]
monitor = [
 ("Accounts overview", "Day P&amp;L and balance for every account, sortable by name, P&amp;L or balance. Simulation accounts are kept out of your totals. One click masks account numbers for screen sharing.", "a"),
 ("Prop-firm rules", "Per account: stage, drawdown, daily loss and profit limits, and consistency %. Reach a limit and the account locks and flattens; locks lift at the next trading day. The profit lock counts banked P&amp;L only, so an open winner never locks you out early.", "a"),
 ("Risk fail-safe", "If SST can't read an account's balance, rules or positions, new trades on it wait until it can. A lock already in place is still enforced.", "a"),
 ("Positions and open P&amp;L", "Your position and its open P&amp;L — in dollars, points or both — on the chart's position line and in the console header, plus time in trade and the P&amp;L each stop and target would book if hit.", "a"),
 ("Connection and copier status", "A connection indicator and a COPIER ON / OFF button sit in view at all times, so you know what is live.", "a"),
 ("Automated strategy overview", "See which NinjaTrader strategies are running, on which account and instrument, and whether they are in sync.", "a"),
 ("Max micros per account", "Set the most micros each account may hold (1 mini = 10 micros). It's a hard limit on every order that adds contracts — console, chart, copier and your own strategies.", "a"),
]
plan = [
 ("Market Read", "The session at a glance: key levels with their distance from price, market bias, the opening range and the premarket range.", "a"),
 ("Chart levels", "Prior day high and low, Asia / London / New York session ranges, premarket, 15-minute opening range, VWAP, POC from tick data, daily pivots, fair value gaps and EMAs — drawn for you and updated on every tick.", "a"),
 ("Chart tabs and side-by-side charts", "Keep several charts as tabs, each with its own instrument, bar series, indicators and playbook. Show two side by side or stacked; click a chart to make it the one you trade.", "a"),
 ("Playbooks", "Add playbooks for alerts, chart markers and a playbook panel. Import rule playbooks or install playbook packs. A playbook never places an order — you decide.", "a"),
 ("Playbook Builder", "Build your own setups without code — for example a break of the 15-minute high, then a retest within six bars, after 9:45 ET — with a plain-English preview and past hits on the chart.", "p"),
 ("Alert sounds and phone alerts", "Choose sounds per alert type, and get playbook alerts on your phone through the free ntfy app. Alerts only — no account data is ever sent.", "p"),
]
review = [
 ("Trade Journal", "Every fill is recorded automatically and grouped into round-trip trades, with daily summary tiles, a trades list and fills. Prop connections that report no commission are charged each account's fee rate — learned automatically or typed in — so the journal matches the account.", "a"),
 ("Performance history", "Results by day and by account, with an equity curve. Exclude accounts you trade just for fun from your statistics.", "a"),
 ("P&amp;L calendar", "A month at a glance: each day green or red with net P&amp;L, trades and wins / losses, plus weekly totals. Save or copy it as an image to share.", "a"),
 ("Trade notes", "Add notes to any trade. When one of your automated strategies placed the trade, its name is added for you.", "a"),
]
def cat(id_, icon, title, intro, items):
    feats = "\n".join("        " + feature(*f) for f in items)
    return f"""    <section class="cat" id="{id_}" aria-labelledby="{id_}-h">
      <div class="cat-head">
        <div class="icon">{ICONS[icon]}</div>
        <div><h2 id="{id_}-h">{title}</h2><p>{intro}</p></div>
      </div>
      <div class="feature-list">
{feats}
      </div>
    </section>"""

cc = f"""<section class="page-hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Silent Service Trading (SST)</p>
      <h1>Your whole trading day, in one NinjaTrader workspace.</h1>
      <p class="lead">SST runs inside NinjaTrader&nbsp;8 on your own PC. It doesn't trade for you — it gives you one place to trade, monitor, plan and review every account.</p>
      <div class="btn-row" style="margin-top:28px">
        <a class="btn btn-primary" href="/pricing/">See pricing</a>
        <a class="btn btn-secondary" href="/support/#getting-started">Getting started</a>
      </div>
    </div>
    <div>
{shot("SST workspace", "cc-workspace.png", "SST View Screen with chart levels and the Trade Console", eager=True)}
    </div>
  </div>
</section>

<nav class="subnav" aria-label="Feature categories">
  <div class="wrap">
    <ul>
      <li><a href="#trade">Trade</a></li>
      <li><a href="#monitor">Monitor</a></li>
      <li><a href="#plan">Plan</a></li>
      <li><a href="#review">Review</a></li>
      <li><a href="#requirements">Requirements</a></li>
    </ul>
  </div>
</nav>

<div class="section">
  <div class="wrap">
    <div class="legend" style="margin-bottom:56px">
      <span>{badge('a')} In the current release</span>
      <span>{badge('p')} On the roadmap — not in the current release</span>
    </div>
{cat("trade", "trade", "Trade", "Order entry, position management and ATM integration — plus a trade copier for running several accounts at once.", trade)}
{cat("monitor", "monitor", "Monitor", "An overview of every account, its positions and its limits, with connection and status always in view.", monitor)}
{cat("plan", "plan", "Plan", "Market Read, chart levels and playbooks to prepare the session and stay on plan during it.", plan)}
{cat("review", "review", "Review", "A trade journal that fills itself, and the performance history to learn from it.", review)}
  </div>
</div>

<section class="section section-alt" id="requirements" style="scroll-margin-top:96px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Requirements</p>
      <h2>What you need.</h2>
    </div>
    <div class="table-wrap">
      <table>
        <caption class="sr-only">SST requirements</caption>
        <tbody>
          <tr><th scope="row">Platform</th><td>NinjaTrader&nbsp;8</td></tr>
          <tr><th scope="row">Computer</th><td>Windows PC or Windows VPS; NinjaTrader must be open and connected while you trade</td></tr>
          <tr><th scope="row">Markets</th><td>CME futures (index, energy and metals contracts, minis and micros)</td></tr>
          <tr><th scope="row">Accounts</th><td>Any account you can trade in NinjaTrader&nbsp;8, including simulation accounts</td></tr>
          <tr><th scope="row">License</th><td>One license key: 1 machine (Monthly / Annual), up to 2 (Lifetime)</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <h2>Ready to run every account from one console?</h2>
      <p>Launch pricing is open now. Start on simulation accounts and go live when you trust it.</p>
      <div class="btn-row"><a class="btn btn-primary" href="/pricing/">See pricing</a><a class="btn btn-secondary" href="/support/">Questions? Visit support</a></div>
    </div>
  </div>
</section>"""

page("/command-center/", "SST Features | Silent Service Trading",
     "SST features for NinjaTrader 8: Trade Console, trade copier with step-down rotation, prop-firm rules, hedge protection, chart tabs and a self-filling trade journal.",
     "/command-center/", cc)

# ------------------------------------------------------------------ PRICING
pricing = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>Launch pricing.</h1>
    <p class="lead">SST, the trading workspace, in three plans — and NYOpen, the automated New York open strategy. Launch prices are offered through December&nbsp;31, 2026.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="notice" role="note">
      {ICONS['info']}
      <div>
        <p><strong>Your license key and download link arrive by email after checkout.</strong></p>
        <p class="muted">Launch prices are offered through December&nbsp;31, 2026. Subscribe before then and your monthly or annual price stays the same for as long as your subscription stays active. Start on simulation accounts first.</p>
      </div>
    </div>

    <div class="price-group-head" id="sst">
      <p class="eyebrow">Silent Service Trading (SST)</p>
      <h2>The trading workspace.</h2>
      <p class="muted">Trade Console, copier, prop rules and journal for NinjaTrader&nbsp;8. <a href="/command-center/">See the features</a></p>
    </div>

    <div class="plans">
      <div class="plan">
        <h2>Monthly</h2>
        <p class="plan-sub">Flexible. Cancel anytime.</p>
        <p class="price">$49<small>/ month</small></p>
        <p class="price-note">Billed monthly.</p>
        <ul class="checks">
          <li>Silent Service Trading (SST) for NinjaTrader&nbsp;8</li>
          <li>All updates while subscribed</li>
          <li>1 machine</li>
          <li>Direct support from the developer</li>
        </ul>
        <a class="btn btn-secondary btn-block" data-plan="monthly" href="https://buy.stripe.com/6oU4gydih0RP6fo1B4gnK03" target="_blank" rel="noopener">Start monthly</a>
      </div>
      <div class="plan">
        <h2>Annual</h2>
        <p class="plan-sub">Save 15% versus paying monthly.</p>
        <p class="price">$500<small>/ year</small></p>
        <p class="price-note">$41.67 a month, billed yearly · save 15%.</p>
        <ul class="checks">
          <li>Everything in Monthly</li>
          <li>Saves $88 a year</li>
          <li>1 machine</li>
          <li>Direct support from the developer</li>
        </ul>
        <a class="btn btn-secondary btn-block" data-plan="annual" href="https://buy.stripe.com/3cI3cucedasp9rAgvYgnK04" target="_blank" rel="noopener">Start annual</a>
      </div>
      <div class="plan featured">
        <span class="plan-flag badge badge-planned">First 25 seats only</span>
        <h2>Lifetime</h2>
        <p class="plan-sub">Pay once. Never billed again.</p>
        <p class="price">$1,999<small>one time</small></p>
        <p class="price-note">Limited to the first 25 buyers.</p>
        <ul class="checks">
          <li>Every future SST upgrade</li>
          <li>Every automated strategy we release, including NYOpen</li>
          <li>Every playbook we release</li>
          <li>Up to 2 machines</li>
        </ul>
        <a class="btn btn-primary btn-block" data-plan="lifetime" href="https://buy.stripe.com/4gM7sKdihbwt33ca7AgnK05" target="_blank" rel="noopener">Claim a lifetime seat</a>
      </div>
    </div>

    <div class="price-group-head" id="nyopen">
      <p class="eyebrow">Automated strategy</p>
      <h2>NYOpen.</h2>
      <p class="muted">The New York open breakout for ES and NQ, running in NinjaTrader&nbsp;8 on your PC. Works on its own — SST not required. <a href="/automation/">See how it trades and the backtests</a></p>
    </div>

    <div class="plans plans-solo">
      <div class="plan featured">
        <span class="plan-flag badge badge-available">Available now</span>
        <h2>NYOpen</h2>
        <p class="plan-sub">One automated strategy. Cancel anytime.</p>
        <p class="price">$39.99<small>/ month</small></p>
        <p class="price-note">Included free with SST Lifetime.</p>
        <ul class="checks">
          <li>SilentService - NYOpen for NinjaTrader&nbsp;8</li>
          <li>ES, NQ, MES and MNQ</li>
          <li>Fixed stop and target, one trade a day, flat by 3:55&nbsp;PM ET</li>
          <li>Updates while subscribed</li>
        </ul>
        <a class="btn btn-primary btn-block" data-plan="nyopen" href="https://buy.stripe.com/fZuaEW4LL8kh33c1B4gnK06" target="_blank" rel="noopener">Get NYOpen</a>
      </div>
      <div class="plan-aside">
        <h3>Already on SST Lifetime?</h3>
        <p class="muted">NYOpen is yours. Install it and leave its License Key setting empty — it uses your SST key. <a href="/support/#nyopen">Setup steps</a></p>
        <h3>Automated trading carries real risk.</h3>
        <p class="muted">Backtests are hypothetical. Run it on a simulation account first, and check your prop firm's rules on automated trading.</p>
      </div>
    </div>

    <p class="muted small checkout-note">Checkout opens in a new tab, handled securely by Stripe. Changed your mind? Just close that tab — nothing is charged until you press Subscribe or Pay.</p>

    <div class="reqs">
      <span><strong>Platform</strong> NinjaTrader&nbsp;8</span>
      <span><strong>Computer</strong> Windows PC or VPS</span>
      <span><strong>Markets</strong> CME futures</span>
      <span><strong>Checkout</strong> Secure, by Stripe</span>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Compare plans</h2></div>
    <div class="table-wrap">
      <table>
        <caption class="sr-only">Plan comparison</caption>
        <thead><tr><th scope="col">Included</th><th scope="col">Monthly</th><th scope="col">Annual</th><th scope="col">Lifetime</th></tr></thead>
        <tbody>
          <tr><th scope="row">SST</th><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><th scope="row">SST updates</th><td>While subscribed</td><td>While subscribed</td><td class="yes">Forever</td></tr>
          <tr><th scope="row">Automated strategies (<a href="/automation/">NYOpen</a>)</th><td>$39.99 / month each</td><td>$39.99 / month each</td><td class="yes">Included</td></tr>
          <tr><th scope="row">Future playbooks</th><td>Sold separately</td><td>Sold separately</td><td class="yes">Included</td></tr>
          <tr><th scope="row">Machines per license</th><td>1</td><td>1</td><td>2</td></tr>
          <tr><th scope="row">Billing</th><td>$49 monthly</td><td>$500 yearly</td><td>$1,999 once</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Pricing questions</h2></div>
    <div class="faq">
      <details><summary>What does Lifetime include?</summary><div><p>One payment, never billed again. You get every future upgrade of SST, plus every automated strategy and every playbook Silent Service Trading releases, for as long as they're offered. Only the first 25 lifetime seats are sold.</p></div></details>
      <details><summary>How long do launch prices last?</summary><div><p>Launch prices are offered through December&nbsp;31, 2026. If you subscribe before then, your monthly or annual price stays the same for as long as your subscription stays active. If it lapses, a new subscription is at the price offered at that time.</p></div></details>
      <details><summary>What happens when I cancel?</summary><div><p>Monthly and annual plans run to the end of the period you've paid for. After that, SST won't start new sessions. Nothing about your NinjaTrader accounts or positions is changed.</p></div></details>
      <details><summary>Can I switch plans?</summary><div><p>Yes. <a href="mailto:{EMAIL}">Email us</a> and we'll help you move between monthly, annual and lifetime.</p></div></details>
      <details><summary>Is sales tax included?</summary><div><p>Tax is calculated at checkout based on where you are. Checkout and billing are handled securely by Stripe.</p></div></details>
    </div>
    <p class="muted small" style="margin-top:28px">More questions? See <a href="/support/#faq">Support</a>.</p>
  </div>
</section>"""

page("/pricing/", "Pricing — SST for NinjaTrader 8 | Silent Service Trading",
     "Launch pricing for Silent Service Trading (SST): $49 monthly, $500 yearly, or a $1,999 lifetime license (first 25 buyers). NYOpen automated strategy: $39.99 a month.",
     "/pricing/", pricing)

# ------------------------------------------------------------------ AUTOMATION
import csv, datetime as _dt
from collections import OrderedDict as _OD

def _money(v):
    v = v.strip().replace("$", "").replace(",", "")
    neg = v.startswith("(")
    v = float(v.strip("()"))
    return -v if neg else v

def backtest(csv_name):
    """Stats from a NinjaTrader Strategy Analyzer trade export kept in _backtests/ (Jekyll does not publish _ folders)."""
    rows = list(csv.DictReader(open(os.path.join(ROOT, "_backtests", csv_name), newline="")))
    pnl = [_money(r["Profit"]) for r in rows]
    fees = sum(_money(r[k]) for r in rows for k in ("Commission", "Clearing Fee", "Exchange Fee", "IP Fee", "NFA Fee"))
    when = [_dt.datetime.strptime(r["Exit time"], "%m/%d/%Y %I:%M:%S %p") for r in rows]
    eq = peak = dd = 0.0; curve = []; streak = worst = 0
    for x in pnl:
        eq += x; peak = max(peak, eq); dd = min(dd, eq - peak); curve.append(eq)
        streak = streak + 1 if x < 0 else 0; worst = max(worst, streak)
    wins = [x for x in pnl if x > 0]; losses = [x for x in pnl if x < 0]
    months = _OD()
    for t, x in zip(when, pnl):
        k = t.strftime("%b %Y"); months[k] = months.get(k, 0) + x
    return dict(instrument=rows[0]["Instrument"], qty=rows[0]["Qty"], first=when[0], last=when[-1], trades=len(pnl),
                net=sum(pnl), win=len(wins) / len(pnl), pf=(sum(wins) / -sum(losses)) if losses else 0,
                avgwin=sum(wins) / len(wins) if wins else 0, avgloss=sum(losses) / len(losses) if losses else 0,
                maxdd=dd, avg=sum(pnl) / len(pnl), fees=fees, months=months, worst=worst, curve=curve)

def _usd(x, dec=0):
    s = f"${abs(x):,.{dec}f}"
    return ("−" + s) if x < 0 else s

def curve_svg(curve, label):
    w, h, pad = 640, 200, 8
    lo, hi = min(0, min(curve)), max(curve)
    n = len(curve)
    pts = [(0, 0)] + [(i + 1, v) for i, v in enumerate(curve)]
    def xy(i, v):
        return (pad + i * (w - 2 * pad) / n, h - pad - (v - lo) * (h - 2 * pad) / ((hi - lo) or 1))
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in (xy(i, v) for i, v in pts))
    x0, yb = xy(0, lo); xe, _ = xy(n, lo)
    _, yz = xy(0, 0)
    return f"""<svg class="curve" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" preserveAspectRatio="none">
  <line x1="{pad}" x2="{w - pad}" y1="{yz:.1f}" y2="{yz:.1f}" stroke="#243044" stroke-width="1"/>
  <polygon points="{x0:.1f},{yb:.1f} {line} {xe:.1f},{yb:.1f}" fill="rgba(56,189,248,0.10)"/>
  <polyline points="{line}" fill="none" stroke="#38BDF8" stroke-width="2" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>
</svg>"""

def bt_card(name, b):
    tiles = [("Net profit", _usd(b["net"])), ("Trades", f'{b["trades"]}'), ("Win rate", f'{b["win"]*100:.0f}%'),
             ("Profit factor", f'{b["pf"]:.2f}'), ("Max drawdown", _usd(b["maxdd"])), ("Avg trade", _usd(b["avg"], 2)),
             ("Avg win / loss", f'{_usd(b["avgwin"])} / {_usd(b["avgloss"])}'), ("Longest losing run", f'{b["worst"]} trades')]
    tiles_html = "\n".join(f'          <div class="stat"><span>{k}</span><strong>{v}</strong></div>' for k, v in tiles)
    mrows = "\n".join(f'            <tr><th scope="row">{m}</th><td class="num{" neg" if v < 0 else ""}">{_usd(v)}</td></tr>' for m, v in b["months"].items())
    period = f'{b["first"]:%b %-d} – {b["last"]:%b %-d, %Y}'
    return f"""      <article class="bt card">
        <header class="bt-head">
          <h3>{name}</h3>
          <p class="muted small">{b["instrument"]} · {b["qty"]} contract · {period}</p>
        </header>
        <div class="stats">
{tiles_html}
        </div>
        <figure class="bt-curve">
          {curve_svg(b["curve"], f"Equity curve for {name}: from $0 to {_usd(b['net'])} over {b['trades']} trades")}
          <figcaption class="muted small">Cumulative profit per trade, before commissions, fees and slippage.</figcaption>
        </figure>
        <details class="bt-months"><summary>Results by month</summary>
          <table>
            <caption class="sr-only">{name} results by month</caption>
            <tbody>
{mrows}
            </tbody>
          </table>
        </details>
      </article>"""

bt_es = backtest("nyopen-es.csv")
bt_nq = backtest("nyopen-nq.csv")

automation = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Automation</p>
    <h1>Automated trading strategies.</h1>
    <p class="lead">Rule-based strategies that run in NinjaTrader&nbsp;8 on your own PC, inside the same limits SST already enforces: prop rules, max micros and same-firm hedge protection.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="auto-head">
      <div>
        <p class="eyebrow">SilentService – NYOpen</p>
        <h2>Trade the New York open breakout, the same way every day.</h2>
        <p class="muted">NYOpen marks the overnight range and trades the first clean break of it after the New York open — one trade a day, with a fixed stop and target, flat before the close.</p>
        <ul class="checks">
          <li>Range: 3:00–9:30 AM ET</li>
          <li>Entry: first break above or below the range, 9:30–11:00 AM ET</li>
          <li>Fixed dollar stop and target per contract</li>
          <li>One trade a day; flat by 3:55 PM ET</li>
          <li>Turn each weekday on or off</li>
          <li>ES and NQ (and their micros)</li>
        </ul>
      </div>
      <div class="plan featured auto-price">
        <span class="plan-flag badge badge-available">Available now</span>
        <h3>NYOpen</h3>
        <p class="price">$39.99<small>/ month</small></p>
        <p class="price-note">Monthly subscription, cancel anytime. Included with SST Lifetime.</p>
        <a class="btn btn-primary btn-block" data-plan="nyopen" href="https://buy.stripe.com/fZuaEW4LL8kh33c1B4gnK06" target="_blank" rel="noopener">Get NYOpen</a>
        <p class="muted small" style="margin-top:12px">Checkout opens in a new tab, by Stripe. <a href="/support/#nyopen">How setup works</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt" id="backtests" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Backtests</p>
      <h2>NYOpen on ES and NQ, 2026.</h2>
      <p>NinjaTrader Strategy Analyzer, one contract, every trade from January&nbsp;2 to November&nbsp;13, 2026. Results are hypothetical — read the notes below them.</p>
    </div>
    <div class="grid-2 bt-grid">
{bt_card("NYOpen · ES", bt_es)}
{bt_card("NYOpen · NQ", bt_nq)}
    </div>
    <div class="notice bt-notes" role="note">
      {ICONS['info']}
      <div>
        <p><strong>How to read these numbers.</strong></p>
        <ul>
          <li>Profits are before commissions, exchange fees and slippage. At a few dollars per round trip, about 200 trades cost several hundred dollars more than shown, and real fills — especially fast breakout fills — can be worse than the backtest's.</li>
          <li>The strategy's settings were chosen with this same 2026 data in view. Results on data the settings never saw would likely be weaker.</li>
        </ul>
        <p class="muted small">Hypothetical performance results have many inherent limitations. No representation is made that any account will or is likely to achieve profits or losses similar to those shown. Hypothetical results are prepared with the benefit of hindsight, do not involve financial risk, and cannot account for factors such as the ability to keep trading through losses, liquidity, or execution. Actual results will differ, and can include losses greater than any shown here.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <h2>Run it on Sim first.</h2>
      <p>Every automated strategy should run on a simulation account before it touches a funded one — and your prop firm's rules on automated trading still apply.</p>
      <div class="btn-row"><a class="btn btn-primary" href="/pricing/">See SST pricing</a><a class="btn btn-secondary" href="mailto:{EMAIL}?subject=NYOpen%20question">Ask a question</a></div>
    </div>
  </div>
</section>"""

page("/automation/", "Automation — NYOpen strategy for NinjaTrader 8 | Silent Service Trading",
     "SilentService NYOpen: an automated New York open breakout strategy for ES and NQ on NinjaTrader 8, with 2026 backtests. $39.99 a month, included with Lifetime.",
     "/automation/", automation)



# ------------------------------------------------------------------ NYOPEN THANKS (Stripe redirect for the NYOpen link)
nyopen_steps = f"""    <ol class="steps">
      <li><strong>Watch your inbox</strong>Your NYOpen license key and the strategy file arrive by email at the address you used at checkout. Check spam too.</li>
      <li><strong>Install</strong>Close NinjaTrader&nbsp;8. Copy the NYOpen file into <code>Documents\\NinjaTrader&nbsp;8\\bin\\Custom\\Strategies</code>, start NinjaTrader, open the NinjaScript Editor (New → NinjaScript Editor) and press F5 to compile. If you received a .zip instead, use Tools → Import → NinjaScript Add-On.</li>
      <li><strong>Enter your key</strong>Add <em>SilentService - NYOpen</em> to a chart or the Strategies tab. Paste your key into <em>License Key</em>, the first setting. SST Lifetime owners can leave it empty — the SST key on that PC is used.</li>
      <li><strong>Start on Sim</strong>Pick a simulation account and ES or NQ (or MES / MNQ), keep 1 contract, and enable it. The bottom-left of the chart shows your license status. Go live when you trust it.</li>
    </ol>"""

nyopen_thanks = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Payment received</p>
    <h1>NYOpen is on its way.</h1>
    <p class="lead">Thanks for subscribing. Your receipt from Stripe is on its way to the email you used at checkout.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What happens next</p><h2>Four steps to your first NYOpen session.</h2></div>
{nyopen_steps}
    <div class="notice" role="note" style="margin-top:36px">
      {ICONS['info']}
      <div>
        <p><strong>Without a valid license, NYOpen turns itself off when you enable it</strong> and the Log tab says why. If a license lapses while it runs, it takes no new trades — stops, targets and the 3:55&nbsp;PM flatten keep working.</p>
        <p class="muted">Check your prop firm's rules on automated trading before running it on a funded account.</p>
      </div>
    </div>
    <p class="muted" style="margin-top:28px">Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your order email, or visit <a href="/support/#nyopen">Support</a>.</p>
  </div>
</section>"""
page("/automation/thanks/", "Welcome aboard — NYOpen | Silent Service Trading",
     "Thanks for subscribing to NYOpen. Here's how to install it and enter your license key.", "", nyopen_thanks, noindex=True)

# ------------------------------------------------------------------ ABOUT
socials = [("X", "https://x.com/thesubmarinevet"), ("YouTube", "https://youtube.com/@SilentServiceTrading"),
           ("Instagram", "https://instagram.com/silentservicetrading"), ("TikTok", "https://tiktok.com/@silentservicetrading"),
           ("Facebook", "https://facebook.com/thesubmarinevet"), ("Threads", "https://threads.net/@silentservicetrading"),
           ("TradingView", "https://www.tradingview.com/u/thesubmarinevet/")]
follow = "\n".join(f'        <a href="{u}" rel="noopener" target="_blank">{n}<span class="sr-only"> (opens in a new tab)</span></a>' for n, u in socials)
about = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>The Submarine Vet, and the tools he builds.</h1>
    <p class="lead">Silent Service Trading (SST) is the NinjaTrader software built by The Submarine Vet.</p>
  </div>
</section>

<section class="section">
  <div class="wrap founder">
    <div class="founder-mark" aria-hidden="true">
      <!-- FOUNDER PHOTO TO ADD (optional): replace this block with <img src="/assets/img/founder.jpg" alt="..."> -->
      <svg viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="88" fill="none" stroke="#5B8DB8" stroke-opacity=".18" stroke-width="2"/>
        <circle cx="100" cy="100" r="62" fill="none" stroke="#5B8DB8" stroke-opacity=".32" stroke-width="2"/>
        <circle cx="100" cy="100" r="36" fill="none" stroke="#5B8DB8" stroke-opacity=".55" stroke-width="2"/>
        <path d="M100 100 L162 48" stroke="#38BDF8" stroke-width="3" stroke-linecap="round"/>
        <circle cx="100" cy="100" r="6" fill="#38BDF8"/>
      </svg>
    </div>
    <div>
      <p class="eyebrow">The story</p>
      <h2>From reading instruments to building them.</h2>
      <!-- FOUNDER DETAILS TO ADD: boat / rate, years served, how trading started. Keep it plain and specific. -->
      <p>Submarine service teaches a particular kind of discipline: read your instruments instead of guessing, follow procedure the same way every time, and keep the boat inside its limits — through long, quiet stretches and through the moments that suddenly matter.</p>
      <p>Trading futures turned out to reward the same habits. Running several funded accounts at once, the hard part wasn't finding setups. It was keeping track: which account was near its limit, what had copied where, what was still open.</p>
      <p>Silent Service Trading started as the console he built for his own trading in NinjaTrader. Now other traders can run it too.</p>
      <blockquote class="quote">Instruments over instinct.</blockquote>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it fits together</p>
      <h2>One person, one product.</h2>
    </div>
    <div class="grid-2">
      <div class="card"><h3>The Submarine Vet</h3><p>The parent brand and the person behind it: trading content, process and results, told straight.</p></div>
      <a class="card" href="/command-center/"><h3>Silent Service Trading (SST)</h3><p>The NinjaTrader&nbsp;8 software for trading, monitoring, planning and reviewing every account — built and supported by the developer who uses it.</p><span class="more">See the features &rarr;</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <h2>What we believe</h2>
    <ul>
      <li><strong>You make the decisions.</strong> SST copies and protects the trades you place. Playbooks alert; they never enter for you.</li>
      <li><strong>Your accounts stay yours.</strong> It runs inside NinjaTrader on your own machine. Your broker and prop-firm logins never leave it.</li>
      <li><strong>No hype.</strong> No promised returns, no signal selling. The tools are built to keep accounts inside their limits.</li>
    </ul>
    <h2 id="follow" style="scroll-margin-top:96px">Follow along</h2>
    <p>@thesubmarinevet on every platform.</p>
    <div class="follow" style="margin-top:18px">
{follow}
    </div>
  </div>
</section>"""

page("/about/", "About — The Submarine Vet | Silent Service Trading",
     "Silent Service Trading is the software platform of The Submarine Vet, a submarine veteran who trades futures and built SST for NinjaTrader 8.",
     "/about/", about)

# ------------------------------------------------------------------ SUPPORT
support = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Support</p>
    <h1>Help with SST.</h1>
    <p class="lead">Getting started, requirements, answers to common questions, and a direct line to the developer.</p>
  </div>
</section>

<section class="section" id="getting-started" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Getting started</p><h2>From checkout to your first copied trade.</h2></div>
    <ol class="steps">
      <li><strong>Check your email</strong>Your license key and download link arrive by email after checkout. Check spam too.</li>
      <li><strong>Install</strong>In NinjaTrader&nbsp;8: Tools → Import → NinjaScript Add-On, choose the file, then restart NinjaTrader.</li>
      <li><strong>Enter your key</strong>Open Silent Service Trading from NinjaTrader's New menu and paste your license key.</li>
      <li><strong>Start on Sim</strong>Set your prop rules and copier group on simulation accounts first. Go live when you trust it.</li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap grid-2">
    <div class="card contact-card">
      <p class="eyebrow" style="margin:0">Contact</p>
      <h2 style="font-size:22px">Email the developer</h2>
      <p class="muted">Include the email you used at checkout and a short description. Screenshots help.</p>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
    <div class="card">
      <p class="eyebrow" style="margin:0 0 14px">Requirements</p>
      <ul class="checks">
        <li>NinjaTrader&nbsp;8 <span>on Windows or a Windows VPS</span></li>
        <li>NinjaTrader open and connected <span>while you trade</span></li>
        <li>CME futures accounts <span>(prop, broker or simulation)</span></li>
        <li>One license key <span>for 1 machine (Lifetime: 2)</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section section-alt" id="nyopen" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">NYOpen</p><h2>Setting up the NYOpen strategy.</h2></div>
{nyopen_steps}
  </div>
</section>

<section class="section" id="faq" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">FAQ</p><h2>Straight answers.</h2></div>
    <div class="faq">
      <details><summary>Does SST trade for me?</summary><div><p>No. You place the trades — by hand, or with your own NinjaTrader strategies. SST copies them to your other accounts and enforces the limits you set. Playbooks only alert and mark the chart.</p></div></details>
      <details><summary>Is a trade copier allowed by my prop firm?</summary><div><p>Rules differ by firm and change over time. Some firms allow copying between your own accounts, some restrict it, and some limit automated trading. Check your firm's current rules before you copy to its accounts — you're responsible for following them.</p></div></details>
      <details><summary>Does my computer need to stay on?</summary><div><p>Yes. SST runs inside NinjaTrader, so NinjaTrader must be open and connected while you trade. Many traders use a Windows VPS.</p></div></details>
      <details><summary>Which accounts does it work with?</summary><div><p>Any account you can trade in NinjaTrader&nbsp;8, including prop-firm accounts connected there and NinjaTrader's simulation accounts.</p></div></details>
      <details><summary>Can I try it without risking money?</summary><div><p>Yes, and you should. Set it up on simulation accounts first, test your copier group and rules, then move to live accounts.</p></div></details>
      <details><summary>Do you see my account data?</summary><div><p>No. Your accounts, balances and positions stay inside NinjaTrader on your machine. The license check sends only your license key and a machine ID.</p></div></details>
      <details><summary>How do I move my license to a new computer?</summary><div><p>Monthly and Annual licenses run on 1 machine; Lifetime on up to 2. <a href="mailto:{EMAIL}">Email us</a> and we'll free up a seat.</p></div></details>
      <details><summary>How do I cancel or change my plan?</summary><div><p><a href="mailto:{EMAIL}">Email us</a> from the address you used at checkout. Monthly and annual plans run to the end of the period you've paid for.</p></div></details>
      <details><summary>Does NYOpen need SST?</summary><div><p>No. NYOpen is a NinjaTrader&nbsp;8 strategy and runs on its own with its own license key. It's included with an SST Lifetime license — leave its License Key empty and it uses the SST key on that PC.</p></div></details>
      <details><summary>Does NYOpen trade micros?</summary><div><p>Yes — run it on MES or MNQ as well as ES or NQ. The stop and target are set in dollars per contract and converted to ticks, so the distance stays the same at any size.</p></div></details>
      <details><summary>What happens if my NYOpen license runs out?</summary><div><p>If it lapses while running, NYOpen takes no new trades; any open trade keeps its stop, target and 3:55&nbsp;PM flatten. The next time you enable it without a valid license, it turns itself off and the Log tab says why.</p></div></details>
      <details><summary>What's the difference between "Available", "In testing" and "Planned"?</summary><div><p>Available features are in the current release. In-testing features are built and finishing testing before release. Planned features are on the roadmap and not yet in the product — buy for what's available today.</p></div></details>
    </div>
  </div>
</section>"""

page("/support/", "Support — SST | Silent Service Trading",
     "Get started with SST for NinjaTrader 8: installation, requirements, frequently asked questions and direct support from the developer.",
     "/support/", support)

# ------------------------------------------------------------------ THANKS (URL must not change: Stripe redirect)
thanks = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Payment received</p>
    <h1>Welcome aboard.</h1>
    <p class="lead">Thanks for your purchase. Your receipt from Stripe is on its way to the email you used at checkout.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What happens next</p><h2>Four steps to your first copied trade.</h2></div>
    <ol class="steps">
      <li><strong>Watch your inbox</strong>Your license key and download link arrive by email. Check spam too.</li>
      <li><strong>Install</strong>In NinjaTrader&nbsp;8: Tools → Import → NinjaScript Add-On, choose the file, then restart NinjaTrader.</li>
      <li><strong>Enter your key</strong>Open Silent Service Trading from NinjaTrader's New menu and paste your license key.</li>
      <li><strong>Start on Sim</strong>Set your prop rules and copier group on simulation accounts first. Go live when you trust it.</li>
    </ol>
    <p class="muted" style="margin-top:36px">Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your order email, or visit <a href="/support/">Support</a>.</p>
  </div>
</section>"""
page("/command-center/thanks/", "Welcome aboard — SST | Silent Service Trading",
     "Thanks for your purchase. Here's how to install SST and get started.", "", thanks, noindex=True)

# ------------------------------------------------------------------ 404
nf = """<section class="page-hero" style="border-bottom:none;min-height:56vh">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>That page isn't here.</h1>
    <p class="lead">It may have moved when the site was redesigned.</p>
    <div class="btn-row" style="margin-top:28px">
      <a class="btn btn-primary" href="/">Go home</a>
      <a class="btn btn-secondary" href="/command-center/">Features</a>
      <a class="btn btn-secondary" href="/support/">Support</a>
    </div>
  </div>
</section>"""
page("/404.html", "Page not found | Silent Service Trading", "Page not found.", "", nf, noindex=True)
