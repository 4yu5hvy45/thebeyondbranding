"""Search landing pages: services/ (one page per service) and guides/ (pricing articles).

Built by build.py. Edit the copy here; pages live at:
  services/                      hub
  services/<slug>/               one page per service
  guides/                        hub
  guides/<slug>/                 one article per guide
"""
import json, os, re
from apple import head, footer, E, wa, image_card, KCHEV
from pricing import CATEGORIES

UPDATED = "2026-11-02"

SEO_CSS = """<style>
.lede{max-width:760px;margin:0 auto;font-size:clamp(1.1rem,1.7vw,1.32rem);line-height:1.55;color:#3a3a3c;letter-spacing:-.01em}
.lede p+p{margin-top:16px}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:14px}.crumb a:hover{color:var(--ink)}
.tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.tiles div{background:var(--tile);border-radius:22px;padding:26px 24px}
.tiles h3{font-size:1.12rem;font-weight:600;letter-spacing:-.015em}
.tiles p{color:var(--muted);line-height:1.5;margin-top:8px;font-size:.98rem}
@media(max-width:860px){.tiles{grid-template-columns:1fr 1fr}}@media(max-width:560px){.tiles{grid-template-columns:1fr}}
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;counter-reset:s}
.steps div{border-top:2px solid var(--ink);padding-top:18px}
.steps div:before{counter-increment:s;content:"0" counter(s);font:600 .82rem var(--display);color:var(--red)}
.steps h3{font-size:1.15rem;font-weight:600;margin-top:6px}.steps p{color:var(--muted);line-height:1.5;margin-top:6px;font-size:.96rem}
@media(max-width:860px){.steps{grid-template-columns:1fr 1fr;row-gap:28px}}@media(max-width:520px){.steps{grid-template-columns:1fr}}
.tiers3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.tiers3 div{background:var(--tile);border-radius:22px;padding:24px 22px;display:flex;flex-direction:column;gap:6px}
.tiers3 div:nth-child(2){background:var(--ink);color:#f5f5f7}.tiers3 div:nth-child(2) span{color:#a1a1a6}
.tiers3 h3{font-size:1rem;font-weight:600}
.tiers3 div:nth-child(2) h3{color:#f5f5f7}.art .tiers3{margin-top:20px}.art .tiers3 h3{margin:0}
.tiers3 b{font-size:clamp(1.25rem,1.9vw,1.6rem);font-weight:700;letter-spacing:-.02em;font-variant-numeric:tabular-nums;margin-top:6px}
.tiers3 span{font-size:.9rem;color:var(--muted);line-height:1.45}
@media(max-width:600px){.tiers3{grid-template-columns:1fr}}
.fineprint{color:var(--muted);font-size:.92rem;margin-top:14px;line-height:1.5}.fineprint a{color:var(--red)}
.tags{display:flex;flex-wrap:wrap;gap:8px}.tags span{background:var(--tile);border-radius:99px;padding:8px 14px;font-size:.92rem;font-weight:500}
.qa{max-width:860px;margin:0 auto;border-top:1px solid #d2d2d7}
.qa details{border-bottom:1px solid #d2d2d7;padding:20px 0}
.qa summary{cursor:pointer;list-style:none;font-size:clamp(1.05rem,1.6vw,1.25rem);font-weight:600;display:flex;justify-content:space-between;gap:16px}
.qa summary::-webkit-details-marker{display:none}.qa summary:after{content:"+";color:var(--red);font-weight:400;font-size:1.4em;line-height:.8}
.qa details[open] summary:after{content:"–"}
.qa p{color:#3a3a3c;line-height:1.6;margin-top:12px;max-width:70ch}
.hubs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.hubs a{background:var(--tile);border-radius:28px;padding:clamp(26px,3.4vw,40px);display:flex;flex-direction:column;gap:10px;transition:background .25s,transform .45s cubic-bezier(.19,1,.22,1)}
.hubs a:hover{background:#ececf0;transform:translateY(-3px)}
.hubs small{font-size:.82rem;font-weight:600;color:var(--red)}
.hubs h2,.hubs h3{font-size:clamp(1.5rem,2.6vw,2.1rem);font-weight:700;letter-spacing:-.028em;line-height:1.08}
.hubs p{color:var(--muted);line-height:1.5}.hubs b{font-weight:600;margin-top:auto;padding-top:8px}
@media(max-width:760px){.hubs{grid-template-columns:1fr}}
.art{max-width:760px;margin:0 auto;font-size:1.08rem;line-height:1.7;color:#2c2c2e}
.art h2{font-size:clamp(1.6rem,2.8vw,2.2rem);font-weight:700;letter-spacing:-.025em;line-height:1.12;color:var(--ink);margin:52px 0 14px}
.art h3{font-size:1.2rem;font-weight:600;color:var(--ink);margin:28px 0 8px}
.art p{margin-top:14px}.art ul{margin:14px 0 0 1.2em}.art li{margin-top:6px}
.art a{color:var(--red);text-decoration:underline;text-underline-offset:3px}
.art strong{color:var(--ink)}
.art .tbl{overflow-x:auto;margin-top:20px;border-radius:18px;background:var(--tile)}
.art table{width:100%;border-collapse:collapse;font-size:.96rem;min-width:520px}
.art th,.art td{text-align:left;padding:14px 18px;border-bottom:1px solid #e0e0e5;vertical-align:top}
.art th{font-weight:600;color:var(--ink)}.art tr:last-child td{border-bottom:0}
.art .callout{background:var(--ink);color:#f5f5f7;border-radius:22px;padding:24px 26px;margin-top:28px}
.art .callout strong{color:#fff}.art .callout a{color:#fff}
.byline{color:var(--muted);font-size:.9rem;margin-top:14px}
.toc2{max-width:760px;margin:28px auto 0;background:var(--tile);border-radius:18px;padding:18px 22px;font-size:.95rem}
.toc2 b{display:block;margin-bottom:6px}.toc2 a{display:block;padding:4px 0;color:var(--ink)}.toc2 a:hover{color:var(--red)}
</style>"""

PROCESS = [
    ("Brief & quote", "Tell us what you're launching, your timeline and budget. You get a clear scope and a fixed price before any work starts."),
    ("Direction", "Ayush leads the creative direction personally and presents focused routes, each with the thinking behind it."),
    ("Refine", "We develop the chosen route with you through agreed revision rounds until every detail is right."),
    ("Hand-over", "Final, production-ready files and guidance, so your team and printers can use the work without guesswork."),
]

SERVICES = [
    dict(
        slug="brand-identity-design", key="identity", short="Brand Identity",
        title="Brand Identity & Logo Design Studio | Beyond Branding",
        desc="Brand identity and logo design for hospitality, retail and growing brands in the UK, US and UAE. Logo, type, colour and guidelines from $500, led by a senior creative.",
        h1="Brand identity design that makes a growing brand look established.",
        lead="Logo, typography, colour and the guidelines that hold them together. Designed for brands across the UK, US and Middle East, from $500.",
        intro=[
            "A logo on its own rarely fixes how a business is seen. What changes perception is a complete identity: a mark, a type system, a colour palette and clear rules that make every menu, website, sign and social post feel like it came from the same company.",
            "Beyond Branding designs identities for hospitality, luxury retail, food and drink and service businesses. The same studio has produced work for Marriott, DoubleTree by Hilton and the Government of Dubai Media Office, so a growing brand gets the standards of large accounts without the overheads of a large agency.",
        ],
        get=[
            ("Logo system", "Primary logo, secondary lock-ups and an icon or monogram that works from a favicon to a shopfront."),
            ("Typography", "A primary and supporting typeface with a hierarchy for headlines, body copy and small print."),
            ("Colour palette", "Core and accent colours with print (CMYK, Pantone) and screen (RGB, HEX) values."),
            ("Brand guidelines", "A clear guide covering logo use, spacing, colour, type and what to avoid."),
            ("Applications", "Stationery, social templates and mock-ups so you can see the identity in real use."),
            ("Final file pack", "Organised vector, PNG and PDF files ready for printers, developers and your team."),
        ],
        tiers_from="identity",
        industries=["Hospitality & hotels", "Restaurants & cafés", "Luxury retail", "Jewellery", "Food & beverage", "Professional services", "Startups"],
        work_filter=lambda p: "identity" in p["filters"],
        faqs=[
            ("How much does brand identity design cost?", "Brand identity starts at $500 for a logo with a basic usage guide. A Signature identity with logo, type, colour and guidelines is $1,500 to $3,000, and a Full System with stationery and a brand book is $3,000 to $6,000+. Your quote is fixed before work begins."),
            ("What's the difference between a logo and a brand identity?", "A logo is one mark. A brand identity is the whole visual system around it: typography, colour, layout rules and guidelines. The identity is what keeps your brand consistent across every place customers see it."),
            ("Do you work with businesses outside the UK?", "Yes. We work with brands across the UK, Ireland, the US, the UAE and India. Everything runs remotely over WhatsApp, email and video calls."),
            ("Can you refresh an existing logo instead of starting again?", "Yes. If your current mark has recognition worth keeping, we can refine it and build a stronger system around it rather than replacing it outright."),
            ("Who will work on my brand?", "Ayush, the founder and creative director, leads every project from first call to final files, with an in-house production team behind him."),
        ],
    ),
    dict(
        slug="packaging-design", key="packaging", short="Packaging",
        title="Packaging Design Agency for Food, Drink & Retail | Beyond Branding",
        desc="Shelf-ready packaging and label design for food, drink, FMCG and retail brands. Single products from $400, full ranges with a packaging style guide. Print-ready files.",
        h1="Packaging design that sells from the shelf.",
        lead="Labels, boxes, pouches and full product ranges, designed to stand out and print right first time. From $400 per product.",
        intro=[
            "On a shelf or a product page you get a second or two to be noticed and understood. Good packaging does three jobs at once: it signals quality, tells the customer what the product is and makes the range easy to tell apart.",
            "Beyond Branding has designed packaging and product graphics for food and beverage, hospitality, luxury retail, kidswear and sports equipment brands, including guest packaging for Marriott. Every design is delivered as print-ready artwork set up for your printer's specifications.",
        ],
        get=[
            ("Concept routes", "Distinct design directions for your hero product before the range is rolled out."),
            ("Range architecture", "A system for colour, flavour or variant coding so every SKU belongs to one family."),
            ("Dieline artwork", "Artwork built on your printer's dielines, with bleed, safe zones and finishes marked up."),
            ("Regulatory layout", "Space and hierarchy for ingredients, barcodes, nutrition and legal copy."),
            ("Mock-ups", "Realistic renders for approval, pitch decks, e-commerce listings and social launches."),
            ("Packaging style guide", "For larger ranges: rules so new products can be added without starting again."),
        ],
        tiers_from="packaging",
        industries=["Food & beverage", "Coffee & tea", "Bakery & confectionery", "FMCG & e-commerce", "Hospitality amenities", "Kidswear & lifestyle", "Sports equipment"],
        work_filter=lambda p: "packaging" in p["filters"],
        faqs=[
            ("How much does packaging design cost?", "A single product (one SKU) is $400 to $1,200. A family of up to five SKUs on one system is $1,600 to $3,600, and a full range of six or more SKUs with a packaging style guide starts at $4,000. Printing is quoted separately by your printer."),
            ("Do you handle printing?", "We deliver print-ready artwork set up to your printer's dielines and specifications. Printing itself is quoted and supplied by your printer."),
            ("Can you design labels for jars, pouches and bottles?", "Yes. We design labels, sleeves, boxes, pouches and hang tags, and adapt one design system across every format in your range."),
            ("Can you create mock-ups for my online store?", "Yes. Every packaging project includes realistic mock-ups you can use for approvals, Amazon or Shopify listings and social media."),
            ("Do you design for Amazon and e-commerce?", "Yes. We've produced Amazon listing creative alongside packaging, so your product looks consistent from the box to the product page."),
        ],
    ),
    dict(
        slug="website-design", key="web", short="Websites",
        title="Website Design & Development Studio | Beyond Branding",
        desc="Custom website design and development for service, hospitality and retail businesses. Fast, mobile-first sites built in-house to bring in enquiries. Landing pages from $800.",
        h1="Websites designed to win enquiries, not just look good.",
        lead="Custom design, written and built in-house. Mobile-first, fast and set up for search, from single landing pages to full sites. From $800.",
        intro=[
            "Most small business websites fail in the same ways: slow on a phone, vague about what the business does and unclear about what a visitor should do next. A well-built site fixes all three, so it works as a salesperson rather than a brochure.",
            "Beyond Branding designs and builds websites in-house, with no templates and no page builders. Live examples include Soul AV, an AV company in London, and ESPERTI, a construction and fit-out firm in Dublin. Every site is handed over responsive, fast and ready for search engines.",
        ],
        get=[
            ("Custom design", "A site designed around your brand and your customers, not a theme with your logo dropped in."),
            ("Copywriting", "Clear, search-friendly page copy written to explain what you do and move visitors to enquire."),
            ("Mobile-first build", "Hand-built, lightweight code that loads fast on phones, where most of your visitors are."),
            ("Enquiry flows", "WhatsApp, email and form calls to action placed where visitors are ready to act."),
            ("Search foundations", "Page titles, descriptions, structured data, sitemap and clean URLs set up from day one."),
            ("Launch & hand-over", "Help with domain and hosting set-up, analytics in place and a walkthrough of your new site."),
        ],
        tiers_from="web",
        industries=["AV & event services", "Construction & fit-out", "Hospitality & consulting", "Property", "Healthcare & pharma", "Creative & film", "Startups & web apps"],
        work_filter=lambda p: "web" in p["filters"],
        faqs=[
            ("How much does a website cost?", "A single-page landing page or microsite is $800 to $1,800. A full website of five to eight pages is $2,000 to $5,000. E-commerce, 3D and custom builds are scoped on request. Hosting and domains are paid separately."),
            ("Do you use WordPress or a template?", "No. Sites are designed from scratch and hand-built, which keeps them fast, secure and free of plugin bloat. If you need a specific platform, tell us at the brief stage."),
            ("Will my website be optimised for Google?", "Every site launches with search foundations in place: keyword-led titles and descriptions, structured data, a sitemap, fast load times and mobile-friendly layouts."),
            ("Can you redesign my existing website?", "Yes. We can rebuild your current site with stronger design, clearer copy and better performance, keeping the pages and content that already work."),
            ("Do you write the content?", "Yes. Copywriting is part of the process, so the words and design are planned together rather than filled in at the end."),
        ],
    ),
    dict(
        slug="hospitality-branding", key=None, short="Hospitality",
        title="Hotel & Hospitality Branding Agency | Beyond Branding",
        desc="Branding, signage, guest collateral and websites for hotels, restaurants, cafés and holiday homes. Trusted by Marriott and DoubleTree by Hilton. UK, UAE and India.",
        h1="Hospitality branding, from the logo to the room card.",
        lead="Identity, signage, menus, guest collateral and websites for hotels, restaurants, cafés and independent stays. The craft behind work for Marriott and DoubleTree by Hilton.",
        intro=[
            "In hospitality, the brand is experienced in dozens of small moments: the sign outside, the menu, the key card, the welcome note, the website a guest books through. When those moments match, a property feels premium and guests remember it.",
            "Beyond Branding has produced guest packaging and campaign design for Marriott, signage and production artwork for DoubleTree by Hilton, and brand and website work for hospitality consultancies. For independent stays and holiday homes, our Brand My Stay service packages the same thinking at a fixed price.",
        ],
        get=[
            ("Property identity", "Logo, colour and type for a hotel, restaurant, café or holiday home, with clear guidelines."),
            ("Signage & wayfinding", "Exterior signs, room numbers and in-house wayfinding with production-ready artwork."),
            ("Menus & F&B", "Menu design, table talkers and promotional material that carry the brand to the table."),
            ("Guest collateral", "Welcome cards, room guides, amenity packaging and printed stationery."),
            ("Direct-booking website", "A fast website that showcases the property and drives direct enquiries and bookings."),
            ("Campaigns & social", "Seasonal campaigns and social templates your team can keep using."),
        ],
        tiers_from=None,
        industries=["Hotels & resorts", "Restaurants", "Cafés & bakeries", "Holiday homes & Airbnb", "Serviced apartments", "Hospitality consulting"],
        work_filter=lambda p: "hospitality" in p["industry"].lower(),
        faqs=[
            ("What does hospitality branding include?", "It covers the identity itself plus everything guests touch: signage, menus, room collateral, amenity packaging and the website. We scope only the pieces you need."),
            ("How much does hotel or restaurant branding cost?", "Brand identity starts at $500, signage for a single location from $500 and websites from $800. Most hospitality projects combine several of these and are quoted as one fixed price. Fabrication and printing are quoted by your suppliers."),
            ("Do you work with independent stays and Airbnb hosts?", "Yes. Brand My Stay is our fixed-price service for independent stays and holiday homes, covering identity, guest printables, digital guest guides and direct-booking websites."),
            ("Have you worked with hotel groups?", "Yes. Our work includes guest packaging and campaign design for Marriott and signage artwork for DoubleTree by Hilton."),
            ("Can you work with our brand standards?", "Yes. For branded or franchise properties we work within existing brand standards and produce artwork that meets them."),
        ],
    ),
]

GUIDES = [
    dict(
        slug="logo-design-cost",
        title="How Much Does a Logo Cost in 2026? UK, US & UAE Pricing Guide",
        desc="What a logo and brand identity really cost in 2026, from marketplaces to agencies, what drives the price and what you should get for your budget. With real studio prices.",
        h1="How much does a logo cost in 2026?",
        lead="A straight answer, with real numbers: what you'll pay at each level, what changes the price and how to tell whether a quote is fair.",
        service="brand-identity-design",
        body="""
<p><strong>Short answer:</strong> a professionally designed logo typically costs anywhere from about <strong>£100 with a freelancer</strong> to <strong>£2,000+ with an agency</strong>, and a full brand identity from a London agency often runs <strong>£5,000 to £25,000 or more</strong>. At Beyond Branding, a logo with a usage guide starts at <strong>$500</strong>, and a complete identity with guidelines is <strong>$1,500 to $3,000</strong>.</p>
<p>The range is wide because "a logo" can mean very different things. Below is what each level actually gets you.</p>

<h2 id="levels">Logo prices by type of designer</h2>
<p>These are typical 2026 ranges for the UK, based on published industry pricing guides. US and UAE prices follow a similar pattern, with major-city agencies at the top end.</p>
<div class="tbl"><table>
<tr><th>Who designs it</th><th>Typical price</th><th>What you usually get</th></tr>
<tr><td>Logo generators &amp; marketplaces</td><td>Free – £150</td><td>Template-based marks, little originality, limited file rights</td></tr>
<tr><td>Freelance designer</td><td>£100 – £500</td><td>A few logo concepts and basic files; quality varies widely</td></tr>
<tr><td>Small studio</td><td>£500 – £3,000</td><td>Strategy-led logo, type and colour, often with guidelines</td></tr>
<tr><td>Branding agency</td><td>£750 – £2,000+ (logo)<br>£5,000 – £25,000+ (identity)</td><td>Workshops, research, full identity system and brand book</td></tr>
</table></div>

<h2 id="drivers">What drives the price of a logo?</h2>
<h3>1. Logo or full identity</h3>
<p>A logo is one mark. A brand identity adds typography, colour, layout rules and guidelines. The identity is what keeps your website, packaging and signage consistent, and it's where most of the cost (and most of the value) sits.</p>
<h3>2. Number of concepts and revisions</h3>
<p>More initial routes and more revision rounds mean more design time. Cheap quotes often include one concept and limited changes; check before you commit.</p>
<h3>3. Research and strategy</h3>
<p>Looking at your market, competitors and customers before designing is what separates a logo that fits your business from one that just looks nice.</p>
<h3>4. Files and usage rights</h3>
<p>You should receive vector files (AI, EPS, SVG or PDF), web files and full ownership. Some low-cost options restrict usage or only supply low-resolution images.</p>
<h3>5. Experience</h3>
<p>A designer who has worked on established brands will usually charge more, but gets to the right answer faster and avoids costly rebrands later.</p>

<h2 id="our-prices">What a logo costs at Beyond Branding</h2>
<p>We publish our prices so you can budget before you get in touch. Every quote is fixed and agreed before work begins.</p>
[[TIERS:identity]]
<p>For context, the same studio has delivered work for Marriott, DoubleTree by Hilton and the Government of Dubai Media Office. A dedicated production team behind every project is what lets us keep these prices well below typical agency rates.</p>

<h2 id="fair-quote">How to tell if a logo quote is fair</h2>
<ul>
<li>Does it list the deliverables: concepts, revision rounds, file formats and guidelines?</li>
<li>Do you own the final design outright?</li>
<li>Can the designer show relevant work, ideally in your industry?</li>
<li>Is the price fixed, or could it grow with extra rounds?</li>
<li>Will you get vector files your printer and web developer can use?</li>
</ul>
<div class="callout"><strong>Want a number for your project?</strong> Send a one-line brief on <a href="[[WA]]" target="_blank" rel="noopener">WhatsApp</a> and Ayush will reply with a fixed price, usually the same day.</div>
""",
        faqs=[
            ("How much should a small business pay for a logo?", "Most small businesses get good value in the £500 to £3,000 range, where a studio delivers a considered logo plus colour, type and basic guidelines. At Beyond Branding, logos start at $500 and full identities are $1,500 to $3,000."),
            ("Is a £50 logo worth it?", "It can work as a placeholder, but very cheap logos are often template-based, hard to trademark and missing the files you need for print. Most businesses end up paying again to replace them."),
            ("How long does logo design take?", "Timelines depend on scope and feedback speed. A focused logo project moves in days rather than months; a full identity with guidelines takes longer. Your timeline is confirmed with your quote."),
            ("Do I own my logo after it's designed?", "You should. Make sure your contract transfers full ownership and that you receive editable vector files. Every Beyond Branding project includes both."),
        ],
    ),
    dict(
        slug="website-design-cost",
        title="How Much Does a Website Cost in 2026? UK Small Business Guide",
        desc="What a small business website really costs in 2026: DIY builders, freelancers, studios and agencies compared, ongoing costs and what to ask before you sign. With real prices.",
        h1="How much does a website cost in 2026?",
        lead="What small businesses actually pay for a website, what's included at each level and the ongoing costs nobody mentions up front.",
        service="website-design",
        body="""
<p><strong>Short answer:</strong> in the UK, a small business website typically costs <strong>£500 to £4,000 with a freelancer</strong>, <strong>£3,000 to £25,000+ with a web studio</strong> and <strong>£15,000 to £100,000+ with a large agency</strong>. At Beyond Branding, a landing page is <strong>$800 to $1,800</strong> and a full five-to-eight page site is <strong>$2,000 to $5,000</strong>, designed and built in-house.</p>

<h2 id="levels">Website prices by type of provider</h2>
<p>Typical 2026 UK ranges based on published industry pricing guides:</p>
<div class="tbl"><table>
<tr><th>Option</th><th>Typical upfront cost</th><th>Best for</th></tr>
<tr><td>DIY builder (Wix, Squarespace, AI tools)</td><td>Free – £50/month</td><td>Very early-stage businesses with time to build it themselves</td></tr>
<tr><td>Freelancer</td><td>£500 – £4,000</td><td>Simple sites; quality and long-term support vary</td></tr>
<tr><td>Web studio</td><td>£3,000 – £25,000+</td><td>Custom design, copy and a site built to generate enquiries</td></tr>
<tr><td>Large full-service agency</td><td>£15,000 – £100,000+</td><td>Complex platforms and multi-department projects</td></tr>
</table></div>

<h2 id="drivers">What affects the cost of a website?</h2>
<h3>Number of pages and features</h3>
<p>A one-page site is quicker than eight pages with case studies, booking, multiple languages or e-commerce. Features like online payments or custom tools add the most.</p>
<h3>Custom design or template</h3>
<p>Templates are cheaper but look generic and often load slowly. A custom design is built around your customers and your brand.</p>
<h3>Copywriting</h3>
<p>Many quotes assume you'll supply the words. Good copy is often the difference between a site that gets enquiries and one that doesn't, so check whether it's included.</p>
<h3>Search and speed</h3>
<p>Page titles, structured data, fast load times and a mobile-first layout all help you get found on Google. Ask whether they're part of the build or an extra.</p>

<h2 id="ongoing">Ongoing website costs</h2>
<ul>
<li><strong>Domain:</strong> roughly £10 to £30 a year for a .co.uk or .com.</li>
<li><strong>Hosting:</strong> from about £5 to £100+ a month, depending on the platform. Lightweight hand-built sites can be hosted very cheaply.</li>
<li><strong>Updates:</strong> either your own time or a monthly care plan.</li>
<li><strong>Builder subscriptions and plugins:</strong> the hidden cost of many DIY and template sites.</li>
</ul>

<h2 id="our-prices">What a website costs at Beyond Branding</h2>
[[TIERS:web]]
<p>Every site is custom designed, written and hand-built: no templates and no page builders. That keeps sites fast and hosting costs low. See live examples on our <a href="[[ROOT]]websites.html">websites page</a>.</p>

<h2 id="questions">Questions to ask before you sign</h2>
<ul>
<li>Is copywriting included, or do I need to write the content?</li>
<li>Will I own the site and be able to move it to another host?</li>
<li>Is basic SEO (titles, descriptions, sitemap, speed) part of the build?</li>
<li>What happens after launch, and what do changes cost?</li>
<li>Can I see live sites you've built for businesses like mine?</li>
</ul>
<div class="callout"><strong>Planning a new site?</strong> Send your current URL or a one-line brief on <a href="[[WA]]" target="_blank" rel="noopener">WhatsApp</a> and get a fixed quote, usually the same day.</div>
""",
        faqs=[
            ("How much does a small business website cost in the UK?", "Most small businesses pay between £500 and £4,000 with a freelancer and £3,000 or more with a web studio. Beyond Branding builds landing pages from $800 and full five-to-eight page sites for $2,000 to $5,000."),
            ("Is it cheaper to build a website myself?", "A DIY builder is cheaper upfront, but monthly fees, your time and lower conversion rates add up. A professionally built site usually pays for itself in enquiries."),
            ("How long does it take to build a website?", "A landing page can be ready quickly; a full site depends on pages, content and feedback. Your timeline is confirmed with your quote."),
            ("What ongoing costs should I expect?", "Budget for a domain (about £10 to £30 a year), hosting and any updates or care plan. Hand-built sites avoid most plugin and builder subscriptions."),
        ],
    ),
]


# --------------------------------------------------------------------------- helpers
def rel(html, prefix):
    """Rewrite root-relative links for pages `prefix` levels down."""
    return re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]+)"', lambda m: f'{m[1]}="{prefix}{m[2]}"', html)


def tiers_html(key, prefix=""):
    cat = next(c for c in CATEGORIES if c[0] == key)
    t = "".join(f"<div><h3>{E(tr[0])}</h3><b>{E(tr[1])}</b><span>{E(tr[3])}</span></div>" for tr in cat[4])
    return (f'<div class="tiers3 rv">{t}</div><p class="fineprint">Prices in USD, scoped and fixed before work begins. '
            f'<a href="{prefix}packages-global/index.html#{key}">Full rate card</a> · <a href="{prefix}packages-india/index.html#{key}">Prices in INR</a></p>')


def faq_html(faqs):
    return '<div class="qa rv">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs) + "</div>"


def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_ld(site, items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{site}/{u}"} for i, (n, u) in enumerate(items)]}


ORG = lambda site: {"@id": site + "/#organization"}


def _page(title, desc, site, path, ld, body):
    out = head(title, desc, site, path, {"@context": "https://schema.org", "@graph": ld})
    out = out.replace("</head>", SEO_CSS + "</head>", 1)
    return out + body + footer()


# --------------------------------------------------------------------------- service pages
def build_service(s, projects, site):
    path = f"services/{s['slug']}/"
    msg = f"Hi Ayush, I'm interested in {s['short'].lower()} design for my business."
    work = [p for p in projects if s["work_filter"](p)][:6]
    cards = "".join(image_card(p, "c4", (i % 3) * .06) for i, p in enumerate(work))
    get = "".join(f"<div class='rv' style='--d:{(i % 3) * .05:.2f}s'><h3>{E(a)}</h3><p>{E(b)}</p></div>" for i, (a, b) in enumerate(s["get"]))
    steps = "".join(f"<div class='rv'><h3>{E(a)}</h3><p>{E(b)}</p></div>" for a, b in PROCESS)
    inds = "".join(f"<span>{E(x)}</span>" for x in s["industries"])
    intro = "".join(f"<p>{E(x)}</p>" for x in s["intro"])
    if s["tiers_from"]:
        price = f"""<section class="sec2" id="pricing"><div class="wrap" style="max-width:1100px">
  <div class="sec-t rv"><h2>What it costs.</h2></div>{tiers_html(s['tiers_from'])}
</div></section>"""
    else:
        price = f"""<section class="sec2" id="pricing"><div class="wrap" style="max-width:1100px">
  <div class="sec-t rv"><h2>What it costs.</h2></div>
  <div class="tiles">
    <div class="rv"><h3>Property identity</h3><p>From $500. Logo, colour and type with usage guidelines.</p></div>
    <div class="rv"><h3>Signage, one location</h3><p>From $500. Full signage set with production artwork.</p></div>
    <div class="rv"><h3>Direct-booking website</h3><p>From $800. Fast, mobile-first and built to convert.</p></div>
  </div>
  <p class="fineprint">Most hospitality projects combine several services and are quoted as one fixed price. <a href="packages-global/index.html">Full rate card</a> · <a href="stay/index.html">Brand My Stay for holiday homes</a></p>
</div></section>"""
    others = "".join(f'<a class="rv" href="services/{o["slug"]}/index.html"><small>Service</small><h3>{E(o["short"])}</h3><p>{E(o["lead"])}</p><b>Explore {KCHEV}</b></a>'
                     for o in SERVICES if o is not s)[:]
    body = f"""<main>
<section class="hero2" style="padding-bottom:clamp(36px,5vw,56px)">
  <div class="crumb rv"><a href="index.html">Home</a> / <a href="services/index.html">Services</a> / {E(s['short'])}</div>
  <div class="eyebrow rv">{E(s['short'])}</div>
  <h1 class="h-xl rv" style="max-width:20ch;margin:0 auto">{E(s['h1'])}</h1>
  <p class="sub rv" style="--d:.2s;max-width:38ch;margin-left:auto;margin-right:auto;color:var(--muted)">{E(s['lead'])}</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Get a quote on WhatsApp</a><a class="lk" href="#pricing">See prices</a></div>
</section>
<section class="sec2" style="padding-top:0"><div class="wrap"><div class="lede rv">{intro}</div></div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>What you get.</h2></div>
  <div class="tiles">{get}</div>
</div></section>
{price}
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Selected work.</h2><a class="lk" href="portfolio.html">All work</a></div>
  <div class="grid">{cards}</div>
</div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>How it works.</h2></div>
  <div class="steps">{steps}</div>
</div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Who it's for.</h2></div>
  <div class="tags rv">{inds}</div>
  <p class="fineprint rv">Working with clients across the United Kingdom, Ireland, the United States, the UAE and India.</p>
</div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Questions, answered.</h2></div>
  {faq_html(s['faqs'])}
</div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Other services.</h2><a class="lk" href="guides/index.html">Pricing guides</a></div>
  <div class="hubs">{others}</div>
</div></section>
<section class="close">
  <h2 class="h-xl rv">Tell us what you're launching.</h2>
  <p class="sub s rv">Send one line about your brief. You'll hear back from Ayush with a direction and a fixed price.</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="mailto:ayush@beyondbranding.media?subject={E(s['short'])}%20enquiry">Email us</a></div>
</section>
</main>
"""
    svc = {"@type": "Service", "name": s["title"].split(" | ")[0], "serviceType": s["short"], "description": s["desc"], "url": f"{site}/{path}",
           "provider": ORG(site), "areaServed": ["GB", "IE", "US", "AE", "IN"]}
    if s["tiers_from"]:
        cat = next(c for c in CATEGORIES if c[0] == s["tiers_from"])
        lo = re.sub(r"[^\d]", "", cat[4][0][1].split("–")[0])
        svc["offers"] = {"@type": "Offer", "priceCurrency": "USD", "price": lo, "priceSpecification": {"@type": "PriceSpecification", "minPrice": int(lo), "priceCurrency": "USD"}}
    ld = [svc, faq_ld(s["faqs"]), crumbs_ld(site, [("Home", ""), ("Services", "services/"), (s["short"], path)])]
    return rel(_page(s["title"], s["desc"], site, path, ld, body), "../../")


def build_services_hub(site):
    cards = "".join(f'<a class="rv" href="services/{s["slug"]}/index.html"><small>{E(s["short"])}</small><h2>{E(s["h1"])}</h2><p>{E(s["lead"])}</p><b>Explore {KCHEV}</b></a>' for s in SERVICES)
    more = "".join(f'<a class="rv" href="packages-global/index.html#{cid}"><small>{E(lab)}</small><h3>{E(name)}</h3><p>{E(desc)}</p><b>See pricing {KCHEV}</b></a>'
                   for cid, lab, name, desc, _ in CATEGORIES if cid in ("events", "collateral", "signage", "campaigns", "social"))
    body = f"""<main>
<section class="hero2" style="padding-bottom:clamp(36px,5vw,56px)">
  <div class="eyebrow rv">Services</div>
  <h1 class="h-xl rv" style="max-width:18ch;margin:0 auto">Branding, packaging and websites, under one roof.</h1>
  <p class="sub rv" style="--d:.2s;max-width:38ch;margin-left:auto;margin-right:auto;color:var(--muted)">One senior creative leads every project, with a production team behind him. Published prices, fixed quotes.</p>
</section>
<section class="sec2" style="padding-top:0"><div class="wrap"><div class="hubs">{cards}</div></div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Also available.</h2><a class="lk" href="packages-global/index.html">Full rate card</a></div>
  <div class="hubs">{more}</div>
</div></section>
<section class="close">
  <h2 class="h-xl rv">Not sure what you need?</h2>
  <p class="sub s rv">Describe what you're launching and we'll suggest the right scope and price.</p>
  <div class="ctas rv"><a class="pill" href="{wa("Hi Ayush, I'd like help scoping a project.")}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="guides/index.html">Read the pricing guides</a></div>
</section>
</main>
"""
    ld = [{"@type": "CollectionPage", "name": "Services", "url": f"{site}/services/", "about": ORG(site)}, crumbs_ld(site, [("Home", ""), ("Services", "services/")])]
    return rel(_page("Branding, Packaging & Website Design Services | Beyond Branding",
                     "Brand identity, packaging, website design and hospitality branding from one senior-led studio serving the UK, US, UAE and India. Published prices from $500.",
                     site, "services/", ld, body), "../")


# --------------------------------------------------------------------------- guides
def build_guide(g, site):
    path = f"guides/{g['slug']}/"
    svc = next(s for s in SERVICES if s["slug"] == g["service"])
    msg = "Hi Ayush, I read your pricing guide and I'd like a quote."
    body_html = g["body"].replace("[[WA]]", wa(msg)).replace("[[ROOT]]", "")
    body_html = re.sub(r"\[\[TIERS:(\w+)\]\]", lambda m: tiers_html(m[1]), body_html)
    toc = "".join(f'<a href="#{i}">{E(re.sub("<[^>]+>", "", t))}</a>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html))
    body = f"""<main>
<section class="hero2" style="padding-bottom:clamp(28px,4vw,44px)">
  <div class="crumb rv"><a href="index.html">Home</a> / <a href="guides/index.html">Guides</a></div>
  <div class="eyebrow rv">Pricing guide · 2026</div>
  <h1 class="h-xl rv" style="max-width:18ch;margin:0 auto">{E(g['h1'])}</h1>
  <p class="sub rv" style="--d:.2s;max-width:40ch;margin-left:auto;margin-right:auto;color:var(--muted)">{E(g['lead'])}</p>
  <p class="byline rv">By Ayush, Founder &amp; Creative Director · Updated {UPDATED.split('-')[2].lstrip('0')} November 2026</p>
  <nav class="toc2 rv" aria-label="Contents"><b>In this guide</b>{toc}<a href="#faq">FAQs</a></nav>
</section>
<section class="sec2" style="padding-top:clamp(24px,3vw,40px)"><div class="wrap"><article class="art">{body_html}
<h2 id="faq">Frequently asked questions</h2>
</article>
<div style="margin-top:22px">{faq_html(g['faqs'])}</div>
</div></section>
<section class="sec2"><div class="wrap">
  <div class="sec-t rv"><h2>Related.</h2><a class="lk" href="guides/index.html">All guides</a></div>
  <div class="hubs">
    <a class="rv" href="services/{svc['slug']}/index.html"><small>Service</small><h3>{E(svc['short'])}</h3><p>{E(svc['lead'])}</p><b>Explore {KCHEV}</b></a>
    <a class="rv" href="portfolio.html"><small>Work</small><h3>See the portfolio</h3><p>Case studies across hospitality, retail, government and growing brands.</p><b>View work {KCHEV}</b></a>
  </div>
</div></section>
<section class="close">
  <h2 class="h-xl rv">Get a fixed price for your project.</h2>
  <p class="sub s rv">One line about your brief is enough to start. Most quotes go out the same day.</p>
  <div class="ctas rv"><a class="pill" href="{wa(msg)}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="packages-global/index.html">Full rate card</a></div>
</section>
</main>
"""
    art = {"@type": "Article", "headline": g["h1"], "description": g["desc"], "datePublished": UPDATED, "dateModified": UPDATED,
           "author": {"@type": "Person", "name": "Ayush", "jobTitle": "Founder & Creative Director", "url": site + "/"},
           "publisher": ORG(site), "mainEntityOfPage": f"{site}/{path}", "image": f"{site}/assets/og-image.jpg?v=4"}
    ld = [art, faq_ld(g["faqs"]), crumbs_ld(site, [("Home", ""), ("Guides", "guides/"), (g["h1"], path)])]
    out = _page(g["title"], g["desc"], site, path, ld, body).replace('og:type" content="website"', 'og:type" content="article"', 1)
    return rel(out, "../../")


def build_guides_hub(site):
    cards = "".join(f'<a class="rv" href="guides/{g["slug"]}/index.html"><small>Pricing guide · 2026</small><h2>{E(g["h1"])}</h2><p>{E(g["lead"])}</p><b>Read the guide {KCHEV}</b></a>' for g in GUIDES)
    body = f"""<main>
<section class="hero2" style="padding-bottom:clamp(36px,5vw,56px)">
  <div class="eyebrow rv">Guides</div>
  <h1 class="h-xl rv" style="max-width:16ch;margin:0 auto">Straight answers on what design really costs.</h1>
  <p class="sub rv" style="--d:.2s;max-width:38ch;margin-left:auto;margin-right:auto;color:var(--muted)">Plain-English guides to budgeting for branding, packaging and websites, with real numbers.</p>
</section>
<section class="sec2" style="padding-top:0"><div class="wrap"><div class="hubs">{cards}</div></div></section>
<section class="close">
  <h2 class="h-xl rv">Prefer a number for your project?</h2>
  <div class="ctas rv"><a class="pill" href="{wa("Hi Ayush, I'd like a quote.")}" target="_blank" rel="noopener">Message on WhatsApp</a><a class="lk" href="services/index.html">Our services</a></div>
</section>
</main>
"""
    ld = [{"@type": "CollectionPage", "name": "Guides", "url": f"{site}/guides/", "about": ORG(site)}, crumbs_ld(site, [("Home", ""), ("Guides", "guides/")])]
    return rel(_page("Branding & Website Design Pricing Guides | Beyond Branding",
                     "Plain-English guides to what logos, brand identities and websites cost in 2026, with UK, US and UAE price ranges and real studio prices.",
                     site, "guides/", ld, body), "../")


def build_all(projects, site, root):
    def w(path, html_out):
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f: f.write(html_out)
    w("services/index.html", build_services_hub(site))
    for s in SERVICES: w(f"services/{s['slug']}/index.html", build_service(s, projects, site))
    w("guides/index.html", build_guides_hub(site))
    for g in GUIDES: w(f"guides/{g['slug']}/index.html", build_guide(g, site))


SITEMAP_URLS = ["services/"] + [f"services/{s['slug']}/" for s in SERVICES] + ["guides/"] + [f"guides/{g['slug']}/" for g in GUIDES]
