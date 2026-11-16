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
        .replace("{{A_F}}", dirA(False)).replace("{{A_B}}", dirA(True)).replace("{{B_F}}", dirB(False)).replace("{{B_B}}", dirB(True))
        .replace("{{C_F}}", dirAB(False)).replace("{{C_B}}", dirAB(True)).replace("{{DETAIL}}", detail()))
open(f"{OUT}/designs.html", "w").write(html)
print("ok", {k: round(v, 2) for k, v in AR.items()})
