"""Apple-inspired homepage (index.html) and websites page (websites.html).

Design notes (after Apple's HIG and apple.com): one idea per tile, large tight headlines, a one-line
subhead, two calls to action per tile (a filled pill and a text link with a chevron), generous space,
alternating light and dark tiles with a 12px seam, and a quiet, dense footer. Beyond Branding red
replaces Apple's link blue as the single accent.
"""
import html, os
from urllib.parse import quote

E = lambda s: html.escape(s, quote=True)
WA = "https://wa.me/19108301588"
HOME = "index.html"
def wa(m): return WA + "?text=" + quote(m)

# Short, declarative tile lines (homepage copy)
LINES = {
    "dubai-media-office": "Clarity, at government scale.",
    "marriott-indore": "Hospitality, to take home.",
    "valdaria": "A new name with instant pedigree.",
    "doubletree-by-hilton": "A global standard. Made local.",
    "indian-kawfee-co": "Picked up before it's tasted.",
    "manek": "Trust, before the fabric is touched.",
    "aeroengines-america": "Credible from across the hall.",
    "xess": "Energy storage, easy to follow.",
    "dhanraj-jain-jewellers": "Trust, built across the counter.",
    "esperti": "Built from experience. Now it shows.",
    "soul-av": "The right AV, before the first call.",
    "pihoco": "Every dish is a business decision.",
    "tara-and-tot": "Made for memories that last forever.",
    "aiolec": "Commercial displays you can turn in your hand.",
    "sd-med-solutions": "Credibility, before the first sample ships.",
    "market-lens": "Stock research that reads like a trading app.",
}
GRID = ["marriott-indore", "valdaria", "doubletree-by-hilton", "indian-kawfee-co", "manek", "aeroengines-america",
        "tara-and-tot", "dhanraj-jain-jewellers", "xess", "colorado-windows-direct", "overcmr", "pride-of-cows"]

WHY = [
    ("lead", "A senior lead on every project.", "The person who pitches your project is the person who designs it. No hand-offs to juniors."),
    ("tag", "Prices you can see before you ask.", "Every service has a published starting price. Your quote is agreed before any work begins."),
    ("bolt", "Days, not months.", "A dedicated production team behind every project means premium work at a pace that suits launches."),
    ("globe", "One studio. Three cities.", "London, Dubai and Mumbai, working with clients across the UK, US, Middle East and India."),
    ("layers", "From print to pixels.", "Identity, packaging, exhibitions and websites under one roof, so everything looks like one brand."),
    ("chat", "One message away.", "No forms that disappear. Send a WhatsApp and talk to the person doing the work."),
]
ICONS = {
    "lead": '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1.2-3.6 3.8-5.5 7-5.5s5.8 1.9 7 5.5"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="7.5" cy="8" r="1.4"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3 13 9 5 9-5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4V5z"/>',
}
SERVICES = [("identity", "Brand Identity", "Logo, type, colour and guidelines.", "$500"),
            ("packaging", "Packaging", "From one product to a full range.", "$400"),
            ("web", "Websites", "Landing pages to full sites, built in-house.", "$800"),
            ("events", "Exhibitions & Events", "Booths, stages and conference graphics.", "$800"),
            ("campaigns", "Campaigns & Social", "Print, digital ads and social systems.", "$150"),
            ("collateral", "Brochures", "Catalogues, profiles and sales decks.", "$400")]
LOGOS = [("BEYONDCLIENTS-03.svg", "Government of Dubai Media Office"), ("BEYONDCLIENTS-02.svg", "Marriott"),
         ("BEYONDCLIENTS-01.svg", "Radisson"), ("BEYONDCLIENTS-04.svg", "Sunset Hospitality Group"),
         ("BEYONDCLIENTS-06.svg", "WazirX"), ("BEYONDCLIENTS-05.svg", "Wemasy")]

CSS = r"""
:root{
  /* Apple-style tiles: light #F5F5F7 / dark #000 alternating, 12px seams, one red accent. */
  --bg:#FFFFFF; --tile:#F5F5F7; --dark:#000000; --dark-2:#161617; --ink:#1D1D1F; --muted:#6E6E73; --muted-d:#A1A1A6;
  --red:#D91C2B; --red-h:#B8131F; --line:rgba(0,0,0,.08); --seam:12px;
  --display:'Inter',system-ui,-apple-system,'SF Pro Display',sans-serif; --brand:'Archivo',sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}html.lenis{scroll-behavior:auto}
body{background:var(--bg);color:var(--ink);font-family:var(--display);-webkit-font-smoothing:antialiased;overflow-x:hidden;font-feature-settings:"ss01","cv11"}
img{max-width:100%;display:block}
h1,h2,h3{text-wrap:balance}
a{color:inherit;text-decoration:none}
::selection{background:var(--red);color:#fff}
:focus-visible{outline:2px solid var(--red);outline-offset:3px;border-radius:4px}

/* global nav */
.gn{position:sticky;top:0;z-index:50;height:calc(48px + env(safe-area-inset-top));padding:env(safe-area-inset-top) max(16px,env(safe-area-inset-right)) 0 max(16px,env(safe-area-inset-left));
  background:rgba(255,255,255,.8);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--line)}
.gn .in{max-width:1024px;height:48px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px}
.gn .logo{font-family:var(--brand);font-weight:800;font-size:.95rem;letter-spacing:.02em;white-space:nowrap}
.gn .logo em{font-style:normal;color:var(--red)}
.gn nav{display:flex;gap:clamp(16px,3vw,34px);font-size:.78rem;color:rgba(0,0,0,.8)}
.gn nav a:hover{color:#000}
.gn .go{font-size:.78rem;font-weight:500;color:#fff;background:var(--red);padding:6px 14px;border-radius:100px;white-space:nowrap}
.gn .go:hover{background:var(--red-h)}
@media(max-width:820px){.gn nav{display:none}}

/* shared type */
.eyebrow{font-size:clamp(.95rem,1.4vw,1.2rem);font-weight:600;color:var(--red);margin-bottom:8px}
.h-xl{font-size:clamp(2.6rem,6.4vw,5rem);font-weight:700;letter-spacing:-.028em;line-height:1.04}
.h-l{font-size:clamp(2rem,4.6vw,3.5rem);font-weight:700;letter-spacing:-.024em;line-height:1.07}
.h-m{font-size:clamp(1.7rem,3.2vw,2.5rem);font-weight:700;letter-spacing:-.02em;line-height:1.1}
.sub{font-size:clamp(1.1rem,2vw,1.6rem);line-height:1.3;letter-spacing:-.01em;font-weight:400;margin-top:8px}
.sub.s{font-size:clamp(1.02rem,1.6vw,1.3rem)}
.ctas{display:flex;justify-content:center;align-items:center;gap:14px 26px;flex-wrap:wrap;margin-top:22px}
.pill{display:inline-block;background:var(--red);color:#fff;font-size:1.02rem;font-weight:500;padding:11px 22px;border-radius:100px;transition:background .25s}
.pill:hover{background:var(--red-h)}
.pill.o{background:transparent;color:var(--red);box-shadow:inset 0 0 0 1.5px var(--red)}
.pill.o:hover{background:var(--red);color:#fff}
.lk{font-size:1.02rem;color:var(--red);font-weight:500}
.lk::after{content:" ›";font-size:1.15em}
.lk:hover{text-decoration:underline}
.dark .lk{color:#FF5A66}
.dark .pill.o{color:#fff;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.7)}

/* tiles */
.tiles{display:grid;gap:var(--seam);padding:var(--seam) 0 0}
.tile{position:relative;overflow:hidden;text-align:center;background:var(--tile);color:var(--ink)}
.tile.dark{background:var(--dark);color:#F5F5F7}
.tile.dark .sub{color:#F5F5F7}
.tile .copy{position:relative;z-index:2;padding:clamp(44px,6vw,64px) max(20px,4vw) 0}
.full{min-height:clamp(560px,62vw,720px);display:flex;flex-direction:column}
.full .media{flex:1;display:flex;align-items:flex-end;justify-content:center;padding:clamp(28px,4vw,44px) max(16px,4vw) 0}
.half-grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--seam);padding-inline:var(--seam)}
.half{min-height:clamp(480px,48vw,620px);display:flex;flex-direction:column}
.half .copy{padding-top:clamp(40px,5vw,56px)}
.half .h-m{font-size:clamp(1.6rem,2.8vw,2.4rem)}
.half .media{flex:1;margin-top:26px;position:relative;min-height:260px}
.half .media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.19,1,.22,1)}
.half:hover .media img{transform:scale(1.035)}
@media(max-width:760px){.half-grid{grid-template-columns:1fr;padding-inline:0}.half{min-height:520px}}
@media(max-width:760px){.full{min-height:0}.full .media{padding-top:30px}.pair{gap:8px}}

.browser{width:min(980px,100%);border-radius:14px 14px 0 0;overflow:hidden;background:#1d1d1f;box-shadow:0 30px 80px -30px rgba(0,0,0,.45)}
.browser .c{height:28px;display:flex;align-items:center;gap:6px;padding:0 12px;background:#2a2a2c}
.browser .c i{width:9px;height:9px;border-radius:50%;background:#5a5a5e}
.browser img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top}
.browser .url{margin-left:10px;flex:1;max-width:260px;height:18px;border-radius:9px;background:#1d1d1f;color:#a1a1a6;font-size:11px;line-height:18px;text-align:center;letter-spacing:.01em}
.browser .ph{aspect-ratio:16/10;display:grid;place-content:center;gap:10px;text-align:center;padding:24px;background:radial-gradient(120% 90% at 50% 0%,#26262a,#0b0d0e);color:#f5f5f7}
.browser .ph b{font-size:clamp(34px,6vw,72px);letter-spacing:-.04em;line-height:1}
.browser .ph span{font-size:13px;color:#a1a1a6}
.browser .ph em{font-style:normal;display:inline-flex;align-items:center;gap:8px;justify-self:center;font-size:12px;color:#f5f5f7;border:1px solid #3a3a3e;border-radius:99px;padding:6px 12px}
.browser .ph em:before{content:"";width:7px;height:7px;border-radius:50%;background:#2fd06b}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px;width:min(980px,100%)}
.pair img{width:100%;aspect-ratio:4/4.2;object-fit:cover;border-radius:18px 18px 0 0}

/* hero */
.hero{background:var(--bg);text-align:center;padding:clamp(56px,8vw,96px) 0 0;overflow:hidden}
.hero .copy{padding-inline:max(20px,4vw)}
.hero .sub{color:var(--ink);max-width:30ch;margin-inline:auto}
.ribbon{margin-top:clamp(40px,6vw,64px);overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
.ribbon .row{display:flex;gap:16px;width:max-content;animation:rb 60s linear infinite;padding-bottom:8px}
.ribbon:hover .row{animation-play-state:paused}
.ribbon a{flex:0 0 auto;width:clamp(200px,21vw,300px);aspect-ratio:4/5;border-radius:22px;overflow:hidden;position:relative;background:var(--tile)}
.ribbon img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.19,1,.22,1)}
.ribbon a:hover img{transform:scale(1.05)}
.ribbon span{position:absolute;left:14px;bottom:12px;color:#fff;font-size:.82rem;font-weight:600;text-shadow:0 1px 10px rgba(0,0,0,.5)}
@keyframes rb{to{transform:translateX(-50%)}}
.trust{padding:28px 20px 6px;display:flex;justify-content:center;align-items:center;gap:clamp(20px,4vw,52px);flex-wrap:wrap}
.trust small{width:100%;text-align:center;font-size:.8rem;color:var(--muted);margin-bottom:2px}
.trust img{height:40px;width:auto;filter:grayscale(1) brightness(.2);opacity:.55}

/* sections */
.sec{padding:clamp(88px,11vw,150px) max(16px,3vw) 0;max-width:1240px;margin:0 auto}
.sec-t{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.sec-t h2{font-size:clamp(2rem,4vw,3rem);font-weight:700;letter-spacing:-.024em;line-height:1.08;max-width:18ch}
.sec-t h2 span{color:var(--muted)}

/* why cards: horizontal scroll */
.why{--edge:calc(max(0px,(100vw - 1240px)/2) + max(16px,3vw));display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px var(--edge) 30px;scroll-padding-inline:var(--edge);scrollbar-width:none;max-width:none}
.why::-webkit-scrollbar{display:none}
.why .card{flex:0 0 clamp(260px,26vw,340px);scroll-snap-align:start;background:var(--tile);border-radius:22px;padding:30px 28px 34px;min-height:300px;display:flex;flex-direction:column;
  transition:transform .4s cubic-bezier(.19,1,.22,1),box-shadow .4s}
.why .card:hover{transform:scale(1.015);box-shadow:0 14px 34px rgba(0,0,0,.08)}
.why svg{width:34px;height:34px;stroke:var(--red);fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;margin-bottom:auto}
.why h3{font-size:1.45rem;font-weight:700;letter-spacing:-.018em;line-height:1.15;margin:44px 0 10px}
.why p{font-size:.98rem;line-height:1.5;color:var(--muted)}
.why-wrap{max-width:none}
.why-wrap .sec-t{max-width:1240px;margin:0 auto 28px;padding:0 max(16px,3vw)}
.why-nav{display:flex;gap:10px}
.why-nav button{width:38px;height:38px;border-radius:50%;border:0;background:var(--tile);color:var(--ink);font-size:1.1rem;cursor:pointer}
.why-nav button:hover{background:#e8e8ed}

/* services */
.svc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.svc a{background:var(--tile);border-radius:22px;padding:28px;display:flex;flex-direction:column;min-height:210px;transition:transform .4s cubic-bezier(.19,1,.22,1),box-shadow .4s}
.svc a:hover{transform:scale(1.015);box-shadow:0 14px 34px rgba(0,0,0,.08)}
.svc h3{font-size:1.3rem;font-weight:700;letter-spacing:-.015em}
.svc p{font-size:.96rem;color:var(--muted);margin-top:6px;line-height:1.45}
.svc .pr{margin-top:auto;padding-top:20px;display:flex;justify-content:space-between;align-items:baseline}
.svc .pr b{font-size:1.5rem;font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.svc .pr b small{font-size:.8rem;font-weight:500;color:var(--muted);margin-right:5px}
.svc .pr span{color:var(--red);font-size:.95rem;font-weight:500}
@media(max-width:860px){.svc{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.svc{grid-template-columns:1fr}.svc a{min-height:0}}

/* founder */
.founder{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);text-align:left;align-items:stretch}
.founder .ph{min-height:420px;position:relative}
.founder .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 30%}
.founder .copy{padding:clamp(44px,6vw,90px) clamp(24px,5vw,80px);display:flex;flex-direction:column;justify-content:center}
.founder q{font-size:clamp(1.6rem,3vw,2.6rem);font-weight:700;letter-spacing:-.022em;line-height:1.12;quotes:none}
.founder p{font-size:1.05rem;line-height:1.6;color:var(--muted-d);margin-top:18px;max-width:46ch}
.founder .who{margin-top:24px;font-size:.95rem;color:#F5F5F7}
.founder .who b{font-weight:600}
.founder .ctas{justify-content:flex-start}
@media(max-width:760px){.founder{grid-template-columns:1fr}.founder .ph{min-height:380px}}

/* closing */
.close{text-align:center;padding:clamp(90px,12vw,150px) max(20px,4vw)}
.close .h-xl{max-width:16ch;margin:0 auto}
.close .sub{color:var(--muted);max-width:36ch;margin:14px auto 0}
.close .lines{margin-top:22px;font-size:.95rem;color:var(--muted)}
.close .lines a{color:var(--ink);user-select:all}

/* footer */
.ft{background:var(--tile);color:var(--muted);font-size:.76rem;line-height:1.4}
.ft .in{max-width:1024px;margin:0 auto;padding:20px max(16px,4vw) calc(26px + env(safe-area-inset-bottom))}
.ft .note{padding-bottom:16px;border-bottom:1px solid #d2d2d7}
.ft .cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;padding:20px 0;border-bottom:1px solid #d2d2d7}
.ft h4{font-size:.76rem;color:var(--ink);font-weight:600;margin-bottom:8px}
.ft .cols a{display:block;margin-bottom:7px}
.ft .cols a:hover{color:var(--ink);text-decoration:underline}
.ft .legal{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;padding-top:14px}
@media(max-width:700px){.ft .cols{grid-template-columns:1fr 1fr}}

/* websites page bits */
.wcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,330px),1fr));gap:18px}
.wcard{background:var(--tile);border-radius:22px;overflow:hidden;display:flex;flex-direction:column;transition:transform .4s cubic-bezier(.19,1,.22,1),box-shadow .4s}
.wcard:hover{transform:scale(1.012);box-shadow:0 14px 34px rgba(0,0,0,.08)}
.wcard .im{aspect-ratio:16/11;overflow:hidden;background:#e8e8ed}
.wcard .im img{width:100%;height:100%;object-fit:cover}
.wcard .tx{padding:22px 24px 26px;display:flex;flex-direction:column;flex:1}
.wcard small{font-size:.78rem;color:var(--muted);font-weight:500}
.wcard h3{font-size:1.3rem;font-weight:700;letter-spacing:-.015em;margin:4px 0 6px}
.wcard p{font-size:.96rem;color:var(--muted);line-height:1.5}
.wcard .lk{margin-top:auto;padding-top:16px;font-size:.95rem}
.incl{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px 28px}
.incl div{border-top:1px solid #d2d2d7;padding-top:18px}
.incl h3{font-size:1.1rem;font-weight:700;letter-spacing:-.01em;margin-bottom:6px}
.incl p{font-size:.95rem;color:var(--muted);line-height:1.5}
@media(max-width:760px){.incl{grid-template-columns:1fr}}
.tiers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.tier{border-radius:22px;padding:30px 28px;background:var(--tile);display:flex;flex-direction:column;gap:6px}
.tier.hi{background:var(--dark);color:#F5F5F7}
.tier small{font-size:.82rem;color:var(--muted);font-weight:500}
.tier.hi small,.tier.hi p{color:var(--muted-d)}
.tier h3{font-size:1.4rem;font-weight:700;letter-spacing:-.015em}
.tier b{font-size:2rem;font-weight:700;letter-spacing:-.025em;margin:12px 0 4px;font-variant-numeric:tabular-nums}
.tier p{font-size:.95rem;color:var(--muted);line-height:1.5}
.tier .pill{margin-top:22px;align-self:flex-start;font-size:.95rem}
@media(max-width:860px){.tiers{grid-template-columns:1fr}}

.js .rv{opacity:0;transform:translateY(24px);transition:opacity .9s cubic-bezier(.19,1,.22,1),transform .9s cubic-bezier(.19,1,.22,1)}
.js .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.ribbon .row{animation:none}.js .rv{opacity:1;transform:none}}
"""

JS_OLD = r"""
(function(){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
  var why=document.querySelector('.why');
  document.querySelectorAll('.why-nav button').forEach(function(b){b.addEventListener('click',function(){why.scrollBy({left:(b.dataset.d==='r'?1:-1)*why.clientWidth*.8,behavior:'smooth'})})});
})();
"""

from home_parts import CSS2, JS2
CSS = CSS + CSS2
JS = JS2

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'


def head(title, desc, site, path):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{site}/{path}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{site}/assets/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
{FONTS}
<script>document.documentElement.classList.add('js')</script>
<style>{CSS}</style>
</head>
<body>
<header class="gn"><div class="in">
  <a class="logo" href="{HOME}">BEYOND<em>BRANDING</em></a>
  <nav><a href="portfolio.html">Work</a><a href="websites.html">Websites</a><a href="{HOME}#services">Services</a><a href="packages-global/index.html">Pricing</a><a href="{HOME}#about">About</a></nav>
  <a class="go" href="{wa('Hi Ayush, I would like to start a project.')}" target="_blank" rel="noopener">Start a project</a>
</div></header>
"""


def footer():
    return f"""<footer class="ft"><div class="in">
  <p class="note">Starting prices are in US dollars and exclude printing, fabrication and third-party costs. Every quote is scoped to your brief and agreed before work begins.</p>
  <div class="cols">
    <div><h4>Work</h4><a href="portfolio.html">All projects</a><a href="websites.html">Websites</a><a href="portfolio.html#identity">Brand identity</a><a href="portfolio.html#packaging">Packaging</a><a href="portfolio.html#events">Exhibitions</a></div>
    <div><h4>Services</h4><a href="packages-global/index.html#identity">Identity</a><a href="packages-global/index.html#packaging">Packaging</a><a href="packages-global/index.html#web">Websites</a><a href="packages-global/index.html#campaigns">Campaigns</a><a href="packages-global/index.html">All pricing</a></div>
    <div><h4>Studio</h4><a href="{HOME}#about">About Ayush</a><a href="{HOME}#why">Why Beyond Branding</a><span>London · Dubai · Mumbai</span></div>
    <div><h4>Contact</h4><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><a href="mailto:ayush@beyondbranding.media">Email</a><a href="https://instagram.com/beyondbranding.media" target="_blank" rel="noopener">Instagram</a><a href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">LinkedIn</a></div>
  </div>
  <div class="legal"><span>Copyright © 2026 Beyond Branding. All rights reserved.</span><span>beyondbranding.media</span></div>
</div></footer>
<script src="assets/js/lenis.min.js"></script>
<script>{JS}</script>
</body>
</html>
"""


LEADS = ["soul-av", "esperti"]


def lead_sites(projects):
    by = {p["slug"]: p for p in projects}
    return [by[s] for s in LEADS if s in by]


def _live(p):
    return p.get("url") or (p.get("demo") and p["demo"])


STATUS = {"aiolec": "Launch-ready build", "market-lens": "Web app", "sd-med-solutions": "Website", "pihoco": "Website"}


def _dom(p):
    return (p.get("url") or "").replace("https://", "").replace("http://", "").rstrip("/")


def screens(p, n=3):
    sc = p.get("showcase")
    if sc:
        return [sc["hero"]] + [x[0] for x in sc["sections"][:n - 1]]
    return ["assets/" + p["images"][0][0]]


def browser_frame(p, n=3, light=False):
    dom = _dom(p) or (p["client"] + " · " + STATUS.get(p["slug"], "Website"))
    imgs = "".join(f'<img src="{src}" alt="{E(p["client"])} website screen {i + 1}" loading="{"eager" if i == 0 else "lazy"}"{" class=\"on\"" if i == 0 else ""}>'
                   for i, src in enumerate(screens(p, n)))
    return (f'<div class="browser{" light" if light else ""}"><div class="c"><i></i><i></i><i></i><span class="url">{E(dom)}</span></div>'
            f'<div class="scr" data-cycle>{imgs}</div></div>')


def web_card(p, cls, d=0):
    live = p.get("url")
    line = LINES.get(p["slug"], p["hook"])
    ey = (f'<span class="live">Live</span><span>{E(_dom(p))}</span>' if live
          else f'<span>{E(p["industry"])} · {E(STATUS.get(p["slug"], "Website"))}</span>')
    links = f'<a class="pill" href="work/{p["slug"]}.html">Case study</a>'
    if live:
        links += f'<a class="lk" href="{live}" target="_blank" rel="noopener">Visit site</a>'
    desc = f'<p class="d">{E(p["summary"].split(". ")[0].rstrip("."))}.</p>' if "big" in cls else ""
    return f"""<div class="card hov {cls} rv" style="--d:{d}s">
  <div class="cp"><div class="ey">{ey}</div><h3>{E(p['client'])}</h3>{('<p class="d">' + E(line) + '</p>') if not desc else desc}<div class="ctas">{links}</div></div>
  <div class="md"><div class="par">{browser_frame(p)}</div></div>
</div>"""


def feature_tile(p, dark=False):
    """Websites page: full-width card per showcase project."""
    return f'<div class="grid" style="margin-bottom:16px">{web_card(p, "c12 big")}</div>'


def image_card(p, cls, d=0, img=None):
    line = LINES.get(p["slug"], p["hook"])
    src = img or p["images"][0][0]
    return f"""<a class="card im {cls} rv" style="--d:{d}s" href="work/{p['slug']}.html">
  <img class="bg" src="assets/{src}" alt="{E(p['images'][0][1])}" loading="lazy">
  <div class="cp"><div class="ey">{E(p['industry'])}</div><h3>{E(p['client'])}</h3><p class="d">{E(line)}</p></div>
</a>"""


def build_home(projects, site):
    by = {p["slug"]: p for p in projects}
    real = [p for p in projects if not p.get("_pending")]
    logos = "".join(f'<img src="assets/{f}" alt="{a}">' for f, a in LOGOS)
    soul, esp = by.get("soul-av"), by.get("esperti")

    def phone(p):
        if not p or not p.get("showcase"): return ""
        return f'<img src="{p["showcase"]["mobiles"][0]}" alt="{E(p["client"])} on mobile" loading="eager">'
    stage = ""
    if soul:
        stage = f"""<div class="stage" aria-label="Recent website work">
    <span class="tag">Live now · {E(_dom(soul))}</span>
    {browser_frame(soul)}
    {('<div class="phone l">' + phone(esp) + '</div>') if esp else ''}
    {('<div class="phone r">' + phone(by.get('aiolec')) + '</div>') if by.get('aiolec') else ''}
  </div>"""

    webs = [by[s] for s in ("soul-av", "esperti") if s in by]
    smalls = [by[s] for s in ("aiolec", "sd-med-solutions", "market-lens") if s in by]
    web_html = "".join(web_card(p, "c6 big", i * .08) for i, p in enumerate(webs))
    web_html += "".join(web_card(p, "c4 sm", i * .08) for i, p in enumerate(smalls))

    brand_layout = [("dubai-media-office", "c8 tall"), ("marriott-indore", "c4 tall"), ("tara-and-tot", "c4", "tara-and-tot-identity-3.webp"), ("overcmr", "c4"),
                    ("valdaria", "c4"), ("indian-kawfee-co", "c6"), ("doubletree-by-hilton", "c6")]
    brand_html = "".join(image_card(by[t[0]], t[1], (i % 3) * .08, t[2] if len(t) > 2 else None) for i, t in enumerate(brand_layout) if t[0] in by)
    why = "".join(f'<div class="card"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg><h3>{E(t)}</h3><p>{E(d)}</p></div>' for k, t, d in WHY)
    svcs = "".join(f'<a href="packages-global/index.html#{k}" class="rv" style="--d:{(i % 3) * .06}s"><h3>{E(n)}</h3><p>{E(d)}</p><div class="pr"><b><small>From</small>{pr}</b><span>Learn more ›</span></div></a>' for i, (k, n, d, pr) in enumerate(SERVICES))
    words = "".join(f'<span class="w" style="transition-delay:{i * .07:.2f}s">{w}</span> ' for i, w in enumerate("Brands that look the part.".split()))

    col_a = ["soul-av-1.webp", "dubai-media-office-stage.webp", "marriott-indore-hamper.webp", "esperti-1.webp", "colorado-windows-newspaper-ad.webp",
             "overcmr-paddles-display.webp", "aeroengines-america-booth.webp", "stanfords-real-estate-poolside.webp", "xess-conference-stage.webp", "indian-kawfee-jar.webp"]
    col_b = ["doubletree-hilton-signage.webp", "aiolec-1.webp", "gowardhan-ghee-amazon.webp", "dubai-media-office-instagram.webp", "valdaria-exhibition-booth.webp",
             "manek-brochure-bag.webp", "sd-med-solutions-1.webp", "pride-of-cows-retail-signage.webp", "dhanraj-jain-jewellers-counter.webp", "market-lens-1.webp"]
    alt_of = {}
    for p in real:
        for f, a_ in p["images"]:
            alt_of[f] = (p["slug"], a_)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def gi(f, eager):
        if not os.path.exists(os.path.join(root_dir, "assets", f)): return ""
        slug, alt = alt_of.get(f, ("", f))
        href = f"work/{slug}.html" if slug else "portfolio.html"
        return f'<a class="gi" href="{href}" tabindex="-1"><img src="assets/{f}" alt="{E(alt)}" loading="{"eager" if eager else "lazy"}"></a>'
    def col(files, rev):
        items = "".join(gi(f, i < 3) for i, f in enumerate(files))
        return f'<div class="gcol"><div class="gtrk{" rev" if rev else ""}">{items}{items.replace(chr(34) + "eager" + chr(34), chr(34) + "lazy" + chr(34))}</div></div>'
    gal_cols = col(col_a, False) + col(col_b, True)
    row_items = "".join(gi(f, False) for f in [x for pair in zip(col_a, col_b) for x in pair])
    gal_row = row_items + row_items
    out = head("Beyond Branding · Brand, Packaging & Website Design Studio",
               "Beyond Branding is a brand and design studio in London, Dubai and Mumbai. Websites, identity, packaging and exhibitions for Marriott, DoubleTree by Hilton, Dubai Media Office and growing brands.",
               site, "")
    out += f"""<main>
<section class="bbh" aria-label="Beyond Branding">
  <div class="bbh-copy">
    <h1 class="rv"><span class="r">FAST IDEAS. PREMIUM DESIGN.</span><br>ON TIME, EVERY TIME.<span class="shine" aria-hidden="true">FAST IDEAS. PREMIUM DESIGN.<br>ON TIME, EVERY TIME.</span></h1>
    <p class="rv" style="--d:.12s">Branding, packaging, websites and campaigns for hospitality, retail and growing brands across the UK, US and Middle East. Fast execution. Premium craft. No unnecessary layers.</p>
    <div class="rv" style="--d:.2s"><a class="bbcta" href="{wa('Hi Ayush, I would like to start a project.')}" target="_blank" rel="noopener"><span>&#8863;</span>Start a project</a></div>
    <div class="bbrule rv" style="--d:.26s"></div>
    <div class="bblogos rv" style="--d:.3s">{logos}</div>
  </div>
  <div class="bbh-gal" aria-label="Recent work">
    {gal_cols}
    <a class="bbexplore" href="portfolio.html"><span>&#8863;</span>Explore our work</a>
  </div>
  <div class="bbh-row" aria-hidden="true"><div class="trk">{gal_row}</div></div>
  <div class="bbh-mcta"><a class="bbexplore" href="portfolio.html"><span>&#8863;</span>Explore our work</a></div>
</section>

<section class="sec2" id="websites">
  <div class="head2 rv"><h2>Websites that win the work.</h2><p>Designed, written and built in-house. Two are live right now.</p></div>
  <div class="wrap"><div class="grid">{web_html}</div>
  <div class="more rv"><a class="lk" href="websites.html">All website work</a></div></div>
</section>

<section class="sec2">
  <div class="wrap"><div class="stats rv">
    <div><b>8+</b><span>years of brand work</span></div>
    <div><b>{len(real)}</b><span>case studies</span></div>
    <div><b>3</b><span>studios: London, Dubai, Mumbai</span></div>
    <div><b>$500</b><span>projects from</span></div>
  </div></div>
</section>

<section class="sec2" id="work">
  <div class="head2 rv"><h2>Brand, packaging and print.</h2><p>Identity systems, packaging, exhibitions and campaigns for global names and growing brands.</p></div>
  <div class="wrap"><div class="grid">{brand_html}</div>
  <div class="more rv"><a class="lk" href="portfolio.html">Explore all {len(real)} projects</a></div></div>
</section>

<section class="sec why-wrap" id="why" style="max-width:none;padding-inline:0">
  <div class="sec-t rv"><h2>Why Beyond Branding. <span>The short version.</span></h2><div class="why-nav"><button data-d="l" aria-label="Previous">‹</button><button data-d="r" aria-label="Next">›</button></div></div>
  <div class="why">{why}</div>
</section>

<section class="sec" id="services">
  <div class="sec-t rv"><h2>Find the right service. <span>See the price first.</span></h2><a class="lk" href="packages-global/index.html">Compare all packages</a></div>
  <div class="svc">{svcs}</div>
</section>

<section class="sec2" id="about"><div class="wrap">
  <div class="founder2 rv">
    <div class="ph"><img src="assets/founder-ayush.jpg" alt="Ayush, founder of Beyond Branding" loading="lazy"></div>
    <div class="copy">
      <div class="eyebrow">Meet the founder</div>
      <q>I help brands move faster without compromising quality.</q>
      <p>Eight years designing identities, packaging, campaigns and websites for startups and global names like Marriott, DoubleTree by Hilton and the Dubai Government Media Office. Every project is led by me and produced by a dedicated in-house team.</p>
      <div class="who"><b>Ayush</b> · Founder &amp; Creative Director</div>
      <div class="ctas"><a class="pill o" href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">Connect on LinkedIn</a></div>
    </div>
  </div>
</div></section>

<section class="close">
  <h2 class="h-xl rv">Bring us the brief. We'll bring the direction.</h2>
  <p class="sub s rv">Tell us what you're launching, your timeline and a rough budget. You'll hear back from the person doing the work.</p>
  <div class="ctas rv"><a class="pill" href="{wa("Hi Ayush, I'd like to discuss a project.")}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="mailto:ayush@beyondbranding.media">Email us</a></div>
  <p class="lines"><a href="mailto:ayush@beyondbranding.media">ayush@beyondbranding.media</a> · <a href="{WA}" target="_blank" rel="noopener">+1 (910) 830-1588</a></p>
</section>
</main>
"""
    return out + footer()


def build_websites(projects, site, packages):
    webs = [p for p in projects if "web" in p["filters"]]
    order = ["soul-av", "esperti", "aiolec", "sd-med-solutions", "market-lens", "pihoco"]
    feats = sorted([p for p in webs if p.get("showcase")], key=lambda p: order.index(p["slug"]) if p["slug"] in order else 99)
    others = [p for p in webs if not p.get("showcase") and not p.get("_pending")]
    tiles = '<div class="wrap"><div class="grid">' + "".join(web_card(p, "c6 big", (i % 2) * .08) for i, p in enumerate(feats)) + '</div></div>'
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def card(p):
        web_img = f"assets/web-{p['slug']}.webp"
        img = web_img if os.path.exists(os.path.join(root, web_img)) else "assets/" + p["images"][0][0]
        live = _live(p)
        extra = f' · <a class="lk" href="{live}" target="_blank" rel="noopener" style="padding:0">Live site</a>' if live else ""
        return f"""<div class="wcard rv"><a class="im" href="work/{p['slug']}.html"><img src="{img}" alt="{E(p['images'][0][1])}" loading="lazy"></a>
  <div class="tx"><small>{E(p['industry'])}</small><h3>{E(p['client'])}</h3><p>{E(p['summary'])}</p><div><a class="lk" href="work/{p['slug']}.html">Case study</a>{extra}</div></div></div>"""

    cards = "".join(card(p) for p in others)
    incl = [("Design made for your brand", "No templates. Layouts, type and motion designed around your identity and your customers."),
            ("Built mobile-first", "Most visitors arrive on a phone, so every page is designed and tested there first."),
            ("Words that sell", "Headlines and page copy written with you, so the site explains what you do in seconds."),
            ("Enquiries built in", "WhatsApp, booking and contact flows placed where visitors decide, not hidden in a footer."),
            ("Fast and findable", "Lightweight pages, clean structure and the SEO basics set up from day one."),
            ("Launch and handover", "We help you go live on your domain and hand over everything you need to own it.")]
    incl_html = "".join(f"<div class=\"rv\"><h3>{E(t)}</h3><p>{E(d)}</p></div>" for t, d in incl)
    msg = "Hi Ayush, I'm interested in a new website."
    out = head("Websites · Beyond Branding", "Websites designed and built in-house by Beyond Branding: custom design, mobile-first build and enquiry flows. Landing pages from $800.", site, "websites.html")
    out += f"""<main>
<section class="hero2" style="padding-bottom:clamp(48px,6vw,80px)">
  <div class="eyebrow rv">Websites</div>
  <h1>{"".join(f'<span class="w" style="transition-delay:{i*.07:.2f}s">{w}</span> ' for i, w in enumerate("Websites that work as hard as you do.".split()))}</h1>
  <p class="sub rv" style="--d:.25s">Designed, written and built in-house. Fast, considered and made to bring in enquiries.</p>
  <div class="ctas rv" style="--d:.35s"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Start a website</a><a class="lk" href="#pricing">See pricing</a></div>
</section>
{tiles}

{f'''<section class="sec">
  <div class="sec-t rv"><h2>More web work. <span>From product pages to full sites.</span></h2></div>
  <div class="wcards">{cards}</div>
</section>''' if cards else ''}

<section class="sec">
  <div class="sec-t rv"><h2>Every website includes. <span>No surprises.</span></h2></div>
  <div class="incl">{incl_html}</div>
</section>

<section class="sec" id="pricing">
  <div class="sec-t rv"><h2>Pick your website. <span>Clear prices, agreed up front.</span></h2><a class="lk" href="packages-global/index.html#web">Full pricing</a></div>
  <div class="tiers rv">
    <div class="tier"><small>Single page</small><h3>Landing Page</h3><b>$800–$1,800</b><p>One focused page for a launch, a campaign or a new business. Designed, written and built.</p><a class="pill o" href="{wa('Hi Ayush, I would like a landing page.')}" target="_blank" rel="noopener">Get a quote</a></div>
    <div class="tier hi"><small>Most popular</small><h3>Full Website</h3><b>$2,000–$5,000</b><p>Five to eight pages, matched to your brand, with enquiry flows and SEO basics built in.</p><a class="pill" href="{wa('Hi Ayush, I would like a full website.')}" target="_blank" rel="noopener">Get a quote</a></div>
    <div class="tier"><small>Custom</small><h3>E-commerce &amp; Custom</h3><b>Scoped</b><p>Online stores, 3D and interactive builds, quizzes, calculators and custom tools.</p><a class="pill o" href="{wa('Hi Ayush, I need a custom website build.')}" target="_blank" rel="noopener">Talk to us</a></div>
  </div>
</section>

<section class="close">
  <h2 class="h-xl rv">Your next website starts with one message.</h2>
  <p class="sub s rv">Tell us about your business and what the site needs to do. We'll reply with a direction and a price range.</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="mailto:ayush@beyondbranding.media">Email us</a></div>
</section>
</main>
"""
    return out + footer()
