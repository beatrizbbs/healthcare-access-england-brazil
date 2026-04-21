# Project Log

This file records major decisions, workflow notes, data issues, comparability concerns, and changes in project scope over time.

The purpose of this log is to create a transparent record of how the project develops from proposal to dataset to analysis and paper.

---

## How this log will be used

This log should capture:

* Important project decisions
* Data source discoveries
* Variable definition choices
* Comparability problems between England and Brazil
* Changes in scope or design
* Workflow notes that may later help with the methods or limitations sections

Entries do not need to be long. The goal is to document the reasoning behind choices as the project evolves.

---

## Log Entry Template

## [YYYY-MM-DD] Short title

**Phase:**
Project setup / Data discovery / Data collection / Data audit / Cleaning / Harmonization / Analysis / Writing

**Summary:**
Brief description of what was done or decided.

## **Details:**

*
*

**Implications for project design:**
Explain whether this changes the feasible dataset, unit of analysis, variables, or empirical strategy.

## **Next actions:**

*

---

## Entries

## [2026-04-18] Repository initialized and project structure created

**Phase:**
Project setup

**Summary:**
Created the GitHub repository and began organizing it as a reproducible research project.

**Details:**

* Repository created for the England–Brazil healthcare access project
* Initial structure planned for data, code, documentation, outputs, and paper materials
* Proposal prepared for inclusion in `docs/proposal.md`
* GitHub project management setup planned using Issues, labels, milestones, and a project board

**Implications for project design:**
No direct change to the research design, but this establishes the workflow that will support transparent data collection, harmonization, and later analysis.

**Next actions:**

* Finalize repository structure
* Create `docs/data-plan.md`
* Begin identifying candidate data sources for England and Brazil

---

## [2026-04-18] Data-first workflow confirmed

**Phase:**
Project design

**Summary:**
Confirmed that the project will follow a data-first workflow, with literature review and full paper framing coming after feasibility is established.

**Details:**

* Decided to focus first on data availability, comparability, and feasible variables
* Chose not to begin with a full literature review
* Agreed that the empirical design should be shaped by what can actually be measured across England and Brazil

**Implications for project design:**
This means the final paper may narrow its scope depending on data quality, territorial comparability, and outcome availability.

**Next actions:**

* Identify candidate datasets
* Assess access outcome feasibility
* Assess regional unit comparability

---

## [2026-04-18] Initial project management structure defined

**Phase:**
Project setup

**Summary:**
Defined the initial GitHub workflow for managing the project.

**Details:**

* Selected broad labels: `data`, `documentation`, `analysis`, `methods`, `comparability`, `bug`, `blocked`
* Chose a blank GitHub project template
* Planned board columns: Backlog, To do, In progress, Blocked, Done
* Decided to organize the roadmap into broad phase-level Issues rather than highly specific tasks

**Implications for project design:**
This will make it easier to track progress at the level of major research phases while preserving flexibility as the project evolves.

**Next actions:**

* Create the phase Issues
* Assign labels and milestones
* Begin work on data planning

---

 ## [2026-04-19] First cleaned England RTT regional dataset created

**Phase:**  
Data cleaning

**Summary:**  
Created the first cleaned England access dataset using NHS RTT incomplete commissioner data at the regional level for February 2026.

**Details:**  
- Used the `Region` tab from the RTT Incomplete Commissioner workbook
- Filtered to `Treatment Function Code = C_999` to keep total rows only
- Dropped national aggregate rows
- Standardized variable names
- Added period fields (`year`, `month`, `period`)
- Saved cleaned output to `data/interim/england_rtt_region_2026_02.csv`

**Implications for project design:**  
This confirms that England regional RTT access data can be cleaned into a usable subnational dataset. The regional level is currently a feasible pilot unit for England.

**Next actions:**  
- Repeat cleaning for additional months
- Assess whether region codes remain stable over time
- Begin identifying England population and capacity datasets at compatible geography

---

## [2026-04-19] Generalized England RTT regional cleaning pipeline

**Phase:**  
Data cleaning

**Summary:**  
Generalized the England RTT regional cleaning workflow so that it can process any RTT Incomplete Commissioner workbook automatically.

**Details:**  
- Reworked the cleaning script to detect the header row automatically
- Parsed the reporting period from workbook metadata instead of hardcoding the date
- Standardized filtering to total rows only using `Treatment Function Code = C_999`
- Standardized exclusion of national aggregate rows
- Generated clean monthly CSV outputs using a consistent naming structure

**Implications for project design:**  
This converts the England RTT workflow from a one-off cleaning step into a reusable pipeline. It makes it feasible to build a true multi-period panel rather than isolated monthly files.

**Next actions:**  
- Run the generalized script across all downloaded monthly RTT files
- Check whether region codes and names remain stable across time
- Combine monthly outputs into one England panel dataset

---

## [2026-04-19] England RTT regional panel constructed for 2025-03 to 2026-02

**Phase:**  
Data processing

**Summary:**  
Built a combined England regional RTT panel covering March 2025 to February 2026.

**Details:**  
- Downloaded monthly RTT Incomplete Commissioner workbooks from 2025-03 to 2026-02
- Restricted raw RTT files in the working folder to the incomplete commissioner files needed for the panel
- Cleaned each workbook using the generalized region-level pipeline
- Combined all cleaned monthly files into a single processed panel dataset
- Saved the final file to `data/processed/england_rtt_region_panel.csv`

**Implications for project design:**  
This confirms that England RTT data can support a region-by-month panel design. It provides a viable access-delay dataset for England and establishes a working pipeline for repeated data collection and cleaning.

**Next actions:**  
- Validate the final panel structure
- Inspect temporal consistency and regional variation
- Begin evaluating whether RTT should remain the main England access outcome

---

## [2026-04-19] Brazil search for RTT-equivalent dataset did not identify an open national general waiting-time panel

**Phase:**  
Data discovery

**Summary:**  
Investigated whether Brazil has a public national dataset directly comparable to NHS RTT and did not identify a clean open equivalent for general waiting times.

**Details:**  
- Reviewed SISREG, e-SUS Regulação, and e-SUS Captação de Fila as possible sources
- Found these systems relevant conceptually but not available as open public datasets in a form suitable for direct panel construction
- Investigated state-level queue portals as a fallback, but no sufficiently consistent open source was identified for the current design
- Concluded that a direct national general waiting-time comparison with England RTT is not currently feasible using the most accessible public data

**Implications for project design:**  
This weakens the feasibility of a broad England–Brazil comparison based on general waiting-time measures. It suggests that a narrower or conceptually harmonized design may be necessary.

**Next actions:**  
- Identify the strongest publicly accessible Brazil access-delay dataset
- Reassess the comparability strategy between England and Brazil
- Document the lack of a direct RTT-equivalent in comparability notes

---

## [2026-04-19] Brazil oncology delay panel identified as strongest public access dataset candidate

**Phase:**  
Data discovery

**Summary:**  
Identified the oncology treatment-delay panel as the strongest publicly accessible Brazil outcome candidate for measuring timeliness of access.

**Details:**  
- Located the public oncology panel showing time until initiation of treatment
- Confirmed that the panel provides distributions of treatment delay by subnational geography
- Verified that the data can be filtered by month/year of diagnosis and month/year of treatment
- Observed that the panel can generate delay-band counts that could be transformed into outcome measures such as treatment after 60 days

**Implications for project design:**  
This provides Brazil with a viable access-delay outcome, but one that is specific to oncology rather than general elective care. The project may therefore need to narrow its empirical focus to cancer-care timeliness or adopt a conceptually harmonized rather than strictly equivalent comparative design.

**Next actions:**  
- Determine the most appropriate Brazil time dimension for panel construction
- Check whether state-level extraction is feasible and stable over time
- Define candidate Brazil outcome variables from the treatment-delay bins

---

## [2026-04-19] England oncology timing dataset identified as a stronger comparator than general RTT

**Phase:**  
Data discovery / design refinement

**Summary:**  
Identified an England cancer timing dataset that is more closely aligned with the Brazil oncology treatment-delay panel than the general RTT dataset.

**Details:**  
- Found an England CSV containing cancer timing metrics with provider and commissioner rows
- Confirmed the presence of commissioner-level rows, including Integrated Care Boards
- Observed timing standards such as `FDS` and `31D` with outcome fields like `Total`, `Within`, `After`, and `Performance`
- Determined that the cancer-specific timing dataset offers much better conceptual alignment with the Brazil oncology panel than the general elective RTT data

**Implications for project design:**  
This is a major design shift. The strongest comparative path now appears to be a narrower oncology-focused study of treatment timeliness in England and Brazil, rather than a broad study of general healthcare waiting times.

**Next actions:**  
- Inspect the England oncology timing file systematically
- Select an initial England oncology outcome and geography
- Reassess whether the project should formally narrow to oncology

---

## [2026-04-19] Project likely shifting from broad healthcare access to oncology treatment timeliness

**Phase:**  
Project design

**Summary:**  
The available data now suggests that the strongest comparative design is focused on timeliness of access to cancer care rather than general healthcare access.

**Details:**  
- England general RTT data is usable but not strongly comparable to the best currently identified Brazil public access dataset
- Brazil oncology delay data is public, structured, and potentially panel-compatible
- England oncology timing data appears to provide a better conceptual match to Brazil’s oncology treatment-delay panel
- The original broad healthcare-access framing may therefore need to be narrowed to a cancer-care or specialized-care timeliness framework

**Implications for project design:**  
The overall methodology remains viable, but the dependent-variable domain is becoming more specific. The project’s contribution may become stronger because the outcome is more coherent across countries, even if the scope is narrower.

**Next actions:**  
- Decide whether to adopt an explicitly oncology-focused framing
- Build pilot oncology datasets for both countries
- Update `docs/data-plan.md` and `docs/comparability-notes.md` to reflect the design shift

---

## [2026-04-19] Project scope shifted to oncology access timeliness

**Phase:**  
Project design

**Summary:**  
Shifted the empirical focus from broad healthcare access to timeliness of access to cancer care.

**Details:**  
- General RTT data was successfully processed for England but was not strongly comparable to the best public Brazil access dataset.
- Brazil oncology treatment-delay data emerged as the strongest public candidate outcome.
- England oncology timing data appears to provide a better conceptual match to Brazil than general elective RTT.
- Decided to build oncology pilot datasets for both countries.

**Implications for project design:**  
The methodology remains valid, but the dependent variable domain is now narrower and more coherent across countries.

**Next actions:**  
- Build England oncology pilot dataset
- Build Brazil oncology pilot dataset
- Assess geographic level and time structure for both
