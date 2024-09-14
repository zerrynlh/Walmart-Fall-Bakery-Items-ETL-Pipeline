# 🍰 **Seasonal Bakery ETL Pipeline** 🍰

## Overview

This project is an **ETL pipeline** that extracts seasonal bakery data from Walmart, transforms it into a structured format, and loads the cleaned data into a **Snowflake** database. This project leverages modern data engineering tools such as **Apache Airflow** for scheduling and orchestration, **Snowflake** as the target data warehouse, and Python libraries like **Pandas** and **BeautifulSoup** for data extraction and transformation.

The project is organized in a modular way, separating custom functions (`utils.py`), pipeline logic (`pipeline.py`), and the orchestration (`dags.py`) for Airflow. Tests have been written to ensure data integrity and correct transformation.

---

## **Table of Contents**
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup](#setup)
- [How It Works](#how-it-works)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Future Improvements](#future-improvements)

---

## **Technologies Used**
- **Python**: Core language for the ETL process.
- **Apache Airflow**: Orchestrates and schedules the ETL pipeline.
- **Snowflake**: Cloud data warehouse for storing the cleaned bakery data.
- **Pandas**: Data manipulation and transformation.
- **BeautifulSoup**: Web scraping to extract bakery items from a retail site.
- **Regex (re)**: Cleans and transforms textual data from the JSON response.
- **Docker**: Containerizes the application for easy deployment and consistent environments.

---

## **Features**
- **Data Extraction**: Scrapes seasonal bakery items using `BeautifulSoup` and parses JSON content from a Walmart web page.
- **Data Cleaning and Transformation**: Utilizes custom functions to:
  - Convert prices from string format to floats.
  - Strip out HTML tags (like `<li>`) using `regex`.
  - Extract weights in ounces (OZ) from product descriptions.
  - Standardize data, handling missing values and renaming columns for consistency.
- **Loading into Snowflake**: After transformation, the data is loaded into a Snowflake table using the `write_pandas` function.
- **ETL Orchestration**: The ETL process is scheduled to run daily using **Apache Airflow**.
- **Testing**: Includes unit tests for key functions to ensure robustness and accuracy.

---

## **Setup**

### **Prerequisites**
- Python 3.8+
- Docker
- Snowflake account (credentials will be stored in environment variables)
- Airflow installed (if not using Docker)

### **Install Dependencies**

First, clone the repository and install the necessary dependencies:

\`\`\`bash
git clone https://github.com/your-username/seasonal-bakery-etl.git
cd seasonal-bakery-etl

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install required Python libraries
pip install -r requirements.txt
\`\`\`

### **Set Up Environment Variables**

Create a `.env` file in the root directory and add your Snowflake credentials:

\`\`\`
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
\`\`\`

---

## **How It Works**

1. **Extract**:
   - Uses the `requests` library to retrieve HTML content from a Walmart seasonal bakery section.
   - Parses the HTML using `BeautifulSoup` to extract embedded JSON containing product details.
   
2. **Transform**:
   - Cleans the product descriptions by removing HTML tags using regex.
   - Converts prices from strings to numerical values.
   - Extracts weight (OZ) from product descriptions.
   - Handles missing values and ensures consistent column naming for database loading.

3. **Load**:
   - Establishes a connection to Snowflake using the `snowflake-connector-python` library.
   - Inserts the cleaned data into the `BAKERY_ITEMS` table in Snowflake.

4. **Airflow Orchestration**:
   - A DAG (`dags.py`) defines the scheduling logic to run the pipeline daily.
   - The `PythonOperator` in Airflow triggers the ETL pipeline.

---

## **Running the Project**

### **Option 1: Running Locally**

To manually run the ETL pipeline without Airflow:

\`\`\`bash
python pipeline.py
\`\`\`

This will scrape the bakery data, transform it, and load it into Snowflake.

### **Option 2: Running via Airflow**

If Airflow is set up locally:

1. Copy `dags.py` to your Airflow `dags/` directory.
2. Start the Airflow scheduler and web server:
   \`\`\`bash
   airflow scheduler
   airflow webserver
   \`\`\`
3. The pipeline will be scheduled to run daily, or you can trigger it manually through the Airflow UI.

---

## *Testing**

Unit tests for the utility functions are included in the `tests.py` file. To run the tests:

\`\`\`bash
python -m unittest tests.py
\`\`\`

The tests cover:
- HTML tag replacement in product descriptions.
- Conversion of price strings to floats.
- Extraction of weight (OZ) from product descriptions.
- Transformation and cleaning logic for the entire dataset.

---

## **Docker Setup**

### **Dockerizing the Application**

This project includes a Dockerfile to containerize the ETL process. To build and run the Docker container:

1. **Build the Docker image**:
   \`\`\`bash
   docker build -t bakery-etl .
   \`\`\`

2. **Run the Docker container**:
   \`\`\`bash
   docker run --env-file .env bakery-etl
   \`\`\`

This will execute the ETL pipeline inside a Docker container.
