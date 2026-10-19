# Claude Video Skills

Three [Claude Code](https://claude.com/claude-code) skills that turn Claude into a short-form video team: a script
writer, an editor, and a cinematic editor. Built for Instagram Reels first (9:16), with YouTube/16:9 support.

| Skill | What it does |
|---|---|
| **`script-writer`** | hooks, full scripts, on-screen text, captions, CTAs, an SFX column and a filming shot list; story structures (normal → explosion → new normal, but/therefore, re-hooks), hook templates by mechanism, talking-head lighting/background setups |
| **`video-editor`** | raw footage → finished file by conversation: transcription (ElevenLabs Scribe), retake + dead-air cuts from an EDL, cinematic LUTs (incl. Apple Log), one-word captions (red/white, red/black, yellow, documentary), HyperFrames motion graphics, B-roll, J/L cuts, transitions, match-cut finder, music beds from the "most replayed" window, a 720p review → 4K + 1080p render ladder |
| **`creative-video-editor`** | the cinematic mode: low-key film grade (generated `Cine_Gawx` LUT), halation, grain, vignette, framed aspect ratios, small red chapter cards, music-led montage rhythm, bookend storytelling |

## Install (macOS)

```bash
git clone https://github.com/MuhammadaliNazarov/claude-video-skills.git
cd claude-video-skills
./install.sh
```

`install.sh` links the skills into `~/.claude/skills/`, creates the Python env (`uv`), downloads the fonts, generates
the LUTs, and checks your tools. Requirements:

- [uv](https://docs.astral.sh/uv/), Python ≥ 3.10
- ffmpeg **with** `lut3d`, `ass`, `zscale` (`brew install ffmpeg-full`)
- [HyperFrames](https://www.npmjs.com/package/hyperframes) CLI for motion graphics (`npm i -g hyperframes`)
- yt-dlp (optional, for reference videos and music heatmaps)
- An [ElevenLabs](https://elevenlabs.io) API key for transcription, in `skills/video-editor/engine/.env`
  (transcription costs Scribe credits; the skill never transcribes unless you hand it footage and ask for an edit)

## Make it yours

1. Fill in `skills/script-writer/creator-profile.md` (your story is the default material for scripts).
2. Add sound effects to `skills/video-editor/shared/sfx/` and music to `skills/video-editor/shared/music/`, then
   index them (`shared/tools/build-manifest.py sfx|music`). Licences don't allow shipping them; the READMEs say where
   to get free ones.
3. Optional: the YouTube preset is built on the WeAreNoCode `youtube-edit` kit, which isn't redistributable; see
   `skills/video-editor/presets/youtube/README.md`.

## Use

In Claude Code, from the folder with your footage:

```
/script-writer   write a 30 s Reel about my first week in a new city
/video-editor    edit IMG_1234.MOV into a Reel with captions and B-roll
/creative-video-editor   make a cinematic 60 s travel film from these clips
```

Every edit follows ask → plan → confirm → render a 720p review → notes → 4K final. Say **"save this to the skill"**
after any note and Claude writes it into the right file, so the skills learn your style.

## Layout

```
skills/
  script-writer/          SKILL.md, creator-profile.md, references/ (hooks, storytelling, research, sfx, shotlist, setup)
  video-editor/           SKILL.md, engine/ (from browser-use/video-use), presets/instagram, presets/youtube (BYO),
                          shared/ (luts, sfx, music, tools, references)
  creative-video-editor/  SKILL.md, scripts/ (make_gawx_lut.py, cine-finish.py), references/
scripts/fetch-fonts.sh
install.sh
```

## Licence

MIT (see `LICENSE`). Third-party components: `THIRD_PARTY_NOTICES.md`.
