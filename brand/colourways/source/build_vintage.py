"""16 vintage colourways for the approved OFFNORM kit. Builds ../vintage.html
Run from the repo root:  python3 brand/colourways/source/build.py"""
import os, sys, io, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
GS = os.path.join(ROOT, "brand", "garments", "source"); sys.path.insert(0, GS)
spec = importlib.util.spec_from_file_location("gbuild", os.path.join(GS, "build.py")); G = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(G)

FAM = {
 "Era 70an": "Seventies colour: warm, earthy, a little sun-bleached. Minibuses, kopitiam tiles, rattan chairs.",
 "Era 80an": "Eighties colour: shophouse pastels, terrazzo floors, cassette tapes and the old cinema.",
 "Era 90an": "Nineties colour: school sports day, the uniform, a bicycle in the porch, the TV in the corner.",
 "Kenangan": "Colours of things kept in a drawer: studio photos, postcards, the biscuit tin, yesterday's paper.",
}
CW = [
 ("Era 70an", "Bas Mini", "BSM", "The pink city minibus with a cream stripe, faded by years of sun.",
  [("Merah jambu", "#D98C93"), ("Jalur", "#F2E3D0"), ("Marun", "#8C2F39"), ("Tua", "#5C2A2E"), ("Krim", "#F7EEE3")]),
 ("Era 70an", "Kopitiam", "KPT", "Mosaic-tile green, marble-top white and a kopi brown seam.",
  [("Jubin", "#4F7B63"), ("Marmar", "#EDE6D6"), ("Kopi", "#8A5A3B"), ("Gelap", "#2E4A3B"), ("Cawan", "#F6F1E6")]),
 ("Era 70an", "Kerusi Rotan", "KRT", "Rattan tan, cane brown and an olive cushion.",
  [("Rotan", "#C49A5E"), ("Anyaman", "#EFE0C2"), ("Kusyen", "#6B7A3A"), ("Kayu", "#5E4326"), ("Pucat", "#F7EEDC")]),
 ("Era 70an", "Tingkap Nako", "TNK", "Frosted green louvre glass in an aluminium frame.",
  [("Kaca", "#8FB5A3"), ("Kabus", "#E4E8E2"), ("Aluminium", "#6E7676"), ("Bayang", "#4C6B5E"), ("Cahaya", "#F3F5F1")]),
 ("Era 80an", "Rumah Kedai", "RKD", "Shophouse pastel blue, plaster cream and teal shutters.",
  [("Dinding", "#8DB3C7"), ("Plaster", "#F1E8D8"), ("Pintu", "#2F6B6F"), ("Bayang", "#3E5A66"), ("Kapur", "#FAF5EC")]),
 ("Era 80an", "Jubin Terazo", "JTZ", "Terrazzo pink-grey with rust-red flecks.",
  [("Terazo", "#C7B3A8"), ("Simen", "#EFE7E0"), ("Serpih", "#A0523D"), ("Batu", "#6E5E57"), ("Pucat", "#F8F4F0")]),
 ("Era 80an", "Kaset", "KST", "Smoked cassette shell, cream label and red tape.",
  [("Cangkerang", "#5B4A42"), ("Label", "#E9DEC9"), ("Pita", "#C2412D"), ("Gelap", "#2E2522"), ("Kertas", "#F5EFE3")]),
 ("Era 80an", "Panggung Wayang", "PGW", "Old cinema velvet, gold marquee letters, cream ticket.",
  [("Baldu", "#6E2232"), ("Tiket", "#E7D3B0"), ("Emas", "#C9A04E"), ("Gelap", "#3E1219"), ("Skrin", "#F6EEDF")]),
 ("Era 90an", "Hari Sukan", "HSK", "Sports-day house colours after a hundred washes.",
  [("Rumah biru", "#3B4F7A"), ("Padang", "#EFE6CF"), ("Rumah kuning", "#D9A43A"), ("Gelap", "#1F2A44"), ("Kapur", "#F7F1E3")]),
 ("Era 90an", "Seragam Sekolah", "SRG", "The white shirt, the navy shorts and a maroon badge.",
  [("Kemeja", "#F1EDE3"), ("Kelabu", "#B9C2CF"), ("Lencana", "#8A2E2E"), ("Seluar", "#2F3D5C"), ("Putih", "#FBF8F1")]),
 ("Era 90an", "Basikal Lama", "BSK", "Faded frame green, chrome and a brown leather saddle.",
  [("Rangka", "#6E8B6E"), ("Krom", "#E2E2DA"), ("Pelana", "#8A5A34"), ("Gelap", "#3E4F3E"), ("Pucat", "#F4F3EC")]),
 ("Era 90an", "TV Lama", "TVL", "CRT blue-grey, wood-grain cabinet, test-card yellow.",
  [("Skrin", "#5F7387"), ("Siaran", "#D9CFBE"), ("Kad ujian", "#E1B64A"), ("Kabinet", "#6B4B2E"), ("Pucat", "#F2EEE6")]),
 ("Kenangan", "Gambar Studio", "GBS", "Sepia studio portrait, the brown of old photo paper.",
  [("Sepia", "#A07E5E"), ("Kertas", "#EADBC4"), ("Bingkai", "#4A3628"), ("Gelap", "#3A2A1F"), ("Pudar", "#F6EFE2")]),
 ("Kenangan", "Poskad Lama", "PSK", "Faded sky, yellowed card and a red stamp.",
  [("Langit", "#9DB6C4"), ("Kad", "#EFE3C8"), ("Setem", "#B5473A"), ("Dakwat", "#4E6675"), ("Pucat", "#F7F0DE")]),
 ("Kenangan", "Tin Biskut", "TBK", "Cobalt tin, gold rim, cream lid. The one kept for buttons.",
  [("Kobalt", "#2E4C8C"), ("Tudung", "#E9DDBF"), ("Emas", "#C9A24A"), ("Gelap", "#1B2D55"), ("Krim", "#F6F0E1")]),
 ("Kenangan", "Surat Khabar", "SKB", "Newsprint grey, ink black and a red masthead.",
  [("Kertas", "#CFC8B8"), ("Pucat", "#F2EEE4"), ("Tajuk", "#A3302A"), ("Dakwat", "#2B2A28"), ("Putih", "#FAF8F2")]),
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
    fams += f'<section class="band fam vint"><div class="in"><div class="col"><div class="eyebrow"><span>Family</span><span>{fam}</span></div><h2>{fam}</h2><p>{blurb}</p></div><div class="cws">{rows}</div></div></section>'
strip = "".join(f'<a class="chip" href="#cw{i+1:02d}"><span style="background:{p[0][1]}"></span><span style="background:{p[1][1]}"></span><span style="background:{p[2][1]}"></span><b>{i+1:02d}</b> {nm}</a>' for i, (_, nm, _, _, p) in enumerate(CW))
head = open(os.path.join(ROOT, "brand", "identity", "source", "page.html")).read()
head = head[head.index("<meta"):head.index("</style>")]
PAGE = open(f"{HERE}/page_vintage.html").read()
html = (PAGE.replace("{{HEAD}}", head).replace("{{DEFS}}", G.DEFS)
        .replace("{{HERO}}", '<svg class="mk hero-mark" viewBox="0 0 781 83"><use href="#lg_wm" width="781" height="83" filter="url(#t_white)"/></svg>')
        .replace("{{STRIP}}", strip).replace("{{FAMS}}", fams))
open(f"{OUT}/vintage.html", "w").write(html)
print("ok", len(CW))
