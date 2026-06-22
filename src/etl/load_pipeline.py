from pathlib import Path
import pandas as pd

from src.etl.loader import load_all_files

OUTPUT_FILE = Path("output/load_audit.csv")


def main():

    datasets = load_all_files()

    load_order = [
        "companies",
        "sectors",
        "peer_groups",
        "analysis",
        "prosandcons",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "stock_prices",
        "documents",
    ]

    audit_rows = []

    print("\nFULL DATA LOAD")
    print("=" * 60)

    for order, table in enumerate(load_order, start=1):

        df = datasets[table]

        audit_rows.append(
            {
                "load_order": order,
                "table_name": table,
                "row_count": len(df),
                "column_count": len(df.columns),
                "status": "SUCCESS",
            }
        )

        print(
            f"{order:02d}. "
            f"{table:<20} "
            f"Rows={len(df)} "
            f"Cols={len(df.columns)}"
        )

    audit_df = pd.DataFrame(audit_rows)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    audit_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\nLoad Audit Generated")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()