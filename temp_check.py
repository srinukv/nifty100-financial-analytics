import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow"
]

for table in tables:

    print("\n", table.upper())

    df = pd.read_sql(f"""
    SELECT *
    FROM {table}
    WHERE company_id='ABB'
      AND year IS NULL
    """, conn)

    print(df)

conn.close()