# Motion graphics: how to make them better, where references come from, how the skill learns

Agreed with the user 2026-10-13. Applies to video-editor (both presets) and creative-video-editor. Build with
HyperFrames (local CLI + its skills: `hyperframes-core`, `-animation`, `-keyframes`, `-registry`).

## What makes motion graphics premium (check every animation against this)

1. **Motion with meaning.** Every animation lands on the word it illustrates, and the movement itself says something:
   a number counts up, a path draws A → B, a card pushes the old one away, a list fills one item per word. Decoration-
   only motion looks cheap; cut it.
2. **Easing.** Fast in, slow settle (`power2.out` / `power3.out` for entrances, `power2.in` for exits, `power2.inOut`
   for camera moves); overshoot (`back.out`) only on one hero moment per video. Never linear (except count-up proxies
   and continuous drift). Vary durations by weight: small UI 0.25-0.35 s, titles 0.4-0.5 s, big reveals 0.6-0.9 s.
3. **Depth.** Foreground / subject / background layers; soft blur on what's behind; slight parallax (layers moving at
   different speeds); glows and soft shadows. Flat cards pasted on footage read as slides.
4. **Continuity.** Elements transform into the next (a pill becomes a card, a number becomes a chart, the camera
   travels through one graphic world, e.g. Kallaway's recurring infinity loop) instead of popping in and out.
5. **Hierarchy + restraint.** One thing moving at a time; one accent colour (red #FF2A2A) on near-black/white; big
   type, lots of empty space; every element readable in under 2 seconds.
6. **Sound sync.** Every major motion has a sound on its frame (`shared/sfx/manifest.json` `peak_at`), within the
   format's SFX budget.
7. **A consistent system.** The same 5-6 moves, fonts and colours in every video, so the style reads as his. New
   moves enter the system only after he approves them.

## Where references come from

- **Best: screen-recordings of the exact seconds he loves** (Reels/YouTube: Kallaway, Gawx, Ali Abdaal, Johnny Harris,
  Vox, Apple product films). These get measured frame by frame (as in `presets/instagram/references/
  kallaway-split-explainer.md` and `creative-video-editor/references/gawx-cinematic-doc.md`).
- **Galleries:** Dribbble + Behance ("motion graphics", "kinetic typography"), Savee, Pinterest boards,
  Motionographer; Godly and Awwwards for website animation that translates to video.
- **Building blocks:** the HyperFrames registry (~400 blocks: charts, glitch, shimmer, terminals, maps, transitions).
  **Search it before hand-building any named effect** (`hyperframes-registry` skill).
- **Assets:** LottieFiles (animated icons), Mobbin and real product sites (clean UI to recreate as designed windows).

## How the skill learns (the loop)

1. **He sends references** with one line each ("titles should move like this", "this counter", "the transition at
   0:04").
2. **Break each down into numbers:** timing per element (frame-step through it), easing shape, sizes and positions in
   1080x1920 px, colours, fonts, layer order, what triggers each move. Write the breakdown to
   `references/motion/<name>.md` in the skill it belongs to.
3. **Rebuild as a reusable template** in his red/black/white system (a HyperFrames composition or a block with SLOT
   fields), and render a short demo on his own footage (720p review).
4. **He gives timestamped notes** ("at 2 s the text comes in too slow", "the glow is too strong", "use this more").
   Fix → re-render → repeat.
5. **"Save this to the skill"** turns a note into a rule in this file (or the template's notes) and an approved
   template into a named format with an entry in the format table of the preset it belongs to.
6. **Target: his motion system in 3-5 rounds:** ~10 approved templates covering title, pill list, number counter,
   transition, lower third, chapter card, highlight box for screen recordings, progress/step tracker, quote card,
   end card. Track them here:

| Template | Status | File | Notes |
|---|---|---|---|
| title pair (sans + serif italic, red underline) | built (split-explainer) | `presets/instagram/templates/split-explainer/` | awaiting notes |
| glowing frame (photo / B-roll / browser window) | built (split-explainer) | same | awaiting notes |
| number counter ("19 years old") | built (intro Reel, split-explainer) | same | awaiting notes |
| one-word captions red-white / red-black | approved style | `presets/instagram/scripts/ig-captions.py` | user asked for this look |
| chapter card (small red caps) | built | `creative-video-editor/scripts/cine-finish.py --cards` | cinematic only |
| pill list, transition, lower third, highlight box, step tracker, quote card, end card | to build from his references | — | — |

**Next step agreed:** when he sends 3-5 reference clips, build a motion style guide + the first 5 templates (title,
pill list, counter, transition, chapter card) and render a demo on his B-roll for notes.
