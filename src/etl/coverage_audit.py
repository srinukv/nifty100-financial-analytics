from src.etl.loader import load_all_files
import pandas as pd

datasets = load_all_files()

rows = []

companies = datasets["companies"]["id"]

for company in companies:

    pnl = len(
        datasets["profitandloss"]
        [
            datasets["profitandloss"]["company_id"]
            == company
        ]
    )

    bs = len(
        datasets["balancesheet"]
        [
            datasets["balancesheet"]["company_id"]
            == company
        ]
    )

    cf = len(
        datasets["cashflow"]
        [
            datasets["cashflow"]["company_id"]
            == company
        ]
    )

    rows.append(
        {
            "company_id": company,
            "pnl_years": pnl,
            "bs_years": bs,
            "cf_years": cf,
        }
    )

df = pd.DataFrame(rows)

short_history = df[
    (df["pnl_years"] < 5)
    |
    (df["bs_years"] < 5)
    |
    (df["cf_years"] < 5)
]

print(short_history)

short_history.to_csv(
    "output/company_coverage.csv",
    index=False
)