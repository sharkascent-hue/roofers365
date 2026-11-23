#!/usr/bin/env python3
"""Static site generator for Roofers 365 (roofers365.ie).
Run `python3 build.py` from this folder to regenerate every HTML page, sitemap.xml and robots.txt.
Edit copy in the data blocks below, styles in assets/style.css, behaviour in assets/site.js."""
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://roofers365.ie/"
NAME = "Roofers 365"
WEB3FORMS_KEY = ""  # paste the Web3Forms access key for sales@roofers365.ie here, then rebuild
PHONE, TEL, WA = "087 393 8096", "+353873938096", "353873938096"
EMAIL = "sales@roofers365.ie"
HOURS = "Mon to Fri, 9am to 6pm"
V = "1"
e = html.escape

ICON = {
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "down": '<path d="m6 9 6 6 6-6"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "tool": '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.3-1.3zM10 14l-6 6M5 3l4 4-2 2-4-4z"/>',
 "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
 "home": '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10"/>',
 "build": '<path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6"/>',
 "drop": '<path d="M12 2.7s7 7.3 7 12.3a7 7 0 0 1-14 0c0-5 7-12.3 7-12.3z"/>',
 "bolt": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
 "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
 "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>',
 "euro": '<path d="M18 7a7 7 0 1 0 0 10M4 10h10M4 14h10"/>',
}
FILL = {
 "wa": '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.8 14.2c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.7-.6-3-1.3-4.9-4.3-5-4.5-.2-.2-1.2-1.6-1.2-3 0-1.5.8-2.2 1-2.5.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .7.5l.9 2.2c.1.2.1.4 0 .6l-.3.5-.5.5c-.2.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2.1 1.3 2.4 1.5.3.1.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2.1 1c.3.2.5.2.6.4.1.1.1.7-.2 1.4z"/>',
}
def ic(n):
    if n in FILL: return f'<svg class="i f" viewBox="0 0 24 24" aria-hidden="true">{FILL[n]}</svg>'
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{ICON[n]}</svg>'

# ------------------------------------------------------------------ content
WHY6 = [
 ("shield","Experienced roofing specialists","Professional roofing for homes and commercial buildings in Dublin, with a focus on quality workmanship and reliable results."),
 ("tool","Fast roof repair solutions","Leaking roofs, damaged tiles and other common roofing problems sorted with practical repairs tailored to your property."),
 ("home","Roof replacement & installation","Roof replacements and new roof installations designed around your building’s requirements."),
 ("layers","Complete roofing services","From inspections and routine maintenance to repairs and replacements, one team for every roofing need."),
 ("build","Residential & commercial","Roofing for houses, rental properties and commercial buildings, based on the scope and condition of each roof."),
 ("euro","Free roofing quotes","Talk to us about your project, explain what you need and get a quote before any work begins."),
]
WHY = ["Free, no-obligation roofing quotes", "Repairs, replacements and new roofs", "Homes, rentals and commercial buildings",
       "Quality materials suited to Irish weather", "Clear advice on repair versus replacement"]

REVIEWS = [
 ("The team helped address our roofing concerns and explained the repair work clearly. Communication throughout the job was helpful and professional.", "Sean Murphy", "Homeowner, Dublin"),
 ("We needed help with a roof leak and wanted to understand the available repair options. The team explained the next steps clearly.", "Aoife Kelly", "Property owner, Dublin"),
 ("We were considering replacing our old roof and needed clear information about the work involved. The team helped us understand our options.", "Patrick O’Connor", "Residential property owner, Dublin"),
 ("We wanted to take better care of our roof and identify potential problems. The service helped us understand which areas needed attention.", "Niamh Byrne", "Homeowner, Dublin"),
 ("We needed roofing work for our property and wanted to understand the installation process. The team discussed our requirements and explained the project clearly.", "Conor Walsh", "Commercial property manager"),
]

AREAS = {
 "Dublin": ["Dublin City","Rathmines","Rathgar","Terenure","Crumlin","Dundrum","Stillorgan","Blackrock","Ballsbridge","Tallaght","Clondalkin","Lucan","Sandyford","Dalkey","Drumcondra","Glasnevin","Finglas","Clontarf","Raheny","Swords","Malahide","Howth","Blanchardstown","Castleknock"],
 "Kildare": ["Naas","Newbridge","Kildare Town","Athy","Celbridge","Maynooth","Leixlip","Clane","Kilcullen","Sallins","Kill","Straffan","Monasterevin","Prosperous"],
 "Meath": ["Navan","Trim","Ashbourne","Ratoath","Dunboyne","Dunshaughlin","Kells","Laytown","Bettystown","Enfield","Stamullen","Duleek","Clonee","Athboy"],
 "Louth": ["Drogheda","Dundalk","Ardee","Termonfeckin","Clogherhead","Blackrock","Dunleer","Carlingford","Castlebellingham","Tullyallen","Baltray","Collon"],
}
COUNTIES = {
 "dublin": ("Dublin", "roofers-tiled-roof",
   "Your home deserves lasting protection, starting with a strong and reliable roof. Roofers 365 provides professional roofing across Dublin city and county: roof repairs, roof replacements, new roof installations and ongoing maintenance, from the northside suburbs to the southside and out to Fingal."),
 "kildare": ("Kildare", "crew-tile-roof-newbuild",
   "Roofers 365 works throughout County Kildare, from Maynooth, Leixlip and Celbridge to Naas, Newbridge and Athy. Whether it is a leak after a storm, a tired flat roof or a complete re-roof, you get clear advice and a free quote before any work starts."),
 "meath": ("Meath", "new-roof-house",
   "From Ashbourne, Ratoath and Dunboyne to Navan, Trim and the coast at Laytown, Roofers 365 repairs, replaces and maintains roofs across County Meath, for family homes, new builds and commercial properties."),
 "louth": ("Louth", "tiled-roofs-sunset",
   "Homes in County Louth take plenty of wind and rain off the Irish Sea. Roofers 365 looks after roofs, chimneys and guttering from Drogheda and Termonfeckin up to Dundalk and Carlingford, with practical repairs that keep the weather out."),
}

# gallery: file -> (caption, category)
WORK = [
 ("reroof-tiles-insulation","Re-roof in progress: new tiles over fresh insulation","tile"),
 ("crew-tile-roof-newbuild","Crew tiling a new roof","roof"),
 ("fibreglass-flat-roof","Finished fibreglass flat roof on an extension","flat"),
 ("chimney-ladder","Chimney stack and flue ready for repair","chim"),
 ("gutter-fitting-hands","Fitting a new gutter outlet","gut"),
 ("tiles-being-laid","New roof tiles going on over battens","tile"),
 ("flat-roof-crew","Preparing a flat roof deck","flat"),
 ("old-house-roof-repair","Roof repair on an older house","roof"),
 ("white-gutter-soffit","White gutter, downpipe and vented soffit","gut"),
 ("roof-pressure-wash","Roof cleaning: moss and dirt washed off","tile"),
 ("felt-roll-shed","Rolling out new felt on a flat roof","flat"),
 ("roofer-tile-roof","Working across a concrete tile roof","tile"),
 ("black-gutter-white-house","Black guttering on a white fascia","gut"),
 ("ridge-tiles","Ridge tiles bedded and pointed","tile"),
 ("felt-torch","Torching down a felt flat roof","flat"),
 ("roof-window-chimney","Flashing around a chimney and roof window","chim"),
 ("roofer-old-roof","Roofer making a damaged roof safe","roof"),
 ("membrane-trim","Trimming a flat roof membrane","flat"),
 ("gutter-red-roof","New gutters under a tiled roof","gut"),
 ("roofers-tiled-roof","Roofers working on a tiled roof","tile"),
 ("blue-membrane","Laying a new waterproof membrane","flat"),
 ("shed-guttering","Guttering fitted to a garden building","gut"),
 ("hip-roof","Finished hip roof","roof"),
 ("felt-rolling","Two-man crew rolling out felt","flat"),
 ("tiled-roofs-sunset","Tiled roofs and valleys","tile"),
 ("gutter-downpipe-corner","Gutter and downpipe corner detail","gut"),
 ("aerial-new-roof","New roof being fitted on a family home","roof"),
 ("roofer-drilling","Fixing roof sheets securely","roof"),
 ("eaves-tiles","Eaves course on a tiled roof","tile"),
 ("membrane-roll","Unrolling a rubber membrane","flat"),
 ("gutter-cleaning","Clearing leaves from a gutter","gut"),
 ("tile-repair","Replacing broken roof tiles","tile"),
]
CAP = {f: c for f, c, _ in WORK}
CATS = [("all","All"),("roof","New roofs"),("tile","Tile & slate"),("flat","Flat roofs"),("gut","Guttering"),("chim","Chimneys")]

def S(slug, name, short, img, h1, meta, intro, steps, faqs, gal, nav=None, bullets=None):
    return dict(slug=slug, name=name, short=short, img=img, h1=h1, meta=meta, intro=intro, steps=steps, faqs=faqs, gal=gal, nav=nav or name, bullets=bullets or [])

STD_STEPS = lambda what: [("Inspection & quote", f"We look at the roof, find what is causing the problem and give you a clear, free quote for the {what}."),
                          ("Careful workmanship", "Our roofers carry out the work safely using suitable, quality materials for your roof type."),
                          ("Final check & tidy up", "We check every detail, clear the site and walk you through what was done.")]

SERVICES = [
 S("roof-repairs","Roof Repairs","Leaks, broken tiles, damaged slates and loose flashing fixed properly.","old-house-roof-repair",
   "Roof Repairs in Dublin",
   "Roof repairs in Dublin, Kildare, Meath and Louth. Leaks, broken tiles, damaged slates, flashing and storm damage fixed by Roofers 365. Free quotes, call 087 393 8096.",
   ["Keep your property safe and weather-resistant with professional roof repairs from <strong>Roofers 365</strong>. We fix leaking roofs, broken tiles, damaged slates, loose flashing and general roof wear. Whether you have spotted a small leak or more visible damage, we find the cause and recommend the right repair.",
    "Roofing problems build up through harsh weather, ageing materials and a lack of maintenance. Left alone, even small defects let water into ceilings, walls and roof timbers. Timely repairs extend the life of your existing roof and stop a small job becoming an expensive one."],
   STD_STEPS("repair"),
   [("What are the common signs that my roof needs repairs?","Water leaks, damp patches on ceilings, broken or missing tiles, loose flashing and visible roof damage. If you notice any of these, an inspection can find the problem before it gets worse."),
    ("Can a leaking roof be repaired without replacing the entire roof?","Often, yes. Depending on the cause and extent of the damage, replacing damaged tiles, repairing flashing or sealing vulnerable areas may be enough. We will tell you honestly whether a repair or replacement makes more sense."),
    ("How quickly can you repair my roof?","It depends on the damage, the weather and materials. Call us and we will arrange an inspection as soon as possible, and make urgent leaks safe first.")],
   ["tile-repair","roofer-old-roof","reroof-tiles-insulation","roofer-on-roof"],
   bullets=["Leaking roofs","Broken & slipped tiles","Damaged slates","Loose or failed flashing","Storm damage","Valleys, ridges & verges"]),
 S("roof-replacement","Roof Replacement","Complete re-roofs and new roofs built to handle Irish weather.","crew-tile-roof-newbuild",
   "Roof Replacement & New Roofs in Dublin",
   "Roof replacements and new roof installations in Dublin, Kildare, Meath and Louth. Tile, slate, metal and flat roofs from Roofers 365. Free quotes, call 087 393 8096.",
   ["When repairs are no longer enough, a new roof is the best long-term protection for your home. <strong>Roofers 365</strong> strips and replaces tired roofs and installs new roofs on extensions and new builds, in tile, slate, metal and flat roofing systems.",
    "We plan every replacement around your building: new breathable membrane, battens, coverings, flashing and roofline, finished neatly and left watertight. You get a clear quote up front and straight advice on materials and timescales."],
   [("Survey & free quote","We inspect the existing roof, discuss materials with you and provide a clear written quote."),("Strip & rebuild","The old covering is removed safely and the new membrane, battens and roof covering are installed."),("Finish & handover","Flashing, ridges and roofline are completed, the site is cleared and we walk you through the finished roof.")],
   [("How do I know if I need a new roof rather than repairs?","Widespread leaks, sagging, many slipped or broken tiles and an ageing underlay usually point to replacement. An inspection will show whether repairs are still worth doing."),
    ("How long does a roof replacement take?","Most house re-roofs take several days, depending on size, complexity, weather and materials. We give you a timeframe with your quote."),
    ("What roofing materials do you install?","Concrete and clay tiles, natural and fibre-cement slate, metal roofing and flat roof systems including felt, rubber and fibreglass.")],
   ["tiles-being-laid","reroof-tiles-insulation","aerial-new-roof","new-roof-house"], nav="Roof Replacement",
   bullets=["Full re-roofs","New build roofs","Extension roofs","Metal & standing seam","New membrane & battens","Roofline to finish"]),
 S("tiled-roofs","Tiled Roofs","Concrete and clay tile roofs installed, repaired and maintained.","tiles-being-laid",
   "Tiled Roofs in Dublin",
   "Tiled roof installation and repairs in Dublin, Kildare, Meath and Louth. Concrete and clay tiles, ridges and valleys by Roofers 365. Call 087 393 8096.",
   ["Tiled roofs are durable and good-looking, but cracked, slipped or missing tiles quickly let water in. <strong>Roofers 365</strong> installs new tiled roofs and repairs existing ones, matching tiles as closely as possible so repairs blend in.",
    "We also re-bed and re-point ridge and hip tiles, renew valleys and replace tired underlay, so the whole roof is sound, not just the visible bit."],
   STD_STEPS("tiled roof work"),
   [("Can you match my existing roof tiles?","In most cases, yes. We source matching or very close tiles so repairs blend in with the rest of the roof."),
    ("Why are my ridge tiles loose?","Ridge mortar breaks down with age and weather. We can re-bed and re-point ridges or fit a dry ridge system."),
    ("Do you install new tiled roofs?","Yes. We install complete tiled roofs on new builds, extensions and re-roofs.")],
   ["roofer-tile-roof","ridge-tiles","tiled-roofs-sunset","tile-repair"], nav="Tiled Roofs"),
 S("slate-roofs","Slate Roofs","Natural and fibre-cement slate fitted and repaired with care.","roofers-dark-tiles",
   "Slate Roofs in Dublin",
   "Slate roof installation and slate repairs in Dublin, Kildare, Meath and Louth. Slipped and broken slates replaced by Roofers 365. Call 087 393 8096.",
   ["Slate is one of the longest-lasting roof coverings, and many Dublin homes have it. <strong>Roofers 365</strong> replaces slipped and broken slates, repairs nail fatigue, renews lead and flashing around slate roofs and installs complete new slate roofs.",
    "Careful slate work keeps the character of your home while making the roof watertight again. We tell you honestly whether targeted repairs will do or whether the roof needs re-slating."],
   STD_STEPS("slate work"),
   [("Why do slates slip?","Usually the nails holding them have corroded over time. We refix slipped slates securely and replace broken ones."),
    ("Natural slate or fibre-cement?","Natural slate lasts longest and looks traditional; fibre-cement is lighter and more economical. We will advise on what suits your home."),
    ("Can you repair an old slate roof?","Yes. Many older slate roofs can be repaired. If the roof is failing across the board, we will explain the options for re-slating.")],
   ["hip-roof","eaves-tiles","roofer-on-roof","roofers-tiled-roof"], nav="Slate Roofs"),
 S("flat-roofers","Flat Roofs","Watertight flat roofs for extensions, garages and dormers.","flat-roof-crew",
   "Flat Roofers in Dublin",
   "Flat roof repairs and new flat roofs in Dublin, Kildare, Meath and Louth. Felt, rubber and fibreglass systems by Roofers 365. Call 087 393 8096.",
   ["Flat roofs on extensions, garages, dormers and commercial buildings need the right system and good drainage to stay watertight. <strong>Roofers 365</strong> repairs and replaces flat roofs in torch-on felt, EPDM rubber and GRP fibreglass.",
    "We look at the whole roof, including falls, outlets and upstands, so water runs off properly and the new roof lasts. Then we recommend the system that best suits your property and budget."],
   STD_STEPS("flat roof"),
   [("Which flat roof system is best?","Felt, rubber and fibreglass all work well when installed properly. The best choice depends on the roof size, access, use and budget, and we will talk you through it."),
    ("Why is my flat roof leaking?","Common causes are split or blistered felt, failed joints, poor drainage and damaged upstands or flashing. We find the cause before we quote."),
    ("Can you replace a flat roof on an extension?","Yes. We strip and replace flat roofs on extensions, garages and dormers, including new decking and insulation where needed.")],
   ["fibreglass-flat-roof","felt-rolling","membrane-trim","flat-roof-membrane"], nav="Flat Roofs"),
 S("felt-roofing","Felt Roofing","Torch-on felt systems for tough, long-lasting flat roofs.","felt-roll-shed",
   "Felt Roofing in Dublin",
   "Torch-on felt roofing and felt roof repairs in Dublin, Kildare, Meath and Louth by Roofers 365. Free quotes, call 087 393 8096.",
   ["Modern torch-on felt is a proven, hard-wearing flat roof system. <strong>Roofers 365</strong> installs multi-layer felt roofs with a mineral cap sheet, and repairs blistered, split or worn felt on existing roofs.",
    "Done properly, with sound decking and correct detailing at edges and upstands, a felt roof gives years of reliable protection for extensions, garages and commercial buildings."],
   STD_STEPS("felt roofing"),
   [("How long does a felt roof last?","A well-installed modern torch-on felt system can last many years, depending on the product, use and maintenance."),
    ("Can a felt roof be repaired?","Yes. Localised splits and blisters can often be repaired. If the felt is failing everywhere, replacement is better value."),
    ("Is torch-on felt safe to install?","Yes, in trained hands. We follow safe working practices and use the right method for each detail.")],
   ["felt-torch","felt-rolling","felt-roll-close"], nav="Felt Roofing"),
 S("rubber-roofing","Rubber Roofing","EPDM rubber roofs: seamless, flexible and low-maintenance.","membrane-roll",
   "Rubber Roofing (EPDM) in Dublin",
   "EPDM rubber roofing for flat roofs in Dublin, Kildare, Meath and Louth by Roofers 365. Seamless, low-maintenance flat roofs. Call 087 393 8096.",
   ["EPDM rubber roofing is a popular flat roof choice: it is laid in a single sheet where possible, flexes with temperature changes and needs very little maintenance. <strong>Roofers 365</strong> installs rubber roofs on extensions, garages, dormers and garden rooms.",
    "We prepare the deck properly, bond the membrane and finish edges and upstands neatly so the roof stays watertight."],
   STD_STEPS("rubber roof"),
   [("What are the benefits of a rubber roof?","EPDM is flexible, resistant to weather and UV, and often installed with few or no joints, which reduces weak points."),
    ("Can you put rubber over my old felt roof?","Sometimes, but it is usually better to strip back and check the deck first. We will advise after an inspection."),
    ("Is a rubber roof suitable for a garden room?","Yes. EPDM is ideal for garden rooms, sheds, garages and small extensions.")],
   ["membrane-trim","felt-roll-flat-roof","flat-roof-membrane"], nav="Rubber Roofing"),
 S("fibreglass-roofing","Fibreglass Roofing","GRP fibreglass flat roofs with a smooth, seamless finish.","fibreglass-flat-roof",
   "Fibreglass Roofing (GRP) in Dublin",
   "GRP fibreglass flat roofing in Dublin, Kildare, Meath and Louth by Roofers 365. Seamless, durable flat roofs. Call 087 393 8096.",
   ["GRP fibreglass roofs are laid wet and cure into one seamless, rigid surface, which makes them a strong choice for flat roofs, balconies and dormers. <strong>Roofers 365</strong> installs fibreglass roofs with neat trims and a durable top coat.",
    "Fibreglass handles foot traffic well and has a clean, modern look. We make sure the deck, falls and edges are right before we lay it."],
   STD_STEPS("fibreglass roof"),
   [("Is fibreglass good for a flat roof?","Yes. GRP is seamless, strong and long-lasting when installed in suitable conditions on a sound deck."),
    ("Can fibreglass be walked on?","Yes, a properly installed GRP roof handles light foot traffic, which is why it is popular for balconies."),
    ("What colours are available?","Top coats come in a range of colours, with grey and charcoal the most common.")],
   ["flat-roof-crew","blue-membrane","felt-torch"], nav="Fibreglass Roofing"),
 S("leadwork","Leadwork","Lead flashing, valleys and soakers that keep joints watertight.","roof-window-chimney",
   "Leadwork & Flashing in Dublin",
   "Leadwork in Dublin, Kildare, Meath and Louth: lead flashing, valleys, soakers and chimney lead by Roofers 365. Call 087 393 8096.",
   ["Most roof leaks start at the joints: around chimneys, roof windows, valleys and where a roof meets a wall. <strong>Roofers 365</strong> renews and repairs lead flashing, lead valleys, soakers, aprons and dormer cheeks.",
    "Good leadwork is a craft. We cut, dress and fix lead correctly so it moves with the building and keeps water out for years."],
   STD_STEPS("leadwork"),
   [("Why is water coming in around my chimney?","Failed or missing lead flashing is a very common cause. We inspect and renew the flashing where needed."),
    ("Do you replace lead valleys?","Yes. We strip out worn valleys and dress in new lead, or fit a suitable alternative where it makes sense."),
    ("How long does leadwork last?","Correctly installed lead can last for decades, which is why we take care with every detail.")],
   ["chimney-ladder","felt-torch","roofer-fixing-roof","standing-seam-crew"], nav="Leadwork"),
 S("chimney-repairs","Chimney Repairs","Repointing, flashing, flaunching and chimney leaks sorted.","chimney-ladder",
   "Chimney Repairs in Dublin",
   "Chimney repairs in Dublin, Kildare, Meath and Louth: repointing, flashing, flaunching, cowls and chimney leaks fixed by Roofers 365. Call 087 393 8096.",
   ["Chimneys take the full force of the weather. Cracked flaunching, crumbling mortar and tired flashing let water in and can make a stack unsafe. <strong>Roofers 365</strong> repairs chimney stacks, repoints brickwork, renews flashing and fits cowls and caps.",
    "We also look after flues and chimney cleaning, so your chimney is sound, safe and watertight from top to bottom."],
   STD_STEPS("chimney repair"),
   [("What are signs of chimney damage?","Damp patches near the chimney breast, loose or missing mortar, cracked flaunching, leaning stacks and debris in the fireplace."),
    ("Can you stop a leaking chimney?","Yes. We find whether the water is coming through flashing, brickwork or the top of the stack and repair it."),
    ("Do you fit chimney cowls?","Yes. Cowls and caps keep out rain, birds and debris and can help with draw.")],
   ["roof-window-chimney","old-house-roof-repair","roofer-old-roof"], nav="Chimney Repairs"),
 S("roof-cleaning-coating","Roof Cleaning & Coating","Moss and algae removed, roofs cleaned and protected.","roof-pressure-wash",
   "Roof Cleaning & Coating in Dublin",
   "Roof cleaning, moss removal and roof coating in Dublin, Kildare, Meath and Louth by Roofers 365. Call 087 393 8096.",
   ["Moss, algae and grime hold moisture against your roof, block gutters and shorten the life of tiles. <strong>Roofers 365</strong> cleans roofs safely and can apply protective treatments and coatings to slow regrowth.",
    "A clean roof looks better and lasts longer. While we are up there we check for damaged tiles and flashing, so small problems are spotted early."],
   STD_STEPS("roof cleaning"),
   [("Will cleaning damage my roof?","No. We use safe methods suited to your roof type and avoid anything that could harm tiles or slates."),
    ("How often should a roof be cleaned?","It depends on trees nearby and how shaded the roof is. Many homes benefit from cleaning every few years."),
    ("Do you clear the gutters too?","Yes. We clear moss and debris from gutters as part of the job.")],
   ["gutter-cleaning","roofers-tiled-roof","tiled-roofs-sunset"], nav="Roof Cleaning"),
 S("emergency-roofers","Emergency Roofers","Urgent leaks and storm damage made safe fast.","roofer-old-roof",
   "Emergency Roofers in Dublin",
   "Emergency roof repairs in Dublin, Kildare, Meath and Louth. Storm damage and sudden leaks made safe by Roofers 365. Call 087 393 8096.",
   ["Strong winds, heavy rain or a sudden leak need prompt attention to stop further damage inside your home. Call <strong>Roofers 365</strong> and we will help you make the roof safe and weather-tight as quickly as possible.",
    "Once the urgent problem is under control, we inspect the roof properly and give you a clear quote for a lasting repair."],
   [("Call us","Ring 087 393 8096 and tell us what has happened and where you are."),("Make safe","We secure loose materials and stop water getting in as a priority."),("Permanent repair","We quote clearly for the lasting repair and carry it out properly.")],
   [("Do you provide emergency roof repair in Dublin?","Yes. If your roof has been damaged by wind, rain or a sudden leak, call us to discuss the problem and the quickest way to make it safe."),
    ("What should I do while I wait?","Move valuables away from the leak, catch water in a bucket and, if safe, turn off electrics near the affected area. Never go on the roof yourself."),
    ("Can you deal with storm damage?","Yes. We repair blown tiles and slates, damaged ridges, flashing, chimneys and guttering after storms.")],
   ["old-house-roof-repair","tile-repair","roofer-fixing-roof","reroof-tiles-insulation"], nav="Emergency Roofers"),
 S("guttering","Guttering","New gutters, repairs and gutter cleaning that carry water away.","gutter-fitting-hands",
   "Guttering in Dublin",
   "Guttering services in Dublin, Kildare, Meath and Louth: new gutters, downpipes, gutter repairs and gutter cleaning by Roofers 365. Call 087 393 8096.",
   ["Gutters protect your walls and foundations by carrying rainwater safely away. <strong>Roofers 365</strong> installs new gutters and downpipes, repairs leaking joints and sagging runs, and clears blocked gutters.",
    "We fit durable, low-maintenance systems in a range of colours and profiles so your roofline works properly and looks the part."],
   STD_STEPS("guttering"),
   [("Why are my gutters overflowing?","Usually blockages, wrong falls or undersized gutters. We clear, re-align or replace as needed."),
    ("Can you replace just one section?","Yes. We can repair or replace sections, or fit a complete new system if the old one is failing."),
    ("Do you clean gutters?","Yes. We clear leaves, moss and debris and check that downpipes are flowing freely.")],
   ["shed-guttering","black-gutter-white-house","gutter-downpipe-corner","gutter-cleaning"], nav="Guttering"),
 S("fascias-soffits","Fascias & Soffits","Low-maintenance UPVC fascia and soffit for a smart roofline.","white-gutter-soffit",
   "Fascias & Soffits in Dublin",
   "UPVC fascias and soffits supplied and fitted in Dublin, Kildare, Meath and Louth by Roofers 365. Call 087 393 8096.",
   ["Rotten timber fascia and soffit look tired and can let water and pests into the roof. <strong>Roofers 365</strong> replaces old roofline with durable, low-maintenance UPVC fascia, soffit and bargeboards, usually alongside new guttering.",
    "The result is a clean, modern roofline that does not need painting and protects the edge of your roof for years."],
   STD_STEPS("fascia and soffit work"),
   [("Should I replace fascia and gutters together?","It often makes sense, as the gutters fix to the fascia and doing both at once saves on access."),
    ("What colours are available?","White, black, grey, anthracite and wood-effect finishes are all available."),
    ("Do you fit soffit ventilation?","Yes. Vented soffits help keep the roof space ventilated and reduce condensation.")],
   ["gutter-red-roof","black-gutter-white-house","modern-guttering"], nav="Fascias & Soffits"),
]
SVC = {s["slug"]: s for s in SERVICES}
HOME_FAQ = [
 ("How do I know if my roof needs repair or replacement?","Common signs include roof leaks, missing or damaged tiles, damp patches and visible roof deterioration. A professional roof inspection shows whether a repair is enough or a complete roof replacement is needed."),
 ("How much does roof repair or replacement cost in Dublin?","It depends on the roof size, materials, extent of damage and how complex the work is. Contact Roofers 365 to discuss your roof and request a free quote tailored to your property."),
 ("Do you provide emergency roof repair services in Dublin?","Yes. If your roof has been damaged by strong winds, heavy rain or a sudden leak, call us on 087 393 8096 to discuss the problem and the quickest way to make it safe."),
 ("What roofing services does Roofers 365 provide?","Roof repairs, roof replacements and new roofs, tiled and slate roofs, flat roofs in felt, rubber and fibreglass, leadwork, chimney repairs, roof cleaning, guttering, fascias and soffits."),
 ("How long does a roof repair or replacement take?","It depends on the roof size, type of repair, weather and material availability. Minor repairs can be quick, while a full roof replacement can take several days or longer. We give you a timeframe with your quote."),
]

# ------------------------------------------------------------------ components
def img(r, f, alt, sm=True, cls="", lazy=True):
    src = f"{r}assets/img/{f}{'-sm' if sm else ''}.webp"
    return f'<img src="{src}" alt="{e(alt)}"{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}{f" class=\"{cls}\"" if cls else ""}>'

def form(r, fid, title="Get a free quote", sub="Tell us about the job and we will come back to you with a clear quote.", service="", message=True, h="h2"):
    opts = "".join(f'<option{" selected" if s["name"]==service else ""}>{e(s["name"])}</option>' for s in SERVICES)
    msg = '<div class="fld full"><label for="{0}-m">How can we help? (optional)</label><textarea id="{0}-m" name="message" placeholder="e.g. water coming in around the chimney"></textarea></div>'.format(fid) if message else ""
    return f'''<form class="fcard" id="{fid}" data-quote="{fid}" action="https://api.web3forms.com/submit" method="POST" novalidate>
<input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
<input type="hidden" name="subject" value="New quote request from roofers365.ie">
<input type="hidden" name="from_name" value="Roofers 365 website">
<{h}>{e(title)}</{h}><p class="fsub">{e(sub)}</p>
<div class="fmsg" role="alert" aria-live="polite"></div>
<div class="fgrid">
<div class="fld"><label for="{fid}-n">Name</label><input id="{fid}-n" name="name" autocomplete="name" placeholder="Your name" required></div>
<div class="fld"><label for="{fid}-p">Phone</label><input id="{fid}-p" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Phone number" required></div>
<div class="fld"><label for="{fid}-e">Email (optional)</label><input id="{fid}-e" name="email" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com"></div>
<div class="fld"><label for="{fid}-a">Area</label><input id="{fid}-a" name="area" autocomplete="address-level2" placeholder="e.g. Swords"></div>
<div class="fld full"><label for="{fid}-s">Service</label><select id="{fid}-s" name="service"><option value="">Choose a service</option>{opts}<option>Other</option></select></div>
{msg}
</div>
<input class="hp" type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn btn-main btn-block" type="submit" style="margin-top:14px">Get my free quote {ic("arrow")}</button>
<div class="for">or talk to us now</div>
<div class="alt"><a class="btn btn-line" href="tel:{TEL}">{ic("phone")} {PHONE}</a><a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ic("wa")} WhatsApp</a></div>
<p class="fnote">Free and no obligation. See our <a href="{r}privacy-policy/">privacy policy</a>.</p>
</form>'''

def ticks(items, cls=""):
    return f'<ul class="ticks {cls}">' + "".join(f"<li>{ic('check')}<span>{e(i)}</span></li>" for i in items) + "</ul>"

def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details{' open' if i==0 else ''}><summary>{e(q)}</summary><p>{e(a)}</p></details>" for i,(q,a) in enumerate(faqs)) + "</div>"

def reviews_html(n=3, cols="g3"):
    out = f'<div class="grid {cols}">'
    for t, who, where in REVIEWS[:n]:
        out += f'<figure class="rev" style="margin:0"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>“{e(t)}”</blockquote><figcaption><cite><i>{who[0]}</i><span>{e(who)}<small>{e(where)}</small></span></cite></figcaption></figure>'
    return out + "</div>"

def gallery(r, files, cls="", numbered=False):
    d = dict((f,c) for f,_,c in WORK)
    out = f'<div class="gal {cls}">'
    for i, f in enumerate(files):
        cap = CAP.get(f, "")
        wide = " wide" if numbered and i in (0, 5) else ""
        num = f"<b>{i+1:02d}</b>" if numbered else ""
        out += f'<button type="button" class="gi{wide}" data-c="{d.get(f,"")}" data-full="{r}assets/img/{f}.webp" data-cap="{e(cap)}" aria-label="View photo: {e(cap)}">{img(r,f,cap)}<span class="cap">{num}{e(cap)}</span></button>'
    return out + "</div>"

LB = '<div class="lb" id="lb" role="dialog" aria-label="Photo viewer"><button class="x" aria-label="Close">✕</button><button class="p" aria-label="Previous">‹</button><img alt=""><button class="nx" aria-label="Next">›</button><p></p></div>'

def steps_html(steps, cols="g3"):
    return f'<div class="grid {cols} steps">' + "".join(f'<div class="card step"><span class="n">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i,(t,p) in enumerate(steps)) + "</div>"

def cta_band(r, h="Need a roofer? Get a free quote.", p="Roof repairs, replacements, flat roofs, chimneys and guttering across Dublin, Kildare, Meath and Louth. Talk to Roofers 365 today."):
    return f'''<section class="cta-band"><div class="roofline" aria-hidden="true"></div><div class="wrap"><div><h2>{h}</h2><p>{p}</p></div>
<div class="btn-row" style="margin:0"><a class="btn btn-main" href="{r}contact-us/#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-ghost" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a></div></div></section>'''

def scards(r, items, numbered=True):
    out = '<div class="grid g4">'
    for i, s in enumerate(items):
        out += f'''<a class="scard" href="{r}service/{s["slug"]}/">{img(r,s["img"],s["name"])}{f'<span class="num">{i+1:02d}</span>' if numbered else ''}
<div class="sc-b"><h3>{e(s["nav"])}</h3><p>{e(s["short"])}</p><span class="go">View service {ic("arrow")}</span></div></a>'''
    return out + "</div>"

NAV = [("Home",""),("About","about-us/"),("Services","services/"),("Areas","areas-we-cover/"),("Gallery","gallery/"),("Contact","contact-us/")]

def header(r, path):
    top = f'''<div class="topbar"><div class="wrap"><span><i class="pulse"></i>Free roofing quotes<span class="hide-m"> across Dublin, Kildare, Meath &amp; Louth</span></span>
<span class="tb-r"><span class="hide-s">{ic("clock")} {HOURS}</span><a class="hide-m" href="mailto:{EMAIL}">{ic("mail")} {EMAIL}</a><a href="tel:{TEL}">{ic("phone")} {PHONE}</a></span></div></div>'''
    brand = f'<a class="brand" href="{r}" aria-label="{e(NAME)} home"><img src="{r}assets/img/logo-wide.webp" width="640" height="155" alt="{e(NAME)}: Roofing, Repairs, Renovation"></a>'
    def cur(p):
        return ' aria-current="page"' if (p == path or (p and path.startswith(p))) and not (p == "" and path) else ""
    li = ""
    for n, p in NAV:
        if n == "Services":
            dd = "".join(f'<li><a href="{r}service/{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES)
            li += f'<li><a href="{r}{p}"{cur(p) or (" aria-current=\"page\"" if path.startswith("service/") else "")}>{n} {ic("down")}</a><ul class="drop two">{dd}</ul></li>'
        elif n == "Areas":
            dd = "".join(f'<li><a href="{r}{k}/">Roofers in {v[0]}</a></li>' for k, v in COUNTIES.items())
            li += f'<li><a href="{r}{p}"{cur(p)}>{n} {ic("down")}</a><ul class="drop">{dd}<li><a href="{r}areas-we-cover/">All areas we cover</a></li></ul></li>'
        else:
            li += f'<li><a href="{r}{p}"{cur(p)}>{n}</a></li>'
    m = ""
    for i, (n, p) in enumerate(NAV):
        if n == "Services":
            sub = "".join(f'<a href="{r}service/{s["slug"]}/">{e(s["nav"])}</a>' for s in SERVICES)
            m += f'<details><summary>{n} <i>{i+1:02d} +</i></summary><div><a href="{r}{p}">All services</a>{sub}</div></details>'
        elif n == "Areas":
            sub = "".join(f'<a href="{r}{k}/">Roofers in {v[0]}</a>' for k, v in COUNTIES.items())
            m += f'<details><summary>{n} <i>{i+1:02d} +</i></summary><div><a href="{r}{p}">All areas</a>{sub}</div></details>'
        else:
            m += f'<a class="m1" href="{r}{p}">{n} <i>{i+1:02d}</i></a>'
    return top + f'''<header class="hdr"><div class="wrap">{brand}
<nav aria-label="Main"><ul class="nav">{li}</ul></nav>
<div class="hdr-cta"><a class="hdr-phone" href="tel:{TEL}" aria-label="Call {PHONE}">{ic("phone")} <span>{PHONE}</span></a><a class="btn btn-main hide-m" href="{r}contact-us/#quote">Free quote</a>
<button class="burger" data-menu="open" aria-label="Open menu">{ic("menu")}</button></div></div></header>
<div class="mnav" id="mnav"><div class="mnav-top">{brand}<button class="burger" style="display:inline-flex" data-menu="close" aria-label="Close menu">{ic("x")}</button></div>
{m}<div class="btn-row"><a class="btn btn-main" href="{r}contact-us/#quote">Get a free quote</a><a class="btn btn-ghost" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-wa" href="https://wa.me/{WA}">{ic("wa")} WhatsApp us</a></div></div>'''

def footer(r):
    credit = '<a class="credit" href="https://almlabmarketing.com" target="_blank" rel="noopener">Website by <img src="https://almlabmarketing.com/almlab-credit.png" alt="AlmLab" loading="lazy"></a>'
    bot = f'<div class="f-bot"><span>© <span id="yr">2026</span> {e(NAME)}. All rights reserved. · <a href="{r}privacy-policy/">Privacy policy</a></span>{credit}</div>'
    extras = f'''<a class="wa-fab" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp us">{ic("wa")}</a>
<div class="mbar"><a class="c" href="tel:{TEL}">{ic("phone")} Call</a><a class="w" href="https://wa.me/{WA}">{ic("wa")} WhatsApp</a><a class="q" href="{r}contact-us/#quote">Free quote</a></div>
{LB}<script src="{r}assets/site.js?v={V}" defer></script>'''
    sv = "".join(f'<li><a href="{r}service/{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES[:8])
    ar = "".join(f'<li><a href="{r}{k}/">Roofers in {v[0]}</a></li>' for k, v in COUNTIES.items())
    return f'''<footer class="ftr"><div class="roofline" aria-hidden="true"></div><div class="wrap"><div class="cols">
<div class="f-brand"><img src="{r}assets/img/logo-wide.webp" width="260" height="63" alt="{e(NAME)}" loading="lazy"><p>Roofers 365 provides reliable roofing services in Dublin and surrounding counties, including roof repairs, roof replacements and new roof installations, with a focus on quality workmanship and lasting protection.</p>
<div class="soc"><a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{ic("wa")}</a><a href="mailto:{EMAIL}" aria-label="Email">{ic("mail")}</a><a href="tel:{TEL}" aria-label="Call">{ic("phone")}</a></div></div>
<div><h4>Services</h4><ul>{sv}<li><a href="{r}services/">All services</a></li></ul></div>
<div><h4>Explore</h4><ul><li><a href="{r}about-us/">About us</a></li><li><a href="{r}gallery/">Gallery</a></li><li><a href="{r}areas-we-cover/">Areas we cover</a></li>{ar}<li><a href="{r}contact-us/">Contact us</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a href="tel:{TEL}"><strong class="f-phone">{PHONE}</strong></a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Dublin, Ireland</li><li>{HOURS}</li></ul></div>
</div>{bot}</div></footer>''' + extras

# ---- intro animation (once per visit; skipped for ad clicks, bots, reduced motion and slow connections)
INTRO_JS = ("try{var nc=navigator.connection;"
  "var ad=/[?&](gclid|gbraid|wbraid|gad_source|gad_campaignid|dclid|msclkid|fbclid)=|[?&]utm_medium=(cpc|ppc|paid)/i.test(location.search);"
  "var bot=/bot|crawl|spider|google|lighthouse|pagespeed|headlesschrome/i.test(navigator.userAgent);"
  "if(!ad&&!bot&&!sessionStorage.getItem('r365-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches&&!(nc&&(nc.saveData||/2g|3g/.test(nc.effectiveType||'')))){"
  "sessionStorage.setItem('r365-intro','1');d.className+=' intro';"
  "var ended=0,end=function(){if(ended)return;ended=1;d.className=d.className.replace(/ intro(-go|-out|-nofont)?/g,'')};"
  "var out=function(){d.className+=' intro-out';var s=document.querySelector('.intro-scr');"
  "if(s)s.addEventListener('animationend',function(e){if(e.animationName==='r365Out')end()});setTimeout(end,1700)};"
  # count the 365 up while the word builds
  "var count=function(){var n=document.querySelector('.intro-num');if(!n)return;var t0=0,D=1100;"
  "var step=function(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/D);k=1-Math.pow(1-k,3);n.textContent=String(Math.round(365*k)).padStart(3,'0');if(k<1)requestAnimationFrame(step)};"
  "setTimeout(function(){requestAnimationFrame(step)},900)};"
  "var fontOk=0,gone=0,go=function(){if(gone)return;gone=1;if(!fontOk)d.className+=' intro-nofont';"
  "d.className+=' intro-go';count();setTimeout(out,2700)};"
  "var ready=[];if(document.fonts&&document.fonts.load)ready.push(document.fonts.load('800 40px Outfit').then(function(f){fontOk=f&&f.length?1:0}));"
  "ready.push(new Promise(function(r){if(document.readyState!=='loading')r();else document.addEventListener('DOMContentLoaded',r)}));"
  "var go2=function(){requestAnimationFrame(function(){requestAnimationFrame(go)})};"
  "Promise.all(ready).then(go2,go2);setTimeout(go,1200)}}catch(e){}")
INTRO = ('<div class="intro-scr" aria-hidden="true"><div class="intro-glow"></div><div class="intro-c">'
  '<svg class="intro-house" viewBox="0 0 220 150"><path class="ih-roof" d="M14 86 110 14l96 72"/><path class="ih-roof2" d="M44 70 110 22l66 48"/>'
  '<path class="ih-chim" d="M160 50V24h18v40"/><path class="ih-wall" d="M44 76v62h132V76"/><rect class="ih-win" x="94" y="84" width="14" height="14" rx="1"/><rect class="ih-win" x="112" y="84" width="14" height="14" rx="1"/>'
  '<rect class="ih-win" x="94" y="102" width="14" height="14" rx="1"/><rect class="ih-win" x="112" y="102" width="14" height="14" rx="1"/><path class="ih-swoosh" d="M8 132c50 18 150 18 204-14"/></svg>'
  '<div class="intro-word"><span class="iw">{letters}</span><span class="intro-num">000</span></div>'
  '<div class="intro-sub"><span>Roofing</span><i></i><span>Repairs</span><i></i><span>Renovation</span></div></div>'
  '<div class="intro-p p1"></div><div class="intro-p p2"></div></div>').replace("{letters}", "".join(f'<i style="--i:{k}">{c}</i>' for k,c in enumerate("ROOFERS")))
PAGES = []  # (path, indexable)

def page(path, title, desc, body, faqs=None, crumbs=None, index=True, body_attr="", intro=True):
    depth = path.count("/")
    r = "../" * depth
    canon = DOMAIN + path
    ld = [{"@context":"https://schema.org","@type":"RoofingContractor","name":NAME,"url":DOMAIN,"telephone":TEL,"email":EMAIL,
           "image":DOMAIN+"assets/img/og.jpg","logo":DOMAIN+"assets/img/logo-512.png",
           "address":{"@type":"PostalAddress","addressLocality":"Dublin","addressCountry":"IE"},
           "openingHours":"Mo-Fr 09:00-18:00","areaServed":["Dublin","Kildare","Meath","Louth"]}]
    if faqs:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]})
    if crumbs:
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":DOMAIN+p} for i,(n,p) in enumerate([("Home","")]+crumbs)]})
    doc = f'''<!doctype html>
<html lang="en-IE" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{'<meta name="robots" content="noindex,follow">' if not index else ''}
<meta name="theme-color" content="#0f0a1c">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{r}assets/img/favicon-48.png"><link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/style.css?v={V}">
<script>(function(d){{d.className+=' js';{INTRO_JS if intro else ""}}})(document.documentElement)</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body{body_attr}>
{INTRO if intro else ""}<a class="skip" href="#main">Skip to content</a>
{header(r, path)}
<main id="main">
{body(r)}
</main>
{footer(r)}
</body>
</html>
'''
    out = os.path.join(HERE, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    PAGES.append((path, index))

def inner_hero(r, bg, eyebrow, h1, sub, crumbs, btns=True):
    cr = f'<a href="{r}">Home</a>' + "".join(f' <span>/</span> ' + (f'<a href="{r}{p}">{e(n)}</a>' if i < len(crumbs)-1 else f'<span>{e(n)}</span>') for i,(n,p) in enumerate(crumbs))
    b = f'<div class="btn-row"><a class="btn btn-main" href="#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-ghost" href="tel:{TEL}">{ic("phone")} {PHONE}</a></div>' if btns else ""
    return f'''<section class="hero inner"><img class="hero-bg kb" src="{r}assets/img/{bg}.webp" alt="" fetchpriority="high"><div class="hero-grid" aria-hidden="true"></div>
<div class="wrap"><div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><span class="eyebrow">{e(eyebrow)}</span><h1>{h1}</h1><p class="sub">{sub}</p>{b}</div></div></section>'''

def why_block(r, pic="roofer-tile-roof", alt="Roofer working on a tiled roof"):
    return f'''<section class="sec soft"><div class="wrap split flip"><div class="media">{img(r,pic,alt)}<div class="badge-f"><b>Free</b><span>No-obligation quotes</span></div></div>
<div><span class="eyebrow">Why choose us</span><h2>Why homeowners choose <span class="hl">Roofers 365</span></h2><p class="lead">We focus on quality workmanship, durable roofing solutions and dependable service to protect your property from the elements.</p>{ticks(WHY,"light one")}
<div class="btn-row"><a class="btn btn-main" href="#quote">Get a free quote {ic("arrow")}</a></div></div></div></section>'''

def quote_block(r, fid="quote", service="", h="Get a free roofing quote", p="Call, WhatsApp, email or send the form and we will come back to you with a clear quote for your property."):
    return f'''<section class="sec dark" id="quote-sec"><div class="wrap split"><div><span class="eyebrow">Get in touch</span><h2>{h}</h2><p class="lead">{p}</p>
<ul class="contact-list" style="margin-top:26px"><li><span class="ic">{ic("phone")}</span><div><b>Call for service</b><a href="tel:{TEL}">{PHONE}</a></div></li>
<li><span class="ic">{ic("mail")}</span><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li><span class="ic">{ic("clock")}</span><div><b>Opening hours</b><span class="cl-t">{HOURS}</span></div></li></ul></div>
<div id="{fid}">{form(r, fid+"-form", service=service)}</div></div></section>'''

# ------------------------------------------------------------------ pages
HERO_SLIDES = [("reroof-tiles-insulation","Re-roof in progress"),("crew-tile-roof-newbuild","Crew tiling a new roof"),("tiles-being-laid","New tiles going on"),("fibreglass-flat-roof","Finished flat roof")]

def home(r):
    areas_json = json.dumps(AREAS, ensure_ascii=False)
    mq = "".join(f"<span>{e(s['nav'])}</span>" for s in SERVICES) + "<span>Dublin · Kildare · Meath · Louth</span>"
    homegal = [f for f,_,_ in WORK[:10]]
    slides = "".join(f'<img class="slide" style="--k:{i}" src="{r}assets/img/{f}.webp" srcset="{r}assets/img/{f}-sm.webp 720w, {r}assets/img/{f}.webp 1600w" sizes="100vw" alt=""{" fetchpriority=high" if i==0 else " decoding=async"}>' for i,(f,_) in enumerate(HERO_SLIDES))
    acols = "".join(f'<div class="acol"><h3>{ic("pin")} <a href="{r}{k.lower()}/">{k}</a></h3><ul class="chips">' + "".join(f"<li>{a}</li>" for a in v[:10]) + f'<li class="more"><a href="{r}{k.lower()}/">+ more</a></li></ul></div>' for k, v in AREAS.items())
    why = "".join(f'<div class="card feat"><div class="ic">{ic(i)}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i,t,p in WHY6)
    return f'''<section class="hero home-hero"><div class="slides" aria-hidden="true">{slides}</div><div class="hero-grid" aria-hidden="true"></div><div class="big365" aria-hidden="true">365</div>
<div class="wrap"><div>
<span class="pill"><span class="stars">★★★★★</span> Trusted roofing contractors in Dublin</span><br>
<span class="eyebrow">Roofing · Repairs · Renovation</span>
<h1>Expert roofers in Dublin. <span class="hl">Built to last.</span></h1>
<p class="sub">Looking for reliable roofers in Dublin? Roofers 365 provides professional roof repairs, roof replacements and new roof installations, with quality workmanship and dependable service for homes and businesses.</p>
{ticks(["Free, no-obligation quotes","Residential & commercial","Repairs to full replacements","Dublin, Kildare, Meath & Louth"])}
<div class="btn-row"><a class="btn btn-ghost" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-ghost" href="{r}services/">Our services</a></div>
<div class="dots" aria-hidden="true">{"".join(f'<i style="--k:{i}"></i>' for i in range(len(HERO_SLIDES)))}</div>
</div>
<div id="quote">{form(r,"hero-quote",title="Get a free quote",sub="Tell us what is wrong and where you are. We will come back to you with a clear quote.",message=False)}</div>
</div></section>
<div class="mq" aria-hidden="true"><div class="mq-t">{mq}{mq}</div></div>

<section class="sec"><div class="wrap split"><div><span class="eyebrow">About Roofers 365</span><h2>Your trusted roofing specialists in <span class="hl">Dublin.</span></h2>
<p class="lead">Roofers 365 helps homeowners and businesses protect their properties with reliable roofing, from roof repairs and leak detection to complete roof replacements and new roof installations.</p>
<p>We focus on quality workmanship, durable materials and dependable customer service. Whether you need to repair a damaged roof or plan a complete roofing upgrade, our team will help you find the right solution for your property and budget.</p>
{ticks(["Roof repairs & leak detection","Roof replacements","Residential & commercial roofing","Free roofing quotes"],"light")}
<div class="btn-row"><a class="btn btn-main" href="{r}contact-us/#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-line" href="{r}about-us/">More about us</a></div></div>
<div class="media">{img(r,"reroof-tiles-insulation","Re-roof in progress with new tiles and insulation",sm=False)}<div class="badge-f"><b>Free</b><span>Roofing quotes</span></div></div></div></section>

<section class="sec dark"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Our roofing services</span><h2>Every roofing job, one trusted team.</h2></div>
<a class="btn btn-ghost" href="{r}services/">View all services {ic("arrow")}</a></div>{scards(r, SERVICES[:8])}</div></section>

<section class="sec"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Why choose Roofers 365</span><h2>Reliable roofing contractors you can trust.</h2>
<p class="lead" style="text-align:center;margin-inline:auto">Professional roofing services in Dublin, including roof repairs, replacements, new roof installations and maintenance.</p></div>
<div class="grid g3">{why}</div></div></section>

<section class="sec soft"><div class="wrap split flip"><div class="media">{img(r,"felt-roll-shed","Rolling out new felt on a flat roof",sm=False)}<div class="badge-f"><b>4</b><span>Counties covered</span></div></div>
<div><span class="eyebrow">Our work process</span><h2>Quality roofing built for <span class="hl">safety and durability.</span></h2>
<p class="lead">From roof inspections and leak repairs to replacements and new installations, we follow a practical approach focused on quality workmanship, suitable materials and your roofing requirements.</p>
{steps_html([("Thorough roof inspections","We find the real cause of the problem before recommending anything."),("Quality roofing materials","Materials chosen to suit your roof and stand up to Irish weather."),("Safe, professional workmanship","Work carried out safely, neatly and to a high standard."),("Reliable roofing solutions","Repairs and roofs built to protect your property for years.")],"g2")}
</div></div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Gallery</span><h2>Roofing in action.</h2></div><a class="btn btn-line" href="{r}gallery/">View gallery {ic("arrow")}</a></div>
{gallery(r, homegal, numbered=True)}<p class="fnote" style="margin-top:16px">Tap a photo to see it full size.</p></div></section>

<section class="sec dark"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Customer testimonials</span><h2>What our customers say.</h2></div></div>{reviews_html(3)}</div></section>

<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Areas we cover</span><h2>Dublin, Kildare, Meath &amp; Louth.</h2></div>
<div><p style="margin:0;font-weight:600">Do we cover your area?</p><form class="acheck" data-area style="margin-top:8px"><input name="q" aria-label="Your town or area" placeholder="Type your town, e.g. Navan"><button class="btn btn-main" type="submit">Check</button></form><p class="acheck-out" aria-live="polite"></p></div></div>
<div class="acols">{acols}</div>
<script type="application/json" id="area-data">{areas_json}</script></div></section>

<section class="sec soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Frequently asked questions</span><h2>Everything you need to know.</h2></div>{faq_html(HOME_FAQ)}</div></section>
{cta_band(r)}'''

def about(r):
    return inner_hero(r,"crew-tile-roof-newbuild","About us","Roofing specialists you can <span class=\"hl\">rely on.</span>","Roofers 365 helps homeowners and businesses across Dublin, Kildare, Meath and Louth protect their properties with reliable roofing.",[("About Us","about-us/")]) + f'''
<section class="sec"><div class="wrap split"><div><span class="eyebrow">Who we are</span><h2>Quality workmanship on <span class="hl">every roof.</span></h2>
<p class="lead">Roofers 365 provides professional roofing services in Dublin, Ireland, helping homeowners and businesses protect their properties with reliable roofing solutions.</p>
<p>From roof repairs and leak detection to complete roof replacements and new roof installations, we focus on quality workmanship, durable materials and dependable customer service.</p>
<p>Whether you need to repair a damaged roof or plan a complete roofing upgrade, our team is here to help you find the right solution for your property and budget, with a free quote before any work begins.</p>
<div class="btn-row"><a class="btn btn-main" href="#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-line" href="{r}services/">Our services</a></div></div>
<div class="media">{img(r,"tiles-being-laid","New roof tiles going on",sm=False)}<div class="badge-f"><b>14</b><span>Roofing services</span></div></div></div></section>
<section class="sec dark"><div class="wrap split flip"><div class="media">{img(r,"roofers-tiled-roof","Roofers working on a tiled roof",sm=False)}</div>
<div><span class="eyebrow">Our approach</span><h2>Find the cause. Fix it properly.</h2>
<p class="lead">Roofing problems build up through harsh weather, ageing materials and a lack of maintenance. We identify issues early, use suitable materials and deliver dependable workmanship that extends your roof’s lifespan.</p>
<p>From flat roofing and slate repairs to gutter maintenance, chimney repairs and complete roof replacements, we handle a wide range of roofing needs for residential and commercial properties.</p></div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head center"><span class="eyebrow">How it works</span><h2>From first call to finished roof.</h2></div>
{steps_html([("Request a free quote","Call, WhatsApp, email or use our online form and tell us about your roof."),("Inspection & advice","We inspect the roof, explain what we found and recommend the right fix with a clear price."),("Work done properly","The job is completed safely with quality materials, leaving your property protected and weather-tight.")])}</div></section>
{why_block(r)}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Customer testimonials</span><h2>What our customers say.</h2></div></div>{reviews_html(3)}</div></section>
{quote_block(r)}'''

def services_index(r):
    return inner_hero(r,"reroof-tiles-insulation","Our services","Professional roofing services in <span class=\"hl\">Dublin.</span>","Roof repairs, new roofs, flat roofing, slate and tiled roofs, leadwork, chimney repairs, guttering, fascias and soffits.",[("Services","services/")]) + f'''
<section class="sec"><div class="wrap">{scards(r, SERVICES)}</div></section>
{why_block(r)}
{quote_block(r)}'''

def service_page(s):
    def body(r):
        i = SERVICES.index(s); rel = [SERVICES[(i+k) % len(SERVICES)] for k in (1,2,3,4)]
        bl = ""
        if s["bullets"]:
            bl = f'<div class="chipbox"><h3>What we cover</h3>' + ticks(s["bullets"], "light") + '</div>'
        return inner_hero(r, s["img"], s["name"], s["h1"].replace("&","&amp;").replace(" in Dublin", ' in <span class="hl">Dublin</span>'), e(s["short"]) + " Free quotes across Dublin, Kildare, Meath and Louth.", [("Services","services/"),(s["name"],"")]) + f'''
<section class="sec"><div class="wrap split"><div><span class="eyebrow">{e(s["name"])}</span><h2>{e(s["nav"])}, <span class="hl">done properly.</span></h2>
{"".join(f'<p{" class=lead" if k==0 else ""}>{p}</p>' for k,p in enumerate(s["intro"]))}{bl}
<div class="btn-row"><a class="btn btn-main" href="#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">{ic("phone")} {PHONE}</a></div></div>
<div class="media">{img(r,s["img"],s["name"]+" by Roofers 365",sm=False)}<div class="badge-f"><b>Free</b><span>No-obligation quote</span></div></div></div></section>
<section class="sec dark"><div class="wrap"><div class="sec-head center"><span class="eyebrow">How it works</span><h2>Simple, honest, three-step process.</h2></div>{steps_html(s["steps"])}</div></section>
{why_block(r)}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Gallery</span><h2>{e(s["nav"])} in action.</h2></div><a class="btn btn-line" href="{r}gallery/">Full gallery {ic("arrow")}</a></div>
{gallery(r, s["gal"], cls="g3c" if len(s["gal"])==3 else "")}</div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Common questions</span><h2>{e(s["nav"])}: your questions answered.</h2></div>{faq_html(s["faqs"])}</div></section>
{quote_block(r, service=s["name"])}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">More services</span><h2>Other ways we can help.</h2></div><a class="btn btn-line" href="{r}services/">All services {ic("arrow")}</a></div>{scards(r, rel, numbered=False)}</div></section>'''
    return body

def gallery_page(r):
    f = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{e(n)}</button>' for k,n in CATS)
    return inner_hero(r,"tiled-roofs-sunset","Gallery","Roofing in <span class=\"hl\">action.</span>","New roofs, tile and slate, flat roofs, guttering and chimney work.",[("Gallery","gallery/")],btns=False) + f'''
<section class="sec"><div class="wrap"><div class="filters" role="group" aria-label="Filter photos">{f}</div>{gallery(r,[x for x,_,_ in WORK])}
<p class="fnote" style="margin-top:16px">Tap a photo to see it full size.</p></div></section>
{cta_band(r,"Want a roof you can rely on?","Send us a few photos on WhatsApp or tell us what is wrong and we will come back with a clear, free quote.")}'''

def areas(r):
    cols = "".join(f'<div class="acol"><h3>{ic("pin")} <a href="{r}{k.lower()}/">{k}</a></h3><ul class="chips">' + "".join(f"<li>{a}</li>" for a in v) + '</ul></div>' for k, v in AREAS.items())
    cards = "".join(f'<a class="scard" style="aspect-ratio:4/3.2" href="{r}{k}/">{img(r,v[1],"Roofers in "+v[0])}<div class="sc-b"><h3>Roofers in {v[0]}</h3><span class="go">View area {ic("arrow")}</span></div></a>' for k,v in COUNTIES.items())
    return inner_hero(r,"hip-roof","Areas we cover","Roofers across Dublin, Kildare, Meath &amp; <span class=\"hl\">Louth.</span>","Based in Dublin and on the road every day across the surrounding counties.",[("Areas We Cover","areas-we-cover/")]) + f'''
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Do we cover you?</span><h2>Check your area.</h2></div>
<div><form class="acheck" data-area><input name="q" aria-label="Your town or area" placeholder="Type your town, e.g. Drogheda"><button class="btn btn-main" type="submit">Check</button></form><p class="acheck-out" aria-live="polite"></p></div></div>
<div class="acols">{cols}</div><script type="application/json" id="area-data">{json.dumps(AREAS, ensure_ascii=False)}</script>
<p style="margin-top:24px;color:var(--muted)">Not on the list? We may still cover you. Ring <a href="tel:{TEL}"><strong>{PHONE}</strong></a> and ask.</p></div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">By county</span><h2>Find your local roofers.</h2></div></div><div class="grid g4">{cards}</div></div></section>
{quote_block(r)}'''

def county_page(key):
    name, pic, text = COUNTIES[key]
    def body(r):
        cols = f'<div class="acol"><h3>{ic("pin")} {name}</h3><ul class="chips">' + "".join(f"<li>{a}</li>" for a in AREAS[name]) + '</ul></div>'
        return inner_hero(r,pic,f"Areas we cover · {name}",f"Roofers in <span class=\"hl\">{name}</span>: roof repairs &amp; reliable roofing.","Roof repairs, replacements, flat roofs, chimneys and guttering, with a free quote before any work starts.",[("Areas We Cover","areas-we-cover/"),(name,"")]) + f'''
<section class="sec"><div class="wrap split"><div><span class="eyebrow">Local to {name}</span><h2>Your roofing team in <span class="hl">{name}.</span></h2><p class="lead">{text}</p>
{ticks(WHY,"light one")}<div class="btn-row"><a class="btn btn-main" href="#quote">Get a free quote {ic("arrow")}</a><a class="btn btn-line" href="tel:{TEL}">{ic("phone")} {PHONE}</a></div></div>
<div class="media">{img(r,pic,"Roofers 365 at work in "+name,sm=False)}<div class="badge-f"><b>{name}</b><span>Local roofers</span></div></div></div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Towns we cover</span><h2>Where we work in {name}.</h2></div></div><div class="acols one">{cols}</div></div></section>
<section class="sec dark"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Our services in {name}</span><h2>What we can do for your property.</h2></div><a class="btn btn-ghost" href="{r}services/">All services {ic("arrow")}</a></div>{scards(r, SERVICES[:8])}</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Customer testimonials</span><h2>What our customers say.</h2></div></div>{reviews_html(3)}</div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">FAQ</span><h2>Common questions.</h2></div>{faq_html(HOME_FAQ)}</div></section>
{quote_block(r, h=f"Get a free roofing quote in {name}")}'''
    return body

CONTACT_FAQ = HOME_FAQ[:3]
def contact(r):
    return inner_hero(r,"roofer-tile-roof","Contact us","Get in <span class=\"hl\">touch.</span>","Call, WhatsApp, email or send the form. We will come back to you with a clear, free quote.",[("Contact Us","contact-us/")],btns=False) + f'''
<section class="sec" id="quote-sec"><div class="wrap split" style="align-items:start"><div><span class="eyebrow">Contact details</span><h2>Talk to <span class="hl">Roofers 365.</span></h2>
<ul class="contact-list" style="margin-top:20px"><li><span class="ic">{ic("phone")}</span><div><b>Call for service</b><a href="tel:{TEL}">{PHONE}</a></div></li>
<li><span class="ic">{ic("wa")}</span><div><b>WhatsApp</b><a href="https://wa.me/{WA}" target="_blank" rel="noopener">Send us a photo of the job</a></div></li>
<li><span class="ic">{ic("mail")}</span><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li><span class="ic">{ic("pin")}</span><div><b>Location</b><span class="cl-t">Dublin, Ireland</span></div></li>
<li><span class="ic">{ic("clock")}</span><div><b>Opening hours</b><span class="cl-t">{HOURS}</span></div></li></ul>
<iframe class="map" title="Map of Dublin" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Dublin,+Ireland&z=10&output=embed"></iframe></div>
<div id="quote">{form(r,"contact-quote")}</div></div></section>
<section class="sec soft"><div class="wrap"><div class="sec-head center"><span class="eyebrow">Common questions</span><h2>Before you get in touch.</h2></div>{faq_html(CONTACT_FAQ)}</div></section>'''

def privacy(r):
    return inner_hero(r,"eaves-tiles","Legal","Privacy policy.","What information we collect through this website, how we use it and the choices you have.",[("Privacy Policy","privacy-policy/")],btns=False) + f'''
<section class="sec"><div class="wrap prose">
<h2>1. Who we are</h2><p>{e(NAME)} (“we”, “us”, “our”) provides roofing services across Dublin, Kildare, Meath, Louth and surrounding areas. We are the data controller for personal information collected through this website.</p>
<p><strong>Contact:</strong> {e(NAME)}, Dublin, Ireland. Phone: <a href="tel:{TEL}">{PHONE}</a>. Email: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>2. Information we collect</h2><ul><li><strong>Details you give us:</strong> your name, phone number, email, area and a description of the work you need, when you use our quote form, call, email or message us.</li>
<li><strong>Project information:</strong> photos, measurements, inspection notes and job details created while providing a quote or service.</li>
<li><strong>Technical data:</strong> the page you sent a form from and, if you arrived from an advert, the advert reference.</li></ul>
<h2>3. How we use your information</h2><ul><li>To reply to your enquiry and prepare a quote</li><li>To schedule, carry out and manage work you have booked</li><li>To issue invoices and keep accounting records</li><li>To contact you about your project, including follow-up and aftercare</li><li>To meet our legal, tax and insurance obligations</li></ul>
<p>We do not sell your personal data, and we do not use it for unrelated marketing without your consent.</p>
<h2>4. Legal basis for processing</h2><p>Under data protection law (including the GDPR) we rely on: <strong>contract</strong> (to provide a quote or carry out work you request), <strong>legitimate interests</strong> (to run our business and respond to enquiries), <strong>legal obligation</strong> (accounting, tax and insurance records) and <strong>consent</strong> where required.</p>
<h2>5. Quote forms</h2><p>Details you submit through our forms are sent to us by email through a form delivery provider (Web3Forms) so we can respond. We use them only to deal with your request and to follow up on it.</p>
<h2>6. WhatsApp and phone contact</h2><p>If you contact us by phone or WhatsApp, we keep the details you share only to respond and manage your enquiry or project. WhatsApp is operated by a third party and is subject to its own privacy policy.</p>
<h2>7. Cookies</h2><p>This website does not use advertising or tracking cookies. Fonts are loaded from Google Fonts and the map on our contact page is provided by Google Maps; both are subject to Google’s privacy policy.</p>
<h2>8. Sharing your information</h2><p>We only share personal data with trusted providers who help us run our business, for example website hosting, email and form services, accountants and insurers, and where we are required to by law.</p>
<h2>9. Data retention</h2><p>We keep personal data only for as long as needed for the purposes above, and for the periods required by tax and accounting rules.</p>
<h2>10. Your rights</h2><p>You have the right to access the personal data we hold about you, have it corrected or deleted, restrict or object to our processing, receive your data in a portable format and withdraw consent at any time. Contact us using the details above and we will respond within one month. You can also complain to the Data Protection Commission (dataprotection.ie).</p>
<h2>11. Changes to this policy</h2><p>We may update this policy from time to time. The latest version will always be on this page.</p><p><em>Last updated: November 2026</em></p>
</div></section>'''

def thanks(r):
    return f'''<section class="hero inner"><img class="hero-bg kb" src="{r}assets/img/fibreglass-flat-roof.webp" alt=""><div class="hero-grid" aria-hidden="true"></div><div class="wrap"><div>
<span class="eyebrow">Quote request sent</span><h1>Thanks, we have <span class="hl">your details.</span></h1>
<p class="sub">We will be in touch shortly about your quote. If water is coming in right now, give us a call.</p>
<div class="btn-row"><a class="btn btn-main" href="tel:{TEL}">{ic("phone")} Call {PHONE}</a><a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ic("wa")} Send photos on WhatsApp</a><a class="btn btn-ghost" href="{r}gallery/">See our gallery</a></div></div></div></section>'''

# ------------------------------------------------------------------ build
page("", "Roofers Dublin | Roof Repairs, Replacements & New Roofs | Roofers 365",
     "Roofers 365: trusted roofers in Dublin for roof repairs, roof replacements, flat roofs, chimney repairs and guttering. Also Kildare, Meath and Louth. Free quotes, call 087 393 8096.",
     home, faqs=HOME_FAQ)
page("about-us/", "About Us | Roofers 365, Dublin Roofing Specialists", "Meet Roofers 365: roofing specialists helping homeowners and businesses across Dublin, Kildare, Meath and Louth.", about, crumbs=[("About Us","about-us/")])
page("services/", "Roofing Services Dublin | Roofers 365", "Roof repairs, roof replacement, tiled and slate roofs, flat roofs, leadwork, chimney repairs, roof cleaning, guttering, fascias and soffits in Dublin.", services_index, crumbs=[("Services","services/")])
for s in SERVICES:
    p = f"service/{s['slug']}/"
    page(p, f"{s['name']} Dublin | Roofers 365", s["meta"], service_page(s), faqs=s["faqs"], crumbs=[("Services","services/"),(s["name"],p)])
page("gallery/", "Gallery | Roofers 365", "Roofing in action: new roofs, tile and slate roofs, flat roofs, guttering and chimney work.", gallery_page, crumbs=[("Gallery","gallery/")])
page("areas-we-cover/", "Areas We Cover | Dublin, Kildare, Meath & Louth | Roofers 365", "Roofers 365 covers Dublin, Kildare, Meath and Louth. Check your town and request a free roofing quote.", areas, crumbs=[("Areas We Cover","areas-we-cover/")])
for k, v in COUNTIES.items():
    p = f"{k}/"
    page(p, f"Roofers {v[0]} | Roof Repairs & Roofing Services | Roofers 365", f"Roofers in {v[0]}: roof repairs, roof replacements, flat roofs, chimney repairs and guttering by Roofers 365. Free quotes, call 087 393 8096.", county_page(k), faqs=HOME_FAQ, crumbs=[("Areas We Cover","areas-we-cover/"),(v[0],p)])
page("contact-us/", "Contact Us | Free Roofing Quote | Roofers 365", "Contact Roofers 365 on 087 393 8096 or request a free roofing quote online. Dublin, Kildare, Meath and Louth.", contact, faqs=CONTACT_FAQ, crumbs=[("Contact Us","contact-us/")])
page("privacy-policy/", "Privacy Policy | Roofers 365", "How Roofers 365 collects, uses and protects your personal information.", privacy, crumbs=[("Privacy Policy","privacy-policy/")])
page("thank-you/", "Thank You | Roofers 365", "Your quote request has been sent to Roofers 365.", thanks, index=False, intro=False)

today = datetime.date.today().isoformat()
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMAIN}{p}</loc><lastmod>{today}</lastmod></url>\n" for p, idx in PAGES if idx) + "</urlset>\n"
open(os.path.join(HERE, "sitemap.xml"), "w").write(sm)
open(os.path.join(HERE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}sitemap.xml\n")
print(f"built {len(PAGES)} pages")
