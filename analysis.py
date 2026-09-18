import pandas as pd
import numpy as np
from pathlib import Path


class JobAnalysis:
    """
    Performs statistical analysis and exploratory
    analysis on the processed job listings dataset.
    """

    def __init__(self):

        # -----------------------------------------------------
        # Find project root automatically
        # -----------------------------------------------------

        current_path = Path(__file__).resolve()

        self.project_root = None

        for parent in current_path.parents:

            data_folder = parent / "data"

            if data_folder.exists():

                self.project_root = parent
                break

        if self.project_root is None:

            raise FileNotFoundError(
                "Could not locate the project data folder."
            )

        # -----------------------------------------------------
        # Dataset path
        # -----------------------------------------------------

        self.input_path = (
            self.project_root
            / "data"
            / "processed"
            / "job_listings_processed.csv"
        )

        self.df = None

    # =========================================================
    # LOAD DATA
    # =========================================================

    def load_data(self):

        print("\nLoading processed dataset...")

        if not self.input_path.exists():

            raise FileNotFoundError(
                f"\nProcessed dataset not found:\n"
                f"{self.input_path}\n\n"
                f"Please run feature_engineering.py first."
            )

        self.df = pd.read_csv(
            self.input_path
        )

        print("Dataset loaded successfully.")
        print(
            f"Rows: {self.df.shape[0]}"
        )
        print(
            f"Columns: {self.df.shape[1]}"
        )

    # =========================================================
    # DATASET OVERVIEW
    # =========================================================

    def dataset_overview(self):

        print("\n" + "=" * 60)
        print("1. DATASET OVERVIEW")
        print("=" * 60)

        print(
            f"\nDataset shape: "
            f"{self.df.shape}"
        )

        print("\nColumns:")

        for column in self.df.columns:

            print(
                f"- {column}"
            )

        print("\nData Types:")

        print(
            self.df.dtypes
        )

    # =========================================================
    # MISSING VALUES
    # =========================================================

    def missing_value_analysis(self):

        print("\n" + "=" * 60)
        print("2. MISSING VALUE ANALYSIS")
        print("=" * 60)

        missing = (
            self.df.isnull()
            .sum()
        )

        missing = missing[
            missing > 0
        ]

        if missing.empty:

            print(
                "No missing values found."
            )

        else:

            print(missing)

    # =========================================================
    # DESCRIPTIVE STATISTICS
    # =========================================================

    def descriptive_statistics(self):

        print("\n" + "=" * 60)
        print("3. DESCRIPTIVE STATISTICS")
        print("=" * 60)

        numeric_columns = (
            self.df.select_dtypes(
                include=np.number
            ).columns
        )

        if len(numeric_columns) == 0:

            print(
                "No numerical columns available."
            )

            return

        statistics = (
            self.df[
                numeric_columns
            ]
            .describe()
            .T
        )

        statistics["median"] = (
            self.df[
                numeric_columns
            ]
            .median()
        )

        print(
            statistics.round(2)
        )

    # =========================================================
    # JOB CATEGORY ANALYSIS
    # =========================================================

    def category_analysis(self):

        print("\n" + "=" * 60)
        print("4. JOB CATEGORY ANALYSIS")
        print("=" * 60)

        if "job_category" not in self.df.columns:

            print(
                "job_category column not found."
            )

            return

        result = (
            self.df[
                "job_category"
            ]
            .value_counts()
        )

        print(result)

    # =========================================================
    # EXPERIENCE LEVEL ANALYSIS
    # =========================================================

    def experience_analysis(self):

        print("\n" + "=" * 60)
        print("5. EXPERIENCE LEVEL ANALYSIS")
        print("=" * 60)

        if "experience_level" not in self.df.columns:

            print(
                "experience_level column not found."
            )

            return

        result = (
            self.df[
                "experience_level"
            ]
            .value_counts()
        )

        print(result)

    # =========================================================
    # LOCATION ANALYSIS
    # =========================================================

    def location_analysis(self):

        print("\n" + "=" * 60)
        print("6. TOP JOB LOCATIONS")
        print("=" * 60)

        if "location" not in self.df.columns:

            print(
                "location column not found."
            )

            return

        result = (
            self.df[
                "location"
            ]
            .value_counts()
            .head(15)
        )

        print(result)

    # =========================================================
    # COMPANY ANALYSIS
    # =========================================================

    def company_analysis(self):

        print("\n" + "=" * 60)
        print("7. TOP HIRING COMPANIES")
        print("=" * 60)

        if "company_name" not in self.df.columns:

            print(
                "company_name column not found."
            )

            return

        result = (
            self.df[
                "company_name"
            ]
            .value_counts()
            .head(15)
        )

        print(result)

    # =========================================================
    # SKILL ANALYSIS
    # =========================================================

    def skill_analysis(self):

        print("\n" + "=" * 60)
        print("8. SKILL DEMAND ANALYSIS")
        print("=" * 60)

        skills = [
            "python_required",
            "sql_required",
            "machine_learning_required",
            "ai_required",
            "aws_required",
            "java_required",
            "javascript_required",
            "docker_required",
            "cloud_required"
        ]

        available_skills = [
            skill
            for skill in skills
            if skill in self.df.columns
        ]

        if not available_skills:

            print(
                "No skill columns found."
            )

            return

        result = (
            self.df[
                available_skills
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        result.index = (
            result.index
            .str.replace(
                "_required",
                "",
                regex=False
            )
            .str.replace(
                "_",
                " ",
                regex=False
            )
            .str.title()
        )

        print(result)

    # =========================================================
    # DESCRIPTION ANALYSIS
    # =========================================================

    def description_analysis(self):

        print("\n" + "=" * 60)
        print("9. JOB DESCRIPTION ANALYSIS")
        print("=" * 60)

        column = "description_word_count"

        if column not in self.df.columns:

            print(
                "description_word_count "
                "column not found."
            )

            return

        values = (
            self.df[column]
        )

        print(
            f"Average words: "
            f"{values.mean():.2f}"
        )

        print(
            f"Median words: "
            f"{values.median():.2f}"
        )

        print(
            f"Minimum words: "
            f"{values.min()}"
        )

        print(
            f"Maximum words: "
            f"{values.max()}"
        )

    # =========================================================
    # CORRELATION ANALYSIS
    # =========================================================

    def correlation_analysis(self):

        print("\n" + "=" * 60)
        print("10. CORRELATION ANALYSIS")
        print("=" * 60)

        numeric_df = (
            self.df.select_dtypes(
                include=np.number
            )
        )

        if numeric_df.shape[1] < 2:

            print(
                "Not enough numerical columns."
            )

            return

        correlation = (
            numeric_df.corr()
        )

        print(
            correlation.round(2)
        )

    # =========================================================
    # BUSINESS INSIGHTS
    # =========================================================

    def generate_business_insights(self):

        print("\n" + "=" * 60)
        print("11. BUSINESS INSIGHTS")
        print("=" * 60)

        # -----------------------------------------------------
        # Most common job category
        # -----------------------------------------------------

        if "job_category" in self.df.columns:

            categories = (
                self.df[
                    "job_category"
                ]
                .value_counts()
            )

            if not categories.empty:

                print(
                    f"\nMost common job category:"
                    f" {categories.index[0]}"
                )

                print(
                    f"Number of jobs:"
                    f" {categories.iloc[0]}"
                )

        # -----------------------------------------------------
        # Most common experience level
        # -----------------------------------------------------

        if "experience_level" in self.df.columns:

            experience = (
                self.df[
                    "experience_level"
                ]
                .value_counts()
            )

            if not experience.empty:

                print(
                    f"\nMost common experience level:"
                    f" {experience.index[0]}"
                )

                print(
                    f"Number of jobs:"
                    f" {experience.iloc[0]}"
                )

        # -----------------------------------------------------
        # Most common location
        # -----------------------------------------------------

        if "location" in self.df.columns:

            locations = (
                self.df[
                    "location"
                ]
                .value_counts()
            )

            if not locations.empty:

                print(
                    f"\nMost common location:"
                    f" {locations.index[0]}"
                )

        # -----------------------------------------------------
        # Python demand
        # -----------------------------------------------------

        if "python_required" in self.df.columns:

            python_jobs = int(
                self.df[
                    "python_required"
                ].sum()
            )

            percentage = (
                python_jobs
                / len(self.df)
                * 100
            )

            print(
                f"\nJobs mentioning Python:"
                f" {python_jobs}"
                f" ({percentage:.1f}%)"
            )

        # -----------------------------------------------------
        # SQL demand
        # -----------------------------------------------------

        if "sql_required" in self.df.columns:

            sql_jobs = int(
                self.df[
                    "sql_required"
                ].sum()
            )

            percentage = (
                sql_jobs
                / len(self.df)
                * 100
            )

            print(
                f"Jobs mentioning SQL:"
                f" {sql_jobs}"
                f" ({percentage:.1f}%)"
            )

    # =========================================================
    # COMPLETE PIPELINE
    # =========================================================

    def run(self):

        self.load_data()

        self.dataset_overview()

        self.missing_value_analysis()

        self.descriptive_statistics()

        self.category_analysis()

        self.experience_analysis()

        self.location_analysis()

        self.company_analysis()

        self.skill_analysis()

        self.description_analysis()

        self.correlation_analysis()

        self.generate_business_insights()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    analysis = JobAnalysis()

    analysis.run()