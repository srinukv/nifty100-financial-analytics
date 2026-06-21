# Nifty100 Financial Intelligence Platform

## Overview

A production-grade financial intelligence platform for analysing 92 Nifty 100 companies using structured financial statement data.

The platform ingests, validates, stores, analyses, and visualises financial information from multiple datasets covering:

* Profit & Loss Statements
* Balance Sheets
* Cash Flow Statements
* Market Capitalisation
* Financial Ratios
* Sector Classification
* Peer Group Analysis

## Project Objectives

* Build a validated SQLite data warehouse
* Implement 16 Data Quality Rules
* Calculate 50+ Financial KPIs
* Develop Investment Screening Engine
* Build Financial Health Score Model
* Create Interactive Dashboard
* Generate Automated Reports

## Technology Stack

* Python
* Pandas
* NumPy
* SQLite
* SQLAlchemy
* Pytest
* Streamlit
* Plotly

## Repository Structure

data/
db/
src/
tests/
notebooks/
output/
docs/

## Sprint Progress

### Sprint 1 – Data Foundation & ETL

* [ ] Day 01 Environment Setup
* [ ] Day 02 Excel Loader & Normaliser
* [ ] Day 03 Data Quality Validator
* [ ] Day 04 SQLite Schema
* [ ] Day 05 Full Data Load
* [ ] Day 06 Manual Review
* [ ] Day 07 Sprint Review

Sprint 1 – Day 03 Completed

Implemented schema validator with DQ rules.

Generated validation report:
output/validation_failures.csv

Validation Summary:
- DQ-02: 251
- DQ-03: 36
- DQ-05: 243
- DQ-06: 1
- DQ-07: 112
- DQ-09: 1
- DQ-11: 108
- DQ-12: 7
- DQ-14: 5
- DQ-16: 5

Total Failures: 769