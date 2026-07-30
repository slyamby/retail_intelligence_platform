from pathlib import Path

import pandas as pd

from config.settings import MASTER_DATASET, PROCESSED_DATA_DIR, RAW_DATA_DIR
from src.utils.logger import logger

BRANCH_MAPPING = {
    "accra central": "Accra Central",
    "east legon": "East Legon",
    "kumasi": "Kumasi",
    "takoradi": "Takoradi",
    "tema": "Tema",
}

PRODUCT_MAPPING = {
    "printer": "Printer",
    "office printer": "Printer",
    "laptop": "Laptop",
    "laptops": "Laptop",
    "keyboard": "Keyboard",
    "key board": "Keyboard",
    "monitor": "Monitor",
    "led monitor": "Monitor",
    "mouse": "Mouse",
    "wireless mouse": "Mouse",
}

PAYMENT_METHOD_MAPPING = {
    "card": "Card",
    "mobile money": "Mobile Money",
    "momo": "Mobile Money",
    "cash": "Cash",
    "bank transfer": "Bank Transfer",
}


def load_data(
    file_paths: list[Path],
) -> pd.DataFrame:
    """
    Load and combine validated raw CSV files.

    Returns
    -------
    pandas.DataFrame
    """
    # csv_files = list(
    #    RAW_DATA_DIR.glob("*.csv")
    # )

    dataframes = []

    for file_path in file_paths:
        df = pd.read_csv(file_path)

        df["source_file"] = file_path.name

        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def remove_duplicate_rows(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    before = len(data)

    data = data.drop_duplicates()

    after = len(data)

    logger.info(f"Removed {before-after} duplicates.")

    return data


def clean_branch_names(data: pd.DataFrame) -> pd.DataFrame:
    """Standardise branch names using approved business mappings."""

    data = data.copy()

    normalised_branch = data["branch"].astype("string").str.strip().str.lower()

    mapped_branch = normalised_branch.map(BRANCH_MAPPING)

    unmapped_values = normalised_branch[mapped_branch.isna()].dropna().unique()

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped branch values found:",
            unmapped_values.tolist(),
        )

    data["branch"] = mapped_branch

    return data


def clean_product_names(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize product names using approved business mappings"""

    data = data.copy()

    normalised_products = data["product"].astype("string").str.strip().str.lower()

    mapped_product = normalised_products.map(PRODUCT_MAPPING)

    unmapped_values = normalised_products[mapped_product.isna()].dropna().unique()

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped product values found:",
            unmapped_values.tolist(),
        )

    data["product"] = mapped_product

    return data


def clean_payment_methods(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize payment method names using approved business mappings"""

    data = data.copy()

    normalised_payment_method = (
        data["payment_method"].astype("string").str.strip().str.lower()
    )

    mapped_payment_method = normalised_payment_method.map(PAYMENT_METHOD_MAPPING)

    unmapped_values = (
        normalised_payment_method[mapped_payment_method.isna()].dropna().unique()
    )

    if len(unmapped_values) > 0:
        print(
            "Warning: Unmapped payment method found:",
            unmapped_values.tolist(),
        )

    data["payment_method"] = mapped_payment_method

    return data


def clean_dates(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert mixed transaction-date formats to datetime.

    Unparseable values are converted to NaT and reported.
    """

    data = data.copy()

    original_dates = data["transaction_date"].copy()

    data["transaction_date"] = pd.to_datetime(
        data["transaction_date"],
        format="mixed",
        errors="coerce",
        dayfirst=True,
    )

    invalid_date_count = data["transaction_date"].isna().sum()

    logger.warning(
        "%s transaction dates could not be parsed.",
        invalid_date_count,
    )

    if invalid_date_count > 0:
        invalid_values = (
            original_dates[data["transaction_date"].isna()].dropna().unique().tolist()
        )

        logger.warning(
            "Unparseable date values: %s",
            invalid_values,
        )

    return data


def clean_unit_prices(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert unit prices to numeric values
    """

    data = data.copy()

    data["unit_price"] = (
        data["unit_price"]
        .astype("string")
        .str.replace("GHS", "", regex=False)
        .str.replace("₵", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")

    return data


def clean_quantities(data: pd.DataFrame) -> pd.DataFrame:
    """
    Validate quantities
    """

    data = data.copy()

    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")

    """
    invalid_quantity = data["quantity"] <= 0

    logger.warning(
        f"Invalid quantities: {invalid_quantity.sum()}"
    )"""

    return data


def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:

    data = data.copy()

    data["customer_name"] = data["customer_name"].fillna("Unknown")

    return data


def rejected_records(data: pd.DataFrame) -> pd.DataFrame:
    rejected_records = data.loc[
        data["transaction_date"].isna()
        | data["quantity"].isna()
        | data["quantity"].le(0)
    ].copy()

    rejected_records["rejection_reason"] = ""

    rejected_records.loc[
        rejected_records["transaction_date"].isna(), "rejection_reason"
    ] += "Invalid date; "

    rejected_records.loc[
        rejected_records["quantity"].isna(), "rejection_reason"
    ] += "Invalid quantity; "

    rejected_records.loc[
        rejected_records["quantity"].le(0), "rejection_reason"
    ] += "Quantity must be greater than zero; "

    return rejected_records


def save_clean_data(data: pd.DataFrame, output_path: Path = MASTER_DATASET) -> Path:
    """
    Save the cleaned dataset as a CSV file.

    Parameters
    ----------
    data:
        Cleaned sales dataset.

    output_path:
        Destination path for the cleaned CSV file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(output_path, index=False)

    logger.info(
        "Cleaned dataset saved to %s.",
        output_path,
    )

    return output_path
