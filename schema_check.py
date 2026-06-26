import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "financial_ratios",
    "companies"
]

for table in tables:
    print("\n" + "=" * 80)
    print(table.upper())

    df = pd.read_sql(
        f"PRAGMA table_info({table})",
        conn
    )

    print(df["name"].tolist())

print("\n" + "=" * 80)
print("SECTORS")

df = pd.read_sql(
    "PRAGMA table_info(sectors)",
    conn
)

print(df["name"].tolist())