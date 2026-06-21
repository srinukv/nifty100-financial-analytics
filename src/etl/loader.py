from pathlib import Path
import pandas as pd

from src.etl.normaliser import (
    normalize_year,
    normalize_company_id
)

RAW_PATH = Path("data/raw")

CORE_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
}


def get_header_row(filename):
    return 1 if filename in CORE_FILES else 0


def load_excel_file(filepath):

    header = get_header_row(filepath.name)

    df = pd.read_excel(
        filepath,
        header=header
    )

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(
            normalize_company_id
        )

    year_columns = ["year", "Year"]

    for col in year_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                normalize_year
            )

    return df


def load_all_files():

    datasets = {}

    for file in sorted(RAW_PATH.glob("*.xlsx")):

        df = load_excel_file(file)

        datasets[file.stem] = df

        print(
            f"{file.name:<25} "
            f"Rows={len(df):<6} "
            f"Cols={len(df.columns)}"
        )

    return datasets


if __name__ == "__main__":

    datasets = load_all_files()

    print("\nLoaded:", len(datasets), "datasets")