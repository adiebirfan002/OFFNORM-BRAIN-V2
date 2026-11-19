"""Build the Higgsfield team folder, version 2: three images per colourway.
  1_OUTFIT_DESIGN.jpg       our six items in a 3x2 grid (beanie, tee front, arm sleeve / short tights, crew socks, tee back)
  2_REAL_LIFE_REFERENCE.jpg the founder's real-photo references in the same grid, other brands' logos blurred
  3_PHOTO_STYLE.jpg         the outdoor photography style reference
Usage (repo root):  python3 brand/higgsfield/source/package.py <out_dir> <refs_dir>
refs_dir holds REAL_sheet.png (built from source/real_sheet.html) and REF_style.jpg; not kept in this public repo."""
import os, sys, io, re, shutil, subprocess, tempfile, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
DST, REFS = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("pr", os.path.join(HERE, "prompts.py")); P = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(P)
H, WORD = P.H, P.WORD; G = H.G
_ls = importlib.util.spec_from_file_location("ls", os.path.join(ROOT, "brand", "headtotoe", "source", "build_ls.py")); LSM = importlib.util.module_from_spec(_ls)
with contextlib.redirect_stdout(io.StringIO()): _ls.loader.exec_module(LSM)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; TMP = tempfile.mkdtemp()
def jpg(src, dst): subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "93", src, "--out", dst], stdout=subprocess.DEVNULL, check=True)
def design_sheet(k, path, longsleeve=False):
    parts = ([H.beanie(k), LSM.ls(k, False), LSM.ls(k, True), H.tights(k), H.socks(k), '<svg viewBox="0 0 800 800"></svg>'] if longsleeve
             else [H.beanie(k), H.tee(k, False), H.arm_sleeve(k), H.tights(k), H.socks(k), H.tee(k, True)])
    sz = '<svg width="800" height="800" '
    cells = "".join("<div>" + p.replace("<svg ", sz, 1) + "</div>" for p in parts)
    defs = G.DEFS + '<svg width="0" height="0" style="position:absolute"><defs>' + "".join(G.tint(i, h) for i, h in H.TINTS.items()) + '</defs></svg>'
    tag = k["code"] + ("ls" if longsleeve else "")
    f = os.path.join(TMP, tag + ".html")
    open(f, "w").write('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&display=swap">'
                       '<style>html,body{margin:0;background:#fff}.g{display:grid;grid-template-columns:repeat(3,800px);grid-auto-rows:800px}.g svg{display:block}'
                       '.mn{font-family:"IBM Plex Mono",monospace}</style>' + defs + f'<div class="g">{cells}</div>')
    png = os.path.join(TMP, tag + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=2400,1600", "--virtual-time-budget=5000", f"--screenshot={png}", "file://" + f],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    jpg(png, path)

LOC = {
 "KPO": "the limestone hills of Ipoh, Perak at first light: tall jungle-topped karst cliffs behind him, dry gravel, low scrub and scattered dark rocks in the foreground",
 "MSN": "the shore at Cherating, Pahang in monsoon season: a dark rocky headland and wind-bent casuarina trees behind him, wet dark sand and black rocks in the foreground, heavy storm clouds",
 "SGK": "the coastal cliffs of Terengganu at golden hour: a steep green-and-rock headland behind him, dry grass, dark sand and scattered rocks in the foreground",
 "PBK": "the mangrove mudflats of Kuala Selangor at low tide: a wall of dark mangrove forest behind him, cracked mud, roots and stones in the foreground",
 "KNB": "the granite summit plateau of Mount Kinabalu, Sabah: huge bare granite peaks behind him, granite slabs and low alpine scrub in the foreground, drifting cloud",
 "SBH": "Broga Hill, Selangor at sunrise: long grassy ridges and a steep hillside behind him, dry grass, a dirt trail and scattered rocks in the foreground",
}
def head(k):
    return """IMAGES:
Image 1 = OFFNORM OUTFIT DESIGN. Six panels: top row = running beanie, t-shirt front, arm sleeve. Bottom row = short tights, crew socks, t-shirt back. This is the exact product. Copy its colours, colour panels, coloured seams, logos and logo positions exactly.
Image 2 = REAL-LIFE REFERENCE. The same six items in the same six positions. Use it ONLY for how each item really looks when worn: shape, fit, length, fabric texture, thickness and stitching. Ignore its colours, prints, blurred logos, people, and any other clothing in it (white tank top, blue t-shirt, watch, belt).
Image 3 = PHOTOGRAPHY STYLE. Copy only its light, mood, framing, colour grade and film grain. Ignore its person, clothes and location.
"""
def outfit(k):
    b, (tb, tp, ts, tl, tx), sl, tg, so = k["beanie"], k["tee"], k["sleeve"], k["tights"], k["socks"]
    w = lambda h: f"{WORD[h]} ({h})"
    return f"""THE OUTFIT, exactly these items and nothing else:
1. Running beanie: thin smooth stretch-jersey, close fit, soft slouchy top, flat hem band, no cuff, no knit ribbing. All {w(b)}. Small OFN logo in a slightly darker {WORD[b]} on the front-side above the hem.
2. T-shirt: relaxed athletic-fit raglan running tee, heathered quick-dry knit, short sleeves. Body {w(tb)}. Thin raised {WORD[ts]} stitched seams on the two raglan seams only (neck to underarm). The lower half of his RIGHT sleeve is a {w(tp)} panel; his left sleeve is plain {WORD[tb]}. Small {WORD[tl]} round OFFNORM symbol centred on the chest. Back: OFFNORM wordmark across the upper back in {WORD[tx]}, small F and NM marks at the back hem corners.
3. Arm sleeve: one smooth matte compression sleeve, wrist to mid-bicep, all {w(sl)}, on his RIGHT arm only. Left arm bare.
4. Short tights: fitted ribbed compression half tights ending mid-thigh, raw-cut hem, wide waistband with drawcord. All {w(tg)}. Large silver reflective OFN logo running vertically down his LEFT outer thigh. Nothing worn over them.
5. Crew socks: mid-calf, ribbed, cushioned foot. All {w(so)}, with OFFNORM knitted vertically in a darker {WORD[so]}.
6. Plain white running shoes, no branding.
Left and right are HIS left and right: when he faces the camera, his right arm is on the left of the picture and his left thigh is on the right of the picture.
"""
def photo(k):
    return f"""LOCATION: {LOC[k["code"]]}.
PHOTOGRAPHY: outdoor editorial trail-running portrait like Image 3. Low warm sun from the side, hard light with crisp shadows, part of the hills in deep shadow, moody grey clouds. 35mm full-frame camera, f/5.6, runner pin sharp, background slightly soft. Earthy muted grade on the landscape, fine film grain, Kodak Portra 400 look, natural skin with real texture. Photorealistic.
COLOUR RULE: the warm grade must not change the clothes. Every garment keeps the exact colour from Image 1.
SUBJECT: a lean, athletic Malaysian distance runner in his mid-20s, short dark hair, tan skin, calm serious expression.
AVOID: any logo or colour from Image 2 or Image 3, hydration vest, running shorts, long leggings, panels on both sleeves, arm sleeves on both arms, extra stripes or lines on the t-shirt, invented text, cartoon or 3D-render look."""
def head_ls(k):
    return """IMAGES:
Image 1 = OFFNORM OUTFIT DESIGN. Top row = running beanie, long-sleeve top front, long-sleeve top back. Bottom row = short tights, crew socks, empty. This is the exact product. Copy its colours, colour panels, coloured seams, logos and logo positions exactly.
Image 2 = REAL-LIFE REFERENCE. The same items in the same positions. Use it ONLY for how each item really looks when worn: shape, boxy fit, length, fabric texture, mesh panels, thickness and the visible overlock stitching. Ignore its colours (no purple, no lavender, no cream), prints, blurred logos, people, and any other item in it (bandana, waist bag, visor, sunglasses, light shorts, white tank top).
Image 3 = PHOTOGRAPHY STYLE. Copy only its light, mood, framing, colour grade and film grain. Ignore its person, clothes and location.
"""
def outfit_ls(k):
    b, (tb, tp, ts, tl, tx), tg, so = k["beanie"], k["tee"], k["tights"], k["socks"]
    w = lambda h: f"{WORD[h]} ({h})"
    return f"""THE OUTFIT, exactly these items and nothing else:
1. Running beanie: thin smooth stretch-jersey, close fit, soft slouchy top, flat hem band, no cuff, no knit ribbing. All {w(b)}. Small OFN logo in a slightly darker {WORD[b]} on the front-side above the hem.
2. Long-sleeve top: relaxed boxy long-sleeve raglan running top, long straight sleeves with a plain stitched hem (no rib cuff), heathered quick-dry knit. Body {w(tb)}. On EACH side there are two mesh panels: one running down the outer sleeve to the cuff and one running down the side of the body to the hem; both start from the same point on the raglan seam, marked with a small reflective dot. On his RIGHT side these two panels are {w(tp)}. On his LEFT side the same two panels are {WORD[tb]}, the same as the body, so only their mesh texture and stitching show. Every panel seam and both raglan seams are raised contrast overlock stitching in {WORD[ts]}. Small {WORD[tl]} round OFFNORM symbol centred on the chest, a tiny {WORD[ts]} tab on the front hem. Back: OFFNORM wordmark across the upper back in {WORD[tx]}, small F and NM marks at the back hem corners.
3. Short tights: fitted ribbed compression half tights ending mid-thigh, raw-cut hem, wide waistband with drawcord. All {w(tg)}. Large silver reflective OFN logo running vertically down his LEFT outer thigh. Nothing worn over them.
4. Crew socks: mid-calf, ribbed, cushioned foot. All {w(so)}, with OFFNORM knitted vertically in a darker {WORD[so]}.
5. Plain white running shoes, no branding.
No arm sleeve. Left and right are HIS left and right: when he faces the camera, his right side is on the left of the picture.
"""
SHOTS_LS = [
 ("1 · OUTDOOR FRONT (start here)", "SHOT: full body, standing still in the centre of the frame, facing the camera, feet slightly apart, arms relaxed by his sides, plain wrap sunglasses with no branding. Vertical 4:5. He fills about two thirds of the height, landscape all around him. Camera at chest height."),
 ("2 · OUTDOOR BACK", "SHOT: full body from behind, standing still, head turned slightly to his right, so the OFFNORM print on the upper back, the F and NM marks at the hem and the coloured panels on his right side are clearly visible. Vertical 4:5."),
 ("3 · OUTDOOR RUNNING", "SHOT: full body, running mid-stride from left to right along the trail, side-on, both feet off the ground, motion frozen sharp, so the coloured right-side sleeve and body panels are visible. Horizontal 16:9."),
 ("4 · CLOSE-UP LONG-SLEEVE FRONT", "SHOT: medium close-up from chin to waist, facing the camera. The long-sleeve top is the hero: chest symbol, contrast overlock seams, the coloured panels on his RIGHT side, the tonal mesh panels on his LEFT side and the reflective dots where the seams meet, all in sharp focus. Vertical 4:5, 50mm look."),
 ("5 · CLOSE-UP RIGHT SIDE AND CUFF", "SHOT: close-up of his RIGHT side, arm slightly lifted, from shoulder to hip, side-on. The coloured mesh panels running down the sleeve to the plain stitched cuff and down the body side, the overlock stitching and the reflective dot at the raglan seam are the hero. Vertical 4:5, 85mm look."),
]
SHOTS = [
 ("1 · OUTDOOR FRONT (start here)", "SHOT: full body, standing still in the centre of the frame, facing the camera, feet slightly apart, arms relaxed by his sides, plain wrap sunglasses with no branding. Vertical 4:5. He fills about two thirds of the height, landscape all around him. Camera at chest height."),
 ("2 · OUTDOOR BACK", "SHOT: full body from behind, standing still, head turned slightly to his right, so the OFFNORM print on the upper back and the F and NM marks at the hem are clearly visible. Vertical 4:5."),
 ("3 · OUTDOOR RUNNING", "SHOT: full body, running mid-stride from left to right along the trail, both feet off the ground, side-on, motion frozen sharp. Horizontal 16:9."),
 ("4 · CLOSE-UP BEANIE", "SHOT: close-up, head and shoulders, three-quarter profile. The beanie is the hero: jersey fabric, slouchy top, flat hem band and the small tonal OFN logo in sharp focus. Vertical 4:5, 85mm look."),
 ("5 · CLOSE-UP T-SHIRT", "SHOT: medium close-up from chin to waist, facing the camera. The t-shirt is the hero: chest symbol, the two coloured raglan seams, the panel on his RIGHT lower sleeve and the heathered knit in sharp focus. Vertical 4:5, 50mm look."),
 ("6 · CLOSE-UP ARM SLEEVE", "SHOT: close-up of his RIGHT arm from shoulder to hand, hand resting on his hip, side-on. The arm sleeve is the hero, wrist to mid-bicep, smooth and snug, with the t-shirt's sleeve panel just above it. Vertical 4:5, 85mm look."),
 ("7 · CLOSE-UP SHORT TIGHTS", "SHOT: close-up from waist to just above the knees, turned slightly to show his LEFT thigh, his hand resting loosely beside it. The short tights are the hero: rib texture, waistband, raw-cut hem and the large silver reflective OFN logo down the LEFT thigh catching the sun. Vertical 4:5, 85mm look."),
 ("8 · CLOSE-UP CREW SOCKS", "SHOT: low close-up from mid-shin to the shoes, feet planted on the rocky ground, camera at ankle height. The crew socks are the hero: ribbed leg, cushioned foot and the vertical OFFNORM knit. Vertical 4:5, 50mm look."),
]
if os.path.exists(DST): shutil.rmtree(DST)
os.makedirs(DST)
for n, k in enumerate(H.KITS, start=2):
    kd = os.path.join(DST, f'{n}-{k["n"].upper().replace(" ", "-")}'); os.makedirs(kd)
    jpg(os.path.join(OUT, "kits", f'{k["code"]}_{k["n"].replace(" ", "-")}', f'{k["code"]}_99_board.png'), f"{kd}/zz_COLOUR-GUIDE_do-not-upload.jpg")
    for sub, ls_, real, hd, of, shots, label in (
            ("A-TEE-KIT", False, "REAL_sheet.png", head, outfit, SHOTS, "tee + arm sleeve kit"),
            ("B-LONGSLEEVE-KIT", True, "REAL_sheet_ls.png", head_ls, outfit_ls, SHOTS_LS, "long-sleeve kit")):
        sd = os.path.join(kd, sub); os.makedirs(sd)
        design_sheet(k, f"{sd}/1_OUTFIT_DESIGN.jpg", longsleeve=ls_)
        jpg(f"{REFS}/{real}", f"{sd}/2_REAL_LIFE_REFERENCE.jpg")
        shutil.copy(f"{REFS}/REF_style.jpg", f"{sd}/3_PHOTO_STYLE.jpg")
        txt = [f"OFFNORM {k['n']} (OFN—{k['code']}) · {label} · Higgsfield prompts", "",
               "Upload the 3 images in this folder in order (1_OUTFIT_DESIGN, 2_REAL_LIFE_REFERENCE, 3_PHOTO_STYLE).",
               "Copy ONE prompt (everything between the ===== lines), paste, generate 4. Same 3 images for every prompt.", ""]
        for t, shot in shots:
            txt += [f"===== {t} =====", hd(k) + "\n" + shot + "\n\n" + of(k) + "\n" + photo(k).replace("arm sleeves on both arms, ", "an arm sleeve, bandana, purple or lavender colours, " if ls_ else "arm sleeves on both arms, "), ""]
        open(f"{sd}/PROMPTS.txt", "w").write("\n".join(txt))
    print("kit", k["code"])
shutil.copytree(os.path.join(OUT, "logo"), os.path.join(DST, "8-LOGOS-for-fixing"))
open(os.path.join(DST, "1-READ-ME-FIRST.txt"), "w").write("""OFFNORM × HIGGSFIELD (version 2)

Each colourway folder has two kits:
  A-TEE-KIT         tee + arm sleeve + short tights + crew socks + beanie
  B-LONGSLEEVE-KIT  long-sleeve top + short tights + crew socks + beanie (no arm sleeve)
Each kit folder has ONLY 3 images to upload, always in this order:
  1_OUTFIT_DESIGN        our design (colours, panels, logos)
  2_REAL_LIFE_REFERENCE  how the items look in real life (shape, fit, fabric). Same layout as image 1.
  3_PHOTO_STYLE          the outdoor photo look

HOW:
1. Open a colourway folder, e.g. 2-KOPI-O, then A-TEE-KIT or B-LONGSLEEVE-KIT.
2. Upload images 1, 2, 3 from that kit folder into Higgsfield, in that order.
3. Open PROMPTS.txt in the same kit folder, copy prompt 1 (OUTDOOR FRONT), paste, generate 4.
4. Same 3 images for every other prompt in that kit: back, running and the close-ups.
5. Do NOT upload zz_COLOUR-GUIDE. Use it to check colours.
6. If a logo comes out wrong, fix it with Higgsfield's edit tool or the clean logos in 8-LOGOS-for-fixing.

Use the SAME model/face for all 6 colourways. Start with Kopi O, prompt 1, and send it to me first.

CHECK EVERY SHOT:
- tee: panel on the lower RIGHT sleeve only, arm sleeve on the RIGHT arm only
- long sleeve: coloured panels on his RIGHT side only, left-side panels same colour as the body, no arm sleeve
- short tights end mid-thigh, nothing over them
- silver OFN logo down the LEFT thigh
- beanie and socks one colour each, colours match the colour guide
""")
print("done")
