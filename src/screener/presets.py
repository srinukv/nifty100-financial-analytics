"""
Preset Screener Definitions

Each preset is a dictionary of filters that will be passed
to the generic filter engine.
"""

PRESET_SCREENERS = {

    "quality_compounder": {
        "return_on_equity_pct": {
            "operator": ">",
            "value": 15
        },
        "debt_to_equity": {
            "operator": "<",
            "value": 1.0
        },
        "free_cash_flow_cr": {
            "operator": ">",
            "value": 0
        },
        "revenue_cagr_5yr": {
            "operator": ">",
            "value": 10
        }
    },

    "growth_accelerator": {
        "pat_cagr_5yr": {
            "operator": ">",
            "value": 20
        },
        "revenue_cagr_5yr": {
            "operator": ">",
            "value": 15
        },
        "debt_to_equity": {
            "operator": "<",
            "value": 2.0
        }
    },

    "debt_free_blue_chip": {
        "debt_to_equity": {
            "operator": "==",
            "value": 0
        },
        "return_on_equity_pct": {
            "operator": ">",
            "value": 12
        },
        "sales": {
            "operator": ">",
            "value": 5000
        }
    }
}


PENDING_PRESETS = {
    "value_pick": [
        "pe_ratio",
        "pb_ratio",
        "dividend_yield"
    ],

    "dividend_champion": [
        "dividend_yield"
    ],

    "turnaround_watch": [
        "revenue_cagr_3yr",
        "debt_to_equity_yoy_trend"
    ]
}


def get_preset(name: str):
    """
    Return the filter dictionary for a preset.

    Raises:
        ValueError if preset is unknown.
        NotImplementedError if preset depends on
        metrics that are not yet available.
    """

    name = name.lower()

    if name in PRESET_SCREENERS:
        return PRESET_SCREENERS[name]

    if name in PENDING_PRESETS:
        missing = ", ".join(PENDING_PRESETS[name])
        raise NotImplementedError(
            f"'{name}' requires additional metrics: {missing}"
        )

    raise ValueError(f"Unknown preset: {name}")