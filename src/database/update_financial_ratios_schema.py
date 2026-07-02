import sqlite3

DB_PATH = "nifty100.db"

NEW_COLUMNS = [
    ("revenue_cagr_5yr", "REAL"),
    ("pat_cagr_5yr", "REAL"),
    ("eps_cagr_5yr", "REAL"),
    ("composite_quality_score", "REAL"),
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for column_name, column_type in NEW_COLUMNS:
    try:
        cursor.execute(
            f"""
            ALTER TABLE financial_ratios
            ADD COLUMN {column_name} {column_type}
            """
        )
        print(f"Added: {column_name}")
    except sqlite3.OperationalError:
        print(f"Already exists: {column_name}")

conn.commit()
conn.close()

print("\nSchema Updated Successfully")