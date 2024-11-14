import pandas as pd
from database import engine, Base, SessionLocal
from data_generator import augment_data
from loguru import logger
import os

# Define paths
BASE_CSV_PATH = "WHeel Data Final.csv"  # Replace with your base CSV file path
AUGMENTED_CSV_PATH = "augmented_car_sales_data_v4.csv"
TABLE_NAME = "car_sales"

# Function to load the augmented data to the database
def load_to_database(df, table_name, engine):
    """
    Load a DataFrame into the specified database table.
    """
    logger.info(f"Loading data into the database table: {table_name}")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logger.info(f"Data successfully loaded into {table_name}")

# ETL Process
def etl_process():
    """
    End-to-end ETL process: augment data, save to CSV, and load to database.
    """
    # Step 1: Augment the base CSV data with new columns
    logger.info("Starting data augmentation process")
    augmented_csv_path = augment_data(BASE_CSV_PATH, AUGMENTED_CSV_PATH)
    
    # Step 2: Load the augmented CSV data into a DataFrame
    logger.info("Loading augmented data into DataFrame")
    augmented_df = pd.read_csv(augmented_csv_path)
    
    # Step 3: Load the DataFrame into the database
    load_to_database(augmented_df, TABLE_NAME, engine)
    
    logger.info("ETL process completed successfully")

# Run the ETL process
if name == "main":
    etl_process()