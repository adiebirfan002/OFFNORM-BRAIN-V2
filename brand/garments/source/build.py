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
def base(extra, back, cid, c=SKY):
    f = (fold("M290,340 C310,440 280,560 300,720", "#000", .05) + fold("M520,340 C500,440 530,580 510,720", "#000", .05)
         + fold("M400,250 C380,400 420,560 400,720", "#000", .12, 64))
    neck = ('<path d="M324,148 C362,166 438,166 476,148 L468,138 C438,152 362,152 332,138 Z" fill="#000" opacity=".16"/>' if back else
            '<path d="M324,148 C352,190 448,190 476,148 L464,141 C440,174 360,174 336,141 Z" fill="#000" opacity=".13"/>'
            '<path d="M336,141 C360,156 440,156 464,141 C440,174 360,174 336,141Z" fill="#000" opacity=".42"/>')
    return tile(cloth(T2B if back else T2, c["body"], False, f, cid, extra[0] + neck + extra[1] + stitch("M206,692 H594", "#000", .16)), "#F1F2F0")
def sleeve_panels(c, left=True, right=True):
    pl = f'<path d="M262,230 C234,268 214,310 204,352 L200,356 L128,410 L74,352 C130,308 204,256 262,230Z" fill="{c["panel"]}"/>'
    pr = f'<path d="M538,230 C566,268 586,310 596,352 L600,356 L672,410 L726,352 C670,308 596,256 538,230Z" fill="{c["panel"]}"/>'
    sl = seam("M262,230 C204,256 130,308 74,352", c["thread"], 3); sr = seam("M538,230 C596,256 670,308 726,352", c["thread"], 3)
    return (pl if left else "") + (pr if right else ""), (sl if left else "") + (sr if right else "")
def cap(t, x, y, anchor="start", fs=8.5): return mono(t, x, y, fs, INK, anchor, .1)

def dirA(back):
    """A. Centre: a plain tee, two contrast raglan seams, the O small in the middle of the chest."""
    c = SKY
    seams = (seam(RL, c["thread"]) + seam(RR, c["thread"]) + seam("M200,640 H392", c["thread"], 3) + seam("M408,628 H600", c["thread"], 3)
             + rdot(392, 640, 3.2) + rdot(408, 628, 3.2))                    # one hem seam that breaks and misses
    if not back:
        g = logo("sym", 368, 296, 64) + cap("3.2094°N  101.1865°E", 400, 358, "middle", 7.5)
    else:
        g = logo("wm", 322, 236, 156) + cap("OFN—SKY—001  /  30°C  70%  07:10", 400, 270, "middle", 7.5)
    return base(("", seams + g), back, "dA" + ("b" if back else "f"))

def dirB(back):
    """B. Arm: nothing on the chest. One white sleeve carries the O."""
    c = SKY
    pan, ps = sleeve_panels(c, left=not back, right=back)
    rag = seam(RL if not back else RR, c["thread"])
    if not back:
        g = (f'<g transform="translate(150,342) rotate(-38)">{logo("sym", -30, -20, 60)}</g>'
             + cap("3.2094°N  101.1865°E", 216, 684, "start", 7.5)
             + f'<g transform="translate(566,650) rotate(-3)"><rect width="34" height="20" fill="{c["thread"]}"/></g>')
    else:
        g = (f'<g transform="translate(650,342) rotate(38)">{logo("sym", -30, -20, 60)}</g>'
             + logo("f", 222, 636, 40) + logo("nm", 532, 636, 48) + cap("30°C / 70% / 07:10", 400, 684, "middle", 7.5))
    return base((pan, ps + rag + g), back, "dB" + ("b" if back else "f"))

def dirC(back):
    """C. The quiet O: the body's panel lines trace the logo's O in tonal thread. Logo on the arm."""
    c = SKY; th = "#4F8DC2"
    if not back:
        ring = seam("M356,236 H330 A94,94 0 0 0 236,330 V548 A94,94 0 0 0 330,642 H352", th) + seam("M444,236 H470 A94,94 0 0 1 564,330 V548 A94,94 0 0 1 470,642 H374", th)
        bar = seam("M236,470 H384", th, 3.4) + seam("M408,458 H564", th, 3.4)
        cut = seam("M352,642 L436,236", th, 2.2) + seam("M374,642 L458,236", th, 2.2)
        g = f'<g transform="translate(662,348) rotate(38)">{logo("sym", -26, -18, 52, "t_white")}</g>' + cap("3.2094°N  101.1865°E", 216, 684, "start", 7.5)
    else:
        ring = seam("M444,236 H470 A94,94 0 0 1 564,330 V548 A94,94 0 0 1 470,642 H448", th) + seam("M356,236 H330 A94,94 0 0 0 236,330 V548 A94,94 0 0 0 330,642 H426", th)
        bar = seam("M564,470 H416", th, 3.4) + seam("M392,458 H236", th, 3.4)
        cut = seam("M448,642 L364,236", th, 2.2) + seam("M426,642 L342,236", th, 2.2)
        g = f'<g transform="translate(138,348) rotate(-38)">{logo("sym", -26, -18, 52, "t_white")}</g>' + cap("30°C / 70% / 07:10", 584, 684, "end", 7.5)
    return base(("", ring + bar + cut + g), back, "dC" + ("b" if back else "f"))

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
        .replace("{{C_F}}", dirC(False)).replace("{{C_B}}", dirC(True)))
open(f"{OUT}/designs.html", "w").write(html)
print("ok", {k: round(v, 2) for k, v in AR.items()})
