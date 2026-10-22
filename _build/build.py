#!/usr/bin/env python3
"""Builds portfolio.html, work/*.html and sitemap.xml from _build/projects.py.
Run from anywhere:  python3 _build/build.py
"""
import html, json, os, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from projects import PROJECTS, FILTERS, PACKAGES, WHATSAPP, SITE  # noqa: E402
from showcases import UPDATES, NEW  # noqa: E402
for _p in PROJECTS:
    _p.update(UPDATES.get(_p["slug"], {}))
PROJECTS.extend(NEW)
LEAD_ORDER = ["soul-av", "esperti", "aiolec", "dubai-media-office", "sd-med-solutions", "market-lens", "marriott-indore",
              "tara-and-tot", "overcmr", "pihoco"]
_pos = {p["slug"]: i for i, p in enumerate(PROJECTS)}
PROJECTS.sort(key=lambda p: LEAD_ORDER.index(p["slug"]) if p["slug"] in LEAD_ORDER else 100 + _pos[p["slug"]])

E = lambda s: html.escape(s, quote=True)
FILTER_NAME = dict(FILTERS)
BY_SLUG = {p["slug"]: p for p in PROJECTS}


def wa(msg=None):
    u = f"https://wa.me/{WHATSAPP}"
    return u + ("?text=" + quote(msg) if msg else "")


def place(p):
    return p["industry"] + (f" · {p['location']}" if p.get("location") else "")


# --------------------------------------------------------------------------- shared
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800&family=Bebas+Neue&display=swap" rel="stylesheet">'

BASE_CSS = r"""
:root{
  --white:#FAF9F7;--ink:#131113;--red:#D91C2B;--red-deep:#A8121E;
  --muted:#6B6864;--muted-on-red:rgba(250,249,247,0.74);
  --line:rgba(19,17,19,0.12);--line-on-red:rgba(250,249,247,0.24);--line-on-ink:rgba(250,249,247,0.14);
  --ease:cubic-bezier(.22,1,.36,1);--ease-soft:cubic-bezier(.16,1,.3,1);--ease-premium:cubic-bezier(.19,1,.22,1);
  --gutter:clamp(20px,6vw,72px);
}
*{margin:0;padding:0;box-sizing:border-box;}
html.lenis{height:auto;}.lenis.lenis-smooth{scroll-behavior:auto;}
body{background:var(--white);color:var(--ink);font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden;}
::selection{background:var(--red);color:var(--white);}
img{max-width:100%;display:block;}
a{color:inherit;}
#grain{position:fixed;inset:0;z-index:900;pointer-events:none;opacity:0.09;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");}
#wipe{position:fixed;inset:0;z-index:2000;background:var(--red);transform:scaleY(0);transform-origin:bottom;pointer-events:none;transition:transform .55s cubic-bezier(.76,0,.24,1);}
#wipe.cover{transform:scaleY(1);}
#topProgress{position:fixed;top:0;left:0;height:2px;background:var(--red);width:0%;z-index:400;}

header.top{position:fixed;top:0;left:0;right:0;z-index:300;height:calc(48px + env(safe-area-inset-top));padding:env(safe-area-inset-top) 22px 0;
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  background:rgba(250,249,247,0.82);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);
  border-bottom:1px solid rgba(19,17,19,0.08);}
header.top .logo{font-family:'Archivo',sans-serif;font-weight:800;font-size:clamp(0.92rem,3.6vw,1.15rem);letter-spacing:0.02em;text-decoration:none;white-space:nowrap;}
header.top .logo em{color:var(--red);font-style:normal;}
header.top nav{display:flex;align-items:center;gap:8px;}
.pill{display:inline-flex;align-items:center;gap:6px;height:30px;padding:0 15px;border-radius:100px;
  font-family:'Inter',sans-serif;font-weight:500;font-size:12.5px;letter-spacing:-0.01em;text-decoration:none;white-space:nowrap;
  background:rgba(19,17,19,0.05);border:1px solid rgba(19,17,19,0.08);
  transition:background .35s var(--ease-premium),color .35s var(--ease-premium),border-color .35s var(--ease-premium);}
.pill:hover{background:var(--ink);color:var(--white);border-color:var(--ink);}
.pill.red{background:var(--red);border-color:var(--red);color:var(--white);}
.pill.red:hover{background:var(--ink);border-color:var(--ink);}
@media(max-width:560px){header.top{padding-left:16px;padding-right:16px;}.pill.hide-sm{display:none;}.pill{padding:0 12px;}}

.cta{display:inline-flex;align-items:center;gap:10px;padding:16px 28px;border-radius:100px;
  font-family:'Archivo',sans-serif;font-weight:700;font-size:0.8rem;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;
  color:var(--white);background:var(--ink);border:1px solid var(--ink);
  transition:transform .5s var(--ease-premium),background .4s var(--ease-premium),box-shadow .5s var(--ease-premium),color .4s,border-color .4s;}
.cta:hover{background:var(--red);border-color:var(--red);box-shadow:0 14px 36px rgba(217,28,43,0.28);transform:translateY(-2px);}
.cta.ghost{background:transparent;color:var(--ink);border-color:rgba(19,17,19,0.22);}
.cta.ghost:hover{background:var(--ink);color:var(--white);border-color:var(--ink);box-shadow:none;}
.cta.light{background:var(--white);color:var(--red-deep);border-color:var(--white);}
.cta.light:hover{background:var(--ink);color:var(--white);border-color:var(--ink);}
.cta.outline-light{background:transparent;color:var(--white);border-color:rgba(250,249,247,0.4);}
.cta.outline-light:hover{background:var(--white);color:var(--ink);border-color:var(--white);box-shadow:none;}
.actions{display:flex;flex-wrap:wrap;gap:12px;}
@media(max-width:480px){.actions .cta{width:100%;justify-content:center;}}

.kicker{display:flex;align-items:center;gap:9px;font-family:'Archivo',sans-serif;font-weight:700;color:var(--red);
  font-size:0.76rem;letter-spacing:0.16em;text-transform:uppercase;}
.kicker::before{content:"";width:8px;height:8px;background:currentColor;flex-shrink:0;}

.frame{position:relative;overflow:hidden;background:#EFEDE9;border-radius:20px;}
.frame img{width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .7s var(--ease-soft),transform .9s var(--ease);}
.frame.loaded img{opacity:1;}
@media(max-width:900px){.frame{border-radius:16px;}}

/* project cards (hub grid + related) */
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(22px,3vw,44px) clamp(18px,2.4vw,36px);}
.card{display:block;text-decoration:none;color:var(--ink);}
.card .frame{aspect-ratio:4/5;transition:box-shadow .6s var(--ease-premium),transform .6s var(--ease-premium);}
.card .frame::after{content:"Case study \2192";position:absolute;left:14px;bottom:14px;z-index:2;
  font-family:'Archivo',sans-serif;font-weight:700;font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
  background:var(--white);color:var(--ink);padding:9px 13px;border-radius:100px;
  opacity:0;transform:translateY(8px);transition:opacity .45s var(--ease-premium),transform .45s var(--ease-premium);}
.card:hover .frame{transform:translateY(-6px);box-shadow:0 24px 48px -20px rgba(19,17,19,0.22);}
.card:hover .frame img{transform:scale(1.03);}
.card:hover .frame::after{opacity:1;transform:none;}
.card .c-tag{margin-top:18px;font-family:'Archivo',sans-serif;font-weight:700;font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--red);}
.card h3{margin-top:8px;font-weight:700;font-size:1.28rem;letter-spacing:-0.02em;line-height:1.2;}
.card p{margin-top:8px;font-size:0.95rem;line-height:1.6;color:rgba(19,17,19,0.66);max-width:40ch;}
.card .c-svc{margin-top:12px;font-family:'Archivo',sans-serif;font-weight:600;font-size:0.7rem;letter-spacing:0.05em;color:var(--muted);}
@media(hover:none){.card .frame::after{opacity:1;transform:none;}.card:hover .frame{transform:none;}}
@media(max-width:900px){.cards{grid-template-columns:repeat(2,1fr);}}
@media(max-width:560px){.cards{grid-template-columns:1fr;gap:40px;}}

/* close / contact */
.close-cta{background:var(--red);color:var(--white);padding:128px var(--gutter) calc(72px + env(safe-area-inset-bottom));}
.close-cta .inner{max-width:760px;margin:0 auto;}
.close-cta .kicker{color:var(--white);margin-bottom:26px;}
.close-cta h2{font-weight:700;letter-spacing:-0.03em;line-height:1.1;font-size:clamp(2rem,4.6vw,3.2rem);margin-bottom:24px;max-width:18ch;}
.close-cta p{font-size:1.04rem;line-height:1.72;color:var(--muted-on-red);max-width:560px;margin-bottom:36px;}
.site-footer{margin-top:72px;padding-top:28px;border-top:1px solid var(--line-on-red);display:flex;flex-wrap:wrap;gap:10px 22px;
  font-family:'Archivo',sans-serif;font-weight:600;font-size:0.72rem;letter-spacing:0.06em;text-transform:uppercase;}
.site-footer a{text-decoration:none;opacity:0.72;transition:opacity .4s;}
.site-footer a:hover{opacity:1;}
.site-footer .fs-copy{opacity:0.55;width:100%;margin-top:8px;font-weight:500;letter-spacing:0.02em;text-transform:none;}
@media(max-width:900px){.close-cta{padding-top:84px;}}

/* reveal */
.js .rv{opacity:0;transform:translateY(22px);transition:opacity .8s var(--ease-soft),transform .8s var(--ease-soft);}
.js .rv.in{opacity:1;transform:none;}
@media(prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none;transition:none;}.frame img{transition:none;}}
"""

BASE_JS = r"""
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, lenis = null;
  if(window.Lenis && !reduce){
    lenis = new Lenis({duration:1,easing:function(t){return 1-Math.pow(1-t,4)},smoothWheel:true,touchMultiplier:1.1});
    (function raf(t){lenis.raf(t);requestAnimationFrame(raf);})(0);
    window.__lenis = lenis;
  }
  // image fade-in once decoded
  document.querySelectorAll('.frame').forEach(function(f){
    var img=f.querySelector('img'); if(!img) return;
    var done=function(){f.classList.add('loaded')};
    if(img.complete && img.naturalWidth) done(); else {img.addEventListener('load',done,{once:true});img.addEventListener('error',done,{once:true});}
  });
  // scroll reveal
  var io = new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:0.08,rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
  window.__reveal = io;
  // page-wipe on internal navigation
  var wipe=document.getElementById('wipe');
  document.addEventListener('click',function(e){
    var a=e.target.closest('a'); if(!a||a.target==='_blank'||e.metaKey||e.ctrlKey||e.shiftKey) return;
    var href=a.getAttribute('href')||''; if(!href||href.charAt(0)==='#'||/^(https?:|mailto:|tel:)/.test(href)) return;
    e.preventDefault(); wipe.classList.add('cover'); setTimeout(function(){location.href=a.href},520);
  });
  window.addEventListener('pageshow',function(e){if(e.persisted) wipe.classList.remove('cover');});
  // progress bar
  var bar=document.getElementById('topProgress');
  function prog(){var h=document.documentElement,s=h.scrollTop/(h.scrollHeight-h.clientHeight)*100;bar.style.width=(isFinite(s)?s:0)+'%';}
  if(lenis) lenis.on('scroll',prog); else addEventListener('scroll',prog,{passive:true}); prog();
})();
"""


def head(title, desc, url, image, prefix, extra_css, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF9F7">
<link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg">
{FONTS}
<script>document.documentElement.classList.add('js')</script>
{ld}
<style>{BASE_CSS}{extra_css}</style>
</head>
<body>
<div id="grain"></div><div id="wipe"></div><div id="topProgress"></div>
"""


def header(prefix, back_href, back_label):
    return f"""<header class="top">
  <a href="{prefix}index.html" class="logo">BEYOND<em>BRANDING</em></a>
  <nav>
    <a href="{prefix}websites.html" class="pill hide-sm">Websites</a>
    <a href="{prefix}packages-global/index.html" class="pill hide-sm">Pricing</a>
    <a href="{back_href}" class="pill">← {back_label}</a>
    <a href="{wa('Hi Ayush, I found you through your portfolio and would like to discuss a project.')}" target="_blank" rel="noopener" class="pill red">WhatsApp</a>
  </nav>
</header>
"""


def close_cta(h2, p, msg):
    return f"""<section class="close-cta">
  <div class="inner">
    <div class="kicker">Start</div>
    <h2>{h2}</h2>
    <p>{p}</p>
    <div class="actions">
      <a href="{wa(msg)}" target="_blank" rel="noopener" class="cta light">⊟ Message on WhatsApp</a>
      <a href="mailto:ayush@beyondbranding.media" class="cta outline-light">Email Ayush</a>
    </div>
    <div class="site-footer">
      <a href="https://instagram.com/beyondbranding.media" target="_blank" rel="noopener">Instagram</a>
      <a href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">LinkedIn</a>
      <a href="mailto:ayush@beyondbranding.media">Email</a>
      <span class="fs-copy">© Beyond Branding · London · Dubai · Mumbai</span>
    </div>
  </div>
</section>
"""


def foot():
    return f"""<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
<script>{BASE_JS}</script>
"""


def card(p, prefix, href_prefix, eager=False):
    img, alt = p["images"][0]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""<a class="card rv" href="{href_prefix}{p['slug']}.html" data-f="{' '.join(p['filters'])}">
  <div class="frame"><img src="{prefix}assets/{img}" alt="{E(alt)}" {load} decoding="async"></div>
  <div class="c-tag">{E(place(p))}</div>
  <h3>{E(p['client'])}</h3>
  <p>{E(p['result'])}</p>
  <div class="c-svc">{E(p['services'])}</div>
</a>"""


# --------------------------------------------------------------------------- hub
HUB_CSS = r"""
.masthead{padding:calc(124px + env(safe-area-inset-top)) var(--gutter) 64px;max-width:1240px;}
.masthead .kicker{margin-bottom:28px;}
.masthead h1{font-weight:700;letter-spacing:-0.035em;line-height:1.06;font-size:clamp(2.4rem,6vw,4.7rem);max-width:15ch;margin-bottom:30px;}
.masthead h1 em{font-style:normal;color:var(--red);}
.masthead .note{max-width:620px;padding-left:22px;border-left:2px solid var(--red);font-size:clamp(1.02rem,1.5vw,1.18rem);line-height:1.72;color:rgba(19,17,19,0.66);margin-bottom:36px;}
@media(max-width:900px){.masthead{padding-top:calc(96px + env(safe-area-inset-top));padding-bottom:48px;}.masthead .note{padding-left:16px;}}

.proof{margin:0 var(--gutter);padding:34px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  display:grid;grid-template-columns:1.4fr 1fr;gap:28px 56px;align-items:center;max-width:1296px;}
.proof .label{font-family:'Archivo',sans-serif;font-weight:700;font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted);margin-bottom:18px;}
.logos{display:flex;flex-wrap:wrap;align-items:center;gap:14px 34px;}
.logos img{height:44px;width:auto;opacity:0.62;filter:grayscale(1) brightness(0.2);transition:opacity .4s;}
.logos img:hover{opacity:1;}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.stats b{display:block;font-family:'Archivo',sans-serif;font-weight:800;font-size:clamp(2rem,3.6vw,2.8rem);letter-spacing:-0.02em;line-height:1;}
.stats b i{font-style:normal;color:var(--red);}
.stats span{display:block;margin-top:8px;font-size:0.82rem;color:var(--muted);}
@media(max-width:900px){.proof{grid-template-columns:1fr;}.logos{gap:10px 24px;}.logos img{height:36px;}}

.filters{position:sticky;top:calc(48px + env(safe-area-inset-top));z-index:200;margin-top:56px;
  background:rgba(250,249,247,0.9);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line);}
.filters .row{display:flex;gap:8px;overflow-x:auto;padding:14px var(--gutter);scrollbar-width:none;-webkit-overflow-scrolling:touch;}
.filters .row::-webkit-scrollbar{display:none;}
.chip{flex:0 0 auto;display:inline-flex;align-items:center;gap:7px;height:36px;padding:0 16px;border-radius:100px;cursor:pointer;
  border:1px solid rgba(19,17,19,0.14);background:transparent;color:var(--ink);font:500 13px/1 'Inter',sans-serif;letter-spacing:-0.01em;
  transition:background .3s var(--ease-premium),color .3s,border-color .3s;}
.chip sup{font-size:10px;color:var(--muted);font-weight:600;}
.chip:hover{border-color:var(--ink);}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--white);border-color:var(--ink);}
.chip[aria-pressed="true"] sup{color:rgba(250,249,247,0.6);}

.sec{padding:72px var(--gutter) 0;max-width:1440px;margin:0 auto;}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:36px;}
.sec-head h2{font-weight:700;letter-spacing:-0.025em;font-size:clamp(1.5rem,2.6vw,2rem);}
.sec-head span{font-size:0.88rem;color:var(--muted);}
@media(max-width:600px){.sec-head span{display:none;}.sec{padding-top:56px;}}
.is-hidden{display:none !important;}

.feature{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(36px,6vw,104px);align-items:center;
  padding:clamp(40px,6vh,72px) 0;border-top:1px solid var(--line);text-decoration:none;color:var(--ink);}
.feature:first-of-type{border-top:0;padding-top:0;}
.feature:nth-of-type(even) .f-media{order:2;}
.feature .frame{aspect-ratio:4/5;max-width:600px;transition:box-shadow .6s var(--ease-premium),transform .6s var(--ease-premium);}
.feature:hover .frame{transform:translateY(-6px);box-shadow:0 30px 60px -24px rgba(19,17,19,0.24);}
.feature:hover .frame img{transform:scale(1.03);}
.f-tag{font-family:'Archivo',sans-serif;font-weight:700;color:var(--red);font-size:0.74rem;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:16px;}
.feature h3{font-weight:700;letter-spacing:-0.03em;line-height:1.08;font-size:clamp(2rem,3.8vw,3rem);margin-bottom:20px;}
.feature .hook{font-size:1.06rem;line-height:1.7;color:rgba(19,17,19,0.66);max-width:44ch;margin-bottom:26px;}
.feature .hook strong{color:var(--ink);font-weight:600;}
.f-result{display:flex;gap:14px;max-width:46ch;padding:18px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:22px;}
.f-result b{flex:0 0 auto;font-family:'Archivo',sans-serif;font-weight:700;font-size:0.68rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--red);padding-top:4px;}
.f-result span{font-size:0.98rem;line-height:1.6;font-weight:500;}
.f-svc{font-family:'Archivo',sans-serif;font-weight:600;font-size:0.74rem;letter-spacing:0.05em;color:var(--muted);margin-bottom:26px;}
.f-link{display:inline-flex;align-items:center;gap:9px;font-family:'Archivo',sans-serif;font-weight:700;font-size:0.78rem;letter-spacing:0.07em;text-transform:uppercase;transition:gap .4s var(--ease-premium),color .4s;}
.feature:hover .f-link{gap:14px;color:var(--red);}
@media(max-width:900px){.feature{grid-template-columns:1fr;gap:26px;}.feature:nth-of-type(even) .f-media{order:0;}.feature .frame{max-width:none;}}

.band{margin:96px var(--gutter) 0;background:var(--ink);color:var(--white);border-radius:28px;padding:clamp(40px,6vw,80px);
  display:grid;grid-template-columns:1.2fr 1fr;gap:32px 64px;align-items:end;max-width:1296px;}
.band .kicker{margin-bottom:20px;}
.band h2{font-weight:700;letter-spacing:-0.03em;line-height:1.1;font-size:clamp(1.8rem,3.6vw,2.7rem);max-width:17ch;}
.band p{font-size:1rem;line-height:1.7;color:rgba(250,249,247,0.68);margin-bottom:26px;}
.band .cta.ghost{color:var(--white);border-color:rgba(250,249,247,0.3);}
.band .cta.ghost:hover{background:var(--white);color:var(--ink);}
.band .cta.primary{background:var(--red);border-color:var(--red);}
.band .cta.primary:hover{background:var(--white);color:var(--ink);border-color:var(--white);box-shadow:none;}
@media(max-width:900px){.band{grid-template-columns:1fr;border-radius:20px;margin-left:16px;margin-right:16px;}}

.interlude{padding:96px var(--gutter) 24px;max-width:1240px;}
.interlude .kicker{margin-bottom:22px;}
.interlude h2{font-weight:700;letter-spacing:-0.025em;line-height:1.15;font-size:clamp(1.7rem,3.4vw,2.6rem);max-width:24ch;margin-bottom:24px;}
.interlude p{font-size:1.02rem;line-height:1.78;color:rgba(19,17,19,0.66);max-width:62ch;}
.interlude p+p{margin-top:16px;}.interlude strong{color:var(--ink);font-weight:600;}
.pull{display:flex;align-items:baseline;gap:18px;padding:32px var(--gutter) 96px;}
.pull .mark{font-family:'Bebas Neue',sans-serif;color:var(--red);font-size:clamp(1.3rem,2.4vw,1.7rem);letter-spacing:0.02em;flex-shrink:0;}
.pull p{font-size:0.98rem;line-height:1.6;color:var(--muted);max-width:52ch;}
@media(max-width:700px){.pull{flex-direction:column;gap:8px;}}
"""

HUB_JS = r"""
(function(){
  var chips=[].slice.call(document.querySelectorAll('.chip')), items=[].slice.call(document.querySelectorAll('[data-f]'));
  var secs=[].slice.call(document.querySelectorAll('.sec'));
  function apply(f, push){
    chips.forEach(function(c){c.setAttribute('aria-pressed', String(c.dataset.k===f))});
    items.forEach(function(it){
      var on = f==='all' || it.dataset.f.split(' ').indexOf(f)>-1;
      it.classList.toggle('is-hidden',!on);
      if(on) it.classList.add('in');
    });
    secs.forEach(function(s){ s.classList.toggle('is-hidden', !s.querySelector('[data-f]:not(.is-hidden)')); });
    if(push){ history.replaceState(null,'', f==='all' ? location.pathname : '#'+f); }
    if(window.__lenis) window.__lenis.resize();
  }
  chips.forEach(function(c){ c.addEventListener('click', function(){
    apply(c.dataset.k, true);
    var top=document.querySelector('.filters').offsetTop;
    if(scrollY>top){ window.__lenis ? window.__lenis.scrollTo(top,{immediate:false}) : scrollTo({top:top,behavior:'smooth'}); }
  }); });
  var h=location.hash.slice(1);
  if(h && chips.some(function(c){return c.dataset.k===h})) apply(h,false);
})();
"""


def build_hub():
    feats = [p for p in PROJECTS if p.get("featured")]
    rest = [p for p in PROJECTS if not p.get("featured")]
    counts = {k: sum(k in p["filters"] for p in PROJECTS) for k, _ in FILTERS}
    chips = [f'<button class="chip" data-k="all" aria-pressed="true">All work <sup>{len(PROJECTS)}</sup></button>']
    chips += [f'<button class="chip" data-k="{k}" aria-pressed="false">{E(n)} <sup>{counts[k]}</sup></button>' for k, n in FILTERS if counts[k]]

    feat_html = []
    for i, p in enumerate(feats):
        img, alt = p["images"][0]
        load = 'loading="eager" fetchpriority="high"' if i == 0 else 'loading="lazy"'
        feat_html.append(f"""<a class="feature rv" href="work/{p['slug']}.html" data-f="{' '.join(p['filters'])}">
  <div class="f-media"><div class="frame"><img src="assets/{img}" alt="{E(alt)}" {load} decoding="async"></div></div>
  <div class="f-text">
    <div class="f-tag">{E(place(p))}</div>
    <h3>{E(p['client'])}</h3>
    <p class="hook"><strong>{E(p['hook'])}</strong> {E(p['summary'])}</p>
    <div class="f-result"><b>Result</b><span>{E(p['result'])}</span></div>
    <div class="f-svc">{E(p['services'])}</div>
    <span class="f-link">Read the case study <span>→</span></span>
  </div>
</a>""")

    names = ", ".join(p["client"] for p in PROJECTS[:6])
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Work · Beyond Branding", "url": f"{SITE}/portfolio.html",
          "hasPart": [{"@type": "CreativeWork", "name": p["client"], "url": f"{SITE}/work/{p['slug']}.html"} for p in PROJECTS]}
    out = head("Work · Beyond Branding — Brand, Packaging, Exhibition & Web Case Studies",
               f"Case studies from Beyond Branding — identity, packaging, exhibitions, campaigns and websites for {names} and more. London · Dubai · Mumbai.",
               f"{SITE}/portfolio.html", f"{SITE}/assets/og-image.jpg", "", HUB_CSS, ld)
    out += header("", "index.html", "Home")
    out += f"""<main>
<section class="masthead">
  <div class="kicker">Work</div>
  <h1>Design trusted by brands people <em>already trust.</em></h1>
  <p class="note">From the Dubai Government Media Office to Marriott and DoubleTree by Hilton—identity, packaging, exhibitions, campaigns and websites, led by one senior creative team and delivered fast.</p>
  <div class="actions">
    <a href="{wa('Hi Ayush, I saw your work and would like to talk about a project.')}" target="_blank" rel="noopener" class="cta">⊟ Start a project</a>
    <a href="packages-global/index.html" class="cta ghost">See packages &amp; pricing</a>
  </div>
</section>

<section class="proof" aria-label="Clients and track record">
  <div>
    <div class="label">Selected clients</div>
    <div class="logos">
      <img src="assets/BEYONDCLIENTS-03.svg" alt="Government of Dubai Media Office" loading="lazy">
      <img src="assets/BEYONDCLIENTS-02.svg" alt="Marriott" loading="lazy">
      <img src="assets/BEYONDCLIENTS-01.svg" alt="Radisson" loading="lazy">
      <img src="assets/BEYONDCLIENTS-04.svg" alt="Sunset Hospitality Group" loading="lazy">
      <img src="assets/BEYONDCLIENTS-06.svg" alt="WazirX" loading="lazy">
      <img src="assets/BEYONDCLIENTS-05.svg" alt="Wemasy" loading="lazy">
    </div>
  </div>
  <div class="stats">
    <div><b>8<i>+</i></b><span>Years</span></div>
    <div><b>200<i>+</i></b><span>Projects</span></div>
    <div><b>12<i>+</i></b><span>Countries</span></div>
  </div>
</section>

<div class="filters" role="toolbar" aria-label="Filter work by service"><div class="row">{''.join(chips)}</div></div>

<section class="sec" id="case-studies">
  <div class="sec-head"><h2>Case studies</h2><span>The thinking behind the work</span></div>
  {''.join(feat_html)}
</section>

<section class="sec" id="more-work">
  <div class="sec-head"><h2>More work</h2><span>Click any project for the full brief</span></div>
  <div class="cards">{''.join(card(p, '', 'work/') for p in rest)}</div>
</section>

<section class="band rv">
  <div>
    <div class="kicker">Next step</div>
    <h2>Seen something close to what you need?</h2>
  </div>
  <div>
    <p>Most projects here started as one short WhatsApp message. Send yours with a line about the brief and you'll hear back from Ayush directly, with a direction and a price range.</p>
    <div class="actions">
      <a href="{wa('Hi Ayush, I saw your portfolio. Here is what I am working on:')}" target="_blank" rel="noopener" class="cta primary">⊟ Send a brief</a>
      <a href="packages-global/index.html" class="cta ghost">View pricing</a>
    </div>
  </div>
</section>

<section class="interlude rv">
  <div class="kicker">What Changed</div>
  <h2>What these projects taught me.</h2>
  <p>Every project leaves something behind. Marriott reinforced the importance of consistency. Government work reminded me that clarity always beats decoration. Retail brands proved that first impressions often decide the sale.</p>
  <p><strong>Those lessons quietly shape every project that follows.</strong></p>
</section>
<div class="pull rv"><div class="mark">People Before Pixels.</div><p>Design is visible. Thinking isn't. Clients rarely remember a layout or a colour palette—they remember how clearly their message was understood.</p></div>
</main>
"""
    out += close_cta("Tell us what you're launching. We'll show you what it takes.",
                     "No forms, no account managers. Message us with your brief and you'll speak to the person actually doing the work—with an honest view on direction, timeline and budget.",
                     "Hi Ayush, I'd like to discuss a project.")
    out += foot() + f"<script>{HUB_JS}</script>\n</body>\n</html>\n"
    return out


# --------------------------------------------------------------------------- case page
CASE_CSS = r"""
.c-hero{padding:calc(112px + env(safe-area-inset-top)) var(--gutter) 0;max-width:1440px;margin:0 auto;
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:clamp(36px,6vw,104px);align-items:center;}
.crumb{font-size:0.82rem;color:var(--muted);margin-bottom:28px;}
.crumb a{text-decoration:none;color:var(--ink);font-weight:500;}
.crumb a:hover{color:var(--red);}
.c-hero .kicker{margin-bottom:22px;}
.c-hero h1{font-weight:700;letter-spacing:-0.035em;line-height:1.04;font-size:clamp(2.6rem,6vw,4.8rem);margin-bottom:24px;}
.c-hero .lede{font-size:clamp(1.08rem,1.6vw,1.26rem);line-height:1.66;color:rgba(19,17,19,0.66);max-width:42ch;margin-bottom:34px;}
.c-hero .lede strong{display:block;color:var(--ink);font-weight:600;margin-bottom:6px;}
.facts{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:16px 40px;padding:22px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:32px;}
.facts dt{font-family:'Archivo',sans-serif;font-weight:700;font-size:0.66rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;}
.facts dd{font-size:0.92rem;font-weight:500;line-height:1.45;}
.c-hero .frame{aspect-ratio:4/5;border-radius:24px;}
@media(max-width:900px){
  .c-hero{grid-template-columns:1fr;padding-top:calc(88px + env(safe-area-inset-top));gap:36px;}
  .c-hero .media{order:-1;} .crumb{margin-bottom:20px;}
  .facts{grid-template-columns:1fr 1fr;gap:16px 24px;} .facts div:first-child{grid-column:1/-1;}
}

.story{max-width:1240px;margin:0 auto;padding:120px var(--gutter) 0;}
.story .kicker{margin-bottom:40px;}
.srow{display:grid;grid-template-columns:240px minmax(0,1fr);gap:20px 56px;padding:34px 0;border-top:1px solid var(--line);}
.srow:last-child{border-bottom:1px solid var(--line);}
.srow h2{font-family:'Archivo',sans-serif;font-weight:700;font-size:0.76rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--red);padding-top:8px;}
.srow p{font-size:clamp(1.14rem,1.9vw,1.48rem);line-height:1.55;letter-spacing:-0.012em;max-width:38ch;}
.srow.learn p{font-weight:600;}
@media(max-width:800px){.story{padding-top:80px;}.srow{grid-template-columns:1fr;gap:12px;padding:28px 0;}.srow h2{padding-top:0;}}

.gallery{max-width:1240px;margin:0 auto;padding:96px var(--gutter) 0;display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(16px,2.4vw,32px);}
.gallery .frame{aspect-ratio:4/5;}
@media(max-width:700px){.gallery{grid-template-columns:1fr;}}

.offer{margin:120px var(--gutter) 0;background:var(--ink);color:var(--white);border-radius:28px;padding:clamp(36px,6vw,80px);max-width:1296px;}
@media(min-width:1440px){.offer{margin-left:auto;margin-right:auto;}}
.offer-top{display:grid;grid-template-columns:1.1fr 1fr;gap:24px 64px;align-items:end;margin-bottom:44px;}
.offer .kicker{margin-bottom:20px;}
.offer h2{font-weight:700;letter-spacing:-0.03em;line-height:1.1;font-size:clamp(1.8rem,3.6vw,2.7rem);max-width:16ch;}
.offer-top p{font-size:1rem;line-height:1.7;color:rgba(250,249,247,0.66);}
.pkgs{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-bottom:40px;}
.pkg{display:block;text-decoration:none;color:var(--white);border:1px solid var(--line-on-ink);border-radius:18px;padding:26px;
  transition:border-color .4s var(--ease-premium),background .4s var(--ease-premium),transform .4s var(--ease-premium);}
.pkg:hover{border-color:rgba(250,249,247,0.4);background:rgba(250,249,247,0.04);transform:translateY(-3px);}
.pkg small{font-family:'Archivo',sans-serif;font-weight:700;font-size:0.66rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(250,249,247,0.5);}
.pkg h3{font-weight:600;font-size:1.12rem;letter-spacing:-0.015em;margin:10px 0 6px;}
.pkg p{font-size:0.88rem;line-height:1.55;color:rgba(250,249,247,0.6);margin-bottom:22px;}
.pkg .price{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding-top:18px;border-top:1px solid var(--line-on-ink);}
.pkg .price b{font-family:'Archivo',sans-serif;font-weight:800;font-size:1.6rem;letter-spacing:-0.02em;}
.pkg .price b i{font-style:normal;font-family:'Inter',sans-serif;font-weight:500;font-size:0.8rem;color:rgba(250,249,247,0.55);margin-right:6px;letter-spacing:0;}
.pkg .price span{font-size:0.8rem;color:rgba(250,249,247,0.6);white-space:nowrap;}
.pkg:hover .price span{color:var(--white);}
.offer .cta.primary{background:var(--red);border-color:var(--red);}
.offer .cta.primary:hover{background:var(--white);color:var(--ink);border-color:var(--white);box-shadow:none;}
.offer .cta.ghost{color:var(--white);border-color:rgba(250,249,247,0.3);}
.offer .cta.ghost:hover{background:var(--white);color:var(--ink);}
@media(max-width:900px){.offer{border-radius:20px;margin-left:16px;margin-right:16px;margin-top:88px;}.offer-top{grid-template-columns:1fr;}}

.related{max-width:1440px;margin:0 auto;padding:120px var(--gutter) 120px;}
.related .head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:36px;}
.related h2{font-weight:700;letter-spacing:-0.025em;font-size:clamp(1.5rem,2.6vw,2rem);}
.related .head a{font-family:'Archivo',sans-serif;font-weight:700;font-size:0.76rem;letter-spacing:0.07em;text-transform:uppercase;text-decoration:none;white-space:nowrap;}
.related .head a:hover{color:var(--red);}
.next{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:80px;padding:34px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);text-decoration:none;}
.next small{display:block;font-family:'Archivo',sans-serif;font-weight:700;font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;}
.next strong{font-weight:700;letter-spacing:-0.03em;font-size:clamp(1.8rem,4.4vw,3.4rem);line-height:1.05;transition:color .4s;}
.next .arr{font-size:clamp(1.6rem,3vw,2.4rem);transition:transform .5s var(--ease-premium),color .4s;}
.next:hover strong,.next:hover .arr{color:var(--red);}
.next:hover .arr{transform:translateX(8px);}
@media(max-width:900px){.related{padding-top:88px;padding-bottom:88px;}}
"""


def related_for(p):
    pool = [q for q in PROJECTS if q is not p]
    score = lambda q: (-len(set(q["filters"]) & set(p["filters"])), -int(bool(q.get("featured"))), PROJECTS.index(q))
    return sorted(pool, key=score)[:3]


def build_case(p, idx):
    pre = "../"
    url = f"{SITE}/work/{p['slug']}.html"
    cover, cover_alt = p["images"][0]
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    msg = f"Hi Ayush, I saw the {p['client']} project on your website and would like something similar for my brand."
    title = f"{p['client']} — {p['services'].split(' · ')[0]} Case Study · Beyond Branding"
    desc = f"{p['hook']} {p['summary']} {p['services']} by Beyond Branding."
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": f"{p['client']} — {p['services']}", "url": url,
          "image": f"{SITE}/assets/{cover}", "description": f"{p['hook']} {p['summary']}",
          "creator": {"@type": "Organization", "name": "Beyond Branding", "url": SITE}, "about": p["industry"]}

    location = p.get("location") or "—"
    live = f'<a href="{p["url"]}" target="_blank" rel="noopener" class="cta ghost">Visit live site ↗</a>' if p.get("url") else ""
    if p.get("demo"):
        live += f'<a href="{pre}{p["demo"]}" target="_blank" rel="noopener" class="cta ghost">Explore the live build ↗</a>' 
    rows = "".join(
        f'<div class="srow rv{" learn" if lbl == "What I Learned" else ""}"><h2>{E(lbl)}</h2><p>{E(txt)}</p></div>'
        for lbl, txt in p["story"])
    gallery = ""
    if len(p["images"]) > 1:
        gallery = '<section class="gallery">' + "".join(
            f'<div class="frame rv"><img src="{pre}assets/{im}" alt="{E(a)}" loading="lazy" decoding="async"></div>'
            for im, a in p["images"][1:]) + "</section>"
    pkgs = "".join(
        f"""<a class="pkg" href="{pre}packages-global/index.html#{PACKAGES[k]['id']}">
  <small>Service</small><h3>{E(PACKAGES[k]['name'])}</h3><p>{E(PACKAGES[k]['incl'])}</p>
  <div class="price"><b><i>from</i>{PACKAGES[k]['start']}</b><span>See tiers →</span></div>
</a>""" for k in p["packages"])

    out = head(title, desc, url, f"{SITE}/assets/{cover}", pre, CASE_CSS, ld)
    out += header(pre, f"{pre}portfolio.html", "All work")
    out += f"""<main>
<section class="c-hero">
  <div class="intro">
    <div class="crumb"><a href="{pre}portfolio.html">Work</a> &nbsp;/&nbsp; {E(p['client'])}</div>
    <div class="kicker">{E(p['industry'])}</div>
    <h1>{E(p['client'])}</h1>
    <p class="lede"><strong>{E(p['hook'])}</strong>{E(p['summary'])}</p>
    <dl class="facts">
      <div><dt>Services</dt><dd>{E(p['services'])}</dd></div>
      <div><dt>Industry</dt><dd>{E(p['industry'])}</dd></div>
      {('<div><dt>Location</dt><dd>' + E(location) + '</dd></div>') if p.get("location") else ''}
    </dl>
    <div class="actions">
      <a href="{wa(msg)}" target="_blank" rel="noopener" class="cta">⊟ Get something similar</a>
      {live}<a href="#pricing" class="cta ghost">What it costs</a>
    </div>
  </div>
  <div class="media"><div class="frame"><img src="{pre}assets/{cover}" alt="{E(cover_alt)}" loading="eager" fetchpriority="high" decoding="async"></div></div>
</section>

<section class="story" aria-label="Case study">
  <div class="kicker">The work</div>
  {rows}
</section>
{gallery}
<section class="offer rv" id="pricing">
  <div class="offer-top">
    <div><div class="kicker">Work like this</div><h2>Want this for your brand?</h2></div>
    <p>These are the services behind the {E(p['client'])} project. Every quote is scoped to your brief—start with a WhatsApp message and get a clear range before anything is agreed.</p>
  </div>
  <div class="pkgs">{pkgs}</div>
  <div class="actions">
    <a href="{wa(msg)}" target="_blank" rel="noopener" class="cta primary">⊟ Discuss your project</a>
    <a href="{pre}packages-global/index.html" class="cta ghost">All packages</a>
  </div>
</section>

<section class="related">
  <div class="head"><h2>Related work</h2><a href="{pre}portfolio.html">View all work →</a></div>
  <div class="cards">{''.join(card(q, pre, '') for q in related_for(p))}</div>
  <a class="next" href="{nxt['slug']}.html"><div><small>Next project</small><strong>{E(nxt['client'])}</strong></div><span class="arr">→</span></a>
</section>
</main>
"""
    out += close_cta("Have a brief like this one?",
                     f"Tell us what you're working on. You'll hear back from Ayush directly—not an account manager—with an honest view on direction, timeline and budget.",
                     msg)
    out += foot() + "</body>\n</html>\n"
    return out


def build_sitemap():
    urls = ["", "portfolio.html", "websites.html", "packages-global/", "packages-india/"] + [f"work/{p['slug']}.html" for p in PROJECTS]
    body = "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


PENDING = []


def main():
    slugs = [p["slug"] for p in PROJECTS]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    waiting = []
    for p in PROJECTS:
        for k in p["filters"]: assert k in FILTER_NAME, (p["slug"], k)
        for k in p["packages"]: assert k in PACKAGES, (p["slug"], k)
        # keep only images that exist; a project without its cover image stays hidden
        have = [(im, a) for im, a in p["images"] if os.path.exists(os.path.join(ROOT, "assets", im))]
        if not have or have[0][0] != p["images"][0][0]:
            waiting.append((p["client"], [im for im, _ in p["images"]]))
            p["_skip"] = True
        p["images"] = have or p["images"]
    # live sites without screenshots yet stay on the homepage/websites page as a labelled preview
    global PENDING
    PENDING = [p for p in PROJECTS if p.get("_skip") and p.get("url")]
    for p in PENDING: p["_pending"] = True
    PROJECTS[:] = [p for p in PROJECTS if not p.get("_skip")]
    for name, ims in waiting:
        print(f"  waiting for images: {name}  ->  assets/{', assets/'.join(ims)}")
    slugs = [p["slug"] for p in PROJECTS]
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "work")):
        if f.endswith(".html") and f[:-5] not in slugs: os.remove(os.path.join(ROOT, "work", f))
    import pages
    with open(os.path.join(ROOT, "portfolio.html"), "w") as f: f.write(pages.build_work(PROJECTS, SITE, FILTERS))
    for i, p in enumerate(PROJECTS):
        if p.get("showcase"):
            from showcase_case import build_showcase_case
            html_out = build_showcase_case(p, PROJECTS[(i + 1) % len(PROJECTS)], SITE, PACKAGES)
        else:
            html_out = pages.build_case2(p, PROJECTS[(i + 1) % len(PROJECTS)], related_for(p), SITE, PACKAGES)
        with open(os.path.join(ROOT, "work", p["slug"] + ".html"), "w") as f: f.write(html_out)
    import apple
    allp = PROJECTS + PENDING
    with open(os.path.join(ROOT, "index.html"), "w") as f: f.write(apple.build_home(allp, SITE))
    with open(os.path.join(ROOT, "websites.html"), "w") as f: f.write(apple.build_websites(allp, SITE, PACKAGES))
    with open(os.path.join(ROOT, "packages-global", "index.html"), "w") as f: f.write(pages.build_pricing(SITE))
    with open(os.path.join(ROOT, "packages-india", "index.html"), "w") as f: f.write(pages.build_pricing(SITE, inr=True))
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f: f.write(build_sitemap())
    with open(os.path.join(ROOT, "robots.txt"), "w") as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"built portfolio.html + {len(PROJECTS)} case pages")


if __name__ == "__main__":
    main()
