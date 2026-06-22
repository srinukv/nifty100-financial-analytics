from src.etl.loader import load_all_files
import random

datasets = load_all_files()

companies = datasets["companies"]["id"].tolist()

sample_companies = random.sample(companies, 5)

print("\nMANUAL REVIEW")
print("=" * 60)

for company in sample_companies:

    print(f"\nCompany: {company}")

    for table in [
        "profitandloss",
        "balancesheet",
        "cashflow",
    ]:

        df = datasets[table]

        years = (
            df[
                df["company_id"] == company
            ]["year"]
            .dropna()
            .tolist()
        )

        print(
            f"{table:<15} "
            f"records={len(years):<3} "
            f"years={min(years) if years else 'NA'} "
            f"to "
            f"{max(years) if years else 'NA'}"
        )