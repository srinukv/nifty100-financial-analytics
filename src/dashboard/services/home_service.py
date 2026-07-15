from src.dashboard.utils.db import execute_query


def get_dashboard_summary(year: int) -> dict:
    """
    Return dashboard summary KPIs for the selected year.
    """

    query = """
    SELECT
    company_id,
    return_on_equity_pct,
    debt_to_equity,
    revenue_cagr_5yr
FROM financial_ratios
WHERE year = ?;
    """

    df = execute_query(query, (year,))

    return {
    "average_roe": float(round(df["return_on_equity_pct"].mean(), 2)),
    "median_de": float(round(df["debt_to_equity"].median(), 2)),
    "median_revenue_cagr": float(round(df["revenue_cagr_5yr"].median(), 2)),
    "total_companies": int(df["company_id"].nunique()),
    "debt_free_companies": int((df["debt_to_equity"] == 0).sum()),
    "median_pe": "N/A"
}
def get_sector_breakdown():
    """
    Return sector-wise company counts.
    """

    query = """
    SELECT
        broad_sector,
        COUNT(*) AS company_count
    FROM sectors
    GROUP BY broad_sector
    ORDER BY company_count DESC;
    """

    return execute_query(query)

def get_top_quality_companies(year: int):
    """
    Return the Top 5 companies by Composite Quality Score.
    """

    query = """
    SELECT
        c.id AS ticker,
        c.company_name,
        fr.composite_quality_score
    FROM financial_ratios fr
    JOIN companies c
        ON fr.company_id = c.id
    WHERE fr.year = ?
      AND fr.composite_quality_score IS NOT NULL
    ORDER BY fr.composite_quality_score DESC
    LIMIT 5;
    """

    return execute_query(query, (year,))