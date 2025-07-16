import pandas as pd
import numpy as np
import os 
import requests 
import logging  

logging.basicConfig(filename='git.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def get_data(url):
    """

    """
    try:
        df = url
        data = requests.get(df)
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

        except Exception as e:
            logging.error(f"Error occured: {e}")
    
    

        

    

    