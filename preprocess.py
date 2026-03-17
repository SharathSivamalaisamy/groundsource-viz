"""Pre-process Groundsource data into H3 hex-aggregated JSON files per year."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import h3
import pandas as pd
from groundsource import FloodDB

OUTPUT_DIR = Path(__file__).parent / "data"
H3_RESOLUTION = 3  # ~12,000 km² per hex


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Loading dataset...")
    db = FloodDB()
    df = db.df

    # Drop rows without valid coordinates
    df = df.dropna(subset=["centroid_lat", "centroid_lon"])

    # Assign H3 cell to each event
    print(f"Assigning H3 cells (res {H3_RESOLUTION}) to {len(df):,} events...")
    df["h3"] = [
        h3.latlng_to_cell(lat, lon, H3_RESOLUTION)
        for lat, lon in zip(df["centroid_lat"], df["centroid_lon"])
    ]

    # Summary: total events per year
    summary = df.groupby("year").size().to_dict()
    summary = {int(k): int(v) for k, v in summary.items()}

    with open(OUTPUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f)
    print(f"Wrote summary.json ({len(summary)} years)")

    # Per-year hex aggregation
    for year, group in df.groupby("year"):
        year = int(year)
        hex_counts = group.groupby("h3").size().reset_index(name="count")

        records = []
        for _, row in hex_counts.iterrows():
            lat, lon = h3.cell_to_latlng(row["h3"])
            records.append({
                "h": row["h3"],
                "lat": round(lat, 4),
                "lon": round(lon, 4),
                "c": int(row["count"]),
            })

        with open(OUTPUT_DIR / f"{year}.json", "w") as f:
            json.dump(records, f, separators=(",", ":"))

        print(f"  {year}: {len(records):,} hex cells, {summary[year]:,} events")

    print("Done.")


if __name__ == "__main__":
    main()
