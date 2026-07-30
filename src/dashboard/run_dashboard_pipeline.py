from generate_dashboard_data import (create_revenue_column,
                                     generate_customers_by_revenue,
                                     generate_kpis,
                                     generate_payment_method_by_revenue,
                                     generate_revenue_by_branch,
                                     generate_revenue_by_month,
                                     generate_revenue_by_product,
                                     load_master_data)


def run_dashboard_pipeline() -> int:

    data = load_master_data()

    data = create_revenue_column(data)

    generate_kpis(data)

    generate_revenue_by_branch(data)

    generate_revenue_by_product(data)

    generate_revenue_by_month(data)

    generate_payment_method_by_revenue(data)

    generate_customers_by_revenue(data)

    generated_files = [
        "dashboard_kpis.csv",
        "revenue_by_branch.csv",
        "revenue_by_product.csv",
        "monthly_revenue.csv",
        "payment_methods.csv",
        "top_customers.csv",
    ]

    return len(generated_files)


if __name__ == "__main__":
    run_dashboard_pipeline()
