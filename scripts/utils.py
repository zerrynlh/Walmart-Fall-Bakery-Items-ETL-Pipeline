"""Custom functions"""
import re
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# View structure of dictionary
def print_dict_keys(d, indent=0):
    # Loop through dictionary items
    for key, value in d.items():
        # Print the current key with indentation
        print('  ' * indent + str(key))
        
        # If the value is another dictionary, recursively call this function
        if isinstance(value, dict):
            print_dict_keys(value, indent + 1)
        # If the value is a list, print the keys of list elements if they are dicts
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    print_dict_keys(item, indent + 1)

# Get data from website
def extract_data(url, headers):
    r = requests.get(url, headers=headers)

    # Check for successful response
    if r.status_code == 403:
        print("Access Forbidden. The server may be blocking requests.")
        return
    else:
        r = r.text

    soup = BeautifulSoup(r, 'html.parser')

    # Get JSON data from script tag
    script_tag = soup.find('script', id='__NEXT_DATA__')
    
    if script_tag:
        json_content = script_tag.string  # Get the content of the script tag
    
        json_data = json.loads(json_content)
    else:
        print("JSON data not found in the HTML.")
    try:
        json_fall = json_data['props']['pageProps']['initialData']['searchResult']['itemStacks'][0]['items']
    except KeyError as ke:
        logging.error(f'{ke} is not a recognized key.')
        return

    return json_fall

# Remove li tags from document
def replace_li(desc):
    # Ensure desc is a string before replacing
    if isinstance(desc, str):
        new_desc = desc.replace('<li>', '').replace('</li>', '')
        return new_desc.strip()
    else:
        return None

# Conver strings to floats
def safe_convert_price(price_str):
    try:
        return float(price_str.replace('$', '').replace(',', ''))
    except ValueError:
        return None

# Get OZ from item title
def extract_weight(description):
    # Use a regex to find weight in the format 'X OZ'
    if description:
        match = re.search(r'(\d+\.?\d*)\s*OZ', description, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None

# Transfrom JSON data
def transform_data(fall_data):
    prices = [item.get('priceInfo', {}).get('linePrice', 'Price not available') for item in fall_data]
    new_prices = [safe_convert_price(i) for i in prices]

    name = [item.get('name', None) for item in fall_data]

    short_desc = [item.get('shortDescription', None) for item in fall_data]
    new_desc = [replace_li(i) for i in short_desc]

    weights = [extract_weight(i) for i in new_desc]

    rating = [i.get('rating', {}).get('averageRating', None) for i in fall_data]

    reviews = [i.get('rating', {}).get('numberOfReviews', None) for i in fall_data]

    bakery_data = pd.DataFrame()

    bakery_data['Title'] = name
    bakery_data['Price'] = new_prices
    bakery_data['Description'] = new_desc
    bakery_data['Weight'] = weights
    bakery_data['Rating'] = rating
    bakery_data['NumReviews'] = reviews

    # Where number of reviews is Nan, replace with 0
    bakery_data['NumReviews'] = bakery_data['NumReviews'].fillna(0).astype('int64')

    # Where number of reviews is 0, set rating to None
    bakery_data.loc[bakery_data['NumReviews'] == 0, 'Rating'] = None

    # Drop items where the price or title is None
    bakery_data.dropna(subset=['Title', 'Price'], inplace=True)

    # Rename columns before insertion:
    bakery_data.rename(columns=lambda x: x.upper(), inplace=True)
    bakery_data.rename(columns={'NUMREVIEWS': 'NUM_REVIEWS'}, inplace=True)

    return bakery_data

# Load into Snowflake database
def load_data(fall_df, user, passw, account, warehouse, database, schema):
    # Establish connection
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=passw,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema,
            role='ACCOUNTADMIN'
        )
    
        if conn:
            cur = conn.cursor()
            
            #write_pandas(conn, fall_df, 'BAKERY_ITEMS')
            print("Data successfully loaded.")

        cur.close()
        conn.close()
       
    except Exception as e:
        print(f"Error: {e}")
    