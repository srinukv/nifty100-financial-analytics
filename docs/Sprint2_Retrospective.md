# Sprint 2 Retrospective

## Sprint

Sprint 2 – Financial Ratio Engine

## Sprint Goal

Build a financial ratio engine capable of calculating profitability, leverage, efficiency, CAGR, and cash flow KPIs for all companies and populate the `financial_ratios` table in SQLite with validated metrics.

## What Went Well

* Successfully implemented profitability ratios including ROE, ROCE, Net Profit Margin, Operating Profit Margin, and ROA.
* Implemented leverage and efficiency ratios with proper edge case handling.
* Developed the CAGR engine for Revenue, PAT, and EPS.
* Implemented Cash Flow KPIs and Capital Allocation classification.
* Populated the `financial_ratios` table with calculated KPIs.
* Added composite quality scoring.
* Integrated ROCE into the database pipeline.
* Built the ratio validation and edge case reporting process.
* All unit tests passed successfully.

## Challenges Faced

* Source dataset contained duplicate company-year records.
* TTM rows required exclusion from year-based calculations.
* Snapshot values in the company master dataset differed from historical calculated ratios.
* A few companies showed unusually high ROE and ROCE values, requiring further investigation.

## Decisions Taken

* Treated duplicate company-year records as a data quality issue instead of modifying source data.
* Excluded TTM records from CAGR calculations.
* Compared only the latest financial year while validating ROE and ROCE against source values.
* Categorized validation differences into Version Difference, Data Source Issue, and Formula Discrepancy.

## Testing Summary

* 37 unit tests executed successfully.
* Database validation completed.
* KPI population verified.
* Ratio validation completed.
* Edge case report generated successfully.

## Known Issues

* Duplicate company-year records exist in the source dataset.
* Some companies require further investigation due to unusually high ROE and ROCE values.
* These issues have been documented in `output/ratio_edge_cases.log`.

## Sprint Outcome

Sprint 2 objectives were successfully completed. The Financial Ratio Engine, CAGR Engine, Cash Flow KPIs, database population pipeline, testing, and validation framework are complete and ready for the next sprint.
