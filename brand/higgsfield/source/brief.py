"""Build the shareable Higgsfield brief page (brief.html). Run from the repo root."""
import os, io, re, html, base64, contextlib, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); ROOT = os.path.dirname(os.path.dirname(OUT))
spec = importlib.util.spec_from_file_location("pr", os.path.join(HERE, "prompts.py")); P = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(P)
H = P.H; THUMBS = "/private/tmp/claude-501/hf"
kits = ""
for k in H.KITS:
    img = base64.b64encode(open(f'{THUMBS}/{k["code"]}.jpg', "rb").read()).decode()
    blocks = []
    for name, pose in P.SHOTS: blocks.append((name, P.prompt(k, pose=pose)))
    blocks.append(("Hero, female runner", P.prompt(k, who="a lean Malaysian female distance runner in her mid-20s", pose="standing relaxed, facing the camera, arms by her sides")))
    fill = dict(tg=P.WORD[k["tights"]], b=P.WORD[k["beanie"]], tb=P.WORD[k["tee"][0]])
    for i, x in enumerate(P.DETAIL): blocks.append((["Detail: tights logo", "Detail: reflective at night", "Detail: beanie", "Detail: tee back print"][i], x.format(**fill)))
    pr = "".join(f'<div class="pr"><div class="prh"><b>{n}</b><button type="button" class="cp">Copy</button></div><pre>{html.escape(t)}</pre></div>' for n, t in blocks)
    dots = "".join(f'<i style="background:{h}"></i>' for _, h, _ in k["pal"])
    kits += (f'<details class="kit" id="{k["code"].lower()}"><summary><span class="dots">{dots}</span><b>{k["n"]}</b><span class="code">OFN—{k["code"]}</span>'
             f'<span class="hint">Board and 9 prompts</span></summary><div class="kb"><img src="data:image/jpeg;base64,{img}" alt="{k["n"]} reference board">'
             f'<p class="files">Files: <code>kits/{k["code"]}_{k["n"].replace(" ", "-")}/</code></p>{pr}</div></details>')
neg = html.escape(P.NEG)
page = open(os.path.join(HERE, "brief_page.html")).read().replace("{{KITS}}", kits).replace("{{NEG}}", neg)
open(os.path.join(OUT, "brief.html"), "w").write(page); print("ok", len(page))
