<h1 align="center">
  <br>
  <a href="docs/assets/logo.png"><img src="docs/assets/logo.png" alt="Project Logo" width="200"></a>
  <br>
  A Comparative Subnational Panel Study of Cancer Treatment Timelines in England and Brazil
  <br>
</h1>

<h4 align="center">A reproducible comparative research project on delays in access to cancer treatment across subnational health systems in England and Brazil.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-95ba91?style=for-the-badge&logo=python&logoColor=white" alt="Python" height="15" />
  <img src="https://img.shields.io/badge/Pandas-82a976?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" height="15" />
  <img src="https://img.shields.io/badge/Jupyter-528562?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter" height="15" />
  <img src="https://img.shields.io/badge/Markdown-4d8d7f?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown" height="15" />
  <img src="https://img.shields.io/badge/GitHub-227257?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" height="15" />
</p>

<p align="center">
  <a href="#overview">Overview</a> -
  <a href="#scope-change">Scope Change</a> -
  <a href="#research-question">Research Question</a> -
  <a href="#current-data">Current Data</a> -
  <a href="#workflow">Workflow</a> -
  <a href="#repository-structure">Repository Structure</a> -
  <a href="#limitations">Limitations</a>
</p>

## Overview

This repository contains the data, code, documentation, and manuscript materials for a comparative study of cancer-care access timeliness in England and Brazil.

The project originally began as a broader subnational study of healthcare access, infrastructure, and workforce capacity across two publicly funded health systems: the National Health Service (NHS) in England and the Sistema Único de Saúde (SUS) in Brazil. Data discovery changed the feasible design. England has usable general waiting-time data through NHS Referral to Treatment (RTT) releases, but a directly comparable open national general waiting-time dataset for Brazil was not identified. The strongest public Brazil access-delay source found so far is oncology-specific.

The project has therefore narrowed to a more coherent comparative outcome: delays in access to cancer treatment.

## Scope Change

Current scope: **oncology treatment timeliness, measured through subnational delay indicators in England and Brazil**.

This change strengthens comparability by focusing on a shared care domain rather than trying to compare England's general elective RTT pathway with a non-equivalent Brazil data source. The previous England RTT work remains useful as project history and as evidence from the feasibility stage, but it is no longer the main comparative outcome.

The current pilot design uses:

* England cancer waiting times at Integrated Care Board (ICB) level.
* Brazil oncology treatment-delay data at state level.
* A shared headline concept: the share of cancer-treatment cases occurring beyond the main timely-treatment threshold.

## Research Question

How does the timeliness of access to cancer treatment vary across subnational regions in England and Brazil?

## Secondary Questions

* Which regions have higher shares of cancer-treatment cases occurring after 60 days?
* How do delay distributions differ between England and Brazil?
* How comparable are England's cancer waiting-time standards and Brazil's oncology delay bands?
* Can the pilot files be extended into a multi-period subnational panel?
* What demographic, socioeconomic, or health-system variables could later be added to explain variation in treatment timeliness?

## Project Status

Current phase: **oncology pilot dataset construction and comparability assessment**.

Completed so far:

* England RTT regional panel was built during the initial feasibility stage.
* Brazil general waiting-time data search did not identify a strong open national RTT-equivalent source.
* Brazil oncology treatment-delay data was identified as the strongest public access-delay candidate.
* England cancer waiting-time data was identified as a better comparator than general RTT.
* Pilot cleaned oncology datasets were created for December 2025.

Immediate next steps:

* Validate the England and Brazil oncology pilot datasets.
* Decide whether to retain December 2025 as a pilot only or extend to a longer monthly panel.
* Update data documentation and comparability notes.
* Define the first descriptive tables and figures.

## Current Data

### England

Current raw source:

* `data/raw/england/oncology/england_oncology_cwt_commissioner_2025_12.csv`

Current cleaned file:

* `data/interim/england_oncology_62d_icb_2025_12.csv`

Unit of observation:

* Integrated Care Board-month

Current pilot period:

* December 2025

Main cleaning script:

* `src/data_cleaning/clean_england_oncology_62d.py`

Current England outcome:

* `pct_after_62`: share of cancer waiting-time cases recorded after 62 days among filtered ICB commissioner rows.

The England pilot filters to commissioner-basis rows for the 62-day cancer standard, all cancers, all routes, and all treatment modalities. It keeps ICB rows and derives a headline percentage delayed beyond the 62-day threshold.

### Brazil

Current raw source:

* `data/raw/brazil/oncology/brazil_oncology_painel_state_diagnosis_2025_12.csv`

Current cleaned file:

* `data/interim/brazil_oncology_delay_state_2025_12.csv`

Unit of observation:

* State-month, with the current cleaned file also retaining the Brazil total aggregate row for checking.

Current pilot period:

* December 2025

Main cleaning script:

* `src/data_cleaning/clean_brazil_oncology_delay.py`

Current Brazil outcomes:

* `pct_over_60`: share of known nonnegative-delay oncology cases occurring after 60 days.
* `pct_over_120`: share of known nonnegative-delay oncology cases occurring after 120 days.

The Brazil pilot uses treatment-delay bands from the oncology panel, aggregates delay bins into within-60-day and over-60-day counts, and excludes negative-delay cases from the main denominator for now.

## Workflow

The project still follows a data-first workflow:

1. Identify feasible access-timeliness datasets for each country.
2. Build country-specific cleaned pilot files.
3. Assess geography, time structure, and variable comparability.
4. Extend pilots into monthly panels if feasible.
5. Harmonize outcome concepts rather than forcing exact variable equivalence.
6. Produce descriptive analysis of regional variation.
7. Add contextual variables if comparable denominators and covariates are available.
8. Develop the paper framing after the empirical design is stable.

## Reproducibility

Install dependencies with:

```bash
pip install -r requirements.txt
```

Clean the current England oncology pilot:

```bash
python src/data_cleaning/clean_england_oncology_62d.py data/raw/england/oncology/england_oncology_cwt_commissioner_2025_12.csv
```

Clean the current Brazil oncology pilot:

```bash
python src/data_cleaning/clean_brazil_oncology_delay.py data/raw/brazil/oncology/brazil_oncology_painel_state_diagnosis_2025_12.csv
```

## Repository Structure

```text
healthcare-access-england-brazil/
|
├── README.md
├── LICENSE
├── requirements.txt
|
├── data/
│   ├── raw/
│   │   ├── brazil/
│   │   │   └── oncology/
│   │   └── england/
│   │       └── oncology/
│   ├── interim/
│   ├── processed/
│   └── README.md
|
├── src/
│   ├── data_cleaning/
│   │   ├── clean_brazil_oncology_delay.py
│   │   ├── clean_england_oncology_62d.py
│   │   ├── clean_england_rtt_region.py
│   │   └── build_england_rtt_region_panel.py
│   ├── analysis/
│   ├── data_collection/
│   ├── harmonization/
│   └── utils/
|
├── docs/
│   ├── assets/
│   ├── proposal.md
│   ├── project-log.md
│   ├── data-plan.md
│   ├── comparability-notes.md
│   ├── data-dictionary.md
│   └── data-findings.md
|
├── notebooks/
├── outputs/
│   ├── tables/
│   ├── figures/
│   └── maps/
└── paper/
    └── manuscript.md
```

## Documentation Strategy

This project treats documentation as part of the research process.

Key files include:

* `docs/proposal.md` - original research proposal.
* `docs/project-log.md` - running record of project decisions and scope changes.
* `docs/data-plan.md` - planned source inventory and variable mapping.
* `docs/comparability-notes.md` - notes on cross-country measurement differences.
* `docs/data-dictionary.md` - variable definitions for cleaned and analytic files.
* `docs/data-findings.md` - descriptive findings and feasibility observations.

## Expected Methods

The immediate methods are descriptive and diagnostic:

* Validate cleaned country-specific pilot datasets.
* Compare delay distributions and headline delay shares.
* Assess whether a multi-month panel can be built.
* Document measurement differences between England's 62-day cancer waiting-time standard and Brazil's oncology delay bands.

If a longer panel is feasible, later analysis may use subnational panel methods with region and time fixed effects. Any regression design will be treated as observational and interpreted cautiously.

## Limitations

Several challenges shape the current design:

* England and Brazil use different cancer-care measurement systems.
* England's pilot geography is ICBs, while Brazil's pilot geography is states.
* England's headline threshold is based on the 62-day cancer standard; Brazil's current headline threshold is constructed from treatment-delay bands over 60 days.
* The current cleaned datasets cover a pilot month, not yet a full panel.
* The project currently measures access timeliness, not infrastructure or workforce capacity.
* Observational comparisons cannot by themselves establish causal effects.

The project therefore uses conceptual harmonization and treats comparability as an empirical object to document, not as an assumption.

## Author

Beatriz Braga Batista

## License

This project is released under the MIT License.
