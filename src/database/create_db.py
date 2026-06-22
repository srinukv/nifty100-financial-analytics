from pathlib import Path
import sqlite3
import pandas as pd

DB_PATH = Path("nifty100.db")
DATA_DIR = Path("data/validated")

TABLES = [
    "companies",
    "sectors",
    "peer_groups",
    "analysis",
    "prosandcons",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "stock_prices",
    "documents",
]

conn = sqlite3.connect(DB_PATH)

for table in TABLES:

    file_path = DATA_DIR / f"{table}.csv"

    df = pd.read_csv(file_path)

    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False,
    )

    print(
        f"{table:<20} "
        f"loaded {len(df)} rows"
    )

conn.close()

print("\nDatabase created:")
print(DB_PATH)