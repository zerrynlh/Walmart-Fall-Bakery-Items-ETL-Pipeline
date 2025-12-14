# **Seasonal Bakery ETL Pipeline**

## Overview

This project is an ETL pipeline that extracts seasonal bakery data from Walmart, transforms it into a structured format, and loads the cleaned data into a Snowflake database. This project leverages modern data engineering tools such as Apache Airflow for scheduling and orchestration, Snowflake as the target data warehouse, and Python libraries like Pandas and BeautifulSoup for data extraction and transformation.

Custom functions can be located in (`utils.py`), pipeline logic (`pipeline.py`), and the orchestration (`dags.py`) for Airflow.

---

## **Table of Contents**
- [Technologies Used](#technologies-used)
- [ETL Process](#etl-process)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Docker Setup](#docker-setup)

---

## **Technologies Used**
- Python**
- Apache Airflow
- Snowflake*
- Pandas
- BeautifulSoup
- Docker

---

## **ETL Process**
- **Data Extraction**: Scrapes seasonal bakery items using `BeautifulSoup` and parses JSON content from a Walmart web page
- **Data Cleaning and Transformation**: Utilizes custom functions to:
  - Convert prices from string format to floats
  - Strip out HTML tags (like `<li>`) using `regex`
  - Extract weights in ounces (OZ) from product descriptions
  - Standardize data, handling missing values and rename columns for consistency
- **Loading into Snowflake**: After transformation, the data is loaded into a Snowflake table using the `write_pandas` function
- **ETL Orchestration**: The ETL process is scheduled to run daily using Airflow
- **Testing**: Includes unit tests for key functions

---

## **Setup**

### **Prerequisites**
- Python 3.8+
- Docker
- Snowflake account (credentials will be stored in environment variables)
- Airflow installed (if not using Docker)

### **Install Dependencies**

First, clone the repository and install the necessary dependencies:

```
git clone https://github.com/your-username/seasonal-bakery-etl.git
cd seasonal-bakery-etl
```

# Create a virtual environment
```
python -m venv venv
source venv/bin/activate
```

# Install required Python libraries
```
pip install -r requirements.txt
```

### **Set Up Environment Variables**

Create a `.env` file in the root directory and add your Snowflake credentials:

```
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

## **Running the Project**

### **Option 1: Running Locally**

To manually run the ETL pipeline without Airflow:

```
python pipeline.py
```

This will scrape the bakery data, transform it, and load it into Snowflake.

### **Option 2: Running via Airflow**

1. Copy `dags.py` to your Airflow `dags/` directory.
2. Start the Airflow scheduler and web server:
```
   airflow scheduler
   airflow webserver
```
3. The pipeline will be scheduled to run daily, or you can trigger it manually through the Airflow UI.

## **Testing**

Unit tests for the utility functions are included in the `tests.py` file. To run the tests:

```
python -m unittest tests.py
```

The tests cover:
- HTML tag replacement in product descriptions
- Conversion of price strings to floats
- Extraction of weight (OZ) from product descriptions
- Transformation and cleaning logic for the entire dataset

## **Docker Setup**

This project includes a Dockerfile to containerize the ETL process. To build and run the Docker container:

1. **Build the Docker image**:
```
docker build -t bakery-etl .
```

2. **Run the Docker container**:
```
docker run --env-file .env bakery-etl
```
