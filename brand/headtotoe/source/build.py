"""OFFNORM head-to-toe kit, one colourway at a time. Draft 1: Kopi O.
Run from the repo root:  python3 brand/headtotoe/source/build.py"""
import os, sys, io, re, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
GS = os.path.join(ROOT, "brand", "garments", "source"); sys.path.insert(0, GS)
spec = importlib.util.spec_from_file_location("gbuild", os.path.join(GS, "build.py")); G = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(G)
tile, cloth, fold, stitch, seam, bartack, logo, rdot = G.tile, G.cloth, G.fold, G.stitch, G.seam, G.bartack, G.logo, G.rdot
INK = G.INK; BG = "#F1F2F0"

def shade(h, f):   # f<1 darker, f>1 lighter (toward white)
    c = [int(h[i:i+2], 16) for i in (1, 3, 5)]
    c = [round(v * f) if f < 1 else round(v + (255 - v) * (f - 1)) for v in c]
    return "#" + "".join(f"{max(0, min(255, v)):02X}" for v in c)
def tone(h):       # tonal logo: same colour, a step darker (or lighter on very dark cloth)
    return shade(h, 1.28) if G.lum(h) < 0.2 else shade(h, 0.72)

TINTS = {}
def tid(h):
    k = "t_" + h[1:].lower(); TINTS[k] = h; return k

# ---------- the OFN mark: the symbol over F and NM (as in the founder's 6.svg)
WF_RATIO = G.AR["f"]; WN_RATIO = G.AR["nm"]
def ofn(cx, y, w, t, vertical=False):
    """Stacked OFN mark centred on cx. vertical=True stacks O, F, N down a leg."""
    sh_ = w / G.AR["sym"]
    if not vertical:
        h2 = w * 0.36; wf, wn = h2 * WF_RATIO, h2 * WN_RATIO; gap = w * 0.06; row = wf + gap + wn
        return (logo("sym", cx - w / 2, y, w, t) + logo("f", cx - row / 2, y + sh_ + w * 0.08, wf, t)
                + logo("nm", cx - row / 2 + wf + gap, y + sh_ + w * 0.08, wn, t))
    h2 = w * 0.62; wf, wn = h2 * WF_RATIO, h2 * WN_RATIO
    y2 = y + sh_ + w * 0.18; y3 = y2 + h2 + w * 0.18
    return logo("sym", cx - w / 2, y, w, t) + logo("f", cx - wf / 2, y2, wf, t) + logo("nm", cx - wn / 2, y3, wn, t)

# ---------- pieces
def beanie(k):
    c = k["beanie"]; i = k["code"]; t = tid(tone(c))
    crown = "M232,500 C226,300 300,176 400,176 C500,176 574,300 568,500 Z"
    cuff = "M214,486 H586 Q594,486 594,494 V624 Q594,634 584,634 H216 Q206,634 206,624 V494 Q206,486 214,486 Z"
    ribs = "".join(f'<path d="M{238+j*16},{200 if 300<238+j*16<500 else 260} L{236+j*16},500" stroke="#000" stroke-opacity=".10" stroke-width="5"/>' for j in range(21))
    gather = "".join(f'<path d="M400,182 L{400+dx},{248}" stroke="#000" stroke-opacity=".12" stroke-width="2"/>' for dx in (-60, -30, 0, 30, 60))
    cribs = "".join(f'<path d="M{220+j*15.6},490 V630" stroke="#000" stroke-opacity=".09" stroke-width="5"/>' for j in range(24))
    fold_line = '<rect x="206" y="486" width="388" height="10" fill="#000" opacity=".10"/>'
    mark = ofn(400, 510, 74, t)
    return tile(cloth(crown, c, G.dk(c), fold("M310,240 C290,330 286,420 290,500", "#000", .06, 40), "bnc" + i, ribs + gather)
                + cloth(cuff, c, G.dk(c), "", "bnf" + i, cribs + fold_line + mark), BG, label=f'{k["n"]} beanie')

def tee(k, back):
    body, panel, thread, logo_c, text_c = k["tee"]
    G.SKY.update(body=body, panel=panel, thread=thread)
    s = G.final(back)
    s = s.replace('filter="url(#t_ink)"', f'filter="url(#{tid(logo_c)})"')
    if back:
        s = (s.replace("OFN—SKY—001", f"OFN—{k['code']}—001").replace("THE SKY", k["n"].upper())
              .replace("30°C / 70% RH", k["cond"][0]).replace(">07:10<", f">{k['cond'][1]}<").replace("3.2094°N  101.1865°E", k["co"])
              .replace(f'fill="{INK}"', f'fill="{text_c}"').replace(f'stroke="{INK}"', f'stroke="{text_c}"'))
    return s.replace(f'aria-label=""', f'aria-label="{k["n"]} tee {"back" if back else "front"}"')

def arm_sleeve(k):
    c = k["sleeve"]; i = k["code"]; t = tid(tone(c))
    sh_ = "M318,96 C350,90 450,90 482,96 L462,700 C444,706 356,706 338,700 Z"
    top = '<path d="M318,96 C350,90 450,90 482,96 L480,150 C448,144 352,144 320,150 Z" fill="#000" opacity=".10"/>'
    bot = '<path d="M340,650 C360,656 440,656 460,650 L462,700 C444,706 356,706 338,700 Z" fill="#000" opacity=".10"/>'
    grip = stitch("M330,128 C360,122 440,122 470,128", "#fff" if G.dk(c) else "#000", .35, 1.3)
    ribs = "".join(f'<path d="M{330+j*9},150 L{346+j*7.4},650" stroke="#000" stroke-opacity=".05" stroke-width="3"/>' for j in range(17))
    mark = logo("sym", 372, 588, 56, t)
    return tile(cloth(sh_, c, G.dk(c), fold("M372,160 C366,360 376,520 370,690", "#fff", .06, 30), "asl" + i, ribs + top + bot + grip + mark),
                BG, label=f'{k["n"]} arm sleeve')

def shorts(k):
    body, panel, th, logo_c = k["short"]; i = k["code"]
    short = "M250,170 L550,170 L574,420 Q575,430 565,431 L420,436 Q411,436 410,427 L400,330 L390,427 Q389,436 380,436 L235,431 Q225,430 226,420 Z"
    ss = "#fff" if G.dk(body) else "#000"
    inner = (f'<path d="M250,170 L304,170 L276,433 L235,431 Q225,430 226,420 Z" fill="{panel}"/>'      # wearer's right side panel, like the tee
             + '<path d="M250,170 L550,170 L554,212 L246,212 Z" fill="#000" opacity=".16"/>'
             + "".join(f'<path d="M{262+j*13},174 l-1,34" stroke="{ss}" stroke-opacity=".14" stroke-width="1.6"/>' for j in range(22))
             + seam("M304,212 L276,433", th, 3.4) + bartack(303, 216, th, -83)
             + f'<path d="M386,192 C382,250 372,290 364,318 M414,192 C418,250 428,290 436,318" stroke="{th}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
             + stitch("M232,414 L384,424", ss, .3, 1.3) + stitch("M416,424 L568,414", ss, .3, 1.3)
             + f'<path d="M562,372 L574,420" stroke="{ss}" stroke-opacity=".4" stroke-width="2.4"/>' + rdot(562, 372, 3.2)
             + logo("sym", 478, 352, 54, tid(logo_c)))
    fs = (fold("M300,240 C290,320 300,380 290,430", "#000", .05, 40) + fold("M500,240 C510,320 500,380 510,430", "#000", .05, 40)
          + fold("M400,230 L400,330", "#000", .14, 30))
    return tile('<g transform="translate(-200,-54) scale(1.5)">' + cloth(short, body, G.dk(body), fs, "sho" + i, inner) + '</g>', BG, label=f'{k["n"]} shorts')

def tights(k):
    """Short tights after the founder's UVU references: fitted, mid-thigh, ribbed, wide waistband, drawcord,
    raw-cut hem, curved inner-thigh panel seams. One colour; the OFN mark runs big and vertical on one thigh."""
    c = k["tights"]; i = k["code"]; ref = k["tights_logo"]
    body = ("M228,190 L572,190 C590,240 598,300 590,360 L572,560 Q571,570 561,570 L428,566 Q418,566 417,556 L404,352 "
            "Q400,340 396,352 L383,556 Q382,566 372,566 L239,570 Q229,570 228,560 L210,360 C202,300 210,240 228,190 Z")
    band = "M222,112 H578 L574,196 C520,190 280,190 226,196 Z"
    hs = "#fff" if G.dk(c) else "#000"
    ribs = "".join(f'<path d="M{204+j*10.6},196 L{206+j*10.4},572" stroke="{hs}" stroke-opacity=".07" stroke-width="2.2"/>' for j in range(38))
    pseam = lambda d_: f'<path d="{d_}" fill="none" stroke="#000" stroke-opacity=".20" stroke-width="2.2"/>' + stitch(d_, hs, .22, 1.1)
    inner = (ribs + pseam("M396,352 C356,420 344,490 350,566") + pseam("M404,352 C444,420 456,490 450,566")
             + pseam("M400,200 L400,344")
             + '<path d="M232,560 L380,556 L380,566 L238,570 Z" fill="#000" opacity=".10"/><path d="M420,556 L568,560 L562,570 L420,566 Z" fill="#000" opacity=".10"/>'
             + ofn(522, 330, 74, tid(ref), vertical=True))
    b_in = ('<rect x="200" y="100" width="400" height="110" fill="#000" opacity=".22"/>'
            + "".join(f'<path d="M{232+j*13},118 V188" stroke="{hs}" stroke-opacity=".10" stroke-width="2"/>' for j in range(27))
            + f'<g opacity=".55">{logo("wm", 330, 146, 140, tid(tone(c)))}</g>')
    cord = (f'<path d="M392,190 C380,236 362,262 374,304 C382,330 404,344 422,352 M408,190 C428,232 418,256 398,290 C388,310 390,330 398,342"'
            f' stroke="{shade(c, .82) if G.lum(c) > .2 else shade(c, 1.35)}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    folds = fold("M290,230 C284,360 296,460 300,560", "#fff", .06, 34) + fold("M520,230 C528,330 512,460 508,560", "#fff", .05, 30) + fold("M400,210 L400,340", "#000", .12, 24)
    return tile('<g transform="translate(0,60)">' + cloth(body, c, G.dk(c), folds, "tgs" + i, inner) + cloth(band, c, G.dk(c), "", "tgb" + i, b_in) + cord + '</g>',
                BG, label=f'{k["n"]} short tights')

def socks(k):
    c = k["socks"]; i = k["code"]; tc = tone(c); t = tid(tc)
    K = "M0,0 H120 V420 C120,456 138,470 188,486 C258,508 272,572 218,586 C158,602 58,578 22,532 C-4,498 0,460 0,420 Z"
    def one(tx, ty, rot, cid):
        ribs = "".join(f'<path d="M{8+j*9.6},0 V62" stroke="#000" stroke-opacity=".12" stroke-width="2"/>' for j in range(12))
        inner = (ribs + '<rect x="0" y="62" width="120" height="6" fill="#000" opacity=".08"/>'
                 + '<path d="M0,420 C0,460 -4,498 22,532 L62,498 C44,470 56,440 120,420Z" fill="#000" opacity=".07"/>'
                 + '<path d="M188,486 C258,508 272,572 218,586 C204,552 194,520 188,486Z" fill="#000" opacity=".07"/>'
                 + G.vlogo(46, 392, 290, t)
                 + f'<text class="mn" x="60" y="92" font-size="7" fill="{tc}" text-anchor="middle" letter-spacing=".12em">OFN—{i}</text>')
        return f'<g transform="translate({tx},{ty}) rotate({rot})">' + cloth(K, c, G.dk(c), fold("M90,100 V400", "#000", .06, 26), cid, inner) + '</g>'
    return tile(one(190, 96, -4, "sk1" + i) + one(440, 110, 4, "sk2" + i), BG, label=f'{k["n"]} long socks')

def strip(svg):    # tile -> bare inner, for the flat lay
    inner = re.sub(r'^<svg[^>]*>', '', svg); inner = inner[:inner.rfind('</svg>')]
    return re.sub(r'^<rect[^>]*/><rect[^>]*/>', '', inner)
def flatlay(k, parts):
    def place(svg, x, y, s, suf): 
        body = strip(svg)
        body = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}{suf}"', body).replace('url(#', 'url(#').replace('clip-path="url(#', f'clip-path="url(#')
        body = re.sub(r'clip-path="url\(#([^)]+)\)"', lambda m: f'clip-path="url(#{m.group(1)}{suf})"', body)
        return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 800 800">{body}</svg>'
    g = (place(parts["beanie"], 330, 0, 340, "_a") + place(parts["tee"], 150, 210, 700, "_b") + place(parts["sleeve"], 700, 230, 480, "_c")
         + place(parts["tights"], 230, 800, 640, "_e") + place(parts["socks"], 290, 1340, 520, "_f"))
    return f'<svg viewBox="0 0 1100 1820" role="img" aria-label="{k["n"]} head-to-toe flat lay"><rect width="1100" height="1820" fill="{BG}"/>{g}</svg>'

# ---------- colourways. pal roles: Main, Sub, Pop, Deep, Light
def K(code, n, line, co, cond, pal, beanie, tee, sleeve, short, tights, socks, notes):
    return dict(code=code, n=n, line=line, co=co, cond=cond, pal=pal, beanie=beanie, tee=tee, sleeve=sleeve,
                short=short, tights=tights, tights_logo="#B9BEC4", socks=socks, notes=notes)
KITS = [
 K("KPO", "Kopi O", "Black coffee with a gold edge. For the 5am run.", "3.1390°N  101.6869°E", ("26°C / 88% RH", "05:00"),
   [("Kopi", "#2B1D16", "Main"), ("Kacang", "#C9A27A", "Sub"), ("Gula", "#E8B04A", "Pop"), ("Pekat", "#120C09", "Deep"), ("Cawan", "#EDE3D5", "Light")],
   "#E8B04A", ("#2B1D16", "#C9A27A", "#E8B04A", "#EDE3D5", "#EDE3D5"), "#C9A27A", ("#120C09", "#EDE3D5", "#E8B04A", "#C9A27A"), "#2B1D16", "#E8B04A",
   ["Gold at both ends: beanie and socks share the pop.", "Dark through the middle, tee and tights, like black coffee.", "Kacang sleeve carries the tee's right-arm panel down to the wrist."]),
 K("MSN", "The Monsoon", "Storm grey with one red-flag seam. Cherating, November to March.", "4.1300°N  103.3900°E", ("25°C / 90% RH", "NE WIND"),
   [("Ribut", "#2B3440", "Main"), ("Hujan", "#6E7B85", "Sub"), ("Bendera merah", "#E0342B", "Pop"), ("Ombak", "#1B4A5A", "Deep"), ("Buih", "#DDE3E4", "Light")],
   "#E0342B", ("#2B3440", "#6E7B85", "#E0342B", "#DDE3E4", "#DDE3E4"), "#6E7B85", ("#1B4A5A", "#DDE3E4", "#E0342B", "#6E7B85"), "#2B3440", "#E0342B",
   ["Red flag at both ends: the beach warning flag on the beanie and socks.", "Storm grey tee with Hujan rain-grey on the right arm and sleeve.", "Red seams stay thin, like the flag seen from far away."]),
 K("SGK", "Songket", "Plum and woven gold. The dressy one.", "5.3302°N  103.1408°E", ("28°C / 82% RH", "18:30"),
   [("Ungu", "#3A1430", "Main"), ("Sutera", "#F4E9D0", "Sub"), ("Benang emas", "#D4AF37", "Pop"), ("Gelap", "#1C0A18", "Deep"), ("Pucat", "#FAF4E6", "Light")],
   "#D4AF37", ("#3A1430", "#F4E9D0", "#D4AF37", "#D4AF37", "#F4E9D0"), "#F4E9D0", ("#1C0A18", "#3A1430", "#D4AF37", "#F4E9D0"), "#1C0A18", "#D4AF37",
   ["Gold thread is the point: gold seams and a gold chest symbol, like songket weft.", "Silk-cream sleeve panel and arm sleeve.", "Gold beanie and socks frame the plum."]),
 K("PBK", "Paya Bakau", "Mangrove mud, root brown and brackish green.", "3.3460°N  101.2520°E", ("30°C / 85% RH", "07:00"),
   [("Lumpur", "#55503F", "Main"), ("Air", "#C8CDB4", "Sub"), ("Akar", "#B5763A", "Pop"), ("Paya", "#2C2A20", "Deep"), ("Kabut", "#F2F2EA", "Light")],
   "#B5763A", ("#55503F", "#C8CDB4", "#B5763A", "#F2F2EA", "#F2F2EA"), "#C8CDB4", ("#2C2A20", "#F2F2EA", "#B5763A", "#C8CDB4"), "#55503F", "#B5763A",
   ["Root-brown pop on the beanie and socks.", "Mud tee with a brackish-water sleeve panel and matching arm sleeve.", "The quietest kit of the six; the pop is earthy, not loud."]),
 K("KNB", "Kinabalu", "Granite slate and alpine mint.", "6.0750°N  116.5583°E", ("8°C / 85% RH", "02:30"),
   [("Granit", "#3F5560", "Main"), ("Kabus", "#E5E9EA", "Sub"), ("Pucuk", "#9BC2A6", "Pop"), ("Puncak", "#1E2C33", "Deep"), ("Salji", "#F6F8F8", "Light")],
   "#9BC2A6", ("#3F5560", "#E5E9EA", "#9BC2A6", "#F6F8F8", "#F6F8F8"), "#E5E9EA", ("#1E2C33", "#F6F8F8", "#9BC2A6", "#E5E9EA"), "#3F5560", "#9BC2A6",
   ["Mint shoots at both ends.", "Granite tee with a mist-white right arm; the arm sleeve stays mist.", "Printed time is 02:30, when summit climbs start."]),
 K("SBH", "Subuh", "Navy before dawn, the first pink and orange at the edge.", "3.1390°N  101.6869°E", ("24°C / 92% RH", "05:45"),
   [("Fajar", "#2D3A6B", "Main"), ("Merah muda", "#F0C9A8", "Sub"), ("Matahari", "#E57A44", "Pop"), ("Malam", "#161E3D", "Deep"), ("Cahaya", "#FBF1E8", "Light")],
   "#E57A44", ("#2D3A6B", "#F0C9A8", "#E57A44", "#FBF1E8", "#FBF1E8"), "#F0C9A8", ("#161E3D", "#FBF1E8", "#E57A44", "#F0C9A8"), "#2D3A6B", "#E57A44",
   ["Sunrise orange at both ends.", "Navy tee with the first pink light on the right arm and sleeve.", "Reads well in low light: the orange and the reflective tights do the work."]),
]

def build(k):
    parts = dict(beanie=beanie(k), tee=tee(k, False), teeb=tee(k, True), sleeve=arm_sleeve(k), tights=tights(k), socks=socks(k))
    for key in ("tee", "teeb"):
        parts[key] = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}{k["code"]}"', parts[key])
        parts[key] = re.sub(r'clip-path="url\(#([^)]+)\)"', lambda m: f'clip-path="url(#{m.group(1)}{k["code"]})"', parts[key])
    nm_of = {h: nm for nm, h, _ in k["pal"]}
    def chips(*hs): return "".join(f'<span class="chip"><i style="background:{h}"></i>{nm_of.get(h, "Reflective")}</span>' for h in dict.fromkeys(hs))
    T = k["tee"]; S = k["short"]
    tiles = [("Beanie", parts["beanie"], chips(k["beanie"])), ("Tee front", parts["tee"], chips(*T[:4])), ("Tee back", parts["teeb"], chips(T[0], T[4])),
             ("Arm sleeve", parts["sleeve"], chips(k["sleeve"])),
             ("Short tights", parts["tights"], chips(k["tights"], k["tights_logo"])), ("Long socks", parts["socks"], chips(k["socks"]))]
    grid = "".join(f'<figure class="pt">{svg}<figcaption><b>{n}</b><span class="chips">{ch}</span></figcaption></figure>' for n, svg, ch in tiles)
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#F3F4F2" if G.dk(h) else INK}"><b>{nm}</b><span>{h}</span><i>{role}</i></div>' for nm, h, role in k["pal"])
    notes = "".join(f"<li>{x}</li>" for x in k["notes"])
    return (f'<section class="kit" id="{k["code"].lower()}"><header class="kh"><div><div class="eyebrow">OFN—{k["code"]}</div><h2>{k["n"]}</h2><p class="lede">{k["line"]}</p></div></header>'
            f'<div class="pal">{sw}</div><div class="lay"><figure>{flatlay(k, parts)}</figure><ul class="notes">{notes}</ul></div><div class="pgrid">{grid}</div></section>')

defs_extra = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{}</defs></svg>'
body = "".join(build(k) for k in KITS)
nav = "".join(f'<a class="nv" href="#{k["code"].lower()}"><span style="background:{k["pal"][0][1]}"></span><span style="background:{k["pal"][1][1]}"></span><span style="background:{k["pal"][2][1]}"></span>{k["n"]}</a>' for k in KITS)
tints = "".join(G.tint(i, h) for i, h in TINTS.items())
PAGE = open(f"{HERE}/page.html").read()
html = PAGE.replace("{{DEFS}}", G.DEFS + defs_extra.format(tints)).replace("{{NAV}}", nav).replace("{{KITS}}", body)
open(f"{OUT}/head-to-toe.html", "w").write(html)
print("ok", len(html))
