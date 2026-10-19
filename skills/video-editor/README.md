# video-editor

One Claude Code skill for all video editing (linked at `~/.claude/skills/video-editor` by `install.sh`).

- `SKILL.md`: the entry point: which preset, paths, setup, how it learns
- `engine/`: transcription, cut lists, render (from github.com/browser-use/video-use, MIT); API key in `engine/.env`
- `presets/instagram/`: Reels, the default: captions, fonts, safe zones, pacing
- `presets/youtube/`: optional, bring the WeAreNoCode youtube-edit kit (see its README)
- `shared/`: cinematic LUTs (+ Apple Log, generated), your sound effects and music, cut tools, references

Say "save this to the skill" after any note and Claude writes it into the right file.
