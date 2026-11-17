# OFFNORM garment designs

One piece at a time. **Nothing moves to the next step without the founder's approval.**

| File | What |
|---|---|
| [designs.png](designs.png) / [designs.html](designs.html) | The current design page |
| [logo/](logo) | The founder's logo as supplied on 2026-11-16 (PNG only; vector still needed for production) |
| [source/](source) | `build.py` draws the flats and cuts the logo parts out of the PNGs |

## Decided

- **Logo (founder, 2026-11-16):** the O holding F and mirrored F with a diagonal cut; the italic F; the NM zigzag;
  wordmark with the O symbol + FFNORM ®. This replaces options O1-O13 and E1-E5 in `brand/identity`.
- **Design rules (founder approved, 2026-11-16),** from an analysis of FPA: seams as the graphic, thread colour from
  the collection palette, the three logo parts used apart, coordinate and conditions as the small text, labels 3° off.

## Founder feedback on The Sky tee, round 1 (2026-11-16)

- Rejected: the diagonal slash seam across the body.
- No logo on the side of the chest. Try the middle or the arm.
- Minimal, but still showing the identity.

## Status

| Step | Piece | Status |
|---|---|---|
| 1 | FPA analysis and design rules | Approved |
| 2 | The Sky tee flat, round 1 (the slash) | Rejected |
| 2 | The Sky tee flat, round 2: A Centre, B Arm, C The quiet O | Founder liked A and B; asked for the raglan stitch to connect to the white sleeve panel |
| 2 | The Sky tee flat, round 3: A2 Centre, B2 Arm, AB Centre + Arm, with sleeve close-up | Founder chose B2 with changes |
| 2 | The Sky tee flat, round 4: B2 base with changes | Founder: everything okay, but white panel on the right arm only; take D3; no further approval needed for this amendment |
| 2 | The Sky tee, final flat (panel on wearer's right arm, D3 back) | **Approved** (2026-11-16) |
| 3 | 3D mock-ups of the tee for all seven collections | **Accepted by founder 2026-11-17** ("Good enough"). WebGL model in `brand/collections` (lineup.html, `source/tee3d.js`). A model, not a photograph |
| 4 | Other pieces (singlet, shorts, cap, sock, place pieces) | Not designed |

Rebuild: `python3 brand/garments/source/build.py`
