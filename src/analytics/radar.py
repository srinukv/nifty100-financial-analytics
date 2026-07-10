import os
import numpy as np
import matplotlib.pyplot as plt

RADAR_METRICS = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]


def validate_radar_columns(df):
    """
    Validate that all radar metrics are present
    in the analytics DataFrame.
    """


def prepare_radar_dataset(df):
    """
    Return a copy of the analytics dataset
    containing only the columns required
    for radar chart generation.
    """
    validate_radar_columns(df)

    required_columns = [
        "company_id",
        "company_name",
        "peer_group_name",
        "year",
    ] + RADAR_METRICS

    radar_df = df[required_columns].copy()

    return radar_df
def calculate_peer_group_averages(df):
    """
    Calculate average radar metrics for each peer group.
    """
    peer_df = df[
        df["peer_group_name"].notna()
        & (df["peer_group_name"] != "No peer group assigned")
    ].copy()

    peer_averages = (
        peer_df.groupby("peer_group_name")[RADAR_METRICS]
        .mean()
        .reset_index()
    )

    return peer_averages

def calculate_nifty100_average(radar_df):
    """
    Calculate the average radar metrics
    across the entire Nifty 100 dataset.
    """
    nifty_average = radar_df[RADAR_METRICS].mean()

    return nifty_average

def get_company_radar_data(radar_df, company_id):
    """
    Return radar metrics for a single company.
    """
    company_data = radar_df[radar_df["company_id"] == company_id]

    if company_data.empty:
        raise ValueError(f"Company ID {company_id} not found.")

    return company_data.iloc[0]
def get_peer_group_average(peer_avg_df, peer_group_name):
    """
    Return average radar metrics for a peer group.
    """
    peer_average = peer_avg_df[
        peer_avg_df["peer_group_name"] == peer_group_name
    ]

    if peer_average.empty:
        raise ValueError(f"Peer group '{peer_group_name}' not found.")

    return peer_average.iloc[0]
def create_radar_angles(num_metrics):
    """
    Create equally spaced angles for the radar chart.
    """
    angles = np.linspace(0, 2 * np.pi, num_metrics, endpoint=False).tolist()

    # Close the radar chart polygon
    angles += angles[:1]

    return angles

def plot_radar_chart(
    company_name,
    company_values,
    peer_values,
    metric_labels,
    comparison_label="Peer Average",
):
    """
    Create the base radar chart.
    """
    num_metrics = len(metric_labels)

    angles = create_radar_angles(num_metrics)

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw={"polar": True}
    )

    company_plot = list(company_values) + [company_values[0]]
    peer_plot = list(peer_values) + [peer_values[0]]

    ax.plot(
        angles,
        company_plot,
        linewidth=2,
        label=company_name,
    )

    ax.fill(
        angles,
        company_plot,
        alpha=0.25,
    )

    ax.plot(
        angles,
        peer_plot,
        linestyle="--",
        linewidth=2,
        label=comparison_label,
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_labels, fontsize=10)

    ax.set_title(
        company_name,
        fontsize=14,
        pad=20,
    )

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.2, 1.1),
    )

    ax.grid(True)
    return fig, ax, angles
def save_radar_chart(fig, company_name):
    """
    Save the radar chart as a PNG file.
    """
    output_dir = os.path.join("reports", "radar_charts")
    os.makedirs(output_dir, exist_ok=True)

    safe_company_name = (
    company_name.strip()
    .replace("\n", "")
    .replace("\r", "")
    .replace("/", "-")
    .replace("\\", "-")
    .replace(":", "-")
    .replace("*", "")
    .replace("?", "")
    .replace('"', "")
    .replace("<", "")
    .replace(">", "")
    .replace("|", "")
)

    filename = f"{safe_company_name}_radar.png"
    filepath = os.path.join(output_dir, filename)

    fig.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    return filepath
def generate_company_radar_chart(
    radar_df,
    peer_avg_df,
    company_id,
):
    """
    Generate and save a radar chart for one company.
    """
    company = get_company_radar_data(radar_df, company_id)

    if company["peer_group_name"] == "No peer group assigned":
        peer_average = calculate_nifty100_average(radar_df)
        comparison_label = "Nifty 100 Average"
    else:
        peer_average = get_peer_group_average(
        peer_avg_df,
        company["peer_group_name"],
    )
    comparison_label = "Peer Average"
    metric_labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Revenue CAGR",
        "Composite",
    ]

    company_values = [
        company[metric] for metric in RADAR_METRICS
    ]

    peer_values = [
        peer_average[metric] for metric in RADAR_METRICS
    ]

    fig, _, _ = plot_radar_chart(
    company_name=company["company_name"],
    company_values=company_values,
    peer_values=peer_values,
    metric_labels=metric_labels,
    comparison_label=comparison_label,
)

    return save_radar_chart(
        fig,
        company["company_name"],
    )
def generate_all_radar_charts(radar_df, peer_avg_df):
    """
    Generate radar charts for all companies.
    """
    generated_files = []

    for company_id in radar_df["company_id"]:
        output_path = generate_company_radar_chart(
            radar_df,
            peer_avg_df,
            company_id,
        )
        generated_files.append(output_path)

    return generated_files