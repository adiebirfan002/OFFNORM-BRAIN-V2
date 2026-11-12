"""Product mock-ups, drawn as SVG. Each returns an <svg> string. Marks come from <symbol>s (see build.py)."""
INK, HAZE, MON, PINK = "#151617", "#ECEEEC", "#8C9496", "#F4A6C0"

def use(i, x, y, w, color, ar, extra=""):
    return f'<use href="#{i}" x="{x}" y="{y}" width="{w}" height="{round(w/ar,2)}" style="color:{color}" {extra}/>'

def block(lines, x, y, W, fill, lead=1.02, anchor="start", k=0.80):
    """Stacked headline, every line justified to width W."""
    out, cy = [], y
    for ln in lines:
        fs = min(W / (k * len(ln)), 150)
        cy += fs * 0.80
        out.append(f'<text class="hx" x="{x}" y="{round(cy,1)}" font-size="{round(fs,1)}" textLength="{W}" lengthAdjust="spacingAndGlyphs" fill="{fill}">{ln}</text>')
        cy += fs * (lead - 0.80)
    return "".join(out), cy

def mono(t, x, y, fs, fill, anchor="start", sp=0.06, w=500):
    return f'<text class="mn" x="{x}" y="{y}" font-size="{fs}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}" letter-spacing="{sp}em">{t}</text>'

def tile(inner, bg, w=800, h=800, label=""):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/><rect width="{w}" height="{h}" fill="url(#vig)"/>{inner}</svg>')

def cloth(shape, fill, light, folds="", clip_id="c", extra=""):
    """A garment: shadow, body, grain and soft folds clipped to the shape."""
    g = "grainL" if light else "grainD"
    return (f'<clipPath id="{clip_id}"><path d="{shape}"/></clipPath>'
            f'<path d="{shape}" fill="#000" opacity=".28" filter="url(#sh)" transform="translate(0,16)"/>'
            f'<path d="{shape}" fill="{fill}" stroke="{fill}" stroke-width="6" stroke-linejoin="round"/>'
            f'<g clip-path="url(#{clip_id})"><rect width="1700" height="800" fill="{fill}" filter="url(#{g})"/>'
            f'<g filter="url(#blur)">{folds}</g>{extra}</g>')

def fold(d, c, o, w=34):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{o}" stroke-width="{w}" stroke-linecap="round"/>'

def stitch(d, c, o=.5, w=1.6):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{o}" stroke-width="{w}" stroke-dasharray="7 5"/>'

TEE = ("M318,150 C350,196 450,196 482,150 L604,186 C640,200 700,268 726,318 L648,392 L584,340 L584,706 Q584,716 574,716 "
       "L226,716 Q216,716 216,706 L216,340 L152,392 L74,318 C100,268 160,200 196,186 Z")
TEEB = TEE.replace("C350,196 450,196", "C360,170 440,170")

def tee_front(AR):
    f = (fold("M250,330 C300,430 270,560 300,720", "#fff", .07) + fold("M560,330 C520,440 540,580 500,720", "#fff", .06)
         + fold("M400,230 C380,400 420,560 400,720", "#000", .35, 60) + fold("M120,300 L190,360", "#fff", .08, 22)
         + fold("M690,300 L620,360", "#fff", .08, 22))
    x = ('<path d="M318,150 C350,196 450,196 482,150 L470,143 C444,180 356,180 330,143 Z" fill="#26282a"/>'
         '<path d="M330,143 C356,158 444,158 470,143 C444,180 356,180 330,143Z" fill="#0b0c0c"/>'
         + stitch("M222,694 H578", "#fff", .22) + stitch("M160,380 L84,310", "#fff", .2) + stitch("M640,380 L716,310", "#fff", .2)
         + use("ofn", 468, 300, 78, "#F3F4F2", AR["ofn"])
         + mono("OFN—001", 468, 344, 9.5, "#F3F4F2", sp=.14))
    tab = (f'<g transform="translate(205,640) rotate(-3)"><rect x="-22" y="0" width="30" height="46" fill="{PINK}"/>'
           f'<rect x="-22" y="0" width="30" height="46" fill="#000" opacity=".08"/></g>')
    return tile(tab + cloth(TEE, "#17181a", True, f, "c1", x), HAZE, label="Black tee, front")

def tee_back(AR):
    f = (fold("M250,330 C300,430 270,560 300,720", "#000", .08) + fold("M560,330 C520,440 540,580 500,720", "#000", .07)
         + fold("M400,260 C380,400 420,560 400,720", "#fff", .5, 70) + fold("M120,300 L190,360", "#000", .08, 22))
    hl, y = block(["NO RUN", "IS PERFECT."], 300, 420, 200, INK)
    x = ('<path d="M318,150 C360,170 440,170 482,150 L474,140 C440,156 360,156 326,140 Z" fill="#dcdedb"/>'
         + stitch("M222,694 H578", "#000", .25) + stitch("M160,380 L84,310", "#000", .2) + stitch("M640,380 L716,310", "#000", .2)
         + use("stray", 322, 226, 156, INK, 1) + hl
         + mono("31°C / 84% RH / 05:30", 400, y + 22, 10.5, INK, "middle")
         + mono("DESIGNED AT 3°N", 400, y + 40, 10.5, INK, "middle"))
    return tile(cloth(TEEB, "#F1F2EF", False, f, "c2", x), PINK, label="White tee, back print")

def singlet(AR):
    S = ("M296,112 C300,200 250,270 196,296 L196,706 Q196,714 204,714 L596,714 Q604,714 604,706 L604,296 "
         "C550,270 500,200 504,112 L452,112 C440,170 360,170 348,112 Z")
    f = (fold("M240,330 C290,430 260,560 290,720", "#000", .10) + fold("M560,330 C520,440 540,580 510,720", "#000", .08)
         + fold("M400,250 C380,400 420,560 400,720", "#fff", .25, 70))
    holes = ""
    for r in range(7):
        for c in range(9):
            cx, cy = 304 + c * 24, 290 + r * 24
            if r == 0 and c == 8:
                cx += 13; cy -= 13
            holes += f'<circle cx="{cx}" cy="{cy}" r="4.6" fill="#1b1d1e" opacity=".82"/>'
    x = ('<path d="M296,112 C300,200 250,270 196,296" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="12"/>'
         '<path d="M504,112 C500,200 550,270 604,296" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="12"/>'
         '<path d="M348,112 C360,170 440,170 452,112" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="12"/>'
         + holes + stitch("M202,692 H598", "#000", .25)
         + use("wm", 330, 600, 140, INK, AR["wm"]) + mono("VENT GRID / ONE HOLE IS OFF", 400, 478, 9.5, INK, "middle", .14))
    return tile(cloth(S, PINK, False, f, "c3", x), "#1b1d1e", label="Singlet, back, with the vent grid")

def shorts(AR):
    P = ("M226,214 L574,214 L612,560 Q613,572 601,573 L432,588 Q420,589 418,577 L400,396 L382,577 Q380,589 368,588 "
         "L199,573 Q187,572 188,560 Z")
    f = (fold("M300,280 C280,400 300,500 280,590", "#fff", .07) + fold("M500,280 C520,400 500,500 520,590", "#fff", .07)
         + fold("M400,300 L400,420", "#000", .4, 40))
    x = ('<path d="M226,214 L574,214 L579,262 L221,262 Z" fill="#232527"/>'
         + "".join(f'<path d="M{240+i*14},218 l-2,40" stroke="#000" stroke-opacity=".35" stroke-width="2"/>' for i in range(24))
         + '<path d="M384,236 C380,300 372,330 366,352 M416,236 C420,300 428,330 434,352" stroke="#F3F4F2" stroke-width="5" fill="none" stroke-linecap="round"/>'
         + stitch("M196,548 L374,564", "#fff", .22) + stitch("M426,564 L604,548", "#fff", .22)
         + use("stray", 520, 470, 52, "#F3F4F2", 1)
         + '<path d="M600,470 L612,560" stroke="#000" stroke-opacity=".5" stroke-width="3"/>')
    tab = f'<g transform="translate(576,270) rotate(-3)"><rect x="0" y="0" width="40" height="26" fill="{PINK}"/></g>'
    return tile(cloth(P, "#17181a", True, f, "c4", x) + tab, MON, label="Shorts")

def socks(AR):
    K = "M0,0 H132 V300 C132,336 150,350 200,366 C270,388 284,452 230,466 C170,482 70,458 34,412 C6,378 0,340 0,300 Z"
    def one(tx, ty, rot, fill, ink, cid, mark):
        light = fill != "#F1F2EF"
        ribs = "".join(f'<path d="M{8+i*10.5},0 V74" stroke="{ink}" stroke-opacity=".12" stroke-width="2"/>' for i in range(12))
        x = (ribs + f'<rect x="0" y="92" width="132" height="12" fill="{PINK}"/>'
             + f'<path d="M0,300 C0,340 6,378 34,412 L70,380 C50,350 60,320 132,300Z" fill="{ink}" opacity=".10"/>'
             + f'<path d="M200,366 C270,388 284,452 230,466 C215,430 205,400 200,366Z" fill="{ink}" opacity=".10"/>' + mark)
        return f'<g transform="translate({tx},{ty}) rotate({rot})">' + cloth(K, fill, light, fold("M60,110 V330", "#fff" if light else "#000", .08, 30), cid, x) + '</g>'
    a = one(210, 150, -6, "#F1F2EF", INK, "c5", use("ofn", 30, 122, 72, INK, AR["ofn"]))
    b = one(430, 200, 5, "#17181a", "#fff", "c6", use("stray", 42, 120, 48, "#F3F4F2", 1))
    return tile(a + b, HAZE, label="Socks")

def cap(AR):
    C = "M150,500 C138,350 250,262 372,262 C486,262 556,336 560,468 L560,500 Z"
    B = "M548,462 C630,464 704,486 736,518 C740,528 732,534 722,531 C660,516 600,512 548,512 Z"
    f = fold("M300,300 C260,360 250,440 250,500", "#000", .08, 40) + fold("M430,290 C480,340 500,420 500,500", "#fff", .5, 40)
    mesh = "".join(f'<circle cx="{176+c*17+(r%2)*8.5}" cy="{372+r*15}" r="3.2" fill="#000" opacity=".28"/>'
                   for r in range(8) for c in range(7) if 176 + c * 17 < 290 - (0 if r > 2 else (3 - r) * 18) + 20)
    x = (mesh + '<path d="M372,262 C424,330 444,420 444,500 M372,262 C300,330 284,420 284,500" stroke="#000" stroke-opacity=".22" stroke-width="2.5" fill="none"/>'
         + stitch("M372,268 C418,334 437,420 437,500", "#000", .22) + '<rect x="140" y="478" width="430" height="24" fill="#000" opacity=".07"/>'
         + f'<g filter="url(#emb)">{use("ofn", 300, 400, 118, INK, AR["ofn"])}</g>')
    brim = (f'<path d="{B}" fill="#000" opacity=".3" filter="url(#sh)" transform="translate(0,14)"/><path d="{B}" fill="#F1F2EF"/>'
            f'<path d="M548,512 C600,512 660,516 722,531 C732,534 740,528 736,518 C700,512 620,500 548,500Z" fill="{PINK}"/>'
            + stitch("M556,474 C626,476 690,494 722,516", "#000", .25))
    btn = '<ellipse cx="372" cy="262" rx="12" ry="5" fill="#dfe1de"/>'
    return tile(cloth(C, "#F1F2EF", False, f, "c7", x) + brim + btn, "#1b1d1e", label="Cap with embroidered OFN")

def labels(AR):
    bg = ('<rect width="800" height="800" fill="#17181a" filter="url(#grainL)"/>'
          '<path d="M-20,250 C200,225 600,240 820,215" stroke="#000" stroke-opacity=".6" stroke-width="10" fill="none" filter="url(#blur)"/>'
          + stitch("M-20,262 C200,237 600,252 820,227", "#fff", .25))
    main = ('<g transform="translate(400,350) rotate(-3)">'
            '<rect x="-215" y="-78" width="430" height="156" fill="#000" opacity=".45" filter="url(#sh)" transform="translate(0,10)"/>'
            '<rect x="-215" y="-78" width="430" height="156" fill="#F1F2EF"/><rect x="-215" y="-78" width="430" height="156" fill="#F1F2EF" filter="url(#weave)"/>'
            + stitch("M-203,-70 V70", INK, .7, 2) + stitch("M203,-70 V70", INK, .7, 2)
            + use("wm", -160, -34, 320, INK, AR["wm"]) + mono("RUNNING GOODS / 3°N", 0, 52, 11, INK, "middle", .2) + '</g>')
    cond = ('<g transform="translate(560,470) rotate(4)">'
            '<rect x="0" y="0" width="150" height="214" fill="#000" opacity=".45" filter="url(#sh)" transform="translate(0,10)"/>'
            f'<rect x="0" y="0" width="150" height="214" fill="{PINK}"/><rect width="150" height="214" fill="{PINK}" filter="url(#weave)"/>'
            + stitch("M8,10 H142", INK, .7, 2) + use("stray", 16, 26, 34, INK, 1)
            + mono("CONDITIONS", 16, 86, 10.5, INK, sp=.16, w=600) + '<path d="M16,96 H134" stroke="#151617" stroke-width="1.2"/>'
            + mono("31°C", 16, 120, 17, INK, sp=.02, w=600) + mono("84% RH", 16, 144, 17, INK, sp=.02, w=600) + mono("05:30", 16, 168, 17, INK, sp=.02, w=600)
            + mono("OFN—001", 16, 196, 10.5, INK, sp=.16) + '</g>')
    cap = mono("EVERY LABEL IS SEWN 3° OFF LEVEL", 400, 730, 12, "#F1F2EF", "middle", .22)
    arc = ('<g transform="translate(140,350)" stroke="#F4A6C0" stroke-width="1.4" fill="none"><path d="M0,0 H120"/><path d="M0,0 L119.8,-6.3"/></g>'
           + mono("3°", 268, 349, 12, PINK))
    return tile(bg + arc + main + cond + cap, "#17181a", label="Woven labels")

def hangtag(AR):
    back = ('<g transform="translate(545,430) rotate(8)"><rect x="-130" y="-220" width="260" height="440" rx="10" fill="#000" opacity=".3" filter="url(#sh)" transform="translate(0,14)"/>'
            '<rect x="-130" y="-220" width="260" height="440" rx="10" fill="#F6F7F5"/><circle cx="0" cy="-186" r="11" fill="#F4A6C0"/><circle cx="0" cy="-186" r="11" fill="#000" opacity=".18"/>'
            + mono("OFN—001", -104, -120, 22, INK, sp=.04, w=600) + mono("RUN TEE / COTTON", -104, -94, 11, INK, sp=.14)
            + '<path d="M-104,-76 H104" stroke="#151617" stroke-width="1.4"/>'
            + mono("MADE FOR", -104, -48, 10, MON, sp=.16) + mono("31°C / 84% RH", -104, -28, 14, INK, sp=.04, w=600)
            + mono("TESTED AT", -104, 6, 10, MON, sp=.16) + mono("05:30, KUALA LUMPUR", -104, 26, 14, INK, sp=.02, w=600)
            + mono("WILL IT GET HEAVY IN RAIN?", -104, 62, 10, MON, sp=.12) + mono("YES. SO WILL YOU.", -104, 82, 14, INK, sp=.02, w=600)
            + "".join(f'<rect x="{-104+i*7.4}" y="120" width="{(2,4,1.5,3,5,2,3)[i%7]}" height="46" fill="#151617"/>' for i in range(28))
            + mono("DESIGNED AT 3°N", -104, 192, 10, INK, sp=.16) + '</g>')
    front = ('<g transform="translate(270,400) rotate(-6)"><rect x="-130" y="-220" width="260" height="440" rx="10" fill="#000" opacity=".35" filter="url(#sh)" transform="translate(0,14)"/>'
             '<rect x="-130" y="-220" width="260" height="440" rx="10" fill="#17181a"/><circle cx="0" cy="-186" r="11" fill="#F4A6C0"/><circle cx="0" cy="-186" r="11" fill="#000" opacity=".25"/>'
             + use("stray", -66, -80, 132, "#F3F4F2", 1) + use("wm", -84, 150, 168, "#F3F4F2", AR["wm"]) + '</g>')
    string = '<path d="M290,214 C300,120 380,60 430,40 M519,246 C500,150 470,90 430,40" stroke="#151617" stroke-width="2.4" fill="none"/>'
    return tile(back + front + string, PINK, label="Hang tags")

def bib(AR):
    hl = f'<text class="hx" x="0" y="74" font-size="190" text-anchor="middle" fill="{INK}" textLength="500" lengthAdjust="spacingAndGlyphs">6:45</text>'
    holes = "".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#6f7779"/>' for x in (-266, 266) for y in (-112, 122))
    pin = lambda x, y, r: (f'<g transform="translate({x},{y}) rotate({r})" fill="none" stroke="#d9dcdc" stroke-width="3" stroke-linecap="round">'
                           '<path d="M-22,0 H18 a5,5 0 0 1 0,10 H-18"/><circle cx="-24" cy="5" r="5"/></g>')
    b = ('<g transform="translate(400,400) rotate(-2)"><rect x="-290" y="-204" width="580" height="408" rx="6" fill="#000" opacity=".35" filter="url(#sh)" transform="translate(0,14)"/>'
         '<rect x="-290" y="-204" width="580" height="408" rx="6" fill="#F6F7F5"/>'
         '<rect x="-290" y="-204" width="580" height="74" fill="#17181a"/>' + use("wm", -110, -183, 220, "#F3F4F2", AR["wm"])
         + hl + mono("MIN / KM. STILL COUNTS.", 0, 112, 15, INK, "middle", .2, 600)
         + f'<rect x="-290" y="140" width="580" height="64" fill="{PINK}"/>' + mono("OFF DAY CLUB", -230, 179, 15, INK, sp=.2, w=600)
         + mono("KUALA LUMPUR / 3°N", 226, 179, 15, INK, "end", .12)
         + holes + '</g>')
    return tile(b + pin(136, 296, -8) + pin(668, 278, 6) + pin(128, 530, 4) + pin(664, 512, -6), MON, label="Race bib")

def posters(AR):
    wall = ('<rect width="1624" height="800" fill="#9aa1a2" filter="url(#grainD)"/><rect y="700" width="1624" height="100" fill="#2a2c2d"/>'
            '<rect y="696" width="1624" height="8" fill="#000" opacity=".25"/>')
    def P(x, bg, inner, rot=0):
        return (f'<g transform="translate({x},112) rotate({rot})"><rect width="430" height="560" fill="#000" opacity=".4" filter="url(#sh)" transform="translate(0,10)"/>'
                f'<rect width="430" height="560" fill="{bg}"/>{inner}<rect width="430" height="560" fill="#000" opacity=".04" filter="url(#grainD)"/></g>')
    h1, y1 = block(["NO RUN IS", "PERFECT."], 40, 300, 350, "#F3F4F2")
    p1 = P(96, "#17181a", use("stray", 40, 56, 150, "#F3F4F2", 1) + h1 + use("wm", 40, 506, 130, "#F3F4F2", AR["wm"]) + mono("3°N", 390, 524, 12, "#F3F4F2", "end", .16), -1)
    h2, y2 = block(["6:45", "PACE.", "STILL", "COUNTS."], 40, 44, 350, INK)
    p2 = P(596, PINK, h2 + use("ofn", 40, 500, 86, INK, AR["ofn"]) + mono("OFF DAY CLUB / KL", 390, 524, 12, INK, "end", .16), 1)
    h3, y3 = block(["OFF DAY?", "RUN", "ANYWAY."], 40, 44, 350, INK)
    p3 = P(1096, "#F6F7F5", h3 + mono("WALKED THE LAST 2K.", 40, y3 + 34, 13, INK, sp=.14) + mono("LISTED AS A RUN.", 40, y3 + 54, 13, INK, sp=.14)
           + use("wm", 40, 506, 130, INK, AR["wm"]) + use("stray", 350, 488, 44, INK, 1), -0.6)
    return tile(wall + p1 + p2 + p3, "#9aa1a2", 1624, 800, "Street posters")

def mailer(AR):
    tape_txt = "".join(mono("NO RUN IS PERFECT.", -330 + i * 200, 5, 12, INK, sp=.18, w=600) for i in range(5))
    m = ('<g transform="translate(400,410) rotate(3)"><rect x="-240" y="-300" width="480" height="600" rx="8" fill="#000" opacity=".35" filter="url(#sh)" transform="translate(0,16)"/>'
         '<rect x="-240" y="-300" width="480" height="600" rx="8" fill="#17181a"/><rect x="-240" y="-300" width="480" height="600" rx="8" fill="#17181a" filter="url(#grainL)" opacity=".5"/>'
         '<path d="M-240,-214 H240" stroke="#000" stroke-width="3" opacity=".7"/><path d="M-240,-211 H240" stroke="#fff" stroke-width="1" opacity=".12"/>'
         '<path d="M-200,-300 C-180,-100 -210,100 -190,300" stroke="#fff" stroke-opacity=".05" stroke-width="40" fill="none" filter="url(#blur)"/>'
         + use("wm", -190, -90, 380, "#F3F4F2", AR["wm"])
         + mono("RUNNING GOODS FOR THE OFF DAYS", 0, 20, 12, "#F3F4F2", "middle", .22)
         + '<g transform="translate(60,170) rotate(-3)"><rect x="-130" y="-60" width="260" height="120" fill="#F6F7F5"/>'
         + use("stray", -116, -46, 30, INK, 1) + mono("TO: OFF DAY CLUB, MEMBER 0001", -116, 4, 10.5, INK, sp=.1, w=600)
         + mono("FROM: OFFNORM, KUALA LUMPUR", -116, 22, 10.5, INK, sp=.1) + mono("CONTENTS: OFN—001", -116, 40, 10.5, INK, sp=.1) + '</g>'
         + f'<g clip-path="url(#mclip)"><g transform="translate(0,-214) rotate(-3)"><rect x="-330" y="-13" width="660" height="26" fill="{PINK}"/>{tape_txt}</g></g></g>')
    return tile(m, HAZE, label="Mailer bag")
