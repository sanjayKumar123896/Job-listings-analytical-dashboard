# ============================================================
# DATA COLLECTION - JOB LISTINGS ANALYTICAL DASHBOARD
# ============================================================

# Import required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


# ============================================================
# JOB SCRAPER CLASS
# ============================================================

class JobScraper:

    def __init__(self, url):

        # Store main website URL
        self.url = url

        # Store job URLs
        self.job_urls = []

        # Store job titles
        self.job_titles = []

        # Store job information
        self.jobs = []

        # Create a requests session
        self.session = requests.Session()

        # Browser-like headers
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        })


    # ========================================================
    # CONNECT TO WEBSITE
    # ========================================================

    def connect_website(self):

        try:

            # Send request to main webpage
            response = self.session.get(
                self.url,
                timeout=10
            )

            # Check response
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            print("Website connected successfully.")

            return soup

        except requests.exceptions.RequestException as e:

            print(
                "Error connecting to website:",
                e
            )

            return None


    # ========================================================
    # GET JOB LINKS AND BASIC INFORMATION
    # ========================================================

    def get_job_links(self, soup):

        # Find all job cards
        job_cards = soup.find_all(
            "div",
            class_="card-content"
        )

        # Process each job card
        for card in job_cards:

            # ------------------------------------------------
            # JOB TITLE
            # ------------------------------------------------

            title_tag = card.find(
                "h2",
                class_="title"
            )

            if title_tag:

                job_title = title_tag.get_text(
                    strip=True
                )

            else:

                job_title = "Not Available"


            # Store title
            self.job_titles.append(
                job_title
            )


            # ------------------------------------------------
            # COMPANY NAME
            # ------------------------------------------------

            company_tag = card.find(
                "h3",
                class_="company"
            )

            if company_tag:

                company_name = company_tag.get_text(
                    strip=True
                )

            else:

                company_name = "Not Available"


            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            location_tag = card.find(
                "p",
                class_="location"
            )

            if location_tag:

                location = location_tag.get_text(
                    strip=True
                )

            else:

                location = "Not Available"


            # ------------------------------------------------
            # POSTED DATE
            # ------------------------------------------------

            date_tag = card.find(
                "time"
            )

            if date_tag:

                posted_date = date_tag.get_text(
                    strip=True
                )

            else:

                posted_date = "Not Available"


            # ------------------------------------------------
            # INDIVIDUAL JOB URL
            # ------------------------------------------------

            job_url = None

            # Find all links inside the job card
            links = card.find_all(
                "a",
                href=True
            )

            # Check every link
            for link in links:

                href = link.get("href")

                # We need the Apply link.
                # The Apply link contains /fake-jobs/jobs/
                if "/fake-jobs/jobs/" in href:

                    job_url = urljoin(
                        self.url,
                        href
                    )

                    break


            # If a valid job URL was found
            if job_url:

                self.job_urls.append(
                    job_url
                )

                # Store basic information temporarily
                self.jobs.append({

                    "job_title": job_title,

                    "company_name": company_name,

                    "location": location,

                    "posted_date": posted_date,

                    "job_description": "Not Available",

                    "job_url": job_url

                })


        # ----------------------------------------------------
        # DISPLAY TOTAL JOB LINKS
        # ----------------------------------------------------

        print(
            "Individual job links found:",
            len(self.job_urls)
        )


        # ----------------------------------------------------
        # DISPLAY FIRST 5 JOB URLS
        # ----------------------------------------------------

        print("\nFirst 5 job URLs:")

        for url in self.job_urls[:5]:

            print(url)


        # ----------------------------------------------------
        # DISPLAY INDIVIDUAL JOB TITLES
        # ----------------------------------------------------

        print("\nIndividual Job Titles:")

        for number, title in enumerate(
            self.job_titles,
            start=1
        ):

            print(
                f"{number}. {title}"
            )


    # ========================================================
    # SCRAPE JOB DESCRIPTIONS
    # ========================================================

    def scrape_job_details(self):

        print("\nStarting detailed scraping...")

        # Process every individual job URL
        for index, job_url in enumerate(
            self.job_urls,
            start=1
        ):

            print(
                f"Scraping job {index}/{len(self.job_urls)}"
            )

            try:

                # Request individual job page
                response = self.session.get(
                    job_url,
                    timeout=10
                )

                # Check response
                response.raise_for_status()

                # Parse webpage
                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )


                # ------------------------------------------------
                # FIND JOB DESCRIPTION
                # ------------------------------------------------

                description_parts = []


                # Get main page heading and text content
                # Individual job page contains the description
                main_content = soup.find(
                    "main"
                )

                if main_content:

                    # Get all paragraph text
                    paragraphs = main_content.find_all(
                        "p"
                    )

                    for paragraph in paragraphs:

                        text = paragraph.get_text(
                            " ",
                            strip=True
                        )

                        if text:

                            description_parts.append(
                                text
                            )


                # If main content was not found,
                # try all paragraphs
                if not description_parts:

                    paragraphs = soup.find_all(
                        "p"
                    )

                    for paragraph in paragraphs:

                        text = paragraph.get_text(
                            " ",
                            strip=True
                        )

                        if text:

                            description_parts.append(
                                text
                            )


                # Combine description text
                if description_parts:

                    job_description = " ".join(
                        description_parts
                    )

                else:

                    job_description = "Not Available"


                # ------------------------------------------------
                # UPDATE DESCRIPTION
                # ------------------------------------------------

                self.jobs[index - 1][
                    "job_description"
                ] = job_description


            except requests.exceptions.HTTPError as e:

                print(
                    f"Error scraping job {index}: {e}"
                )

            except requests.exceptions.RequestException as e:

                print(
                    f"Error scraping job {index}: {e}"
                )

            except Exception as e:

                print(
                    f"Unexpected error for job {index}: {e}"
                )


        # ----------------------------------------------------
        # SCRAPING COMPLETED
        # ----------------------------------------------------

        print(
            "\nDetailed scraping completed."
        )

        print(
            "Successfully collected:",
            len(self.jobs),
            "jobs"
        )


    # ========================================================
    # CREATE RAW DATASET
    # ========================================================

    def create_raw_dataset(self):

        # Convert list into DataFrame
        df = pd.DataFrame(
            self.jobs
        )


        # ----------------------------------------------------
        # SAVE DATASET
        # ----------------------------------------------------

        output_file = (
            "data/raw/job_listings_raw.csv"
        )

        df.to_csv(
            output_file,
            index=False
        )


        # ----------------------------------------------------
        # DISPLAY DATASET INFORMATION
        # ----------------------------------------------------

        print("\n")
        print(
            "=" * 45
        )

        print(
            "RAW DATASET CREATED SUCCESSFULLY"
        )

        print(
            "=" * 45
        )

        print(
            "Rows:",
            df.shape[0]
        )

        print(
            "Columns:",
            df.shape[1]
        )

        print(
            "File:",
            output_file
        )


        # ----------------------------------------------------
        # DISPLAY COLUMNS
        # ----------------------------------------------------

        print("\nColumns:")

        for column in df.columns:

            print(
                "-",
                column
            )


        # ----------------------------------------------------
        # DISPLAY FIRST 5 RECORDS
        # ----------------------------------------------------

        print("\nFirst 5 records:")

        print(
            df.head()
        )


        return df


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    # Main website URL
    url = (
        "https://realpython.github.io/fake-jobs/"
    )


    # Create scraper object
    scraper = JobScraper(
        url
    )


    # --------------------------------------------------------
    # CONNECT TO WEBSITE
    # --------------------------------------------------------

    soup = scraper.connect_website()


    # Stop if connection failed
    if soup is None:

        return


    # --------------------------------------------------------
    # GET JOB LINKS AND BASIC INFORMATION
    # --------------------------------------------------------

    scraper.get_job_links(
        soup
    )


    # --------------------------------------------------------
    # SCRAPE INDIVIDUAL JOB DESCRIPTIONS
    # --------------------------------------------------------

    scraper.scrape_job_details()


    # --------------------------------------------------------
    # CREATE RAW DATASET
    # --------------------------------------------------------

    scraper.create_raw_dataset()


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()