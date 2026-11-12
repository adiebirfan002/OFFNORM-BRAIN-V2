"""Builds the OFFNORM collection line-up proposal: ../lineup.html
Run from the repo root:  python3 brand/collections/source/build.py"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(OUT, "..", "identity", "source"))
from kit import *
from mocks import tile, cloth, fold, stitch, mono, TEE, TEEB
INK, CHALK = "#151617", "#F3F4F2"

# name, code, place, lat, lon, altitude, conditions (estimate), founder's words, palette, tee (body, panel, seam, light?), band (bg, fg), hero pieces, note
C = [
 dict(n="The Moss", code="MOS", place="Mossy Forest, Gunung Brinchang, Cameron Highlands", lat=4.5239, lon=101.3819, alt="about 2,000 m",
      cond=("14°C", "95% RH", "06:30"), words="Cold, misty, dark, green",
      pal=[("Lumut", "#2F3B2A"), ("Lichen", "#8A9A5B"), ("Kabus", "#C9CFCB"), ("Kulit kayu", "#3A2E24"), ("Spora", "#B7C948")],
      tee=("#2F3B2A", "#C9CFCB", "#B7C948", False), band=("#222B1F", CHALK), motif="moss",
      hero=["Brushed long sleeve", "Packable mist shell"], idea="Still and soft. Heavier brushed cotton for a cold start, dots that cluster like moss on bark."),
 dict(n="The Wild", code="WLD", place="Gunung Tahan, Taman Negara, Pahang", lat=4.6325, lon=102.2342, alt="2,187 m, highest point in the peninsula",
      cond=("12°C", "96% RH", "05:45"), words="Cold, misty, mysterious, wild, high altitude, the river",
      pal=[("Malam", "#121A17"), ("Sungai", "#8A6B4A"), ("Rimba", "#1F3A2E"), ("Kabus", "#BFC6C0"), ("Enggang", "#E08A2B")],
      tee=("#121A17", "#8A6B4A", "#E08A2B", False), band=("#101613", CHALK), motif="river",
      hero=["River short, quick drain", "Trail long sleeve"], idea="Moving and dark. Night black with the tea-brown of the river and one hornbill-orange seam. The back print is a river."),
 dict(n="The Sky", code="SKY", place="Sky Mirror, Sasaran, Kuala Selangor (suggested)", lat=3.2094, lon=101.1865, alt="sea level, a sandbar at low tide",
      cond=("30°C", "70% RH", "07:10"), words="Harmonious, blue, warm, clouds",
      pal=[("Langit", "#7FB2DD"), ("Awan", "#F1F2EF"), ("Senja", "#F2C7A0"), ("Biru tua", "#2E5C8A"), ("Matahari", "#F4D24A")],
      tee=("#7FB2DD", "#F1F2EF", "#F4D24A", True), band=("#CFE2F2", INK), motif="sky",
      hero=["Open-mesh singlet", "Featherweight cap"], idea="Air. The lightest fabrics in the line, pale blue and white, a sun ring on the back."),
 dict(n="The Ocean", code="OCN", place="Pulau Redang, Terengganu", lat=5.7750, lon=103.0150, alt="sea level",
      cond=("29°C", "78% RH", "07:00"), words="As far as the eyes can see, peace, blue, warmth, waves",
      pal=[("Karang", "#1E9AA8"), ("Laut dalam", "#0F4C6B"), ("Pasir", "#E6D9BD"), ("Buih", "#F3F4F2"), ("Batu karang", "#F0775A")],
      tee=("#1E9AA8", "#E6D9BD", "#F0775A", False), band=("#0F4C6B", CHALK), motif="waves",
      hero=["Salt-wash tee", "Swim-run short"], idea="Water at peace. Teal and sand with a coral seam, calm rows of waves on the back."),
 dict(n="The Caves", code="CAV", place="Niah Caves, Niah National Park, Sarawak", lat=3.8139, lon=113.7814, alt="inside limestone, almost no light",
      cond=("24°C", "95% RH", "no light"), words="Mysterious, dark, unique, unpredictable, brown, green, unknown, stalactite, stalagmite",
      pal=[("Guano", "#4A3A2A"), ("Batu kapur", "#B9B0A0"), ("Lumut gua", "#4F6A4A"), ("Gelap", "#141414"), ("Walit", "#C9A24A")],
      tee=("#4A3A2A", "#4F6A4A", "#C9A24A", False), band=("#191613", CHALK), motif="cave",
      hero=["Reflective night tee", "Headlamp cap"], idea="The night-run collection. Brown and cave green, with reflective dots that hang and rise like stalactites and stalagmites."),
 dict(n="The Dune", code="DUN", place="Klebang dunes, Melaka", lat=2.2164, lon=102.1943, alt="sea level, open sand",
      cond=("34°C", "55% RH", "13:00"), words="Warm, hot, dry, sandy",
      pal=[("Pasir", "#D9B98A"), ("Kering", "#B58B5A"), ("Silau", "#F3EBDD"), ("Bayang", "#6B4E33"), ("Bahang", "#D9532B")],
      tee=("#D9B98A", "#F3EBDD", "#D9532B", True), band=("#EBDCC2", INK), motif="dune",
      hero=["Sun-cape cap", "Loose UV long sleeve"], idea="Heat and glare. Sand tones that hide sweat marks, loose cuts, ripple lines on the back."),
 dict(n="The Monsoon", code="MSN", place="Cherating, Pahang (suggested), November to March", lat=4.1300, lon=103.3900, alt="sea level, east coast",
      cond=("25°C", "90% RH", "NE wind"), words="Dark, waves, wild ocean, chaotic",
      pal=[("Ribut", "#2B3440"), ("Hujan", "#6E7B85"), ("Ombak", "#1B4A5A"), ("Buih", "#DDE3E4"), ("Bendera merah", "#E0342B")],
      tee=("#2B3440", "#6E7B85", "#E0342B", False), band=("#1D242D", CHALK), motif="rain",
      hero=["Rain shell", "Drain-hem short"], idea="The Ocean's dark twin: the same sea in the other season. Storm grey with one red-flag seam, rain coming in sideways."),
]

def dots(kind, col):
    random.seed(7); o = []
    def d(x, y, r, hollow=False):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" ' + (f'fill="none" stroke="{col}" stroke-width="1.2"/>' if hollow else f'fill="{col}"/>'))
    cx, cy = 400, 368
    if kind == "moss":
        for i in range(150):
            a = random.uniform(0, 6.283); rr = random.gauss(0, 1) * 34
            d(cx + math.cos(a) * rr * 1.5 + random.uniform(-8, 8), cy + math.sin(a) * rr, random.choice((1.4, 2, 2.6, 3.4, 4.4)), random.random() < .15)
    elif kind == "river":
        for k in range(3):
            for i in range(34):
                t = i / 33; y = 290 + t * 160
                d(cx + math.sin(t * 6.2 + k * .25) * (46 - k * 4) + (k - 1) * 13, y, 3.6 - k * .9 - (0 if i % 5 else -.6))
    elif kind == "sky":
        for k, (n, r, R) in enumerate(((14, 4.6, 34), (22, 3.2, 54), (30, 2.0, 74))):
            for i in range(n):
                a = 6.283 * i / n; d(cx + math.cos(a) * R, cy + math.sin(a) * R, r, (i + k) % 4 == 0)
        d(cx + 96, cy - 70, 4.6)
    elif kind == "waves":
        for row in range(6):
            for i in range(26):
                x = 300 + i * 8; d(x, 310 + row * 22 + math.sin(i * .55 + row * .9) * 6, 3.4 - row * .35)
    elif kind == "cave":
        for i in range(15):
            x = 302 + i * 14; L = random.randint(2, 7)
            for j in range(L): d(x, 292 + j * 11, 3.6 - j * .38)
            Lb = random.randint(1, 5)
            for j in range(Lb): d(x, 452 - j * 11, 3.6 - j * .5)
    elif kind == "dune":
        for row in range(7):
            for i in range(30):
                x = 296 + i * 7.2; d(x, 300 + row * 21 + math.sin(i * .22 + row * .5) * 13, 2.8 if (i + row) % 3 else 1.6)
    elif kind == "rain":
        for s in range(26):
            x0 = random.uniform(292, 520); y0 = random.uniform(286, 430); L = random.randint(3, 7)
            for j in range(L): d(x0 - j * 6.5, y0 + j * 9.5, 3.4 - j * .4)
    return "".join(o)

def seam(d_, c, w=4.2):
    return (f'<path d="{d_}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{d_}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="{w}" stroke-dasharray="1.2 3.2"/>')

def tee(c, i, back):
    body, panel, sm, light = c["tee"]; ink = INK if light else CHALK
    L = "M338,170 C292,200 244,262 224,338"; R_ = "M462,170 C508,200 556,262 576,338"
    sL = "M224,338 C250,440 236,560 252,646"; sR = "M576,338 C550,440 564,560 548,646"
    pl = f'<path d="M276,226 C250,262 232,300 224,338 L216,340 L152,392 L98,340 C150,300 220,250 276,226Z" fill="{panel}"/>'
    pr = f'<path d="M524,226 C550,262 568,300 576,338 L584,340 L648,392 L702,340 C650,300 580,250 524,226Z" fill="{panel}"/>'
    fc = "#000" if light else "#fff"
    f = (fold("M300,330 C320,430 290,560 310,720", fc, .06) + fold("M510,330 C490,440 520,580 500,720", fc, .05)
         + fold("M400,240 C380,400 420,560 400,720", "#000", .16 if light else .28, 60))
    if back:
        neck = '<path d="M318,150 C360,170 440,170 482,150 L474,140 C440,156 360,156 326,140 Z" fill="#000" opacity=".18"/>'
        g = (f'<g transform="translate(400,368) scale(1.22) translate(-400,-368)">{dots(c["motif"], ink)}</g>' + seam("M372,160 V214", sm) + seam("M428,160 V214", sm)
             + mono(c["n"].upper(), 400, 500, 10.5, sm if not light else INK, "middle", .2, 600)
             + mono(f'{c["lat"]:.4f}°N {c["lon"]:.4f}°E', 400, 516, 9, ink, "middle", .1))
    else:
        neck = ('<path d="M318,150 C350,196 450,196 482,150 L470,143 C444,180 356,180 330,143 Z" fill="#000" opacity=".16"/>'
                '<path d="M330,143 C356,158 444,158 470,143 C444,180 356,180 330,143Z" fill="#000" opacity=".5"/>')
        g = (f'<svg x="452" y="296" width="92" height="{92/OFNW*100:.1f}" viewBox="0 0 {OFNW} 100" style="color:{ink}"><use href="#ofn"/></svg>'
             + mono(f'OFN—{c["code"]}—001', 452, 334, 8.5, ink, sp=.12))
    x = (pl + pr + neck + seam(L, sm) + seam(R_, sm) + seam(sL, sm) + seam(sR, sm) + seam("M252,646 H548", sm)
         + seam("M276,226 C220,250 150,300 98,340", sm, 3) + seam("M524,226 C580,250 650,300 702,340", sm, 3)
         + f'<circle cx="252" cy="646" r="4" fill="{CHALK}"/><circle cx="548" cy="646" r="4" fill="{CHALK}"/>' + stitch("M222,694 H578", fc, .2) + g)
    return tile(cloth(TEEB if back else TEE, body, not light, f, f"t{i}{'b' if back else 'f'}", x), "#E9EBE8", label=f'{c["n"]} tee, {"back" if back else "front"}')

wm, WMW = word2("OFFNORM"); ofn, OFNW = word2("OFN")
DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<symbol id="wm" viewBox="0 0 {WMW} 100">{wm}</symbol><symbol id="ofn" viewBox="0 0 {OFNW} 100">{ofn}</symbol>
<radialGradient id="vig" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="13"/></filter>
<filter id="grainL" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  .2 0 0 0 -.07" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
<filter id="grainD" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  .3 0 0 0 -.1" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
</defs></svg>'''

# coordinate chart: longitude 99..119.5 E, latitude 1..7 N, points only (no coastline drawn)
def X(lon): return 60 + (lon - 99) / 20.5 * 900
def Y(lat): return 300 - (lat - 1) / 6.2 * 260
grid = "".join(f'<path d="M{X(l):.0f},30 V306" stroke="currentColor" stroke-opacity=".18"/><text class="mn" x="{X(l):.0f}" y="326" font-size="11" text-anchor="middle" fill="currentColor" opacity=".7">{l}°E</text>' for l in range(100, 120, 2))
grid += "".join(f'<path d="M56,{Y(l):.0f} H964" stroke="currentColor" stroke-opacity=".18"/><text class="mn" x="46" y="{Y(l)+4:.0f}" font-size="11" text-anchor="end" fill="currentColor" opacity=".7">{l}°N</text>' for l in range(1, 8))
LAB = {"MOS": (-12, -12, "end"), "WLD": (12, -12, "start"), "SKY": (-12, 18, "end"), "OCN": (12, -10, "start"), "CAV": (-12, -12, "end"), "DUN": (12, 18, "start"), "MSN": (14, 16, "start")}
pts = "".join(f'<circle cx="{X(c["lon"]):.1f}" cy="{Y(c["lat"]):.1f}" r="9" fill="{c["pal"][0][1]}" stroke="currentColor" stroke-width="2"/>'
              f'<text class="hx" x="{X(c["lon"])+LAB[c["code"]][0]:.1f}" y="{Y(c["lat"])+LAB[c["code"]][1]:.1f}" font-size="15" text-anchor="{LAB[c["code"]][2]}" fill="currentColor">{c["n"].upper()}</text>' for c in C)
kl = f'<path d="M{X(101.69)-6:.1f},{Y(3.14):.1f}h12m-6,-6v12" stroke="currentColor" stroke-width="2"/><text class="mn" x="{X(101.69)+10:.1f}" y="{Y(3.14)+22:.1f}" font-size="11" fill="currentColor" opacity=".8">KL 3.14°N</text>'
chart = f'<svg viewBox="0 0 1000 340" class="chart" role="img" aria-label="The seven coordinates plotted by latitude and longitude">{grid}{kl}{pts}</svg>'

def band(c, i):
    bg, fg = c["band"]
    sw = "".join(f'<div style="background:{h};color:{"#151617" if sum(int(h[j:j+2],16) for j in (1,3,5))>380 else "#F3F4F2"}"><b>{n}</b>{h.upper()}</div>' for n, h in c["pal"])
    core = ["Panel tee", "Singlet", "5-inch short", "Cap", "Crew sock"]
    pcs = "".join(f"<li>{p}</li>" for p in core) + "".join(f'<li class="hero">{p}</li>' for p in c["hero"])
    return f'''<section class="band col-band" style="background:{bg};color:{fg};--cbg:{bg};--cfg:{fg}"><div class="in">
  <div class="chead"><div class="eyebrow"><span>Collection {i+1} of 7</span><span>OFN—{c["code"]}</span></div>
    <h2 class="cname">{c["n"]}</h2>
    <div class="coord">{c["lat"]:.4f}°N&nbsp;&nbsp;{c["lon"]:.4f}°E</div>
    <div class="place">{c["place"]} · {c["alt"]}</div></div>
  <div class="cgrid">
    <div class="cinfo">
      <p class="words">{c["words"]}.</p>
      <p>{c["idea"]}</p>
      <div class="condlabel"><b>Conditions</b><span>{c["cond"][0]}</span><span>{c["cond"][1]}</span><span>{c["cond"][2]}</span><i>estimate, to be logged on site</i></div>
      <div class="sw5">{sw}</div>
      <ul class="pcs">{pcs}</ul>
    </div>
    <figure class="mock">{tee(c, i, False)}<figcaption><b>Front</b><span>Small mark, product number, contrast seams</span></figcaption></figure>
    <figure class="mock">{tee(c, i, True)}<figcaption><b>Back</b><span>The place drawn in dots, with its coordinate</span></figcaption></figure>
  </div>
</div></section>'''

head = open(os.path.join(OUT, "..", "identity", "source", "page.html")).read()
head = head[head.index("<meta"):head.index("</style>")]
PAGE = open(f"{HERE}/page.html").read()
matrix = "".join(f'<tr><th>{c["n"]}</th><td>OFN—{c["code"]}</td><td>{c["lat"]:.4f}°N, {c["lon"]:.4f}°E</td><td>{" / ".join(c["cond"])}</td><td>{", ".join(c["hero"])}</td></tr>' for c in C)
html = (PAGE.replace("{{HEAD}}", head).replace("{{DEFS}}", DEFS).replace("{{CHART}}", chart)
        .replace("{{HERO}}", f'<svg class="mk hero-mark" viewBox="0 0 {WMW} 100" style="color:#F3F4F2"><use href="#wm"/></svg>')
        .replace("{{BANDS}}", "".join(band(c, i) for i, c in enumerate(C))).replace("{{MATRIX}}", matrix))
open(f"{OUT}/lineup.html", "w").write(html)
print("ok")
