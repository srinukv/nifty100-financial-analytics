from src.screener.engine import (
    load_master_dataframe,
    prepare_analytics_dataframe,
    run_preset_screener,
)

PRESETS = [
    "quality_compounder",
    "growth_accelerator",
    "debt_free_blue_chip",
]

master_df = load_master_dataframe()
analytics_df = prepare_analytics_dataframe(master_df)

print(f"Analytics Universe: {len(analytics_df)} companies\n")

for preset in PRESETS:
    result = run_preset_screener(analytics_df, preset)

    print("=" * 60)
    print(f"Preset : {preset}")
    print(f"Companies Returned : {len(result)}")

    if not result.empty:
        print(result[
            [
                "company_id",
                "company_name",
                "composite_quality_score",
            ]
        ].head(10))

    print()