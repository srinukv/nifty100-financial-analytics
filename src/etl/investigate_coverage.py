from src.etl.loader import load_all_files

datasets = load_all_files()

for company in ["ATGL", "SBIN"]:

    print("\n" + "=" * 60)
    print(company)

    for table in [
        "profitandloss",
        "balancesheet",
        "cashflow",
    ]:

        df = datasets[table]

        rows = df[
            df["company_id"] == company
        ]

        print(
            table,
            len(rows)
        )

        if len(rows) > 0:
            print(
                rows["year"]
                .sort_values()
                .tolist()
            )