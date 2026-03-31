from pathlib import Path

import geopandas as gpd


INPUT_FILE = Path("data/interim/coolr_reports_points_clean.geojson")
OUTPUT_DIR = Path("data/processed/regions")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned dataset...")
    gdf = gpd.read_file(INPUT_FILE)

    print(f"Total rows: {len(gdf)}")

    # -------------------------
    # Nepal selection
    # -------------------------
    print("\nSelecting Nepal...")

    nepal_gdf = gdf[gdf["country_name"] == "nepal"].copy()

    print(f"Nepal rows: {len(nepal_gdf)}")

    # -------------------------
    # Save outputs
    # -------------------------
    output_geojson = OUTPUT_DIR / "nepal_landslides.geojson"
    output_csv = OUTPUT_DIR / "nepal_landslides.csv"

    nepal_gdf.to_file(output_geojson, driver="GeoJSON")
    nepal_gdf.drop(columns="geometry").to_csv(output_csv, index=False)

    print(f"Saved: {output_geojson}")
    print(f"Saved: {output_csv}")

    # -------------------------
    # Quick diagnostics
    # -------------------------
    print("\nUncertainty distribution (Nepal):")
    print(nepal_gdf["uncertainty_radius_m"].value_counts(dropna=False))

    print("\nTrigger distribution (Nepal):")
    print(nepal_gdf["landslide_trigger"].value_counts().head(10))

    print("\nCategory distribution (Nepal):")
    print(nepal_gdf["landslide_category"].value_counts().head(10))


if __name__ == "__main__":
    main()