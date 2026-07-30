from pathlib import Path

import pandas as pd

from config.settings import PROCESSED_DATA_DIR
from src.utils.logger import logger


def load_summary_dataset(file_path: Path) -> pd.DataFrame:
    """
    Load a dashboard summary dataset.

    Raises
    ------
    FileNotFoundError
        If the expected dashboard file is missing.

    ValueError
        If the file is empty.
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Dashboard dataset not found:" f"{file_path}")

    data = pd.read_csv(file_path)

    if data.empty:
        raise ValueError(f"Dashboard dataset is empty: " f"{file_path}")

    return data


def format_currency(
    value: float,
) -> str:
    """
    Format a numeric value as Ghana cedis.
    """

    return f"GHS {value:,.2f}"


def generate_branch_insight(
    data: pd.DataFrame,
) -> str:
    """
    Identify the highest revenue-generating branch.
    """

    top_branch = data.loc[data["revenue"].idxmax()]

    branch_name = top_branch["branch"]
    branch_revenue = top_branch["revenue"]

    return (
        f"{branch_name} generated the highest "
        f"branch revenue at "
        f"{format_currency(branch_revenue)}"
    )


def generate_product_insight(data: pd.DataFrame) -> str:
    """
    Identify the highest revenue-generating product.
    """

    top_product = data.loc[data["revenue"].idxmax()]

    product_name = top_product["product"]
    product_revenue = top_product["revenue"]

    return (
        f"{product_name} was the highest "
        f"revenue-generating product at "
        f"{format_currency(product_revenue)}."
    )


def generate_payment_insight(data: pd.DataFrame) -> str:
    """
    Identify the most frequently used payment method.
    """
    top_payment = data.loc[data["revenue"].idxmax()]

    payment_method = top_payment["payment_method"]

    transaction_count = int(top_payment["revenue"])

    return (
        f"{payment_method} was the most-used "
        f"payment method with "
        f"{transaction_count:,} transactions."
    )


def get_kpi_value(
    data: pd.DataFrame,
    kpi_column: str,
) -> float:
    """
    Retrieve a KPI value from a wide-format KPI dataset.

    Parameters
    ----------
    data:
        KPI DataFrame containing KPI values as columns.

    kpi_column:
        Name of the KPI column to retrieve.

    Returns
    -------
    float
        Numeric KPI value.

    Raises
    ------
    ValueError
        If the KPI column is missing, contains no value,
        or contains a non-numeric value.
    """

    normalised_data = data.copy()

    normalised_data.columns = (
        normalised_data.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    normalised_kpi_column = kpi_column.strip().lower().replace(" ", "_")

    if normalised_kpi_column not in normalised_data.columns:
        raise ValueError(
            f"KPI column not found: {kpi_column}. "
            f"Available KPI columns: "
            f"{normalised_data.columns.tolist()}"
        )

    kpi_values = normalised_data[normalised_kpi_column].dropna()

    if kpi_values.empty:
        raise ValueError(f"KPI column contains no value: " f"{kpi_column}")

    try:
        return float(kpi_values.iloc[0])

    except (TypeError, ValueError) as error:
        raise ValueError(f"KPI value in '{kpi_column}' " "is not numeric.") from error


def generate_average_sale_insight(
    data: pd.DataFrame,
) -> str:
    """
    Report the average transaction value.
    """

    average_sale = get_kpi_value(
        data=data,
        kpi_column="average_sales",
    )

    return "Average transaction value was " f"{format_currency(average_sale)}."


def generate_customer_concentration_insight(
    customer_data: pd.DataFrame,
    kpi_data: pd.DataFrame,
) -> str:
    """
    Calculate the share of revenue contributed by
    customers in the top-customer dataset.
    """

    total_revenue = get_kpi_value(
        data=kpi_data,
        kpi_column="total_revenue",
    )

    top_customer_revenue = customer_data["revenue"].sum()

    if total_revenue <= 0:
        return (
            "Customer revenue concentration could "
            "not be calculated because total "
            "revenue was zero."
        )

    revenue_share = top_customer_revenue / total_revenue * 100

    customer_count = len(customer_data)

    return (
        f"The top {customer_count} customers "
        f"contributed {revenue_share:.1f}% "
        f"of total revenue."
    )


def generate_business_insights(data_dir: Path = PROCESSED_DATA_DIR) -> list[str]:
    """
    Generate executive business insights from
    dashboard-ready summary datasets.
    """

    logger.info("Business insight generation started.")

    kpi_data = load_summary_dataset(file_path=(data_dir / "dashboard_kpis.csv"))

    branch_data = load_summary_dataset(file_path=(data_dir / "revenue_by_branch.csv"))

    product_data = load_summary_dataset(file_path=(data_dir / "revenue_by_product.csv"))

    payment_data = load_summary_dataset(file_path=(data_dir / "payment_methods.csv"))

    customer_data = load_summary_dataset(file_path=(data_dir / "top_customers.csv"))

    insights = [
        generate_branch_insight(branch_data),
        generate_product_insight(product_data),
        generate_payment_insight(payment_data),
        generate_average_sale_insight(kpi_data),
        generate_customer_concentration_insight(
            customer_data=customer_data,
            kpi_data=kpi_data,
        ),
    ]

    logger.info(
        "%s business insights generated.",
        len(insights),
    )

    return insights
