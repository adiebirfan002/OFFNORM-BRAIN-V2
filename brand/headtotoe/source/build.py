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
    c = k["tights"]; i = k["code"]; ref = k["tights_logo"]
    legL, legR = "M226,150 L398,162 L384,720 L268,720 Z", "M574,150 L402,162 L416,720 L532,720 Z"
    band = "M222,110 H578 L576,160 C520,154 280,154 224,160 Z"
    hs = "#fff" if G.dk(c) else "#000"
    L_in = '<rect x="258" y="694" width="140" height="26" fill="#000" opacity=".16"/>' + stitch("M268,697 H384", hs, .35, 1.2)
    R_in = ('<rect x="402" y="694" width="140" height="26" fill="#000" opacity=".16"/>' + stitch("M416,697 H532", hs, .35, 1.2)
            + "".join(f'<path d="M{410+j*8},170 L{420+j*8.6},690" stroke="#000" stroke-opacity=".05" stroke-width="3"/>' for j in range(15))
            + ofn(488, 230, 66, tid(ref), vertical=True))
    L_in += "".join(f'<path d="M{236+j*8},170 L{272+j*7.2},690" stroke="#000" stroke-opacity=".05" stroke-width="3"/>' for j in range(15))
    b_in = "".join(f'<path d="M{232+j*12},114 V156" stroke="{hs}" stroke-opacity=".12" stroke-width="2"/>' for j in range(29))
    return tile(cloth(legL, c, G.dk(c), fold("M300,200 C296,400 304,560 300,700", "#fff", .06, 30), "tgl" + i, L_in)
                + cloth(legR, c, G.dk(c), fold("M470,200 C474,400 466,560 470,700", "#fff", .06, 30), "tgr" + i, R_in)
                + cloth(band, c, G.dk(c), "", "tgb" + i, b_in), BG, label=f'{k["n"]} 3/4 tights')

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
         + place(parts["short"], 20, 840, 560, "_d") + place(parts["tights"], 520, 840, 560, "_e") + place(parts["socks"], 260, 1310, 520, "_f"))
    return f'<svg viewBox="0 0 1100 1820" role="img" aria-label="{k["n"]} head-to-toe flat lay"><rect width="1100" height="1820" fill="{BG}"/>{g}</svg>'

# ---------- colourways
KPO = dict(code="KPO", n="Kopi O", co="3.1390°N  101.6869°E", cond=("26°C / 88% RH", "05:00"),
    line="Black coffee with a gold edge. For the 5am run.",
    pal=[("Kopi", "#2B1D16", "Main"), ("Kacang", "#C9A27A", "Sub"), ("Gula", "#E8B04A", "Pop"), ("Pekat", "#120C09", "Deep"), ("Cawan", "#EDE3D5", "Light")],
    beanie="#E8B04A",
    tee=("#2B1D16", "#C9A27A", "#E8B04A", "#EDE3D5", "#EDE3D5"),     # body, right-sleeve panel, seams, logo, back text
    sleeve="#C9A27A",
    short=("#120C09", "#EDE3D5", "#E8B04A", "#C9A27A"),               # body, side panel, seams+cord, logo
    tights="#2B1D16", tights_logo="#B9BEC4",
    socks="#E8B04A")
KITS = [KPO]

def build(k):
    parts = dict(beanie=beanie(k), tee=tee(k, False), teeb=tee(k, True), sleeve=arm_sleeve(k), short=shorts(k), tights=tights(k), socks=socks(k))
    P = {nm: h for nm, h, _ in k["pal"]}
    nm_of = {h: nm for nm, h, _ in k["pal"]}
    def chips(*hs): return "".join(f'<span class="chip"><i style="background:{h}"></i>{nm_of.get(h, "Reflective")}</span>' for h in hs)
    rows = [
     ("Beanie", parts["beanie"], "One colour: the pop", chips(k["beanie"]),
      "Gula only. The OFN mark is embroidered tone on tone, a shade darker than the knit, so the beanie stays one colour."),
     ("Tee", parts["tee"] + parts["teeb"], "Main, sub and pop", chips(*k["tee"][:3], k["tee"][3]),
      "Kopi body, Kacang right-sleeve panel, Gula on the raglan seams and hem tab, Cawan for the chest symbol and the back print. The pop stays thin so it reads as an edge, like the gold rim on a kopi cup."),
     ("Arm sleeve", parts["sleeve"], "One colour", chips(k["sleeve"]),
      "Kacang, so the sleeve carries on the tee's right-arm panel down to the wrist. Tonal symbol at the wrist, silicone grip inside the top hem."),
     ("Shorts", parts["short"], "Same vibe, different mix", chips(*k["short"]),
      "Pekat body with a Cawan side panel on the wearer's right, the same side as the tee's panel. Gula seam and drawcord, Kacang symbol. No Kopi, so it doesn't copy the tee."),
     ("3/4 tights", parts["tights"], "One colour + vertical OFN", chips(k["tights"], k["tights_logo"]),
      "Kopi only, with the OFN mark stacked down the right outer thigh in reflective print, as you asked for earlier. The reflective silver is a finish, not a sixth colour."),
     ("Long socks", parts["socks"], "One colour, same as the beanie", chips(k["socks"]),
      "Gula, matching the beanie so the outfit is gold at both ends. OFFNORM wordmark knitted vertically, tone on tone."),
    ]
    cards = "".join(f'<article class="pc"><div class="pics {"two" if n=="Tee" else ""}">{svg}</div><div class="txt"><small>{n}</small><h3>{rule}</h3><div class="chips">{ch}</div><p>{why}</p></div></article>'
                    for n, svg, rule, ch, why in rows)
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#F3F4F2" if G.dk(h) else INK}"><b>{nm}</b><span>{h}</span><i>{role}</i></div>' for nm, h, role in k["pal"])
    return flatlay(k, parts), cards, sw

defs_extra = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{}</defs></svg>'
k = KPO
fl, cards, sw = build(k)
tints = "".join(G.tint(i, h) for i, h in TINTS.items())
PAGE = open(f"{HERE}/page.html").read()
html = (PAGE.replace("{{DEFS}}", G.DEFS + defs_extra.format(tints)).replace("{{NAME}}", k["n"]).replace("{{CODE}}", k["code"])
        .replace("{{LINE}}", k["line"]).replace("{{SW}}", sw).replace("{{FLAT}}", fl).replace("{{CARDS}}", cards))
open(f"{OUT}/kopi-o.html", "w").write(html)
print("ok", len(html))
