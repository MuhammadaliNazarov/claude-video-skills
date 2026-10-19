---
name: creative-video-editor
description: The user's CINEMATIC editing skill, separate from the everyday video-editor. Use only when the user wants something more cinematic, artistic, filmic, moody or "like Gawx" — a personal documentary, a travel film, a making-of, a story Reel with a film look — or says creative, cinematic, film look, moody, aesthetic, short film, Gawx. Low-key red/teal film grade (Cine_Gawx LUT), grain, halation, vignette, framed 4:5 / 1.37:1 / 2.39:1 pictures, small red chapter cards, music-led montage bursts, object close-ups, bookend storytelling with the meaning said out loud. For normal talking-head Reels with one-word captions use video-editor instead.
---

# Creative video editor (cinematic)

The opposite of the fast talking-head Reel: dark, deliberate, music-led, every frame composed. The reference is Gawx
Art's "Perfect Imperfection." (studied in `references/gawx-cinematic-doc.md`, with measured colour, cut rhythm,
typography and structure). Read that file before every project.

## What this skill borrows (read-only) and what it owns

| Borrowed from `video-editor` (don't edit it from here) | Owned here |
|---|---|
| transcription + EDL + per-segment render: `~/.claude/skills/video-editor/engine/` (`$VU_PY $VU/helpers/render.py`, run with `--draft` for 720p review, `--uhd` for 4K, grade `none` so the look is applied once, here) | `luts/Cine_Gawx.cube`, `luts/AppleLog_Cine_Gawx.cube` (rebuild: `scripts/make_gawx_lut.py`) |
| the sound library `~/.claude/skills/video-editor/shared/sfx/` (`manifest.json` peak times) | `scripts/cine-finish.py`: grade + halation + grain + vignette + frame + chapter cards |
| fonts in `~/.claude/skills/video-editor/presets/instagram/assets/fonts/` | `references/cinematic-storytelling.md`: the bookend structure |
| HyperFrames for anything animated | this file's rules |

```bash
VE=~/.claude/skills/video-editor; VU="$VE/engine"; VU_PY="$VE/.venv/bin/python"; CV=~/.claude/skills/creative-video-editor
```

## Workflow

1. **Intake:** the story (what was made / where he went / what changed), the platform (Reel 9:16 by default, YouTube
   16:9 with `--landscape`), the frame shape, music (a calm cinematic or lo-fi track, or he adds trending audio in-app).
2. **Shot plan (before filming, if he hasn't shot yet):** dark room + one practical lamp or window on one side of the
   face; red objects in frame; macro shots of hands and objects; an overhead table shot; a silhouette in a doorway; wide
   static establishing frames; 2-3 handheld or fisheye selfies; golden hour exteriors. Shoot 4K (Apple Log if he wants
   the most grading room).
3. **Structure:** the bookend (`references/cinematic-storytelling.md`): repeating-pattern opening that reveals what's
   missing → origin through objects, numbered → a date that sets stakes → a question → process / journey (one
   music-only montage) → meaning said out loud → the bookend line, completed. Number the chapters.
4. **Cut:** calm narrated stretches (a shot every 3-5 s, holds on faces and objects) alternating with music-only
   montage bursts (a cut every 0.6-1.2 s on the beat). Measured on the reference: average shot 3.0 s, median 1.8 s.
   Let shots breathe; no punch-ins, no zoom-bounces, no one-word captions.
5. **Finish:** `python3 $CV/scripts/cine-finish.py base.mp4 review.mp4 --res 720 --frame 4x5 --cards cards.json`
   (review), then the same with `--res 4k` after approval (render ladder: 720p review, 4K final).
6. **Sound:** music bed + real ambience (trains, streets, room tone); sounds only where the picture makes them
   (`transition/camera-shutter` on photos, `cinematic/remembering-woosh` on memories, `action/*` foley on hands
   working). Master to -14 LUFS, music ducked under narration.
7. **Captions:** small and low, pale yellow (`ig-captions.py --style doc-yellow` from video-editor) or none; chapter
   cards carry the structure.

**Music:** `~/.claude/skills/video-editor/shared/music/` (README "Pick by context": cinematic, deep-reflective,
memories-nostalgia, no-talking-storytelling suit this skill; `music-cut.py` cuts the most-replayed window).

## Motion graphics

Same rules and learning loop: `~/.claude/skills/video-editor/shared/references/motion-graphics.md`. In this skill motion
stays minimal: slow drifts, chapter cards, words spread across the frame; no bouncy UI.

## Cuts (the cinematic grammar)

Read `~/.claude/skills/video-editor/shared/references/cuts.md`. This skill leans on: **match cuts** between chapters and
objects (run `~/.claude/skills/video-editor/shared/tools/match-finder.py` on the B-roll; graphic = same shape/framing,
movement = same direction), **J-cuts on ambience** (hear the train before you see it) and **L-cuts** of narration over
detail shots (`split-edits.py`), **dissolves** for time passing and **fades to black** between parts
(`transition-join.py`), **cut on action** inside process montages, **cross-cutting** for "preparation vs the day",
and one **smash cut** from a loud montage to silence before the meaning line.

## Look settings (cine-finish.py)

| Flag | Default | Notes |
|---|---|---|
| `--lut` | `luts/Cine_Gawx.cube` | `AppleLog_Cine_Gawx.cube` for Apple Log footage |
| `--strength` | 0.85 | 0.6-0.7 for dim selfie footage (keeps the face readable) |
| `--grain` | 6 | 4 subtle, 10 heavy |
| `--halation` | 0.25 | warm glow around highlights (lamps, windows); 0 off |
| `--vignette` | 0.6 | 0 off |
| `--frame` | full | `4x5` (Reel with a picture on black + card below), `137` (the reference's 1.37:1), `239` (scope) |
| `--cards` | — | JSON list of `{text, start, end, pos}`; small red Inter caps, fade 0.3 s |

**Honesty rule:** the look is half lighting. Flat, evenly lit footage graded with Cine_Gawx gets the colour but not
the mood; say so and suggest relighting (one side of the face, rest dark) or using the darker takes.

## Typography (from the reference)

Small red uppercase chapter cards ("1. THE MOVE", "3. THE LAYOUT"), words spread across a wide frame
("SAN · FRANCISCO · 2026"), stacked part titles ("PART TWO / THE BUILD"), credits as a word grid, "THE END" in white +
red. Never big headlines; never more than one line of text on screen at a time.

## Learning

"Save this to the skill" → one rule here or in the reference file. A new cinematic reference gets its own breakdown in
`references/` and, if its colour differs, its own LUT generator in `scripts/`.
