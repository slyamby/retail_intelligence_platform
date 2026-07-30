import pandas as pd
import pytest


@pytest.fixture
def sample_sales_data() -> pd.DataFrame:
    """
    Return a small valid BrightMart sales dataset
    for automated tests.
    """

    return pd.DataFrame(
        {
            "transaction_date": [
                "2026-01-10",
                "2026-01-11",
                "2026-02-01",
            ],
            "branch": [
                "Accra Central",
                "Kumasi",
                "Accra Central",
            ],
            "product": [
                "Laptop",
                "Printer",
                "Keyboard",
            ],
            "quantity": [
                2,
                1,
                3,
            ],
            "unit_price": [
                5000.00,
                2500.00,
                300.00,
            ],
            "customer_name": [
                "Customer A",
                "Customer B",
                "Customer C",
            ],
            "payment_method": [
                "Card",
                "Cash",
                "Mobile Money",
            ],
        }
    )
