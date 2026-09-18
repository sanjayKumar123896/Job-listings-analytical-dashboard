import pandas as pd
from pathlib import Path


class JobFeatureEngineer:
    """
    Feature engineering for the job listings dataset.
    """

    def __init__(self):
        # Project root:
        # project/
        # └── venv/
        #     └── src/
        #         └── feature_engineering.py

        self.project_root = Path(__file__).resolve().parents[2]

        self.input_path = (
            self.project_root
            / "data"
            / "processed"
            / "job_listings_cleaned.csv"
        )

        self.output_path = (
            self.project_root
            / "data"
            / "processed"
            / "job_listings_processed.csv"
        )

        self.df = None

    # ---------------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------------

    def load_data(self):
        """Load cleaned dataset."""

        if not self.input_path.exists():

            raise FileNotFoundError(
                f"\nCleaned dataset not found:\n"
                f"{self.input_path}\n\n"
                f"Please make sure data_cleaning.py "
                f"has been executed successfully."
            )

        self.df = pd.read_csv(
            self.input_path
        )

        print("Cleaned dataset loaded successfully.")
        print(f"Rows: {self.df.shape[0]}")
        print(f"Columns: {self.df.shape[1]}")

    # ---------------------------------------------------------
    # JOB CATEGORY
    # ---------------------------------------------------------

    def create_job_category(self):
        """Create job category from title and description."""

        def categorize(row):

            text = (
                str(row.get("job_title", ""))
                + " "
                + str(row.get("job_description", ""))
            ).lower()

            if any(
                word in text
                for word in [
                    "data scientist",
                    "data analyst",
                    "data engineer",
                    "machine learning",
                    "analytics"
                ]
            ):
                return "Data & Analytics"

            if any(
                word in text
                for word in [
                    "software developer",
                    "software engineer",
                    "developer",
                    "programmer",
                    "python",
                    "java",
                    "frontend",
                    "backend",
                    "full stack"
                ]
            ):
                return "Software Development"

            if any(
                word in text
                for word in [
                    "marketing",
                    "seo",
                    "social media",
                    "content"
                ]
            ):
                return "Marketing"

            if any(
                word in text
                for word in [
                    "sales",
                    "business development",
                    "account executive"
                ]
            ):
                return "Sales & Business"

            if any(
                word in text
                for word in [
                    "designer",
                    "design",
                    "ux",
                    "ui"
                ]
            ):
                return "Design"

            if any(
                word in text
                for word in [
                    "finance",
                    "accountant",
                    "accounting"
                ]
            ):
                return "Finance"

            if any(
                word in text
                for word in [
                    "manager",
                    "management",
                    "operations"
                ]
            ):
                return "Management & Operations"

            if any(
                word in text
                for word in [
                    "human resources",
                    "recruiter",
                    "hr "
                ]
            ):
                return "Human Resources"

            if any(
                word in text
                for word in [
                    "health",
                    "medical",
                    "nurse"
                ]
            ):
                return "Healthcare"

            return "Other"

        self.df["job_category"] = self.df.apply(
            categorize,
            axis=1
        )

        print("✓ Job category created.")

    # ---------------------------------------------------------
    # EXPERIENCE LEVEL
    # ---------------------------------------------------------

    def create_experience_level(self):
        """Create experience level from job information."""

        def detect_level(row):

            text = (
                str(row.get("job_title", ""))
                + " "
                + str(row.get("job_description", ""))
            ).lower()

            if any(
                word in text
                for word in [
                    "chief",
                    "director",
                    "vice president",
                    " vp ",
                    "executive"
                ]
            ):
                return "Executive"

            if any(
                word in text
                for word in [
                    "senior",
                    "sr.",
                    "lead",
                    "principal"
                ]
            ):
                return "Senior"

            if any(
                word in text
                for word in [
                    "junior",
                    "jr.",
                    "associate"
                ]
            ):
                return "Junior"

            if any(
                word in text
                for word in [
                    "intern",
                    "internship",
                    "trainee",
                    "entry level",
                    "entry-level",
                    "graduate"
                ]
            ):
                return "Entry Level"

            return "Mid Level / Unspecified"

        self.df["experience_level"] = self.df.apply(
            detect_level,
            axis=1
        )

        print("✓ Experience level created.")

    # ---------------------------------------------------------
    # DESCRIPTION WORD COUNT
    # ---------------------------------------------------------

    def create_description_word_count(self):
        """Calculate number of words in job descriptions."""

        self.df["description_word_count"] = (
            self.df["job_description"]
            .fillna("")
            .astype(str)
            .apply(
                lambda text: len(text.split())
            )
        )

        print("✓ Description word count created.")

    # ---------------------------------------------------------
    # DESCRIPTION CHARACTER COUNT
    # ---------------------------------------------------------

    def create_description_character_count(self):
        """Calculate description length."""

        self.df["description_character_count"] = (
            self.df["job_description"]
            .fillna("")
            .astype(str)
            .str.len()
        )

        print("✓ Description character count created.")

    # ---------------------------------------------------------
    # SKILL FEATURES
    # ---------------------------------------------------------

    def create_skill_features(self):
        """Create binary skill indicators."""

        text = (
            self.df["job_title"].fillna("").astype(str)
            + " "
            + self.df["job_description"].fillna("").astype(str)
        ).str.lower()

        skills = {
            "python_required": ["python"],
            "sql_required": ["sql"],
            "machine_learning_required": [
                "machine learning",
                "machine-learning"
            ],
            "ai_required": [
                "artificial intelligence",
                " ai "
            ],
            "aws_required": [
                "aws",
                "amazon web services"
            ],
            "java_required": ["java"],
            "javascript_required": ["javascript"],
            "docker_required": ["docker"],
            "cloud_required": [
                "cloud computing",
                "cloud"
            ]
        }

        for column, keywords in skills.items():

            self.df[column] = text.apply(
                lambda value: int(
                    any(
                        keyword in value
                        for keyword in keywords
                    )
                )
            )

        print("✓ Skill features created.")

    # ---------------------------------------------------------
    # SAVE DATA
    # ---------------------------------------------------------

    def save_data(self):
        """Save feature-engineered dataset."""

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.df.to_csv(
            self.output_path,
            index=False,
            encoding="utf-8"
        )

        print("\n========================================")
        print("FEATURE ENGINEERING COMPLETED")
        print("========================================")
        print(f"Rows: {self.df.shape[0]}")
        print(f"Columns: {self.df.shape[1]}")
        print(
            f"Saved to:\n{self.output_path}"
        )

    # ---------------------------------------------------------
    # RUN PIPELINE
    # ---------------------------------------------------------

    def run(self):

        self.load_data()

        self.create_job_category()

        self.create_experience_level()

        self.create_description_word_count()

        self.create_description_character_count()

        self.create_skill_features()

        self.save_data()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    engineer = JobFeatureEngineer()

    engineer.run()