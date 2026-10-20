#!/usr/bin/env python3
"""Generates the static pages for thesubmarinevet.com (redesign branch).
Output is plain HTML committed to the repo; GitHub Pages serves it as-is."""
import json, sys, os

ROOT = sys.argv[1]
SITE = "https://thesubmarinevet.com"
EMAIL = "thesubmarineveteran@gmail.com"

LOGO = """<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
  <rect x="1" y="1" width="30" height="30" rx="8" fill="#141B26" stroke="#2C3A52"/>
  <circle cx="16" cy="16" r="9.5" fill="none" stroke="#5B8DB8" stroke-width="1.6" stroke-opacity=".55"/>
  <circle cx="16" cy="16" r="5" fill="none" stroke="#5B8DB8" stroke-width="1.6"/>
  <path d="M16 16 L23.5 9.5" stroke="#38BDF8" stroke-width="2" stroke-linecap="round"/>
  <circle cx="16" cy="16" r="1.8" fill="#38BDF8"/>
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

NAV = [("Home", "/"), ("Command Center", "/command-center/"), ("Pricing", "/pricing/"), ("About", "/about/"), ("Support", "/support/")]

DISCLAIMER = ("Silent Service Command Center is a software tool, not financial advice. Futures trading involves substantial risk of loss and is not "
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;650;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
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
      <a class="btn btn-primary btn-sm" href="/pricing/">Get Command Center</a>
    </nav>
  </div>
</header>
"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="logo" href="/" aria-label="Silent Service Trading — home">{LOGO}<span class="logo-text"><strong>Silent Service Trading</strong><span>by The Submarine Vet</span></span></a>
        <p>Command Center: one NinjaTrader&nbsp;8 workspace for trading, monitoring and reviewing every account you run.</p>
      </div>
      <div class="foot-col">
        <h2>Product</h2>
        <ul>
          <li><a href="/command-center/">Command Center</a></li>
          <li><a href="/command-center/#trade">Features</a></li>
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

def shot(label, file_hint, alt, bar="Silent Service Command Center"):
    # Placeholder frame until the real screenshot (file_hint) is added.
    return f"""<figure class="shot">
  <div class="shot-bar" aria-hidden="true"><i></i><i></i><i></i><span>{bar}</span></div>
  <!-- SCREENSHOT TO ADD: /assets/img/{file_hint}  — replace the div below with:
       <img src="/assets/img/{file_hint}" alt="{alt}" width="1600" height="1000" loading="lazy"> -->
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
     "sameAs": ["https://x.com/thesubmarinevet", "https://www.youtube.com/@thesubmarinevet", "https://www.instagram.com/thesubmarinevet",
                "https://www.facebook.com/thesubmarinevet", "https://www.tiktok.com/@thesubmarinevet", "https://www.threads.net/@thesubmarinevet",
                "https://www.tradingview.com/u/thesubmarinevet/"]},
    {"@type": "SoftwareApplication", "name": "Silent Service Command Center", "applicationCategory": "FinanceApplication",
     "operatingSystem": "Windows (NinjaTrader 8)", "url": SITE + "/command-center/",
     "offers": [
       {"@type": "Offer", "name": "Monthly", "price": "149.99", "priceCurrency": "USD", "url": SITE + "/pricing/"},
       {"@type": "Offer", "name": "Annual", "price": "1439.90", "priceCurrency": "USD", "url": SITE + "/pricing/"},
       {"@type": "Offer", "name": "Lifetime", "price": "2999.00", "priceCurrency": "USD", "url": SITE + "/pricing/"}]}
  ]}
home_ld = '<script type="application/ld+json">' + json.dumps(ld, separators=(",", ":")) + "</script>\n"

pillars = [
 ("trade", "Trade", "Order entry, trims, ATM templates and a trade copier that sizes every follower on its own terms.", "/command-center/#trade"),
 ("monitor", "Monitor", "Every account's day at a glance, prop-firm limits enforced automatically, connection and strategy status.", "/command-center/#monitor"),
 ("plan", "Plan", "Market Read with the levels intraday traders draw by hand, plus playbooks that alert and mark the chart.", "/command-center/#plan"),
 ("review", "Review", "A trade journal that records itself, with daily results, per-account views and an equity curve.", "/command-center/#review"),
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
      <p class="eyebrow">Command Center for NinjaTrader&nbsp;8</p>
      <h1>Command Your Trading.<br><span class="accent">Stay in Control.</span></h1>
      <p class="lead">One integrated NinjaTrader&nbsp;8 workspace for managing trading accounts, monitoring positions, following playbooks, and reviewing performance.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/pricing/">See pricing</a>
        <a class="btn btn-secondary" href="/command-center/">Take the tour</a>
      </div>
      <p class="hero-note">Early access now open · Runs inside NinjaTrader on your own PC</p>
    </div>
    <div>
{shot("Command Center workspace", "cc-workspace.png", "The Command Center workspace in NinjaTrader 8 with the Trade Console, accounts panel and chart")}
    </div>
  </div>
</section>

<section class="strip" aria-label="Highlights">
  <div class="wrap">
    <ul>
      <li>{ICONS['nt']}Built for NinjaTrader&nbsp;8</li>
      <li>{ICONS['pc']}Runs locally — your logins stay on your PC</li>
      <li>{ICONS['shield']}Prop-firm limits enforced per account</li>
      <li>{ICONS['hand']}You place every trade</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">One workspace</p>
      <h2>Everything a multi-account trader juggles, in one window.</h2>
      <p>Command Center brings the four jobs of an active trading day together, so you stop switching between tabs, spreadsheets and dashboards.</p>
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
      <h2>How a session runs in Command Center.</h2>
    </div>

    <div class="row">
      <div>
        <h3>Enter, manage and copy trades from one console.</h3>
        <p>Place the trade once. Command Center copies it to your follower accounts, each with its own size and limits, and keeps every bracket on the instrument it was placed on.</p>
        <ul class="checks">
          <li>Buy, sell, reverse, close and trim ¼ or ½ in one click</li>
          <li>Use your own NinjaTrader ATM templates</li>
          <li>Copy minis as micros, with contract caps per account</li>
          <li>FLATTEN ALL ACCOUNTS when you need everything closed now</li>
        </ul>
      </div>
{shot("Trade Console and trade copier", "cc-trade.png", "The Trade Console with order buttons, trims and the copier status")}
    </div>

    <div class="row flip">
      <div>
        <h3>Watch every account, and let the rules enforce themselves.</h3>
        <p>Enter each prop account's limits once. When an account reaches its daily loss or drawdown limit, Command Center locks it and flattens it — even if you're not watching.</p>
        <ul class="checks">
          <li>Day P&amp;L and balance for every account, sortable</li>
          <li>Drawdown, daily limits and consistency per account</li>
          <li>Connection and copier status always in view</li>
        </ul>
      </div>
{shot("Accounts and prop-firm rules", "cc-monitor.png", "The accounts panel and prop-firm rules table")}
    </div>

    <div class="row">
      <div>
        <h3>Plan the session, then review it.</h3>
        <p>Market Read puts the day's key levels on the chart. After the close, the journal has already recorded every trade, so review starts with the facts.</p>
        <ul class="checks">
          <li>Prior day, session and opening-range levels, VWAP and POC</li>
          <li>Playbooks that alert and mark the chart — never place orders</li>
          <li>Daily results, per-account views and an equity curve</li>
        </ul>
      </div>
{shot("Market Read and trade journal", "cc-plan-review.png", "The chart with Market Read levels next to the trade journal")}
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
      <p>Command Center was built by The Submarine Vet for his own futures trading on NinjaTrader — the tool he wanted when running several funded accounts at once. Silent Service Trading is where that tool, and the ones that follow, now live.</p>
      <blockquote class="quote">Instruments over instinct.</blockquote>
      <p style="margin-top:24px"><a href="/about/">Read the story &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Pricing</p>
      <h2>Founder pricing for early access.</h2>
      <p>Monthly, annual, or a limited lifetime license. Every plan includes all Command Center updates.</p>
    </div>
    <div class="grid-3">
      <div class="card"><h3>Monthly</h3><p class="price">$149.99<small>/ month</small></p><p class="price-note">Cancel anytime.</p></div>
      <div class="card"><h3>Annual</h3><p class="price">$1,439.90<small>/ year</small></p><p class="price-note">$119.99 a month — save 20%.</p></div>
      <div class="card"><h3>Lifetime</h3><p class="price">$2,999<small>once</small></p><p class="price-note">First 25 seats. Includes every future bot and playbook.</p></div>
    </div>
    <div class="btn-row" style="justify-content:center;margin-top:32px"><a class="btn btn-primary" href="/pricing/">Compare plans</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <h2>Take command of every account.</h2>
      <p>Join the early-access crew, set it up on simulation accounts, and go live when you trust it.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/pricing/">Get Command Center</a>
        <a class="btn btn-secondary" href="/support/#getting-started">How setup works</a>
      </div>
    </div>
  </div>
</section>"""

page("/", "Command Center for NinjaTrader 8 | Silent Service Trading",
     "One NinjaTrader 8 workspace to manage trading accounts, monitor positions, follow playbooks and review performance. Command Center early access is open.",
     "/", home, extra=home_ld)

# ------------------------------------------------------------------ COMMAND CENTER
trade = [
 ("Trade Console", "Buy and sell at market or limit with stop-loss and take-profit in ticks. Reverse, close and cancel from the same panel. Buttons never move — status messages appear below them, so a click always lands where you aim.", "a"),
 ("One-click trims", "Trim ¼ or ½ of a position in one click, rounded to the nearest contract and always leaving at least one open.", "a"),
 ("ATM integration", "Pick any of your NinjaTrader ATM strategy templates from the console. Brackets and ATM orders stay on the instrument they were placed on, even after you switch to another.", "a"),
 ("Trade copier", "Trade one lead account and copy to followers, each with its own multiplier, maximum contracts and daily loss / profit lock. Copy minis as micros (NQ → MNQ, ES → MES and more).", "a"),
 ("Flatten all accounts", "One click turns the copier off, cancels every working order and closes every position on every account — and logs what each account held.", "a"),
 ("Step-down rotation", "One follower takes each trade until it reaches its target or loss limit, then the next account takes over, with working exit orders on the follower.", "t"),
]
monitor = [
 ("Accounts overview", "Day P&amp;L and balance for every account, sortable by name, P&amp;L or balance. Simulation accounts are kept out of your totals.", "a"),
 ("Prop-firm rules", "Per account: stage, drawdown, daily loss and profit limits, and consistency %. Reach a limit and the account locks and flattens; locks lift at the next trading day.", "a"),
 ("Positions and open P&amp;L", "Your position and its open P&amp;L — in dollars, points or both — on the chart's position line and in the console header.", "a"),
 ("Connection and copier status", "A connection indicator and a COPIER ON / OFF button sit in view at all times, so you know what is live.", "a"),
 ("Automated strategy overview", "See which NinjaTrader strategies are running, on which account and instrument, and whether they are in sync.", "a"),
 ("Max micros per account", "Set the most micros each account may trade. The copier caps to it, and your own strategies can read it and size down.", "t"),
]
plan = [
 ("Market Read", "The session at a glance: key levels with their distance from price, market bias and the opening range.", "a"),
 ("Chart levels", "Prior day high and low, Asia / London / New York session ranges, premarket, 15-minute opening range, VWAP, POC from tick data, daily pivots, fair value gaps and EMAs — drawn for you.", "a"),
 ("Playbooks", "Add playbooks for alerts, chart markers and a playbook panel. Import rule playbooks or install playbook packs. A playbook never places an order — you decide.", "a"),
 ("Playbook Builder", "Build your own setups without code — for example a break of the 15-minute high, then a retest within six bars, after 9:45 ET — with a plain-English preview and past hits on the chart.", "p"),
 ("Alert sounds and phone alerts", "Choose sounds per alert type, and get playbook alerts on your phone through the free ntfy app. Alerts only — no account data is ever sent.", "p"),
]
review = [
 ("Trade Journal", "Every fill is recorded automatically and grouped into round-trip trades, with daily summary tiles, a trades list and fills.", "a"),
 ("Performance history", "Results by day and by account, with an equity curve. Exclude accounts you trade just for fun from your statistics.", "a"),
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
      <p class="eyebrow">Silent Service Command Center</p>
      <h1>Your whole trading day, in one NinjaTrader workspace.</h1>
      <p class="lead">Command Center runs inside NinjaTrader&nbsp;8 on your own PC. It doesn't trade for you — it gives you one place to trade, monitor, plan and review every account.</p>
      <div class="btn-row" style="margin-top:28px">
        <a class="btn btn-primary" href="/pricing/">See pricing</a>
        <a class="btn btn-secondary" href="/support/#getting-started">Getting started</a>
      </div>
    </div>
    <div>
{shot("Command Center workspace", "cc-workspace.png", "The Command Center workspace in NinjaTrader 8")}
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
      <span>{badge('t')} Built, finishing testing before release</span>
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
        <caption class="sr-only">Command Center requirements</caption>
        <tbody>
          <tr><th scope="row">Platform</th><td>NinjaTrader&nbsp;8</td></tr>
          <tr><th scope="row">Computer</th><td>Windows PC or Windows VPS; NinjaTrader must be open and connected while you trade</td></tr>
          <tr><th scope="row">Markets</th><td>CME futures (index, energy and metals contracts, minis and micros)</td></tr>
          <tr><th scope="row">Accounts</th><td>Any account you can trade in NinjaTrader&nbsp;8, including simulation accounts</td></tr>
          <tr><th scope="row">License</th><td>One license key, up to 2 machines</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta">
      <h2>Ready to run every account from one console?</h2>
      <p>Early access is open at founder pricing. Start on simulation accounts and go live when you trust it.</p>
      <div class="btn-row"><a class="btn btn-primary" href="/pricing/">See pricing</a><a class="btn btn-secondary" href="/support/">Questions? Visit support</a></div>
    </div>
  </div>
</section>"""

page("/command-center/", "Command Center Features | Silent Service Trading",
     "Command Center for NinjaTrader 8: Trade Console, trade copier, prop-firm rules, account overview, Market Read, playbooks and a self-filling trade journal.",
     "/command-center/", cc)

# ------------------------------------------------------------------ PRICING
pricing = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1>Founder pricing for early access.</h1>
    <p class="lead">One product, three ways to pay. Every plan includes all Command Center updates while it's active.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="notice" role="note">
      {ICONS['info']}
      <div>
        <p><strong>Command Center is in early access.</strong> After checkout, your license key and download link arrive by email — during early access they're sent personally, usually within a few hours.</p>
        <p class="muted">Founder prices stay with you for as long as you stay subscribed. Start on simulation accounts first.</p>
      </div>
    </div>

    <div class="plans">
      <div class="plan">
        <h2>Monthly</h2>
        <p class="plan-sub">Flexible. Cancel anytime.</p>
        <p class="price">$149.99<small>/ month</small></p>
        <p class="price-note">Billed monthly.</p>
        <ul class="checks">
          <li>Command Center for NinjaTrader&nbsp;8</li>
          <li>All updates while subscribed</li>
          <li>Up to 2 machines</li>
          <li>Direct support from the developer</li>
        </ul>
        <a class="btn btn-secondary btn-block" data-plan="monthly" href="mailto:{EMAIL}?subject=Command%20Center%20-%20Monthly">Start monthly</a>
      </div>
      <div class="plan">
        <h2>Annual</h2>
        <p class="plan-sub">Save 20% versus paying monthly.</p>
        <p class="price">$1,439.90<small>/ year</small></p>
        <p class="price-note">$119.99 a month, billed yearly · save 20%.</p>
        <ul class="checks">
          <li>Everything in Monthly</li>
          <li>Saves $360 a year</li>
          <li>Up to 2 machines</li>
          <li>Direct support from the developer</li>
        </ul>
        <a class="btn btn-secondary btn-block" data-plan="annual" href="mailto:{EMAIL}?subject=Command%20Center%20-%20Annual">Start annual</a>
      </div>
      <div class="plan featured">
        <span class="plan-flag badge badge-planned">First 25 seats only</span>
        <h2>Lifetime</h2>
        <p class="plan-sub">Pay once. Never billed again.</p>
        <p class="price">$2,999<small>one time</small></p>
        <p class="price-note">Limited to the first 25 founders.</p>
        <ul class="checks">
          <li>Every future Command Center upgrade</li>
          <li>Every bot (automated strategy) we release</li>
          <li>Every playbook we release</li>
          <li>Up to 2 machines</li>
        </ul>
        <a class="btn btn-primary btn-block" data-plan="lifetime" href="mailto:{EMAIL}?subject=Command%20Center%20-%20Lifetime">Claim a lifetime seat</a>
      </div>
    </div>

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
          <tr><th scope="row">Command Center</th><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><th scope="row">Command Center updates</th><td>While subscribed</td><td>While subscribed</td><td class="yes">Forever</td></tr>
          <tr><th scope="row">Future bots and playbooks</th><td>Sold separately</td><td>Sold separately</td><td class="yes">Included</td></tr>
          <tr><th scope="row">Machines per license</th><td>2</td><td>2</td><td>2</td></tr>
          <tr><th scope="row">Billing</th><td>$149.99 monthly</td><td>$1,439.90 yearly</td><td>$2,999 once</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Pricing questions</h2></div>
    <div class="faq">
      <details><summary>What does Lifetime include?</summary><div><p>One payment, never billed again. You get every future upgrade of Command Center, plus every bot (automated strategy) and every playbook Silent Service Trading releases, for as long as they're offered. Only the first 25 lifetime seats are sold.</p></div></details>
      <details><summary>What happens when I cancel?</summary><div><p>Monthly and annual plans run to the end of the period you've paid for. After that, Command Center won't start new sessions. Nothing about your NinjaTrader accounts or positions is changed.</p></div></details>
      <details><summary>Can I switch plans?</summary><div><p>Yes. <a href="mailto:{EMAIL}">Email us</a> and we'll help you move between monthly, annual and lifetime.</p></div></details>
      <details><summary>Is sales tax included?</summary><div><p>Tax is calculated at checkout based on where you are. Checkout and billing are handled securely by Stripe.</p></div></details>
    </div>
    <p class="muted small" style="margin-top:28px">More questions? See <a href="/support/#faq">Support</a>.</p>
  </div>
</section>"""

page("/pricing/", "Pricing — Command Center for NinjaTrader 8 | Silent Service Trading",
     "Founder pricing for Command Center: $149.99 monthly, $1,439.90 yearly, or a $2,999 lifetime license limited to the first 25 founders.",
     "/pricing/", pricing)

# ------------------------------------------------------------------ ABOUT
socials = [("X", "https://x.com/thesubmarinevet"), ("YouTube", "https://youtube.com/@thesubmarinevet"),
           ("Instagram", "https://instagram.com/thesubmarinevet"), ("TikTok", "https://tiktok.com/@thesubmarinevet"),
           ("Facebook", "https://facebook.com/thesubmarinevet"), ("Threads", "https://threads.net/@thesubmarinevet"),
           ("TradingView", "https://www.tradingview.com/u/thesubmarinevet/")]
follow = "\n".join(f'        <a href="{u}" rel="noopener" target="_blank">{n}<span class="sr-only"> (opens in a new tab)</span></a>' for n, u in socials)
about = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>The Submarine Vet, and the tools he builds.</h1>
    <p class="lead">Silent Service Trading is the software platform of The Submarine Vet. Command Center is its first product.</p>
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
      <p>Command Center started as the console he built for his own trading in NinjaTrader. It became Silent Service Trading's first product.</p>
      <blockquote class="quote">Instruments over instinct.</blockquote>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How it fits together</p>
      <h2>One brand, one platform, one flagship.</h2>
    </div>
    <div class="grid-3">
      <div class="card"><h3>The Submarine Vet</h3><p>The parent brand and the person behind it: trading content, process and results, told straight.</p></div>
      <div class="card"><h3>Silent Service Trading</h3><p>The software platform: tools for NinjaTrader traders, built and supported by the developer who uses them.</p></div>
      <a class="card" href="/command-center/"><h3>Command Center</h3><p>The flagship NinjaTrader&nbsp;8 application for trading, monitoring, planning and reviewing every account.</p><span class="more">See Command Center &rarr;</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <h2>What we believe</h2>
    <ul>
      <li><strong>You make the decisions.</strong> Command Center copies and protects the trades you place. Playbooks alert; they never enter for you.</li>
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
     "Silent Service Trading is the software platform of The Submarine Vet, a submarine veteran who trades futures. Command Center is its flagship product.",
     "/about/", about)

# ------------------------------------------------------------------ SUPPORT
support = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Support</p>
    <h1>Help with Command Center.</h1>
    <p class="lead">Getting started, requirements, answers to common questions, and a direct line to the developer.</p>
  </div>
</section>

<section class="section" id="getting-started" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Getting started</p><h2>From checkout to your first copied trade.</h2></div>
    <ol class="steps">
      <li><strong>Check your email</strong>Your license key and download link arrive by email after checkout. During early access they're sent personally, usually within a few hours.</li>
      <li><strong>Install</strong>In NinjaTrader&nbsp;8: Tools → Import → NinjaScript Add-On, choose the file, then restart NinjaTrader.</li>
      <li><strong>Enter your key</strong>Open Command Center from NinjaTrader's New menu and paste your license key.</li>
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
        <li>One license key <span>for up to 2 machines</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="faq" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">FAQ</p><h2>Straight answers.</h2></div>
    <div class="faq">
      <details><summary>Does Command Center trade for me?</summary><div><p>No. You place the trades — by hand, or with your own NinjaTrader strategies. Command Center copies them to your other accounts and enforces the limits you set. Playbooks only alert and mark the chart.</p></div></details>
      <details><summary>Is a trade copier allowed by my prop firm?</summary><div><p>Rules differ by firm and change over time. Some firms allow copying between your own accounts, some restrict it, and some limit automated trading. Check your firm's current rules before you copy to its accounts — you're responsible for following them.</p></div></details>
      <details><summary>Does my computer need to stay on?</summary><div><p>Yes. Command Center runs inside NinjaTrader, so NinjaTrader must be open and connected while you trade. Many traders use a Windows VPS.</p></div></details>
      <details><summary>Which accounts does it work with?</summary><div><p>Any account you can trade in NinjaTrader&nbsp;8, including prop-firm accounts connected there and NinjaTrader's simulation accounts.</p></div></details>
      <details><summary>Can I try it without risking money?</summary><div><p>Yes, and you should. Set it up on simulation accounts first, test your copier group and rules, then move to live accounts.</p></div></details>
      <details><summary>Do you see my account data?</summary><div><p>No. Your accounts, balances and positions stay inside NinjaTrader on your machine. The license check sends only your license key and a machine ID.</p></div></details>
      <details><summary>How do I move my license to a new computer?</summary><div><p>Each license runs on up to 2 machines. <a href="mailto:{EMAIL}">Email us</a> and we'll free up a seat.</p></div></details>
      <details><summary>How do I cancel or change my plan?</summary><div><p><a href="mailto:{EMAIL}">Email us</a> from the address you used at checkout. Monthly and annual plans run to the end of the period you've paid for.</p></div></details>
      <details><summary>What's the difference between "Available", "In testing" and "Planned"?</summary><div><p>Available features are in the current release. In-testing features are built and finishing testing before release. Planned features are on the roadmap and not yet in the product — buy for what's available today.</p></div></details>
    </div>
  </div>
</section>"""

page("/support/", "Support — Command Center | Silent Service Trading",
     "Get started with Command Center for NinjaTrader 8: installation, requirements, frequently asked questions and direct support from the developer.",
     "/support/", support)

# ------------------------------------------------------------------ THANKS (URL must not change: Stripe redirect)
thanks = f"""<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Payment received</p>
    <h1>Welcome aboard.</h1>
    <p class="lead">Thanks for joining the early-access crew. Your receipt from Stripe is on its way to the email you used at checkout.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">What happens next</p><h2>Four steps to your first copied trade.</h2></div>
    <ol class="steps">
      <li><strong>Watch your inbox</strong>Your license key and download link arrive by email. During early access they're sent personally, usually within a few hours. Check spam too.</li>
      <li><strong>Install</strong>In NinjaTrader&nbsp;8: Tools → Import → NinjaScript Add-On, choose the file, then restart NinjaTrader.</li>
      <li><strong>Enter your key</strong>Open Command Center from NinjaTrader's New menu and paste your license key.</li>
      <li><strong>Start on Sim</strong>Set your prop rules and copier group on simulation accounts first. Go live when you trust it.</li>
    </ol>
    <p class="muted" style="margin-top:36px">Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your order email, or visit <a href="/support/">Support</a>.</p>
  </div>
</section>"""
page("/command-center/thanks/", "Welcome aboard — Command Center | Silent Service Trading",
     "Thanks for your purchase. Here's how to install Command Center and get started.", "", thanks, noindex=True)

# ------------------------------------------------------------------ 404
nf = """<section class="page-hero" style="border-bottom:none;min-height:56vh">
  <div class="wrap">
    <p class="eyebrow">404</p>
    <h1>That page isn't here.</h1>
    <p class="lead">It may have moved when the site was redesigned.</p>
    <div class="btn-row" style="margin-top:28px">
      <a class="btn btn-primary" href="/">Go home</a>
      <a class="btn btn-secondary" href="/command-center/">Command Center</a>
      <a class="btn btn-secondary" href="/support/">Support</a>
    </div>
  </div>
</section>"""
page("/404.html", "Page not found | Silent Service Trading", "Page not found.", "", nf, noindex=True)
