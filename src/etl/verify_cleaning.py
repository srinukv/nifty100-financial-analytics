import pandas as pd

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
]

for table in tables:

    df = pd.read_csv(
        f"data/processed/{table}_clean.csv"
    )

    dupes = (
        df.groupby(
            ["company_id", "year"]
        )
        .size()
        .reset_index(name="count")
    )

    dupes = dupes[
        dupes["count"] > 1
    ]

    print(
        f"{table}: duplicates = {len(dupes)}"
    )