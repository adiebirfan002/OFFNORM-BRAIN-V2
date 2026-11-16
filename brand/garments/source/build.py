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

# ---------- Design 01: The Sky panel tee
SKY = dict(body="#7FB2DD", panel="#F1F2EF", thread="#F4D24A", deep="#2E5C8A")
def sky_front():
    c = SKY
    pl = f'<path d="M276,226 C250,262 232,300 224,338 L216,340 L152,392 L98,340 C150,300 220,250 276,226Z" fill="{c["panel"]}"/>'
    wedge = f'<path d="M216,588 L295,588 L218,716 Z" fill="{c["panel"]}"/>'
    f = (fold("M300,330 C320,430 290,560 310,720", "#000", .05) + fold("M510,330 C490,440 520,580 500,720", "#000", .05)
         + fold("M400,240 C380,400 420,560 400,720", "#000", .13, 60))
    neck = ('<path d="M318,150 C350,196 450,196 482,150 L470,143 C444,180 356,180 330,143 Z" fill="#000" opacity=".13"/>'
            '<path d="M330,143 C356,158 444,158 470,143 C444,180 356,180 330,143Z" fill="#000" opacity=".42"/>')
    x = (pl + wedge + neck + seam("M338,170 C292,200 244,262 224,338", c["thread"]) + seam("M276,226 C220,250 150,300 98,340", c["thread"], 3)
         + seam("M548,176 L224,716", c["thread"]) + seam("M560,182 L236,722", c["thread"], 2.6)
         + seam("M216,588 H292", c["thread"], 3) + seam("M287,612 H584", c["thread"], 3)
         + rdot(548, 176) + rdot(292, 588, 3.4) + rdot(287, 612, 3.4) + rdot(584, 612, 3.4)
         + logo("sym", 504, 300, 58) + mono("OFN—SKY—001", 504, 354, 7.5, INK, sp=.1)
         + f'<text class="mn" transform="translate(402,434) rotate(-59)" font-size="8.5" fill="{INK}" letter-spacing=".14em">3.2094°N  101.1865°E</text>'
         + f'<text class="mn" transform="translate(524,206) rotate(38)" font-size="8.5" fill="{INK}" letter-spacing=".12em">The Sky</text>'
         + stitch("M222,694 H578", "#000", .18)
         + f'<g transform="translate(574,650) rotate(-3)"><rect x="0" y="0" width="34" height="20" fill="{c["thread"]}"/></g>')
    pins = (pin(1, 388, 440, 110, 520) + pin(2, 200, 330, 70, 190) + pin(3, 290, 600, 110, 640) + pin(4, 548, 318, 700, 250)
            + pin(5, 420, 404, 700, 470) + pin(6, 548, 176, 690, 120) + pin(7, 592, 660, 716, 640))
    return tile(cloth(TEE, c["body"], False, f, "g1f", x) + pins, "#F1F2F0", label="The Sky panel tee, front")
def sky_back():
    c = SKY
    pr = f'<path d="M524,226 C550,262 568,300 576,338 L584,340 L648,392 L702,340 C650,300 580,250 524,226Z" fill="{c["panel"]}"/>'
    wedge = f'<path d="M584,588 L505,588 L582,716 Z" fill="{c["panel"]}"/>'
    f = (fold("M300,330 C320,430 290,560 310,720", "#000", .05) + fold("M510,330 C490,440 520,580 500,720", "#000", .05)
         + fold("M400,240 C380,400 420,560 400,720", "#000", .13, 60))
    neck = '<path d="M318,150 C360,170 440,170 482,150 L474,140 C440,156 360,156 326,140 Z" fill="#000" opacity=".16"/>'
    ring = ""
    for k_, (n, r, R) in enumerate(((18, 3.8, 62), (26, 2.3, 76))):
        for i in range(n):
            a = 6.283 * i / n; x_, y_ = 478 + math.cos(a) * R * 1.3, 292 + math.sin(a) * R * .86
            if k_ == 0 and i == 16: x_ += 16; y_ -= 16
            ring += f'<circle cx="{x_:.1f}" cy="{y_:.1f}" r="{r}" fill="#fff"/>'
    x = (pr + wedge + neck + seam("M462,170 C508,200 556,262 576,338", c["thread"]) + seam("M524,226 C580,250 650,300 702,340", c["thread"], 3)
         + seam("M252,176 L576,716", c["thread"]) + seam("M240,182 L564,722", c["thread"], 2.6)
         + seam("M584,588 H508", c["thread"], 3) + seam("M513,612 H216", c["thread"], 3)
         + rdot(252, 176) + rdot(508, 588, 3.4) + rdot(513, 612, 3.4) + rdot(216, 612, 3.4)
         + ring + logo("sym", 428, 256, 100)
         + logo("f", 244, 470, 66) + logo("nm", 326, 470, 78)
         + mono("3.2094°N", 244, 546, 8, INK, sp=.08) + mono("101.1865°E", 326, 546, 8, INK, sp=.08)
         + mono("30°C / 70% / 07:10", 478, 388, 8.5, INK, "middle", .14)
         + stitch("M222,694 H578", "#000", .18))
    pins = pin(8, 300, 256, 90, 200) + pin(9, 560, 262, 720, 190) + pin(10, 262, 500, 90, 500) + pin(11, 478, 392, 716, 440)
    return tile(cloth(TEEB, c["body"], False, f, "g1b", x) + pins, "#F1F2F0", label="The Sky panel tee, back")

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
        .replace("{{SKY_F}}", sky_front()).replace("{{SKY_B}}", sky_back()))
open(f"{OUT}/designs.html", "w").write(html)
print("ok", {k: round(v, 2) for k, v in AR.items()})
