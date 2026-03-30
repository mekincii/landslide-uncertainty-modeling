# Cleaning Rules — COOLR Reports Points

## Purpose

This document defines the initial cleaning and standardization rules for the raw
COOLR reports points dataset used in the project.

The goal is not to remove all uncertainty. The goal is to:

- preserve useful uncertainty information
- remove clearly invalid or unusable records
- standardize heterogeneous fields
- produce a reproducible, analysis-ready event table

---

## Dataset Philosophy

The COOLR reports points dataset is treated as a **biased observational dataset**
of landslides, not as complete ground truth.

This means:

- missingness is expected
- spatial precision is heterogeneous
- event labels may be inconsistent across sources
- source metadata must be preserved

---

## Input

Raw input file:

```text
data/raw/coolr/coolr_reports_points_raw.csv