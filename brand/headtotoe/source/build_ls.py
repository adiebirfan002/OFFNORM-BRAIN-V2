"""OFFNORM long-sleeve tee, drawn from the approved Sky tee (D3), for the six head-to-toe colourways.
Run from the repo root:  python3 brand/headtotoe/source/build_ls.py  -> brand/headtotoe/longsleeve.html"""
import os, io, re, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("h2t", os.path.join(HERE, "build.py")); H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(H)
G = H.G; INK = G.INK; BG = H.BG
JX, JY = G.JX, G.JY
# body and raglan as the approved tee; sleeves run to the wrist, angled down from the shoulder
LS = ("M324,148 C352,190 448,190 476,148 L612,186 C668,206 712,260 730,330 L768,640 L700,662 L640,420 L600,370 L600,700 Q600,712 588,712 "
      "L212,712 Q200,712 200,700 L200,370 L160,420 L100,662 L32,640 L70,330 C88,260 132,206 188,186 Z")
LSB = LS.replace("C352,190 448,190", "C362,166 438,166")
# wearer's right sleeve panel: starts at the raglan midpoint J, runs down the outer forearm to the cuff, so every seam meets another seam
PANEL = f"M{JX},{JY} C242,273.5 218,322 200,370 L160,420 L100,662 L32,640 L64,380 C130,330 212,272 {JX},{JY} Z"
PSEAM = f"M{JX},{JY} C212,272 130,330 64,380"
def ls(k, back):
    body, panel, thread, logo_c, text_c = k["tee"]; i = k["code"] + ("b" if back else "f")
    pan, ps = (G.flip(PANEL), G.flip(PSEAM)) if back else (PANEL, PSEAM)
    jx = 800 - JX if back else JX
    f = (G.fold("M290,340 C310,440 280,560 300,720", "#000", .05) + G.fold("M520,340 C500,440 530,580 510,720", "#000", .05)
         + G.fold("M400,250 C380,400 420,560 400,720", "#000", .12, 64) + G.fold("M90,420 C80,520 70,600 64,650", "#000", .06, 26)
         + G.fold("M710,420 C720,520 730,600 736,650", "#000", .06, 26))
    neck = ('<path d="M324,148 C362,166 438,166 476,148 L468,138 C438,152 362,152 332,138 Z" fill="#000" opacity=".16"/>'
            + G.stitch("M330,152 C364,170 436,170 470,152", "#000", .28, 1.2) if back else
            '<path d="M324,148 C352,190 448,190 476,148 L464,141 C440,174 360,174 336,141 Z" fill="#000" opacity=".13"/>'
            '<path d="M336,141 C360,156 440,156 464,141 C440,174 360,174 336,141Z" fill="#000" opacity=".42"/>'
            + G.stitch("M320,154 C350,198 450,198 480,154", "#000", .28, 1.2))
    cuffs = ('<path d="M32,640 L100,662 L104,646 L37,624 Z" fill="#000" opacity=".14"/><path d="M768,640 L700,662 L696,646 L763,624 Z" fill="#000" opacity=".14"/>'
             + "".join(f'<path d="M{37+j*7},{624+j*2.2} l-4,16" stroke="#000" stroke-opacity=".12" stroke-width="1.6"/>' for j in range(10))
             + "".join(f'<path d="M{763-j*7},{624+j*2.2} l4,16" stroke="#000" stroke-opacity=".12" stroke-width="1.6"/>' for j in range(10)))
    hems = (G.stitch("M206,690 H594", "#000", .3, 1.3) + '<path d="M200,370 V700 M600,370 V700" stroke="#000" stroke-opacity=".10" stroke-width="2" fill="none"/>'
            + G.stitch("M160,420 L100,662", "#000", .18, 1.1) + G.stitch("M640,420 L700,662", "#000", .18, 1.1))
    seams = (G.seam(G.RL, thread) + G.seam(G.RR, thread) + G.seam(ps, thread, 3.4) + G.bartack(jx, JY, thread, 50 if back else -50)
             + G.rdot(596 if back else 204, 366, 3.6))
    if not back:
        g = G.logo("sym", 368, 296, 64, H.tid(logo_c)) + f'<g transform="translate(566,648) rotate(-3)"><rect width="34" height="20" fill="{thread}"/></g>'
    else:
        blk = (G.block("D3").replace("OFN—SKY—001", f"OFN—{k['code']}—LS1").replace("THE SKY", k["n"].upper()).replace("30°C / 70% RH", k["cond"][0])
               .replace(">07:10<", f">{k['cond'][1]}<").replace("3.2094°N  101.1865°E", k["co"])
               .replace(f'fill="{INK}"', f'fill="{text_c}"').replace(f'stroke="{INK}"', f'stroke="{text_c}"').replace('filter="url(#t_ink)"', f'filter="url(#{H.tid(text_c)})"'))
        g = blk + G.logo("f", 248, 632, 40, H.tid(text_c)) + G.logo("nm", 504, 632, 48, H.tid(text_c))
    inner = f'<path d="{pan}" fill="{panel}"/>' + neck + hems + cuffs + seams + g
    return G.tile(G.cloth(LSB if back else LS, body, False, f, "ls" + i, inner), BG, label=f'{k["n"]} long-sleeve tee {"back" if back else "front"}')

rows = ""
for k in H.KITS:
    nm_of = {h: n for n, h, _ in k["pal"]}
    body, panel, thread, logo_c, text_c = k["tee"]
    chips = "".join(f'<span class="chip"><i style="background:{h}"></i>{nm_of[h]}</span>' for h in dict.fromkeys((body, panel, thread, logo_c)))
    rows += (f'<article class="ls" id="{k["code"].lower()}"><header><small>OFN—{k["code"]}—LS1</small><h2>{k["n"]}</h2><div class="chips">{chips}</div></header>'
             f'<div class="pair"><figure>{ls(k, False)}<figcaption>Front</figcaption></figure><figure>{ls(k, True)}<figcaption>Back</figcaption></figure></div></article>')
tints = "".join(G.tint(i, h) for i, h in H.TINTS.items())
page = open(os.path.join(HERE, "page_ls.html")).read()
page = page.replace("{{DEFS}}", G.DEFS + f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{tints}</defs></svg>').replace("{{ROWS}}", rows)
open(os.path.join(OUT, "longsleeve.html"), "w").write(page); print("ok", len(page))
