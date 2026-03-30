# Progress Log

## 2026-03-30 — Project initialization and COOLR acquisition

### Project setup
- Created the project `landslide-uncertainty-modeling`.
- Initialized a local Git repository.
- Added initial `.gitignore`.
- Created the first folder structure for:
  - `data/`
  - `data_pipeline/`
  - `outputs/`
- Created the initial commit:
  - `Initial project structure`

### Data acquisition decision
- Decided to use **COOLR** as the primary baseline global landslide inventory for the new research-grade version of the project.
- The project will treat COOLR as a **biased observational dataset**, not as complete ground truth.
- Regional higher-quality inventories, especially from Türkiye, may be integrated later for comparison and validation.

### Download approach
- The NASA Landslide Viewer UI did not provide a direct export option in the current interface.
- Instead of relying on manual UI download, a programmatic approach was adopted using the NASA ArcGIS service behind the viewer.
- A Python download script was created in:
  - `data_pipeline/01_download/01_download_coolr.py`

### Raw COOLR download
- Queried the NASA `COOLR_Reports_Points` ArcGIS layer programmatically.
- Implemented pagination because the service returns at most 2000 records per request.
- Successfully downloaded the full raw table and saved it to:
  - `data/raw/coolr/coolr_reports_points_raw.csv`

### Download result
- Total rows downloaded: **14,753**
- Total columns: **30**

### Raw columns
- `objectid`
- `source_name`
- `source_link`
- `event_id`
- `event_date`
- `event_time`
- `event_title`
- `event_description`
- `location_description`
- `location_accuracy`
- `landslide_category`
- `landslide_trigger`
- `landslide_size`
- `landslide_setting`
- `fatality_count`
- `injury_count`
- `storm_name`
- `photo_link`
- `comments`
- `event_import_source`
- `event_import_id`
- `latitude`
- `longitude`
- `country_name`
- `country_code`
- `admin_division_name`
- `gazetteer_closest_point`
- `gazetteer_distance`
- `submitted_date`
- `last_edited_date`

### First observations
- The dataset is heterogeneous and clearly multi-source.
- `event_import_source` is dominated by `GLC`, but also includes other imported datasets.
- Useful uncertainty-related fields are available:
  - `location_accuracy`
  - `gazetteer_distance`
  - `location_description`
- Important missingness exists:
  - `event_date` missing in about 11%
  - `event_time` missing in about 55%
  - `injury_count` missing in about 57%
  - `last_edited_date` nearly empty
- Several categorical fields contain inconsistent naming and capitalization, such as:
  - `unknown` vs `Unknown`
  - `rock_fall` vs `Rock fall`

### Interpretation
- The raw dataset is not clean ground truth.
- It should be treated as a global observational landslide inventory with uncertainty, reporting bias, and source heterogeneity.
- These properties align with the scientific goals of the project.

### Next step
- Design the initial cleaning rules and canonical schema before any modeling.