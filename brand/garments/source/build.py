"""OFFNORM garment designs, one piece at a time, each awaiting founder approval. Builds ../designs.html
Run from the repo root:  python3 brand/garments/source/build.py"""
import os, sys, base64, math
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(OUT, "..", "identity", "source"))
from mocks import tile, cloth, fold, stitch, mono, TEE, TEEB
INK, CHALK = "#151617", "#F3F4F2"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
P8, P9 = b64(f"{OUT}/logo/offnorm-logo-parts.png"), b64(f"{OUT}/logo/offnorm-logo-full.png")
# the founder's logo, cut from the supplied PNGs (bounding boxes measured from the pixels)
PARTS = {"sym": (P8, 956, 774, 300, 118, 339, 243), "f": (P8, 956, 774, 175, 416, 261, 224),
         "nm": (P8, 956, 774, 481, 416, 308, 224), "wm": (P9, 1112, 920, 179, 673, 781, 83)}
AR = {k: v[5] / v[6] for k, v in PARTS.items()}
syms = "".join(f'<symbol id="lg_{k}" viewBox="{x-3} {y-3} {w+6} {h+6}"><image href="data:image/png;base64,{d}" width="{W}" height="{H}"/></symbol>'
               for k, (d, W, H, x, y, w, h) in PARTS.items())
def tint(i, hexc):
    r, g, b = (int(hexc[j:j+2], 16) / 255 for j in (1, 3, 5))
    return f'<filter id="{i}" color-interpolation-filters="sRGB"><feColorMatrix values="0 0 0 0 {r:.3f}  0 0 0 0 {g:.3f}  0 0 0 0 {b:.3f}  1.55 0 0 0 -0.42"/></filter>'
DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{syms}
{tint("t_ink", INK)}{tint("t_white", "#FFFFFF")}{tint("t_yel", "#F4D24A")}{tint("t_blue", "#2E5C8A")}
<radialGradient id="vig" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".10"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="13"/></filter>
<filter id="grainL" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  .12 0 0 0 -.045" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
<filter id="grainD" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  .22 0 0 0 -.08" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
</defs></svg>'''
def logo(k, x, y, w, t="t_ink"):
    return f'<use href="#lg_{k}" x="{x}" y="{y}" width="{w}" height="{w/AR[k]:.1f}" filter="url(#{t})"/>'
def seam(d_, c, w=4.2):
    return (f'<path d="{d_}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{d_}" fill="none" stroke="#000" stroke-opacity=".22" stroke-width="{w}" stroke-dasharray="1.2 3.2"/>')
def rdot(x, y, r=4): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#000" stroke-opacity=".25" stroke-width=".8"/>'
def pin(n, x, y, tx, ty):
    return (f'<path d="M{x},{y} L{tx},{ty}" stroke="{INK}" stroke-width="1.2"/><circle cx="{x}" cy="{y}" r="3" fill="{INK}"/>'
            f'<circle cx="{tx}" cy="{ty}" r="14" fill="{INK}"/><text class="mn" x="{tx}" y="{ty+4.5}" font-size="13" font-weight="600" text-anchor="middle" fill="#fff">{n}</text>')

# ---------- Design 01, round 2: The Sky tee in three directions (round 1, "the slash", was rejected)
SKY = dict(body="#7FB2DD", panel="#F1F2EF", thread="#F4D24A", deep="#2E5C8A")
T2 = ("M324,148 C352,190 448,190 476,148 L612,186 C660,204 722,276 748,330 L672,410 L600,356 L600,700 Q600,712 588,712 "
      "L212,712 Q200,712 200,700 L200,356 L128,410 L52,330 C78,276 140,204 188,186 Z")
T2B = T2.replace("C352,190 448,190", "C362,166 438,166")
RL, RR = "M340,168 C300,198 232,272 204,352", "M460,168 C500,198 568,272 596,352"
# --- sleeve construction. The raglan seam is split at its midpoint J; the lower-sleeve panel is bounded by
#     the raglan seam from J to the underarm, the sleeve hem, and one panel seam that starts exactly at J.
JX, JY = 267.5, 241.25
PANEL_L = f"M{JX},{JY} C242,273.5 218,312 204,352 L200,356 L128,410 L82.4,362 C150,318 212,268 {JX},{JY} Z"
PSEAM_L = f"M{JX},{JY} C212,268 150,318 82.4,362"
def flip(d):
    import re
    nums = iter(re.findall(r"-?\d+\.?\d*", d)); res = ""; k = 0
    for m in re.finditer(r"[A-Za-z]|-?\d+\.?\d*", d):
        t_ = m.group(0)
        if t_.isalpha(): res += t_; k = 0
        else:
            v = round(800 - float(t_), 2) if k % 2 == 0 else float(t_)
            res += ("," if k % 2 else (" " if res and not res[-1].isalpha() else "")) + f"{v:g}"; k += 1
    return res
PANEL_R, PSEAM_R = flip(PANEL_L), flip(PSEAM_L)
def base(extra, back, cid, c=SKY, vb=None):
    f = (fold("M290,340 C310,440 280,560 300,720", "#000", .05) + fold("M520,340 C500,440 530,580 510,720", "#000", .05)
         + fold("M400,250 C380,400 420,560 400,720", "#000", .12, 64))
    neck = ('<path d="M324,148 C362,166 438,166 476,148 L468,138 C438,152 362,152 332,138 Z" fill="#000" opacity=".16"/>'
            + stitch("M330,152 C364,170 436,170 470,152", "#000", .28, 1.2) if back else
            '<path d="M324,148 C352,190 448,190 476,148 L464,141 C440,174 360,174 336,141 Z" fill="#000" opacity=".13"/>'
            '<path d="M336,141 C360,156 440,156 464,141 C440,174 360,174 336,141Z" fill="#000" opacity=".42"/>'
            + stitch("M320,154 C350,198 450,198 480,154", "#000", .28, 1.2))
    # construction every tee has: turned sleeve hems, body hem, side seams
    hems = (stitch("M138,400 L62,320", "#000", .3, 1.3) + stitch("M662,400 L738,320", "#000", .3, 1.3) + stitch("M206,690 H594", "#000", .3, 1.3)
            + '<path d="M200,356 V700 M600,356 V700" stroke="#000" stroke-opacity=".10" stroke-width="2" fill="none"/>')
    svg = tile(cloth(T2B if back else T2, c["body"], False, f, cid, extra[0] + neck + hems + extra[1]) + (extra[2] if len(extra) > 2 else ""), "#F1F2F0")
    return svg.replace('viewBox="0 0 800 800"', f'viewBox="{vb}"') if vb else svg
def bartack(x, y, c, rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot})"><rect x="-7" y="-2.6" width="14" height="5.2" rx="1" fill="{c}"/><rect x="-7" y="-2.6" width="14" height="5.2" rx="1" fill="none" stroke="#000" stroke-opacity=".3" stroke-width=".7"/></g>'
def sleeve(c, side, thread=None):
    """One lower-sleeve panel with its seams, joined to the raglan at J. side: 'L' or 'R' as drawn."""
    th = thread or c["thread"]; L = side == "L"
    pan = f'<path d="{PANEL_L if L else PANEL_R}" fill="{c["panel"]}"/>'
    jx = JX if L else 800 - JX; ux = 204 if L else 596
    seams = (seam(PSEAM_L if L else PSEAM_R, th, 3.4) + bartack(jx, JY, th, -50 if L else 50) + rdot(ux, 352, 3.6))
    return pan, seams
def raglans(c, tl=None, tr=None):
    return seam(RL, tl or c["thread"]) + seam(RR, tr or c["thread"])
def cap(t, x, y, anchor="start", fs=8.5): return mono(t, x, y, fs, INK, anchor, .1)
def spin(n, x, y, tx, ty, r=14, fs=13):
    return (f'<path d="M{x},{y} L{tx},{ty}" stroke="{INK}" stroke-width="{r/12:.1f}"/><circle cx="{x}" cy="{y}" r="{r/5:.1f}" fill="{INK}"/>'
            f'<circle cx="{tx}" cy="{ty}" r="{r}" fill="{INK}"/><text class="mn" x="{tx}" y="{ty+fs*.35:.1f}" font-size="{fs}" font-weight="600" text-anchor="middle" fill="#fff">{n}</text>')
TONAL = "#4F8DC2"
HEMBREAK = lambda c: (seam("M200,640 H392", c["thread"], 3) + seam("M408,628 H600", c["thread"], 3) + rdot(392, 640, 3.2) + rdot(408, 628, 3.2))

def dirA(back):
    """A2. Centre: plain body, both raglans in contrast thread, the O small in the middle of the chest."""
    c = SKY
    seams = raglans(c) + rdot(204, 352, 3.6) + rdot(596, 352, 3.6) + HEMBREAK(c)
    g = (logo("sym", 368, 296, 64) + cap("3.2094°N  101.1865°E", 400, 358, "middle", 7.5)) if not back else \
        (logo("wm", 322, 236, 156) + cap("OFN—SKY—001  /  30°C  70%  07:10", 400, 270, "middle", 7.5))
    return base(("", seams + g), back, "dA" + ("b" if back else "f"))

def dirB(back, vb=None, pins=""):
    """B2. Arm: nothing on the chest. The white lower-sleeve panel carries the O; every seam meets at a point."""
    c = SKY; side = "R" if back else "L"
    pan, ps = sleeve(c, side)
    rag = raglans(c, tr=TONAL) if not back else raglans(c, tl=TONAL)
    if not back:
        g = (f'<g transform="translate(160,338) rotate(-40)">{logo("sym", -27, -19, 54)}</g>' + cap("3.2094°N  101.1865°E", 216, 680, "start", 7.5)
             + f'<g transform="translate(566,648) rotate(-3)"><rect width="34" height="20" fill="{c["thread"]}"/></g>')
    else:
        g = (f'<g transform="translate(640,338) rotate(40)">{logo("sym", -27, -19, 54)}</g>'
             + logo("f", 222, 632, 40) + logo("nm", 532, 632, 48) + cap("30°C / 70% / 07:10", 400, 680, "middle", 7.5))
    return base((pan, rag + ps + g, pins), back, "dB" + ("b" if back else "f") + ("z" if vb else ""), vb=vb)

def dirAB(back):
    """AB. Both: the O in the middle of the chest, one white lower-sleeve panel carrying the coordinate."""
    c = SKY; side = "R" if back else "L"
    pan, ps = sleeve(c, side)
    seams = raglans(c) + ps + rdot(596 if not back else 204, 352, 3.6) + HEMBREAK(c)
    if not back:
        g = (logo("sym", 368, 296, 64) + cap("OFN—SKY—001", 400, 358, "middle", 7.5)
             + f'<text class="mn" transform="translate(132,352) rotate(-40)" font-size="7.5" fill="{INK}" letter-spacing=".1em">3.2094°N</text>'
             + f'<text class="mn" transform="translate(140,364) rotate(-40)" font-size="7.5" fill="{INK}" letter-spacing=".1em">101.1865°E</text>')
    else:
        g = (logo("wm", 322, 236, 156) + cap("30°C  /  70%  /  07:10", 400, 270, "middle", 7.5)
             + f'<text class="mn" transform="translate(634,322) rotate(40)" font-size="7.5" fill="{INK}" letter-spacing=".1em">THE SKY</text>')
    return base((pan, seams + g), back, "dAB" + ("b" if back else "f"))

def detail():
    pins = (spin(1, 300, 204, 330, 176, 9, 8.5) + spin(2, JX, JY, 318, 262, 9, 8.5) + spin(3, 176, 300, 150, 252, 9, 8.5)
            + spin(4, 204, 352, 262, 372, 9, 8.5) + spin(5, 100, 360, 78, 404, 9, 8.5) + spin(6, 180, 358, 208, 424, 9, 8.5))
    return dirB(False, vb="40 150 310 310", pins=pins)

# ---------- Design 01, round 4: the founder's brief. B2 with both white sleeve panels, the O centre front,
#            A2's wordmark and details on the back, and the data block rearranged.
def rule(d_, w=.8, o=1): return f'<path d="{d_}" stroke="{INK}" stroke-width="{w}" stroke-opacity="{o}" fill="none"/>'
def t(txt, x, y, fs=6, anchor="middle", o=1, w=500, sp=.08):
    return f'<text class="mn" x="{x}" y="{y}" font-size="{fs}" fill="{INK}" fill-opacity="{o}" text-anchor="{anchor}" font-weight="{w}" letter-spacing="{sp}em">{txt}</text>'
def block(kind):
    wm = logo("wm", 300, 226, 200)                      # wordmark spans x 300..500
    if kind == "D1":     # stack
        return (wm + rule("M300,260 H500") + t("OFN—SKY—001", 400, 273, 6.6, w=600) + t("3.2094°N  101.1865°E", 400, 284, 6.2)
                + t("30°C  /  70% RH  /  07:10", 400, 295, 6.2))
    if kind == "D2":     # spec strip: three labelled cells, the width of the wordmark
        cells = [(333, "NO.", ["OFN—SKY—001"]), (400, "COORDINATE", ["3.2094°N", "101.1865°E"]), (467, "CONDITIONS", ["30°C / 70% RH", "07:10"])]
        g = wm + rule("M300,258 H500") + rule("M300,296 H500") + rule("M366.5,262 V292", .6, .6) + rule("M433.5,262 V292", .6, .6)
        for x, lab, vals in cells:
            g += t(lab, x, 268, 4.2, o=.62, sp=.16)
            y0 = 281 if len(vals) == 1 else 277
            for i, v in enumerate(vals): g += t(v, x, y0 + i * 8.4, 5.9, w=600, sp=.04)
        return g
    # D3: split. number left, conditions right, coordinate centred below
    return (wm + t("OFN—SKY—001", 300, 266, 6.4, "start", w=600) + t("THE SKY", 300, 276, 5.6, "start", .7)
            + t("30°C / 70% RH", 500, 266, 6.4, "end", w=600) + t("07:10", 500, 276, 5.6, "end", .7)
            + rule("M300,284 H500", .6, .6) + t("3.2094°N  101.1865°E", 400, 295, 6.2))
def final(back, kind="D3", vb=None):
    c = SKY
    pl, sl = sleeve(c, "R" if back else "L"); pr, sr = "", ""      # wearer's right arm only (founder, round 5)
    seams = raglans(c) + sl + rdot(204 if back else 596, 352, 3.6)
    if not back:
        g = logo("sym", 368, 296, 64) + f'<g transform="translate(566,648) rotate(-3)"><rect width="34" height="20" fill="{c["thread"]}"/></g>'
    else:
        g = block(kind) + logo("f", 248, 632, 40) + logo("nm", 504, 632, 48)
    return base((pl + pr, seams + g), back, "fin" + ("b" if back else "f") + kind + ("z" if vb else ""), vb=vb)

# ---------- Designs 02-04 for The Sky: cap, shorts with 3/4 tights, long socks (flats, awaiting approval)
def gtile(shapes, label):
    """shapes: list of (path, fill, light?, clip id, inner svg). Draws each as cloth on one tile."""
    out = ""
    for d_, fill, light, cid, inner in shapes:
        out += cloth(d_, fill, light, fold("M0,0", "#000", 0), cid, inner)
    return tile(out, "#F1F2F0", label=label)
def vlogo(x, y, w, tint="t_ink"):      # the wordmark set vertically, reading bottom to top
    return f'<g transform="translate({x},{y}) rotate(-90)">{logo("wm", 0, 0, w, tint)}</g>'

def lum(h): return (0.299 * int(h[1:3], 16) + 0.587 * int(h[3:5], 16) + 0.114 * int(h[5:7], 16)) / 255
def dk(h): return lum(h) < 0.55                      # dark fabric -> white logo, light grain
def tn(h): return "t_white" if dk(h) else "t_ink"
def ik(h): return "#F3F4F2" if dk(h) else INK
# Colour combos per collection. Each piece takes a different pairing from the collection's five colours,
# so the cap, shorts and socks are not just the tee's colours repeated.
KIT = [
 dict(code="MOS", n="The Moss", co="4.5239°N  101.3819°E", cap=("#8A9A5B", "#C9CFCB", "#B7C948"), sh=("#3A2E24", "#8A9A5B", "#2F3B2A", "#B7C948"), so=("#C9CFCB", "#2F3B2A", "#2F3B2A", "#B7C948", "#B7C948")),
 dict(code="WLD", n="The Wild", co="4.6325°N  102.2342°E", cap=("#8A6B4A", "#121A17", "#E08A2B"), sh=("#1F3A2E", "#8A6B4A", "#121A17", "#E08A2B"), so=("#BFC6C0", "#E08A2B", "#121A17", "#8A6B4A", "#E08A2B")),
 dict(code="SKY", n="The Sky", co="3.2094°N  101.1865°E", cap=("#F1F2EF", "#7FB2DD", "#F4D24A"), sh=("#2E5C8A", "#7FB2DD", "#7FB2DD", "#F4D24A"), so=("#F1F2EF", "#F2C7A0", "#F2C7A0", "#2E5C8A", "#F4D24A")),
 dict(code="OCN", n="The Ocean", co="5.7750°N  103.0150°E", cap=("#E6D9BD", "#1E9AA8", "#F0775A"), sh=("#0F4C6B", "#E6D9BD", "#1E9AA8", "#F0775A"), so=("#F3F4F2", "#F0775A", "#0F4C6B", "#1E9AA8", "#F0775A")),
 dict(code="CAV", n="The Caves", co="3.8139°N  113.7814°E", cap=("#B9B0A0", "#4A3A2A", "#C9A24A"), sh=("#141414", "#4F6A4A", "#4A3A2A", "#C9A24A"), so=("#B9B0A0", "#4F6A4A", "#141414", "#C9A24A", "#C9A24A")),
 dict(code="DUN", n="The Dune", co="2.2164°N  102.1943°E", cap=("#F3EBDD", "#B58B5A", "#D9532B"), sh=("#6B4E33", "#D9B98A", "#B58B5A", "#D9532B"), so=("#F3EBDD", "#D9532B", "#B58B5A", "#6B4E33", "#D9532B")),
 dict(code="MSN", n="The Monsoon", co="4.1300°N  103.3900°E", cap=("#6E7B85", "#2B3440", "#E0342B"), sh=("#1B4A5A", "#6E7B85", "#2B3440", "#E0342B"), so=("#DDE3E4", "#E0342B", "#2B3440", "#1B4A5A", "#E0342B")),
]
def cap_front(k):
    body, panel, th = k["cap"]; i = k["code"]
    crown = "M250,470 C250,300 320,230 400,230 C480,230 550,300 550,470 Z"
    brim = "M232,462 C300,452 500,452 568,462 C592,520 520,562 400,562 C280,562 208,520 232,462 Z"
    inner = (f'<path d="M250,470 C250,300 320,230 400,232 C360,300 336,380 330,470 Z" fill="{panel}"/>'
             + seam("M400,232 C360,300 336,380 330,470", th, 3.4) + seam("M400,232 C440,300 464,380 470,470", th, 3.4)
             + bartack(330, 462, th) + bartack(470, 462, th) + logo("sym", 368, 340, 64, tn(body))
             + '<rect x="240" y="452" width="320" height="20" fill="#000" opacity=".08"/>')
    sc = "#fff" if dk(panel) else "#000"
    b_in = (stitch("M250,480 C320,470 480,470 550,480", sc, .3, 1.3) + stitch("M246,500 C320,520 480,520 554,500", sc, .3, 1.3)
            + f'<text class="mn" x="400" y="546" font-size="8" fill="{ik(panel)}" text-anchor="middle" letter-spacing=".14em">{k["co"]}</text>')
    btn = f'<ellipse cx="400" cy="231" rx="13" ry="5" fill="{th}"/>'
    return tile(cloth(brim, panel, dk(panel), "", "cpb" + i, b_in) + cloth(crown, body, dk(body), fold("M300,300 C280,360 270,420 270,470", "#000", .06, 40), "cpc" + i, inner) + btn, "#F1F2F0", label=f'{k["n"]} cap')
def shorts_tights(k):
    sh, panel, tg, th = k["sh"]; i = k["code"]
    legL, legR = "M236,418 L390,430 L374,700 L270,700 Z", "M564,418 L410,430 L426,700 L530,700 Z"
    short = "M250,170 L550,170 L574,420 Q575,430 565,431 L420,436 Q411,436 410,427 L400,330 L390,427 Q389,436 380,436 L235,431 Q225,430 226,420 Z"
    hs = "#fff" if dk(tg) else "#000"
    t_in_L = (seam("M250,430 C262,520 266,610 274,696", th, 3.2) + rdot(274, 694, 3.2)
              + f'<text class="mn" transform="translate(286,660) rotate(-87)" font-size="8" fill="{ik(tg)}" letter-spacing=".14em">{k["co"]}</text>'
              + '<rect x="262" y="676" width="120" height="24" fill="#000" opacity=".16"/>' + stitch("M272,678 H374", hs, .35, 1.2))
    t_in_R = ('<rect x="420" y="676" width="120" height="24" fill="#000" opacity=".16"/>' + stitch("M428,678 H528", hs, .35, 1.2) + logo("sym", 452, 610, 46, tn(tg)))
    ss = "#fff" if dk(sh) else "#000"
    s_in = (f'<path d="M250,170 L304,170 L276,433 L235,431 Q225,430 226,420 Z" fill="{panel}"/>'
            + '<path d="M250,170 L550,170 L554,212 L246,212 Z" fill="#000" opacity=".12"/>'
            + "".join(f'<path d="M{262+j*13},174 l-1,34" stroke="{ss}" stroke-opacity=".16" stroke-width="1.6"/>' for j in range(22))
            + seam("M304,212 L276,433", th, 3.4) + bartack(303, 216, th, -83)
            + f'<path d="M386,192 C382,250 372,290 364,318 M414,192 C418,250 428,290 436,318" stroke="{th}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
            + stitch("M232,414 L384,424", ss, .3, 1.3) + stitch("M416,424 L568,414", ss, .3, 1.3)
            + f'<path d="M562,372 L574,420" stroke="{ss}" stroke-opacity=".4" stroke-width="2.4"/>' + rdot(562, 372, 3.2)
            + logo("sym", 478, 360, 54, tn(sh)) + f'<g transform="translate(520,214) rotate(-3)"><rect width="30" height="16" fill="{th}"/></g>')
    f1 = fold("M320,440 C316,540 322,620 318,700", "#fff", .07, 30); f2 = fold("M480,440 C484,540 478,620 482,700", "#fff", .07, 30)
    fs = fold("M300,240 C290,320 300,380 290,430", "#000", .05, 40) + fold("M500,240 C510,320 500,380 510,430", "#000", .05, 40) + fold("M400,230 L400,330", "#000", .14, 30)
    return tile(cloth(legL, tg, dk(tg), f1, "stl" + i, t_in_L) + cloth(legR, tg, dk(tg), f2, "str" + i, t_in_R) + cloth(short, sh, dk(sh), fs, "sts" + i, s_in), "#F1F2F0", label=f'{k["n"]} shorts with 3/4 tights')
def socks(k):
    a, ah, b, bh, band = k["so"]; i = k["code"]
    K = "M0,0 H120 V420 C120,456 138,470 188,486 C258,508 272,572 218,586 C158,602 58,578 22,532 C-4,498 0,460 0,420 Z"
    def one(tx, ty, rot, body, heel, cid):
        ink = ik(body)
        ribs = "".join(f'<path d="M{8+j*9.6},0 V62" stroke="{ink}" stroke-opacity=".16" stroke-width="2"/>' for j in range(12))
        inner = (ribs + f'<rect x="0" y="70" width="120" height="10" fill="{band}"/>'
                 + f'<path d="M0,420 C0,460 -4,498 22,532 L62,498 C44,470 56,440 120,420Z" fill="{heel}"/>'
                 + f'<path d="M188,486 C258,508 272,572 218,586 C204,552 194,520 188,486Z" fill="{heel}"/>'
                 + vlogo(46, 392, 290, tn(body))
                 + f'<text class="mn" x="60" y="98" font-size="7" fill="{ink}" text-anchor="middle" letter-spacing=".12em">OFN—{i}</text>')
        return f'<g transform="translate({tx},{ty}) rotate({rot})">' + cloth(K, body, dk(body), fold("M90,100 V400", "#000", .06, 26), cid, inner) + '</g>'
    return tile(one(190, 96, -4, a, ah, "sk1" + i) + one(440, 110, 4, b, bh, "sk2" + i), "#F1F2F0", label=f'{k["n"]} long socks')
def kitrows():
    out = ""
    for k in KIT:
        sw = "".join(f'<i style="background:{h}"></i>' for h in dict.fromkeys(list(k["cap"]) + list(k["sh"]) + list(k["so"])))
        out += (f'<div class="kitrow"><div class="kithead"><b>{k["n"]}</b><span class="mn">OFN—{k["code"]}</span><div class="chips">{sw}</div></div>'
                f'<figure class="flat">{cap_front(k)}<figcaption><b>Cap</b></figcaption></figure>'
                f'<figure class="flat">{shorts_tights(k)}<figcaption><b>Shorts + 3/4 tights</b></figcaption></figure>'
                f'<figure class="flat">{socks(k)}<figcaption><b>Long socks</b></figcaption></figure></div>')
    return out

head = open(os.path.join(OUT, "..", "identity", "source", "page.html")).read()
head = head[head.index("<meta"):head.index("</style>")]
PAGE = open(f"{HERE}/page.html").read()
def part(k, cap, w):
    h = 300 / AR[k]
    return (f'<figure class="plate dark"><div class="stage"><svg viewBox="0 0 300 {h:.0f}" style="width:{w}"><use href="#lg_{k}" width="300" height="{h:.0f}" '
            f'filter="url(#t_white)"/></svg></div><figcaption><b>{cap[0]}</b><span>{cap[1]}</span></figcaption></figure>')
html = (PAGE.replace("{{HEAD}}", head).replace("{{DEFS}}", DEFS)
        .replace("{{HERO}}", f'<svg class="mk hero-mark" viewBox="0 0 781 83"><use href="#lg_wm" width="781" height="83" filter="url(#t_white)"/></svg>')
        .replace("{{PARTS}}", part("sym", ("The O", "Chest mark, cap, labels"), "62%") + part("f", ("The F", "Back, sleeve, sock"), "44%")
                 + part("nm", ("The NM", "Back, hem, shorts"), "52%") + part("wm", ("Wordmark", "Neck label, hang tag, packaging"), "86%"))
        .replace("{{F_F}}", final(False)).replace("{{F_B}}", final(True))
        .replace("{{D3}}", final(True, "D3", "262 212 276 100"))
        .replace("{{KIT}}", kitrows())
        .replace("{{SHOT}}", "data:image/png;base64," + b64(f"{OUT}/shots/SKY_front.png")))
open(f"{OUT}/designs.html", "w").write(html)
print("ok", {k: round(v, 2) for k, v in AR.items()})
