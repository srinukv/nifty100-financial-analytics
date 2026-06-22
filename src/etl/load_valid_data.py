from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

OUTPUT_DIR = Path("data/validated")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def main():

    datasets = load_all_files()

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
                df["company_id"]
                .isin(companies)
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