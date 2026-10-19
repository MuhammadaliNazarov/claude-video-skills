# Music library (bring your own)

`manifest.json` holds every track: `id`, file, title, artist, `mood`, `contexts`, `vocals`, `bpm`, `duration`,
`drop_at` (biggest energy jump) and **`best_window`** (the 15 s to start from). Pull a bed with `music-cut.py`
(browse with `--list --context <tag>`).

## Filling it (nothing ships with the repo; music is copyrighted)

1. Put tracks in sub-folders named by context (the folder name becomes the first context tag), e.g.
   `shared/music/educational/track.mp3`, `shared/music/emotional-sad/other.mp3`.
2. Build the index: `$VU_PY $VE/shared/tools/build-manifest.py music` (bpm, `drop_at`, `best_window` = loudest 15 s).
3. Better windows (optional): the best start is the 15 s viewers replay most. For a song on YouTube, yt-dlp exposes the
   "most replayed" heatmap (`yt-dlp -J <url> | jq .heatmap`); put the peak segment's start in `best_window`
   (cross-correlate with librosa if the YouTube version is offset from your file). Edit `mood`, `contexts`, `vocals`
   (`instrumental` / `vocals`) by hand; re-running the builder keeps them.

## Pick by context

| Context | Use for |
|---|---|
| `educational` | talking head teaching, explainers, tips (instrumental or soft vocals under speech) |
| `storytelling` (spoken) | life story with voice |
| `no-talking-storytelling` | text-on-screen journeys, age stamps, photo timelines (piano intros work well) |
| `deep-reflective` | late-night thoughts, lessons, car talks |
| `emotional-sad` | struggle, loss, homesickness |
| `memories-nostalgia` | old photos, "core memories", tributes |
| `motivational` / `challenge` | discipline, "day X of…", gym, grind, do-it-scared |
| `transformation` | before/after, glow-up, progress |
| `hype-flex` | wins, money, confidence |
| `aesthetic-vlog` / `travel` | day in the life, cities, cafés |
| `romantic` | couples, crushes |
| `relatable-reframe` / `opinion` | "negative thought → reframe" lists, permission lists, opinions |
| `comedy` | punchlines, irony |
| `cinematic` | slow, filmic beds for the creative-video-editor skill |

## Rules

- **Under a voice:** prefer `vocals: instrumental` tracks; duck the bed ~16-19 dB under speech (editor skill).
- **Text-on-screen formats:** start the bed so its drop (`--at drop --lead N`) lands on the reveal line.
- **Best window** is usually the part people recognise; start there by default.
- **BPM** can read double or half on slow/fast tracks (e.g. 162 may be 81); check by ear before beat-syncing cuts.
- **Copyright:** most popular songs are label music. Instagram can mute or limit a Reel that carries them in the
  file. Best practice: edit to the local file for timing, then post the no-music version and add the same song from
  Instagram's audio library (trending audio also helps reach), lining it up at the same second.
- **Tags:** correct a tag after a post ("save this to the skill") and it sticks.
