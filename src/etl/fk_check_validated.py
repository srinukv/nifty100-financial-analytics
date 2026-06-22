from pathlib import Path
import pandas as pd

VALIDATED_DIR = Path("data/validated")

companies = set(
pd.read_csv(
VALIDATED_DIR / "companies.csv"
)["id"]
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

total_errors = 0

for table in tables:
    df = pd.read_csv(
    VALIDATED_DIR / f"{table}.csv"
)

invalid = df[
    ~df["company_id"].isin(companies)
]

count = len(invalid)

total_errors += count

print(
    f"{table:<20} {count}"
)

print("\nTotal FK Errors:", total_errors)
