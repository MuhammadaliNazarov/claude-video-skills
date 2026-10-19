# Shot lists (every script ends with one)

Sources (studied 2026-10-13): Jeremiah Birnbaum, "How to Make a SHOT LIST" (Movie Mentor, 121k views) and Porker_13,
"Shot List Like a Pro Filmmaker" (32k views), adapted for a phone, one person and a B-roll-heavy Reel.
A shot list turns the script into a filming plan: every shot the edit needs, in the order you'll film it, so nothing
is missing in the edit room.

## Shot vocabulary (abbreviation → what it does)

| Abbr | Shot | Frames | Use it for |
|---|---|---|---|
| EST | Establishing | the place, usually outside | where we are (your campus, a city street, your hometown, a café) |
| WS | Wide | person in the whole environment, wide lens (0.5x / 1x), everything sharp | orientation, walking into a scene |
| LS | Long | same size, **telephoto** (2x-5x): background compressed, soft | cinematic walking shots, "alone in the city" |
| MED | Medium | waist up; neutral, like the eye sees | talking head default, doing an action |
| MCU | Medium close-up | chest up; more intimacy | the talking head for key lines |
| CU | Close-up | neck up, or one object | emotion, a detail that matters. **"Size in frame = importance to the story" (Hitchcock). Shoot many.** |
| ECU/XCU | Extreme close-up | eyes, hands, a keyboard key, coffee pouring | heighten a moment, texture B-roll, transitions |
| POV | Point of view | what he sees (phone at eye height) | laptop screen, a letter, the street ahead; follow with his reaction (CU) |
| OTS | Over the shoulder | behind him toward what he looks at | working, reading, talking to someone |
| INS | Insert | a single object/action cutaway | proof: a screenshot, an acceptance email, a passport |

Angles: eye level (neutral), low (power, ambition), high (small, overwhelmed), top-down (desk, food, hands), Dutch
(unease, sparingly). Movement: static (tripod), handheld (energy, vlog), push-in (realisation), pull-out (reveal),
pan/tilt (follow), walk-and-talk, tracking (follow from behind).

## The columns (one row per shot)

`Scene | Shot | Script line / beat | INT/EXT | Location (specific: "desk by the window", not "dorm") | Time / light |
Type | Angle | Movement | Audio (talk / ambience / none) | Subject | Description (what happens, where the camera is) |
Length to film | Planned cut (L, J, match, action, smash, jump) | Notes`

- **Numbering:** a new scene = a change of time or location (1, 2, 3…); shots are letters (1A, 1B, 1C). Say "scene 2,
  shot C, take 1" on set.
- **Order the list for filming, not for the edit:** group by location and light; inside a location, must-have shots
  first, then wide → close; batch everything at one spot before moving.
- **Combine shots** where one move does two jobs (a push-in from MED to CU; walk past the camera from WS into MCU).
  Fewer, better shots make the shoot faster.

## B-roll rules (he edits B-roll-heavy)

- **Every spoken line gets proof:** plan 1-3 B-roll shots per line of the script, matching the action AND the emotion
  (tired → studying tired; "my parents" → a call home; "my hometown" → old photos, local food, the city).
- **The B-roll formula per action:** WS (where) → MED (what) → CU (detail) → ECU (texture) → POV (his eyes) → reaction
  CU. Five angles of one action = a mini montage and free cut-on-action points.
- **Film for the cut:** hold every shot 5+ s, start 2 s before the action and end 2 s after (handles for J/L cuts and
  transitions); repeat a movement from two angles to cut on action; plan match-cut pairs on purpose (a circle → a
  circle: coffee cup → clock; same framing in two places: dorm door → plane door).
- **Variety:** change at least two of {size, angle, location, light} between consecutive B-roll shots.
- **Close-ups are the most forgotten shot:** at least a third of the list should be CU/ECU/INS.
- **Sound:** record 10 s of room/street tone at every location (fills gaps, smooths J/L cuts); note shots where the
  natural sound is part of the story (keyboard, kettle, train).
- **Phone settings:** 4K 30 fps (24 for cinematic), the 1x lens for faces (0.5x distorts close), lock exposure/focus
  (long-press), 60 fps for anything to slow down, horizon level, clean the lens.

## Process

1. **Know the location:** go there, or ask him for photos of the spot, and write the list there.
2. **Storyboard the important shots** (a stick-figure frame or a reference screenshot per key shot); the hook shot
   always gets one.
3. **Review with someone** (or with Claude): a second pass catches too many shots and missing close-ups.
4. On the day: tick shots off, add a column for "got it / retake".

## Output (append to every script)

```
SHOT LIST — <title>   (~N shots, ~M min to film, locations in filming order)
| Sc | Shot | Line / beat | INT/EXT | Location | Light | Type | Angle | Move | Audio | Description | Hold | Cut |
| 1 | 1A | hook | INT | desk by the window | day, window key | MCU | eye | static | talk | … | full take | — |
| 1 | 1B | "I come from…" | INT | desk | same | INS | top-down | static | none | old photo of your hometown on the desk | 6 s | L-cut over voice |
…
MUST-HAVES: 1A, 2C, 3B
ROOM TONE: desk (10 s), street (10 s)
```
