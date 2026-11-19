"""Write Higgsfield prompts for every head-to-toe kit. Run from the repo root."""
import os, io, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
spec = importlib.util.spec_from_file_location("h2t", os.path.join(ROOT, "brand", "headtotoe", "source", "build.py")); H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(H)
# plain colour words an image model understands, per hex
WORD = {
 "#2B1D16": "espresso brown", "#C9A27A": "warm sand tan", "#E8B04A": "golden yellow", "#120C09": "near-black", "#EDE3D5": "cream",
 "#2B3440": "storm slate grey", "#6E7B85": "rain grey", "#E0342B": "flag red", "#1B4A5A": "deep sea teal", "#DDE3E4": "pale foam grey",
 "#3A1430": "deep plum", "#F4E9D0": "silk cream", "#D4AF37": "metallic songket gold", "#1C0A18": "black plum", "#FAF4E6": "off-white",
 "#55503F": "mud olive brown", "#C8CDB4": "pale sage green", "#B5763A": "root copper brown", "#2C2A20": "dark swamp brown", "#F2F2EA": "mist white",
 "#3F5560": "granite blue-grey", "#E5E9EA": "mist white", "#9BC2A6": "soft alpine mint", "#1E2C33": "summit charcoal", "#F6F8F8": "snow white",
 "#2D3A6B": "pre-dawn navy", "#F0C9A8": "dawn peach", "#E57A44": "sunrise orange", "#161E3D": "midnight navy", "#FBF1E8": "warm white",
 "#C7B3A8": "terrazzo pink-grey", "#EFE7E0": "cement white", "#A0523D": "rust red", "#6E5E57": "stone grey-brown", "#F8F4F0": "pale off-white",
 "#6E2232": "velvet burgundy", "#E7D3B0": "ticket cream", "#C9A04E": "antique gold", "#3E1219": "dark burgundy", "#F6EEDF": "screen cream",
 "#F1EDE3": "school-shirt white", "#B9C2CF": "pale blue-grey", "#8A2E2E": "maroon", "#2F3D5C": "school navy", "#FBF8F1": "warm white",
 "#5F7387": "CRT blue-grey", "#D9CFBE": "broadcast beige", "#E1B64A": "test-card yellow", "#6B4B2E": "wood-cabinet brown", "#F2EEE6": "pale cream",
 "#2E4C8C": "cobalt blue", "#E9DDBF": "biscuit-tin cream", "#C9A24A": "tin gold", "#1B2D55": "deep cobalt navy", "#F6F0E1": "cream",
 "#141C2E": "midnight blue", "#E7E9EE": "moon white", "#AEB6C2": "silver grey", "#0A0F1A": "near-black navy", "#F7F8FA": "bright white",
 "#0F6E8C": "deep sea blue", "#F2E6CC": "sand", "#F2A541": "fishing-boat orange", "#083A4A": "deep-sea teal", "#F8F3E8": "foam white",
}
W = lambda h: f"{WORD[h]} ({h})"
def prompt(k, who="a lean Malaysian male distance runner in his mid-20s", pose="standing relaxed, facing the camera, arms by his sides"):
    b, (tb, tp, ts, tl, _), sl, tg, so = k["beanie"], k["tee"], k["sleeve"], k["tights"], k["socks"]
    return (f"Full-body studio fashion photograph of {who}, {pose}, wearing the complete OFFNORM running kit exactly as in the reference images:\n"
            f"- a {W(b)} ribbed knit beanie with a folded cuff and a small tone-on-tone embroidered OFN logo on the cuff;\n"
            f"- a {W(tb)} short-sleeve raglan running t-shirt, thin {WORD[ts]} seam lines along both raglan seams, a {WORD[tp]} panel on the lower RIGHT sleeve only, "
            f"a small {WORD[tl]} round OFFNORM symbol centred on the chest, a tiny {WORD[ts]} tab on the lower front hem;\n"
            f"- one {W(sl)} compression arm sleeve on the RIGHT forearm only, plain, small tonal logo at the wrist;\n"
            f"- {W(tg)} fitted ribbed compression short tights ending mid-thigh, wide waistband with drawcord, raw-cut hem, "
            f"a silver reflective OFN logo printed vertically down the outer LEFT thigh;\n"
            f"- {W(so)} ribbed knee-high running socks with OFFNORM knitted vertically down the shin in a darker tone of the same colour;\n"
            f"- plain white running shoes.\n"
            f"Seamless light grey studio backdrop, soft diffused key light from the left, gentle shadow on the floor, natural skin texture, "
            f"premium sportswear lookbook, 85mm lens, f/4, sharp fabric detail showing the ribbed knit, colours true to the references. "
            f"No shorts over the tights, no extra logos, no other brands, no added text.")
NEG = ("extra logos, misspelled text, distorted logo, other brand marks, stripes, swoosh, shorts over the tights, long leggings, "
       "sleeve panel on both arms, arm sleeves on both arms, cartoon, 3D render, plastic skin, extra fingers, cropped feet")
SHOTS = [
 ("Hero, front", "standing relaxed, facing the camera, arms by his sides"),
 ("Back view", "standing with his back to the camera, head turned slightly, so the OFFNORM print across the upper back and the F and NM marks at the hem are visible"),
 ("Three-quarter", "standing at a three-quarter angle to the camera, weight on one leg"),
 ("Running", "mid-stride running across the frame from left to right, both feet off the ground, motion caught sharp"),
]
DETAIL = [
 "Close-up of the left thigh of a runner wearing {tg} ribbed compression short tights with a silver reflective OFN logo printed vertically, hand resting near it, studio light, sharp rib texture.",
 "Night street photo, camera flash on, runner in {tg} short tights: the vertical OFN logo glows bright white from the flash, everything else dark.",
 "Close-up of a {b} ribbed beanie on a runner's head, tone-on-tone OFN logo embroidered on the folded cuff, light grey studio background.",
 "Close-up of the upper back of a {tb} raglan running t-shirt, printed OFFNORM wordmark with small technical text underneath, studio light.",
]
md = ["# OFFNORM × Higgsfield prompts", "", "Copy one block per generation. Upload the matching reference images first (see README).", "",
      "## Negative prompt (use with every generation where the model has a negative field)", "", "```", NEG, "```", ""]
for k in H.KITS:
    d = os.path.join(OUT, "kits", f'{k["code"]}_{k["n"].replace(" ", "-")}')
    txt = [f"OFFNORM {k['n']} (OFN—{k['code']}) — Higgsfield prompts", ""]
    md += [f"## {k['n']} · OFN—{k['code']}", ""]
    for name, pose in SHOTS:
        p = prompt(k, pose=pose)
        md += [f"### {name}", "", "```", p, "```", ""]; txt += [f"=== {name} ===", p, ""]
    pf = prompt(k, who="a lean Malaysian female distance runner in her mid-20s", pose="standing relaxed, facing the camera, arms by her sides")
    md += ["### Hero, female runner", "", "```", pf, "```", ""]; txt += ["=== Hero, female runner ===", pf, ""]
    fill = dict(tg=WORD[k["tights"]], b=WORD[k["beanie"]], tb=WORD[k["tee"][0]])
    md += ["### Detail shots", ""]
    for x in DETAIL:
        md += ["```", x.format(**fill), "```", ""]; txt += ["=== Detail ===", x.format(**fill), ""]
    txt += ["=== Negative prompt ===", NEG]
    open(os.path.join(d, f'{k["code"]}_prompts.txt'), "w").write("\n".join(txt))
open(os.path.join(OUT, "PROMPTS.md"), "w").write("\n".join(md))
print("ok")
