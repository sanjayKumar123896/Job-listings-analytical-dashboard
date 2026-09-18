import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Job Listings Analytical Dashboard",
    page_icon="💼",
    layout="wide"
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    current_path = Path.cwd()

    for path in [current_path] + list(current_path.parents):

        data_path = (
            path
            / "data"
            / "processed"
            / "job_listings_processed.csv"
        )

        if data_path.exists():

            return pd.read_csv(data_path)

    return None


df = load_data()

# ============================================================
# ERROR HANDLING
# ============================================================

if df is None:

    st.error(
        "Processed dataset could not be found."
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("💼 Job Analytics")

st.sidebar.markdown(
    "### Navigation"
)

page = st.sidebar.radio(
    "Select Page",
    [
        "Home",
        "Dataset Viewer",
        "Summary Statistics",
        "Job Analysis",
        "Business Insights"
    ]
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.title(
        "💼 Job Listings Analytical Dashboard"
    )

    st.subheader(
        "Interactive Data Analysis of Job Listings"
    )

    st.markdown(
        """
        This dashboard demonstrates the complete data analytics
        workflow from **web scraping to business insight generation**.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Jobs",
            len(df)
        )

    with col2:

        st.metric(
            "Companies",
            df["company_name"].nunique()
        )

    with col3:

        st.metric(
            "Locations",
            df["location"].nunique()
        )

    with col4:

        st.metric(
            "Job Categories",
            df["job_category"].nunique()
        )

    st.divider()

    # --------------------------------------------------------
    # QUICK INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "📌 Quick Insights"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        top_category = (
            df["job_category"]
            .mode()[0]
        )

        st.info(
            f"**Top Job Category**\n\n"
            f"{top_category}"
        )

    with col2:

        top_experience = (
            df["experience_level"]
            .mode()[0]
        )

        st.info(
            f"**Most Common Experience Level**\n\n"
            f"{top_experience}"
        )

    with col3:

        top_location = (
            df["location"]
            .mode()[0]
        )

        st.info(
            f"**Most Common Location**\n\n"
            f"{top_location}"
        )

    st.divider()

    # --------------------------------------------------------
    # PROJECT OBJECTIVE
    # --------------------------------------------------------

    st.subheader(
        "🎯 Project Objective"
    )

    st.write(
        """
        The objective of this project is to collect job listing data
        through web scraping, clean and transform the data, perform
        exploratory data analysis, identify patterns, and present
        actionable insights through an interactive dashboard.
        """
    )

    # --------------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------------

    st.subheader(
        "🌐 Data Source"
    )

    st.write(
        "The dataset was collected from the Fake Python Jobs website "
        "for educational and web-scraping practice purposes."
    )

    st.caption(
        "The dataset contains 100 collected job listings."
    )

    # --------------------------------------------------------
    # DOWNLOAD COMPLETE DATASET
    # --------------------------------------------------------

    st.subheader(
        "📥 Download Processed Dataset"
    )

    full_csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Processed Dataset",
        data=full_csv,
        file_name="job_listings_processed.csv",
        mime="text/csv"
    )

    st.divider()

    st.caption(
        "⚠️ Note: This is a demonstration dataset and should not "
        "be interpreted as representative of the overall real-world "
        "job market."
    )


# ============================================================
# DATASET VIEWER
# ============================================================

elif page == "Dataset Viewer":

    st.title(
        "📋 Dataset Viewer"
    )

    st.write(
        f"Showing **{len(df)} records** and "
        f"**{len(df.columns)} columns**."
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

    st.divider()

    st.subheader(
        "Dataset Columns"
    )

    column_data = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": [
            str(df[column].dtype)
            for column in df.columns
        ]
    })

    st.dataframe(
        column_data,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SUMMARY STATISTICS
# ============================================================

elif page == "Summary Statistics":

    st.title(
        "📊 Summary Statistics"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Job Listings",
            len(df)
        )

    with col2:

        st.metric(
            "Companies",
            df["company_name"].nunique()
        )

    with col3:

        st.metric(
            "Locations",
            df["location"].nunique()
        )

    with col4:

        st.metric(
            "Categories",
            df["job_category"].nunique()
        )

    st.divider()

    st.subheader(
        "📈 Numerical Summary"
    )

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )

    st.subheader(
        "🔍 Missing Values"
    )

    missing = df.isnull().sum()

    missing = missing[
        missing > 0
    ]

    if len(missing) == 0:

        st.success(
            "No missing values found."
        )

    else:

        st.dataframe(
            missing.to_frame(
                "Missing Values"
            ),
            use_container_width=True
        )


# ============================================================
# JOB ANALYSIS
# ============================================================

elif page == "Job Analysis":

    st.title(
        "🔎 Interactive Job Analysis"
    )

    st.markdown(
        "Use the filters in the sidebar to explore the dataset."
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.sidebar.subheader(
        "🎛️ Filters"
    )

    categories = sorted(
        df["job_category"]
        .dropna()
        .unique()
    )

    selected_categories = st.sidebar.multiselect(
        "Job Category",
        categories,
        default=categories
    )

    experience_levels = sorted(
        df["experience_level"]
        .dropna()
        .unique()
    )

    selected_experience = st.sidebar.multiselect(
        "Experience Level",
        experience_levels,
        default=experience_levels
    )

    locations = sorted(
        df["location"]
        .dropna()
        .unique()
    )

    selected_locations = st.sidebar.multiselect(
        "Location",
        locations,
        default=locations
    )

    companies = sorted(
    df["company_name"]
    .dropna()
    .unique()
    )

    selected_companies = st.sidebar.multiselect(
    "Company Name",
    companies,
    default=companies
    )
    
    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    filtered_df = df[
        (df["job_category"].isin(
            selected_categories
        ))
        &
        (df["experience_level"].isin(
            selected_experience
        ))
        &
        (df["location"].isin(
            selected_locations
        ))
        &
        (df["company_name"].isin(
            selected_companies
        ))
       
    ]

    # --------------------------------------------------------
    # EMPTY FILTER HANDLING
    # --------------------------------------------------------

    if filtered_df.empty:

        st.warning(
            "⚠️ No job listings match the selected filters."
        )

        st.info(
            "Please select at least one value from each filter."
        )

        st.stop()

    # --------------------------------------------------------
    # FILTER SUMMARY
    # --------------------------------------------------------

    st.subheader(
        "📌 Filtered Results"
    )

    st.write(
        f"Showing **{len(filtered_df)}** out of "
        f"**{len(df)}** total job listings."
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Jobs",
            len(filtered_df)
        )

    with col2:

        st.metric(
            "Companies",
            filtered_df[
                "company_name"
            ].nunique()
        )

    with col3:

        st.metric(
            "Locations",
            filtered_df[
                "location"
            ].nunique()
        )

    with col4:

        avg_words = round(
            filtered_df[
                "description_word_count"
            ].mean()
        )

        st.metric(
            "Avg Description Words",
            avg_words
        )

    st.divider()

    # --------------------------------------------------------
    # CHART 1
    # --------------------------------------------------------

    st.subheader(
        "📊 Job Category Distribution"
    )

    category_counts = (
        filtered_df[
            "job_category"
        ]
        .value_counts()
    )

    fig1, ax1 = plt.subplots(
        figsize=(10, 5)
    )

    category_counts.plot(
        kind="bar",
        ax=ax1
    )

    ax1.set_xlabel(
        "Job Category"
    )

    ax1.set_ylabel(
        "Number of Jobs"
    )

    ax1.set_title(
        "Job Listings by Category"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig1)

    # --------------------------------------------------------
    # CHART 2
    # --------------------------------------------------------

    st.subheader(
        "📈 Experience Level Distribution"
    )

    experience_counts = (
        filtered_df[
            "experience_level"
        ]
        .value_counts()
    )

    fig2, ax2 = plt.subplots(
        figsize=(10, 5)
    )

    experience_counts.plot(
        kind="bar",
        ax=ax2
    )

    ax2.set_xlabel(
        "Experience Level"
    )

    ax2.set_ylabel(
        "Number of Jobs"
    )

    ax2.set_title(
        "Job Listings by Experience Level"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig2)

    # --------------------------------------------------------
    # CHART 3
    # --------------------------------------------------------

    st.subheader(
        "📍 Top Job Locations"
    )

    location_counts = (
        filtered_df[
            "location"
        ]
        .value_counts()
        .head(10)
    )

    fig3, ax3 = plt.subplots(
        figsize=(10, 5)
    )

    location_counts.plot(
        kind="bar",
        ax=ax3
    )

    ax3.set_xlabel(
        "Location"
    )

    ax3.set_ylabel(
        "Number of Jobs"
    )

    ax3.set_title(
        "Top 10 Job Locations"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig3)

    # --------------------------------------------------------
    # CHART 4 — SKILL DEMAND
    # --------------------------------------------------------

    st.subheader(
        "💻 Technical Skill Demand"
    )

    skill_columns = [
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

    available_skill_columns = [
        column
        for column in skill_columns
        if column in filtered_df.columns
    ]

    skill_counts = (
        filtered_df[
            available_skill_columns
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    skill_counts.index = (
        skill_counts.index
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

    fig4, ax4 = plt.subplots(
        figsize=(10, 5)
    )

    skill_counts.plot(
        kind="bar",
        ax=ax4
    )

    ax4.set_xlabel(
        "Skill"
    )

    ax4.set_ylabel(
        "Number of Jobs"
    )

    ax4.set_title(
        "Technical Skill Demand"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    st.pyplot(fig4)

    # ---------------------------------------------------------
    # CHART 5 — COMPANY DEMAND ANALYSIS
    # ---------------------------------------------------------

    st.subheader(
    "🏢 Company-wise Job Demand"
    )

   # Count job listings for each company
    company_counts = (
    filtered_df["company_name"]
    .value_counts()
    .head(10)
    .sort_values(ascending=True)
    )

    # Create chart
    fig5, ax5 = plt.subplots(
    figsize=(10, 6)
    )

    company_counts.plot(
    kind="barh",
    ax=ax5
    )

    # Axis labels
    ax5.set_xlabel(
    "Number of Jobs"
    )

    ax5.set_ylabel(
    "Company Name"
    )

    # Chart title
    ax5.set_title(
        "Top 10 Companies by Job Listings"
    )

    # Add value labels to bars
    for i, value in enumerate(company_counts):
        ax5.text(
        value + 0.05,
        i,
        str(value),
        va="center"
        )

    plt.tight_layout()

    # Display chart
    st.pyplot(fig5)

    # --------------------------------------------------------
    # DOWNLOAD FILTERED DATASET
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📥 Download Filtered Dataset"
    )

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=csv_data,
        file_name="filtered_job_listings.csv",
        mime="text/csv"
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.title(
        "💡 Business Insights"
    )

    st.markdown(
        "Key findings generated from the collected job listing dataset."
    )

    # --------------------------------------------------------
    # BASIC INSIGHTS
    # --------------------------------------------------------

    most_common_category = (
        df["job_category"]
        .mode()[0]
    )

    most_common_experience = (
        df["experience_level"]
        .mode()[0]
    )

    most_common_location = (
        df["location"]
        .mode()[0]
    )

    average_description = round(
        df["description_word_count"].mean(),
        2
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"📌 Most common job category: "
            f"**{most_common_category}**"
        )

        st.info(
            f"📌 Most common experience level: "
            f"**{most_common_experience}**"
        )

    with col2:

        st.warning(
            f"📌 Most frequently appearing location: "
            f"**{most_common_location}**"
        )

        st.success(
            f"📌 Average job description length: "
            f"**{average_description} words**"
        )

    st.divider()

    # --------------------------------------------------------
    # SKILL INSIGHTS
    # --------------------------------------------------------

    st.subheader(
        "💻 Technical Skill Insights"
    )

    skill_columns = [
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

    available_skill_columns = [
        column
        for column in skill_columns
        if column in df.columns
    ]

    skill_counts = (
        df[
            available_skill_columns
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    skill_percentage = (
        skill_counts
        / len(df)
        * 100
    )

    skill_table = pd.DataFrame({
        "Skill": [
            skill
            .replace("_required", "")
            .replace("_", " ")
            .title()
            for skill in skill_counts.index
        ],
        "Job Listings": skill_counts.values,
        "Percentage": skill_percentage.round(1).values
    })

    st.dataframe(
        skill_table,
        use_container_width=True,
        hide_index=True
    )

    top_skill = skill_table.iloc[0]["Skill"]

    st.info(
        f"📌 **{top_skill}** is the most frequently identified "
        f"technical skill in this collected dataset."
    )

    st.divider()

    # --------------------------------------------------------
    # LIMITATION
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Dataset Limitation"
    )

    st.write(
        """
        This analysis is based on the Fake Python Jobs demonstration dataset
        and this dashboard provides an analytical overview of job listings
        across various job categories, locations,company names,experience levels 
        attributes in the collected dataset.The findings describe patterns within 
        this collected dataset and should not be treated as a representation of the
        complete real-world job market.
        """
    )

    st.divider()

    st.subheader(
        "🚀 Future Improvements"
    )

    st.write(
        """
        • Collect a larger real-world job dataset

        • Expand the analysis to include all major job categories 
          for broader market insights.

        • Add salary analysis using an appropriate data source

        • Add remote, hybrid and onsite analysis using a suitable source

        • Add advanced machine learning models

        • Implement automated periodic data collection
        """
    )