import time
from pathlib import Path

from config.settings import (DASHBOARD_KPI_FILE, EXPECTED_OUTPUT_FILENAMES,
                             MASTER_DATASET, MONTHLY_REVENUE_FILE,
                             PAYMENT_METHOD_FILE, PROCESSED_DATA_DIR,
                             REVENUE_BY_BRANCH_FILE, REVENUE_BY_PRODUCT_FILE,
                             STAGING_DATA_DIR, TOP_CUSTOMERS_FILE)
from src.dashboard.generate_dashboard_data import run_dashboard_pipeline
from src.pipeline.run_pipeline import run_pipeline
from src.reporting.insight_generator import generate_business_insights
from src.reporting.report_generator import (build_summary_report,
                                            save_summary_report)
from src.utils.logger import logger
from src.utils.output_manager import (prepare_staging_directory,
                                      publish_staged_outputs,
                                      verify_expected_outputs)
from src.utils.pipeline_stats import PipelineStatistics


def get_expected_output_files() -> list[Path]:
    """
    Return the expected reporting output files.
    """

    return [
        MASTER_DATASET,
        DASHBOARD_KPI_FILE,
        REVENUE_BY_BRANCH_FILE,
        REVENUE_BY_PRODUCT_FILE,
        MONTHLY_REVENUE_FILE,
        PAYMENT_METHOD_FILE,
        TOP_CUSTOMERS_FILE,
    ]


def get_generated_output_files() -> list[Path]:
    """
    Return reporting output files that exist.
    """

    expected_files = get_expected_output_files()

    return [file_path for file_path in expected_files if file_path.exists()]


def display_success_summary(
    rows_processed: int,
    dashboard_files_generated: int,
    total_execution_time: float,
    summary_report_name: str,
    business_insights: list[str],
) -> None:
    """
    Display a clear client-friendly success summary.
    """

    print()
    print("=" * 60)
    print("BRIGHTMART REPORTING AUTOMATION")
    print("=" * 60)
    print()
    print("REPORTING WORKFLOW COMPLETED SUCCESSFULLY")
    print()
    print(f"Rows processed: {rows_processed:,}")
    print("Dashboard files generated: " f"{dashboard_files_generated}")
    print("Execution time: " f"{total_execution_time:.2f} seconds")
    print("Summary report: " f"{summary_report_name}")

    if business_insights:
        print()
        print("KEY BUSINESS INSIGHTS")
        print("-" * 60)

        for insight in business_insights:
            print(f"- {insight}")

    print()
    print("=" * 60)
    print("STATUS: SUCCESS")
    print("=" * 60)


def display_failure_summary(
    total_execution_time: float,
    summary_report_name: str,
) -> None:
    """
    Display a clear client-friendly failure summary.
    """

    print()
    print("=" * 60)
    print("BRIGHTMART REPORTING AUTOMATION")
    print("=" * 60)
    print()
    print("THE REPORTING WORKFLOW COULD NOT BE COMPLETED")
    print()
    print("Execution stopped after " f"{total_execution_time:.2f} seconds.")
    print("Failure report: " f"{summary_report_name}")
    print()
    print("Please check the failure report and log file " "for additional details.")
    print()
    print("=" * 60)
    print("STATUS: FAILED")
    print("=" * 60)


def display_progress(
    step_number: int,
    total_steps: int,
    message: str,
) -> None:
    """
    Display the current reporting workflow step.
    """

    print(f"[{step_number}/{total_steps}] " f"{message}...")


def get_staged_output_files() -> list[Path]:
    """
    Return files generated during the current
    staging run.
    """

    if not STAGING_DATA_DIR.exists():
        return []

    return sorted(
        file_path for file_path in STAGING_DATA_DIR.iterdir() if file_path.is_file()
    )


def run_reporting_pipeline() -> None:
    """
    Run the complete BrightMart reporting workflow.

    The reporting workflow:
    1. Cleans and validates raw sales data.
    2. Creates the master sales dataset.
    3. Generates dashboard-ready KPI datasets.
    4. Reports the overall execution status.
    """

    start_time = time.perf_counter()

    logger.info("=" * 60)
    logger.info("BrightMart reporting automation started.")
    logger.info("=" * 60)

    pipeline_stats = PipelineStatistics()
    dashboard_files_generated = 0
    business_insights: list[str] = []

    try:
        total_steps = 5

        display_progress(
            1,
            total_steps,
            "Preparing the output environment",
        )

        prepare_staging_directory(STAGING_DATA_DIR)

        display_progress(
            2,
            total_steps,
            "Cleaning and validating sales data",
        )

        pipeline_stats = run_pipeline(
            display_summary=False,
            output_path=(STAGING_DATA_DIR / "master_sales.csv"),
        )

        display_progress(
            3,
            total_steps,
            "Generating dashboard datasets",
        )

        dashboard_output_files = run_dashboard_pipeline(
            input_path=(STAGING_DATA_DIR / "master_sales.csv"),
            output_dir=STAGING_DATA_DIR,
        )

        dashboard_files_generated = len(dashboard_output_files)

        generated_files = [
            STAGING_DATA_DIR / "master_sales.csv",
            *dashboard_output_files,
        ]

        verify_expected_outputs(
            generated_files=generated_files,
            expected_filenames=(EXPECTED_OUTPUT_FILENAMES),
        )

        display_progress(
            4,
            total_steps,
            "Generating business insights",
        )

        business_insights = generate_business_insights(data_dir=STAGING_DATA_DIR)

        published_files = publish_staged_outputs(
            staged_files=generated_files,
            final_directory=(PROCESSED_DATA_DIR),
        )

        display_progress(
            5,
            total_steps,
            "Creating pipeline summary report",
        )

        total_execution_time = round(
            time.perf_counter() - start_time,
            2,
        )

        report_content = build_summary_report(
            pipeline_stats=pipeline_stats,
            dashboard_files_generated=(dashboard_files_generated),
            total_execution_time=(total_execution_time),
            execution_status="SUCCESS",
            generated_files=published_files,
            business_insights=business_insights,
        )

        summary_report_path = save_summary_report(report_content)

        display_success_summary(
            rows_processed=(pipeline_stats.rows_after_cleaning),
            dashboard_files_generated=(dashboard_files_generated),
            total_execution_time=(total_execution_time),
            summary_report_name=(summary_report_path.name),
            business_insights=business_insights,
        )

        logger.info(
            "BrightMart reporting automation "
            "completed successfully in %.2f seconds.",
            total_execution_time,
        )

    except Exception as error:
        total_execution_time = round(
            time.perf_counter() - start_time,
            2,
        )

        pipeline_stats.execution_status = "FAILED"

        generated_files = get_staged_output_files()

        failure_report = build_summary_report(
            pipeline_stats=pipeline_stats,
            dashboard_files_generated=(dashboard_files_generated),
            total_execution_time=(total_execution_time),
            execution_status="FAILED",
            generated_files=generated_files,
            business_insights=business_insights,
            error_message=str(error),
        )

        summary_report_path = save_summary_report(failure_report)

        logger.exception(
            "BrightMart reporting automation failed " "after %.2f seconds.",
            total_execution_time,
        )

        display_failure_summary(
            total_execution_time=(total_execution_time),
            summary_report_name=(summary_report_path.name),
        )

        raise


if __name__ == "__main__":
    run_reporting_pipeline()
