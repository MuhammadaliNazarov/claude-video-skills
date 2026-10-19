# Reference: Kallaway "dopamine addiction loop" (split explainer)

Studied 2026-10-13 from `a downloaded copy of the reference video` (111.5 s, 720x1280, 23.976 fps,
-14.3 LUFS). Every frame at 0.5 s, full transcript, audio measured. This is the template for **talking-head explainer
Reels**; recreate it with `templates/split-explainer/` and the `red-white` / `red-black` caption styles. The user's
palette replaces his: **red + black + white** (no cyan, no gold, no green, no purple).

## The format in one paragraph

Black canvas with a faint dot grid. The top ~70% is a motion-graphics stage; the speaker sits in a **rounded card
docked at the bottom** (top edge at 73% of the height, 6% side insets, only the top corners visible). A persistent title
(heavy sans + serif italic) names the topic. **One spoken word at a time** sits just above the card at 64% height. Every
1-2 s something on the stage changes, driven by the words. Every ~10-15 s the edit **breaks the pattern**: the speaker
goes full screen for 1-3 s (a rhetorical line or an aside), or a full-frame film clip plays. A numbered recurring object
(the red neon infinity loop) is the chapter fixture: the camera returns to it at each step, and it ends as the recap.

## Storytelling (structure, with times)

| Time | Beat | What carries it |
|---|---|---|
| 0.0-3.5 | **Hook:** "Here's how to make your storytelling so addictive it is scientifically impossible to skip." | title builds word by word in 1.5 s; 4 visual changes in 4 s (creator clips → glowing brain in a red circle → wall of Reels thumbnails → it turns red) |
| 3.5-11.5 | **Name the thing + promise + authority by analogy:** "the dopamine addiction loop… only four steps… same psychology casinos use" | title "The Dopamine Addiction Loop"; infinity loop draws itself, numbers 1-4 land on it; brain ↔ loop ↔ slot machine linked by glowing lines |
| 11.5-36 | **Step 1 Stakes** (definition → 3 parts → example → caveat) | camera dives into the loop to "1 Stakes"; phone mockups of his own videos; 3 numbered chips fill one by one with labels; a script page writes the example sentence |
| 34.5-51 | **Step 2 Big Question** (definition → contrast with step 1 → casino example) | loop rotates to "2 Big Question"; a real Reel in a frame with a "10K followers" tag and a "Did he actually hit 10k?" bubble; blackjack cards, next card flips |
| 51-71 | **Step 3 Head fake** ("this is really where you hook them") | "3 Headfake"; road splits A / B, a headlight beam swings from A to B; "Art of Contrast" title; film clips (Fight Club) for "crazy head fake no one saw coming" |
| 71.5-84.5 | **Step 4 Re-hook** (casino analogy) | loop recap 1-2-3-4; full-frame casino footage of cards being dealt |
| 85-96 | **Good vs great** (one loop vs cascading loops) | two graph boxes: one arc vs a chain of arcs |
| 91-96 | **Recap:** "stakes, big question, head fake, re-hook" | the loop re-forms with all four labels, title "Super Addicting Story" |
| 96.5-110 | **CTA:** proof (100,000 views) + "Comment 'storytelling'" | full-screen face, then a YouTube card of his long video; "Comment "storytelling" to get video link"; ends on IG logo + handle, fade to black |

Rules this teaches:
- **Hook = outcome + absurd claim** ("scientifically impossible to skip") in the first sentence, no greeting.
- **Name the framework, number it, preview the count** ("only four steps") so the viewer knows how long to stay.
- **Explain each step the same way:** name → what it does → one concrete example (often an analogy from a familiar world:
  casinos) → why it matters.
- **Re-hook lines between steps** ("Now, step three is the head fake, and this is really where you hook them").
- **Recap the whole framework** before the CTA; CTA with social proof and a comment keyword.

## Speech and cut

- 433 words in 107 s = **242 words a minute** (4 words/s). Median gap between words **0.04 s**, the longest 0.38 s:
  every breath and pause is cut. No jump cut is hidden: the stage graphics carry the eye.
- Energetic, slightly smiling delivery, constant hand gestures framed inside the card, eyes on the lens.
- He holds a small object in one hand the whole time (a prop that keeps the hands busy).

## Layout and framing (in 1080x1920 numbers)

| Mode | Share of time | Geometry |
|---|---|---|
| **Split** (stage + speaker card) | ~75% | card: x 68-1012, top y 1410, radius ~37, runs off the bottom edge; speaker framed waist-up, centred, room visible |
| **Full-screen speaker** | ~15% (16.5-17.5, 30.5-34, 52.5-53.5, 68-71, 82.5-84.5, 96.5-99.5) | tighter crop than the card (punch ~1.4x), face upper-middle, caption stays at 64% |
| **Full-frame B-roll / film clip** | ~10% (71.5-75, 78.5-82.5) | clip fills the frame, caption on top |

- Studio: dark room, grey acoustic panels, framed B/W photos, **one vertical LED tube** as the colour accent (his is cyan;
  ours should be red). Black cap, black sweater: wardrobe disappears into the black canvas.
- Watermark: Instagram glyph + `@HANDLE` (condensed caps, ~22 px) top-right of the stage (y ~25%) in split mode,
  bottom-left above the caption in full mode.

## Typography

| Role | His | Ours |
|---|---|---|
| Captions | heavy grotesk, sentence case as spoken, punctuation kept, ~84 px, tight tracking, white, soft dark halo, no box | `ig-captions.py --style red-white` (Inter Black 86, -3.2 tracking, red key words) or `red-black` (black word on a red box) |
| Title line 1 | same grotesk bold, ~48 px | Inter Bold / Black |
| Title line 2 | high-contrast **serif italic**, ~90 px, with a thin red glowing underline | Instrument Serif Italic (or Playfair Display Italic), red underline glow |
| Chapter numbers | huge grotesk number (~200 px) + label (~80 px) beside it ("1 Stakes") | Inter Black |
| Small labels | grotesk bold 26-34 px, white | Inter Bold |

Mixed pairs inside one title are the signature: "How to make your / *Storytelling addictive*", "How does the / *Big
Question* / works in casino", "Art of *Contrast*", "Super Addicting *Story*", "Comment *"storytelling"*".

## Colour

His: black canvas, red neon (the loop, the hook wall), white glow, gold (chips), green (road), purple (CTA card).
**Ours: black #0A0A0A canvas + red #FF2A2A neon + white.** Map his gold/green/purple to red, white or a dim red
(#7A1414) so one accent runs the whole video.

## Motion graphics

- **Everything glows:** white or red bloom (`filter: drop-shadow(0 0 18px)` / box-shadow glow), on black, with a faint
  dot grid (`radial-gradient` dots, 2 px every 24 px, white at .07) and a soft vignette.
- **3D-looking hero objects** (glass brain, neon loop, slot machine, chips, phone mockups, a script page, cards): stills or
  short renders, never flat icons. Thin white lines connect related objects (line draws, 0.3 s).
- **Word-driven:** each object or label lands on the word that names it (numbers 1-4 on "four steps"; chip 2 on
  "something at risk"). Items fill one by one, earlier ones stay.
- **Camera moves through the graphic world:** push into the loop to reveal "1 Stakes", rotate to "2", pull back for the
  recap. Text types/rises in word by word (titles build in ~1.5 s).
- Hard cuts are rare (30 in 111 s); most changes are animated transitions on the stage (one every ~1-2 s).

## Sound

- A continuous **bass-heavy music bed**, ducked under the voice (more sub-bass in the 40 ms gaps than under speech);
  it drops out under the film-clip section (70-90 s) and returns. Master -14 LUFS, very compressed (LRA 3.4).
- Light tonal accents on some reveals (a sustained tone at ~600-700 Hz at 1.2 s and 3.0 s); no whoosh on every
  change. Ends on an upbeat sting. (Measured from the waveform, not heard.)

## Recreate checklist

1. Script: hook (outcome + bold claim) → name + count → steps (name, job, example, why) → recap → CTA with keyword.
2. Record: dark room, one red LED accent, black clothes, mid shot with hands; 16:9 or 4K vertical so the card crop holds.
3. Cut every pause (target median gap < 0.1 s): `tighten-cut.py --maxgap 0.08`, `dead-air.py --max 0.15`.
4. Build in `templates/split-explainer/`: title pair, stage objects per beat, full-screen breaks every 10-15 s.
5. Captions last: `ig-captions.py --style red-white --pos ref` (one word at a time).
6. Bed ducked under voice, drop it under a pattern break, sting at the end, -14 LUFS.
