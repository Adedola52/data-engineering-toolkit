import pandas as pd 
import numpy as np
import os 
from sqlalchemy import create_engine 
import logging 

logging.basicConfig(filename='Api.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')


def query_database():
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    
    try:
        engine = create_engine(
            f"mssql+pyodbc://{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")
        query = "SELECT * FROM "
        df = pd.read_sql(query, con = engine)
        logging.info("Read data from database successfully")

    except Exception as e:
        logging.error(f"Error reading data from database: {e}")



def transform_data(df):
    transform = df
    transform["TransactionType"] = transform["Amount"].where(transform["Amount"]<0, "Debit", "Credit")
    transform["TransactionYear"] = transform["TransactionDate"].dt.year.astype("Int64")

    conditions = [
    transform["Amount"].between(-500000, -50001),
    transform["Amount"].between(-50000, -1),
    transform["Amount"].between(0, 50000),
    transform["Amount"].between(50001, 500000)]
    choices = [
    "High Debit Transaction",
    "Medium Debit Transaction",
    "Low Credit Transaction",
    "Medium Credit Transaction"
]

    transform["AmountCategory"] = np.select(conditions, choices, default="High Credit Transaction")




def load_to_db(data):
    """
      Connects to a SQL Server database using credentials stored in environment variables.
      Uses the ODBC driver to establish the connection and exports the cleaned country data
      to specified database

    """

    try:
        transformed_data = data

        DB_HOST = os.getenv("DB_HOST") 
        DB_NAME = os.getenv("DB_NAME")

         
        engine = create_engine(f"mssql+pyodbc://{DB_HOST}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

        transformed_data.to_sql(name='country_data', con=engine ,if_exists='replace', index=False)
        logging.info("Transformed data exported to database successfully")

    except Exception as e:
        logging.error(f'An error occurred sending transformed data to db: {e}')


    