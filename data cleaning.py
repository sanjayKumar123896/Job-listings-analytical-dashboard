import pandas as pd
from pathlib import Path


class JobDataCleaner:
    """
    Class responsible for cleaning and preprocessing
    the raw job listings dataset.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

    # ---------------------------------------------------------
    # 1. LOAD DATA
    # ---------------------------------------------------------

    def load_data(self):
        """Load the raw CSV dataset."""

        try:
            self.df = pd.read_csv(self.input_path)

            print("Raw dataset loaded successfully.")
            print(f"Rows: {self.df.shape[0]}")
            print(f"Columns: {self.df.shape[1]}")

        except FileNotFoundError:
            print(f"File not found: {self.input_path}")
            raise

    # ---------------------------------------------------------
    # 2. STANDARDIZE COLUMN NAMES
    # ---------------------------------------------------------

    def standardize_columns(self):
        """Standardize column names."""

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        print("\nColumn names standardized.")

    # ---------------------------------------------------------
    # 3. REMOVE DUPLICATES
    # ---------------------------------------------------------

    def remove_duplicates(self):
        """Remove duplicate job records."""

        before = len(self.df)

        self.df.drop_duplicates(
            subset=["job_url"],
            inplace=True
        )

        after = len(self.df)

        print(
            f"\nDuplicates removed: "
            f"{before - after}"
        )

    # ---------------------------------------------------------
    # 4. CLEAN TEXT COLUMNS
    # ---------------------------------------------------------

    def clean_text(self):
        """Clean text-based columns."""

        text_columns = [
            "job_title",
            "company_name",
            "location",
            "job_description"
        ]

        for column in text_columns:

            if column in self.df.columns:

                self.df[column] = (
                    self.df[column]
                    .fillna("")
                    .astype(str)
                    .str.replace(
                        r"\s+",
                        " ",
                        regex=True
                    )
                    .str.strip()
                )

        print("Text columns cleaned.")

    # ---------------------------------------------------------
    # 5. CLEAN DATE
    # ---------------------------------------------------------

    def clean_date(self):
        """Convert posted date into datetime."""

        if "posted_date" in self.df.columns:

            self.df["posted_date"] = pd.to_datetime(
                self.df["posted_date"],
                errors="coerce"
            )

            print("Posted date converted.")

    # ---------------------------------------------------------
    # 6. HANDLE MISSING VALUES
    # ---------------------------------------------------------

    def handle_missing_values(self):
        """Handle missing values appropriately."""

        # Text fields
        text_columns = [
            "job_title",
            "company_name",
            "location",
            "job_description"
        ]

        for column in text_columns:

            if column in self.df.columns:

                self.df[column] = (
                    self.df[column]
                    .fillna("Not Available")
                )

        print("Missing values handled.")

    # ---------------------------------------------------------
    # 7. VALIDATE URLS
    # ---------------------------------------------------------

    def validate_urls(self):
        """Remove records without job URLs."""

        if "job_url" in self.df.columns:

            before = len(self.df)

            self.df = self.df[
                self.df["job_url"].notna()
            ]

            self.df = self.df[
                self.df["job_url"].astype(str).str.strip() != ""
            ]

            after = len(self.df)

            print(
                f"Invalid URL records removed: "
                f"{before - after}"
            )

    # ---------------------------------------------------------
    # 8. RESET INDEX
    # ---------------------------------------------------------

    def reset_index(self):
        """Reset DataFrame index."""

        self.df.reset_index(
            drop=True,
            inplace=True
        )

    # ---------------------------------------------------------
    # 9. DISPLAY CLEANING REPORT
    # ---------------------------------------------------------

    def cleaning_report(self):
        """Display final dataset information."""

        print("\n================================")
        print("CLEANING REPORT")
        print("================================")

        print(
            f"Rows: {self.df.shape[0]}"
        )

        print(
            f"Columns: {self.df.shape[1]}"
        )

        print("\nMissing values:")

        print(
            self.df.isnull().sum()
        )

        print("\nData types:")

        print(
            self.df.dtypes
        )

    # ---------------------------------------------------------
    # 10. SAVE CLEANED DATASET
    # ---------------------------------------------------------

    def save_data(self):
        """Save cleaned dataset."""

        output_path = Path(
            self.output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.df.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        print(
            "\nCleaned dataset saved successfully!"
        )

        print(
            f"Location: {output_path}"
        )

    # ---------------------------------------------------------
    # 11. COMPLETE PIPELINE
    # ---------------------------------------------------------

    def run(self):
        """Run the complete cleaning pipeline."""

        self.load_data()

        self.standardize_columns()

        self.remove_duplicates()

        self.clean_text()

        self.clean_date()

        self.handle_missing_values()

        self.validate_urls()

        self.reset_index()

        self.cleaning_report()

        self.save_data()


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    input_file = (
        "data/raw/job_listings_raw.csv"
    )

    output_file = (
        "data/processed/job_listings_cleaned.csv"
    )

    cleaner = JobDataCleaner(
        input_file,
        output_file
    )

    cleaner.run()