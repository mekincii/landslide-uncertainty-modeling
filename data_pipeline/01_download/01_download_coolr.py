from pathlib import Path
import requests
import pandas as pd

BASE_URL = (
    "https://gis.earthdata.nasa.gov/gis05/rest/services/"
    "Landslides/COOLR_Reports_Points/FeatureServer/0/query"
)

OUT_CSV = Path("data/raw/coolr/coolr_reports_points_raw.csv")
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def fetch_batch(offset: int, batch_size: int = 2000):
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "f": "json",
        "resultOffset": offset,
        "resultRecordCount": batch_size,
    }
    r = requests.get(BASE_URL, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()

    if "error" in data:
        raise RuntimeError(f"ArcGIS error: {data['error']}")

    return data.get("features", [])

all_rows = []
offset = 0
batch_size = 2000

while True:
    features = fetch_batch(offset, batch_size=batch_size)
    if not features:
        break

    all_rows.extend([f["attributes"] for f in features])
    print(f"Fetched {len(features)} rows at offset {offset}")
    offset += batch_size

df = pd.DataFrame(all_rows)
df.to_csv(OUT_CSV, index=False)

print(f"\nSaved {len(df)} rows to: {OUT_CSV}")
print("\nColumns:")
print(df.columns.tolist())