# Nifty100 Financial Analytics

A comprehensive financial analytics platform for analyzing Nifty 100 companies using Python, SQLite, Pandas, and Excel-based reporting. The project provides automated ETL, financial ratio computation, stock screening, peer-group analytics, radar chart visualization, and professional Excel reports to support investment research and financial analysis.

---

# Project Overview

The project processes financial statements of Nifty 100 companies, calculates key financial ratios, identifies investment opportunities using configurable screeners, compares companies within peer groups, and generates analyst-friendly reports.

---

# Tech Stack

* Python 3.13
* Pandas
* SQLite
* OpenPyXL
* PyYAML
* Matplotlib
* Pytest
* Git & GitHub

---

# Project Structure

```text
nifty100-financial-analytics/
│
├── config/
│   └── screener_config.yaml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── output/
│   ├── screener_output.xlsx
│   └── peer_comparison.xlsx
│
├── reports/
│   └── radar_charts/
│
├── src/
│   ├── analytics/
│   │   ├── peer.py
│   │   └── radar.py
│   │
│   ├── database/
│   ├── etl/
│   ├── ratios/
│   ├── reports/
│   │   └── peer_report.py
│   │
│   ├── screener/
│   │   ├── engine.py
│   │   ├── presets.py
│   │   ├── scoring.py
│   │   └── export.py
│   │
│   └── utils/
│
├── tests/
│   ├── analytics/
│   ├── etl/
│   ├── ratios/
│   ├── reports/
│   └── screener/
│
├── nifty100.db
├── requirements.txt
└── README.md
```

---

# Sprint 1 — Data Foundation

## Features

* Project setup
* Virtual environment configuration
* ETL pipeline
* Data cleaning
* Data validation
* SQLite database creation
* Foreign key validation
* Processed CSV generation
* Database loading
* Data Quality validation rules
* Documentation

### Outputs

* SQLite database
* Processed datasets
* Data quality reports

---

# Sprint 2 — Financial Ratio Engine

Implemented financial analytics for all companies.

## Financial Ratios

* Net Profit Margin
* Operating Profit Margin
* Return on Equity (ROE)
* Return on Capital Employed (ROCE)
* Return on Assets (ROA)
* Debt-to-Equity
* Interest Coverage Ratio
* Asset Turnover
* Net Debt

## Growth Metrics

* Revenue CAGR
* PAT CAGR
* EPS CAGR

## Cash Flow Metrics

* Free Cash Flow
* CFO Quality Score
* CapEx Intensity

## Quality Metrics

* Composite Quality Score
* High Leverage Flag
* Debt-Free Label
* Interest Coverage Warning

### Outputs

* Financial ratio dataset
* SQLite ratio tables
* `ratio_edge_cases.log`
* `capital_allocation.csv`

---

# Sprint 3 — Financial Screener & Peer Analytics

## Day 15 – Screener Engine

Implemented:

* Latest-year analytics dataset
* Generic filtering engine
* YAML configuration loader
* Duplicate company-year validation
* Composite score sorting
* Financial-sector Debt-to-Equity exemption

---

## Day 16 – Preset Screeners

Implemented reusable preset screeners.

Available presets:

* Quality Compounder
* Growth Accelerator
* Debt-Free Blue Chip

Framework prepared for:

* Value Pick
* Dividend Champion
* Turnaround Watch

---

## Day 17 – Composite Scoring

Implemented:

* Metric normalization
* Winsorization (P10/P90)
* Weighted scoring model
* Sector-relative scoring

Generated:

* `output/screener_output.xlsx`

---

## Day 18 – Peer Analytics

Implemented peer-group analytics.

### Features

* Peer group loader
* Peer mapping
* Percentile computation
* SQLite persistence

Supported metrics:

* ROE
* ROCE
* Net Profit Margin
* Debt-to-Equity
* Free Cash Flow
* PAT CAGR
* Revenue CAGR
* EPS CAGR
* Interest Coverage
* Asset Turnover

Generated:

* `peer_percentiles` SQLite table

---

## Day 19 – Radar Chart Visualization

Implemented radar chart analytics.

### Features

* Company financial profile radar charts
* Peer-group average overlay
* Nifty 100 average fallback
* PNG export
* Batch generation for all companies

Generated:

```text
reports/radar_charts/
```

containing radar charts for all companies.

---

## Day 20 – Peer Comparison Report

Implemented a professional Excel reporting engine.

### Features

* Multi-sheet workbook
* One worksheet per peer group
* Percentile-based conditional formatting
* Benchmark company highlighting
* Median summary row

Generated:

```text
output/peer_comparison.xlsx
```

---

## Day 21 – Testing & Sprint Review

Completed project validation.

### Verification

* Automated unit tests passed
* Quality Compounder preset manually verified
* IT Services peer ranking validated
* FMCG peer ranking validated
* Sprint review completed

---

# Testing

The project follows Test-Driven Development (TDD).

Current test coverage includes:

* ETL
* Ratio Engine
* Screener
* Analytics
* Reporting

**Current Status**

* 76 Tests Passed
* 0 Failures

---

# Reports Generated

## Screener Report

```text
output/screener_output.xlsx
```

Includes:

* Multiple preset screener worksheets
* Composite scores
* Conditional formatting

---

## Peer Comparison Report

```text
output/peer_comparison.xlsx
```

Includes:

* One worksheet per peer group
* Financial metrics
* Percentile rankings
* Benchmark highlighting
* Median summary row

---

## Radar Charts

```text
reports/radar_charts/
```

Contains radar chart visualizations for all companies with peer comparison overlays.

---

# Configuration

Screening thresholds are configurable through:

```text
config/screener_config.yaml
```

Analysts can modify screening criteria without changing source code.

---

# Database

SQLite stores:

* Company master data
* Financial statements
* Financial ratios
* Market capitalization
* Sector information
* Peer groups
* Peer percentile rankings

---

# Key Features

* Automated ETL pipeline
* Financial ratio computation
* Configurable stock screening
* Composite quality scoring
* Peer-group analytics
* Percentile ranking engine
* Radar chart visualization
* Professional Excel reporting
* SQLite data storage
* Modular architecture
* Test-Driven Development (TDD)

---

# Future Enhancements

* Interactive dashboard using Power BI or Streamlit
* Historical trend analysis
* Portfolio comparison
* Valuation models (DCF, Relative Valuation)
* Risk analytics
* Performance attribution
* REST API for financial analytics
* Automated report scheduling

---

# Author

**Venkata Srinivasarao Killadi**

B.Tech – Computer Science & Engineering (Data Science)

Anil Neerukonda Institute of Technology & Sciences (ANITS)

---

# License

This project is developed for educational purposes and portfolio demonstration.
