"""Awwwards-style case study for website projects that carry a `showcase` dict.

showcase = dict(
  year, role, stack, tagline, statement, intro=[para, ...],
  theme=dict(bg, bg2, fg, muted, accent, line),          # the page wears the client's own colours
  fonts_href,                                            # Google Fonts URL so type specimens render in the real faces
  palette=[(name, hex, note), ...], type=[(family_css, label, role, sample), ...],
  hero, sections=[(img, title, caption), ...], mobiles=[img, ...], features=[(title, text), ...],
)
Paths are relative to the site root.
"""
import html
from urllib.parse import quote

E = lambda s: html.escape(s, quote=True)
WA = "https://wa.me/19108301588"


def wa(m): return WA + "?text=" + quote(m)


CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--fg);font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit}
::selection{background:var(--accent);color:var(--bg)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.w{max-width:1440px;margin:0 auto;padding-inline:max(20px,env(safe-area-inset-left),4vw)}

/* bar */
.bar{position:fixed;inset:0 0 auto;z-index:50;display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding:calc(14px + env(safe-area-inset-top)) max(20px,4vw) 14px;mix-blend-mode:difference;color:#fff}
.bar .logo{font-family:'Archivo',sans-serif;font-weight:800;font-size:1rem;letter-spacing:.02em;text-decoration:none}
.bar nav{display:flex;gap:22px;font-family:'Archivo',sans-serif;font-weight:700;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase}
.bar nav a{text-decoration:none;opacity:.85}.bar nav a:hover{opacity:1}
.bar .logo,.bar nav a{white-space:nowrap}
@media(max-width:600px){.bar nav a.hide{display:none}.bar nav{gap:14px;font-size:.62rem}.bar .logo{font-size:.86rem}}

/* hero */
.hero{padding-top:calc(130px + env(safe-area-inset-top))}
.kick{font-family:'Archivo',sans-serif;font-weight:700;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);display:flex;gap:14px;flex-wrap:wrap}
.hero h1{font-family:'Archivo',sans-serif;font-weight:900;font-size:clamp(4rem,16vw,15rem);line-height:.82;letter-spacing:-.04em;margin:22px 0 28px;text-transform:uppercase}
.hero h1 span{display:inline-block;transform:translateY(40%);opacity:0;animation:up 1.1s cubic-bezier(.19,1,.22,1) forwards}
@keyframes up{to{transform:none;opacity:1}}
.tag{font-size:clamp(1.2rem,2.4vw,2rem);line-height:1.25;letter-spacing:-.015em;max-width:30ch;font-weight:500}
.meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:clamp(40px,6vw,80px);padding:22px 0;border-block:1px solid var(--line)}
.meta dt{font-family:'Archivo',sans-serif;font-weight:700;font-size:.64rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.meta dd{font-size:.95rem;line-height:1.45}
.meta a{text-decoration:none;border-bottom:1px solid var(--accent)}
@media(max-width:800px){.meta{grid-template-columns:1fr 1fr}}

.frame{border-radius:14px;overflow:hidden;background:var(--bg2);box-shadow:0 40px 90px -30px rgba(0,0,0,.55)}
.frame .chrome{height:30px;display:flex;align-items:center;gap:6px;padding:0 14px;background:var(--bg2);border-bottom:1px solid var(--line)}
.frame .chrome i{width:9px;height:9px;border-radius:50%;background:var(--line)}
.frame .chrome u{margin:0 auto;text-decoration:none;font-size:.7rem;color:var(--muted);letter-spacing:.02em}
.frame img{width:100%;aspect-ratio:16/10;object-fit:cover}
.hero-shot{margin-top:clamp(40px,6vw,80px);will-change:transform}

/* intro */
.intro{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:40px clamp(40px,7vw,120px);padding-block:clamp(90px,12vw,180px)}
.intro h2{font-size:clamp(1.8rem,3.6vw,3.2rem);line-height:1.12;letter-spacing:-.025em;font-weight:600}
.intro h2 em{font-style:normal;color:var(--accent)}
.intro p{font-size:1.05rem;line-height:1.75;color:var(--muted)}
.intro p+p{margin-top:18px}
.intro .lbl{font-family:'Archivo',sans-serif;font-weight:700;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin-bottom:18px}
@media(max-width:860px){.intro{grid-template-columns:1fr}}

/* sections */
.sect{padding-bottom:clamp(80px,10vw,150px)}
.sect .row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,3fr);gap:24px clamp(30px,5vw,80px);align-items:start}
.sect .row+.row{margin-top:clamp(70px,9vw,130px)}
.sect .cap{position:sticky;top:110px}
.sect .n{font-family:'Archivo',sans-serif;font-weight:800;font-size:.8rem;color:var(--accent);letter-spacing:.1em}
.sect h3{font-size:clamp(1.3rem,2vw,1.7rem);font-weight:600;letter-spacing:-.02em;margin:12px 0 10px;line-height:1.2}
.sect p{font-size:.98rem;line-height:1.7;color:var(--muted);max-width:34ch}
.sect .row:nth-child(even){grid-template-columns:minmax(0,3fr) minmax(0,1fr)}
.sect .row:nth-child(even) .cap{order:2}
@media(max-width:860px){.sect .row,.sect .row:nth-child(even){grid-template-columns:1fr}.sect .row:nth-child(even) .cap{order:0}.sect .cap{position:static}}

/* mobile */
.mob{background:var(--accent);color:var(--bg);padding-block:clamp(90px,11vw,160px);overflow:hidden}
.mob h2{font-family:'Archivo',sans-serif;font-weight:900;font-size:clamp(2.4rem,7vw,6.4rem);line-height:.9;letter-spacing:-.03em;text-transform:uppercase;max-width:12ch}
.mob p{font-size:1.05rem;line-height:1.65;max-width:40ch;margin-top:18px;opacity:.85}
.phones{display:flex;justify-content:center;gap:clamp(14px,3vw,48px);margin-top:clamp(50px,7vw,90px)}
.phone{width:clamp(150px,22vw,320px);border-radius:clamp(26px,3.6vw,48px);background:#0b0b0c;padding:clamp(7px,.9vw,12px);box-shadow:0 40px 80px -30px rgba(0,0,0,.6)}
.phone img{border-radius:clamp(20px,2.8vw,38px);aspect-ratio:390/844;object-fit:cover;width:100%}
.phone:nth-child(2){transform:translateY(-8%)}
@media(max-width:600px){.phone:nth-child(3){display:none}.phone{width:44vw}}

/* design system */
.ds{padding-block:clamp(90px,12vw,170px)}
.ds-h{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:44px}
.ds-h h2{font-size:clamp(1.8rem,3.4vw,3rem);font-weight:600;letter-spacing:-.025em}
.ds-h p{color:var(--muted);max-width:44ch;line-height:1.65}
.sw{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.sw>div{border-radius:14px;padding:110px 16px 16px;border:1px solid var(--line);display:flex;flex-direction:column;gap:2px}
.sw b{font-size:.9rem;font-weight:600}
.sw code{font-family:ui-monospace,Menlo,monospace;font-size:.78rem;opacity:.75}
.sw small{font-size:.74rem;opacity:.7;margin-top:6px}
.ty{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:10px}
.ty>div{border:1px solid var(--line);border-radius:14px;padding:26px}
.ty .s{font-size:clamp(2.2rem,4vw,3.4rem);line-height:1.05;margin-bottom:18px;overflow-wrap:anywhere}
.ty b{font-size:.92rem;font-weight:600;display:block}
.ty small{color:var(--muted);font-size:.82rem}

/* features */
.ft{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden}
.ft>div{background:var(--bg);padding:30px 26px 34px}
.ft .n{font-family:'Archivo',sans-serif;font-weight:800;font-size:.76rem;color:var(--accent);letter-spacing:.1em}
.ft h3{font-size:1.14rem;font-weight:600;letter-spacing:-.015em;margin:14px 0 8px}
.ft p{font-size:.93rem;line-height:1.65;color:var(--muted)}
.credits{display:flex;flex-wrap:wrap;gap:12px 40px;margin-top:40px;font-size:.88rem;color:var(--muted)}
.credits b{color:var(--fg);font-weight:600;margin-right:8px}

/* cta + next */
.cta{background:var(--fg);color:var(--bg);margin-top:clamp(90px,12vw,170px)}
.cta .w{padding-block:clamp(80px,10vw,140px);display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:30px 60px;align-items:end}
.cta h2{font-family:'Archivo',sans-serif;font-weight:900;font-size:clamp(2.4rem,6vw,5.4rem);line-height:.92;letter-spacing:-.03em;text-transform:uppercase}
.cta p{font-size:1.02rem;line-height:1.65;opacity:.75;margin-bottom:24px}
.cta .price{font-family:'Archivo',sans-serif;font-weight:800;font-size:1.6rem;margin-bottom:18px}
.cta .price small{font-family:'Inter',sans-serif;font-weight:500;font-size:.85rem;opacity:.7;margin-right:6px}
.btns{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:10px;padding:15px 24px;border-radius:100px;font-family:'Archivo',sans-serif;font-weight:700;font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;text-decoration:none;background:#D91C2B;color:#fff;border:1.5px solid #D91C2B;transition:transform .35s cubic-bezier(.19,1,.22,1),background .3s}
.btn:hover{transform:translateY(-2px);background:#A8121E}
.btn.ghost{background:transparent;color:inherit;border-color:currentColor;opacity:.8}
.btn.ghost:hover{opacity:1;background:transparent}
@media(max-width:860px){.cta .w{grid-template-columns:1fr}}
.next{display:block;text-decoration:none;padding-block:clamp(70px,9vw,130px);border-bottom:1px solid var(--line)}
.next small{font-family:'Archivo',sans-serif;font-weight:700;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.next strong{display:block;font-family:'Archivo',sans-serif;font-weight:900;font-size:clamp(2.6rem,9vw,8rem);line-height:.9;letter-spacing:-.04em;text-transform:uppercase;margin-top:14px;transition:color .4s}
.next:hover strong{color:var(--accent)}
.foot{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;padding-block:28px calc(28px + env(safe-area-inset-bottom));font-size:.8rem;color:var(--muted)}
.foot a{text-decoration:none}

.js .rv{opacity:0;transform:translateY(30px);transition:opacity 1s cubic-bezier(.19,1,.22,1),transform 1s cubic-bezier(.19,1,.22,1)}
.js .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.js .rv,.hero h1 span{opacity:1;transform:none;animation:none;transition:none}.hero-shot{transform:none!important}}
"""

JS = r"""
(function(){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});
  var hs=document.querySelector('.hero-shot');
  if(hs && !matchMedia('(prefers-reduced-motion: reduce)').matches){
    addEventListener('scroll',function(){var r=hs.getBoundingClientRect(),v=innerHeight;var t=Math.max(-1,Math.min(1,(r.top-v*.2)/v));hs.style.transform='scale('+(1-Math.max(0,t)*.06)+')'},{passive:true});
    dispatchEvent(new Event('scroll'));
  }
})();
"""


def build_showcase_case(p, nxt, site, packages):
    sc = p["showcase"]; th = sc["theme"]
    url = f"{site}/work/{p['slug']}.html"
    live = p.get("url") or (("../" + p["demo"]) if p.get("demo") else None)
    live_label = (p.get("url") or "").replace("https://", "").rstrip("/") or (p["client"] + " · " + sc.get("status", "Launch-ready build"))
    msg = f"Hi Ayush, I saw the {p['client']} website case study and would like a website like this."
    letters = "".join(f'<span style="animation-delay:{i*40}ms">{E(ch) if ch != " " else "&nbsp;"}</span>' for i, ch in enumerate(p["client"]))
    rows = "".join(f"""
    <div class="row rv"><div class="cap"><div class="n">{i+1:02d}</div><h3>{E(t)}</h3><p>{E(c)}</p></div>
      <div class="frame"><div class="chrome"><i></i><i></i><i></i><u>{E(live_label)}</u></div><img src="../{img}" alt="{E(p['client'])} website: {E(t)}" loading="lazy"></div></div>"""
                   for i, (img, t, c) in enumerate(sc["sections"]))
    phones = "".join(f'<div class="phone rv"><img src="../{m}" alt="{E(p["client"])} on mobile" loading="lazy"></div>' for m in sc["mobiles"])
    sw = "".join(f'<div style="background:{h};color:{"#111" if _light(h) else "#f4f1ea"}"><b>{E(n)}</b><code>{h}</code><small>{E(note)}</small></div>' for n, h, note in sc["palette"])
    ty = "".join(f'<div><div class="s" style="font-family:{fam}">{E(sample)}</div><b>{E(label)}</b><small>{E(role)}</small></div>' for fam, label, role, sample in sc["type"])
    ft = "".join(f'<div class="rv"><div class="n">{i+1:02d}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(sc["features"]))
    intro = "".join(f"<p>{E(x)}</p>" for x in sc["intro"])
    web_from = packages["web"]["start"]
    live_dd = f'<a href="{live}" target="_blank" rel="noopener">{E(live_label)} ↗</a>' if live else "—"
    title = f"{p['client']} — Website Case Study · Beyond Branding"
    desc = f"{sc['tagline']} How Beyond Branding designed and built the {p['client']} website."
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{site}/{sc['hero']}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{th['bg']}">
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link href="{sc['fonts_href']}" rel="stylesheet">
<script>document.documentElement.classList.add('js')</script>
<style>:root{{--bg:{th['bg']};--bg2:{th['bg2']};--fg:{th['fg']};--muted:{th['muted']};--accent:{th['accent']};--line:{th['line']}}}{CSS}</style>
</head>
<body>
<header class="bar"><a class="logo" href="../index.html">BEYOND BRANDING</a>
  <nav><a class="hide" href="../websites.html">Websites</a><a href="../portfolio.html">All work</a>{f'<a href="{live}" target="_blank" rel="noopener">Visit site ↗</a>' if live else ''}</nav></header>
<main>
<section class="hero w">
  <div class="kick"><span>Website case study</span><span>{E(sc['year'])}</span><span>{E(p['industry'])}</span></div>
  <h1 aria-label="{E(p['client'])}">{letters}</h1>
  <p class="tag">{E(sc['tagline'])}</p>
  <dl class="meta">
    <div><dt>Client</dt><dd>{E(p['client'])}</dd></div>
    <div><dt>Our role</dt><dd>{E(sc['role'])}</dd></div>
    <div><dt>Industry</dt><dd>{E(p['industry'])}{(' · ' + E(p['location'])) if p.get('location') else ''}</dd></div>
    <div><dt>{'Live site' if live else 'Status'}</dt><dd>{live_dd if live else E(sc.get('status', 'Launch-ready build'))}</dd></div>
  </dl>
  <div class="frame hero-shot"><div class="chrome"><i></i><i></i><i></i><u>{E(live_label)}</u></div><img src="../{sc['hero']}" alt="{E(p['client'])} website homepage" fetchpriority="high"></div>
</section>

<section class="intro w">
  <div class="rv"><div class="lbl">The idea</div><h2>{sc['statement']}</h2></div>
  <div class="rv">{intro}</div>
</section>

<section class="sect w" aria-label="Key screens">{rows}
</section>

<section class="mob">
  <div class="w"><h2 class="rv">Made for the phone in their hand.</h2><p class="rv">{E(sc['mobile_note'])}</p>
  <div class="phones">{phones}</div></div>
</section>

<section class="ds w">
  <div class="ds-h rv"><h2>Design system</h2><p>{E(sc['ds_note'])}</p></div>
  <div class="sw rv">{sw}</div>
  <div class="ty rv">{ty}</div>
</section>

<section class="w">
  <div class="ds-h rv"><h2>What's built in</h2><p>Every feature exists to move a visitor one step closer to getting in touch.</p></div>
  <div class="ft">{ft}</div>
  <div class="credits rv"><span><b>Design &amp; build</b>Beyond Branding</span><span><b>Stack</b>{E(sc['stack'])}</span><span><b>Devices</b>Desktop, tablet, mobile</span></div>
</section>

<section class="cta">
  <div class="w">
    <h2 class="rv">Want a website that works this hard?</h2>
    <div class="rv">
      <div class="price"><small>Websites from</small>{web_from}</div>
      <p>Designed and built in-house, from first wireframe to launch. Send us a line about your business and we'll come back with a direction and a price range.</p>
      <div class="btns"><a class="btn" href="{wa(msg)}" target="_blank" rel="noopener">⊟ Start a website</a><a class="btn ghost" href="../packages-global/index.html#web">See pricing</a></div>
    </div>
  </div>
</section>

<div class="w">
  <a class="next" href="{nxt['slug']}.html"><small>Next project</small><strong>{E(nxt['client'])} →</strong></a>
  <div class="foot"><span>© Beyond Branding · London · Dubai · Mumbai</span><span><a href="mailto:ayush@beyondbranding.media">ayush@beyondbranding.media</a></span></div>
</div>
</main>
<script>{JS}</script>
</body>
</html>
"""


def _light(hexc):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 150
