# OFFNORM identity (proposal, round 2)

**Status: proposal, awaiting founder.** Nothing here is final.

Idea: **norm: off.** The first O of OFFNORM is a switch set to off. The second O stays normal.

Round 2 follows the founder's notes on round 1: keep the letters, make the O the identity, add a mark like ACG or
FPA from OFN or OFNM, and draw the mock-ups from `Collection Reference` (six FPA product screenshots: panelled
raglan tees, contrast flatlock seams, colour-blocked sleeves, small chest mark, dotted back graphic, two-tone cap).
The reference photos themselves are not in this repo and were not edited; the mock-ups are new drawings.

| File | What |
|---|---|
| [proposal.png](proposal.png) | The full proposal as one image |
| [proposal.html](proposal.html) | The same page (open in a browser) |
| [svg/](svg) | Recommended marks, black and white |
| [svg/options/](svg/options) | The wordmark with each of the seven O options |
| [source/](source) | `kit.py` letters and O variants, `mocks.py` + `mocks2.py` mock-ups, `build.py` builds everything |

## O options (founder to pick)

O1 Switch (recommended), O2 Shift, O3 Slip, O4 Solid, O5 Exit, O6 Lanes, O7 Dots.

## Emblems (founder to pick)

E1 Switch badge OFN (recommended), E2 Switch badge OFNM, E3 Quad OFNM, E4 Spaced letters, E5 Plate.

## Rules

- Letters are drawn as geometry in `kit.py`. Never retype the logo in a font.
- Low bars: the F bar and the R waist sit below centre.
- Sewn labels and tabs sit 3° off level (Kuala Lumpur is at 3°N). The master logo stays straight.
- Colours, from the reference: Tarmac #17181A, Kopi #4B3B25, Subuh #1B2233, Santan #E9E3D5, Monsoon #C7CEC9,
  Kunyit #D9CC3C (seams). Round 1's pink is dropped.
- Type: Archivo Expanded (headlines), Archivo (text), IBM Plex Mono (numbers and conditions).
- Use ™ until the trademark is registered; ® is shown for the final look only.

Rebuild: `python3 brand/identity/source/build.py`
