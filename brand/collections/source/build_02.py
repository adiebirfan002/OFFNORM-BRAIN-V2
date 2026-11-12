"""Line-up 02: seven living things native to Malaysia. Builds ../lineup-02.html
Run from the repo root:  python3 brand/collections/source/build_02.py   (reuses the drawing code in build.py)"""
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import build as B
INK, CHALK = B.INK, B.CHALK

C = [
 dict(n="Enggang", code="ENG", place="Royal Belum State Park, Perak", lat=5.5497, lon=101.3479, alt="Rhinoceros hornbill · Buceros rhinoceros · Vulnerable",
      cond=("24°C", "92% RH", "06:45"), words="Burung Enggang. Black wings, white tail, an orange casque you can see across a valley",
      pal=[("Bulu", "#151515"), ("Ekor", "#F1EEE6"), ("Balung", "#F28C1E"), ("Paruh", "#F6C63C"), ("Kanopi", "#24402F")],
      tee=("#151515", "#F1EEE6", "#F28C1E", False), band=("#111411", CHALK), motif="fan",
      hero=["High-vis casque cap", "Wing-panel wind vest"], idea="The be-seen collection. Black and white with one loud orange, for dawn and dusk on the road. Royal Belum is reported to hold all ten of Malaysia's hornbill species."),
 dict(n="Harimau", code="HRM", place="Endau-Rompin National Park, Johor and Pahang", lat=2.4389, lon=103.2728, alt="Malayan tiger · Panthera tigris jacksoni · Critically Endangered",
      cond=("25°C", "90% RH", "19:10"), words="Harimau Malaya. Stripes, patience, the hour before dark",
      pal=[("Belang", "#17130F"), ("Jingga", "#C96A1E"), ("Perut", "#F3EAD8"), ("Senja", "#7A3B12"), ("Mata", "#E8B23A")],
      tee=("#C96A1E", "#17130F", "#F3EAD8", False), band=("#17130F", CHALK), motif="stripes",
      hero=["Dusk long sleeve", "Stripe-vent short"], idea="The dusk collection. Fewer than 150 Malayan tigers are reported left in the wild, so this one should be small, numbered, and tied to a tiger conservation partner."),
 dict(n="Rafflesia", code="RAF", place="Gunung Gading National Park, Lundu, Sarawak", lat=1.6905, lon=109.8458, alt="Rafflesia tuan-mudae · no leaves, no stem, one huge flower",
      cond=("27°C", "95% RH", "10:00"), words="Bunga Rafflesia. Rare, heavy, slow, gone in days",
      pal=[("Kelopak", "#9E2B1F"), ("Bintik", "#EBCFB4"), ("Rongga", "#4A1410"), ("Lantai hutan", "#2B2118"), ("Akar", "#55683C")],
      tee=("#9E2B1F", "#4A1410", "#EBCFB4", False), band=("#2B1512", CHALK), motif="rafflesia",
      hero=["Heavyweight rest-day tee", "Wide recovery short"], idea="The rest-day collection. The flower takes months to grow and is open for only a few days, so the drop could work the same way: on sale for seven days, then gone."),
 dict(n="Bunga Raya", code="RYA", place="Perdana Botanical Garden, Kuala Lumpur", lat=3.1430, lon=101.6847, alt="Hibiscus rosa-sinensis · national flower since 28 July 1960",
      cond=("31°C", "74% RH", "07:30"), words="Bunga Raya. Red, open, five petals, everybody's flower",
      pal=[("Merah raya", "#D81E2C"), ("Putih", "#F6F4EF"), ("Debunga", "#F5C83B"), ("Daun", "#1F6B3A"), ("Merah tua", "#8E0F1B")],
      tee=("#F6F4EF", "#D81E2C", "#1F6B3A", True), band=("#D81E2C", CHALK), motif="raya",
      hero=["Race-day singlet", "Five-panel cap"], idea="The race-day collection, timed for Merdeka and Malaysia Day. Five petals, five core pieces. The friendliest of the seven and the natural first drop."),
 dict(n="Penyu", code="PNY", place="Turtle Islands Park, Selingan, Sabah", lat=6.1494, lon=118.0540, alt="Green and hawksbill turtles nest on these beaches",
      cond=("28°C", "82% RH", "22:30"), words="Penyu. Slow on land, tireless at sea, always comes back to the same beach",
      pal=[("Karapas", "#3F5B46"), ("Pasir malam", "#CBB994"), ("Plastron", "#E9E0C3"), ("Laut", "#1F7F86"), ("Dalam", "#12333A")],
      tee=("#3F5B46", "#CBB994", "#E9E0C3", False), band=("#12333A", CHALK), motif="shell",
      hero=["Long-run tee", "Shell-back run vest"], idea="The long slow distance collection. For the runs measured in hours, not pace. Shell green and night sand."),
 dict(n="Beruang Matahari", code="BRG", place="Bornean Sun Bear Conservation Centre, Sepilok, Sabah", lat=5.8636, lon=117.9500, alt="Sun bear · Helarctos malayanus · Vulnerable · the smallest bear",
      cond=("29°C", "85% RH", "12:00"), words="Beruang Matahari. Small, strong, a gold crescent on the chest",
      pal=[("Bulu", "#1B1612"), ("Bulan sabit", "#F0B84A"), ("Muncung", "#C9A47A"), ("Madu", "#D98A1F"), ("Kulit kayu", "#4A382A")],
      tee=("#1B1612", "#4A382A", "#F0B84A", False), band=("#1B1612", CHALK), motif="crescent",
      hero=["Crescent chest tee", "Tempo short"], idea="The short-and-hard collection, for midday heat and tempo runs. Black with one gold crescent, the way the bear wears it."),
 dict(n="Gajah Pygmy", code="GJH", place="Sukau, Lower Kinabatangan, Sabah", lat=5.5095, lon=118.2874, alt="Bornean elephant · Endangered · about 1,000 left",
      cond=("27°C", "90% RH", "16:30"), words="Gajah Pygmy. Gentle, muddy, never walks alone",
      pal=[("Lumpur", "#7B7770"), ("Gading", "#EDE6D6"), ("Rumput", "#6F8A4A"), ("Kinabatangan", "#8C6F4E"), ("Tebing", "#2E2C2A")],
      tee=("#7B7770", "#EDE6D6", "#6F8A4A", False), band=("#2E2C2A", CHALK), motif="prints",
      hero=["Club tee", "Mud-day trail sock"], idea="The group-run collection, made for Off Day Club. Mud grey and riverbank green, with a line of footprints walking up the back."),
]

def dots(kind, col):
    random.seed(11); o = []
    def d(x, y, r, hollow=False):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" ' + (f'fill="none" stroke="{col}" stroke-width="1.2"/>' if hollow else f'fill="{col}"/>'))
    cx, cy = 400, 368
    if kind == "fan":        # tail feathers: a fan with one pale band
        for k in range(11):
            a = math.radians(-150 + k * 12)
            for j in range(9):
                R = 26 + j * 13; d(cx + math.cos(a) * R, cy + 78 + math.sin(a) * R, 2.2 + j * .32, j in (6, 7))
    elif kind == "stripes":
        for k in range(8):
            x0 = 316 + k * 24; L = random.randint(9, 15); top = 292 + random.randint(0, 26)
            for j in range(L):
                t = j / (L - 1); d(x0 + math.sin(t * 3.14 + k) * 9, top + j * 10, 1.2 + 3.6 * math.sin(t * 3.14))
    elif kind == "rafflesia":
        for i in range(16):
            a = 6.283 * i / 16; d(cx + math.cos(a) * 22, cy + math.sin(a) * 22, 2.6)
        for p in range(5):
            a0 = 6.283 * p / 5 - 1.57; px, py = cx + math.cos(a0) * 62, cy + math.sin(a0) * 62
            for i in range(14):
                a = 6.283 * i / 14; d(px + math.cos(a) * 30, py + math.sin(a) * 30, 3.1)
            for i in range(5):
                a = random.uniform(0, 6.283); r = random.uniform(4, 20); d(px + math.cos(a) * r, py + math.sin(a) * r, 1.8, True)
    elif kind == "raya":
        for p in range(5):
            a0 = 6.283 * p / 5 - 1.57
            for i in range(18):
                t = 6.283 * i / 18; ex, ey = 34 * math.cos(t) + 46, 21 * math.sin(t)
                d(cx + ex * math.cos(a0) - ey * math.sin(a0), cy + 6 + ex * math.sin(a0) + ey * math.cos(a0), 2.8)
        for j in range(9): d(cx + j * 9.5, cy + 6 - j * 9.5, 2.6 if j < 7 else 3.8)
        for a in (-.5, .2, .9): d(cx + 76 + math.cos(a) * 12, cy - 70 + math.sin(a) * 12, 2)
    elif kind == "shell":
        for i in range(34):
            a = 6.283 * i / 34; d(cx + math.cos(a) * 74, cy + math.sin(a) * 92, 3.2)
        for row in range(-3, 4):
            for col_ in range(-2, 3):
                x = cx + col_ * 30 + (15 if row % 2 else 0); y = cy + row * 26
                if ((x - cx) / 60) ** 2 + ((y - cy) / 78) ** 2 < 1: d(x, y, 4.6, True)
    elif kind == "crescent":
        for k, (R, r) in enumerate(((70, 4.4), (58, 3.4), (47, 2.4))):
            n = 15 - k * 2
            for i in range(n):
                a = math.radians(20 + i * 140 / (n - 1)); d(cx + math.cos(a) * R * 1.25, cy - 40 + math.sin(a) * R, r)
    elif kind == "prints":
        for k in range(5):
            x = 350 + (k % 2) * 62 + k * 6; y = 450 - k * 40
            for i in range(12):
                a = 6.283 * i / 12; d(x + math.cos(a) * 15, y + math.sin(a) * 15, 2.2)
            d(x, y, 7)
            for t in (-1, 0, 1): d(x + t * 12, y - 24 + abs(t) * 4, 3.2)
    return "".join(o)
B.dots = dots

LAB = {"ENG": (-12, -12, "end"), "HRM": (12, 20, "start"), "RAF": (0, -16, "middle"), "RYA": (-12, 20, "end"), "PNY": (-14, -10, "end"), "BRG": (-14, 6, "end"), "GJH": (-14, 22, "end")}
pts = "".join(f'<circle cx="{B.X(c["lon"]):.1f}" cy="{B.Y(c["lat"]):.1f}" r="9" fill="{c["pal"][2][1] if c["code"] in ("ENG","BRG") else c["tee"][0]}" stroke="currentColor" stroke-width="2"/>'
              f'<text class="hx" x="{B.X(c["lon"])+LAB[c["code"]][0]:.1f}" y="{B.Y(c["lat"])+LAB[c["code"]][1]:.1f}" font-size="14" text-anchor="{LAB[c["code"]][2]}" fill="currentColor">{c["n"].upper()}</text>' for c in C)
chart = f'<svg viewBox="0 0 1000 340" class="chart" role="img" aria-label="The seven habitats plotted by latitude and longitude">{B.grid}{B.kl}{pts}</svg>'

PAGE = open(f"{HERE}/page_02.html").read()
matrix = "".join(f'<tr><th>{c["n"]}</th><td>OFN—{c["code"]}</td><td>{c["lat"]:.4f}°N, {c["lon"]:.4f}°E</td><td>{c["place"]}</td><td>{", ".join(c["hero"])}</td></tr>' for c in C)
html = (PAGE.replace("{{HEAD}}", B.head).replace("{{DEFS}}", B.DEFS).replace("{{CHART}}", chart)
        .replace("{{HERO}}", f'<svg class="mk hero-mark" viewBox="0 0 {B.WMW} 100" style="color:#F3F4F2"><use href="#wm"/></svg>')
        .replace("{{BANDS}}", "".join(B.band(c, i) for i, c in enumerate(C)).replace("The place drawn in dots, with its coordinate", "Drawn in dots, with the coordinate where it lives")).replace("{{MATRIX}}", matrix))
open(f"{OUT}/lineup-02.html", "w").write(html)
print("ok 02")
