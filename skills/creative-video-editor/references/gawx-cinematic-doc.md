# Reference: Gawx Art "Perfect Imperfection." (cinematic personal documentary)

Studied 2026-10-13 from `a downloaded copy of the reference video` (16:13, 1482x1080 ≈ 1.37:1,
1.6M views). 162 stills at 6 s, 240 frames colour-measured, 323 cuts measured, the full narration read. Use for
cinematic personal stories, "making of" projects, travel chapters and moody Reels. Grade: `luts/Cine_Gawx.cube` (this skill).

## The look (measured)

| Measure | Value | What it means |
|---|---|---|
| Median brightness | **0.14** (mean .22) | low-key: most of the frame sits in shadow; light falls on one subject |
| Highlights | p95 .63, p99 **.82** | a film shoulder: nothing clips, whites are cream not white |
| Blacks | p1 0.0, p5 .035 | deep, real blacks (not faded) |
| Highlight tint | blue -0.09 vs luma, green +0.02 | creamy yellow-green highlights (print-film emulation) |
| Mid tint | blue -0.04, green +0.01 | slightly olive mids |
| Shadow tint | red +0.014 | faintly warm shadows (and lots of red set dressing in them) |
| Saturation | median **.25** | muted overall, but… |
| Colour families | reds + skin **48%**, teal/cyan **35%**, greens **1%**, yellows 5% | two-colour world: red and teal. Greens are pushed to teal, yellows to orange |

**Recreate:** `Cine_Gawx.cube` (normal footage) / `AppleLog_Cine_Gawx.cube` (Apple Log), then
`noise=alls=6:allf=t` (fine grain) and `vignette=PI/5`. On the user's footage the LUT lands saturation .27 and the same
.81 highlight ceiling. **The look is half lighting:** he shoots dark rooms with one practical lamp or window, red
objects and walls (cups, carpet, bags, a red backdrop), silhouettes in doorways. A bright evenly lit room won't become
this with a LUT; light one side of the face and keep the rest dark.

## Editing (measured)

- **Average shot 3.0 s, median 1.8 s**; 52 shots under 1 s, 45 over 5 s. Rhythm alternates: calm narrated stretches
  (~25-30 cuts per 2 min) and **music-only montage bursts** (52-65 cuts per 2 min) for travel and process sections.
- **Shot vocabulary:** extreme close-ups of objects and hands (lens dials, a pen, thread, paper), overhead table shots,
  hero objects on a red surface, silhouettes in doorways and corridors, wide static establishing frames, handheld
  fisheye selfies to camera, train windows and platforms at golden hour, his face lit from one side.
- **Photos as photos:** in the travel chapter many shots are framed with a thin black or white border inside the frame
  (like prints or scans), mixed with full-bleed footage.
- **Sound:** narration over music; whole minutes with music only; real ambience (trains, streets) under montages.

## Typography

- **Small red uppercase chapter cards**, numbered: "2. THE LITTLE TILLE BOY", "3. THE LAYOUT", "7. THE BRICK", usually
  bottom-centre over a calm shot or alone on black; never big.
- **Words spread across the frame:** "CENTRO · HISTÓRICO · CDMX" set as three words far apart over a wide shot;
  "PART TWO / ANATOMY OF A PHOTOBOOK" stacked and spaced.
- **Subtitles small, red or pale yellow, low**: the documentary subtitle style (our `doc-yellow`; a red variant fits
  the user's palette).
- Credits as a grid of words, white with red highlights; ends on "THE END" in white + red.

## Storytelling (the structure that carries 16 minutes)

1. **Bookend hook:** "This is my cup collection. This is the one I made. … This is my photo book collection… but I
   haven't made one of my own, until now." The pattern sets up the promise; the film ends on the same line with the
   object finished ("This is the one I made").
2. **Origin through objects (numbered):** the cameras that defined him, one per era (first camera → 14 → 16 → 18 → the
   big one → photography) — a timeline told through things.
3. **Stakes + date:** "I promised myself to go back to Japan and make a photo book… My flight is departing in 2 weeks."
4. **The question:** "But how do you even make a photo book?" → teaches the four aspects (images, sequence, layout,
   object), each numbered and compared to film-making.
5. **Rehearsal → journey:** a practice day in Mexico City, then the trip as music-led chapters with almost no talking.
6. **The making:** process close-ups in order (select, sequence, layout, fold, stitch with red thread, cover, embroider).
7. **Meaning, said out loud:** "There's a strange beauty in imperfection… the most human thing is to make something
   imperfect." Then the bookend line.

(A sponsor read sits between the rehearsal and the trip, framed as a product he designed.)

## For a Reel (9:16) in this style

- Grade `Cine_Gawx` + grain + vignette; keep the frame dark and let one practical light do the work.
- Option: a **4:5 or 1.37:1 picture inside the 9:16 frame** on black, with small red chapter text in the bar below.
- Open on a bookend line ("This is my ___. This is the one I made."), number the chapters, let one montage run on
  music only, close on the meaning line and the bookend.
- Captions: `doc-yellow` (or red, small, low), not one-word captions; no big headline text.
- Sounds: real ambience + `cinematic/remembering-woosh` for memories, `transition/camera-shutter` on photos; few.
