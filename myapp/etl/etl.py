import traceback
import pandas as pd
from sqlalchemy.orm import Session
from Database.database import engine, SessionLocal
from Database.models import (
    CarMake, Model, FuelType, Color, BodyStyle, Transmission, Option, Damage, Cars
)
from Database.data_simulation import augment_data
from loguru import logger
from sqlalchemy.exc import IntegrityError
import psycopg2
from psycopg2.extras import execute_batch
import numpy as np

CSV_FOLDER = "./Database/csv/"
# Define paths
BASE_CSV_PATH = CSV_FOLDER + "Wheel Data Final.csv"  # Base CSV file path
AUGMENTED_CSV_PATH = CSV_FOLDER + "car_sales_augmented.csv"  # Augmented CSV file path
FACT_CSV_PATH = CSV_FOLDER + "car_sales_fact.csv"  # Fact table CSV file path
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

def load_to_database(df, table_name, engine):
    """
    Load data into the specified database table using psycopg2's execute_batch.
    """
    import psycopg2
    from psycopg2.extras import execute_batch
    import numpy as np

    try:
        conn_params = {
            "dbname": "cars",
            "user": "postgres",
            "password": "postgrespostgres",
            "host": "postgresql_db",
            "port": 5432,
        }
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()

        # Ensure table name is quoted
        table_name_quoted = f'"{table_name}"'

        # Prepare the INSERT query with placeholders
        insert_query = f"""
            INSERT INTO {table_name_quoted} (
                "ID", "Car_make_ID", "Model_ID", "Fuel_type_ID", "Color_ID",
                "Body_style_ID", "Transmission_ID", "Options_ID", "Damage_ID",
                "Year", "Mileage", "Horsepower", "Website_post_date",
                "Sell_date", "Num_of_prev_owners", "Estimated_price"
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Convert DataFrame to a list of tuples, ensuring native Python types
        data = df.to_records(index=False)
        data = [
            tuple(
                int(x) if isinstance(x, np.integer) else
                float(x) if isinstance(x, np.floating) else
                str(x) if isinstance(x, np.datetime64) else
                x
                for x in row
            )
            for row in data
        ]

        # Use execute_batch for efficient bulk inserts
        execute_batch(cursor, insert_query, data)

        conn.commit()
        print(f"Data successfully loaded into table {table_name}")
    except Exception as e:
        print(f"Error loading data to database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# Function to populate predefined dimension tables
def populate_predefined_dimension_tables(session):
    logger.info("Populating predefined dimension tables")
    try:
        # Populate car makes and models
        car_make_records = {}
        for make in CAR_MAKE:
            car_make = CarMake(car_make=make)
            try:
                session.add(car_make)
                session.flush()  # Get ID for model-to-make mapping
                car_make_records[make] = car_make.ID
            except IntegrityError:
                session.rollback()  # Ignore duplicates
                car_make = session.query(CarMake).filter_by(car_make=make).one()
                car_make_records[make] = car_make.ID

        for make, model_list in MODELS.items():
            car_make_id = car_make_records[make]
            for model in model_list:
                model_record = Model(model=model, Car_make_id=car_make_id)
                try:
                    session.add(model_record)
                    session.flush()
                except IntegrityError:
                    session.rollback()

        # Populate other dimension tables
        dimension_data_mapping = {
            "FuelType": ("fuel_type", FUEL_TYPES),
            "Color": ("color", COLORS),
            "BodyStyle": ("body_style", BODY_STYLES),
            "Transmission": ("transmission", TRANSMISSIONS),
            "Option": ("option", OPTIONS),
            "Damage": ("damage", DAMAGES),
        }

        for model_name, (column_name, data_list) in dimension_data_mapping.items():
            model_class = globals()[model_name]
            for value in data_list:
                record = model_class(**{column_name: value})
                try:
                    session.add(record)
                    session.flush()
                except IntegrityError:
                    session.rollback()

        session.commit()
        logger.info("Predefined dimension tables populated successfully")

    except Exception:
        session.rollback()
        logger.error("Error populating dimension tables")
        logger.error(traceback.format_exc())
        raise

# Function to fetch mappings from dimensional tables
def get_mapping(session, model, column_name):
    records = session.query(model).all()
    return {getattr(record, column_name): record.ID for record in records}

# Function to transform augmented data into a fact table
def transform_to_fact_table(augmented_csv_path, fact_csv_path, session):
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

    fact_df = df[
        ["Car_make_id", "Model_id", "Fuel_type_id", "Color_id", "Body_style_id",
         "Transmission_id", "Options_id", "Damage_id", "Year", "Mileage",
         "Horsepower", "Website_post_date", "Sell_date", "Num_of_prev_owners", "Estimated_price"]
    ]

    fact_df.insert(0, "ID", range(1, len(fact_df) + 1))

    logger.info(f"Saving fact table to {fact_csv_path}")
    fact_df.to_csv(fact_csv_path, index=False)

    logger.info("Fact table transformation complete")

# Full ETL Process
def etl_process():
    session = SessionLocal()
    try:
        logger.info("Starting data augmentation")
        augment_data(BASE_CSV_PATH, AUGMENTED_CSV_PATH)

        logger.info("Populating predefined dimension tables")
        populate_predefined_dimension_tables(session)

        logger.info("Transforming augmented data into a fact table")
        transform_to_fact_table(AUGMENTED_CSV_PATH, FACT_CSV_PATH, session)

        logger.info("Loading fact table into the database")
        fact_df = pd.read_csv(FACT_CSV_PATH)
        fact_df['Sell_date'] = fact_df['Sell_date'].where(fact_df['Sell_date'].notna(), None)
        load_to_database(fact_df, TABLE_NAME, engine)

        logger.info("ETL process completed successfully")
    except Exception:
        logger.error("ETL process failed")
        logger.error(traceback.format_exc())
    finally:
        session.close()

if __name__ == "__main__":
    etl_process()
