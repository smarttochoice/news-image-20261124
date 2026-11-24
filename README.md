# news-image-20261124

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/smarttochoice/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/smarttochoice/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image summing up the world news of **Tuesday 24 November 2026** — a
one-page newspaper front page, drawn programmatically (no scraped photos, no
AI-image-generator text to garble), so every word stays crisp and legible at
300 px across.

Bounty: [news-image-20261124](https://make.fun/bounty/news-image-20261124)

Want to try make.fun yourself? Start here: https://make.fun/r/w57pvztf

## What the image shows

The masthead names the day — **TUESDAY · 24 NOVEMBER 2026** — and the page
carries the day's six most consequential stories, across regions and fields,
each with its own drawn pictogram, headline and one-line summary, plus four
more in an "Also today" box:

| Story | Panel |
| --- | --- |
| Jensen Huang reinstated as Nvidia CEO; shares jump 31%, the biggest one-day gain since 2003 | Hero: chip, NVDA +31% |
| COP31 ends with no climate deal (UN talks in Türkiye end divided over fossil fuels) | Climate: globe, 0 deal |
| Factory fire in Indonesia kills at least 24; dozens missing | Disaster: flame, 24 dead |
| Russian strikes kill in the Kyiv region; a Russian cargo ship burns off Finland | War: burst, Kyiv |
| Trump blames Democrats for a $1 trillion Wall Street rout after the midterms | Markets: falling bars, $1 tn |
| Carlos Alcaraz wins his first ATP Finals title, beating Zverev in Turin | Sport: tennis ball, No. 1 |

Also today: the World Chess Championship opens in Geneva (Gukesh defends his
crown against Sindarov); India–New Zealand Test ends in a draw at
Wellington; the UK sanctions Myanmar generals over the Rohingya ruling; a
supermoon meets the Pleiades in tonight's sky.

Every claim is as reported on 24 Nov 2026 (BBC, Reuters, AP, Times of
India).

## Layout

- `main.ts` — the entry: checks `entry.png` is a whole PNG within the
  1024×1024 / 1 MiB limits and copies it to `/output/entry.png` (Node 22,
  standard library only)
- `entry.png` — the image, 1024×1024, ~135 KB
- `draw.py` — the program that draws the image with PIL and DejaVu fonts;
  re-running it reproduces `entry.png` byte-for-byte from the same fonts

## Verification

- `python3 draw.py` → `entry.png` 1024×1024, 135,068 bytes, visually
  checked: every headline and summary sits inside its panel, no clipped or
  garbled text, date legible in the masthead. Re-run gives the identical
  SHA-256.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` → writes `out/entry.png`,
  byte-identical to the committed image; run twice, same bytes.
- Kit check: `node cli/makefun.mjs check --kit . --repo <repo>
  --transcripts transcripts.tar.gz` — all passed, 0 failed.
