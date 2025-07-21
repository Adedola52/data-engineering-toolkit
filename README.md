# Data Engineering Toolkit

A modular data engineering project that automates the process of cleaning, transforming, and exporting transaction data from raw format to a SQL Server database and finally to a CSV file. Ideal for pipeline practice and real-world simulation.

## Purpose
The purpose of this project is to demonstrate a practical and modular approach to handling end-to-end data workflows. It covers:

- Data cleaning (removing duplicates, nulls, trimming text, etc.)
- Data transformation (calculating new columns, formatting types, etc.)
- Data loading to SQL Server and exporting final data to a .csv file

## Contribution Guide
If you’d like to contribute:
- Fork the repository
- Create a new branch (git checkout -b feature/your-feature)
- Make your changes
- Commit and push (git commit -m "your message" && git push origin)

## How to Run - Setting up your environment
1. Clone this repo
```
git clone https://github.com/Adedola52/data-engineering-toolkit
```

2. Change directory to the cloned directory
```
cd data-engineering-toolkit
```
3. Set up environment variables
```
DB_NAME - your database name
DB_HOST - your Sql server 
```


5. Run the pipeline step-by-step
   
Execute each stage in order:
```
python data_cleaning.py -  Cleans raw data and sends to SQL
python transformation.py - Transforms data and updates SQL table
python data_loading.py   - Loads transformed data from SQL and saves to CSV
```

5. Check output
- Cleaned and transformed data is saved in your SQL Server database
- Final result is exported as Transaction_data.csv in the current folder

