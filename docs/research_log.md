# Research Log

## Project
landslide-uncertainty-modeling

---

## Purpose of this document

This document records:
- methodological decisions
- reasoning behind choices
- dataset interpretations
- emerging research insights

It is intended to support:
- paper writing
- thesis development
- reproducibility of scientific reasoning

---

## 2026-03-30 — Dataset selection and philosophy

### Selected dataset
NASA COOLR Reports Points

### Core decision
The dataset is treated as a **biased observational dataset**, not ground truth.

### Reasoning
- Multiple data sources merged
- Uneven spatial distribution
- Inconsistent reporting practices
- Missing values across critical fields

### Implication
The modeling approach must:
- account for uncertainty
- avoid assuming completeness
- treat absence as unknown, not negative

---

## Data acquisition

### Method
Programmatic download via NASA ArcGIS REST API.

### Why not manual download
- UI export unreliable or unavailable
- Not reproducible
- Cannot guarantee completeness

### Result
- Rows: 14,753
- Columns: 30

### Key insight
The dataset is already processed and aggregated, not raw field observations.

---

## Initial observations

### Source composition
Dominant source: GLC

Insight:
COOLR is not independent → it is largely derived from GLC.

Implication:
- Cannot claim independence from GLC
- Must treat as composite dataset

---

### Spatial structure

Observation:
Strong clustering in:
- South Asia
- Southeast Asia
- USA

Interpretation:
Spatial distribution reflects:
- reporting bias
- infrastructure bias
- data availability

---

### Missingness

Observation:
High missing values in:
- event_time
- injury_count
- storm_name

Interpretation:
Missingness is structural, not accidental.

Decision:
Do NOT remove missing rows.

---

## Cleaning methodology

### Philosophy
Cleaning is not data purification.
Cleaning is standardization while preserving uncertainty.

---

### Row filtering decision

Only remove:
- invalid coordinates
- missing coordinates

Result:
- 14,753 → 14,723 rows

Reason:
Aggressive filtering would destroy valuable information.

---

### Duplicate handling

Decision:
Do NOT remove duplicates yet.

Reason:
- duplicates may represent multi-source confirmation
- removal requires source-aware logic

---

### Category handling

Decision:
Preserve detailed categories.

Reason:
- early aggregation loses information
- later modeling may benefit from granularity

---

### Trigger handling

Decision:
Merge only obvious variants (e.g., rain-related).

Reason:
- reduce noise
- avoid premature ontology creation

---

## Uncertainty modeling

### Key feature introduced
uncertainty_radius_m

### Mapping rationale
Convert categorical location accuracy into numeric scale.

Example:
- exact → 100 m
- 1km → 1000 m
- 5km → 5000 m

### Critical insight
Uncertainty is not noise.
Uncertainty is signal.

### Implication
Future modeling must:
- incorporate spatial uncertainty explicitly
- avoid treating all points as equally precise

---

## Temporal data handling

### Problem
ArcGIS timestamps not directly usable.

### Solution
Mixed parsing:
- epoch milliseconds
- fallback datetime parsing

### Observation
Temporal distribution heavily skewed to recent years.

### Decision
Temporal features are:
- retained
- used only for diagnostics

Reason:
- unreliable for modeling
- incomplete coverage historically

---

## Exploration insights

### Source dominance

GLC contributes majority of data.

Conclusion:
COOLR ≈ GLC + smaller sources

Research implication:
- dataset dependency must be acknowledged
- comparisons with GLC must be careful

---

### Country distribution

Top countries:
- USA
- India
- Myanmar
- Philippines

Interpretation:
Counts reflect reporting, not true frequency.

---

### Uncertainty distribution

Multi-scale structure observed:
- 100 m → 250 km

Interpretation:
Dataset is inherently multi-resolution.

---

### Temporal behavior

Most events concentrated post-2005.

Interpretation:
Temporal bias is strong.

---

## Meta decision: exploration stopping

Decision:
Stop further general exploration.

Reason:
- key structural properties already identified
- additional plots provide diminishing insight

This is a deliberate research efficiency decision.

---

## Region Selection — Nepal

### Decision
Select Nepal as the primary region for the first modeling phase.

### Reasoning
- Geographically compact and coherent
- Strong landslide relevance (Himalayan terrain)
- Moderate dataset size (~587 events)
- Suitable for controlled experimentation
- Familiar from previous work

### Implication
The modeling pipeline will be developed and validated first on Nepal before extending to additional regions.

## Nepal dataset characteristics

### Size
- 587 events after filtering

### Uncertainty structure
The majority of events have spatial uncertainty between 5 km and 25 km.
Only a very small portion of events (~11) are labeled as exact.

Interpretation:
The dataset is dominated by coarse spatial accuracy, reinforcing the need for uncertainty-aware modeling.

### Trigger distribution
Rain is the dominant trigger (~75% of events), with smaller contributions from monsoon and earthquake-related events.

Interpretation:
Nepal landslides in this dataset are primarily rainfall-driven.

### Category distribution
The dataset is heavily dominated by the generic "landslide" category (~90%).

Interpretation:
Category information is limited in discriminative power and will not be a primary modeling feature.

### Overall interpretation
The Nepal subset provides a compact, physically meaningful, and uncertainty-rich dataset suitable for controlled experimentation.

