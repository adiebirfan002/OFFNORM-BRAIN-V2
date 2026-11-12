"""Round 2 mock-ups, drawn after the founder's Collection Reference: panelled raglan tees with contrast
flatlock seams, colour-blocked sleeves, a small chest mark, a dotted back graphic, two-tone cap."""
import mocks
from mocks import use, block, mono, tile, cloth, fold, stitch, TEE, TEEB
from kit import _pill_points
YEL, BROWN, NAVY, GREY, CREAM, TAUPE = "#D9CC3C", "#4B3B25", "#1B2233", "#C7CEC9", "#E9E3D5", "#5A524C"
mocks.PINK = YEL

def seam(d, c=YEL, w=4.2):
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="{w}" stroke-dasharray="1.2 3.2"/>')
def dot(x, y, r=4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F3F4F2"/>'

def panel_tee(AR, body, panel, bg, cid, back=False, graphic=""):
    shape = TEEB if back else TEE
    L = "M338,170 C292,200 244,262 224,338"; R = "M462,170 C508,200 556,262 576,338"
    sideL = "M224,338 C250,440 236,560 252,646"; sideR = "M576,338 C550,440 564,560 548,646"
    pl = f'<path d="M276,226 C250,262 232,300 224,338 L216,340 L152,392 L98,340 C150,300 220,250 276,226Z" fill="{panel}"/>'
    pr = f'<path d="M524,226 C550,262 568,300 576,338 L584,340 L648,392 L702,340 C650,300 580,250 524,226Z" fill="{panel}"/>'
    f = (fold("M300,330 C320,430 290,560 310,720", "#fff", .06) + fold("M510,330 C490,440 520,580 500,720", "#fff", .05)
         + fold("M400,240 C380,400 420,560 400,720", "#000", .28, 60))
    neck = ('<path d="M318,150 C360,170 440,170 482,150 L474,140 C440,156 360,156 326,140 Z" fill="#000" opacity=".22"/>' if back else
            '<path d="M318,150 C350,196 450,196 482,150 L470,143 C444,180 356,180 330,143 Z" fill="#000" opacity=".2"/>'
            '<path d="M330,143 C356,158 444,158 470,143 C444,180 356,180 330,143Z" fill="#000" opacity=".55"/>')
    x = (pl + pr + neck + seam(L) + seam(R) + seam(sideL) + seam(sideR) + seam("M252,646 H548")
         + seam("M276,226 C220,250 150,300 98,340", w=3) + seam("M524,226 C580,250 650,300 702,340", w=3)
         + dot(252, 646) + dot(548, 646) + stitch("M222,694 H578", "#fff", .2) + graphic)
    return cloth(shape, body, True, f, cid, x)

def tee_front(AR):
    g = (use("e_sw", 448, 292, 96, "#F3F4F2;--ko:" + BROWN, AR["e_sw"])
         + f'<text class="mn" transform="translate(226,236) rotate(-38)" font-size="9" fill="#F3F4F2" letter-spacing=".1em">Off day</text>'
         + f'<text class="mn" transform="translate(528,204) rotate(38)" font-size="9" fill="#F3F4F2" letter-spacing=".1em">Run anyway</text>')
    return tile(panel_tee(AR, BROWN, GREY, "#F1F2EF", "d1", graphic=g), "#E9EBE8", label="Panelled run tee, front")

def tee_back(AR):
    rings = ""
    for k, (n, r, inset) in enumerate(((16, 5.2, 0), (22, 3.9, 20), (28, 2.6, 38), (34, 1.5, 54))):
        pts = _pill_points(n, 318 - inset, 330 - inset, 164 + 2 * inset, 100 + 2 * inset)
        for i, (x, y) in enumerate(pts):
            if k == 1 and i == 4: x += 16; y -= 16
            op = "" if (i + k) % 3 else ' fill-opacity=".0" stroke="#F3F4F2" stroke-width="1.3"'
            rings += f'<circle cx="{round(x,1)}" cy="{round(y,1)}" r="{r}" fill="#F3F4F2"{op}/>'
    txt = (f'<text class="mn" x="400" y="374" font-size="12.5" fill="{YEL}" text-anchor="middle" letter-spacing=".04em">Off Day</text>'
           f'<text class="mn" x="400" y="390" font-size="12.5" fill="{YEL}" text-anchor="middle" letter-spacing=".04em">Club Run°</text>')
    g = rings + txt + seam("M372,160 V214") + seam("M428,160 V214") + dot(372, 216) + dot(428, 216)
    return tile(panel_tee(AR, NAVY, CREAM, "#fff", "d2", back=True, graphic=g), "#E9EBE8", label="Panelled run tee, back")

def cap(AR):
    C = "M150,500 C138,350 250,262 372,262 C486,262 556,336 560,468 L560,500 Z"
    B = "M548,462 C630,464 704,486 736,518 C740,528 732,534 722,531 C660,516 600,512 548,512 Z"
    f = fold("M300,300 C260,360 250,440 250,500", "#fff", .07, 40) + fold("M200,420 C190,450 190,480 190,500", "#000", .3, 40)
    x = ('<path d="M372,262 C424,330 444,420 444,500 L284,500 C284,420 300,330 372,262Z" fill="#E7DE8E"/>'
         + seam("M372,262 C424,330 444,420 444,500", "#cfc7b0", 2.4) + seam("M372,262 C300,330 284,420 284,500", "#cfc7b0", 2.4)
         + '<rect x="140" y="480" width="430" height="22" fill="#000" opacity=".12"/>'
         + f'<g filter="url(#emb)">{use("osw", 326, 404, 74, "#3d3733", AR["osw"])}</g>')
    brim = (f'<path d="{B}" fill="#000" opacity=".3" filter="url(#sh)" transform="translate(0,14)"/><path d="{B}" fill="{TAUPE}"/>'
            + stitch("M556,474 C626,476 690,494 722,516", "#fff", .3))
    return tile(cloth(C, TAUPE, True, f, "d3", x) + brim + '<ellipse cx="372" cy="262" rx="12" ry="5" fill="#6a625c"/>', "#E9EBE8", label="Two-tone cap")

def shorts(AR):
    P = ("M226,214 L574,214 L612,560 Q613,572 601,573 L432,588 Q420,589 418,577 L400,396 L382,577 Q380,589 368,588 "
         "L199,573 Q187,572 188,560 Z")
    f = (fold("M300,280 C280,400 300,500 280,590", "#fff", .06) + fold("M500,280 C520,400 500,500 520,590", "#fff", .06)
         + fold("M400,300 L400,420", "#000", .4, 40))
    x = ('<path d="M226,214 L574,214 L579,258 L221,258 Z" fill="#000" opacity=".25"/>'
         + seam("M560,262 C580,380 590,470 606,556", YEL, 3) + dot(560, 262, 3.4)
         + stitch("M196,548 L374,564", "#fff", .2) + stitch("M426,564 L604,548", "#fff", .2)
         + use("e_row", 452, 500, 108, "#F3F4F2", AR["e_row"]))
    return tile(cloth(P, "#46443A", True, f, "d4", x), "#E9EBE8", label="Shorts")

def detail(AR):
    bg = (f'<rect width="800" height="800" fill="{BROWN}" filter="url(#grainL)"/>'
          f'<path d="M-20,640 C200,560 380,300 420,-20 L-20,-20Z" fill="{GREY}"/><path d="M-20,640 C200,560 380,300 420,-20 L-20,-20Z" fill="{GREY}" filter="url(#grainD)" opacity=".6"/>'
          '<path d="M-20,640 C200,560 380,300 420,-20" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="26" filter="url(#blur)"/>'
          + seam("M-20,640 C200,560 380,300 420,-20", YEL, 13) + seam("M300,820 C420,700 700,640 820,650", YEL, 13)
          + '<circle cx="300" cy="812" r="0"/>')
    em = f'<g filter="url(#emb)">{use("e_sw", 400, 330, 300, "#F3F4F2;--ko:" + BROWN, AR["e_sw"])}</g>'
    cap_ = mono("CHEST MARK, 38 MM, SILICONE PRINT", 400, 470, 13, "#F3F4F2", sp=.16)
    return tile(bg + em + cap_, BROWN, label="Chest mark close-up")

def swap(svg):
    return svg.replace('href="#stray"', 'href="#osw"')
def labels(AR): return swap(mocks.labels(AR))
def hangtag(AR): return swap(mocks.hangtag(AR))
def posters(AR): return swap(mocks.posters(AR))
