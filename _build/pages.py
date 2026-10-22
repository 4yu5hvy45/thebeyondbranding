"""Work page (portfolio.html) and standard case-study pages, on the same design system as the homepage."""
import json, re
from apple import head, footer, E, wa, WA, LINES, image_card, web_card

WORK_CSS = """<style>
.chips{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;padding:0 16px;margin-bottom:34px}
.chips button{border:0;background:var(--tile);color:var(--ink);font:500 .9rem var(--display);padding:9px 16px;border-radius:99px;cursor:pointer;transition:background .25s,color .25s}
.chips button:hover{background:#e8e8ed}.chips button.on{background:var(--ink);color:#fff}
.chips button span{color:var(--muted);margin-left:4px;font-weight:400}.chips button.on span{color:#a1a1a6}
.wk .card.im{min-height:clamp(360px,30vw,460px)}
.wk [hidden]{display:none!important}
/* case page */
.cs-hero{text-align:center;padding:clamp(56px,8vw,104px) 16px 0}
.cs-hero h1{font-size:clamp(2.2rem,9vw,6rem);overflow-wrap:anywhere;font-weight:700;letter-spacing:-.045em;line-height:.98}
.cs-hero .sub{max-width:30ch;margin:16px auto 0}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:14px}.crumb a:hover{color:var(--ink)}
.cover{margin-top:clamp(40px,6vw,64px);border-radius:28px;overflow:hidden;background:var(--tile)}
.cover img{width:100%;max-height:82vh;object-fit:cover}
.meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:28px;padding:22px 0;border-top:1px solid #d2d2d7;border-bottom:1px solid #d2d2d7}
.meta dt{font-size:.78rem;color:var(--muted)}.meta dd{font-size:.98rem;font-weight:500;margin-top:4px}
@media(max-width:700px){.meta{grid-template-columns:1fr 1fr}}
.story{max-width:980px;margin:0 auto}
.story .row{display:grid;grid-template-columns:220px minmax(0,1fr);gap:28px;padding:30px 0;border-bottom:1px solid #e5e5ea}
.story .row:last-child{border-bottom:0}
.story h2{font-size:1rem;font-weight:600;color:var(--red);padding-top:6px}
.story p{font-size:clamp(1.15rem,1.8vw,1.45rem);line-height:1.45;letter-spacing:-.012em}
@media(max-width:700px){.story .row{grid-template-columns:1fr;gap:8px}}
.gal{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.gal img{width:100%;height:100%;object-fit:cover;border-radius:24px;background:var(--tile)}
.gal .w{grid-column:span 2}
@media(max-width:700px){.gal{grid-template-columns:1fr}.gal .w{grid-column:auto}}
.pk{background:var(--tile);border-radius:28px;padding:clamp(28px,4vw,52px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:32px;align-items:center}
.pk h2{font-size:clamp(1.8rem,3.4vw,2.8rem);font-weight:700;letter-spacing:-.03em;line-height:1.05}
.pk p{color:var(--muted);margin-top:10px;line-height:1.5}
.pk .ctas{justify-content:flex-start}
.pk ul{list-style:none;display:grid;gap:10px}
.pk li a{display:flex;justify-content:space-between;align-items:baseline;gap:12px;background:#fff;border-radius:16px;padding:18px 20px;transition:transform .4s cubic-bezier(.19,1,.22,1)}
.pk li a:hover{transform:translateX(4px)}
.pk li b{font-weight:600}.pk li small{display:block;color:var(--muted);font-size:.85rem;margin-top:2px}
.pk li span{font-weight:700;font-size:1.2rem;white-space:nowrap}.pk li span small{display:inline;font-weight:500;color:var(--muted);margin-right:4px}
@media(max-width:800px){.pk{grid-template-columns:1fr}}
.nextp{display:flex;justify-content:space-between;align-items:center;gap:20px;border-top:1px solid #d2d2d7;padding-top:26px}
.nextp small{color:var(--muted);font-size:.85rem}.nextp b{display:block;font-size:clamp(2rem,5vw,3.6rem);font-weight:700;letter-spacing:-.035em;line-height:1.05;transition:color .3s}
.nextp:hover b{color:var(--red)}.nextp i{font-style:normal;font-size:2rem}
</style>"""

FILTER_JS = """<script>
(function(){var b=[].slice.call(document.querySelectorAll('.chips button')),c=[].slice.call(document.querySelectorAll('.wk [data-f]'));
function set(f){b.forEach(function(x){x.classList.toggle('on',x.dataset.k===f)});c.forEach(function(x){x.hidden=!(f==='all'||x.dataset.f.split(' ').indexOf(f)>-1)});
 if(window.ScrollTrigger)ScrollTrigger.refresh();}
b.forEach(function(x){x.addEventListener('click',function(){set(x.dataset.k);history.replaceState(null,'',x.dataset.k==='all'?location.pathname:'#'+x.dataset.k)})});
function fromHash(){var h=location.hash.slice(1);if(h&&b.some(function(x){return x.dataset.k===h}))set(h)}fromHash();addEventListener('hashchange',fromHash);})();
</script>"""


def sub(html):
    """Rewrite root-relative links for pages one folder down (work/)."""
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]+)"', r'\1="../\2"', html)


def _cls(i, n):
    return "c4"


def build_work(projects, site, filters):
    webs = [p for p in projects if "web" in p["filters"] and p.get("showcase")]
    rest = [p for p in projects if p not in webs]
    counts = {k: sum(1 for p in projects if k in p["filters"]) for k, _ in filters}
    chips = f'<button class="on" data-k="all">All work<span>{len(projects)}</span></button>' + "".join(
        f'<button data-k="{k}">{E(n)}<span>{counts[k]}</span></button>' for k, n in filters if counts[k])
    web_html = "".join(web_card(p, "c6 big", (i % 2) * .06).replace('<div class="card hov', f'<div data-f="{" ".join(p["filters"])}" class="card hov', 1)
                       for i, p in enumerate(webs))
    cards = "".join(image_card(p, "c4", (i % 3) * .06).replace('<a class="card im', f'<a data-f="{" ".join(p["filters"])}" class="card im', 1)
                    for i, p in enumerate(rest))
    words = "".join(f'<span class="w" style="transition-delay:{i * .07:.2f}s">{w}</span> ' for i, w in enumerate("All the work.".split()))
    out = head("Work · Beyond Branding", f"{len(projects)} case studies from Beyond Branding: websites, brand identity, packaging, exhibitions and campaigns for Marriott, DoubleTree by Hilton, Dubai Media Office and growing brands.", site, "portfolio.html")
    out = out.replace("</head>", WORK_CSS + "</head>", 1)
    out += f"""<main>
<section class="hero2" style="padding-bottom:clamp(40px,5vw,64px)">
  <div class="eyebrow rv">Work</div>
  <h1>{words}</h1>
  <p class="sub rv" style="--d:.25s">Websites, identities, packaging and exhibitions. Every project led by one senior creative.</p>
</section>
<div class="wk">
  <div class="chips rv" role="toolbar" aria-label="Filter projects">{chips}</div>
  <div class="wrap"><div class="grid">{web_html}{cards}</div></div>
</div>
<section class="close">
  <h2 class="h-xl rv">Seen something close to what you need?</h2>
  <p class="sub s rv">Send one line about your brief and you'll hear back from Ayush with a direction and a price range.</p>
  <div class="ctas rv"><a class="pill" href="{wa("Hi Ayush, I've seen your work and I'd like to discuss a project.")}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="packages-global/index.html">View pricing</a></div>
</section>
</main>
"""
    return out + footer().replace("</body>", FILTER_JS + "</body>", 1)


def build_case2(p, nxt, related, site, packages):
    imgs = p["images"]
    gal = ""
    if len(imgs) > 1:
        rest = imgs[1:]
        gal = '<section class="sec2"><div class="wrap"><div class="gal">' + "".join(
            f'<img class="rv{" w" if (len(rest) % 2 and i == len(rest) - 1) else ""}" src="assets/{f}" alt="{E(a)}" loading="lazy">' for i, (f, a) in enumerate(rest)) + "</div></div></section>"
    story = "".join(f'<div class="row rv"><h2>{E(l)}</h2><p>{E(t)}</p></div>' for l, t in p["story"])
    pk = "".join(f'<li><a href="packages-global/index.html#{packages[k]["id"]}"><div><b>{E(packages[k]["name"])}</b><small>{E(packages[k]["incl"])}</small></div><span><small>From</small>{packages[k]["start"]}</span></a></li>'
                 for k in p["packages"] if k in packages)
    rel = "".join(image_card(q, "c4", i * .06) for i, q in enumerate(related))
    live = p.get("url")
    meta = [("Client", p["client"]), ("Industry", p["industry"]), ("Location", p.get("location", "—")), ("Services", p["services"].replace(" · ", ", "))]
    meta_html = "".join(f"<div><dt>{a}</dt><dd>{E(b)}</dd></div>" for a, b in meta)
    msg = f"Hi Ayush, I saw the {p['client']} project and I'd like something similar."
    ld = {"@context": "https://schema.org", "@type": "CreativeWork", "name": f"{p['client']} · {p['services']}", "description": p["summary"],
          "creator": {"@type": "Organization", "name": "Beyond Branding", "url": site}, "image": f"{site}/assets/{imgs[0][0]}", "url": f"{site}/work/{p['slug']}.html"}
    out = head(f"{p['client']} · {p['services'].split(' · ')[0]} · Beyond Branding", f"{p['hook']} {p['summary']}", site, f"work/{p['slug']}.html")
    out = out.replace("</head>", WORK_CSS + f'<script type="application/ld+json">{json.dumps(ld)}</script></head>', 1)
    out = out.replace('content="' + site + '/assets/og-image.jpg"', f'content="{site}/assets/{imgs[0][0]}"', 1)
    out += f"""<main>
<section class="cs-hero">
  <div class="crumb rv"><a href="portfolio.html">Work</a> / {E(p['client'])}</div>
  <div class="eyebrow rv">{E(p['industry'])}{(' · ' + E(p['location'])) if p.get('location') else ''}</div>
  <h1 class="rv">{E(p['client'])}</h1>
  <p class="sub rv">{E(p['hook'])}</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Get something similar</a>{f'<a class="lk" href="{live}" target="_blank" rel="noopener">Visit the live site</a>' if live else '<a class="lk" href="#price">What it costs</a>'}</div>
</section>
<div class="wrap">
  <div class="cover rv"><img src="assets/{imgs[0][0]}" alt="{E(imgs[0][1])}" fetchpriority="high"></div>
  <dl class="meta rv">{meta_html}</dl>
</div>
<section class="sec2"><div class="wrap"><div class="story">
  <div class="row rv"><h2>Overview</h2><p>{E(p['summary'])}</p></div>
  {story}
  <div class="row rv"><h2>Result</h2><p>{E(p['result'])}</p></div>
</div></div></section>
{gal}
<section class="sec2" id="price"><div class="wrap"><div class="pk rv">
  <div><h2>Want this for your brand?</h2><p>These are the services behind this project. Every quote is scoped to your brief and agreed before work begins.</p>
  <div class="ctas"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Discuss your project</a><a class="lk" href="packages-global/index.html">All pricing</a></div></div>
  <ul>{pk}</ul>
</div></div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv" style="padding:0"><h2>Related work.</h2><a class="lk" href="portfolio.html">All work</a></div>
  <div class="grid">{rel}</div>
  <a class="nextp rv" href="work/{nxt['slug']}.html" style="margin-top:clamp(56px,7vw,90px)"><div><small>Next project</small><b>{E(nxt['client'])}</b></div><i>→</i></a>
</div></section>
<section class="close">
  <h2 class="h-xl rv">Have a brief like this one?</h2>
  <p class="sub s rv">Tell us what you're working on. You'll hear back from Ayush directly with an honest view on direction, timeline and budget.</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="mailto:ayush@beyondbranding.media">Email us</a></div>
</section>
</main>
"""
    return sub(out + footer())


PRICE_CSS = """<style>
.note-i{max-width:760px;margin:0 auto;background:var(--tile);border-radius:20px;padding:20px 24px;color:var(--muted);line-height:1.55;font-size:.98rem}
.note-i b{color:var(--ink)}
.cur{display:inline-flex;background:var(--tile);border-radius:99px;padding:4px;margin-top:22px}
.cur a{padding:8px 16px;border-radius:99px;font-size:.88rem;font-weight:500;color:var(--muted)}
.cur a.on{background:#fff;color:var(--ink);box-shadow:0 2px 8px rgba(0,0,0,.08)}
.toc{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:28px;padding:0 16px}
.toc a{background:var(--tile);border-radius:99px;padding:8px 14px;font-size:.88rem;font-weight:500}.toc a:hover{background:#e8e8ed}
.cat{scroll-margin-top:72px;padding:clamp(40px,5vw,64px) 0;border-top:1px solid #e5e5ea;display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,2fr);gap:32px}
.cat:first-child{border-top:0}
.cat small{font-size:.82rem;font-weight:600;color:var(--red)}
.cat h2{font-size:clamp(1.7rem,2.8vw,2.4rem);font-weight:700;letter-spacing:-.028em;line-height:1.08;margin-top:6px}
.cat p{color:var(--muted);line-height:1.5;margin-top:10px}
.tiers3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.tiers3 div{background:var(--tile);border-radius:22px;padding:24px 22px;display:flex;flex-direction:column;gap:6px}
.tiers3 div:nth-child(2){background:var(--ink);color:#f5f5f7}.tiers3 div:nth-child(2) span{color:#a1a1a6}
.tiers3 h3{font-size:1rem;font-weight:600}
.tiers3 b{font-size:clamp(1.25rem,1.9vw,1.6rem);font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums;margin-top:6px}
.tiers3 span{font-size:.9rem;color:var(--muted);line-height:1.45}
@media(max-width:860px){.cat{grid-template-columns:1fr;gap:20px}}
@media(max-width:600px){.tiers3{grid-template-columns:1fr}}
.bund{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.bund div{background:var(--tile);border-radius:28px;padding:32px 28px}
.bund h3{font-size:1.35rem;font-weight:700;letter-spacing:-.02em}
.bund b{display:block;font-size:1.7rem;font-weight:700;letter-spacing:-.025em;margin:12px 0 14px;font-variant-numeric:tabular-nums}
.bund li{list-style:none;color:var(--muted);padding:8px 0;border-top:1px solid #e0e0e5;font-size:.95rem}
@media(max-width:860px){.bund{grid-template-columns:1fr}}
</style>"""


def build_pricing(site, inr=False):
    from pricing import CATEGORIES, BUNDLES
    col = 2 if inr else 1
    path = "packages-india/" if inr else "packages-global/"
    cats = ""
    for i, (cid, lab, name, desc, tiers) in enumerate(CATEGORIES):
        t = "".join(f"<div><h3>{E(tr[0])}</h3><b>{E(tr[col])}</b><span>{E(tr[3])}</span></div>" for tr in tiers)
        cats += f'<section class="cat rv" id="{cid}"><div><small>{i + 1:02d} · {E(lab)}</small><h2>{E(name)}</h2><p>{E(desc)}</p></div><div class="tiers3">{t}</div></section>'
    toc = "".join(f'<a href="#{cid}">{E(lab)}</a>' for cid, lab, *_ in CATEGORIES)
    bund = "".join(f'<div class="rv"><h3>{E(n)}</h3><b>{E(inr_v if inr else usd)}</b><ul>{"".join(f"<li>{E(x)}</li>" for x in items)}</ul></div>' for n, usd, inr_v, items in BUNDLES)
    cur = "INR" if inr else "USD"
    msg = "Hi Ayush, I've seen your pricing and I'd like a quote."
    words = "".join(f'<span class="w" style="transition-delay:{i * .07:.2f}s">{w}</span> ' for i, w in enumerate("What it actually costs.".split()))
    out = head(f"Pricing ({cur}) · Beyond Branding",
               f"Beyond Branding rate card in {cur}: brand identity, packaging, websites, exhibitions, brochures, signage, campaigns and social, each in three clear tiers.", site, path)
    out = out.replace("</head>", PRICE_CSS + "</head>", 1)
    out += f"""<main>
<section class="hero2" style="padding-bottom:0">
  <div class="eyebrow rv">Pricing · {'India' if inr else 'Global'}</div>
  <h1>{words}</h1>
  <p class="sub rv" style="--d:.25s">Eight areas of work, three tiers each. The same craft behind Marriott, Dubai Media Office and Valdaria, scoped to what you need.</p>
  <div class="cur rv"><a href="../packages-global/index.html"{' class="on"' if not inr else ''}>USD</a><a href="../packages-india/index.html"{' class="on"' if inr else ''}>INR</a></div>
  <div class="toc rv">{toc}</div>
</section>
<section class="sec2" style="padding-top:clamp(48px,6vw,72px)"><div class="note-i rv"><b>Prices in {cur}.</b> Every range reflects real scope (concepts, revision rounds and deliverables), not a floor price with everything stripped out. Need something between two tiers, or one item from a category? Message us; most requests are quoted the same day.</div></section>
<div class="wrap" style="max-width:1240px">{cats}</div>
<section class="sec2"><div class="wrap">
  <div class="head2 rv" style="padding:0"><h2>Bundles.</h2><p>Where most engagements land: several categories, one continuous system.</p></div>
  <div class="bund">{bund}</div>
</div></section>
<section class="close">
  <h2 class="h-xl rv">Only need one thing?</h2>
  <p class="sub s rv">Every category has a per-item base rate and a minimum fee, so a small ask gets a fast, fair quote. Tell us what you need and we'll send a number, usually the same day.</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="portfolio.html">See the work</a></div>
</section>
</main>
"""
    out = sub(out + footer())
    if inr:
        out = out.replace("Starting prices are in US dollars and exclude", "Prices on this page are in Indian rupees (elsewhere on the site, in US dollars) and exclude")
    return out
