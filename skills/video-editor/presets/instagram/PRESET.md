# Instagram preset (`presets/instagram/`)

Vertical Reels, 1080x1920. This file holds only what is **different for Instagram**. Everything else comes from the two
skills it stands on, and you read them, not just this file:

| Need | Read | Why |
|---|---|---|
| Transcription, the EDL, `render.py`, grade, the Hard Rules, the ask → confirm → execute → self-eval loop | **the engine** `engine/ENGINE.md` + `engine/helpers/` | the engine; its 12 Hard Rules apply here unchanged |
| Retake removal on a raw take (paper cut, tighten, sliver, edge audit, dead air) | **the YouTube preset** (`presets/youtube/PRESET.md`) "Cut stage" | best-in-class cut tools; they work on any aspect |
| Animated overlays (HyperFrames), the format library, glass, camera, sound, traps, verify | **the YouTube preset** "Format library", "Camera", "Sound", "Animating glass", "Traps", "Verify" | the motion know-how; re-laid out for 9:16 by the rules below |
| HyperFrames composition contract, keyframes, registry blocks | the `hyperframes*` skills | how to build and render a vertical composition |
| Sound and image lookup | `media-use` | `resolve` for icons, logos, images; bundled SFX |

When this file and a borrowed rule disagree, **this file wins for Instagram** (pacing, text sizes, captions, safe zones,
music). When in doubt about a borrowed number, scale it: YouTube values are for a 1920-wide frame; on a 1080-wide frame,
positions scale by 0.5625 and text needs to be **larger**, not smaller (phones, arm's length).

```bash
VE=~/.claude/skills/video-editor; VU="$VE/engine"; VU_PY="$VE/.venv/bin/python"; IG=~/.claude/skills/video-editor/presets/instagram
YT=~/.claude/skills/video-editor/presets/youtube; SHARED=~/.claude/skills/video-editor/shared
# outputs: <footage folder>/edit/  (the engine's rule: never inside the skill folder)
```

## Two routes

| The clip | Route |
|---|---|
| Talking head, a few takes, captions + light motion (most Reels) | **Quick:** engine transcribe → `takes_packed.md` → EDL → `render.py` → `ig-captions.py --burn` (captions LAST) |
| A raw take full of retakes ("let me say that again") | **Cut first:** the YouTube preset's Cut stage → flat cut → then Quick or Motion |
| Titles, pills, punch-ins, B-roll, counters, a designed hook | **Motion:** flat cut → a hand-built HyperFrames composition at 1080x1920 → render → captions burned last (or as HTML in the composition) |

`compose.py` from the YouTube preset is **16:9 only**: never run it for a Reel. Build vertical compositions by hand on the
skeleton below, borrowing each format's spec (timings, eases, glass recipe) and re-placing it inside the safe zone.

### Quick route

```bash
$VU_PY "$VU/helpers/transcribe_batch.py" "<footage>"                 # cached per clip; Scribe costs credits: ask first
$VU_PY "$VU/helpers/pack_transcripts.py" --edit-dir "<footage>/edit"
#   read takes_packed.md, propose the strategy, WAIT for a yes, write edit/edl.json (the engine's EDL format)
$VU_PY "$VU/helpers/render.py" "<footage>/edit/edl.json" -o "<footage>/edit/preview.mp4" --preview --no-subtitles
python3 "$IG/scripts/ig-captions.py" --edl "<footage>/edit/edl.json" --style red-white --em "key,words" \
  --out "<footage>/edit/captions.ass" --burn "<footage>/edit/preview.mp4" "<footage>/edit/preview-captioned.mp4"
```

`render.py` scales a portrait source to 1080x1920, tone-maps iPhone HDR to Rec.709, fades every join, and levels to
-14 LUFS. A 16:9 source for a Reel needs a reframe first (crop to 9:16 on the subject, `crop=ih*9/16:ih:X:0`, X from a
frame), never a letterboxed 16:9 in a 9:16 frame unless asked.

### Cut-first route

Run the YouTube preset's Cut stage as written (its transcribe lines already use Scribe + `scribe-words.py`), with
`--maxgap 0.25` on `tighten-cut.py` and `dead-air.py --max 0.30 --max-sentence 0.28 --target 0.18` (Reels breathe less).
`apply-cut.py` keeps the source size; feed its `public/input-video.mp4` to the Motion route, or to `ig-captions.py
--words` (transcribe the flat cut, `scribe-words.py`, then caption) for a captions-only Reel.

## Canvas, safe zones, delivery

- **1080x1920, 30 fps** (keep 24/25 if the source is), H.264 High, yuv420p, BT.709 tags, AAC 48 kHz, -14 LUFS, true
  peak under -1 dBTP. 15 to 60 s performs best; up to 3 min is allowed. Source in 4K vertical when possible (punch-ins).
- **Safe zones** (Instagram UI covers them):
  - top 220 px: the header and the progress bar
  - bottom 420 px: caption, username, audio label
  - right 150 px: the like / comment / share rail
  - **Key text lives inside x 90-930, y 220-1500.** Nothing important bottom-right, ever.
- **The grid crop:** the profile grid shows the middle 1080x1440 (3:4). The cover frame's title sits inside y 240-1680.
  Export a cover: `ffmpeg -ss <t> -i final.mp4 -frames:v 1 cover.png` at the strongest title frame.
- **Render ladder:** review at 720p, final at 4K (2160x3840) after approval; see the root SKILL.md "Render ladder".
- **Deliver** to `~/Movies/Instagram Renders/<project>/<project>.mp4` + `cover.png` + a no-music twin when music was
  added (so the user can attach trending audio in the app). Open from Finder; AirDrop to the phone.

## Captions (`scripts/ig-captions.py`)

Word-timed from the Scribe transcript, burned **last** (after every overlay), fonts from `assets/fonts/`. Pick the style
by the vibe of the footage and say which one you picked at the strategy step.

**The user's palette is red + black + white. They do not like cyan: never propose cyan.** The default is `red-white`,
one word on screen at a time (the Kallaway look, see `references/kallaway-split-explainer.md`).

| Style | Look | Pick when |
|---|---|---|
| `red-white` | **ONE word at a time**, Inter Black 86 px, tracking -3.2, white with a soft dark halo, key words red `#FF2A2A`, punctuation kept, each word held until the next one, no pop, at `--pos ref` (64% down) | **the default**: talking-head explainers, storytelling, business, any Reel |
| `red-black` | ONE word at a time, black Inter Black 76 px on a red box | loud, high-energy, hooks, light or busy backgrounds |
| `red` | ONE word at a time, every word red with a soft black halo, key words white | dark or dramatic footage |
| `yellow-white` | white, the key word lemon `#F4F25C`, 3 words a cue, a 90 ms pop | only when asked for yellow |
| `cyan-white` | the same with cyan | only if the user asks for cyan by name |
| `doc-yellow` | Inter Medium 54 px, the whole line pale yellow `#F3E8A6`, thin outline, sentence case, up to 7 words, no pop, low | documentary, storytelling, cinematic, calm voice-over, film looks |
| `yellow` | Anton 118 px, all lemon yellow, UPPERCASE, 2 words | a loud hook or a one-word punch, short stretches only |

- **Key words** (`--em`): one per cue at most; the word that carries the point (the number, the result, the twist).
  Numbers highlight automatically. Never highlight filler or a whole sentence.
- **Position:** one-word styles default to `--pos ref` (64% down, just above a docked speaker card; also right on a
  full-screen face's chest); `--margin-v N` sets an exact spot (the split template with selfie footage uses 790).
  Others: `middle`, `lower` (doc), `upper`. Always check a frame: a caption never covers the mouth or eyes.
- Cues break on punctuation and on pauses of 0.3 s or more, hold 0.12 s past the last word, and never overlap.
- No captions over a full-frame title that already says the words.

## Formats learned from references

| Format | Template | Breakdown |
|---|---|---|
| **Split explainer** (Kallaway): black dot-grid stage on top, speaker in a rounded card at the bottom, title pair (heavy sans + serif italic with a red glowing underline), glowing objects landing on their words, a full-screen speaker break every 10-15 s, one-word captions, 240 wpm with every pause cut, a ducked bass bed | `templates/split-explainer/index.html` (copy into `public/`, edit the SLOT and TIMELINE blocks; card geometry notes for mid-shot vs selfie footage at the top of its script) | `references/kallaway-split-explainer.md`: structure with times, layout numbers, fonts, motion, sound, recreate checklist |

Read the breakdown before building that format; add a new row (template + breakdown) for every reference studied.

## Title text and graphics (the look)

From the references the user collected (Reels that do well right now). **One loud font, one quiet one:**

| Role | Fonts (in `assets/fonts/`) | Use |
|---|---|---|
| Loud headline | Anton, Bebas Neue, Archivo Black, Ultra, Montserrat Black | the hook title, a big number, one word that lands; huge (180 to 260 px), tight leading, top third (y 240-700) |
| Quiet support | Inter Medium/Bold, Montserrat SemiBold, Poppins Bold | sub lines, labels, captions |
| Elegant / cinematic | Playfair Display (italic), Instrument Serif, EB Garamond | aesthetic, story, luxury; pair a serif word with a sans word ("Follow" + "FOR MORE") |
| Handwritten accent | Reenie Beanie | one word or an arrow note, never a sentence |

- **Colours:** red `#FF2A2A` (neon glow: `0 0 26px rgba(255,42,42,.8)`), dim red `#7A1414`, white, near-black
  `#0A0A0A`. Lemon `#F4F25C` and documentary yellow `#F3E8A6` only when asked. No cyan. Two colours a frame at most.
- **Eyebrow labels:** 24 to 28 px Inter Bold, UPPERCASE, letter-spacing .4em, white, above a headline ("TITLE FONT").
- **Pill labels** for a short list of names: white boxes (radius 8, padding 8x14), black 34 to 40 px text, in a row,
  one pill per word as it is said.
- **Headline + key word:** "Use these **fonts**": white bold with the key word yellow, the same rule as the captions.
- **Motion:** words rise 0.35 to 0.4 s `power2.out`; out 0.3 s. No bounces, no typewriter for headlines. A headline may
  sit behind the head with the subject matte (`npx hyperframes remove-background`), YouTube preset format 1.
- **Text over a busy background** gets a soft shadow (`0 6px 30px rgba(0,0,0,.35)`), never a box (pills excepted).

Formats that translate well to 9:16 (YouTube preset numbers): 2 lower line → captions; 5 punchline chip; 41 pills; 4a
logo card (centred, 420 px plate, y 300-750); 24 stat tiles (stacked); 33 search; 42 chat (phone/float); 13b AI chat
window; 20c clip / B-roll; 35 masked title; 37 image reveal; 10 success stamp; 17 vignette. Skip the long-form doctrine,
chapter tags, slot wall, deck, subscribe bar and description pointer.

## Vertical composition skeleton

```html
<div id="root" data-composition-id="reel" data-start="0" data-duration="D" data-fps="30" data-width="1080" data-height="1920">
  <div id="video-zoom">   <!-- the camera; transform-origin 50% 18% keeps the head in frame -->
    <video id="bg-video" src="input-video.mp4" playsinline data-has-audio="true" data-start="0" data-duration="D" data-track-index="1"></video>
  </div>
  <div id="title" class="clip" data-start="..." data-duration="..." data-track-index="3">...</div>
  <audio id="sfx-pop" src="sfx/pop.mp3" data-start="..." data-duration="0.4" data-track-index="10" data-volume="0.34"></audio>
</div>
```

`html, body` and the root are 1080x1920. Copy fonts with `cp "$IG/assets/fonts/"*.ttf public/fonts/` and declare each
with `@font-face` (`font-display: block`), then assert they loaded (`document.fonts.check('400 200px "Anton"')`). GSAP:
`cp "$YT/assets/vendor/gsap.min.js" public/vendor/`. Sounds: `cp "$SHARED/sfx/"*.mp3 public/sfx/`. Then
`hyperframes check public`, snapshots at every beat (`hyperframes snapshot`), read them, `hyperframes render public -o
out.mp4`, BT.709 remux (YouTube preset Pipeline step 6), captions burned, `verify-render.py --res 1080x1920` if it applies.

## Colour grade (LUTs in `$SHARED/luts/`)

Every Reel gets a look unless the user says "no grade". Built by `make_luts.py` (rerun it after changing a look):

| LUT | Footage in | Look | Pairs with |
|---|---|---|---|
| `Cine_TealOrange.cube` | normal iPhone/camera video | teal shadows, warm highlights, S-curve, muted greens | red-white captions; travel, lifestyle, hype |
| `Cine_Film.cube` | normal | lifted blacks, soft contrast, cream highlights | doc-yellow; storytelling, documentary, vlogs |
| `Cine_Moody.cube` | normal | darker mids, cool blue-teal shadows, low saturation | red or red-white; night, tech, serious |
| `AppleLog_to_Rec709.cube` | **Apple Log** | the technical conversion only (filmic shoulder) | a clean, natural look |
| `AppleLog_Cine_*.cube` | **Apple Log** | the conversion and the look in one LUT | as above |

- **Is it Log?** Apple Log looks flat and grey before grading. Check `ffprobe -show_entries stream=color_transfer,color_primaries,codec_name`
  (Apple Log: ProRes, bt2020 primaries). render.py tone-maps only `arib-std-b67`/`smpte2084` sources: if a Log file is
  tagged HLG, re-tag it first (`ffmpeg -i in.mov -c copy -color_trc unknown log.mov`) so the LUT is the only conversion.
  Normal iPhone HDR (HLG) is tone-mapped by render.py first, then the normal-footage LUT applies on top.
- **In the EDL:** `"grade": "lut3d=file=$HOME/.claude/skills/video-editor/shared/luts/Cine_TealOrange.cube:interp=tetrahedral"`
  (applied per segment during extraction, Hard Rule 2). Add a trim after it when a shot needs one:
  `...,eq=brightness=0.02:saturation=1.05`.
- **Strength:** at 60%: `split[a][b];[b]lut3d=file=<cube>:interp=tetrahedral[g];[a][g]blend=all_expr='A*0.4+B*0.6'`.
- **Motion route:** grade `input-video.mp4` with the same filter before it goes into `public/`.
- **Check skin** on a frame before and after (a side-by-side `hstack`), and keep every clip in one Reel on the same LUT.
  One grade per video; a different look per shot reads as a mistake.

## Motion graphics

Check every animation against `$SHARED/references/motion-graphics.md` (meaning, easing, depth, continuity,
restraint, sound sync, one system); add approved templates to its tracker.

## Cuts (read `$SHARED/references/cuts.md`)

The 10 cut types with tools (`$SHARED/tools/split-edits.py` for J/L, `transition-join.py` for fades/dissolves/smash,
`match-finder.py` for match cuts and cut-on-action points). For Reels: jump cuts for pace, **L-cuts over B-roll**
(voice continues over the proof shot), a **J-cut** into each new section, at most one **smash cut** (punchline or
"but then…"), **cut on action** when B-roll shows movement; no dissolves; fade only at the very end. Name the cut type
for each special transition in the plan so it is a decision, not an accident.

## Pacing and camera (Reels)

- **Frame one is the hook:** a moving image plus the promise as on-screen text by 0.3 s. It must work muted. No logo
  intro, no "hey guys".
- Something changes every 1.5 to 3 s: a cut, a punch-in, a title, a B-roll. Pauses over 0.3 s go (`dead-air.py`
  numbers above). Keep the last take of every line (paper-cut does).
- **Camera:** top-anchored origin (`50% 18%` on a vertical frame); punch 112 to 120% in 0.25 s on the key word, back to
  100% at every cut. 1080x1920 sources hold about 115%; 4K vertical holds 150%. 3 to 6 moves per 30 s.
- End on the payoff or a loop back to the first frame (a seamless loop replays). No outro card; a one-line "Follow for
  more" is fine when the user wants it.

## Sound (free library, Instagram rules)

- **Effects:** `$SHARED/sfx/` is your sound library (bring your own, see `$SHARED/sfx/README.md`): categorised folders (meme, ui, transition, cinematic, action, cartoon, gaming) plus a core set of free effects, peak-normalised to -3 dBFS; use `manifest.json`'s `peak_at` to place each hit. Suggested core set: typing, key-press,
  click, click-soft, pop, ping, notification, chime, sparkle, riser, impact-bass-1/2, glitch-1/2/3, whoosh,
  whoosh-short, whoosh-cinematic, error. Reels allow more sound than YouTube: a whoosh on a fast transition, an impact
  on a big title, a riser into the reveal, a pop on each pill. Still tie each to something on screen, about 1 per 3 s at
  most, and never let one cover a spoken word.
- **Script SFX cues:** a script from `script-writer` carries an SFX column (`folder/name @ "word"`). Place each at
  that word's start minus the file's `peak_at` (`$SHARED/sfx/manifest.json`); keep its budget; skip a cue that would sit
  on a stressed syllable and say so.
- **Music library:** `$SHARED/music/` (78 tracks, categorised by context; read `$SHARED/music/README.md`, browse
  `python3 $SHARED/music/music-cut.py --list --context <tag>`, cut a bed from its most-replayed window with
  `music-cut.py <id> --len N -o bed.mp3`). Propose a track id at the strategy step.
- **Music:** best done in the Instagram app (trending audio gets reach): deliver the no-music twin. For a bed in the
  file, the user names a track or link; `yt-dlp -x --audio-format mp3 -o "$SHARED/music/%(title)s.%(ext)s" <url>`, then
  duck it under the voice (the YouTube preset's "Sound" ducking command; -18 dB under speech on a Reel). Instagram may mute
  or block a copyrighted track it recognises; say so once when the user picks a famous song.
- More effects on demand: `media-use` `resolve --type sfx` (the bundled set answers without an account; its catalog and
  `--type bgm` need the `heygen` CLI signed in, which the user does themselves).

## Strategy step (what to ask for a Reel)

Ask only what the material leaves open: the hook line, the caption style (propose one from the table), whether there is
a title card, music in the file or in the app, length target, and the Instagram handle if a "follow" line is wanted.
Then the 4 to 8 sentence plan, and **wait for a yes** (engine Hard Rule 11).

## Keeping the preset yours

"Save this to the skill" after a note: write it as one plain rule in the section above it belongs to (captions, look,
pacing, sound). A rule that is the same on YouTube goes into `presets/youtube/PRESET.md` instead and this file keeps pointing there.
A new caption style is a row in the table plus an entry in `STYLES` in `scripts/ig-captions.py`.
