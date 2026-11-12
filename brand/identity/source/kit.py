"""OFFNORM letter kit. Every letter is drawn as geometry (no font).
Cap height 100, y down. Each glyph returns (path_d, advance_width)."""
S = 27    # vertical stem
T = 24    # horizontal bar
WAIST = 46  # top of the low bar (normal would be ~39)

def rrect(x, y, w, h, r, cw=True):
    r = max(0, min(r, w / 2, h / 2))
    if cw:
        return (f"M{x+r},{y}H{x+w-r}A{r},{r} 0 0 1 {x+w},{y+r}V{y+h-r}A{r},{r} 0 0 1 {x+w-r},{y+h}"
                f"H{x+r}A{r},{r} 0 0 1 {x},{y+h-r}V{y+r}A{r},{r} 0 0 1 {x+r},{y}Z")
    return (f"M{x+r},{y}A{r},{r} 0 0 0 {x},{y+r}V{y+h-r}A{r},{r} 0 0 0 {x+r},{y+h}H{x+w-r}"
            f"A{r},{r} 0 0 0 {x+w},{y+h-r}V{y+r}A{r},{r} 0 0 0 {x+w-r},{y}Z")

def poly(pts):
    return "M" + "L".join(f"{round(x,2)},{round(y,2)}" for x, y in pts) + "Z"

def O(w=146, r=50):
    return rrect(0, 0, w, 100, r) + rrect(S, T, w - 2 * S, 100 - 2 * T, max(r - S + 3, 6), cw=False), w

def F(w=98, mid=80):
    m = WAIST
    return poly([(0, 0), (w, 0), (w, T), (S, T), (S, m), (mid, m), (mid, m + T), (S, m + T), (S, 100), (0, 100)]), w

def N(w=126, D=41):
    y1 = 100 * (w - S - D) / (w - D)
    y2 = 100 * S / (w - D)
    return poly([(0, 100), (0, 0), (D, 0), (w - S, y1), (w - S, 0), (w, 0), (w, 100), (w - D, 100), (S, y2), (S, 100)]), w

def M(w=164, D=43, A=14):
    half = w / 2
    slope = 100 / (half - A / 2)
    yT = slope * (half - D)
    yL = slope * S
    return poly([(0, 100), (0, 0), (D, 0), (half, yT), (w - D, 0), (w, 0), (w, 100), (w - S, 100), (w - S, yL),
                 (half + A / 2, 100), (half - A / 2, 100), (S, yL), (S, 100)]), w

def R(w=124, B=None, Dl=41, kick=4):
    B = B or WAIST + T  # bowl bottom lines up with the F bar
    rb = B / 2
    outer = f"M0,0H{w-rb}A{rb},{rb} 0 0 1 {w-rb},{B}H{S}V100H0Z"
    ch = B - 2 * T
    inner = rrect(S, T, w - 2 * S + 2, ch, ch / 2, cw=False)
    lx = w - rb - Dl + 2
    leg = poly([(lx, B - 1), (lx + Dl, B - 1), (w + kick, 100), (w + kick - Dl, 100)])
    return outer + inner + leg, w + kick

GLYPH = {"O": O, "F": F, "N": N, "M": M, "R": R}
# pair spacing (default gap, then exceptions)
GAP = 13
KERN = {("O", "F"): 11, ("F", "F"): 9, ("F", "N"): 8, ("N", "O"): 11, ("O", "R"): 11, ("R", "M"): 9, ("F", "O"): 5}

def word(text, gap=GAP, **kw):
    """Returns (list of (d, x)), total width."""
    x = 0
    out = []
    prev = None
    for ch in text:
        if prev:
            x += KERN.get((prev, ch), gap) if gap == GAP else gap
        d, w = GLYPH[ch](**kw.get(ch, {}))
        out.append((d, x))
        x += w
        prev = ch
    return out, x

def word_svg(text, fill="currentColor", **kw):
    parts, w = word(text, **kw)
    g = "".join(f'<path transform="translate({round(x,2)},0)" d="{d}"/>' for d, x in parts)
    return f'<g fill="{fill}" fill-rule="nonzero">{g}</g>', w

def reg(x, y, r=9, fill="currentColor"):
    """Registered mark drawn as geometry: ring + small R."""
    sw = r * 0.2
    k = r * 0.011
    rd, _ = R()
    return (f'<g fill="{fill}"><path fill-rule="evenodd" d="M{x-r},{y}a{r},{r} 0 1 0 {2*r},0a{r},{r} 0 1 0 {-2*r},0Z'
            f'M{x-r+sw},{y}a{r-sw},{r-sw} 0 1 1 {2*(r-sw)},0a{r-sw},{r-sw} 0 1 1 {-2*(r-sw)},0Z"/>'
            f'<path transform="translate({x-62*k},{y-50*k}) scale({k})" d="{rd}"/></g>')

def stray(cell=40, dot=14, off=0.55, fill="currentColor"):
    """The Stray: nine dots, one off the grid. Returns (svg, size)."""
    c = []
    for row in range(3):
        for col in range(3):
            cx, cy = col * cell, row * cell
            if row == 0 and col == 2:
                cx += cell * off
                cy -= cell * off
            c.append(f'<circle cx="{cx}" cy="{cy}" r="{dot}"/>')
    return f'<g fill="{fill}">' + "".join(c) + "</g>", 2 * cell


# ---------- O variants: the O carries the identity. Each returns an svg fragment, width 146, height 100.
import math
OW = 146
_OUT = rrect(0, 0, OW, 100, 50)

def _pill_points(n, x=13.5, y=12, w=119, h=76):
    """n points evenly spaced along a pill centre line."""
    r = h / 2; straight = w - 2 * r; per = 2 * straight + 2 * math.pi * r
    pts = []
    for i in range(n):
        d = per * i / n
        if d < straight: pts.append((x + r + d, y))
        elif d < straight + math.pi * r:
            a = (d - straight) / r - math.pi / 2; pts.append((x + w - r + r * math.cos(a), y + r + r * math.sin(a)))
        elif d < 2 * straight + math.pi * r: pts.append((x + w - r - (d - straight - math.pi * r), y + h))
        else:
            a = (d - 2 * straight - math.pi * r) / r + math.pi / 2; pts.append((x + r + r * math.cos(a), y + r + r * math.sin(a)))
    return pts

def o_plain():
    return f'<path d="{O()[0]}"/>'
def o_switch():   # a toggle set to off: the knob sits at the left
    return f'<path d="{_OUT}{rrect(S, T, OW-2*S, 100-2*T, 26, cw=False)}"/><circle cx="{S+26}" cy="50" r="15.5"/>'
def o_hole():     # solid pill, round counter pushed to one side
    return f'<path d="{_OUT}M77,50a27,27 0 1 0 -54,0a27,27 0 1 0 54,0Z"/>'
def o_shift():    # counter knocked off centre
    return f'<path d="{_OUT}{rrect(S+12, T-9, OW-2*S, 100-2*T, 26, cw=False)}"/>'
def o_slip(dx=18):  # cut on the low-bar line, lower half slips
    c = WAIST + T / 2 - 4
    top = (f"M0,{c}V50A50,50 0 0 1 50,0H96A50,50 0 0 1 146,50V{c}Z"
           f"M119,{c}V50A26,26 0 0 0 93,24H53A26,26 0 0 0 27,50V{c}Z")
    bot = (f"M0,{c}H146V50A50,50 0 0 1 96,100H50A50,50 0 0 1 0,50Z"
           f"M27,{c}V50A26,26 0 0 0 53,76H93A26,26 0 0 0 119,50V{c}Z")
    return f'<path d="{top}"/><path transform="translate({dx},0)" d="{bot}"/>'
def o_exit():     # the track with a way out
    d = rrect(13, 12.5, 120, 75, 37.5)
    return (f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="25" pathLength="100" stroke-dasharray="8.5 5.5 86"/>')
def o_lanes():    # two lanes of a track
    return (f'<path d="{rrect(4.5,4.5,137,91,45.5)}" fill="none" stroke="currentColor" stroke-width="9"/>'
            f'<path d="{rrect(22.5,22.5,101,55,27.5)}" fill="none" stroke="currentColor" stroke-width="9"/>')
def o_dots(n=14, r=9.2, off=3):
    out = ""
    for i, (x, y) in enumerate(_pill_points(n)):
        if i == off: x += 15; y -= 15
        out += f'<circle cx="{round(x,1)}" cy="{round(y,1)}" r="{r}"/>'
    return out
OVAR = {"plain": o_plain, "switch": o_switch, "hole": o_hole, "shift": o_shift, "slip": o_slip, "exit": o_exit, "lanes": o_lanes, "dots": o_dots}

def word2(text, first="plain", rest="plain", fill="currentColor"):
    """Word where the first O uses one variant and later O's another. Returns (svg, width)."""
    x = 0; out = []; prev = None; seen = 0
    for ch in text:
        if prev: x += KERN.get((prev, ch), GAP)
        if ch == "O":
            frag = OVAR[first if seen == 0 else rest](); seen += 1; w = OW
            out.append(f'<g transform="translate({round(x,2)},0)">{frag}</g>')
        else:
            d, w = GLYPH[ch](); out.append(f'<path transform="translate({round(x,2)},0)" d="{d}"/>')
        x += w; prev = ch
    return f'<g fill="{fill}">' + "".join(out) + "</g>", x


# ---------- Round 3 O's: the founder's own sketches (mirrored F, triangle, interlocked FF, italic) mixed with the pill O.
def _rtri(pts, t=0.22):
    """Rounded triangle path through three points (corner rounding t)."""
    d = ""
    n = len(pts)
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        a = (p1[0] + (p0[0] - p1[0]) * t, p1[1] + (p0[1] - p1[1]) * t)
        b = (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
        d += ("M" if i == 0 else "L") + f"{a[0]:.1f},{a[1]:.1f}Q{p1[0]},{p1[1]} {b[0]:.1f},{b[1]:.1f}"
    return d + "Z"
def o_hook(dy=9):     # two halves that do not line up, after the interlocked FF block
    l = "M73,0H50A50,50 0 0 0 50,100H73ZM73,24H53A26,26 0 0 0 53,76H73Z"
    r = "M73,0H96A50,50 0 0 1 96,100H73ZM73,24H93A26,26 0 0 1 93,76H73Z"
    return f'<path fill-rule="evenodd" transform="translate(0,{-dy})" d="{l}"/><path fill-rule="evenodd" transform="translate(0,{dy})" d="{r}"/>'
def o_peak():         # the triangle from the founder's sketch becomes the hole of the O
    return f'<path fill-rule="evenodd" d="{_OUT}{_rtri([(73,14),(118,80),(28,80)])}"/>'
def o_lean():         # leaning forward, after the italic sketches
    return f'<g transform="translate(11,0) skewX(-13)"><path d="{O()[0]}"/></g>'
def o_bar():          # the low bar of the F runs through the O
    return f'<path d="{_OUT}{rrect(S, T, OW-2*S, WAIST-T, 11, cw=False)}{rrect(S, WAIST+13, OW-2*S, 100-T-WAIST-13, 8.5, cw=False)}"/>'
def o_block():        # the squarer O drawn in the sketches
    return f'<path d="{O(r=30)[0]}"/>'
def o_mirror():       # one half solid, one half open: half of it is off
    return (f'<path fill-rule="evenodd" d="M73,0H50A50,50 0 0 0 50,100H73Z"/>'
            f'<path fill-rule="evenodd" d="M73,0H96A50,50 0 0 1 96,100H73ZM73,24H93A26,26 0 0 1 93,76H73Z"/>')
OVAR.update({"hook": o_hook, "peak": o_peak, "lean": o_lean, "bar": o_bar, "block": o_block, "mirror": o_mirror})

def f_mirror(x=0):
    d, w = F()
    return f'<path transform="translate({x + w},0) scale(-1,1)" d="{d}"/>', w
def f_flip(x=0, y=0):
    d, w = F()
    return f'<path transform="translate({x + w},{y + 100}) scale(-1,-1)" d="{d}"/>', w
