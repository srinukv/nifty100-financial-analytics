from src.screener.engine import (
    load_master_dataframe,
    prepare_analytics_dataframe,
    run_preset_screener,
)


def test_supported_presets():

    master_df = load_master_dataframe()

    analytics_df = prepare_analytics_dataframe(master_df)

    presets = [
        "quality_compounder",
        "growth_accelerator",
        "debt_free_blue_chip",
    ]

    for preset in presets:

        result = run_preset_screener(analytics_df, preset)

        print("\n" + "=" * 60)
        print(f"Preset : {preset}")
        print(f"Companies Returned : {len(result)}")

        if not result.empty:

            print(
                result[
                    [
                        "company_id",
                        "composite_quality_score",
                    ]
                ].head(10)
            )

        else:
            print("No companies matched.")