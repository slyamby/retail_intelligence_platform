import pandas as pd


def validate_sales_data(
        data: pd.DataFrame
):
    
    issues = {}

    issues["missing_dates"] = (
        data["transaction_date"]
        .isna()
        .sum()
    )

    issues["negative_prices"] = (
        data["unit_price"] < 0
    ).sum()

    issues["invalid_quantities"] = (
        data["quantity"] <= 0
    ).sum()

    return issues