# OFFNORM × Higgsfield pack

Everything needed to turn the head-to-toe kits into photo-real model shots on Higgsfield.

## What's in the pack

| Folder / file | What it is | Upload to Higgsfield? |
|---|---|---|
| `kits/<CODE>_<name>/<CODE>_00_full_kit.png` | Whole outfit laid flat, 1100×1820 | Yes, always first |
| `kits/.../<CODE>_01_beanie.png` … `_06_long_socks.png` | One garment per image, 2048×2048 PNG, plain light-grey background, no text | Yes, as garment references |
| `kits/.../<CODE>_99_board.png` | Labelled board with colour names and hex codes | No. For the team, to check results against |
| `kits/.../<CODE>_prompts.txt` | Ready prompts for that kit: front, back, three-quarter, running, female runner, 4 detail shots, negative prompt | Copy and paste |
| `logo/` | Transparent PNGs: OFN mark, OFN vertical, symbol, wordmark, each in black and white | For fixing logos after generation |
| `PROMPTS.md` | All prompts for all six kits in one file | — |

Kits: KPO Kopi O, MSN The Monsoon, SGK Songket, PBK Paya Bakau, KNB Kinabalu, SBH Subuh.

## Recommended workflow

1. **Lock one model first.** Generate a single runner with no garments in mind (or train a Soul ID from 20+ photos of a real person who has agreed to it). Reuse that same face/body as a reference for every kit so the lookbook is consistent. Do not use photos of athletes from other brands.
2. **Pick a model that takes several reference images** for the garment shots. Higgsfield hosts several image models; use one that accepts multiple references (check the model's upload limit in the app). Soul 2.0 is strong for realism and fashion mood; a multi-reference model keeps the garments closer to the drawings. Try both on one kit and keep the better one.
3. **Upload references in this priority order** (if the model limits you, stop where it stops):
   1. `_00_full_kit` 2. `_02_tee_front` 3. `_05_short_tights` 4. `_06_long_socks` 5. `_01_beanie` 6. `_03_tee_back` (only for the back-view shot) 7. `_04_arm_sleeve`
   plus the locked model image.
4. **Paste the prompt** from `<CODE>_prompts.txt`, and the negative prompt if the model has a field for it.
5. **Generate 4 at a time**, pick the closest, then iterate with small prompt edits instead of rewriting.
6. **Check every result against `_99_board.png`** (checklist below).
7. **Fix logos and small text afterwards.** AI image models usually distort logos and small text. Use the edit/inpaint tool on the logo area, or place the transparent PNG from `logo/` in Photoshop/Canva, warped to the fabric.
8. **Video (optional).** Take the best still into image-to-video with a short motion prompt, e.g. "the runner jogs slowly toward the camera, studio light, camera static, 5 seconds".

## Shot list per kit

- Hero front, back view, three-quarter, running mid-stride (in the prompts file)
- Female runner hero
- Details: tights logo close-up, tights logo under camera flash at night (shows the reflective print), beanie close-up, tee back print close-up

## Checklist before a shot is approved

- [ ] Sleeve panel on the wearer's RIGHT arm only; arm sleeve on the RIGHT forearm only
- [ ] Short tights end mid-thigh, no shorts over them
- [ ] OFN on the tights runs vertically down the outer LEFT thigh, silver
- [ ] Beanie and socks are the same single colour
- [ ] Tee seams are thin pop-colour lines along the raglan seams
- [ ] Colours match the board (judge on a calibrated screen)
- [ ] Logos are correct (fix in post if not); no invented text or other brands

## Known limits

- The references are flat drawings, not photos of samples. Fabric drape and fit will be the AI's interpretation until real samples exist.
- Hex codes are screen colours. Colours in AI images drift; judge against the board, and do lab dips with the factory.
- Higgsfield's model line-up and upload limits change. Check the current options in the app.
- The data printed on the tee back (temperature, time, coordinate) is placeholder text for colourways without a collection location.
