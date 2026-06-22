# Nifty100 Financial Analytics

A Financial Data Engineering and Analytics project built using Python, Pandas, SQLite, and ETL best practices on Nifty100 company financial datasets.

---

# Project Overview

The objective of this project is to build a production-style financial analytics pipeline that:

* Ingests raw financial datasets
* Profiles and validates data quality
* Cleans and standardizes records
* Performs foreign key and coverage audits
* Creates processed and validated data layers
* Loads validated data into SQLite
* Supports downstream analytics and dashboard development

---

# Repository

GitHub Repository:

https://github.com/srinukv/nifty100-financial-analytics

---

# Tech Stack

* Python
* Pandas
* NumPy
* SQLite
* OpenPyXL
* Git
* GitHub

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
├── sql/
│   └── exploratory_queries.sql
│
├── src/
│   ├── database/
│   │   └── create_db.py
│   │
│   ├── etl/
│   │   ├── loader.py
│   │   ├── validator.py
│   │   ├── data_cleaner.py
│   │   ├── verify_cleaning.py
│   │   ├── fk_audit.py
│   │   ├── fk_check.py
│   │   ├── fk_check_validated.py
│   │   ├── load_pipeline.py
│   │   ├── load_valid_data.py
│   │   ├── manual_review.py
│   │   ├── coverage_audit.py
│   │   └── investigate_coverage.py
│   │
│   └── reports/
│
├── nifty100.db
├── README.md
└── requirements.txt
```

---

# Source Datasets

| Dataset               | Records |
| --------------------- | ------: |
| companies.xlsx        |      92 |
| profitandloss.xlsx    |    1276 |
| balancesheet.xlsx     |    1312 |
| cashflow.xlsx         |    1187 |
| financial_ratios.xlsx |    1184 |
| market_cap.xlsx       |     552 |
| stock_prices.xlsx     |    5520 |
| documents.xlsx        |    1585 |
| analysis.xlsx         |      20 |
| sectors.xlsx          |      92 |
| peer_groups.xlsx      |      56 |
| prosandcons.xlsx      |      16 |

Total Datasets: 12

---

# Sprint 1 Deliverables

## Day 01 – Data Profiling & Loader Foundation

### Completed

* Project setup
* Dataset inspection
* Data profiling
* ETL loader implementation
* Standardized loading framework

### Deliverables

* loader.py
* data_profiler.py

Status: ✅ Completed

---

## Day 02 – Validation Foundation

### Completed

* Validation architecture
* Data normalization utilities
* Company ID normalization
* Year normalization
* Validation reporting framework

### Deliverables

* normaliser.py
* validation framework

Status: ✅ Completed

---

## Day 03 – Schema Validator

### Implemented Data Quality Rules

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

### Deliverables

* validator.py
* validation_failures.csv

Status: ✅ Completed

---

## Day 04 – Data Cleaning & FK Audit

### Duplicate Removal

| Table            | Removed |
| ---------------- | ------: |
| profitandloss    |      13 |
| balancesheet     |     175 |
| cashflow         |      34 |
| financial_ratios |     119 |
| market_cap       |       0 |

Total Duplicates Removed: **341**

### FK Audit Findings

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

Status: ✅ Completed

---

## Day 05 – Full Data Load & FK Validation

### Completed

* Full load of all 12 datasets
* Load order implementation
* Load audit generation
* Validated data layer creation
* FK validation

### Results

* 438 orphan rows identified
* Orphan rows excluded from validated layer
* FK Errors reduced to 0

### Deliverables

* load_pipeline.py
* load_valid_data.py
* fk_check.py
* fk_check_validated.py
* load_audit.csv

Status: ✅ Completed

---

## Day 06 – Manual Data Quality Review

### Manual Review

Reviewed:

* BRITANNIA
* INDUSINDBK
* HCLTECH
* HAVELLS
* DIVISLAB

### Coverage Audit Findings

#### ATGL

* P&L: 8 years
* Balance Sheet: 8 years
* Cash Flow: 0 years

Finding:
Source dataset missing cashflow records.

#### SBIN

* P&L: 13 years
* Balance Sheet: 0 years
* Cash Flow: 12 years

Finding:
Source dataset missing balance sheet records.

#### JIOFIN

* P&L: 3 years
* Balance Sheet: 3 years
* Cash Flow: 2 years

Finding:
Recently listed company with limited history.

### Deliverables

* manual_review.py
* coverage_audit.py
* investigate_coverage.py

Status: ✅ Completed

---

## Day 07 – Sprint Wrap-Up & Database Review

### Completed

* SQLite database creation
* Validated data loaded into database
* Exploratory SQL queries created
* Sprint review completed

### Database

```text
nifty100.db
```

### Database Tables

| Table            | Rows |
| ---------------- | ---: |
| companies        |   92 |
| sectors          |   92 |
| peer_groups      |   56 |
| analysis         |   16 |
| prosandcons      |   14 |
| profitandloss    | 1177 |
| balancesheet     | 1227 |
| cashflow         | 1091 |
| financial_ratios | 1160 |
| market_cap       |  552 |
| stock_prices     | 5520 |
| documents        | 1457 |

### Deliverables

* create_db.py
* exploratory_queries.sql
* nifty100.db

Status: ✅ Completed

---

# Key Achievements

### Data Quality

* Implemented 16 Data Quality Rules
* Generated validation reports
* Identified duplicate and orphan records

### Data Cleaning

* Removed 341 duplicate records
* Created processed datasets

### Referential Integrity

* Detected 438 orphan records
* Achieved FK Errors = 0

### Database Layer

* Created SQLite database
* Loaded validated datasets
* Prepared foundation for analytics

---

# Sprint 1 Outcome

Successfully delivered:

* ETL Pipeline
* Data Validation Framework
* Data Cleaning Framework
* Processed Data Layer
* Validated Data Layer
* Foreign Key Validation
* Coverage Auditing
* SQLite Database
* Exploratory SQL Layer

## Sprint 1 Status

✅ COMPLETED

---

# Next Sprint

Sprint 2 – Financial Ratio Engine

Planned Topics:

* Revenue Growth
* Profit Growth
* CAGR Calculations
* Financial Ratios
* Company Ranking Engine
* Sector Benchmarking

---
