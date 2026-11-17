"""20 extra colourways for the approved OFFNORM kit. Builds ../colourways.html
Run from the repo root:  python3 brand/colourways/source/build.py"""
import os, sys, io, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
GS = os.path.join(ROOT, "brand", "garments", "source"); sys.path.insert(0, GS)
spec = importlib.util.spec_from_file_location("gbuild", os.path.join(GS, "build.py")); G = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(G)

# family, name, code, one line, palette: body, panel, thread, deep, light  (each a (name, hex))
FAM = {
 "Makan": "Colours off the table. Warm, edible, instantly Malaysian.",
 "Kain": "Colours from cloth: batik, songket, the pasar malam awning.",
 "Langit": "Colours from the sky at the hours people run: subuh, petang, senja.",
 "Alam": "Colours from the land: highland mist, red earth, bougainvillea, the Sabah sea.",
}
CW = [
 ("Makan", "Teh Tarik", "TTK", "Milk tea, pulled. Soft and warm, the easiest colourway to wear.",
  [("Teh", "#C89B6D"), ("Susu", "#F3E7D3"), ("Tarik", "#7A4A2A"), ("Gelas", "#4A2E1C"), ("Buih", "#FBF4E8")]),
 ("Makan", "Kopi O", "KPO", "Black coffee with a gold edge. For the 5am run.",
  [("Kopi", "#2B1D16"), ("Kacang", "#C9A27A"), ("Gula", "#E8B04A"), ("Pekat", "#120C09"), ("Cawan", "#EDE3D5")]),
 ("Makan", "Sambal", "SBL", "Chilli red with a yellow kick. The loudest of the twenty.",
  [("Cili", "#B3261E"), ("Bawang", "#F2D6C2"), ("Kunyit", "#F5B700"), ("Belacan", "#5A120E"), ("Nasi", "#FFF4EA")]),
 ("Makan", "Pandan", "PDN", "Leaf green and coconut white. Fresh, quiet, very local.",
  [("Pandan", "#5E8C3A"), ("Santan", "#E6EFD9"), ("Daun", "#1F3D1A"), ("Gelap", "#2C4A22"), ("Kelapa", "#F4F7EE")]),
 ("Makan", "Durian", "DRN", "Husk yellow and thorn green. Divisive on purpose.",
  [("Isi", "#C9B13A"), ("Duri", "#3E5A2A"), ("Krim", "#F6E7A1"), ("Kulit", "#2E3B1F"), ("Pucat", "#FBF6DD")]),
 ("Makan", "Kuih Lapis", "KLP", "Pink, cream and green in layers, like the kuih.",
  [("Merah jambu", "#D9445A"), ("Lapis", "#F7E3C6"), ("Hijau", "#2E8B57"), ("Merah tua", "#6B1A2A"), ("Krim", "#FFF7EC")]),
 ("Kain", "Batik Indigo", "BTK", "Deep indigo with a wax-resist gold line.",
  [("Nila", "#22356F"), ("Kain", "#E8E2D4"), ("Lilin", "#C98A2B"), ("Malam", "#121D3D"), ("Putih", "#F5F1E8")]),
 ("Kain", "Songket", "SGK", "Plum and woven gold. The dressy one.",
  [("Ungu", "#3A1430"), ("Benang emas", "#D4AF37"), ("Sutera", "#F4E9D0"), ("Gelap", "#1C0A18"), ("Pucat", "#FAF4E6")]),
 ("Kain", "Pasar Malam", "PSM", "Night-market black under yellow bulbs and red awnings.",
  [("Malam", "#1B1B1F"), ("Lampu", "#F2B134"), ("Kanopi", "#E2463D"), ("Arang", "#0B0B0D"), ("Kertas", "#F6F2E8")]),
 ("Kain", "Kampung", "KPG", "Timber brown, attap beige, banana-leaf green.",
  [("Kayu", "#8C6B47"), ("Atap", "#EADBC4"), ("Pisang", "#3C6E47"), ("Tiang", "#4A3624"), ("Dinding", "#F7F1E6")]),
 ("Kain", "Tanah Merah", "TNM", "Laterite red earth with a charcoal line.",
  [("Tanah", "#A9472A"), ("Debu", "#E8C8A8"), ("Arang", "#2F2A26"), ("Bata", "#5C2614"), ("Pasir", "#F6EADF")]),
 ("Langit", "Subuh", "SBH", "Navy before dawn, the first pink and orange at the edge.",
  [("Fajar", "#2D3A6B"), ("Merah muda", "#F0C9A8"), ("Matahari", "#E57A44"), ("Malam", "#161E3D"), ("Cahaya", "#FBF1E8")]),
 ("Langit", "Hujan Petang", "HJP", "Four o'clock rain grey with one warm yellow.",
  [("Awan", "#6F7C86"), ("Kabut", "#D9DEE2"), ("Lampu", "#F2C14E"), ("Ribut", "#39424A"), ("Putih", "#F4F6F7")]),
 ("Langit", "Senja", "SNJ", "Sunset orange over a violet sea.",
  [("Senja", "#E2683C"), ("Awan", "#F6D9B8"), ("Ungu", "#5B2A6E"), ("Bara", "#7A2F1C"), ("Cahaya", "#FFF4E8")]),
 ("Langit", "Bulan", "BLN", "Moon white on midnight blue. Made for night runs, with silver reflective seams.",
  [("Malam", "#141C2E"), ("Bulan", "#E7E9EE"), ("Perak", "#AEB6C2"), ("Gelap", "#0A0F1A"), ("Cahaya", "#F7F8FA")]),
 ("Alam", "Kinabalu", "KNB", "Granite slate and alpine mint.",
  [("Granit", "#3F5560"), ("Kabus", "#E5E9EA"), ("Pucuk", "#9BC2A6"), ("Puncak", "#1E2C33"), ("Salji", "#F6F8F8")]),
 ("Alam", "Kabus Genting", "KBG", "Cloud grey and pine. The pale one for highland runs.",
  [("Kabus", "#B9C3C2"), ("Awan", "#F7F8F6"), ("Pain", "#3E6B5A"), ("Batu", "#5F6E6C"), ("Putih", "#FFFFFF")]),
 ("Alam", "Laut Sabah", "LSB", "Deep sea blue, sand and a fishing-boat orange.",
  [("Laut", "#0F6E8C"), ("Pasir", "#F2E6CC"), ("Bot", "#F2A541"), ("Dalam", "#083A4A"), ("Buih", "#F8F3E8")]),
 ("Alam", "Bunga Kertas", "BKT", "Bougainvillea magenta with a leaf-green seam.",
  [("Bunga", "#C2367A"), ("Kelopak", "#F7E6EF"), ("Daun", "#3F7D4E"), ("Tua", "#5E1A3C"), ("Pucat", "#FFF6FA")]),
 ("Alam", "Paya Bakau", "PBK", "Mangrove mud, root brown and brackish green.",
  [("Lumpur", "#55503F"), ("Air", "#C8CDB4"), ("Akar", "#B5763A"), ("Paya", "#2C2A20"), ("Kabut", "#F2F2EA")]),
]
INK = G.INK
def lum(h): return G.lum(h)
def kit(name, code, pal):
    (bn, body), (pn, panel), (tn, thread), (dn, deep), (ln, light) = pal
    k = dict(code=code, n=name, co="3.1390°N  101.6869°E",
             cap=(light, body, thread),
             sh=(deep, panel, body, thread),
             so=(light, thread, deep, body, thread))
    return k
def tee(body, panel, thread):
    G.SKY.update(body=body, panel=panel, thread=thread)
    s = G.final(False)
    return s if not G.dk(body) else s.replace('filter="url(#t_ink)"', 'filter="url(#t_white)"')
cards = ""; fams = ""
for fam, blurb in FAM.items():
    rows = ""
    for i, (f, name, code, line, pal) in enumerate(CW):
        if f != fam: continue
        n = CW.index((f, name, code, line, pal)) + 1
        k = kit(name, code, pal)
        sw = "".join(f'<div style="background:{h};color:{"#F3F4F2" if G.dk(h) else INK}"><b>{nm}</b><span>{h}</span><i>{role}</i></div>'
                     for (nm, h), role in zip(pal, ("Body", "Panel", "Thread", "Deep", "Light")))
        rows += (f'<article class="cw" id="cw{n:02d}"><header><small>{n:02d} · OFN—{code}</small><h3>{name}</h3><p>{line}</p></header>'
                 f'<div class="sw">{sw}</div>'
                 f'<div class="kitgrid"><figure class="big">{tee(pal[0][1], pal[1][1], pal[2][1])}<figcaption>Tee</figcaption></figure>'
                 f'<figure>{G.cap_front(k)}<figcaption>Cap</figcaption></figure>'
                 f'<figure>{G.shorts_tights(k)}<figcaption>Shorts + 3/4 tights</figcaption></figure>'
                 f'<figure>{G.socks(k)}<figcaption>Long socks</figcaption></figure></div></article>')
    fams += f'<section class="band fam"><div class="in"><div class="col"><div class="eyebrow"><span>Family</span><span>{fam}</span></div><h2>{fam}</h2><p>{blurb}</p></div><div class="cws">{rows}</div></div></section>'
strip = "".join(f'<a class="chip" href="#cw{i+1:02d}"><span style="background:{p[0][1]}"></span><span style="background:{p[1][1]}"></span><span style="background:{p[2][1]}"></span><b>{i+1:02d}</b> {nm}</a>' for i, (_, nm, _, _, p) in enumerate(CW))
head = open(os.path.join(ROOT, "brand", "identity", "source", "page.html")).read()
head = head[head.index("<meta"):head.index("</style>")]
PAGE = open(f"{HERE}/page.html").read()
html = (PAGE.replace("{{HEAD}}", head).replace("{{DEFS}}", G.DEFS)
        .replace("{{HERO}}", '<svg class="mk hero-mark" viewBox="0 0 781 83"><use href="#lg_wm" width="781" height="83" filter="url(#t_white)"/></svg>')
        .replace("{{STRIP}}", strip).replace("{{FAMS}}", fams))
open(f"{OUT}/colourways.html", "w").write(html)
print("ok", len(CW))
