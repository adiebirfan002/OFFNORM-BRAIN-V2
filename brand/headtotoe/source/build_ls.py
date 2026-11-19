"""OFFNORM long-sleeve tee, drawn from the approved Sky tee (D3), for the six head-to-toe colourways.
Run from the repo root:  python3 brand/headtotoe/source/build_ls.py  -> brand/headtotoe/longsleeve.html"""
import os, io, re, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("h2t", os.path.join(HERE, "build.py")); H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(H)
G = H.G; INK = G.INK; BG = H.BG
JX, JY = G.JX, G.JY
# Long sleeve v2, after the founder's FPA reference: relaxed boxy body, long straight sleeves with a plain hem,
# contrast overlock stitching on every panel seam, mesh panels for air. OFFNORM's twist: both side panels are cut,
# but only the wearer's RIGHT side is coloured, and every panel seam starts from one point J on the raglan seam.
LS = ("M330,140 C356,184 444,184 470,140 L620,176 C680,196 724,240 742,300 L782,656 L710,678 L640,420 L628,380 L626,712 Q626,724 614,724 "
      "L186,724 Q174,724 174,712 L172,380 L160,420 L90,678 L18,656 L58,300 C76,240 120,196 180,176 Z")
LSB = LS.replace("C356,184 444,184", "C366,160 434,160")
J = (257.25, 247.5)
RAG_L = "M344,160 C300,200 214,280 172,380"; RAG_R = G.flip(RAG_L)
LOW = "C225,285 193,330 172,380"                         # raglan from J down to the underarm
SEAM_A = f"M{J[0]},{J[1]} C200,280 110,330 47,400"        # J to the outer sleeve: sleeve panel
SEAM_B = f"M{J[0]},{J[1]} C222,400 214,600 232,724"       # J to the hem: side-body panel
P_SLEEVE = f"M{J[0]},{J[1]} {LOW} L160,420 L90,678 L18,656 L47,400 C110,330 200,280 {J[0]},{J[1]} Z"
P_SIDE = f"M{J[0]},{J[1]} {LOW} L174,712 Q174,724 186,724 L232,724 C214,600 222,400 {J[0]},{J[1]} Z"
def ls(k, back):
    body, panel, thread, logo_c, text_c = k["tee"]; i = k["code"] + ("b" if back else "f")
    R = (lambda d: G.flip(d)) if back else (lambda d: d)       # wearer's right is drawn on the right when seen from the back
    L = (lambda d: d) if back else (lambda d: G.flip(d))
    hs = "#fff" if G.dk(body) else "#000"
    mesh = (f'<pattern id="m{i}" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.5" fill="{hs}" fill-opacity=".16"/></pattern>'
            f'<pattern id="mp{i}" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.5" fill="#000" fill-opacity=".10"/></pattern>')
    panels = (f'<path d="{R(P_SLEEVE)}" fill="{panel}"/><path d="{R(P_SIDE)}" fill="{panel}"/>'
              f'<path d="{R(P_SLEEVE)}" fill="url(#mp{i})"/><path d="{R(P_SIDE)}" fill="url(#mp{i})"/>'
              f'<path d="{L(P_SLEEVE)}" fill="url(#m{i})"/><path d="{L(P_SIDE)}" fill="url(#m{i})"/>')
    f = (G.fold("M300,340 C320,440 290,560 310,720", "#000", .05) + G.fold("M500,340 C480,440 510,580 490,720", "#000", .05)
         + G.fold("M400,250 C380,400 420,560 400,720", "#000", .12, 64) + G.fold("M80,430 C70,530 60,610 54,660", "#000", .06, 26)
         + G.fold("M720,430 C730,530 740,610 746,660", "#000", .06, 26))
    neck = ('<path d="M330,140 C366,160 434,160 470,140 L462,130 C434,146 366,146 338,130 Z" fill="#000" opacity=".16"/>'
            + G.stitch("M336,146 C366,166 434,166 464,146", "#000", .28, 1.2) if back else
            '<path d="M330,140 C356,184 444,184 470,140 L458,133 C436,168 364,168 342,133 Z" fill="#000" opacity=".13"/>'
            '<path d="M342,133 C364,150 436,150 458,133 C436,168 364,168 342,133Z" fill="#000" opacity=".42"/>'
            + G.stitch("M326,148 C354,194 446,194 474,148", "#000", .28, 1.2))
    hems = (G.stitch("M180,704 H620", "#000", .3, 1.3) + G.stitch("M22,640 L92,662", "#000", .3, 1.3) + G.stitch("M778,640 L708,662", "#000", .3, 1.3))
    ov = lambda d: G.seam(d, thread, 3.4)                     # contrast overlock on every panel seam
    seams = (ov(RAG_L) + ov(RAG_R) + ov(SEAM_A) + ov(SEAM_B) + ov(G.flip(SEAM_A)) + ov(G.flip(SEAM_B))
             + G.rdot(J[0], J[1], 4.2) + G.rdot(800 - J[0], J[1], 4.2))   # reflective dots where the seams meet
    if not back:
        g = G.logo("sym", 368, 292, 64, H.tid(logo_c)) + f'<g transform="translate(500,688) rotate(-3)"><rect width="34" height="20" fill="{thread}"/></g>'
    else:
        blk = (G.block("D3").replace("OFN—SKY—001", f"OFN—{k['code']}—LS1").replace("THE SKY", k["n"].upper()).replace("30°C / 70% RH", k["cond"][0])
               .replace(">07:10<", f">{k['cond'][1]}<").replace("3.2094°N  101.1865°E", k["co"])
               .replace(f'fill="{INK}"', f'fill="{text_c}"').replace(f'stroke="{INK}"', f'stroke="{text_c}"').replace('filter="url(#t_ink)"', f'filter="url(#{H.tid(text_c)})"'))
        g = blk + G.logo("f", 262, 650, 40, H.tid(text_c)) + G.logo("nm", 490, 650, 48, H.tid(text_c))
    inner = mesh + panels + neck + hems + seams + g
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
