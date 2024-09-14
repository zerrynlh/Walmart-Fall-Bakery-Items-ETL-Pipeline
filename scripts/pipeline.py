import os
import requests
import json
import re
from bs4 import BeautifulSoup
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from .utils import extract_data, transform_data, load_data

url = 'https://www.walmart.com/browse/food/seasonal-bakery/976759_976779_7443156_4622028?povid=976759_ItemCarousel_4302028_Fallbakerytreats_ViewAll_Rweb_Sept_05'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

# Retrieve connection info from environment variables for loading into database
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
account = os.getenv('SNOWFLAKE_ACCOUNT')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')

def etl_func():
    df1 = extract_data(url, headers)
    df2 = transform_data(df1)
    load_data(df2, user, password, account, warehouse, database, schema)
    print(df2.head())