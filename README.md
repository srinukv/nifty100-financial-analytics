# Nifty100 Financial Analytics

A Financial Data Engineering and Analytics project built on Nifty100 company financial datasets using Python, Pandas, ETL pipelines, Data Quality Validation, Data Cleaning, and Data Loading best practices.

---

# Project Objective

Build a production-style financial analytics pipeline that:

* Loads and profiles raw financial datasets
* Validates data quality using business rules
* Cleans and standardizes financial data
* Ensures referential integrity
* Generates audit reports
* Creates processed and validated datasets
* Prepares data for database loading and downstream analytics

---

# Repository

GitHub Repository:

https://github.com/srinukv/nifty100-financial-analytics

---

# Project Structure

```text
nifty100-financial-analytics/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── validated/
│
├── output/
│
├── src/
│   └── etl/
│       ├── loader.py
│       ├── validator.py
│       ├── data_cleaner.py
│       ├── verify_cleaning.py
│       ├── fk_audit.py
│       ├── fk_check.py
│       ├── fk_check_validated.py
│       ├── load_pipeline.py
│       ├── load_valid_data.py
│       ├── manual_review.py
│       ├── coverage_audit.py
│       └── investigate_coverage.py
│
├── README.md
└── requirements.txt
```

---

# Source Datasets

| Dataset               | Rows |
| --------------------- | ---: |
| companies.xlsx        |   92 |
| profitandloss.xlsx    | 1276 |
| balancesheet.xlsx     | 1312 |
| cashflow.xlsx         | 1187 |
| financial_ratios.xlsx | 1184 |
| market_cap.xlsx       |  552 |
| stock_prices.xlsx     | 5520 |
| documents.xlsx        | 1585 |
| analysis.xlsx         |   20 |
| sectors.xlsx          |   92 |
| peer_groups.xlsx      |   56 |
| prosandcons.xlsx      |   16 |

Total Datasets: 12

---

# Sprint 1 Progress

---

## Day 01 – Data Profiling & Loader Foundation

### Completed

* Project structure setup
* Dataset profiling
* Raw data inspection
* ETL loader implementation
* Standardized loading process
* Data loading verification

### Deliverables

* loader.py
* Dataset profiling report

### Status

✅ Completed

---

## Day 02 – Validation Foundation

### Completed

* Validation framework design
* Data quality architecture
* Year normalization support
* Company identifier normalization
* Validation reporting setup

### Deliverables

* Validation framework
* Normalization utilities

### Status

✅ Completed

---

## Day 03 – Schema Validator

### Data Quality Rules

| Rule  | Description                  |
| ----- | ---------------------------- |
| DQ-01 | Company PK Uniqueness        |
| DQ-02 | Company-Year Uniqueness      |
| DQ-03 | Foreign Key Integrity        |
| DQ-04 | Balance Sheet Balance        |
| DQ-05 | OPM Cross Check              |
| DQ-06 | Positive Sales               |
| DQ-07 | Year Format                  |
| DQ-08 | Ticker Format                |
| DQ-09 | Net Cash Flow Check          |
| DQ-10 | Non-Negative Fixed Assets    |
| DQ-11 | Tax Rate Range               |
| DQ-12 | Dividend Payout Cap          |
| DQ-13 | URL Validation (Deferred)    |
| DQ-14 | EPS Sign Consistency         |
| DQ-15 | Balance Sheet Equality Check |
| DQ-16 | Coverage Check               |

### Validation Results

| Rule  | Failures |
| ----- | -------: |
| DQ-02 |      251 |
| DQ-03 |       36 |
| DQ-05 |      243 |
| DQ-06 |        1 |
| DQ-07 |      112 |
| DQ-09 |        1 |
| DQ-11 |      108 |
| DQ-12 |        7 |
| DQ-14 |        5 |
| DQ-16 |        5 |

Total Validation Failures: 769

### Deliverables

* validator.py
* validation_failures.csv

### Status

✅ Completed

---

## Day 04 – Data Cleaning & Standardization

### Duplicate Removal

| Table            | Removed |
| ---------------- | ------: |
| profitandloss    |      13 |
| balancesheet     |     175 |
| cashflow         |      34 |
| financial_ratios |     119 |
| market_cap       |       0 |

Total Duplicates Removed: 341

### Verification

| Table            | Remaining Duplicates |
| ---------------- | -------------------: |
| profitandloss    |                    0 |
| balancesheet     |                    0 |
| cashflow         |                    0 |
| financial_ratios |                    0 |
| market_cap       |                    0 |

### Foreign Key Audit

Missing Company IDs:

```text
AGTL
ULTRACEMCO
UNIONBANK
UNITDSPR
VBL
VEDL
WIPRO
ZOMATO
ZYDUSLIFE
```

### Deliverables

* data_cleaner.py
* verify_cleaning.py
* fk_audit.py
* cleaning_report.csv
* processed datasets

### Status

✅ Completed

---

## Day 05 – Full Data Load

### Objectives

* Load all 12 datasets
* Define load order
* Generate audit report
* Validate referential integrity

### Load Results

| Dataset          | Rows |
| ---------------- | ---: |
| companies        |   92 |
| profitandloss    | 1276 |
| balancesheet     | 1312 |
| cashflow         | 1187 |
| financial_ratios | 1184 |
| market_cap       |  552 |
| stock_prices     | 5520 |
| documents        | 1585 |

### Load Audit

Generated:

```text
output/load_audit.csv
```

### FK Validation

Detected orphan rows:

| Table            | Removed |
| ---------------- | ------: |
| analysis         |       4 |
| balancesheet     |      85 |
| cashflow         |      96 |
| documents        |     128 |
| financial_ratios |      24 |
| profitandloss    |      99 |
| prosandcons      |       2 |

Total Orphan Rows Removed: 438

### Final FK Validation

```text
Total FK Errors: 0
```

### Deliverables

* load_pipeline.py
* load_valid_data.py
* fk_check.py
* fk_check_validated.py
* validated datasets

### Status

✅ Completed

---

## Day 06 – Manual Data Quality Review

### Manual Review

Randomly Reviewed Companies:

1. BRITANNIA
2. INDUSINDBK
3. HCLTECH
4. HAVELLS
5. DIVISLAB

### Findings

* All reviewed companies contain 12+ years of records
* Coverage is consistent across datasets
* No missing year sequences identified
* No loader defects detected

### Coverage Audit

Coverage exceptions identified:

#### ATGL

```text
P&L = 8 years
BS  = 8 years
CF  = 0 years
```

Finding:

Source dataset contains no cashflow records.

#### SBIN

```text
P&L = 13 years
BS  = 0 years
CF  = 12 years
```

Finding:

Source dataset contains no balance sheet records.

#### JIOFIN

```text
P&L = 3 years
BS  = 3 years
CF  = 2 years
```

Finding:

Recently listed company with limited financial history.

Expected DQ-16 warning.

### Final Assessment

* No loader bugs identified
* Coverage exceptions caused by source data availability
* ETL pipeline functioning correctly

### Deliverables

* manual_review.py
* coverage_audit.py
* investigate_coverage.py

### Status

✅ Completed

---

# Sprint 1 Status

| Day    | Status     |
| ------ | ---------- |
| Day 01 | ✅ Complete |
| Day 02 | ✅ Complete |
| Day 03 | ✅ Complete |
| Day 04 | ✅ Complete |
| Day 05 | ✅ Complete |
| Day 06 | ✅ Complete |
| Day 07 | ✅ Complete |
Sprint 1 Status: COMPLETED

---

# Technologies Used

* Python
* Pandas
* NumPy
* OpenPyXL
* Git
* GitHub

---

# Upcoming Work

## Day 07

SQLite Database Load

Planned Deliverables:

* SQLite Database Creation
* Table Creation Scripts
* Bulk Data Loading
* Table Count Verification
* Database Audit Report

---

Author: Srinivas K
