import pandas as pd

from src.data.clean_data import (clean_branch_names, clean_dates,
                                 clean_payment_methods, clean_product_names,
                                 clean_quantities, clean_unit_prices,
                                 handle_missing_values, rejected_records,
                                 remove_duplicate_rows, save_clean_data)


def test_remove_duplicate_rows():
    """
    Duplicate rows should be removed while
    retaining one copy of each record.
    """

    data = pd.DataFrame(
        {
            "transaction_id": [
                "TX001",
                "TX001",
                "TX002",
            ],
            "product": [
                "Laptop",
                "Laptop",
                "Printer",
            ],
        }
    )

    result = remove_duplicate_rows(data)

    assert len(result) == 2
    assert result["transaction_id"].tolist() == [
        "TX001",
        "TX002",
    ]


def test_clean_branch_names():
    """
    Branch names should be normalised using
    the approved mapping.
    """

    data = pd.DataFrame(
        {
            "branch": [
                " ACCRA CENTRAL ",
                "east legon",
                "KUMASI",
                " Tema ",
            ]
        }
    )

    result = clean_branch_names(data)

    assert result["branch"].tolist() == [
        "Accra Central",
        "East Legon",
        "Kumasi",
        "Tema",
    ]


def test_clean_branch_names_sets_unmapped_values_to_missing():
    """
    Branches not found in the approved mapping
    should become missing values.
    """

    data = pd.DataFrame(
        {
            "branch": [
                "Accra Central",
                "Cape Coast",
            ]
        }
    )

    result = clean_branch_names(data)

    assert result.loc[0, "branch"] == ("Accra Central")

    assert pd.isna(result.loc[1, "branch"])


def test_clean_product_names():
    """
    Product aliases should be converted to
    approved product names.
    """

    data = pd.DataFrame(
        {
            "product": [
                "LAPTOPS",
                " office printer ",
                "Key Board",
                "LED Monitor",
                "wireless mouse",
            ]
        }
    )

    result = clean_product_names(data)

    assert result["product"].tolist() == [
        "Laptop",
        "Printer",
        "Keyboard",
        "Monitor",
        "Mouse",
    ]


def test_clean_payment_methods():
    """
    Payment-method aliases should be converted
    to approved values.
    """

    data = pd.DataFrame(
        {
            "payment_method": [
                " CARD ",
                "momo",
                "MOBILE MONEY",
                "cash",
                "BANK TRANSFER",
            ]
        }
    )

    result = clean_payment_methods(data)

    assert result["payment_method"].tolist() == [
        "Card",
        "Mobile Money",
        "Mobile Money",
        "Cash",
        "Bank Transfer",
    ]


def test_clean_dates_converts_mixed_formats():
    """
    Supported mixed date formats should be
    converted to pandas datetime values.
    """

    data = pd.DataFrame(
        {
            "transaction_date": [
                "15/01/2026",
                "2026-02-20",
                "03-03-2026",
            ]
        }
    )

    result = clean_dates(data)

    assert pd.api.types.is_datetime64_any_dtype(result["transaction_date"])

    assert result["transaction_date"].isna().sum() == 0

    assert result.loc[
        0,
        "transaction_date",
    ] == pd.Timestamp("2026-01-15")


def test_clean_dates_converts_invalid_values_to_nat():
    """
    Unparseable date values should become NaT.
    """

    data = pd.DataFrame(
        {
            "transaction_date": [
                "2026-01-15",
                "not-a-date",
            ]
        }
    )

    result = clean_dates(data)

    assert result.loc[
        0,
        "transaction_date",
    ] == pd.Timestamp("2026-01-15")

    assert pd.isna(
        result.loc[
            1,
            "transaction_date",
        ]
    )


def test_clean_unit_prices():
    """
    Currency labels, symbols and commas should
    be removed before numeric conversion.
    """

    data = pd.DataFrame(
        {
            "unit_price": [
                "GHS 5,000.00",
                "₵2,500",
                "300",
                "invalid",
            ]
        }
    )

    result = clean_unit_prices(data)

    assert (
        result.loc[
            0,
            "unit_price",
        ]
        == 5000.00
    )

    assert (
        result.loc[
            1,
            "unit_price",
        ]
        == 2500.00
    )

    assert (
        result.loc[
            2,
            "unit_price",
        ]
        == 300.00
    )

    assert pd.isna(
        result.loc[
            3,
            "unit_price",
        ]
    )


def test_clean_quantities():
    """
    Quantity values should be converted to
    numeric values, with invalid entries
    becoming missing.
    """

    data = pd.DataFrame(
        {
            "quantity": [
                "5",
                "2.5",
                "invalid",
                None,
            ]
        }
    )

    result = clean_quantities(data)

    assert (
        result.loc[
            0,
            "quantity",
        ]
        == 5
    )

    assert (
        result.loc[
            1,
            "quantity",
        ]
        == 2.5
    )

    assert pd.isna(
        result.loc[
            2,
            "quantity",
        ]
    )

    assert pd.isna(
        result.loc[
            3,
            "quantity",
        ]
    )


def test_handle_missing_customer_names():
    """
    Missing customer names should be replaced
    with 'Unknown'.
    """

    data = pd.DataFrame(
        {
            "customer_name": [
                "Customer A",
                None,
                pd.NA,
            ]
        }
    )

    result = handle_missing_values(data)

    assert result["customer_name"].tolist() == [
        "Customer A",
        "Unknown",
        "Unknown",
    ]


def test_rejected_records_identifies_invalid_rows():
    """
    Rows with invalid dates, missing quantities
    or non-positive quantities should be rejected.
    """

    data = pd.DataFrame(
        {
            "transaction_date": pd.to_datetime(
                [
                    "2026-01-10",
                    None,
                    "2026-01-12",
                    "2026-01-13",
                ]
            ),
            "quantity": [
                2,
                1,
                None,
                0,
            ],
            "product": [
                "Laptop",
                "Printer",
                "Keyboard",
                "Monitor",
            ],
        }
    )

    result = rejected_records(data)

    assert len(result) == 3

    assert result.index.tolist() == [
        1,
        2,
        3,
    ]


def test_rejected_records_assigns_reasons():
    """
    Each rejected record should include an
    appropriate rejection reason.
    """

    data = pd.DataFrame(
        {
            "transaction_date": pd.to_datetime(
                [
                    None,
                    "2026-01-11",
                    "2026-01-12",
                ]
            ),
            "quantity": [
                2,
                None,
                -1,
            ],
        }
    )

    result = rejected_records(data)

    assert "Invalid date" in result.loc[0, "rejection_reason"]

    assert "Invalid quantity" in result.loc[1, "rejection_reason"]

    assert "Quantity must be greater than zero" in result.loc[2, "rejection_reason"]


def test_rejected_records_can_have_multiple_reasons():
    """
    A row that violates multiple rules should
    contain all applicable rejection reasons.
    """

    data = pd.DataFrame(
        {
            "transaction_date": [pd.NaT],
            "quantity": [None],
        }
    )

    result = rejected_records(data)

    rejection_reason = result.loc[
        0,
        "rejection_reason",
    ]

    assert "Invalid date" in rejection_reason
    assert "Invalid quantity" in rejection_reason


def test_save_clean_data(
    sample_sales_data,
    tmp_path,
):
    """
    Cleaned data should be written to the
    supplied output path.
    """

    output_path = tmp_path / "master_sales.csv"

    returned_path = save_clean_data(
        data=sample_sales_data,
        output_path=output_path,
    )

    assert returned_path == output_path
    assert output_path.exists()

    saved_data = pd.read_csv(output_path)

    assert len(saved_data) == 3

    assert saved_data.columns.tolist() == (sample_sales_data.columns.tolist())
