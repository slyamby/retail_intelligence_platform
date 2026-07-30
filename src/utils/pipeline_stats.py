class PipelineStatistics:
    """Store and display statistics from a pipeline execution."""

    def __init__(self):

        self.rows_loaded = 0

        self.rows_after_cleaning = 0

        self.duplicates_removed = 0

        self.invalid_quantities = 0

        self.invalid_dates = 0

        self.customer_names_filled = 0

        self.execution_time = 0

        self.execution_status = "NOT STARTED"

    def display(self):
        """Display the pipeline execution summary."""

        print()

        print("=" * 60)

        print("BRIGHTMART PIPELINE SUMMARY")

        print("=" * 60)

        print(f"Rows Loaded: {self.rows_loaded}")

        print(f"Rows After Cleaning: {self.rows_after_cleaning}")

        print(f"Duplicates Removed: {self.duplicates_removed}")

        print(f"Invalid Quantities: {self.invalid_quantities}")

        print(f"Invalid Dates: {self.invalid_dates}")

        print(f"Customer Names Filled: {self.customer_names_filled}")

        print(f"Execution Time: {self.execution_time} seconds")

        print(f"Execution Status: {self.execution_status}")

        print("=" * 60)
