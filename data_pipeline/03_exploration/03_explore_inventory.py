from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt


INPUT_FILE = Path("data/interim/coolr_reports_points_clean.geojson")
OUTPUT_DIR = Path("outputs/figures")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned dataset...")
    gdf = gpd.read_file(INPUT_FILE)

    print(f"Rows: {len(gdf)}")

    # -------------------------
    # 1. Global distribution
    # -------------------------
    print("Plotting global distribution...")

    fig, ax = plt.subplots(figsize=(12, 6))
    gdf.plot(ax=ax, markersize=2)
    ax.set_title("Global Landslide Distribution (COOLR)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "global_distribution.png", dpi=300)
    plt.close()

    # -------------------------
    # 2. Top 20 countries
    # -------------------------
    print("Plotting country distribution...")

    country_counts = gdf["country_name"].value_counts().head(20)

    plt.figure(figsize=(12, 6))
    country_counts.plot(kind="bar")
    plt.title("Top 20 Countries by Landslide Count")
    plt.ylabel("Count")
    plt.xlabel("country_name")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "country_counts.png", dpi=300)
    plt.close()

    # -------------------------
    # 3. Top 20 countries (log scale)
    # -------------------------
    print("Plotting log-scale country distribution...")

    plt.figure(figsize=(12, 6))
    country_counts.plot(kind="bar", logy=True)
    plt.title("Top 20 Countries by Landslide Count (log scale)")
    plt.ylabel("Count")
    plt.xlabel("country_name")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "country_counts_log.png", dpi=300)
    plt.close()

    # -------------------------
    # 4. Source distribution
    # -------------------------
    print("Plotting source distribution...")

    source_counts = gdf["event_import_source"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    source_counts.plot(kind="bar")
    plt.title("Top Data Sources")
    plt.ylabel("Count")
    plt.xlabel("event_import_source")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "source_distribution.png", dpi=300)
    plt.close()

    # -------------------------
    # 5. Uncertainty distribution
    # -------------------------
    print("Plotting uncertainty distribution...")

    uncertainty_counts = gdf["uncertainty_radius_m"].value_counts(dropna=False).sort_index()

    plt.figure(figsize=(10, 6))
    uncertainty_counts.plot(kind="bar")
    plt.title("Uncertainty Radius Distribution (m)")
    plt.ylabel("Count")
    plt.xlabel("uncertainty_radius_m")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "uncertainty_distribution.png", dpi=300)
    plt.close()

    # -------------------------
    # 6. Temporal distribution (diagnostic only)
    # -------------------------
    print("Plotting temporal distribution...")

    df = gdf.dropna(subset=["event_date"]).copy()

    valid_years = df["event_date"].dt.year
    valid_years = valid_years[(valid_years >= 1900) & (valid_years <= 2100)]

    print(f"Valid dated rows: {len(valid_years)}")

    if len(valid_years) > 0:
        year_counts = valid_years.value_counts().sort_index()

        plt.figure(figsize=(12, 6))
        plt.bar(year_counts.index, year_counts.values)
        plt.title("Landslides per Year (valid dates only)")
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "temporal_distribution.png", dpi=300)
        plt.close()

        print(f"Temporal year range: {year_counts.index.min()} - {year_counts.index.max()}")
    else:
        print("No usable temporal distribution produced.")

    # -------------------------
    # 7. Temporal trends for top 5 countries (diagnostic only)
    # -------------------------
    print("Plotting country temporal trends...")

    top_countries = gdf["country_name"].value_counts().head(5).index.tolist()

    df_time = gdf.dropna(subset=["event_date", "country_name"]).copy()
    df_time["year"] = df_time["event_date"].dt.year
    df_time = df_time[(df_time["year"] >= 1900) & (df_time["year"] <= 2100)]

    if len(df_time) > 0:
        plt.figure(figsize=(12, 6))

        for country in top_countries:
            country_df = df_time[df_time["country_name"] == country]
            counts = country_df.groupby("year").size()
            if len(counts) > 0:
                plt.plot(counts.index, counts.values, label=country)

        plt.legend()
        plt.title("Temporal Trends (Top Countries)")
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "country_temporal_trends.png", dpi=300)
        plt.close()
    else:
        print("No usable country temporal trends produced.")

    # -------------------------
    # 8. Console summaries
    # -------------------------
    print("\nTop 10 countries:")
    print(gdf["country_name"].value_counts().head(10))

    print("\nTop 10 sources:")
    print(gdf["event_import_source"].value_counts().head(10))

    print("\nUncertainty counts:")
    print(gdf["uncertainty_radius_m"].value_counts(dropna=False).sort_index())

    print("\nExploration complete. Figures saved.")


if __name__ == "__main__":
    main()