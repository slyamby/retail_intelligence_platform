import time
from pathlib import Path

from config.settings import MASTER_DATASET, RAW_DATA_DIR
from src.data.clean_data import (clean_branch_names, clean_dates,
                                 clean_payment_methods, clean_product_names,
                                 clean_quantities, clean_unit_prices,
                                 handle_missing_values, load_data,
                                 rejected_records, remove_duplicate_rows,
                                 save_clean_data)
from src.data.validate import validate_sales_data
from src.utils.logger import logger
from src.utils.pipeline_stats import PipelineStatistics
from src.validation.input_validator import validate_raw_input_files


def run_pipeline(
    display_summary: bool = True,
    output_path: Path = MASTER_DATASET,
) -> PipelineStatistics:
    """
    Run the complete BrightMart data-cleaning pipeline.

    Parameters
    ----------
    display_summary:
        Whether to display pipeline statistics in the terminal.

    output_path:
        Location where the cleaned master dataset will be saved.

    Returns
    -------
    PipelineStatistics
        Statistics describing the cleaning pipeline execution.
    """

    stats = PipelineStatistics()
    start_time = time.perf_counter()

    logger.info("BrightMart data-cleaning pipeline started.")

    try:
        # Validate input files before loading them.
        validated_files = validate_raw_input_files(RAW_DATA_DIR)

        # Load all validated files.
        data = load_data(validated_files)

        stats.rows_loaded = len(data)

        missing_customer_names_before = data["customer_name"].isna().sum()

        rows_before_duplicates = len(data)

        # Standardise categorical values.
        data = clean_branch_names(data)
        data = clean_product_names(data)
        data = clean_payment_methods(data)

        # Convert dates and numeric values.
        data = clean_dates(data)
        data = clean_unit_prices(data)
        data = clean_quantities(data)

        # Capture invalid records after type conversion
        # but before invalid rows are removed or repaired.
        rejected = rejected_records(data)

        # Handle permitted missing values.
        data = handle_missing_values(data)

        # Remove duplicates.
        data = remove_duplicate_rows(data)

        stats.duplicates_removed = rows_before_duplicates - len(data)

        stats.customer_names_filled = int(missing_customer_names_before)

        stats.rows_after_cleaning = len(data)

        # Validate the final cleaned dataset.
        validation_issues = validate_sales_data(data)

        stats.invalid_quantities = validation_issues["invalid_quantities"]

        stats.invalid_dates = validation_issues["missing_dates"]

        # Save to the path supplied by the caller.
        save_clean_data(
            data=data,
            output_path=output_path,
        )

        # Save the rejected records here if the function
        # does not already save them.
        if not rejected.empty:
            logger.warning(
                "%s records were rejected.",
                len(rejected),
            )

        stats.execution_status = "SUCCESS"

        logger.info("BrightMart data-cleaning pipeline " "completed successfully.")

    except Exception:
        stats.execution_status = "FAILED"

        logger.exception("BrightMart data-cleaning pipeline failed.")

        raise

    finally:
        stats.execution_time = round(
            time.perf_counter() - start_time,
            2,
        )

        if display_summary:
            stats.display()

    return stats


if __name__ == "__main__":
    run_pipeline()
