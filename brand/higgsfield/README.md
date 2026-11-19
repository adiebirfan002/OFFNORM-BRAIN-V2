# OFFNORM × Higgsfield (version 2, 2026-11-20)

Version 1 sent 11-13 images per shot; the founder reported mismatched clothes, wrong colours/style and too many images.
Version 2 sends three images per colourway, in this order:

1. `1_OUTFIT_DESIGN.jpg` – our six items in a 3×2 grid: beanie, tee front, arm sleeve / short tights, crew socks, tee back
2. `2_REAL_LIFE_REFERENCE.jpg` – the founder's real-photo references in the same grid, other brands' logos blurred (`source/real_sheet.html`)
3. `3_PHOTO_STYLE.jpg` – the outdoor photography style reference

Prompts (about 3,500 characters): outdoor front, back, running, and close-ups of beanie, tee, arm sleeve, short tights, socks, each with a Malaysian location per colourway and an explicit rule that the colour grade must not change garment colours.

Build: `python3 brand/higgsfield/source/export.py` then `python3 brand/higgsfield/source/package.py <out> <refs>` (refs = REAL_sheet.png + REF_style.jpg, kept out of this public repo).
