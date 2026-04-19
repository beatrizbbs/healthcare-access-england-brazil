
<h1 align="center">
  <br>
  <a href="docs/assets/logo.png"><img src="docs/assets/logo.png" alt="Project Logo" width="200"></a>
  <br>
A Comparative Subnational Panel Study of Healthcare Access in England and Brazil
  <br>
</h1>


<h4 align="center">A reproducible research project examining how healthcare infrastructure and workforce capacity are associated with access to care across subnational regions in England and Brazil.</h4>

## Overview

This repository contains the data, code, documentation, and manuscript materials for a comparative subnational panel analysis of healthcare access in two publicly funded health systems: the National Health Service (NHS) in England and the Sistema Único de Saúde (SUS) in Brazil.

The project focuses on a central empirical question: how strongly are healthcare infrastructure constraints—such as hospital beds, workforce availability, and facility distribution—associated with access to care across regions and over time?

The study is designed as a data-first research project. The first priority is to identify what subnational data are available, how comparable they are across countries, and which empirical design is feasible. Literature review and full paper framing will follow after the data structure, variable availability, and comparability issues are clear.

## Research Question

To what extent do healthcare infrastructure and workforce constraints affect access to healthcare services across subnational regions in England and Brazil?

## Secondary Questions

* Which infrastructure factors are the strongest predictors of healthcare access outcomes?
* How do the effects of infrastructure constraints differ between England and Brazil?
* To what extent do regional demographic and socioeconomic characteristics moderate these relationships?
* Are there lagged relationships between changes in healthcare capacity and changes in healthcare access?

## Working Hypotheses

* Lower levels of healthcare infrastructure and workforce capacity are associated with poorer access outcomes.
* The relationship between capacity constraints and access is stronger in regions with greater demographic pressure or lower baseline capacity.
* The strength of the relationship differs between England and Brazil because of institutional and structural differences.
* Infrastructure changes may affect access with a lag rather than immediately.

## Project Status

Current phase: **Project setup and data feasibility mapping**.

The immediate goal is to determine:

* Which datasets are available for England and Brazil,
* Which territorial units are usable and consistent over time,
* Which variables are conceptually comparable,
* Which primary access outcomes are empirically feasible,
* What final panel design can realistically be implemented.

## Research Design

The project uses a comparative quantitative design based on subnational panel data. The planned empirical strategy is fixed-effects regression, with region and year fixed effects, to estimate within-region associations between changes in healthcare capacity and changes in healthcare access over time.

The study does **not** assume from the outset that all estimates can be interpreted as fully causal. The primary goal is to establish robust comparative evidence on within-region relationships between infrastructure constraints and access outcomes, while carefully documenting issues of measurement, comparability, and endogeneity.

## Data-First Workflow

This repository is organized around a data-first workflow:

1. Set up the research repository and project management structure.
2. Identify candidate data sources for England and Brazil.
3. Assess data availability, consistency, and comparability.
4. Build country-specific cleaned datasets.
5. Harmonize variables conceptually across countries.
6. Construct a master panel dataset.
7. Run descriptive analysis and feasibility checks.
8. Estimate preliminary econometric models.
9. Conduct literature review and paper framing after the empirical design is confirmed.
10. Develop the full research paper.

This sequence is intentional: the project will be defined by what can be credibly measured and compared, rather than by a theoretical design that later proves infeasible in the data.

## Planned Data Sources

### England

Planned sources include:

* NHS England administrative and performance data
* NHS workforce and capacity statistics
* Office for National Statistics (ONS) demographic data
* ONS socioeconomic indicators

### Brazil

Planned sources include:

* DATASUS administrative health data
* CNES-related infrastructure and workforce records
* Instituto Brasileiro de Geografia e Estatística (IBGE) demographic data
* IBGE socioeconomic indicators

These sources are subject to revision as data feasibility work progresses.

## Core Variable Families

### Candidate access outcomes

* Waiting times
* Treatment delays
* Backlog or congestion indicators
* Service utilization measures
* Other access-related performance indicators where comparable

### Candidate infrastructure variables

* Hospital beds per capita
* Physicians per capita
* Nurses per capita
* Facility density
* Hospital or clinic availability

### Candidate controls

* Population density
* Age structure
* Population size
* Income or deprivation indicators
* Poverty or socioeconomic conditions
* Year fixed effects and other common shocks

The final variable set will depend on availability, measurement consistency, and cross-country comparability.

## Repository Structure

```text
healthcare-access-england-brazil/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── README.md
│
├── src/
│   ├── data_collection/
│   ├── data_cleaning/
│   ├── harmonization/
│   ├── analysis/
│   └── utils/
│
├── notebooks/
├── outputs/
│   ├── tables/
│   ├── figures/
│   └── maps/
│
├── docs/
│   ├── assets/
│   ├── proposal.md
│   ├── project-log.md
│   ├── data-plan.md
│   ├── comparability-notes.md
│   ├── data-dictionary.md
│   └── data-findings.md
│
└── paper/
    └── manuscript.md
```

## Documentation Strategy

This project treats documentation as part of the research process, not as an afterthought.

Key files include:

* `docs/proposal.md` — original research proposal
* `docs/project-log.md` — ongoing record of decisions, issues, and workflow notes
* `docs/data-plan.md` — candidate datasets, sources, units, and variable mapping
* `docs/comparability-notes.md` — notes on variable equivalence and cross-country comparability
* `docs/data-dictionary.md` — final variable definitions for the analytic dataset
* `docs/data-findings.md` — descriptive findings and feasibility observations before full modeling

## Project Management

GitHub is used as the project management system as well as the code repository.

### Issues

Issues are used to track discrete research and data tasks, such as:

* Collect England waiting time data
* Collect Brazil workforce data
* Compare subnational territorial units
* Define harmonized infrastructure variables
* Audit missingness in the master panel

### Project Board

A GitHub Project board is used to organize workflow stages, typically with columns such as:

* Backlog
* To do
* In progress
* Blocked
* Done

### Branches

Major changes are handled through branches, for example:

* `data-england`
* `data-brazil`
* `cleaning`
* `harmonization`
* `fe-models`

### Milestones and Releases

Planned milestone tags include:

* `v0.1-project-setup`
* `v0.2-raw-data-collected`
* `v0.3-feasibility-mapped`
* `v0.4-master-panel-built`
* `v0.5-descriptive-analysis`
* `v0.6-first-results`
* `v0.7-literature-review`
* `v0.8-paper-draft`

## Reproducibility Principles

This repository is intended to support transparent and reproducible research.

Principles include:

* Preserving raw data separately from cleaned and processed data,
* Documenting all variable transformations,
* Using scripts rather than manual spreadsheet editing wherever possible,
* Keeping code modular and traceable,
* Recording comparability decisions explicitly,
* Separating exploratory work from final analytic workflows.

## Expected Methods

The main planned econometric approach is fixed-effects panel regression of the form:

$$
Access_{it} = \beta_0 + \beta_1 Infrastructure_{it} + \gamma X_{it} + \mu_i + \tau_t + \epsilon_{it}
$$

Extensions may include:

* Lagged infrastructure variables,
* Pooled country interactions,
* Country-specific models,
* Alternative access measures,
* Robustness checks using alternative lag structures or model forms.

These methods remain provisional until the data structure is finalized.

## Limitations Acknowledged from the Start

Several challenges are built into the project design:

* Direct cross-country equivalence of variables may be limited,
* Territorial units may differ in scale and administrative meaning,
* Dome infrastructure measures may refer to different scopes of care,
* Access outcomes may not be perfectly comparable,
* Observational panel methods do not fully eliminate endogeneity concerns.

The project therefore adopts a conceptual harmonization approach and interprets findings with appropriate caution.

## Author

Beatriz Braga Batista

## License

This project is released under the MIT License.
