"""Builds the OFFNORM identity: SVG marks in ../svg and the proposal page ../proposal.html
Run from the repo root:  python3 brand/identity/source/build.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kit import *
import mocks, mocks2
OUT = os.path.dirname(HERE)
INK, HAZE, MON, PINK = mocks.INK, mocks.HAZE, mocks.MON, mocks.PINK
YEL = mocks2.YEL

# ---------- marks (each: inner svg using currentColor / var(--ko), viewBox w, h)
PICK = "switch"   # the O the founder is being recommended
KO = "var(--ko,#fff)"
def m_wm(v=PICK, regmark=True):
    s, w = word2("OFFNORM", v)
    return (s + (reg(w + 16, 11, 10) if regmark else ""), w + (28 if regmark else 0), 100)
def m_ofn():
    s, w = word2("OFN", PICK); return s + reg(w + 16, 11, 10), w + 28, 100
def m_osw(v=PICK):
    return f'<g fill="currentColor">{OVAR[v]()}</g>', OW, 100
def e_switch(text):
    """The switch badge: a toggle set to off. The knob is the O, the rest of the letters ride in the track."""
    parts, wl = word(text); k = 0.6; H = 120; x0 = 60 + 42 + 24
    W = x0 + wl * k + 44
    letters = "".join(f'<path transform="translate({round(x,2)},0)" d="{d}"/>' for d, x in parts)
    return (f'<rect width="{W}" height="{H}" rx="{H/2}" fill="currentColor"/><circle cx="60" cy="60" r="42" fill="{KO}"/>'
            f'<circle cx="60" cy="60" r="16" fill="currentColor"/><g transform="translate({x0},30) scale({k})" fill="{KO}">{letters}</g>', W, H)
def e_quad():
    k = 0.6
    def cell(frag, w, cx, cy): return f'<g transform="translate({cx - w*k/2},{cy - 30}) scale({k})">{frag}</g>'
    g = (cell(OVAR[PICK](), OW, 92, 96) + cell(f'<path d="{F()[0]}"/>', F()[1], 208, 96)
         + cell(f'<path d="{N()[0]}"/>', N()[1], 92, 204) + cell(f'<path d="{M()[0]}"/>', M()[1], 208, 204))
    return f'<rect width="300" height="300" rx="58" fill="currentColor"/><g fill="{KO}">{g}</g>', 300, 300
def e_row(text="OFN"):
    x = 0; out = ""
    for ch in text:
        if ch == "O": out += f'<g transform="translate({x},0)">{OVAR[PICK]()}</g>'; x += OW + 70
        else:
            d, w = GLYPH[ch](); out += f'<path transform="translate({x},0)" d="{d}"/>'; x += w + 70
    return f'<g fill="currentColor">{out}</g>', x - 70, 100
def e_plate():
    s, w = word2("OFN", PICK); k = 0.8
    return (f'<rect x="6" y="6" width="428" height="268" rx="44" fill="none" stroke="currentColor" stroke-width="12"/>'
            f'<g transform="translate({220 - w*k/2},44) scale({k})">{s}</g><rect x="44" y="150" width="352" height="8" fill="currentColor"/>'
            f'<text class="hx" x="220" y="198" font-size="25" text-anchor="middle" fill="currentColor" textLength="352" lengthAdjust="spacingAndGlyphs">OFFNORM RUNNING</text>'
            f'<text class="hx" x="220" y="236" font-size="25" text-anchor="middle" fill="currentColor" textLength="352" lengthAdjust="spacingAndGlyphs">KUALA LUMPUR 3°N</text>', 440, 280)
def m_icon():
    return f'<rect width="200" height="200" rx="44" fill="currentColor"/><g transform="translate(34,59) scale(0.9)" fill="{KO}" style="color:{KO}">{OVAR[PICK]()}</g>', 200, 200

MARKS = {"wm": m_wm(), "ofn": m_ofn(), "osw": m_osw(), "e_sw": e_switch("FN"), "e_sw4": e_switch("FNM"), "e_quad": e_quad(),
         "e_row": e_row(), "e_plate": e_plate(), "icon": m_icon()}
for v in OVAR:
    if v != "plain": MARKS["wm_" + v] = m_wm(v, False); MARKS["o_" + v] = m_osw(v)
AR = {k: v[1] / v[2] for k, v in MARKS.items()}
FILES = {"wm": "wordmark", "ofn": "monogram-OFN", "osw": "symbol-O", "e_sw": "emblem-switch-OFN", "e_sw4": "emblem-switch-OFNM",
         "e_quad": "emblem-quad-OFNM", "e_row": "emblem-row-OFN", "e_plate": "emblem-plate-OFN", "icon": "app-icon"}
FILES.update({"wm_" + v: "options/wordmark-O-" + v for v in OVAR if v != "plain"})
import shutil; shutil.rmtree(f"{OUT}/svg", ignore_errors=True)
os.makedirs(f"{OUT}/svg/options", exist_ok=True)
for k, name in FILES.items():
    s, w, h = MARKS[k]
    for tone, fg, ko, bg in (("black", INK, "#FFFFFF", None), ("white", "#FFFFFF", INK, INK)):
        body = s.replace("currentColor", fg).replace("var(--ko,#fff)", ko)
        pad = 40 if bg else 0
        rect = f'<rect x="{-pad}" y="{-pad}" width="{w+2*pad}" height="{h+2*pad}" fill="{bg}"/>' if bg else ""
        open(f"{OUT}/svg/{name}-{tone}.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {round(w+2*pad,2)} {round(h+2*pad,2)}">{rect}{body}</svg>\n')

symbols = "".join(f'<symbol id="{k}" viewBox="0 0 {round(w,2)} {round(h,2)}">{s}</symbol>' for k, (s, w, h) in MARKS.items())
DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{symbols}
<radialGradient id="vig" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></radialGradient>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="13"/></filter>
<filter id="emb" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="1.6" stdDeviation=".8" flood-color="#000" flood-opacity=".5"/></filter>
<filter id="grainL" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  .2 0 0 0 -.07" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
<filter id="grainD" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  .3 0 0 0 -.1" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in" result="g"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g"/></feMerge></filter>
<filter id="weave" x="0" y="0" width="100%" height="100%"><feTurbulence type="turbulence" baseFrequency="0.9 0.08" numOctaves="1" seed="2"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  .5 0 0 0 -.12" result="n"/><feComposite in="n" in2="SourceAlpha" operator="in"/></filter>
<clipPath id="mclip"><rect x="-240" y="-300" width="480" height="600" rx="8"/></clipPath>
</defs></svg>'''

def mark(k, color=INK, ko="#fff", cls="", px=None):
    s, w, h = MARKS[k]
    wpx = f";width:{px}px" if px else ""
    return f'<svg class="mk {cls}" viewBox="0 0 {round(w,2)} {round(h,2)}" style="color:{color};--ko:{ko}{wpx}" aria-hidden="true"><use href="#{k}"/></svg>'

def plate(k, title, note, dark=False, cls="", size=""):
    bg = "dark" if dark else ""
    return (f'<figure class="plate {bg} {cls}"><div class="stage">{mark(k, "#F3F4F2" if dark else INK, INK if dark else "#fff", size)}</div>'
            f'<figcaption><b>{title}</b><span>{note}</span></figcaption></figure>')

# construction diagram: low waist
fd, fw = F(); rd, rw = R()
constr = f'''<svg viewBox="-40 -30 560 160" class="diagram" role="img" aria-label="The low bar on F and R">
<g fill="{INK}"><path d="{fd}"/><path transform="translate(130,0)" d="{rd}"/><g transform="translate(290,0)">{OVAR[PICK]()}</g></g>
<g stroke="{YEL}" stroke-width="2"><path d="M-30,50 H460" stroke-dasharray="5 5"/><path d="M-30,58 H270"/></g>
<text class="mn" x="466" y="54" font-size="11" fill="{INK}">centre</text></svg>'''
tilt = f'''<svg viewBox="0 0 520 190" class="diagram" role="img" aria-label="Labels sit 3 degrees off level">
<path d="M40,150 H480" stroke="{INK}" stroke-width="1.2" stroke-dasharray="5 5"/>
<g transform="translate(260,96) rotate(-3)"><rect x="-150" y="-44" width="300" height="88" fill="{INK}"/>
<svg x="-110" y="-16" width="220" height="{220/AR['wm']}" viewBox="0 0 {MARKS['wm'][1]} 100" style="color:#F3F4F2"><use href="#wm"/></svg></g>
<path d="M40,150 L479.4,127" stroke="{YEL}" stroke-width="2"/><text class="mn" x="486" y="134" font-size="12" fill="{INK}">3°</text></svg>'''

ONOTES = [("switch", "O1 Switch", "A toggle set to off. Norm: off. Reads as an O and as a switch", True),
          ("shift", "O2 Shift", "The counter is knocked off centre. The quietest option", False),
          ("slip", "O3 Slip", "Cut on the low-bar line, the lower half slips forward", False),
          ("hole", "O4 Solid", "A solid pill with the hole pushed to one side. The heaviest", False),
          ("exit", "O5 Exit", "A running track with a way out. Risk: can read as a C", False),
          ("lanes", "O6 Lanes", "Two lanes of a track. Lighter than the other letters", False),
          ("dots", "O7 Dots", "Reflective dots, one off. Best as a print, weak as a logo", False)]
oplates = "".join(
    f'<figure class="plate opt {"pick" if pk else ""}"><div class="stage">{mark("o_"+v, INK, "#fff", "osolo")}{mark("wm_"+v, INK, "#fff", "w90")}</div>'
    f'<figcaption><b>{t}{" · recommended" if pk else ""}</b><span>{n}</span></figcaption></figure>' for v, t, n, pk in ONOTES)

M = mocks2
tiles = [("Panel tee, front", "Switch badge on the chest, contrast seams, a line of copy on each shoulder", M.tee_front(AR), ""),
         ("Panel tee, back", "The O drawn in reflective dots, one dot off, with the run name inside", M.tee_back(AR), ""),
         ("Chest mark close-up", "How the badge sits against the seam", M.detail(AR), ""),
         ("Cap", "Two-tone five-panel, the O alone on the side", M.cap(AR), ""),
         ("Shorts", "Spaced letters at the hem, one contrast seam", M.shorts(AR), ""),
         ("Labels", "Wordmark label and conditions label, both sewn 3° off level", M.labels(AR), ""),
         ("Street posters", "The copy does the shouting, the logo stays small", M.posters(AR), "wide"),
         ("Hang tags", "Front carries the O, back carries the conditions and one honest answer", M.hangtag(AR), "")]
mock_html = "".join(f'<figure class="mock {c}">{svg}<figcaption><b>{t}</b><span>{n}</span></figcaption></figure>' for t, n, svg, c in tiles)

PAGE = open(f"{HERE}/page.html").read()
R_ = {"DEFS": DEFS, "HERO": mark("wm", "#F3F4F2", INK, "hero-mark"), "OPLATES": oplates,
      "IDEA": mark("osw", INK, "#fff", "idea-sym"),
      "E_SW": plate("e_sw", "E1 Switch badge, OFN · recommended", "The knob is the O. One shape, like the ACG triangle", cls="pick", size="w60"),
      "E_SW4": plate("e_sw4", "E2 Switch badge, OFNM", "Same idea with four letters", size="w70"),
      "E_QUAD": plate("e_quad", "E3 Quad, OFNM", "Four letters in a square block", True, size="h60"),
      "E_ROW": plate("e_row", "E4 Spaced letters", "The FPA way: small, wide apart, no box", size="w60"),
      "E_PLATE": plate("e_plate", "E5 Plate", "Letters over the full name, the way ACG spells itself out", size="h70"),
      "P_WM": plate("wm", "Wordmark", "The O in OFF is off. The O in NORM is normal", cls="span2", size="w80"),
      "P_OSW": plate("osw", "Symbol", "The O alone: cap, sock, zip pull", size="w50"),
      "P_BADGE": plate("e_sw", "Badge", "OFN in the switch. Chest, patch, hang tag", True, size="w60"),
      "P_ICON": plate("icon", "App icon", "Instagram, Strava club, favicon", size="h50"),
      "P_DARK": plate("e_sw", "Reversed", "White on Tarmac", True, size="w60"),
      "P_YEL": f'<figure class="plate pink"><div class="stage">{mark("e_sw", INK, YEL, "w60")}</div><figcaption><b>On Kunyit</b><span>The seam colour from your reference</span></figcaption></figure>',
      "CONSTR": constr, "TILT": tilt, "MOCKS": mock_html}
html = PAGE
for k, v in R_.items(): html = html.replace("{{" + k + "}}", v)
open(f"{OUT}/proposal.html", "w").write(html)
print("ok", [k for k in R_ if "{{" + k + "}}" not in PAGE])
