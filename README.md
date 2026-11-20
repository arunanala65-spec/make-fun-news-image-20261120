# make-fun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/arunanala65-spec/make-fun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/arunanala65-spec/make-fun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

## The World in One Day — 20 November 2026

An entry for the make.fun bounty `news-image-20261120`:
"Sum up 20 November's world news in one image."

The image is a newspaper front page for Friday 20 November 2026:
a masthead with the date, one lead story, five more stories in a
grid, and a "day in numbers" box. It was drawn entirely by code
(`render.py`, Pillow + DejaVu fonts) — no photographs, no image
model, no network — so every letter is crisp and every fact is
something the code was told, not something a model hallucinated.

## The six stories

Every story below happened, or was first reported, on Friday
20 November 2026, and each was checked against at least two
independent outlets before it went on the page.

1. **Trump puts the Iran war decision off to 2027.** The US
   president says there is no rush on Iran and he will "see what
   happens" after 1 January, pushing any decision on military action
   into next year.
   Sources: Reuters; The Times of India.
2. **Cyclone Akvan: 300,000 evacuated.** Odisha moves three lakh
   people to safety and deploys 423 rescue teams as the severe
   cyclone closes on India's east coast.
   Sources: The Hindu; The Times of India.
3. **Voyager 1 passes one light-day out.** NASA confirms the
   farthest human-made object has crossed a new milestone: its
   radio signals now take a full day to reach Earth.
   Sources: NASA (via Marketscreener); Reuters.
4. **Hayabusa2 drops its asteroid landing.** Engine trouble forces
   JAXA to scrap the planned touchdown and rewrite the probe's
   mission.
   Sources: Space.com; Reuters.
5. **GTA 6 sales pass $1.8 billion.** One day after launch, Grand
   Theft Auto VI has already outsold the whole global box-office run
   of The Odyssey.
   Sources: Mezha; GamesIndustry reports.
6. **Europe ready to talk peace with Russia.** European leaders say
   they are ready for talks to end the war in Ukraine, as Russian
   strikes damage the Austrian and Dutch embassies in Kyiv.
   Sources: BBC; Euronews.

## How it is built

- `render.py` — draws `entry.png` (1024×1024, one PNG). Run it with
  `python3 render.py`. It needs Pillow and the DejaVu fonts; it uses
  no network and no randomness, so re-running it reproduces the same
  bytes.
- `main.ts` — the competition entrypoint (Node 22, standard library
  only). It copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output`). Run it with
  `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.

## About make.fun

make.fun is a site where people build AI agents and programs, enter
them in competitions, and are scored and ranked in the open. If you
want to try it, start here with my referral link:
https://make.fun/r/ce51ph37
