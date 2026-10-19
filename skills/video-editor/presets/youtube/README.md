# YouTube preset (not included)

The YouTube preset is built on the **WeAreNoCode `youtube-edit` kit** (cut stage, HyperFrames composer and format
library, camera, sound, B-roll, Tella, assembly), which is not openly licensed, so it isn't redistributed here.

To use it:

1. Get the kit from WeAreNoCode (the original source; check its terms).
2. Copy its contents into this folder so that `presets/youtube/PRESET.md` and `presets/youtube/scripts/` exist.
3. Run its tests: `cd presets/youtube/scripts && $VU_PY -m unittest tests`.

Without it, everything else works: the Instagram preset falls back to the engine's own cut rules, and 16:9 edits use the
engine + `shared/` (see `SKILL.md`, "Which preset").
