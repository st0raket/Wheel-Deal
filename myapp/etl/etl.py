import traceback
import pandas as pd
from sqlalchemy.orm import Session
from etl.Database.database import engine, SessionLocal
from etl.Database.models import (
    CarMake, Model, FuelType, Color, BodyStyle, Transmission, Option, Damage, Cars
)
from etl.Database.data_simulation import augment_data
from loguru import logger

# Define paths
BASE_CSV_PATH = "Wheel Data Final.csv"  # Base CSV file path
AUGMENTED_CSV_PATH = "car_sales_augmented.csv"  # Augmented CSV file path
FACT_CSV_PATH = "car_sales_fact.csv"  # Fact table CSV file path
TABLE_NAME = "Cars"

# Predefined Values
CAR_MAKE = ["Audi", "BMW", "Chevrolet", "Ford", "Mercedes-Benz", "Toyota"]
MODELS = {
    "Audi": ["A4", "A6", "Q5", "Q7"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Chevrolet": ["Equinox", "Impala", "Malibu", "Silverado"],
    "Ford": ["Explorer", "F-150", "Fusion", "Mustang"],
    "Mercedes-Benz": ["GLC", "C-Class", "E-Class", "S-Class"],
    "Toyota": ["Camry", "Corolla", "Prius", "RAV4"],
}
FUEL_TYPES = ["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid"]
COLORS = ["black", "white", "silver", "red", "blue", "beige"]
BODY_STYLES = ["Sedan", "SUV", "Hatchback", "Convertible", "Coupe", "Wagon", "Van", "Truck"]
TRANSMISSIONS = ["Automatic", "Manual"]
OPTIONS = ["Base", "Advanced", "Luxe", "Full"]
DAMAGES = ["Total", "None", "Low", "Medium"]

# Function to load a DataFrame into the database
def load_to_database(df, table_name, engine):
    """
    Load a DataFrame into the specified database table.
    """
    try:
        logger.info(f"Loading data into the database table: {table_name}")
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        logger.info(f"Data successfully loaded into {table_name}")
    except Exception:
        logger.error(f"Error loading data to database: {traceback.format_exc()}")
        raise

# Function to populate predefined dimension tables
def populate_predefined_dimension_tables(session):
    """
    Populate predefined values for all dimension tables, including model-to-make mapping.

    Args:
        session: SQLAlchemy session.
    """
    logger.info("Populating predefined dimension tables")

    # Populate car makes and models
    car_make_records = {}
    for make in CAR_MAKE:
        car_make = CarMake(car_make=make)
        session.add(car_make)
        session.flush()  # Get ID for model-to-make mapping
        car_make_records[make] = car_make.ID  # Store the ID

    for make, model_list in MODELS.items():
        car_make_id = car_make_records[make]
        for model in model_list:
            session.add(Model(model=model, Car_make_id=car_make_id))

    # Populate other dimension tables
    for fuel in FUEL_TYPES:
        session.add(FuelType(fuel_type=fuel))
    for color in COLORS:
        session.add(Color(color=color))
    for body_style in BODY_STYLES:
        session.add(BodyStyle(body_style=body_style))
    for transmission in TRANSMISSIONS:
        session.add(Transmission(transmission=transmission))
    for option in OPTIONS:
        session.add(Option(option=option))
    for damage in DAMAGES:
        session.add(Damage(damage=damage))

    session.commit()
    logger.info("Predefined dimension tables populated successfully")

# Function to fetch mappings from dimensional tables
def get_mapping(session, model, column_name):
    """
    Create a mapping dictionary from a dimensional table.

    Args:
        session: SQLAlchemy session.
        model: SQLAlchemy model for the table.
        column_name: Column name to map.

    Returns:
        dict: Mapping of {value: id}.
    """
    records = session.query(model).all()
    return {getattr(record, column_name): record.ID for record in records}

# Function to transform augmented data into a fact table
def transform_to_fact_table(augmented_csv_path, fact_csv_path, session):
    """
    Transforms the augmented CSV into a fact table with IDs.

    Args:
        augmented_csv_path (str): Path to the augmented CSV.
        fact_csv_path (str): Path to save the fact table CSV.
        session: SQLAlchemy session.
    """
    logger.info("Loading augmented CSV")
    df = pd.read_csv(augmented_csv_path)


    logger.info("Fetching mappings for categorical variables")
    mappings = {
        "Car_make": get_mapping(session, CarMake, "car_make"),
        "Model": get_mapping(session, Model, "model"),
        "Fuel_type": get_mapping(session, FuelType, "fuel_type"),
        "Color": get_mapping(session, Color, "color"),
        "Body_style": get_mapping(session, BodyStyle, "body_style"),
        "Transmission": get_mapping(session, Transmission, "transmission"),
        "Options": get_mapping(session, Option, "option"),
        "Damage": get_mapping(session, Damage, "damage"),
    }

    logger.info("Transforming categorical values to IDs")
    df["Car_make_id"] = df["Car_make"].map(mappings["Car_make"])
    df["Model_id"] = df["Model"].map(mappings["Model"])
    df["Fuel_type_id"] = df["Fuel_type"].map(mappings["Fuel_type"])
    df["Color_id"] = df["Color"].map(mappings["Color"])
    df["Body_style_id"] = df["Body_style"].map(mappings["Body_style"])
    df["Transmission_id"] = df["Transmission"].map(mappings["Transmission"])
    df["Options_id"] = df["Options"].map(mappings["Options"])
    df["Damage_id"] = df["Damage"].map(mappings["Damage"])

    # Keep only necessary columns
    fact_df = df[
        ["Car_make_id", "Model_id", "Fuel_type_id", "Color_id", "Body_style_id",
         "Transmission_id", "Options_id", "Damage_id", "Year", "Mileage",
         "Horsepower", "Website_post_date", "Sell_date", "Num_of_prev_owners", "Estimated_price"]
    ]

    # Add an auto-incrementing ID column
    fact_df.insert(0, "ID", range(1, len(fact_df) + 1))

    logger.info(f"Saving fact table to {fact_csv_path}")
    fact_df.to_csv(fact_csv_path, index=False)

    logger.info("Fact table transformation complete")

# Full ETL Process
def etl_process():
    """
    End-to-end ETL process: augment data, create dimension tables, transform to fact table, and load to database.
    """
    session = SessionLocal()
    try:
        # Step 1: Augment the base CSV data with new columns
        logger.info("Starting data generation process")
        augment_data(BASE_CSV_PATH, AUGMENTED_CSV_PATH)

        # Step 2: Populate dimension tables
        populate_predefined_dimension_tables(session)

        # Step 3: Transform the augmented data into a fact table
        transform_to_fact_table(AUGMENTED_CSV_PATH, FACT_CSV_PATH, session)

        # Step 4: Load the fact table into the database
        logger.info("Loading fact table into the database")
        fact_df = pd.read_csv(FACT_CSV_PATH)
        load_to_database(fact_df, TABLE_NAME, engine)

        logger.info("ETL process completed successfully")
    except Exception:
        logger.error(f"ETL process failed: {traceback.format_exc()}")
    finally:
        session.close()

if __name__ == "__main__":
    etl_process()
