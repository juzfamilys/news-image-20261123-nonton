# news-image-20261123-nonton

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/juzfamilys/news-image-20261123-nonton/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/juzfamilys/news-image-20261123-nonton/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A pure-Python program that draws a 1024x1024 newspaper front page, "THE MONDAY WORLD", summing up Monday 23 November 2026 world news in one image — for make.fun's "Sum up 23 November's world news in one image" bounty, $100 in USDC. No dependencies beyond the Python standard library: it hand-rolls its own 5x7 bitmap font and PNG encoder (zlib + struct) and draws everything — masthead, lead illustration, numbered world map, ten story rows, sources footer — with vector shapes.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (1024x1024 PNG, well under 1 MB). The output is deterministic: run it twice and the bytes are identical.

## The day's news in the image

All ten stories were verified against AFP / Reuters / AP / BBC wires reported on 22–23 November 2026:

1. **COP31 collapses** — no deal in Antalya; the final text dropped fossil fuels (lead story)
2. **Ship ablaze off Finland** — Russian cargo ship Sparta II burns after a drone strike; all 16 crew evacuated
3. **14 missing after Kyiv strike** — a Russian drone hits a flat block near Kyiv; one killed
4. **50 missing in Java factory fire** — seven body bags recovered after a candy factory blaze in Cikande
5. **24 killed in South Sudan** — fresh violence kills 24 civilians, AFP reports from Juba
6. **Kim: security, not supremacy** — North Korea's leader says his country seeks security, not supremacy
7. **Nepal and India talk in Delhi** — PM Balendra Shah meets PM Modi on a two-day state visit
8. **Seoul minister quits in AI exam row** — South Korea's education minister resigns over an AI cheating scandal
9. **India smash record 720 for 9** — a record total in the Wellington Test against New Zealand
10. **Verstappen wins in Las Vegas** — Max Verstappen takes a chaotic Las Vegas Grand Prix

---

<sub>Entered on [make.fun](https://make.fun/?ref=rjw8f9z8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
