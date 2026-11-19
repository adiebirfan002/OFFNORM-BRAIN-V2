"""Export the head-to-toe kits as clean reference PNGs for Higgsfield.
Run from the repo root:  python3 brand/higgsfield/source/export.py
Writes HTML stubs to /tmp then screenshots them with headless Chrome."""
import os, sys, io, re, contextlib, importlib.util, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
spec = importlib.util.spec_from_file_location("h2t", os.path.join(ROOT, "brand", "headtotoe", "source", "build.py")); H = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(H)
G = H.G
_s2 = importlib.util.spec_from_file_location("h2t02", os.path.join(ROOT, "brand", "headtotoe", "source", "build_02.py")); S2 = importlib.util.module_from_spec(_s2)
with contextlib.redirect_stdout(io.StringIO()): _s2.loader.exec_module(S2)
ALL = H.KITS + S2.KITS
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP = tempfile.mkdtemp()
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=Inter:wght@500;600;700&display=swap">'
def defs(): return G.DEFS + '<svg width="0" height="0" style="position:absolute"><defs>' + "".join(G.tint(i, h) for i, h in H.TINTS.items()) + '</defs></svg>'
def shoot(body, path, w, h, transparent=False, css=""):
    f = os.path.join(TMP, os.path.basename(path) + ".html")
    open(f, "w").write(f'<!doctype html><meta charset="utf-8">{FONTS}<style>html,body{{margin:0;background:{"transparent" if transparent else "#F1F2F0"}}}'
                       f'.mn{{font-family:"IBM Plex Mono",monospace}}{css}</style>{defs()}{body}')
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}", "--virtual-time-budget=4000", f"--screenshot={path}"]
    if transparent: args.insert(3, "--default-background-color=00000000")
    subprocess.run(args + ["file://" + f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
PIECES = [("01_beanie", "beanie", "Running beanie"), ("02_tee_front", "tee", "Tee, front"), ("03_tee_back", "teeb", "Tee, back"),
          ("04_arm_sleeve", "sleeve", "Arm sleeve"), ("05_short_tights", "tights", "Short tights"), ("06_socks", "socks", "Crew socks")]
for k in ALL:
    d = os.path.join(OUT, "kits", f'{k["code"]}_{k["n"].replace(" ", "-")}'); os.makedirs(d, exist_ok=True)
    parts = dict(beanie=H.beanie(k), tee=H.tee(k, False), teeb=H.tee(k, True), sleeve=H.arm_sleeve(k), tights=H.tights(k), socks=H.socks(k))
    for fn, key, _ in PIECES:
        svg = parts[key].replace("<svg ", '<svg width="2048" height="2048" ', 1)
        shoot(svg, os.path.join(d, f'{k["code"]}_{fn}.png'), 2048, 2048)
    fl = H.flatlay(k, parts).replace("<svg ", '<svg width="1100" height="1820" ', 1)
    shoot(fl, os.path.join(d, f'{k["code"]}_00_full_kit.png'), 1100, 1820)
    # labelled board for the team (not for upload as a garment reference)
    nm_of = {h: n for n, h, _ in k["pal"]}
    cells = "".join(f'<figure>{parts[key]}<figcaption>{label}</figcaption></figure>' for _, key, label in PIECES)
    sw = "".join(f'<div style="background:{h};color:{"#F3F4F2" if G.dk(h) else G.INK}"><b>{n}</b><span>{h} · {r}</span></div>' for n, h, r in k["pal"])
    css = ("body{font-family:Inter,sans-serif;color:#17181A;padding:40px;width:2320px}h1{margin:0 0 6px;font-size:56px}p{margin:0 0 24px;font-size:24px;color:#555}"
           ".sw{display:grid;grid-template-columns:repeat(5,1fr);border-radius:12px;overflow:hidden;margin-bottom:28px}.sw div{padding:18px;font-size:20px;display:flex;flex-direction:column}"
           ".sw span{font-family:'IBM Plex Mono',monospace;font-size:16px;opacity:.85}.g{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}"
           "figure{margin:0;background:#fff;border-radius:12px;overflow:hidden}figure svg{display:block;width:100%;height:auto}figcaption{padding:12px 16px;font-size:24px;font-weight:600}")
    shoot(f'<h1>OFFNORM · {k["n"]} · OFN—{k["code"]}</h1><p>{k["line"]}</p><div class="sw">{sw}</div><div class="g">{cells}</div>',
          os.path.join(d, f'{k["code"]}_99_board.png'), 2400, 2080, css=css)
    print("kit", k["code"])
# logo files, transparent
L = os.path.join(OUT, "logo"); os.makedirs(L, exist_ok=True)
for col, hexc in (("black", "#151617"), ("white", "#FFFFFF")):
    t = H.tid(hexc)
    shoot(f'<svg width="1600" height="1200" viewBox="0 0 800 600">{H.ofn(400, 60, 340, t)}</svg>', os.path.join(L, f"OFN_mark_{col}.png"), 1600, 1200, True)
    shoot(f'<svg width="800" height="2000" viewBox="0 0 400 1000">{H.ofn(200, 40, 220, t, vertical=True)}</svg>', os.path.join(L, f"OFN_vertical_{col}.png"), 800, 2000, True)
    shoot(f'<svg width="1600" height="1200" viewBox="0 0 800 600">{G.logo("sym", 160, 140, 480, t)}</svg>', os.path.join(L, f"symbol_{col}.png"), 1600, 1200, True)
    shoot(f'<svg width="3000" height="400" viewBox="0 0 1500 200">{G.logo("wm", 40, 40, 1420, t)}</svg>', os.path.join(L, f"wordmark_{col}.png"), 3000, 400, True)
print("done")
