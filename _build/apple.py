"""Apple-inspired homepage (index.html) and websites page (websites.html).

Design notes (after Apple's HIG and apple.com): one idea per tile, large tight headlines, a one-line
subhead, two calls to action per tile (a filled pill and a text link with a chevron), generous space,
alternating light and dark tiles with a 12px seam, and a quiet, dense footer. Beyond Branding red
replaces Apple's link blue as the single accent.
"""
import html, json, os, re
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
# (file, alt, optical height in px). Tight-cropped copies of BEYONDCLIENTS-0x.svg, plus ESPERTI and Soul AV.
LOGOS = [("client-marriott.svg", "Marriott", 22), ("client-dubai-media-office.svg", "Government of Dubai Media Office", 34),
         ("client-esperti.svg", "ESPERTI", 23), ("client-soul-av.svg", "Soul AV", 20),
         ("client-radisson.svg", "Radisson", 30), ("client-aiolec.svg", "Aiolec", 20),
         ("client-wazirx.svg", "WazirX", 22), ("client-wemasy.svg", "Wemasy", 24)]
# SF-Symbols-style glyphs (2px rounded strokes) used by the button system
ARROW = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11.5M11 5.5 15.5 10 11 14.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_L = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4.5 7 10l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5 13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
KCHEV = '<svg class="chv" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5 10.5 8 6 12.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
KDOWN = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2.5v10M3.5 8.5 8 13l4.5-4.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SERVICE_TAG = {"web": "Website", "identity": "Identity", "packaging": "Packaging", "events": "Exhibition",
               "campaigns": "Campaign", "signage": "Signage", "collateral": "Collateral"}

# ---- hero settings -------------------------------------------------------------------------------
HERO_LEAD = ("Branding, packaging and websites for hospitality and retail brands in the UK, US and Middle East. "
             "Fast execution, premium craft.")
# Paste a Calendly (or similar) link here. While empty, "Book a 15-min call" opens WhatsApp with a call request.
CALL_URL = ""
# Hero layout. "A" = calm: logos stay in the left column, ungridded and quiet.
#              "B" = strip: left column is headline + CTA only; logos run in one row along the bottom of the hero.
# "K" = Kern-style: grotesk headline with reflection, side panel, red project band (current)
HERO_VARIANT = "K"
# Four projects shown in the hero work row (image file or a VIDEO_CARDS token)
# Markets shown under the client logos in the hero panel
HERO_MARKETS = ["United Kingdom", "Ireland", "United States", "UAE"]
HERO_WORK = ["@soul-av-video", "esperti-1.webp", "dubai-media-office-stage.webp", "doubletree-hilton-signage.webp",
             "marriott-indore-hamper.webp", "aiolec-1.webp", "valdaria-exhibition-booth.webp", "overcmr-paddles-display.webp"]
# Gallery cards that play a muted screen recording instead of a still: token -> (project slug, video, poster)
VIDEO_CARDS = {"@soul-av-video": ("soul-av", "soul-av-scroll.mp4", "soul-av-scroll-poster.webp")}
# Client quote under the logo wall. Leave as None until you have a real, approved quote. Example shape:
# TESTIMONIAL = {"quote": "Two sentences from the client.", "name": "Chris Small", "role": "Director, ESPERTI",
#                "photo": "assets/testimonial-chris.webp"}   # photo optional (square, ~96px)
TESTIMONIAL = None


def sec_bar(n, label, right=""):
    """Kern-style section bar: red square, number, label; optional link/controls on the right."""
    return f'<div class="sx-bar"><span><i></i><em>{n}</em>{label}</span>{right}</div>'


def testimonial():
    t = TESTIMONIAL
    if not t:
        return ""
    ph = f'<img src="{E(t["photo"])}" alt="" width="44" height="44" loading="lazy">' if t.get("photo") else ""
    return (f'<figure class="bbquote rv" style="--d:.36s"><blockquote>&ldquo;{E(t["quote"])}&rdquo;</blockquote>'
            f'<figcaption>{ph}<span><b>{E(t["name"])}</b>{E(t.get("role", ""))}</span></figcaption></figure>')


# (question, answer, optional trailing HTML link). Answers only restate claims already made elsewhere on the site.
FAQS = [
    ("How much does a project cost?",
     "Every service has a published starting price: brand identity from $500, packaging from $400 and websites from $800. "
     "Your quote is scoped to your brief and agreed before any work begins, so there are no surprises.",
     'See the full breakdown on our <a href="packages-global/index.html">pricing page</a>.'),
    ("Do you work with clients in the UK, US and Middle East?",
     "Yes. We work with brands across the UK, Ireland, the US and the Middle East. Live examples include the websites for "
     "Soul AV in London and ESPERTI in Dublin, and event branding for the Government of Dubai Media Office.", ""),
    ("How fast can you deliver?",
     "Days, not months. A dedicated production team sits behind every project, so we can move at launch pace without cutting corners. "
     "Your timeline is confirmed with your quote.", ""),
    ("Who will actually work on my project?",
     "Ayush, the founder, leads every project personally, from first call to final files, with an in-house team producing the work. "
     "No hand-offs to juniors.", ""),
    ("Do you design and build websites in-house?",
     "Yes. Websites are designed, written and built in-house, from single landing pages to full multi-page sites, "
     "and handed over fast, responsive and ready for search.", 'See <a href="websites.html">recent website work</a>.'),
    ("How do we get started?",
     "Send a WhatsApp or email with what you're launching, your timeline and a rough budget. "
     "You'll hear back from the person doing the work, with a clear scope and price.", ""),
]

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

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">'


def head(title, desc, site, path, jsonld=None):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{site}/{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Beyond Branding"><meta property="og:url" content="{site}/{path}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{site}/assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Beyond Branding: brand, packaging and website design studio">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{site}/assets/og-image.jpg">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
{ld}
{FONTS}
<script>document.documentElement.classList.add('js')</script>
<style>{CSS}</style>
</head>
<body>
<header class="kn">
  <a class="kn-logo" href="{HOME}" aria-label="Beyond Branding home"><span>BEYOND<em>BRANDING</em></span></a>
  <nav class="kn-nav"><a href="portfolio.html">Work</a><a href="websites.html">Websites</a><a href="{HOME}#services">Services</a><a href="packages-global/index.html">Pricing</a><a href="{HOME}#about">About</a></nav>
  <a class="kn-cell" href="{WA}" target="_blank" rel="noopener">WhatsApp {KCHEV}</a>
  <span class="kprog" aria-hidden="true"></span>
  <a class="kn-go" href="{wa('Hi Ayush, I would like to start a project.')}" target="_blank" rel="noopener">Start<span class="kn-x"> a project</span> {KCHEV}</a>
</header>
"""


def footer():
    return f"""<footer class="ft"><div class="in">
  <p class="note">Starting prices are in US dollars and exclude printing, fabrication and third-party costs. Every quote is scoped to your brief and agreed before work begins.</p>
  <div class="cols">
    <div><h4>Work</h4><a href="portfolio.html">All projects</a><a href="websites.html">Websites</a><a href="portfolio.html#identity">Brand identity</a><a href="portfolio.html#packaging">Packaging</a><a href="portfolio.html#events">Exhibitions</a></div>
    <div><h4>Services</h4><a href="packages-global/index.html#identity">Identity</a><a href="packages-global/index.html#packaging">Packaging</a><a href="packages-global/index.html#web">Websites</a><a href="packages-global/index.html#campaigns">Campaigns</a><a href="packages-global/index.html">All pricing</a></div>
    <div><h4>Studio</h4><a href="{HOME}#about">About Ayush</a><a href="{HOME}#why">Why Beyond Branding</a><span>London · Dubai · Mumbai</span></div>
    <div><h4>Contact</h4><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><a href="mailto:ayush@beyondbranding.media">Email</a><a href="https://instagram.com/thebeyondbranding" target="_blank" rel="noopener">Instagram</a><a href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">LinkedIn</a></div>
  </div>
  <div class="legal"><span>Copyright © 2026 Beyond Branding. All rights reserved.</span><span>thebeyondbranding.com</span></div>
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


def build_home(projects, site, variant=None, preview=False):
    variant = (variant or HERO_VARIANT).upper()
    by = {p["slug"]: p for p in projects}
    real = [p for p in projects if not p.get("_pending")]
    logos = "".join(f'<span><img src="assets/{f}" alt="{E(a)}" style="--h:{h}px" height="{h}"></span>' for f, a, h in LOGOS)
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
    svcs = "".join(f'<a class="srow rv" style="--d:{i * .05:.2f}s" href="packages-global/index.html#{k}"><span class="n">{i + 1:02d}</span><h3>{E(n)}</h3><p>{E(d)}</p><b><small>From</small>{pr}</b><span class="go">{KCHEV}</span></a>' for i, (k, n, d, pr) in enumerate(SERVICES))
    words = "".join(f'<span class="w" style="transition-delay:{i * .07:.2f}s">{w}</span> ' for i, w in enumerate("Brands that look the part.".split()))

    col_a = ["dubai-media-office-stage.webp", "esperti-1.webp", "marriott-indore-hamper.webp", "colorado-windows-newspaper-ad.webp",
             "overcmr-paddles-display.webp", "aeroengines-america-booth.webp", "stanfords-real-estate-poolside.webp", "xess-conference-stage.webp", "indian-kawfee-jar.webp"]
    col_b = ["doubletree-hilton-signage.webp", "@soul-av-video", "aiolec-1.webp", "dubai-media-office-instagram.webp", "valdaria-exhibition-booth.webp", "gowardhan-ghee-amazon.webp",
             "manek-brochure-bag.webp", "sd-med-solutions-1.webp", "pride-of-cows-retail-signage.webp", "dhanraj-jain-jewellers-counter.webp", "market-lens-1.webp"]
    alt_of = {}
    for p in real:
        for f, a_ in p["images"]:
            alt_of[f] = (p["slug"], a_)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def label(pj):
        if not pj: return ""
        tag = SERVICE_TAG.get((pj.get("filters") or [""])[0], "")
        where = (pj.get("location") or "").split(" · ")[0]
        meta = " · ".join(x for x in (where, "Live site" if pj.get("url") else "") if x) or tag
        return (f'<span class="lb">{E(pj["client"])}<small class="t">{tag}</small><small class="l">{E(meta)}</small></span>'
                f'<span class="vc" aria-hidden="true">View case</span>')

    def gi(f, eager):
        if f in VIDEO_CARDS:  # muted looping screen recording of a live site
            slug, src, poster = VIDEO_CARDS[f]
            pj = by.get(slug)
            return (f'<a class="gi vid" href="work/{slug}.html" tabindex="-1"><video src="assets/{src}" poster="assets/{poster}" '
                    f'muted loop playsinline preload="none" aria-label="{E(pj["client"] if pj else slug)} website scrolling"></video>{label(pj)}</a>')
        if not os.path.exists(os.path.join(root_dir, "assets", f)): return ""
        slug, alt = alt_of.get(f, ("", f))
        href = f"work/{slug}.html" if slug else "portfolio.html"
        hi = ' fetchpriority="high"' if eager and f == col_a[0] else ""
        return (f'<a class="gi" href="{href}" tabindex="-1"><img src="assets/{f}" alt="{E(alt)}" width="1122" height="1402" '
                f'loading="{"eager" if eager else "lazy"}"{hi}>{label(by.get(slug))}</a>')
    def col(files, rev):
        items = "".join(gi(f, i < 3) for i, f in enumerate(files))
        return f'<div class="gcol"><div class="gtrk{" rev" if rev else ""}">{items}{items.replace(chr(34) + "eager" + chr(34), chr(34) + "lazy" + chr(34)).replace(' fetchpriority="high"', "")}</div></div>'
    gal_cols = col(col_a, False) + col(col_b, True)
    row_items = "".join(gi(f, False) for f in [x for pair in zip(col_a, col_b) for x in pair])
    gal_row = row_items + row_items
    desc = ("Brand identity, packaging and website design for hospitality, retail and growing brands in the UK, US and "
            "Middle East. Trusted by Marriott and Dubai Media Office. Projects from $500.")
    org_id = site + "/#organization"
    services = [("Brand identity design", 500), ("Packaging design", 400), ("Website design and development", 800),
                ("Exhibition and event design", 800), ("Campaign and social media design", 150), ("Brochure and catalogue design", 400)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": org_id, "name": "Beyond Branding", "url": site + "/",
         "logo": site + "/assets/apple-touch-icon.png", "image": site + "/assets/og-image.jpg", "description": desc,
         "email": "ayush@beyondbranding.media", "telephone": "+1-910-830-1588", "priceRange": "$$",
         "slogan": "Fast ideas. Premium design. On time, every time.",
         "areaServed": [{"@type": "Country", "name": n} for n in ("United Kingdom", "Ireland", "United States", "United Arab Emirates", "India")],
         "knowsAbout": ["Brand identity", "Packaging design", "Website design", "Exhibition design", "Hospitality branding", "Retail branding"],
         "founder": {"@type": "Person", "name": "Ayush", "jobTitle": "Founder & Creative Director", "sameAs": ["https://linkedin.com/in/ayush-branding"]},
         "sameAs": ["https://instagram.com/thebeyondbranding", "https://linkedin.com/in/ayush-branding"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Design services", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n},
              "priceSpecification": {"@type": "PriceSpecification", "minPrice": pr, "priceCurrency": "USD"}} for n, pr in services]}},
        {"@type": "WebSite", "@id": site + "/#website", "url": site + "/", "name": "Beyond Branding", "publisher": {"@id": org_id}, "inLanguage": "en"},
        {"@type": "FAQPage", "@id": site + "/#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in FAQS]},
    ]}
    faq = "".join(f'<details><summary>{E(q)}<i>{CHEV_R}</i></summary><p>{E(a)}{(" " + x) if x else ""}</p></details>' for q, a, x in FAQS)
    out = head("Beyond Branding | Brand, Packaging & Website Design Studio", desc, site, "", ld)
    if preview:  # side-by-side comparison pages: never indexed
        out = out.replace("<meta name=\"robots\" content=\"index,follow,max-image-preview:large\">", "<meta name=\"robots\" content=\"noindex,nofollow\">", 1)
    out += f"""<main>
<section class="bbh v{variant.lower()}" aria-label="Beyond Branding">
  <div class="bbh-copy">
    <h1 class="rv"><span class="ey">Brand, packaging &amp; website design studio</span><span class="hl" data-shine="FAST IDEAS. PREMIUM DESIGN.&#10;ON TIME, EVERY TIME."><span class="r">FAST IDEAS. PREMIUM DESIGN.</span><br><span class="k">ON TIME, EVERY TIME.</span></span></h1>
    <p class="lead rv" style="--d:.12s">{E(HERO_LEAD)}</p>
    <div class="rv" style="--d:.2s">
      <div class="bbact"><a class="btn fill lg" href="{wa('Hi Ayush, I would like to start a project.')}" target="_blank" rel="noopener"><span class="ic">{ARROW}</span><span class="tx">Start a project<small>From $500 &middot; Fixed quote</small></span></a><a class="btn gray lg" href="portfolio.html"><span class="ic">{ARROW}</span><span class="tx">Explore our work</span></a></div>
    </div>
    <div class="bbh-row" aria-hidden="true"><div class="trk">{gal_row}</div></div>
    {'<div class="bbtrust rv" style="--d:.3s"><small>Trusted by teams at</small><div class="bblogos">' + logos + '</div></div>' if variant == "A" else ""}
    {testimonial()}
  </div>
  <div class="bbh-gal">
    <div class="gwin" aria-label="Recent work">
      {gal_cols}
    </div>
  </div>
  {'<div class="bbstrip"><small>Trusted by</small><div class="bblogos">' + logos + '</div></div>' if variant == "B" else ""}
<script>
(function(){{var r=matchMedia('(prefers-reduced-motion: reduce)').matches;
  // play the live-site loops only while on screen
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{var v=e.target;if(e.isIntersecting&&!r){{v.preload='auto';var p=v.play();if(p)p.catch(function(){{}})}}else v.pause()}})}},{{threshold:.15}});
  document.querySelectorAll('.bbh video').forEach(function(v){{io.observe(v)}});
  // headline shine: once on load, again on hover
  var hl=document.querySelector('.bbh .hl');if(!hl||r)return;
  setTimeout(function(){{hl.classList.add('sweep')}},1100);
  hl.addEventListener('animationend',function(){{hl.classList.remove('sweep')}});
  hl.addEventListener('mouseenter',function(){{if(!hl.classList.contains('sweep')){{void hl.offsetWidth;hl.classList.add('sweep')}}}});
}})();
</script>
</section>

<section class="sx" id="websites">
  {sec_bar("01", "Websites", f'<a href="websites.html">All website work {KCHEV}</a>')}
  <div class="sx-head"><h2 class="rv">Websites that win the work. <span>Designed, written and built in-house.</span></h2><p class="rv" style="--d:.1s">Two are live right now, for clients in London and Dublin. Every build is fast, responsive and ready for search.</p></div>
  <div class="sxb"><div class="grid">{web_html}</div></div>
</section>

<section class="sx sx-stats" aria-label="The studio in numbers">
  <div class="kstats rv">
    <div><b><span data-n="8">8</span><em>+</em></b><span>Years of brand work</span></div>
    <div><b><span data-n="{len(real)}">{len(real)}</span></b><span>Case studies</span></div>
    <div><b><span data-n="3">3</span></b><span>Studios: London, Dubai, Mumbai</span></div>
    <div><b><em>$</em><span data-n="500">500</span></b><span>Projects from</span></div>
  </div>
</section>

<section class="sx" id="work">
  {sec_bar("02", "Brand &amp; print", f'<a href="portfolio.html">Explore all {len(real)} projects {KCHEV}</a>')}
  <div class="sx-head"><h2 class="rv">Brand, packaging and print. <span>For global names and growing brands.</span></h2><p class="rv" style="--d:.1s">Identity systems, packaging, exhibitions and campaigns, designed to work on the shelf, the stage and the screen.</p></div>
  <div class="sxb"><div class="grid">{brand_html}</div></div>
</section>

<section class="sx" id="why">
  {sec_bar("03", "Why us", f'<div class="why-nav"><button data-d="l" aria-label="Previous">{CHEV_L}</button><button data-d="r" aria-label="Next">{CHEV_R}</button></div>')}
  <div class="sx-head"><h2 class="rv">Why Beyond Branding. <span>The short version.</span></h2><p class="rv" style="--d:.1s">How we work, in six points. Senior-led, priced up front and quick to move.</p></div>
  <div class="why">{why}</div>
</section>

<section class="sx" id="services">
  {sec_bar("04", "Services", f'<a href="packages-global/index.html">Compare all packages {KCHEV}</a>')}
  <div class="sx-head"><h2 class="rv">Find the right service. <span>See the price first.</span></h2><p class="rv" style="--d:.1s">Every service has a published starting price. Your quote is scoped to your brief and agreed before any work begins.</p></div>
  <div class="sxb"><div class="srows">{svcs}</div></div>
</section>

<section class="sx" id="about">
  {sec_bar("05", "Founder", '<a href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">LinkedIn ' + KCHEV + '</a>')}
  <div class="sxb sx-pad"><div class="founder2 rv">
    <div class="ph"><img src="assets/founder-ayush.jpg" alt="Ayush, founder of Beyond Branding" loading="lazy"></div>
    <div class="copy">
      <div class="eyebrow">Meet the founder</div>
      <q>I help brands move faster without compromising quality.</q>
      <p>Eight years designing identities, packaging, campaigns and websites for startups and global names like Marriott, DoubleTree by Hilton and the Dubai Government Media Office. Every project is led by me and produced by a dedicated in-house team.</p>
      <div class="who"><b>Ayush</b> · Founder &amp; Creative Director</div>
      <div class="ctas"><a class="pill o" href="https://linkedin.com/in/ayush-branding" target="_blank" rel="noopener">Connect on LinkedIn</a></div>
    </div>
  </div></div>
</section>

<section class="sx sx-faq" id="faq">
  {sec_bar("06", "FAQ")}
  <div class="sxb fq">
    <div class="fq-h"><h2 class="rv">Questions, answered.</h2><p class="rv" style="--d:.1s">What most clients ask before we start. Anything else, just message us.</p></div>
    <div class="faq rv">{faq}</div>
  </div>
</section>

<section class="close sx">
  {sec_bar("07", "Start a project")}
  <h2 class="h-xl rv">Bring us the brief. <span class="r">We'll bring the direction.</span></h2>
  <p class="sub s rv">Tell us what you're launching, your timeline and a rough budget. You'll hear back from the person doing the work.</p>
  <div class="ctas rv"><a class="pill" href="{wa("Hi Ayush, I'd like to discuss a project.")}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="pill t" href="{E(CALL_URL or wa("Hi Ayush, I'd like to book a 15-minute call about a project."))}" target="_blank" rel="noopener">Book a 15-min call</a><a class="lk" href="mailto:ayush@beyondbranding.media?subject=New%20project%20enquiry">Email us</a></div>
  <p class="lines"><a href="mailto:ayush@beyondbranding.media">ayush@beyondbranding.media</a> · <a href="{WA}" target="_blank" rel="noopener">+1 (910) 830-1588</a></p>
</section>
</main>
"""
    if variant == "K":
        def wcell(f):
            if f in VIDEO_CARDS:
                slug, src, poster = VIDEO_CARDS[f]
                media = (f'<video src="assets/{src}" poster="assets/{poster}" muted loop playsinline preload="none" '
                         f'aria-label="{E(by[slug]["client"])} website scrolling"></video>')
            else:
                slug, alt = alt_of.get(f, ("", f))
                media = f'<img src="assets/{f}" alt="{E(alt)}" width="1122" height="1402" loading="eager">'
            pj = by.get(slug, {})
            tag = SERVICE_TAG.get((pj.get("filters") or [""])[0], "")
            where = (pj.get("location") or "").split(" · ")[0]
            live = '<b class="live">Live</b>' if pj.get("url") else ""
            return (f'<a class="kw" href="work/{slug}.html"><span class="kw-m">{media}</span>'
                    f'<span class="kw-c"><span class="kw-n">{E(pj.get("client", ""))}{live}</span><span class="kw-t">{tag}{(" · " + E(where)) if where else ""}</span></span></a>')
        work = "".join(wcell(f) for f in HERO_WORK)
        hero_k = f"""<section class="kh" aria-label="Beyond Branding">
  <div class="kh-main">
    <div class="kh-left">
      <span class="kh-ey"><i></i>Brand, packaging &amp; website design studio</span>
      <h1 class="kh-h rv"><span class="sr">Brand, packaging and website design studio. </span><span class="fx r">Fast ideas. Premium design.</span><span class="fx k">On time, every time.</span></h1>
      <div class="kh-body rv" style="--d:.15s">
        <p>{E(HERO_LEAD)}</p>
        <div class="kh-act"><div class="kh-cta"><a class="kb ink" href="{wa('Hi Ayush, I would like to start a project.')}" target="_blank" rel="noopener">Start a project {KCHEV}</a><a class="kb line" href="portfolio.html">Explore our work</a></div>
        <small class="kh-note">From $500 &middot; Fixed quote before we start</small></div>
      </div>
    </div>
    <aside class="kh-side" aria-label="Clients">
      <div class="kh-tr"><span class="kh-lbl"><i></i>Trusted by</span><p>Global hotel groups, government media and growing brands.</p></div>
      <div class="kh-logos">{logos}</div>
      <div class="kh-mk"><span class="kh-lbl">Clients across</span><ul>{"".join(f"<li>{E(m)}</li>" for m in HERO_MARKETS)}</ul></div>
    </aside>
  </div>
  <div class="kh-bar"><span><i></i>Selected work</span><div class="kh-ctl"><a href="portfolio.html">View all {len(real)} projects {KCHEV}</a><button class="kq" data-d="-1" aria-label="Previous project">{CHEV_L}</button><button class="kq" data-d="1" aria-label="Next project">{CHEV_R}</button></div></div>
  <div class="kh-work"><div class="kw-trk">{work}</div></div>
  <script>(function(){{
  var r=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{var v=e.target;if(e.isIntersecting&&!r){{v.preload='auto';var p=v.play();if(p)p.catch(function(){{}})}}else v.pause()}})}},{{threshold:.2}});
  function watch(){{document.querySelectorAll('.kh video').forEach(function(v){{io.observe(v)}})}}
  // stepped carousel: one card at a time, eased, infinite, pauses on hover / when off-screen / tab hidden
  var box=document.querySelector('.kh-work'),trk=box&&box.querySelector('.kw-trk');
  if(trk){{var items=[].slice.call(trk.children),N=items.length;items.slice(0,4).forEach(function(n){{var c=n.cloneNode(true);c.setAttribute('aria-hidden','true');c.tabIndex=-1;trk.appendChild(c)}});
    var i=0,busy=false,hover=false,vis=true;
    function w(){{return trk.children[0].getBoundingClientRect().width}}
    function go(d){{if(busy)return;busy=true;
      if(d<0&&i===0){{trk.style.transition='none';i=N;trk.style.transform='translate3d('+(-i*w())+'px,0,0)';void trk.offsetWidth;trk.style.transition=''}}
      i+=d;trk.style.transform='translate3d('+(-i*w())+'px,0,0)'}}
    trk.addEventListener('transitionend',function(){{busy=false;if(i>=N){{trk.style.transition='none';i=0;trk.style.transform='translate3d(0,0,0)';void trk.offsetWidth;trk.style.transition=''}}}});
    document.querySelectorAll('.kq').forEach(function(b){{b.addEventListener('click',function(){{go(+b.dataset.d)}})}});
    box.addEventListener('mouseenter',function(){{hover=true}});box.addEventListener('mouseleave',function(){{hover=false}});
    new IntersectionObserver(function(es){{vis=es[0].isIntersecting}}).observe(box);
    var x0=null;box.addEventListener('touchstart',function(e){{x0=e.touches[0].clientX}},{{passive:true}});
    box.addEventListener('touchend',function(e){{if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)go(dx<0?1:-1);x0=null}});
    addEventListener('resize',function(){{trk.style.transition='none';trk.style.transform='translate3d('+(-i*w())+'px,0,0)';void trk.offsetWidth;trk.style.transition=''}});
    if(!r)setInterval(function(){{if(!hover&&vis&&!document.hidden)go(1)}},4200)}}
  watch();
}})();</script>
  {testimonial()}
</section>"""
        out = re.sub(r'<section class="bbh v[a-z]".*?</section>', lambda m: hero_k, out, count=1, flags=re.S)
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
