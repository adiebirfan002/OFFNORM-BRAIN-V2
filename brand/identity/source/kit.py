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
