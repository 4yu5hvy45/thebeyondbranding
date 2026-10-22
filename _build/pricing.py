# Rate cards. Edit here; pricing/ (USD) and pricing/india/ (INR) are generated from this file.
# Each category: (id, number label, name, description, [(tier, usd, inr, includes), ...])

CATEGORIES = [
    ("identity", "Identity", "Brand Identity & Logo",
     "Logo, type system, colour and the guidelines that keep it consistent everywhere it's used.",
     [("Starter", "$500 – $1,200", "₹25,000 – ₹60,000", "Logo + basic usage guide"),
      ("Signature", "$1,500 – $3,000", "₹75,000 – ₹1,50,000", "Logo + type + colour + guidelines"),
      ("Full System", "$3,000 – $6,000+", "₹1,50,000 – ₹3,00,000+", "Above + stationery + brand book")]),
    ("packaging", "Packaging", "Packaging Design",
     "Shelf-ready design that carries the brand from label to unboxing, with print-ready files.",
     [("Single SKU", "$400 – $1,200", "₹20,000 – ₹50,000", "One product, print-ready"),
      ("SKU Family", "$1,600 – $3,600", "₹80,000 – ₹1,80,000", "Up to 5 SKUs, one system"),
      ("Full Range", "$4,000 – $10,000+", "₹2,00,000 – ₹5,00,000+", "6+ SKUs + packaging style guide")]),
    ("web", "Web", "Websites",
     "A brand-consistent website or landing page, designed and built in-house to bring in enquiries.",
     [("Landing Page", "$800 – $1,800", "₹40,000 – ₹90,000", "Single-page microsite"),
      ("Full Website", "$2,000 – $5,000", "₹1,00,000 – ₹2,50,000", "5–8 pages, brand-matched"),
      ("Custom", "Scoped on request", "Scoped on request", "E-commerce, 3D and custom builds")]),
    ("events", "Events", "Event & Exhibition Branding",
     "Stage branding, booth graphics and delegate collateral for launches, trade shows and annual forums. Design only; fabrication is quoted by your booth contractor.",
     [("Booth Graphics", "$800 – $2,000", "₹40,000 – ₹90,000", "Backdrop, standees, signage"),
      ("Stage & Conference", "$3,000 – $7,000", "₹1,50,000 – ₹3,50,000", "Stage, backdrops, delegate kits"),
      ("Flagship System", "$8,000 – $20,000+", "₹4,00,000 – ₹10,00,000+", "Multi-day or annual forum scale")]),
    ("collateral", "Collateral", "Brochures & Sales Collateral",
     "Catalogues, brochures and sales decks, priced per page so a small request stays a small quote.",
     [("Compact", "$400 – $800", "₹15,000 – ₹30,000", "4–6 pages"),
      ("Standard", "$700 – $1,800", "₹35,000 – ₹80,000", "8–16 pages"),
      ("Premium", "$2,500 – $5,000+", "₹90,000 – ₹2,00,000+", "16+ pages, photography direction")]),
    ("signage", "Environment", "Retail & Environmental Signage",
     "Store signage, wayfinding and counter branding that carries the identity into physical space.",
     [("Single Location", "$500 – $1,500", "₹25,000 – ₹75,000", "Full signage set, one site"),
      ("Rollout", "$300 – $800", "₹15,000 – ₹40,000", "Per additional location"),
      ("Multi-site", "Scoped on request", "Scoped on request", "Large multi-site chains")]),
    ("campaigns", "Campaigns", "Print & Digital Ad Campaigns",
     "Newspaper, magazine and digital ad creative built from one core campaign idea.",
     [("Single Creative", "$150 – $400", "₹8,000 – ₹20,000", "1 print or digital ad"),
      ("Campaign Set", "$700 – $1,800", "₹35,000 – ₹80,000", "5–8 creatives, one idea"),
      ("Multi-market", "Scoped on request", "Scoped on request", "Multi-market rollouts")]),
    ("social", "Social", "Social Media Content Systems",
     "A reusable template system so your team can post on-brand without redesigning every time.",
     [("Template System", "$400 – $900", "₹20,000 – ₹45,000", "10–15 reusable templates"),
      ("Monthly Retainer", "$800 – $1,800/mo", "₹40,000 – ₹90,000/mo", "Ongoing content design"),
      ("Multi-platform", "Scoped on request", "Scoped on request", "Multi-platform systems")]),
]

BUNDLES = [
    ("Startup Identity Launch", "$2,400 – $4,400", "₹1,20,000 – ₹2,20,000",
     ["Signature brand identity", "Social content template system", "Compact brochure (4–6 pages)"]),
    ("Retail / Product Launch", "$6,000 – $13,000", "₹3,00,000 – ₹6,50,000",
     ["Brand identity system", "Packaging: SKU family", "Signage + sales collateral"]),
    ("Event & Exhibition Complete", "$5,000 – $12,000", "₹2,50,000 – ₹6,00,000",
     ["Stage & conference branding", "Booth graphics", "Social content + delegate collateral"]),
]

# "From" price shown on the homepage, work and case pages (USD)
STARTS = {"identity": "$500", "packaging": "$400", "web": "$800", "events": "$800", "collateral": "$400",
          "signage": "$500", "campaigns": "$150", "social": "$400"}
STARTS_INR = {"identity": "₹25,000", "packaging": "₹20,000", "web": "₹40,000", "events": "₹40,000", "collateral": "₹15,000",
              "signage": "₹25,000", "campaigns": "₹8,000", "social": "₹20,000"}
