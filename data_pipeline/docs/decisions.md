# Decisions Log

## 2026-03-30 — COOLR initial cleaning decisions

### Dataset treatment
- COOLR reports points are treated as a biased observational dataset, not complete ground truth.

### Coordinate filtering
- Rows with missing latitude or longitude are removed.
- Rows with invalid latitude/longitude ranges are removed.
- No other row-level filtering is applied in the first cleaning pass.

### Duplicate handling
- No duplicate removal is performed yet.
- Duplicate detection is deferred to a later dedicated step.

### Uncertainty handling
- `location_accuracy` is preserved and normalized.
- A derived numeric field `uncertainty_radius_m` is created.
- Initial radius mapping:
  - `exact` -> 100
  - `1km` -> 1000
  - `5km` -> 5000
  - `10km` -> 10000
  - `25km` -> 25000
  - `50km` -> 50000
  - `100km` -> 100000
  - `250km` -> 250000
- `unknown` and missing values remain missing in `uncertainty_radius_m`

### Category handling
- Landslide categories are normalized conservatively.
- Obvious formatting and spelling inconsistencies are corrected.
- Detailed categories are preserved.
- No broad class merging is performed yet.

### Trigger handling
- Trigger labels are normalized conservatively.
- Obvious rainfall variants are merged under `rain`.
- No higher-level trigger ontology is imposed yet.

### Output level
- The current cleaned dataset is considered an interim standardized dataset.
- It is suitable for exploration and dataset understanding, but not yet final modeling.