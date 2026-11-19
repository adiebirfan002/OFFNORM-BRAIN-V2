"""Build the team folder for Higgsfield: one folder per colourway with every image in upload order and its prompts.
Usage (repo root):  python3 brand/higgsfield/source/package.py <out_dir> <refs_dir>
refs_dir holds the founder's real-photo references (not kept in this public repo):
  REF_beanie, REF_shirt_front, REF_shirt_back, REF_armsleeve, REF_shorttights, REF_socks (.jpg)"""
import os, sys, io, shutil, subprocess, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
DST, REFS = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("pr", os.path.join(HERE, "prompts.py")); P = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(P)
H, WORD = P.H, P.WORD
W = lambda h: f"{WORD[h]} ({h})"
def jpg(src, dst): subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "93", src, "--out", dst], stdout=subprocess.DEVNULL, check=True)

FILES = ["01_DESIGN_full_kit", "02_DESIGN_beanie", "03_DESIGN_tee_front", "04_DESIGN_arm_sleeve", "05_DESIGN_short_tights", "06_DESIGN_socks",
         "07_PHOTO_beanie", "08_PHOTO_tee_front", "09_PHOTO_arm_sleeve", "10_PHOTO_short_tights", "11_PHOTO_socks"]
BACK = ["12_DESIGN_tee_back", "13_PHOTO_tee_back"]

def prompt(k, shot, back=False):
    b, (tb, tp, ts, tl, tx), sl, tg, so = k["beanie"], k["tee"], k["sleeve"], k["tights"], k["socks"]
    lst = "\n".join(f"Image {i+1}: {f}" for i, f in enumerate(FILES + (BACK if back else [])))
    d_ids = "1-6" + (", 12" if back else ""); p_ids = "7-11" + (", 13" if back else "")
    tee_p = "Images 8 and 13" if back else "Image 8"; tee_d = "Images 3 and 12" if back else "Image 3"
    return f"""REFERENCE IMAGES, in upload order:
{lst}

HOW TO READ THEM:
- DESIGN images ({d_ids}) are OFFNORM's design. They decide the COLOURS, colour panels, which seams are coloured, the logos and where the logos sit. Follow them exactly.
- PHOTO images ({p_ids}) show how each garment looks in real life: shape, fit on the body, length, fabric, texture, thickness, stitching and how it wrinkles. Match them closely so the clothes look like real products.
- Every garment = shape and fabric from its PHOTO + colours and logos from its DESIGN.
- In the PHOTOS, ignore every logo, brand name, text, print, dot pattern and colour, and do not copy the people's faces or bodies. The only branding is OFFNORM's.

{shot}

SUBJECT: a lean, athletic Malaysian distance runner in his mid-20s, short dark hair, natural tan skin with real skin texture, calm confident expression, runner's build with defined calves and shoulders.

OUTFIT, head to toe:

1. RUNNING BEANIE (shape from Image 7, colour and logo from Image 2): a thin, smooth stretch-jersey running beanie, close fit with a soft slouchy gathered top and a flat-stitched hem band, no cuff, no knit ribbing. Colour: {W(b)} only. A small OFN logo (an oval O symbol above the letters F and NM) printed tone-on-tone in a slightly darker {WORD[b]} on the front-side, just above the hem band.

2. T-SHIRT (fit, fabric and stitching from {tee_p}, design from {tee_d}): a relaxed athletic-fit short-sleeve raglan running t-shirt in lightweight heathered quick-dry performance knit with a fine visible texture, thin ribbed crew neck, sleeves ending above the elbow. Body: {W(tb)}. The two raglan seams, from the neck to the underarms, are raised contrast stitched seams in {WORD[ts]}, the same thin bold stitched-line style as the photo. The lower half of the RIGHT sleeve only is a {W(tp)} panel; the left sleeve stays {WORD[tb]}. A small {WORD[tl]} round OFFNORM symbol (an oval O with two F shapes cut by a slash) centred on the chest. A tiny {WORD[ts]} woven tab on the lower front hem, wearer's left. Back: the OFFNORM wordmark across the upper back in {WORD[tx]} with one line of small technical text under it, and small F and NM marks at the two back hem corners.
Do not copy from the shirt photo: the panels on both sleeves, the coloured lines down the body sides and along the hem, its chest logo, the spiral print, the reflective dots, the waist belt, the cap, the sunglasses or the watch.

3. ARM SLEEVE (shape from Image 9, colour from Image 4): one smooth, matte compression arm sleeve from the wrist to mid-bicep, snug with no wrinkles. Colour: {W(sl)}, plain, with a small tone-on-tone OFFNORM symbol near the wrist. RIGHT arm only; the left arm is bare (the photo shows two sleeves, use only one).

4. SHORT TIGHTS (fit, length, fabric and seams from Image 10, colour and logo from Image 5): fitted compression half tights in fine vertical ribbed fabric, ending mid-thigh above the knee, with a curved panel seam on the inner thigh and a clean raw-cut hem. Wide flat waistband with a thin drawcord and a small tone-on-tone OFFNORM wordmark on the waistband. Colour: {W(tg)} only, no dot print. A large silver reflective OFN logo (the oval O symbol stacked above an F and an NM mark) printed vertically down the outer LEFT thigh, in the same position and size as the logo in the photo. No shorts over the tights.

5. CREW SOCKS (height, rib and cushioning from Image 11, colour and logo from Image 6): mid-calf crew running socks with a ribbed leg and cuff, a cushioned terry foot and small knitted L and R marks at the toes. Colour: {W(so)} only. The word OFFNORM knitted vertically down the outer side of the sock leg in a darker tone of the same {WORD[so]}.

6. SHOES: clean plain white running shoes with no visible branding.

PHOTOGRAPHY: premium sportswear lookbook photo, seamless light grey studio backdrop, soft diffused key light from the front-left, gentle fill, soft natural shadow on the floor, full-frame camera, 85mm lens, f/4, eye-level, sharp focus on the fabric so the rib texture, heathered knit and stitching are visible, colours true to the DESIGN images, natural colour grading, high resolution, photorealistic.

AVOID: logos, text, prints or colours from the photos (UVU, Nike, FPA or any other brand), misspelled or invented text, a chunky knitted or cuffed beanie, knee-high socks, stripes, shorts over the tights, long leggings, a sleeve panel or arm sleeve on both arms, changed colours, cartoon, 3D-render look, plastic skin, distorted hands or feet."""
def short(k):
    b, (tb, tp, ts, tl, tx), sl, tg, so = k["beanie"], k["tee"], k["sleeve"], k["tights"], k["socks"]
    return (f"Photoreal full-body studio lookbook photo of a lean Malaysian male runner, mid-20s, facing the camera, light grey seamless backdrop, soft light, 85mm. "
            f"Images 1-6 are OFFNORM DESIGNS (colours, panels, logos: follow exactly). Images 7-11 are PHOTOS (shape, fit, fabric: match closely; ignore their logos, prints, colours and people). "
            f"Beanie: thin stretch-jersey running beanie like Image 7, {WORD[b]}, small tonal OFN logo above the hem. "
            f"T-shirt: relaxed heathered raglan running tee like Image 8, {WORD[tb]}, {WORD[ts]} raised stitched raglan seams, {WORD[tp]} panel on the lower RIGHT sleeve only, small {WORD[tl]} OFFNORM symbol on the chest. "
            f"Arm sleeve: {WORD[sl]} compression sleeve like Image 9, RIGHT arm only, wrist to mid-bicep. "
            f"Short tights: {WORD[tg]} ribbed compression half tights like Image 10, mid-thigh, big silver reflective vertical OFN logo on the outer LEFT thigh, no shorts. "
            f"Socks: {WORD[so]} mid-calf crew socks like Image 11, OFFNORM knitted vertically in a darker tone. White unbranded running shoes. No other brands, no invented text.")
SHOTS = [
 ("A · FRONT (start here)", "SHOT: full body, standing relaxed, facing the camera, arms loose by his sides, feet hip-width apart, whole body from beanie to shoes in frame with space around it. Vertical 4:5 or 3:4 frame.", False),
 ("B · BACK (also upload the 2 images in the BACK-SHOT folder, as Image 12 and 13)", "SHOT: full body from behind, standing straight, head turned slightly to his right, so the OFFNORM print across the upper back and the F and NM marks at the back hem are clearly visible. Vertical 4:5 or 3:4 frame.", True),
 ("C · RUNNING", "SHOT: full body, running mid-stride from left to right, both feet off the ground, arms pumping, motion frozen sharp, side-on so the right-arm sleeve and the left-thigh logo are both visible. Horizontal 16:9 frame.", False),
]
if os.path.exists(DST): shutil.rmtree(DST)
os.makedirs(DST)
for n, k in enumerate(H.KITS, start=2):
    name = k["n"].upper().replace(" ", "-")
    kd = os.path.join(DST, f"{n}-{name}"); os.makedirs(os.path.join(kd, "BACK-SHOT"))
    src = os.path.join(OUT, "kits", f'{k["code"]}_{k["n"].replace(" ", "-")}'); c = k["code"]
    for f, s in zip(FILES[:6], ["00_full_kit", "01_beanie", "02_tee_front", "04_arm_sleeve", "05_short_tights", "06_socks"]):
        jpg(f"{src}/{c}_{s}.png", f"{kd}/{f}.jpg")
    for f, r in zip(FILES[6:], ["REF_beanie", "REF_shirt_front", "REF_armsleeve", "REF_shorttights", "REF_socks"]):
        shutil.copy(f"{REFS}/{r}.jpg", f"{kd}/{f}.jpg")
    jpg(f"{src}/{c}_03_tee_back.png", f"{kd}/BACK-SHOT/12_DESIGN_tee_back.jpg"); shutil.copy(f"{REFS}/REF_shirt_back.jpg", f"{kd}/BACK-SHOT/13_PHOTO_tee_back.jpg")
    jpg(f"{src}/{c}_99_board.png", f"{kd}/zz_COLOUR-GUIDE_do-not-upload.jpg")
    txt = [f"OFFNORM {k['n']} (OFN—{c}) · Higgsfield prompts", "",
           "1. Upload images 01 to 11 from this folder, in number order.",
           "2. Copy one prompt (everything between the ===== lines) and paste it.",
           "3. Generate 4, keep the best.", ""]
    for t, shot, back in SHOTS: txt += [f"===== {t} =====", prompt(k, shot, back), ""]
    txt += ["===== SHORT VERSION (only if Higgsfield says the prompt is too long) =====", short(k), ""]
    open(os.path.join(kd, "PROMPTS.txt"), "w").write("\n".join(txt))
    print("kit", c)
shutil.copytree(os.path.join(OUT, "logo"), os.path.join(DST, "8-LOGOS-for-fixing"))
open(os.path.join(DST, "1-READ-ME-FIRST.txt"), "w").write("""OFFNORM × HIGGSFIELD

GOAL: photo-real shots of one runner wearing the full OFFNORM kit (running beanie, tee, arm sleeve, short tights, crew socks) in 6 colourways.

HOW (same for every colourway):
1. Open a colourway folder, e.g. 2-KOPI-O.
2. Upload images 01 to 11 into Higgsfield, in number order.
   01-06 DESIGN = our colours and logos.  07-11 PHOTO = real-life shape, fit and fabric.
3. Open PROMPTS.txt in the same folder, copy prompt A, paste, generate 4.
4. For the back view use prompt B and also upload the 2 images in BACK-SHOT (they become 12 and 13).
5. Do NOT upload zz_COLOUR-GUIDE. Use it to check the colours.
6. If a logo comes out wrong, fix it with Higgsfield's edit tool or the clean logos in 8-LOGOS-for-fixing.

Use the SAME model/face for all 6 colourways. Start with Kopi O, prompt A, and send it to me before doing the rest.

CHECK EVERY SHOT:
- tee panel and arm sleeve on the RIGHT arm only
- short tights end mid-thigh, no shorts on top
- silver OFN logo vertical on the LEFT thigh
- beanie and socks the same colour
- no UVU / Nike / FPA logos, prints or colours from the photos

If Higgsfield takes fewer than 11 images: upload 01 and 07-11, and use the SHORT VERSION prompt at the bottom of PROMPTS.txt.
""")
print("done")
