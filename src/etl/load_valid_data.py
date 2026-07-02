from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

OUTPUT_DIR = Path("data/validated")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PROCESSED_DIR = Path("data/processed")

# Only these tables should use cleaned CSVs
CLEANED_TABLES = {
    "profitandloss",
    "balancesheet",
    "cashflow",
    "market_cap",
}


def main():

    datasets = load_all_files()

    # Replace only core datasets with cleaned CSVs
    for table in CLEANED_TABLES:

        clean_file = PROCESSED_DIR / f"{table}_clean.csv"

        if clean_file.exists():

            datasets[table] = pd.read_csv(clean_file)

            print(
                f"{table:<20}"
                f" loaded from processed CSV"
            )

    companies = set(
        datasets["companies"]["id"]
    )

    fk_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "financial_ratios",
    ]

    print("\nVALIDATED LOAD")
    print("=" * 50)

    for table, df in datasets.items():

        if table in fk_tables:

            before = len(df)

            df = df[
                df["company_id"].isin(companies)
            ]

            removed = before - len(df)

            print(
                f"{table:<20}"
                f" removed={removed}"
            )

        df.to_csv(
            OUTPUT_DIR / f"{table}.csv",
            index=False,
        )

    print("\nValidated datasets created")


if __name__ == "__main__":
    main()