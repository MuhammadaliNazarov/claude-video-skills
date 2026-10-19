---
name: video-editor
description: The user's one video editing skill. Edit any video by conversation, from raw footage to a finished file. Instagram Reels / vertical 9:16 (the default; the user mainly posts on Instagram), YouTube 16:9 hooks and long form, and anything else (montage, travel, interview, tutorial, screen recordings). Transcribes with ElevenLabs Scribe, cuts retakes and dead air, colour grades with cinematic LUTs (including Apple Log), adds word-timed captions (one word at a time in red/white or red/black by default; yellow and documentary styles too), split-explainer layouts learned from reference Reels, HyperFrames motion graphics, punch-ins, B-roll, free sound effects, music beds, and renders locally. Use whenever the user drops footage, names a video file, or says edit, cut, Reel, Instagram, YouTube, captions, subtitles, grade, LUT, Apple Log, animate, overlay, highlight this screen recording, or render.
---

# Video editor

One skill, three parts. Read this file, then **the engine rules and the one preset that fits**, before touching footage.

| Part | Read | What it holds |
|---|---|---|
| Engine | `engine/ENGINE.md`, `engine/helpers/` | transcription (Scribe), `takes_packed.md`, the EDL, `render.py`, `grade.py`, `timeline_view.py`, the 12 Hard Rules, the ask → confirm → execute → self-eval loop. Adapted from browser-use/video-use (MIT). |
| Instagram preset | `presets/instagram/PRESET.md` | vertical 1080x1920: safe zones, Reel pacing, caption styles (`scripts/ig-captions.py`), title fonts (`assets/fonts/`), colour grade rules, free sound rules |
| YouTube preset | `presets/youtube/PRESET.md` | 16:9 / 4K: the cut stage (paper cut, tighten, sliver, edge audit, dead air), the HyperFrames composer and its ~40-format library, camera, sound, B-roll, Tella, assembly, verify. Adapted from the WeAreNoCode youtube-edit kit; **optional, not bundled** (`presets/youtube/README.md`). If `PRESET.md` is missing there, use the engine's own cut rules. |
| Shared | `shared/` | `luts/` (Cine_TealOrange, Cine_Film, Cine_Moody, AppleLog_to_Rec709, AppleLog_Cine_*; `make_luts.py` rebuilds them), `sfx/` (your sound effects, -3 dBFS, `manifest.json`), `music/` (your tracks), `tools/` (`build-manifest.py`, cut tools), `img/` |

**Scripts come first:** when the user has no script yet, or asks for hooks, ideas or a caption, use the `script-writer` skill; its scripts end with editor notes this skill executes.

## Which preset

| The request | Use |
|---|---|
| Instagram, Reel, story, TikTok, Shorts, vertical footage, or no platform named with vertical footage | **Instagram preset** (it borrows the cut stage, formats, camera and sound from the YouTube preset; it says where) |
| YouTube, a hook, long form, 16:9 / 4K, a Tella tutorial, assembling sections | **YouTube preset** |
| Anything else (a montage, travel, an interview, a general 16:9 edit) | **Engine** alone, plus `shared/` looks and sounds; borrow preset rules where they fit |
| A screen recording to highlight | the preset for where it will be posted: zoom on the region, dim or blur the rest, a box or underline on the word, click and typing sounds, private data blurred; on a Reel, the recording sits in a phone or browser frame or is cropped to the part that matters |

Not sure? Ask once: "Is this for Instagram or YouTube?"

## Paths (use these in every command)

```bash
VE=~/.claude/skills/video-editor; VU="$VE/engine"; VU_PY="$VE/.venv/bin/python"
IG="$VE/presets/instagram"; YT="$VE/presets/youtube"; SK="$YT"; SHARED="$VE/shared"
```

All outputs go in `<footage folder>/edit/` (the engine's Hard Rule 12); never write inside `$VE` except when saving a
rule, a LUT or a shared asset on purpose.

## Hard rules that span everything

- **Transcription costs money (Scribe credits).** Never transcribe unless the user handed over footage and asked for an
  edit. Transcripts are cached per file stem; delete a flat cut's cached JSON after re-cutting it.
- **Strategy before execution:** describe the material, propose the plan (preset, caption style, look, music, length),
  wait for a yes.
- **Captions and subtitles go on last**, after every overlay.
- **Grade once per video**, per segment during extraction; protect skin; check a before/after frame.
- **Verify the rendered file** (frames at every cut, loudness -14 LUFS, duration) before showing it.
- Python helpers run with `$VU_PY`; the system `python3` lacks numpy.

## Cut types

`shared/references/cuts.md`: the 10 cuts (cut, jump, match, J, L, fade, dissolve, cut on action, cross-cutting, smash)
with when to use each and the tool that does it (`shared/tools/`). Both presets and the cinematic skill use it.

## Motion graphics

`shared/references/motion-graphics.md`: the 7 quality rules every animation is checked against, where references
come from, the learning loop (reference → numbers → template → notes → saved), and the template tracker. Read it before
building any animation; search the HyperFrames registry before hand-building an effect.

## Render ladder (always, every video)

1. **Review render at 720p** (fast; what the user watches and gives notes on):
   engine `render.py … --draft` (720x1280 / 1280x720), HyperFrames `render … --quality draft` on a copy of the
   composition at 720 wide or the default with `-o review.mp4` then `scale=720:-2`; captions with
   `ig-captions.py --width 720 --height 1280`. Self-eval runs on this file.
2. **Final at 4K only after the user approves the review** (no notes left):
   engine `render.py … --uhd` (2160x3840 vertical / 3840x2160 landscape, CRF 18), HyperFrames
   `render … --resolution portrait-4k --quality high` (or `landscape-4k`; the 1080x1920 composition renders at 2x DPR,
   so text and graphics are truly sharp), captions `ig-captions.py --width 2160 --height 3840` (same layout, scaled),
   music/loudness master as usual (-14 LUFS). Verify: `ffprobe` shows 2160x3840, BT.709 tags, duration matches review.
3. **Deliver both** next to each other: `<project>-4k.mp4` (the master, for upload / YouTube / archive) and
   `<project>-1080.mp4` (a high-bitrate 1080x1920 copy, ~20 Mb/s, made from the 4K master with `scale=1080:-2:flags=lanczos`).
   Tell the user honestly: Instagram plays Reels at up to 1080x1920 and re-encodes every upload, so 4K helps by giving
   its encoder the cleanest source (and keeps YouTube/TikTok/future re-use at full quality), not by showing 4K; turn on
   Instagram > Settings > Media quality > "Upload at highest quality". Footage shot in 1080p is upscaled in the 4K
   master (no new detail); say so when that is the case. A note after the final costs a 720p review again, then 4K.

## Machine setup (`install.sh` at the repo root does most of this)

| Tool | State | Check |
|---|---|---|
| ffmpeg **full** build (libass, zscale, lut3d) | `ffmpeg-full` linked over `ffmpeg` | `ffmpeg -filters \| grep -E " (ass\|zscale\|lut3d) "`; if missing: `brew unlink ffmpeg && brew link --force --overwrite ffmpeg-full` |
| Python env | `$VE/.venv` (requests, numpy, pillow, librosa, matplotlib) | `cd $VE && uv sync` |
| ElevenLabs key | `$VU/.env` (mode 600) | `curl -s -o /dev/null -w '%{http_code}' -H "xi-api-key: $(sed -n 's/^ELEVENLABS_API_KEY=//p' $VU/.env)" https://api.elevenlabs.io/v1/user` → 200 |
| Node + HyperFrames CLI | Node 26, `hyperframes` global | `hyperframes doctor` |
| HyperFrames agent skills | installed by the CLI as their own skills (`hyperframes`, `hyperframes-core`, `-animation`, `-keyframes`, `-registry`, `media-use`, ...) | `hyperframes skills check`; read them for the composition contract |
| auto-editor, yt-dlp, Chrome | installed | `auto-editor --version`, `yt-dlp --version` |
| YouTube preset tests (if installed) | all pass | `cd $YT/scripts && $VU_PY -m unittest tests` |

## Keeping it yours

- **"Save this to the skill":** write the note as one plain rule where it belongs: Instagram-only → the Instagram
  preset; YouTube-only → the YouTube preset; both → the shared section of the YouTube preset (the Instagram preset points
  there) or this file when it is about routing or setup. Replace a rule a new one contradicts; never keep both.
- New look: edit `LOOKS` in `shared/luts/make_luts.py`, run it with `$VU_PY`, add a row to the Instagram preset's
  colour table. New caption style: a row in the caption table + an entry in `STYLES` in `ig-captions.py`.
- **Engine updates:** clone the upstream https://github.com/browser-use/video-use somewhere (`git pull`) and compare
  `diff -r <clone>/helpers $VU/helpers` and copy changes in by hand; the engine copy has local path edits
  only in `ENGINE.md`.
