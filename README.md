# The World Today — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rayarvan77/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rayarvan77/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Entry for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

## The poster

A one-page broadsheet, **"THE WORLD TODAY"**, drawn entirely in code — flat
Pillow shapes, no photographs, no network — so a reader who missed the day
can catch up in a few seconds:

- **Lead story — Kyiv region:** Russian drone strikes bring down part of a
  five-storey block of flats in Dymer; at least 15 people are killed across
  the region (11 in Dymer, 3 in a supermarket strike in Vyshneve, 1 in Bila
  Tserkva) while rescuers dig through the rubble.
- **Climate:** COP31, the longest UN climate summit ever, collapses in
  Antalya with no deal after a fossil-fuel rift splits nearly 200 nations.
- **Libya:** Ukrainian sea drones sink the Russian corvette *Merkury* in
  Benghazi port and hit a cargo ship, 2,400 km from the front line.
- **Markets:** Asian stocks slide on AI-boom doubts — Nikkei down 5%,
  Kospi sharply lower — while Bitcoin steadies off a two-year low.
- **Mexico:** follow-up raids in Sinaloa after the capture of cartel boss
  Fausto Isidro Meza Flores, "El Chapo Isidro".
- **Sport:** Carlos Alcaraz beats world No. 1 Alexander Zverev 6–2, 7–6 to
  win his first ATP Finals title in Turin.
- **Trade:** the EU and Indonesia sign a trade deal a decade in the making,
  scrapping most tariffs — 98.5% on EU goods.

Every fact above was checked against wire reporting from 23 November 2026
before the poster was drawn.

## How it works

- `draw_poster.py` paints the 1024×1024 poster with Pillow and writes
  `entry.png`. It uses fixed fonts, fixed colours and no randomness, so its
  output is byte-identical on every run.
- `main.py` is the entrypoint the grader runs (Python 3.13, standard library
  only). It copies `entry.png` into the output directory
  (`$MAKEFUN_OUTPUT_DIR`, default `/output`) and verifies the result is a
  whole 1024×1024 PNG under 1 MiB, printing its SHA-256.

## Run it

```sh
python3 draw_poster.py entry.png   # re-render the poster (needs Pillow)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Licence

MIT — see [LICENSE](LICENSE).
