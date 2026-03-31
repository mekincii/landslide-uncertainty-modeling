from pathlib import Path
import re

import geopandas as gpd
import pandas as pd


INPUT_CSV = Path("data/raw/coolr/coolr_reports_points_raw.csv")
OUTPUT_DIR = Path("data/interim")
OUTPUT_CSV = OUTPUT_DIR / "coolr_reports_points_clean.csv"
OUTPUT_GEOJSON = OUTPUT_DIR / "coolr_reports_points_clean.geojson"


KEEP_COLUMNS = [
    "event_id",
    "source_name",
    "source_link",
    "event_date",
    "event_time",
    "event_title",
    "event_description",
    "location_description",
    "location_accuracy",
    "landslide_category",
    "landslide_trigger",
    "landslide_size",
    "landslide_setting",
    "fatality_count",
    "injury_count",
    "storm_name",
    "comments",
    "event_import_source",
    "latitude",
    "longitude",
    "country_name",
    "country_code",
    "admin_division_name",
    "gazetteer_closest_point",
    "gazetteer_distance",
    "submitted_date",
]

LOCATION_ACCURACY_TO_RADIUS_M = {
    "exact": 100,
    "1km": 1000,
    "5km": 5000,
    "10km": 10000,
    "25km": 25000,
    "50km": 50000,
    "100km": 100000,
    "250km": 250000,
    "unknown": pd.NA,
}

def parse_mixed_datetime(series):
    """
    Parse datetime values from a mixed column.

    Handles:
    - ArcGIS epoch milliseconds
    - ISO/date-like strings
    - missing values

    Returns pandas datetime series.
    """
    numeric = pd.to_numeric(series, errors="coerce")

    # First try ArcGIS-style epoch milliseconds
    dt_from_ms = pd.to_datetime(numeric, unit="ms", errors="coerce")

    # Then try normal string parsing
    dt_from_str = pd.to_datetime(series, errors="coerce")

    # Prefer millisecond parsing when available
    return dt_from_ms.fillna(dt_from_str)


def normalize_text(value):
    """Normalize text conservatively for categorical fields."""
    if pd.isna(value):
        return pd.NA

    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)

    if text == "":
        return pd.NA

    return text


def normalize_location_accuracy(value):
    """Normalize location_accuracy values to a controlled vocabulary."""
    value = normalize_text(value)

    if pd.isna(value):
        return pd.NA

    mapping = {
        "exact": "exact",
        "known exactly": "exact",
        "1km": "1km",
        "known within 1 km": "1km",
        "5km": "5km",
        "known within 5 km": "5km",
        "10km": "10km",
        "known within 10 km": "10km",
        "25km": "25km",
        "50km": "50km",
        "100km": "100km",
        "250km": "250km",
        "unknown": "unknown",
    }

    return mapping.get(value, value)


def normalize_category(value):
    """Normalize landslide category values conservatively."""
    value = normalize_text(value)

    if pd.isna(value):
        return pd.NA

    category_map = {
        "rock_fall": "rock fall",
        "rockfall": "rock fall",
        "rotational_slide": "rotational slide",
        "translational_slide": "translational slide",
        "riverbank_collapse": "riverbank collapse",
        "unkown": "unknown",
        "unknown": "unknown",
    }

    return category_map.get(value, value)


def normalize_trigger(value):
    """Normalize landslide trigger values conservatively."""
    value = normalize_text(value)

    if pd.isna(value):
        return pd.NA

    trigger_map = {
        "downpour": "rain",
        "heavy rain": "rain",
        "heavy rainfall": "rain",
        "continuous_rain": "rain",
        "snowfall_snowmelt": "snowfall snowmelt",
        "no_apparent_trigger": "no apparent trigger",
        "dam_embankment_collapse": "dam embankment collapse",
        "leaking_pipe": "leaking pipe",
        "unknown": "unknown",
    }

    return trigger_map.get(value, value)


def validate_coordinates(df):
    """Remove rows with missing or invalid coordinates."""
    before = len(df)

    df = df.dropna(subset=["latitude", "longitude"]).copy()

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    df = df.dropna(subset=["latitude", "longitude"]).copy()

    df = df[df["latitude"].between(-90, 90)].copy()
    df = df[df["longitude"].between(-180, 180)].copy()

    after = len(df)
    print(f"Coordinate validation: kept {after} / {before} rows")

    return df


def print_unmapped_location_accuracy(df):
    """Print location_accuracy values that remain outside the controlled mapping."""
    allowed = set(LOCATION_ACCURACY_TO_RADIUS_M.keys())
    values = (
        df["location_accuracy"]
        .dropna()
        .astype(str)
        .value_counts()
    )

    unmapped = values[~values.index.isin(allowed)]
    if len(unmapped) > 0:
        print("\nUnmapped location_accuracy values:")
        print(unmapped)
    else:
        print("\nAll non-null location_accuracy values are mapped.")


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Reading raw file: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)

    print(f"Initial rows: {len(df)}")
    print(f"Initial columns: {len(df.columns)}")

    missing_keep_cols = [col for col in KEEP_COLUMNS if col not in df.columns]
    if missing_keep_cols:
        raise ValueError(f"Missing expected columns: {missing_keep_cols}")

    df = df[KEEP_COLUMNS].copy()

    df = validate_coordinates(df)

    df["event_date"] = parse_mixed_datetime(df["event_date"])
    df["submitted_date"] = parse_mixed_datetime(df["submitted_date"])

    numeric_cols = ["fatality_count", "injury_count", "gazetteer_distance"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    text_cols = [
        "event_id",
        "source_name",
        "source_link",
        "event_time",
        "event_title",
        "event_description",
        "location_description",
        "landslide_size",
        "landslide_setting",
        "storm_name",
        "comments",
        "event_import_source",
        "country_name",
        "country_code",
        "admin_division_name",
        "gazetteer_closest_point",
    ]
    for col in text_cols:
        df[col] = df[col].apply(normalize_text)

    df["location_accuracy"] = df["location_accuracy"].apply(normalize_location_accuracy)
    df["landslide_category"] = df["landslide_category"].apply(normalize_category)
    df["landslide_trigger"] = df["landslide_trigger"].apply(normalize_trigger)

    df["uncertainty_radius_m"] = df["location_accuracy"].map(LOCATION_ACCURACY_TO_RADIUS_M)

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    )

    df.to_csv(OUTPUT_CSV, index=False)
    gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

    print(f"Saved cleaned CSV: {OUTPUT_CSV}")
    print(f"Saved cleaned GeoJSON: {OUTPUT_GEOJSON}")
    print(f"Final rows: {len(df)}")

    print("\nMissing values summary:")
    print(df.isna().sum().sort_values(ascending=False).head(15))

    print("\nlocation_accuracy value counts:")
    print(df["location_accuracy"].value_counts(dropna=False))

    print_unmapped_location_accuracy(df)

    print("\nlandslide_category value counts:")
    print(df["landslide_category"].value_counts(dropna=False).head(25))

    print("\nlandslide_trigger value counts:")
    print(df["landslide_trigger"].value_counts(dropna=False).head(25))


if __name__ == "__main__":
    main()