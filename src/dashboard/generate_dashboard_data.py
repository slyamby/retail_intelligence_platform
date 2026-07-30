from pathlib import Path

import pandas as pd

from config.settings import (DASHBOARD_KPI_FILE, MASTER_DATASET,
                             MONTHLY_REVENUE_FILE, PAYMENT_METHOD_FILE,
                             PROCESSED_DATA_DIR, REVENUE_BY_BRANCH_FILE,
                             REVENUE_BY_PRODUCT_FILE, TOP_CUSTOMERS_FILE)
from src.utils.logger import logger


def load_master_data(input_path: Path = MASTER_DATASET) -> pd.DataFrame:
    """
    Purpose:
        Load and preprocess the master sales dataset.

    Inputs:
        Clean master sales dataset.

    Outputs:
        Preprocessed DataFrame.
    """

    data = pd.read_csv(input_path)

    data["transaction_date"] = pd.to_datetime(data["transaction_date"], errors="coerce")

    logger.info(f"Loaded master sales data with {len(data)} rows.")

    return data


def create_revenue_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Purpose:
        Create a revenue column based on quantity and unit price.

    Inputs:
        Clean master sales dataset.

    Outputs:
        DataFrame with revenue column.
    """

    data["revenue"] = data["quantity"] * data["unit_price"]

    logger.info(f"Created revenue column with {len(data)} rows.")

    return data


def save_dashboard_data_set(
    data: pd.DataFrame,
    file_path: Path,
) -> Path:
    """
    Purpose:
        Save the processed dashboard data to a CSV file.

    Inputs:
        Processed DataFrame.

    Outputs:
        None.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(file_path, index=False)

    logger.info(f"SUCCESS! File saved to %s", file_path)

    return file_path


def generate_kpis(data: pd.DataFrame, output_path: Path = DASHBOARD_KPI_FILE) -> Path:
    """
    Purpose:
        Generate key performance indicators (KPIs) from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves KPIs to a CSV file.
    """

    total_revenue = data["revenue"].sum()

    total_transactions = len(data)

    average_sale = total_revenue / total_transactions if total_revenue > 0 else 0

    number_of_customers = data["customer_name"].nunique()

    number_of_products = data["product"].nunique()

    number_of_branches = data["branch"].nunique()

    kpis = pd.DataFrame(
        {
            "Total Revenue": [total_revenue],
            "Total Transactions": [total_transactions],
            "Average Sales": [average_sale],
            "Customers": [number_of_customers],
            "Products": [number_of_products],
            "Branches": [number_of_branches],
        }
    )

    return save_dashboard_data_set(data=kpis, file_path=output_path)


def generate_revenue_by_branch(
    data: pd.DataFrame,
    output_path: Path = REVENUE_BY_BRANCH_FILE,
) -> Path:
    """
    Purpose:
        Generate revenue by branch from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves revenue by branch to a CSV file.
    """

    branch_revenue = (
        data.groupby(
            "branch",
            as_index=False,
        )["revenue"]
        .sum()
        .sort_values(
            by="revenue",
            ascending=False,
        )
    )

    return save_dashboard_data_set(
        data=branch_revenue,
        file_path=output_path,
    )


def generate_revenue_by_product(
    data: pd.DataFrame, output_path: Path = REVENUE_BY_PRODUCT_FILE
) -> Path:
    """
    Purpose:
        Generate revenue by product from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves revenue by product to a CSV file.
    """

    product_revenue = (
        data.groupby(
            "product",
            as_index=False,
        )["revenue"]
        .sum()
        .sort_values(
            by="revenue",
            ascending=False,
        )
    )

    return save_dashboard_data_set(data=product_revenue, file_path=output_path)


def generate_revenue_by_month(
    data: pd.DataFrame, output_path: Path = MONTHLY_REVENUE_FILE
) -> Path:
    """
    Purpose:
        Generate revenue by month from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves revenue by month to a CSV file.
    """
    data = data.copy()

    # Storing date in the format Jan-2026 instead of 2026-01-01
    data["month"] = data["transaction_date"].dt.to_period("M").dt.to_timestamp()

    monthly_revenue = (
        data.groupby(
            "month",
            as_index=False,
        )["revenue"]
        .sum()
        .sort_values(
            by="month",
            ascending=True,
            ignore_index=True,
        )
    )

    return save_dashboard_data_set(data=monthly_revenue, file_path=output_path)


def generate_customers_by_revenue(
    data: pd.DataFrame, output_path: Path = TOP_CUSTOMERS_FILE
):
    """
    Purpose:
        Generate revenue by customer from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves revenue by customer to a CSV file.
    """

    top_10_customers = (
        data.groupby(
            "customer_name",
            as_index=False,
        )["revenue"]
        .sum()
        .sort_values(
            by="revenue",
            ascending=False,
        )
        .head(10)
    )

    return save_dashboard_data_set(data=top_10_customers, file_path=output_path)


def generate_payment_method_by_revenue(
    data: pd.DataFrame, output_path: Path = PAYMENT_METHOD_FILE
):
    """
    Purpose:
        Generate revenue by payment method from the processed sales data.

    Inputs:
        Processed DataFrame.

    Outputs:
        None. Saves revenue by payment method to a CSV file.
    """

    payment_method = (
        data.groupby(
            "payment_method",
            as_index=False,
        )["revenue"]
        .sum()
        .sort_values(
            by="revenue",
            ascending=False,
        )
    )

    return save_dashboard_data_set(data=payment_method, file_path=output_path)


def run_dashboard_pipeline(
    input_path: Path = MASTER_DATASET,
    output_dir: Path = PROCESSED_DATA_DIR,
) -> list[Path]:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = load_master_data(input_path=input_path)

    data = create_revenue_column(data)

    kpi_path = generate_kpis(
        data=data,
        output_path=(output_dir / "dashboard_kpis.csv"),
    )

    branch_revenue_path = generate_revenue_by_branch(
        data=data,
        output_path=(output_dir / "revenue_by_branch.csv"),
    )

    product_revenue_path = generate_revenue_by_product(
        data=data, output_path=(output_dir / "revenue_by_product.csv")
    )

    monthly_revenue_path = generate_revenue_by_month(
        data=data,
        output_path=(output_dir / "monthly_revenue.csv"),
    )

    payment_method_path = generate_payment_method_by_revenue(
        data=data,
        output_path=(output_dir / "payment_methods.csv"),
    )

    customer_revenue_path = generate_customers_by_revenue(
        data=data,
        output_path=(output_dir / "top_customers.csv"),
    )

    generated_files = [
        kpi_path,
        branch_revenue_path,
        product_revenue_path,
        monthly_revenue_path,
        payment_method_path,
        customer_revenue_path,
    ]

    logger.info(
        "Generated %s dashboard datasets.",
        len(generated_files),
    )

    return generated_files


if __name__ == "__main__":
    run_dashboard_pipeline()
