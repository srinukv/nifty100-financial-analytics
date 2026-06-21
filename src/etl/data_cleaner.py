from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_company_year_duplicates(df):

    before = len(df)

    df = (
        df.sort_values(by="id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="last",
        )
    )

    removed = before - len(df)

    return df, removed


def main():

    datasets = load_all_files()

    cleaning_report = []

    tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
    ]

    for table in tables:

        df = datasets[table]

        cleaned_df, removed = (
            clean_company_year_duplicates(df)
        )

        cleaned_df.to_csv(
            OUTPUT_DIR / f"{table}_clean.csv",
            index=False,
        )

        cleaning_report.append(
            {
                "table": table,
                "duplicates_removed": removed,
            }
        )

        print(
            f"{table}: removed {removed} duplicates"
        )

    report_df = pd.DataFrame(cleaning_report)

    report_df.to_csv(
        OUTPUT_DIR / "cleaning_report.csv",
        index=False,
    )

    print("\nCleaning Complete")


if __name__ == "__main__":
    main()