# Groundsource Flood Visualization

Interactive timelapse of 2.6 million flash flood events detected worldwide (2000-2026), from Google's Groundsource dataset.

**Live demo:** [https://SharathSivamalaisamy.github.io/groundsource-viz](https://SharathSivamalaisamy.github.io/groundsource-viz)

![Screenshot](https://raw.githubusercontent.com/SharathSivamalaisamy/groundsource-viz/main/screenshot.png)

## Controls

- **Slider** — scrub through years 2000-2026
- **Play button** — auto-advance timelapse (1.5s per year)
- **Space** — play/pause
- **Arrow keys** — step forward/back one year
- **Hover** — see event count per hex cell

## How it works

Events are aggregated into [H3 hexagonal grid cells](https://h3geo.org/) (resolution 3, ~12,000 km² each) per year. The map renders ~6,000 hex cells for recent years using [Deck.gl](https://deck.gl/) on a CARTO dark basemap.

The preprocessing pipeline uses the [`groundsource`](https://github.com/SharathSivamalaisamy/groundsource) Python package to load and enrich the raw dataset.

## Bias note

The 807x growth in detected events (498 in 2000 to 402,012 in 2024) primarily reflects the expansion of digital news coverage, not a proportional increase in flooding. See [`groundsource`](https://github.com/SharathSivamalaisamy/groundsource) for the full bias analysis.

## Data

- **Source:** [Google Groundsource](https://research.google/blog/introducing-groundsource-turning-news-reports-into-data-with-gemini/) (CC BY 4.0)
- **Records:** 2,646,302 events across 175 countries
