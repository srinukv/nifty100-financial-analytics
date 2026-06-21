from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

OUTPUT_FILE = Path("output/validation_failures.csv")


def add_failure(
    failures,
    rule_id,
    severity,
    table_name,
    record_identifier,
    message,
):
    failures.append(
        {
            "rule_id": rule_id,
            "severity": severity,
            "table_name": table_name,
            "record_identifier": record_identifier,
            "message": message,
        }
    )


def validate():

    datasets = load_all_files()

    failures = []

    # ==================================================
    # DQ-01 Primary Key Uniqueness
    # ==================================================

    tables_with_id = [
        "companies",
        "analysis",
        "prosandcons",
        "sectors",
        "peer_groups",
    ]

    for table in tables_with_id:

        df = datasets[table]

        dupes = df[
            df["id"].duplicated(keep=False)
        ]

        for _, row in dupes.iterrows():

            add_failure(
                failures,
                "DQ-01",
                "CRITICAL",
                table,
                str(row["id"]),
                "Duplicate primary key",
            )

    # ==================================================
    # DQ-02 Company-Year Uniqueness
    # ==================================================

    year_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
    ]

    for table in year_tables:

        df = datasets[table]

        duplicate_keys = (
            df.groupby(
                ["company_id", "year"]
            )
            .size()
            .reset_index(name="count")
        )

        duplicate_keys = duplicate_keys[
            duplicate_keys["count"] > 1
        ]

        for _, row in duplicate_keys.iterrows():

            add_failure(
                failures,
                "DQ-02",
                "CRITICAL",
                table,
                f"{row['company_id']}_{row['year']}",
                "Duplicate company-year key",
            )

    # ==================================================
    # DQ-03 Foreign Key Integrity
    # ==================================================

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

    for table in fk_tables:

        df = datasets[table]

        invalid_companies = (
            df.loc[
                ~df["company_id"].isin(companies),
                "company_id",
            ]
            .drop_duplicates()
        )

        for company_id in invalid_companies:

            add_failure(
                failures,
                "DQ-03",
                "CRITICAL",
                table,
                str(company_id),
                "Foreign key missing in companies",
            )

    # ==================================================
    # DQ-04 Balance Sheet Balance (<1%)
    # ==================================================

    df = datasets["balancesheet"]

    balance_failures = df[
        (
            abs(
                df["total_assets"]
                - df["total_liabilities"]
            )
            / df["total_assets"]
        ) > 0.01
    ]

    for _, row in balance_failures.iterrows():

        add_failure(
            failures,
            "DQ-04",
            "WARNING",
            "balancesheet",
            f"{row['company_id']}_{row['year']}",
            "Balance sheet mismatch >1%",
        )

    # ==================================================
    # DQ-05 OPM Cross Check
    # ==================================================

    df = datasets["profitandloss"].copy()

    df = df[df["sales"] > 0]

    df["calculated_opm"] = (
        df["operating_profit"]
        / df["sales"]
    ) * 100

    opm_failures = df[
        abs(
            df["calculated_opm"]
            - df["opm_percentage"]
        ) > 0.5
    ]

    for _, row in opm_failures.iterrows():

        add_failure(
            failures,
            "DQ-05",
            "WARNING",
            "profitandloss",
            f"{row['company_id']}_{row['year']}",
            "OPM percentage mismatch",
        )

    # ==================================================
    # DQ-06 Positive Sales
    # ==================================================

    df = datasets["profitandloss"]

    sales_failures = df[
        df["sales"] <= 0
    ]

    for _, row in sales_failures.iterrows():

        add_failure(
            failures,
            "DQ-06",
            "WARNING",
            "profitandloss",
            f"{row['company_id']}_{row['year']}",
            "Sales must be positive",
        )

    # ==================================================
    # DQ-07 Year Format
    # ==================================================

    year_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
    ]

    for table in year_tables:

        df = datasets[table]

        invalid_years = df[
            (
                df["year"].isna()
            )
            |
            (
                df["year"] < 2000
            )
            |
            (
                df["year"] > 2035
            )
        ]

        for _, row in invalid_years.iterrows():

            add_failure(
                failures,
                "DQ-07",
                "CRITICAL",
                table,
                str(row.get("company_id", "UNKNOWN")),
                f"Invalid year: {row['year']}",
            )   

    # ==================================================
    # DQ-08 Ticker Format
    # ==================================================

    tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "analysis",
        "documents",
        "prosandcons",
        "financial_ratios",
    ]

    for table in tables:

        df = datasets[table]

        invalid = df[
            ~df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.len()
            .between(2, 12)
        ]

        for _, row in invalid.iterrows():

            add_failure(
                failures,
                "DQ-08",
                "CRITICAL",
                table,
                str(row["company_id"]),
                "Invalid ticker length",
            )
# ==================================================
     # DQ-09 Net Cash Check
     # ==================================================

    df = datasets["cashflow"].copy()

    df["calculated_net_cash"] = (
    df["operating_activity"]
            + df["investing_activity"]
            + df["financing_activity"]
        )

    net_cash_failures = df[
            abs(
                df["net_cash_flow"]
                - df["calculated_net_cash"]
            ) > 10
        ]

    for _, row in net_cash_failures.iterrows():

            add_failure(
                failures,
                "DQ-09",
                "WARNING",
                "cashflow",
                f"{row['company_id']}_{row['year']}",
                "Net cash flow mismatch",
            )

    # ==================================================
    # DQ-10 Non-Negative Fixed Assets
    # ==================================================

    df = datasets["balancesheet"]

    fixed_asset_failures = df[
        df["fixed_assets"] < 0
    ]

    for _, row in fixed_asset_failures.iterrows():

        add_failure(
            failures,
            "DQ-10",
            "WARNING",
            "balancesheet",
            f"{row['company_id']}_{row['year']}",
            "Negative fixed assets",
        )

    # ==================================================
    # DQ-11 Tax Rate Range
    # ==================================================

    df = datasets["profitandloss"]

    tax_failures = df[
        (df["tax_percentage"] < 0)
        |
        (df["tax_percentage"] > 60)
    ]

    for _, row in tax_failures.iterrows():

        add_failure(
            failures,
            "DQ-11",
            "WARNING",
            "profitandloss",
            f"{row['company_id']}_{row['year']}",
            "Tax percentage outside range",
        )

    # ==================================================
    # DQ-12 Dividend Payout Cap
    # ==================================================

    df = datasets["profitandloss"]

    dividend_failures = df[
        df["dividend_payout"] > 200
    ]

    for _, row in dividend_failures.iterrows():

        add_failure(
            failures,
            "DQ-12",
            "WARNING",
            "profitandloss",
            f"{row['company_id']}_{row['year']}",
            "Dividend payout exceeds 200%",
        )

    # ==================================================
    # DQ-14 EPS Sign Consistency
    # ==================================================

    df = datasets["profitandloss"]

    eps_failures = df[
        (
            df["net_profit"] > 0
        )
        &
        (
            df["eps"] <= 0
        )
    ]

    for _, row in eps_failures.iterrows():

        add_failure(
            failures,
            "DQ-14",
            "WARNING",
            "profitandloss",
            f"{row['company_id']}_{row['year']}",
            "Positive profit but EPS <= 0",
        )
    # ==================================================
    # DQ-15 BSE/ASE Balance (INFO)
    # ==================================================

    df = datasets["balancesheet"]

    strict_balance = df[
        df["total_assets"]
        != df["total_liabilities"]
    ]

    for _, row in strict_balance.iterrows():

        add_failure(
            failures,
            "DQ-15",
            "INFO",
            "balancesheet",
            f"{row['company_id']}_{row['year']}",
            "Assets not exactly equal liabilities",
        )
    # ==================================================
    # DQ-16 Coverage Check
    # ==================================================

    pnl_counts = (
        datasets["profitandloss"]
        .groupby("company_id")
        .size()
    )

    bs_counts = (
        datasets["balancesheet"]
        .groupby("company_id")
        .size()
    )

    cf_counts = (
        datasets["cashflow"]
        .groupby("company_id")
        .size()
    )

    all_companies = (
        set(pnl_counts.index)
        | set(bs_counts.index)
        | set(cf_counts.index)
    )

    for company in all_companies:

        pnl_years = pnl_counts.get(company, 0)
        bs_years = bs_counts.get(company, 0)
        cf_years = cf_counts.get(company, 0)

        if (
            pnl_years < 5
            or bs_years < 5
            or cf_years < 5
        ):

            add_failure(
                failures,
                "DQ-16",
                "WARNING",
                "coverage",
                company,
                f"P&L={pnl_years}, BS={bs_years}, CF={cf_years}",
            )

    # ==================================================
    # Validation Summary
    # ==================================================

    print("\n==============================")
    print("Validation Rule Summary")
    print("==============================")

    if failures:

        summary = (
            pd.DataFrame(failures)
            .groupby("rule_id")
            .size()
            .reset_index(name="failure_count")
        )

        print(summary.to_string(index=False))

    # ==================================================
    # Generate Validation Report
    # ==================================================

    failures_df = pd.DataFrame(failures)

    failures_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n==============================")
    print("Validation Complete")
    print("==============================")
    print(f"Total Failures: {len(failures_df)}")
    print(f"Output File   : {OUTPUT_FILE}")


if __name__ == "__main__":
    validate()
