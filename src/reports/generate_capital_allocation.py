import sqlite3
import pandas as pd

from src.ratios.ratios import (
    calculate_cfo_quality_score,
    get_cfo_quality_label,
    classify_capital_allocation,
)

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    cf.company_id,
    cf.year,
    cf.operating_activity,
    cf.investing_activity,
    cf.financing_activity,
    pl.net_profit
FROM cashflow cf
JOIN profitandloss pl
ON cf.company_id = pl.company_id
AND cf.year = pl.year
"""

df = pd.read_sql(query, conn)

patterns = []

for _, row in df.iterrows():

    score = calculate_cfo_quality_score(
        row["operating_activity"],
        row["net_profit"]
    )

    label = get_cfo_quality_label(score)

    pattern = classify_capital_allocation(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        label
    )

    patterns.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": "+" if row["operating_activity"] >= 0 else "-",
        "cfi_sign": "+" if row["investing_activity"] >= 0 else "-",
        "cff_sign": "+" if row["financing_activity"] >= 0 else "-",
        "pattern_label": pattern
    })

output = pd.DataFrame(patterns)

output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print(output.head())

print("\nRows:", len(output))
print("\nReport Generated Successfully")