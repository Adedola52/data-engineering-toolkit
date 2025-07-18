import pandas as pd
import numpy as np
import os 
import requests 
import logging
from sqlalchemy import create_engine

logging.basicConfig(filename='git.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def get_data(url):
    """
    Fetches JSON data from the specified URL and returns it as a pandas DataFrame.

    Parameters:
        url (str): The API endpoint or URL from which to fetch the data.

    Returns:
        DataFrame: A pandas DataFrame containing the normalized JSON response.

    Raises:
        Logs errors if HTTP, connection, timeout, or general request exceptions occur.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 

        response = data.json()
        normalize_response = pd.json_normalize(response)
        dataframe = pd.DataFrame(normalize_response)
        logging.info("Data fetched")

    except  requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Connection Error:{errc}")

    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")

    except requests.exceptions.RequestException as errr:
        logging.error(f"Something went wrong:{errr}")
    
    return dataframe


def clean_data(get_data):
    """
    Cleans the fetched data by removing duplicates, stripping whitespace, capitalizing names,
    standardizing gender values, formatting phone numbers, and handling null values.

    Parameters:
        get_data (DataFrame): Raw data to be cleaned.

    Returns:
        DataFrame: A cleaned pandas DataFrame ready for loading into the database.
    """
    if get_data.empty:
        return logging.info("Data is empty")
    else:
        try:

            # drops duplicate
            remove_duplicates = get_data.drop_duplicates()

            # strips object columns
            columns = remove_duplicates.columns
            for x in columns:
                if remove_duplicates[x].dtypes == 'object':
                    remove_duplicates[x] = remove_duplicates[x].str.strip()

            # capitalze firstname, middlename and lastname
            names = ["FistName", "MiddleName", "LastName"]
            for i in names:
                remove_duplicates[i] = remove_duplicates[i].str.capitalize()

            # standardize the gender column
            remove_duplicates["Gender"] = np.where(remove_duplicates["Gender"].str.contains("^m", case = False), "Male",
                                                   np.where(remove_duplicates["Gender"].str.contains("^f", case = False), "Female"),
                                                   "Unknown")
            
            # Change datatypes and concatenate the countrycode and phonenumber
            for i in ["PhoneNumber", "CountryCode"]:
                remove_duplicates[i] = remove_duplicates[i].astype("object")
            remove_duplicates["PhoneNumber"] = remove_duplicates['CountryCode'][:3] + remove_duplicates['PhoneNumber'][1:]
            

            # checkes for null values and drop rows with null values
            null_checks = remove_duplicates.isnull().sum()
            for key, counts in null_checks.items():
                if counts > 0:
                    remove_duplicates[key].dropna(inplace =True)
                    logging.info(f"{key} has {counts} null values and rows has been dropped")
                else:
                    logging.info(f"{key} has no null values")
            return remove_duplicates

        except Exception as e:
            logging.error(f"Error occured: {e}")


def load_to_database(cleaned_data) -> None:
    """
    Loads cleaned data into a SQL Server database table named 'cleaned_data'.

    Parameters:
        cleaned_data (DataFrame): The cleaned pandas DataFrame to load into the database.

    Returns:
        None
    """

    if cleaned_data.empty:
        logging.info("No data to load into the database")
        return

    try:
        DB_HOST = os.getenv("DB_HOST")
        DB_NAME = os.getenv("DB_NAME")

        engine = create_engine(
            f"mssql+pyodbc://{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        cleaned_data.to_sql(name="cleaned_data", con=engine, if_exists='replace', index=False)
        logging.info("Data loaded to database successfully.")

    except Exception as e:
        logging.error(f"Error occurred while connecting to DB or loading data: {e}")

    
if __name__ == "__main__":
    data = get_data("url")
    cleandata = clean_data(data)
    load_to_database(cleandata)


    

    