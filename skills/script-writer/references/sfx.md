# Sound effects for scripts

Every script row gets an SFX cell: a file from the editor's library, or `—` (silence is a choice). The editor
(`video-editor`) places each cue at `word_time - peak_at` from `~/.claude/skills/video-editor/shared/sfx/manifest.json`,
so name the **exact word** the sound lands on.

Library: `~/.claude/skills/video-editor/shared/sfx/`, **75 sounds**, all at -3 dBFS.
Write cues as `folder/name` (root files have no folder): `cinematic/hit`, `ui/mouse-click`, `whoosh-short`.

## Budget (how many per video)

| Format family | Sounds | Why |
|---|---|---|
| Text on screen + trending song (most Advice / Opinion / Easy / Relatable) | **0-2** | the song is the soundtrack; only add a hit on the beat-drop line or a pop on a pill |
| Talking head / explainer | **1 per ~3 s at most**, never over a spoken word's stress | punctuate reveals, numbers, cuts to B-roll |
| Storytelling (normal → explosion → new normal) | **4-8 in 60 s**, clustered at the explosion and the win | sound marks the turning points, not every line |
| Calm / reflective (car talk, quote to camera, gratitude) | **0-1** | a sound breaks the intimacy |
| Comedy / relatable meme | 1-3 meme sounds, **on the punchline only** | overuse kills the joke |

## Beat → sound (the map)

| The line / beat | First choice | Alternatives | Never |
|---|---|---|---|
| **Hook: bold claim or shocking number** | `cinematic/hit` on the key word | `impact-bass-1`, `cinematic/boom` (short trim) | a meme sound on a serious hook |
| **Hook: curiosity / mystery** ("nobody talks about this") | `cinematic/metallic-rise` into the last word | `riser` (trim to 1.5 s) | |
| **Lock-in / "here's what happened"** | `—` | `transition/woosh-1` if cutting to B-roll | |
| **Cut to B-roll / scene change** | `transition/woosh-1` (fast) | `transition/woosh-2`, `whoosh-short`, `transition/woop` (playful) | a whoosh under on-screen text appearing |
| **Flashback / "3 years ago" / old photo** | `cinematic/remembering-woosh` | `transition/reverse-playback`, `transition/film-burn` (trim), `transition/camera-shutter` on a photo | |
| **Age stamp / timestamp line** ("16 years old:", "7:44 PM") | `ui/digital-beep` or `ui/toggle`, soft | `transition/camera-shutter` for photos | a sound on every stamp (pick 2-3) |
| **Struggle / sad beat / rock bottom** | `cinematic/downer` | `cinematic/heartbeat` (tension, trim 2-3 s), music dips instead | cartoon or gaming sounds |
| **Rising tension before the turn** | `cinematic/heartbeat` → cut | `riser`, `cinematic/energy-fields` (trim, fade) | |
| **THE EXPLOSION / turning point** ("until I…", "so I quit") | `cinematic/hit` or `cinematic/boom` | `impact-bass-2`, `glitch-1` (tech story) | |
| **Re-hook** ("but here's the thing…", "step 3 is where…") | `transition/woosh-2` or a music drop | `cinematic/metallic-rise` (short) | stacking two sounds |
| **Numbered point lands** ("1. Stakes") | `pop` or `click-soft` | `ui/mouse-click`, `cartoon/pop` | |
| **A number counting up / stats** | `ui/glitchy-counter` (trim to the count) | `ui/digital-loading` | |
| **Money / earnings** | `gaming/coin-collect` (quiet) | `chime` | a cash sound on a vulnerable money story |
| **Win / milestone / achievement** ("I got in", "first $1,000") | `gaming/level-up` | `gaming/level-complete`, `sparkle`, `chime` | |
| **Growth / transformation montage** | `gaming/power-up` (start) → `sparkle` (end) | `cinematic/metallic-rise` | |
| **App / phone / screen recording** | `ui/mouse-click` per click, `ui/keyboard-typing` while typing | `ui/notification-sound` for a DM/notification, `typing` | clicks with no cursor on screen |
| **Glitch / AI / tech reveal** | `ui/glitch` | `glitch-2`, `glitch-3` | |
| **Mistake / fail / "it flopped"** | `cartoon/womp-womp` (funny) or `cinematic/downer` (sincere) | `meme/bruh`, `error` | womp-womp on a real loss |
| **Punchline / ironic beat** | `meme/vine-boom` | `meme/huh`, `meme/bonk`, `cartoon/boing` | more than one per 15 s |
| **Exit / "I left" / running away** | `cartoon/running` (funny) | `transition/woosh-2` | |
| **Warning / "stop doing this"** | `gaming/health-low-beeps` (short) | `error` | |
| **Action on screen** (cooking, coffee, cleaning, pouring) | the matching `action/*` sound under the shot | `action/pouring-water`, `action/stir-coffee-and-tea`, `action/sponge`, `action/boiling-juicy-dishes` | |
| **Paper / document / list appears** | `transition/paper-slide` | `action/paper-swipe` | |
| **CTA** ("comment STORY", "follow to see") | `—` or `ui/notification-sound` (soft) | `pop` on the keyword | a big hit (it reads as an ad) |
| **Ending loop back to the hook** | the hook's sound again | | |

## Rules

- **Name the word:** `cinematic/hit @ "quit"`. The editor lines the transient up with that word.
- **One sound per beat**, never two at once; never over the stressed syllable of a spoken word (put it in the gap
  before or on the cut).
- **Meme / cartoon / gaming packs = playful formats only.** Serious stories use cinematic + transition + ui.
- Long files (vortex 26 s, film-burn 30 s, energy-fields 14 s, glitchy-counter 14 s, brushing 15 s, heartbeat 8 s)
  are beds: write the length you want ("heartbeat 2.5 s, fade").
- If the video uses a trending song, write `music drop @ "<word>"` instead of a hit; the drop is the sound.
