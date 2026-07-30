import pandas as pd

from src.dashboard.generate_dashboard_data import (create_revenue_column,
                                                   generate_kpis,
                                                   generate_revenue_by_branch)


def test_create_revenue_column(sample_sales_data):
    """
    Revenue should equal quantity multiplied
    by unit price.
    """

    result = create_revenue_column(sample_sales_data.copy())

    expected_revenue = [
        10000.00,
        2500.00,
        900.00,
    ]

    assert result["revenue"].tolist() == (expected_revenue)


def test_generate_kpis(sample_sales_data, tmp_path):
    """
    KPI generation should create the correct
    summary values and save a CSV file.
    """

    data = create_revenue_column(sample_sales_data.copy())

    output_path = tmp_path / "dashboard_kpis.csv"

    returned_path = generate_kpis(
        data=data,
        output_path=output_path,
    )

    assert returned_path == output_path
    assert output_path.exists()

    kpis = pd.read_csv(output_path)

    assert (
        kpis.loc[
            0,
            "Total Revenue",
        ]
        == 13400.00
    )

    assert (
        kpis.loc[
            0,
            "Total Transactions",
        ]
        == 3
    )

    assert (
        round(
            kpis.loc[0, "Average Sales"],
            2,
        )
        == 4466.67
    )

    assert (
        kpis.loc[
            0,
            "Customers",
        ]
        == 3
    )

    assert (
        kpis.loc[
            0,
            "Products",
        ]
        == 3
    )

    assert (
        kpis.loc[
            0,
            "Branches",
        ]
        == 2
    )


def test_generate_revenue_by_branch(
    sample_sales_data,
    tmp_path,
):
    """
    Revenue should be grouped correctly by branch.
    """
    data = create_revenue_column(sample_sales_data.copy())

    output_path = tmp_path / "revenue_by_branch.csv"

    generate_revenue_by_branch(
        data=data,
        output_path=output_path,
    )

    result = pd.read_csv(output_path)

    accra_revenue = result.loc[
        result["branch"] == "Accra Central",
        "revenue",
    ].iloc[0]

    kumasi_revenue = result.loc[
        result["branch"] == "Kumasi",
        "revenue",
    ].iloc[0]

    assert accra_revenue == 10900.00
    assert kumasi_revenue == 2500.00
