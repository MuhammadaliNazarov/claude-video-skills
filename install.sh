#!/usr/bin/env bash
# Install the three skills into Claude Code and set up their tools. Safe to re-run.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
SKILLS="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
VE="$REPO/skills/video-editor"
ok()   { printf '  \033[32mok\033[0m    %s\n' "$1"; }
warn() { printf '  \033[33mwarn\033[0m  %s\n' "$1"; }

echo "1. Linking skills into $SKILLS"
mkdir -p "$SKILLS"
for d in "$REPO"/skills/*/; do
  name="$(basename "$d")"; target="$SKILLS/$name"
  if [ -L "$target" ] || [ ! -e "$target" ]; then ln -sfn "${d%/}" "$target"; ok "$name"
  else warn "$target exists and is not a link; left alone (move it away and re-run)"; fi
done

echo "2. Python env (uv)"
if command -v uv >/dev/null; then (cd "$VE" && uv sync -q) && ok "$VE/.venv"
else warn "uv not found: brew install uv (or pipx install uv), then re-run"; fi
PY="$VE/.venv/bin/python"; [ -x "$PY" ] || PY=python3

echo "3. Fonts (Google Fonts, OFL)"
"$REPO/scripts/fetch-fonts.sh" >/dev/null && ok "$(ls "$VE/presets/instagram/assets/fonts" | grep -c ttf) fonts"

echo "4. LUTs (generated locally)"
"$PY" "$VE/shared/luts/make_luts.py" >/dev/null && ok "shared/luts"
"$PY" "$REPO/skills/creative-video-editor/scripts/make_gawx_lut.py" >/dev/null && ok "creative-video-editor/luts"

echo "5. ElevenLabs key (for transcription)"
ENVF="$VE/engine/.env"
if [ ! -f "$ENVF" ]; then cp "$VE/engine/.env.example" "$ENVF"; chmod 600 "$ENVF"; warn "add your key to $ENVF"
elif grep -q '^ELEVENLABS_API_KEY=.\+' "$ENVF"; then ok "key present"; else warn "add your key to $ENVF"; fi

echo "6. Tools"
FILTERS="$(ffmpeg -hide_banner -filters 2>/dev/null || true)"
if grep -qE ' lut3d ' <<<"$FILTERS" && grep -qE ' ass ' <<<"$FILTERS" && grep -qE ' zscale ' <<<"$FILTERS"; then ok "ffmpeg (lut3d, ass, zscale)"
else warn "ffmpeg lacks lut3d/ass/zscale: brew install ffmpeg-full && brew unlink ffmpeg && brew link --force --overwrite ffmpeg-full"; fi
command -v hyperframes >/dev/null && ok "hyperframes $(hyperframes --version 2>/dev/null | head -1)" \
  || warn "HyperFrames CLI missing (motion graphics): npm i -g hyperframes"
command -v yt-dlp >/dev/null && ok "yt-dlp" || warn "yt-dlp missing (reference downloads): brew install yt-dlp"

echo "7. Bring your own media (optional)"
[ -f "$VE/shared/sfx/manifest.json" ] && ok "sfx manifest" || warn "no sound effects yet: see skills/video-editor/shared/sfx/README.md"
[ -f "$VE/shared/music/manifest.json" ] && ok "music manifest" || warn "no music yet: see skills/video-editor/shared/music/README.md"
[ -f "$VE/presets/youtube/PRESET.md" ] && ok "YouTube preset" || warn "YouTube preset not installed (optional): see skills/video-editor/presets/youtube/README.md"
[ -s "$REPO/skills/script-writer/creator-profile.md" ] && echo "     fill in skills/script-writer/creator-profile.md so scripts use your story"
echo "Done. In Claude Code: /video-editor, /creative-video-editor, /script-writer"
