# Data Inventory

This file documents the datasets used and considered for the project, including their sources, geographic level, time coverage, file locations, and notes on use.

The repository separates data into three stages:

- `raw/` — original downloaded source files
- `interim/` — cleaned intermediate files derived from raw data
- `processed/` — final analysis-ready datasets

Large raw public files may be stored locally and not committed to GitHub. When that happens, this file should still document the source, date downloaded, and intended use.

---

## Folder structure

```text
data/
├── raw/
├── interim/
├── processed/
└── README.md
````

---

## England

### NHS England RTT Incomplete Commissioner Workbooks

**Source:** NHS England RTT waiting times data

**Description:** Monthly Referral to Treatment waiting times for incomplete pathways, commissioner basis

**Geography:** England commissioning regions

**Time coverage currently collected:** 2025-03 to 2026-02

**Raw file location:** `data/raw/england/rtt/`

**Primary use:** Main England access dataset for pilot panel construction

#### Files collected

* `rtt_incomplete_commissioner_2025_03.xlsx`
* `rtt_incomplete_commissioner_2025_04.xlsx`
* `rtt_incomplete_commissioner_2025_05.xlsx`
* `rtt_incomplete_commissioner_2025_06.xlsx`
* `rtt_incomplete_commissioner_2025_07.xlsx`
* `rtt_incomplete_commissioner_2025_08.xlsx`
* `rtt_incomplete_commissioner_2025_09.xlsx`
* `rtt_incomplete_commissioner_2025_10.xlsx`
* `rtt_incomplete_commissioner_2025_11.xlsx`
* `rtt_incomplete_commissioner_2025_12.xlsx`
* `rtt_incomplete_commissioner_2026_01.xlsx`
* `rtt_incomplete_commissioner_2026_02.xlsx`

#### Notes

* The `Region` tab is currently used for the pilot England panel.
* Only rows with `Treatment Function Code = C_999` are retained in the cleaned dataset.
* National aggregate rows are dropped.
* The first cleaned England panel currently covers 7 commissioning regions across 12 months.

---

## Interim files

### England cleaned monthly RTT regional files

**Location:** `data/interim/`

**Description:** Cleaned monthly England RTT region-level files derived from the RTT incomplete commissioner workbooks

**Primary use:** Intermediate step before stacking into a panel

#### Expected file pattern

* `england_rtt_region_YYYY_MM.csv`

#### Notes

* These files contain one row per region per month.
* Columns are standardized for later stacking and analysis.

---

## Processed files

### England RTT region panel

**File:** `data/processed/england_rtt_region_panel.csv`

**Description:** Combined England regional panel built from monthly RTT incomplete commissioner files

**Geography:** England commissioning regions

**Time coverage:** 2025-03 to 2026-02

**Unit of observation:** region-month

**Primary use:** Main England access panel for descriptive analysis and later merging with denominator and infrastructure data

#### Main variables

* `region_code`
* `region_name`
* `year`
* `month`
* `period`
* `median_wait_weeks`
* `p92_wait_weeks`
* `total_incomplete`
* `total_within_18`
* `pct_within_18`
* `total_52_plus`
* `total_65_plus`
* `total_78_plus`
* `pct_52_plus`

#### Notes

* This is the first successfully constructed panel dataset in the project.
* It currently captures healthcare access outcomes only.
* Population denominators and infrastructure variables still need to be added.

---

## Brazil

No Brazil datasets documented yet.

