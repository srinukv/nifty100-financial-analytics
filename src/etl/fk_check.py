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

total_fk_errors = 0

print("\nFK CHECK")
print("=" * 40)

for table in tables:

    df = datasets[table]

    invalid = df[
        ~df["company_id"].isin(companies)
    ]

    count = len(invalid)

    total_fk_errors += count

    print(
        f"{table:<20} {count}"
    )

print("\nTotal FK Errors:", total_fk_errors)