from src.etl.loader import load_all_files

datasets = load_all_files()

companies = set(
    datasets["companies"]["id"]
)

tables = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "financial_ratios",
]

all_missing = set()

for table in tables:

    df = datasets[table]

    missing = set(
        df.loc[
            ~df["company_id"].isin(companies),
            "company_id",
        ]
    )

    all_missing.update(missing)

    print(
        f"{table}: {len(missing)} missing"
    )

print("\nMissing Company IDs")
print("-" * 30)

for company in sorted(all_missing):
    print(company)