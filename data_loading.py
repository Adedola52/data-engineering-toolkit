import pandas as pd 
import numpy as np 
from sqlalchemy import create_engine 
import os 
import logging 

logging.basicConfig(filename='budgetanalyzer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

def load_data(transformed_data):
    """
    Loads transformed data from the database.

    Reads data from the 'transformed_data' table in the connected SQL Server database
    and returns it as a pandas DataFrame.

    Returns:
        DataFrame: The queried data as a pandas DataFrame. 
    """

    try:
        db_host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_Name")

        engine = create_engine(f"mssql+pyodbc://{db_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        query = "SELECT * FROM transformed_data"
        data_load = pd.read_sql(query, con = engine)
        
        return data_load
    
    except Exception as e:
        logging.error(f"Error retrieving data from database: {e}")


def send_to_file(data_load):
    """
    Saves the loaded data to a CSV file.

    Parameters:
        data_load (DataFrame): A pandas DataFrame containing the data to be saved.

    Returns:
        None

    Notes:
        The data will be saved as 'Transaction_data.csv' in the current working directory.
    """

    try:
        data_load.to_csv("Transaction_data.csv", index = False)
    
    except Exception as e:
        logging.error(f"Error sending data to file: {e}")



if __name__ == "__main__":
    load_ = load_data()
    send_to_file(load_)
