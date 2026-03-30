# Source Notes

## COOLR baseline download

- Dataset: NASA COOLR Reports Points
- Access method: NASA ArcGIS REST service behind the Landslide Viewer
- Retrieval method: Python script with paginated requests
- Script: `data_pipeline/01_download/01_download_coolr.py`
- Download date: 2026-03-30
- Output file: `data/raw/coolr/coolr_reports_points_raw.csv`

## Notes
- The viewer UI in the current NASA interface did not expose a direct CSV export option.
- Programmatic download was preferred for reproducibility.
- The service returned records in batches of 2000, so pagination was required.
- The raw dataset contains 14,753 rows and 30 columns.
- This raw file must remain unchanged.