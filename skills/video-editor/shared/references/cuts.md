# The 10 cuts (and how to do each one here)

Source: Jonny Duncan, "10 Editing Cuts Every Video Editor Should Know" (1.2M views, studied 2026-10-13). Editing is
invisible storytelling: every cut should have a reason. Plan the important ones before filming (shot list).

| # | Cut | What it is / why | Tool here |
|---|---|---|---|
| 1 | **Cut** (standard) | instant switch of picture + sound; "ready for new information" | EDL range boundary (engine `render.py`) |
| 2 | **Jump cut** | a piece removed from the same shot; time skips. Talking heads use it to remove pauses/mistakes; films use it to show time passing | the cut stage (paper cut, dead air); dress with a punch-in (alternate 1.0 / 1.08-1.12 scale) or cover with B-roll |
| 3 | **Match cut** | the next shot matches the last in **shape/colour/framing** (graphic), **movement** (camera/person/object moving the same way) or **sound** (a sound becomes another) | `shared/tools/match-finder.py` finds graphic + movement pairs and action peaks; audio match: end a shot on a sound that the next shot continues (clap → door slam, keyboard → rain) |
| 4 | **J-cut** | the next scene's sound starts **before** its picture: you hear it, then see it. Leads the viewer in | `"split": +N` on the range, then `shared/tools/split-edits.py` |
| 5 | **L-cut** | the current sound **continues after** the picture cuts: you keep hearing the line over the next shot. Bridges, feels natural, great with B-roll over narration | `"split": -N`, `split-edits.py`; B-roll cutaways over the voice track are L/J cuts by construction |
| 6 | **Fade** (to/from black, white) | a story or chapter **begins or ends**; to white = a dream, a memory, a flash, death | `shared/tools/transition-join.py --type fadeblack / fadewhite`, `--head-fade` / `--tail-fade` |
| 7 | **Dissolve** | one shot melts into the next: **time passing** inside a scene or between scenes | `transition-join.py --type dissolve --dur 0.6-1.2` |
| 8 | **Cut on action** | cut in the **middle of a movement**: the out point of shot A continues as the in point of shot B (a hand reaching, a turn, a door opening); hides the cut | `match-finder.py` "CUT-ON-ACTION points"; cut 2-4 frames into the motion and start B at the same phase |
| 9 | **Cross-cutting** | alternate between two things happening **at the same time** (two people on a call, prep vs the event, past vs present) | EDL ranges interleaved A, B, A, B; shorten each return as tension rises |
| 10 | **Smash cut** | abrupt cut to **contrasting** picture and sound: loud/chaotic → silent/calm (or the reverse) for shock or comedy | `transition-join.py --type smash` (sound stops dead, no crossfade); or end a music bed hard on the frame |

## Rules of use

- **Default is the plain cut.** Every other cut needs a reason: time (jump, dissolve), connection (match, J/L),
  continuity (action), contrast (smash), parallel story (cross), beginning/end (fade).
- **Talking-head Reels:** jump cuts for pace; **L-cuts over B-roll** (keep the voice while the picture shows the proof);
  a J-cut into a new section (hear the next line over the last shot); one smash cut per video at most (a punchline or a
  "but then…"). No dissolves in fast Reels; a fade to black only at the very end, if any.
- **Cinematic edits:** match cuts between chapters, J-cuts on ambience (hear the train before you see it), dissolves for
  time, fades to black between parts, cut on action in process montages, cross-cutting for "prep vs the day".
- **Sound sells the cut:** J/L splits of 0.3-1.0 s feel natural; a smash cut needs the outgoing sound to stop dead.
- Captions follow the **sound**, not the picture: after `split-edits.py`, build captions from its `--words-out`.
- Check each special cut by frames (`timeline_view.py` on the output, ±1 s) before showing the user.
