from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw")

CORE_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}

for file in sorted(RAW_PATH.glob("*.xlsx")):

    header_row = 1 if file.name in CORE_FILES else 0

    print("\n" + "=" * 100)
    print(file.name)
    print("=" * 100)

    df = pd.read_excel(file, header=header_row)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nColumn Names:")
    for col in df.columns:
        print(col)