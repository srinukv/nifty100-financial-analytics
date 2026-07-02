import sqlite3
import pandas as pd

DB_PATH = "nifty100.db"
OUTPUT_FILE = "output/ratio_edge_cases.log"


def load_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fr.company_id,
        fr.year,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        c.roe_percentage AS source_roe,
        c.roce_percentage AS source_roce
    FROM financial_ratios fr
    JOIN companies c
        ON fr.company_id = c.id
    WHERE fr.year IS NOT NULL
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df = (
    df.sort_values("year")
      .groupby("company_id", as_index=False)
      .tail(1)
      .reset_index(drop=True)
)

    return df
def classify_anomaly(row):
    """
    Categorize ratio validation anomalies.
    """

    max_diff = max(
        row["roe_abs_difference"],
        row["roce_abs_difference"]
    )

    if max_diff >= 50:
        return "Formula Discrepancy"

    if max_diff >= 15:
        return "Data Source Issue"

    return "Version Difference"

def main():
    df = load_data()
    df["roe_difference"] = (
    df["return_on_equity_pct"] -
    df["source_roe"]
).round(2)

    df["roce_difference"] = (
    df["return_on_capital_employed_pct"] -
    df["source_roce"]
).round(2)

    df["roe_abs_difference"] = (
    df["roe_difference"]
    .abs()
)

    df["roce_abs_difference"] = (
    df["roce_difference"]
    .abs()
)
    anomalies = df[
    (df["roe_abs_difference"] > 5) |
    (df["roce_abs_difference"] > 5)
    ].copy()
    anomalies["category"] = anomalies.apply(
    classify_anomaly,
    axis=1
)
    print("\nAnomalies Found:", len(anomalies))

    print(
    anomalies[
        [
            "company_id",
            "return_on_equity_pct",
            "source_roe",
            "roe_difference",
            "return_on_capital_employed_pct",
            "source_roce",
            "roce_difference",
        ]
        ].head(20)
    )
    print("\nCategory Summary:\n")

    print(
    anomalies["category"]
    .value_counts()
)

    print("\nSample Categorized Anomalies:\n")

    print(
    anomalies[
        [
            "company_id",
            "roe_difference",
            "roce_difference",
            "category"
        ]
    ].head(10)
)
    
    print(df.head())
    print(f"\nRows loaded: {len(df)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("Nifty100 Ratio Edge Case Report\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"Companies Compared : {len(df)}\n")
        f.write(f"Anomalies Found    : {len(anomalies)}\n\n")

        f.write("Category Summary\n")
        f.write("-" * 30 + "\n")

        for category, count in anomalies["category"].value_counts().items():
            f.write(f"{category}: {count}\n")

        f.write("\nDetailed Anomalies\n")
        f.write("-" * 30 + "\n\n")

        for _, row in anomalies.iterrows():
            f.write(
                f"{row['company_id']} | "
                f"ROE Diff: {row['roe_difference']:.2f} | "
                f"ROCE Diff: {row['roce_difference']:.2f} | "
                f"{row['category']}\n"
        )

    print(f"\nEdge case report saved to: {OUTPUT_FILE}")
if __name__ == "__main__":
    main()