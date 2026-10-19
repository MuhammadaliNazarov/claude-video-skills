# Sound library (bring your own; peak-normalise to -3 dBFS)

`manifest.json` lists every file with its duration and **`peak_at`** (seconds into the file where the transient
hits). Place a sound at `event_time - peak_at` so the hit lands on the frame (YouTube preset "Sound" rule).


| Folder | Sounds | Use on |
|---|---|---|
| (root) core 19 | typing, key-press, click, click-soft, pop, ping, notification, chime, sparkle, riser, impact-bass-1/2, glitch-1/2/3, whoosh, whoosh-short, whoosh-cinematic, error | the default set (HyperFrames / Pixabay) |
| `meme/` | vine-boom, roblox-oof, bonk, ahhh, bruh, core, huh, taco-bell-bell | comedy beats, a punchline, a fail; Relatable / humour Reels only, never on a serious line |
| `ui/` | notification-sound, mouse-click, keyboard-typing, toggle, glitch, digital-loading, glitchy-counter (13.9 s, trim it), digital-beep | screen recordings, app windows, a number counting up, a toggle or checkbox |
| `transition/` | woosh-1, woosh-2, deep-woosh, camera-shutter, film-burn (30 s, trim), reverse-playback, woop, paper-slide | a cut into B-roll, a photo landing (shutter), a flashback (reverse), a card sliding in (paper) |
| `cinematic/` | metallic-rise, boom, hit, remembering-woosh, downer, heartbeat, energy-fields, vortex | a title slam (hit / boom), a reveal (metallic-rise into hit), a memory (remembering-woosh), a sad turn (downer), tension (heartbeat) |
| `action/` | brushing, deck-brushing, sponge, boiling-juicy-dishes, stir-ice-in-the-glass, stir-coffee-and-tea, pouring-water, paper-swipe | foley that matches the picture: cooking, coffee, cleaning, paper |
| `cartoon/` | pop, running, punch, womp-womp, blinking, slide-whistle, boing, ricochet | playful edits, a fail (womp-womp), a quick exit (running) |
| `gaming/` | coin-collect, power-up, level-up, health-low-beeps, pixelated-explosions, level-complete, laser, jump | wins and milestones (level-up / level-complete), money (coin-collect), a warning (health-low-beeps) |

Rules: a sound must match something on screen; about one every 3 s on a Reel at most; never over a spoken word;
long beds (vortex, energy-fields, film-burn, glitchy-counter, brushing) get trimmed and faded (`afade`).
## Filling it (nothing ships with the repo)

Sound-effect licences (Pixabay's included) don't allow redistributing the files as a pack, so download them yourself:

1. Get free effects from [Pixabay sound effects](https://pixabay.com/sound-effects/) or run
   `hyperframes skills update media-use` and use its sound search. Name them as in the table above (`whoosh.mp3`,
   `transition/camera-shutter.mp3`, `cinematic/hit.mp3`, ...) so the skills find them; anything missing is skipped.
2. Optional: peak-normalise each to -3 dBFS (`ffmpeg -i in.mp3 -af volumedetect -f null -` shows `max_volume`; apply
   `-af volume=<-3 minus max>dB`).
3. Build the index: `$VU_PY $VE/shared/tools/build-manifest.py sfx` (writes `manifest.json` with `duration`,
   `peak_at`, `category`).
