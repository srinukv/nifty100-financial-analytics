from src.screener.engine import (
    load_master_dataframe,
    prepare_analytics_dataframe,
    run_preset_screener,
)

from src.screener.scoring import (
    prepare_scoring_metrics,
    calculate_composite_score,
    calculate_sector_relative_score,
)

from src.screener.export import export_screeners_to_excel


master_df = load_master_dataframe()

analytics_df = prepare_analytics_dataframe(master_df)

scoring_df = prepare_scoring_metrics(analytics_df)

result_df = calculate_composite_score(scoring_df)

result_df = calculate_sector_relative_score(result_df)

presets = [
    "quality_compounder",
    "growth_accelerator",
    "debt_free_blue_chip",
]

results = {}

for preset in presets:
    results[preset] = run_preset_screener(
        result_df,
        preset,
    )

export_screeners_to_excel(results)

print("Excel export completed successfully.")