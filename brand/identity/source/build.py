"""Builds the OFFNORM identity: SVG marks in ../svg and the proposal page ../proposal.html
Run from the repo root:  python3 brand/identity/source/build.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from kit import *
import mocks
OUT = os.path.dirname(HERE)
INK, HAZE, MON, PINK = mocks.INK, mocks.HAZE, mocks.MON, mocks.PINK

# ---------- marks (each: inner svg using currentColor / var(--ko), viewBox w, h)
def m_wm(regmark=True):
    s, w = word_svg("OFFNORM")
    return (s + (reg(w + 16, 11, 10) if regmark else ""), w + (28 if regmark else 0), 100)
def m_ofn():
    s, w = word_svg("OFN"); return s + reg(w + 16, 11, 10), w + 28, 100
def m_off():
    s, w = word_svg("OFF"); return s, w, 100
def m_stray():
    s, _ = stray(); return f'<g transform="translate(14,36)">{s}</g>', 130, 130
def m_badge():
    s, w = word_svg("OFN", fill="var(--ko,#fff)"); k = 0.66
    W, H = w * k + 120, 100 * k + 64
    return (f'<rect width="{W}" height="{H}" rx="{H/2}" fill="currentColor"/><g transform="translate(60,32) scale({k})">{s}</g>', W, H)
def m_stack():
    a, wa = word_svg("OFF"); b, wb = word_svg("NORM"); k = wb / wa
    return (f'<g transform="scale({k})">{a}</g><g transform="translate(0,{100*k+20})">{b}</g>' + reg(wb + 16, 11, 10), wb + 28, 100 * k + 120)
def m_lockh():
    s, _ = stray(); w, ww = word_svg("OFFNORM")
    return (f'<g transform="translate(11,28) scale(0.77)">{s}</g><g transform="translate(142,0)">{w}</g>' + reg(142 + ww + 16, 11, 10), 142 + ww + 28, 100)
def m_lockv():
    s, _ = stray(); w, ww = word_svg("OFN")
    return (f'<g transform="translate({ww/2-56},50) scale(1.4)">{s}</g><g transform="translate(0,250)">{w}</g>' + reg(ww + 16, 261, 10), ww + 28, 350)
def m_icon():
    s, _ = stray()
    return f'<rect width="200" height="200" rx="44" fill="currentColor"/><g transform="translate(49,71)" style="color:var(--ko,#fff)">{s}</g>', 200, 200

MARKS = {"wm": m_wm(), "wm0": m_wm(False), "ofn": m_ofn(), "off": m_off(), "stray": m_stray(), "badge": m_badge(),
         "stack": m_stack(), "lockh": m_lockh(), "lockv": m_lockv(), "icon": m_icon()}
AR = {k: v[1] / v[2] for k, v in MARKS.items()}
FILES = {"wm": "wordmark", "ofn": "monogram-OFN", "stray": "symbol-stray", "badge": "badge", "stack": "stacked",
         "lockh": "lockup-horizontal", "lockv": "lockup-vertical", "icon": "app-icon"}
os.makedirs(f"{OUT}/svg", exist_ok=True)
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
fd, fw = F(); rd, rw = R(); od, ow = O()
constr = f'''<svg viewBox="-40 -30 560 160" class="diagram" role="img" aria-label="The low bar on F and R">
<g fill="{INK}"><path d="{fd}"/><path transform="translate(130,0)" d="{rd}"/><path transform="translate(290,0)" d="{od}"/></g>
<g stroke="{PINK}" stroke-width="1.6"><path d="M-30,50 H460" stroke-dasharray="5 5"/><path d="M-30,58 H270"/></g>
<text class="mn" x="466" y="54" font-size="11" fill="{INK}">centre</text>
</svg>'''
tilt = f'''<svg viewBox="0 0 520 190" class="diagram" role="img" aria-label="Labels sit 3 degrees off level">
<path d="M40,150 H480" stroke="{INK}" stroke-width="1.2" stroke-dasharray="5 5"/>
<g transform="translate(260,96) rotate(-3)"><rect x="-150" y="-44" width="300" height="88" fill="{INK}"/>
<svg x="-110" y="-16" width="220" height="{220/AR['wm']}" viewBox="0 0 {MARKS['wm'][1]} 100" style="color:#F3F4F2"><use href="#wm"/></svg></g>
<path d="M40,150 L479.4,127" stroke="{PINK}" stroke-width="1.6"/><text class="mn" x="486" y="134" font-size="12" fill="{INK}">3°</text></svg>'''
pattern = "".join(f'<circle cx="{20+c*26 + (9 if (r,c) in ((1,5),(3,13),(4,2),(0,20),(5,24),(2,17)) else 0)}" cy="{20+r*26 - (9 if (r,c) in ((1,5),(3,13),(4,2),(0,20),(5,24),(2,17)) else 0)}" r="5.4" fill="{"#F4A6C0" if (r,c) in ((1,5),(3,13),(4,2),(0,20),(5,24),(2,17)) else "#F3F4F2"}"/>' for r in range(7) for c in range(30))

M = mocks
tiles = [("Run tee, front", "OFN on the chest, product number under it, pink tab at the hem", M.tee_front(AR), ""),
         ("Run tee, back", "The Stray, the belief line, and the conditions it was made for", M.tee_back(AR), ""),
         ("Singlet", "The vent holes are the symbol: a grid with one hole off", M.singlet(AR), ""),
         ("Cap", "OFN embroidered, pink under the brim", M.cap(AR), ""),
         ("Shorts", "Small Stray at the hem, tab on the waistband", M.shorts(AR), ""),
         ("Socks", "One mark per sock, pink band", M.socks(AR), ""),
         ("Street posters", "Black, pink and white. The copy does the shouting, the logo stays small", M.posters(AR), "wide"),
         ("Labels", "Wordmark label and conditions label, both sewn 3° off level", M.labels(AR), ""),
         ("Hang tags", "Front carries the symbol, back carries the conditions and one honest answer", M.hangtag(AR), ""),
         ("Race bib", "For Off Day Club runs. Your pace is the number", M.bib(AR), ""),
         ("Mailer", "Wordmark, address label, belief-line tape", M.mailer(AR), "")]
mock_html = "".join(f'<figure class="mock {c}">{svg}<figcaption><b>{t}</b><span>{n}</span></figcaption></figure>' for t, n, svg, c in tiles)

PAGE = open(f"{HERE}/page.html").read()
html = (PAGE.replace("{{DEFS}}", DEFS).replace("{{HERO}}", mark("wm", "#F3F4F2", INK, "hero-mark"))
        .replace("{{P_WM}}", plate("wm", "Wordmark", "Neck label, site header, packaging, back print", cls="span2", size="w80"))
        .replace("{{P_OFN}}", plate("ofn", "Monogram", "The registered short mark. Chest, cap, sock", size="w60"))
        .replace("{{P_STRAY}}", plate("stray", "Symbol: the Stray", "Nine dots, one off. Avatar, vent grid, pattern", size="h60"))
        .replace("{{P_BADGE}}", plate("badge", "Badge", "Patches, stickers, zip pulls", True, size="w60"))
        .replace("{{P_STACK}}", plate("stack", "Stacked", "Square spaces. Off is always the bigger word", True, size="h70"))
        .replace("{{P_LOCKH}}", plate("lockh", "Horizontal lockup", "Symbol with wordmark, for headers and signage", cls="span2", size="w80"))
        .replace("{{P_LOCKV}}", plate("lockv", "Vertical lockup", "Centre chest, hang tag, swing ticket", size="h70"))
        .replace("{{P_ICON}}", plate("icon", "App icon and avatar", "Instagram, Strava club, favicon", size="h50"))
        .replace("{{P_PINK}}", f'<figure class="plate pink"><div class="stage">{mark("ofn", INK, "#fff", "w60")}</div><figcaption><b>On Bandung pink</b><span>The one accent. Black marks only</span></figcaption></figure>')
        .replace("{{CONSTR}}", constr).replace("{{TILT}}", tilt).replace("{{PATTERN}}", pattern)
        .replace("{{SIZES}}", "".join(f'<div>{mark("wm", px=w)}<span>{w}px</span></div>' for w in (240, 120, 64)) + "".join(f'<div>{mark("stray", px=w)}<span>{w}px</span></div>' for w in (48, 24, 16)))
        .replace("{{MOCKS}}", mock_html))
open(f"{OUT}/proposal.html", "w").write(html)
print("ok", {k: round(v, 2) for k, v in AR.items()})
