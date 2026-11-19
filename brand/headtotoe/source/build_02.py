"""Head to toe, set 02: seven more colourways with the full set and the long sleeve.
Run from the repo root:  python3 brand/headtotoe/source/build_02.py  -> brand/headtotoe/head-to-toe-02.html"""
import os, io, re, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
def load(name, f):
    sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, f)); m = importlib.util.module_from_spec(sp)
    with contextlib.redirect_stdout(io.StringIO()): sp.loader.exec_module(m)
    return m
H = load("h2t", "build.py"); LSM = load("ls", "build_ls.py"); G = H.G; K = H.K
KL = "3.1390°N  101.6869°E"
KITS = [
 K("JTZ", "Jubin Terazo", "Terrazzo pink-grey with rust-red flecks. Era 80an.", KL, ("31°C / 75% RH", "17:30"),
   [("Terazo", "#C7B3A8", "Main"), ("Simen", "#EFE7E0", "Sub"), ("Serpih", "#A0523D", "Pop"), ("Batu", "#6E5E57", "Deep"), ("Pucat", "#F8F4F0", "Light")],
   "#A0523D", ("#C7B3A8", "#EFE7E0", "#A0523D", "#6E5E57", "#6E5E57"), "#EFE7E0", None, "#6E5E57", "#A0523D",
   ["Rust flecks at both ends: beanie and socks in Serpih.", "The softest top of the set: terrazzo body, cement-white panel, thin rust seams, stone-grey print.", "Batu stone-grey tights ground the pale top."]),
 K("PGW", "Panggung Wayang", "Old cinema velvet, gold marquee letters, cream ticket. Era 80an.", "3.1424°N  101.6970°E", ("28°C / 82% RH", "20:45"),
   [("Baldu", "#6E2232", "Main"), ("Tiket", "#E7D3B0", "Sub"), ("Emas", "#C9A04E", "Pop"), ("Gelap", "#3E1219", "Deep"), ("Skrin", "#F6EEDF", "Light")],
   "#C9A04E", ("#6E2232", "#E7D3B0", "#C9A04E", "#C9A04E", "#F6EEDF"), "#E7D3B0", None, "#3E1219", "#C9A04E",
   ["Gold marquee at both ends.", "Velvet-red top with a ticket-cream panel; the chest symbol is gold, like the letters over the cinema door.", "Dark velvet tights, almost black."]),
 K("SRG", "Seragam Sekolah", "The white shirt, the navy shorts and a maroon badge. Era 90an.", KL, ("30°C / 78% RH", "07:15"),
   [("Kemeja", "#F1EDE3", "Main"), ("Kelabu", "#B9C2CF", "Sub"), ("Lencana", "#8A2E2E", "Pop"), ("Seluar", "#2F3D5C", "Deep"), ("Putih", "#FBF8F1", "Light")],
   "#8A2E2E", ("#F1EDE3", "#B9C2CF", "#8A2E2E", "#8A2E2E", "#2F3D5C"), "#B9C2CF", None, "#2F3D5C", "#8A2E2E",
   ["Maroon badge colour at both ends, and on the chest symbol like a school crest.", "White-shirt top with a grey panel; navy print on the back.", "Navy tights, the school shorts."]),
 K("TVL", "TV Lama", "CRT blue-grey, wood-grain cabinet, test-card yellow. Era 90an.", KL, ("27°C / 85% RH", "19:00"),
   [("Skrin", "#5F7387", "Main"), ("Siaran", "#D9CFBE", "Sub"), ("Kad ujian", "#E1B64A", "Pop"), ("Kabinet", "#6B4B2E", "Deep"), ("Pucat", "#F2EEE6", "Light")],
   "#E1B64A", ("#5F7387", "#D9CFBE", "#E1B64A", "#F2EEE6", "#F2EEE6"), "#D9CFBE", None, "#6B4B2E", "#E1B64A",
   ["Test-card yellow at both ends.", "Screen blue-grey top with a broadcast-beige panel.", "Wood-cabinet brown tights: the TV set itself."]),
 K("TBK", "Tin Biskut", "Cobalt tin, gold rim, cream lid. The one kept for buttons.", KL, ("29°C / 80% RH", "16:00"),
   [("Kobalt", "#2E4C8C", "Main"), ("Tudung", "#E9DDBF", "Sub"), ("Emas", "#C9A24A", "Pop"), ("Gelap", "#1B2D55", "Deep"), ("Krim", "#F6F0E1", "Light")],
   "#C9A24A", ("#2E4C8C", "#E9DDBF", "#C9A24A", "#C9A24A", "#F6F0E1"), "#E9DDBF", None, "#1B2D55", "#C9A24A",
   ["Gold rim at both ends.", "Cobalt top with a cream-lid panel and a gold chest symbol.", "Deep cobalt tights."]),
 K("BLN", "Bulan", "Moon white on midnight blue. Made for night runs.", KL, ("24°C / 90% RH", "21:30"),
   [("Malam", "#141C2E", "Main"), ("Bulan", "#E7E9EE", "Sub"), ("Perak", "#AEB6C2", "Pop"), ("Gelap", "#0A0F1A", "Deep"), ("Cahaya", "#F7F8FA", "Light")],
   "#AEB6C2", ("#141C2E", "#E7E9EE", "#AEB6C2", "#F7F8FA", "#F7F8FA"), "#E7E9EE", None, "#141C2E", "#AEB6C2",
   ["Silver at both ends; the seams are silver too, made in reflective thread for night runs.", "Midnight top with a moon-white panel.", "Midnight tights, so the reflective OFN does the work in the dark."]),
 K("LSB", "Laut Sabah", "Deep sea blue, sand and a fishing-boat orange.", "4.4800°N  118.6110°E", ("29°C / 80% RH", "06:30"),
   [("Laut", "#0F6E8C", "Main"), ("Pasir", "#F2E6CC", "Sub"), ("Bot", "#F2A541", "Pop"), ("Dalam", "#083A4A", "Deep"), ("Buih", "#F8F3E8", "Light")],
   "#F2A541", ("#0F6E8C", "#F2E6CC", "#F2A541", "#F8F3E8", "#F8F3E8"), "#F2E6CC", None, "#083A4A", "#F2A541",
   ["Boat orange at both ends.", "Sea-blue top with a sand panel.", "Deep-sea tights."]),
]
def build(k):
    parts = dict(beanie=H.beanie(k), tee=H.tee(k, False), teeb=H.tee(k, True), sleeve=H.arm_sleeve(k), tights=H.tights(k), socks=H.socks(k))
    for key in ("tee", "teeb"):
        parts[key] = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}{k["code"]}"', parts[key])
        parts[key] = re.sub(r'clip-path="url\(#([^)]+)\)"', lambda m: f'clip-path="url(#{m.group(1)}{k["code"]})"', parts[key])
    lsf, lsb = LSM.ls(k, False), LSM.ls(k, True)
    nm_of = {h: nm for nm, h, _ in k["pal"]}
    def chips(*hs): return "".join(f'<span class="chip"><i style="background:{h}"></i>{nm_of.get(h, "Reflective")}</span>' for h in dict.fromkeys(hs))
    T = k["tee"]
    tiles = [("Running beanie", parts["beanie"], chips(k["beanie"])), ("Tee front", parts["tee"], chips(*T[:4])), ("Tee back", parts["teeb"], chips(T[0], T[4])),
             ("Arm sleeve", parts["sleeve"], chips(k["sleeve"])), ("Long sleeve front", lsf, chips(*T[:4])), ("Long sleeve back", lsb, chips(T[0], T[1], T[4])),
             ("Short tights", parts["tights"], chips(k["tights"], k["tights_logo"])), ("Crew socks", parts["socks"], chips(k["socks"]))]
    grid = "".join(f'<figure class="pt">{svg}<figcaption><b>{n}</b><span class="chips">{ch}</span></figcaption></figure>' for n, svg, ch in tiles)
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#F3F4F2" if G.dk(h) else G.INK}"><b>{nm}</b><span>{h}</span><i>{role}</i></div>' for nm, h, role in k["pal"])
    notes = "".join(f"<li>{x}</li>" for x in k["notes"])
    return (f'<section class="kit" id="{k["code"].lower()}"><header class="kh"><div><div class="eyebrow">OFN—{k["code"]}</div><h2>{k["n"]}</h2><p class="lede">{k["line"]}</p></div></header>'
            f'<div class="pal">{sw}</div><div class="lay"><figure>{H.flatlay(k, parts)}</figure><ul class="notes">{notes}</ul></div><div class="pgrid">{grid}</div></section>')
body = "".join(build(k) for k in KITS)
nav = "".join(f'<a class="nv" href="#{k["code"].lower()}"><span style="background:{k["pal"][0][1]}"></span><span style="background:{k["pal"][1][1]}"></span><span style="background:{k["pal"][2][1]}"></span>{k["n"]}</a>' for k in KITS)
tints = "".join(G.tint(i, h) for i, h in {**H.TINTS, **LSM.H.TINTS}.items())
page = open(os.path.join(HERE, "page_02.html")).read()
page = page.replace("{{DEFS}}", G.DEFS + f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{tints}</defs></svg>').replace("{{NAV}}", nav).replace("{{KITS}}", body)
open(os.path.join(OUT, "head-to-toe-02.html"), "w").write(page); print("ok", len(page))
