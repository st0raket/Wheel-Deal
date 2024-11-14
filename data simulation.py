from faker import Faker
import pandas as pd
import random
from loguru import logger

# Initialize Faker
fake = Faker()

# Define data generation functions for additional columns
def generate_color():
    """Generates a random car color."""
    return random.choice(["black", "white", "silver", "red", "blue", "beige"])

def generate_body_style():
    """Generates a random car body style."""
    return random.choice(["Sedan", "SUV", "Hatchback", "Convertible", "Coupe", "Wagon", "Van", "Truck"])

def generate_powertrain():
    """Generates a random powertrain type."""
    return random.choice(["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid"])

def generate_num_of_prev_owners():
    """Generates a random number of previous owners."""
    return random.randint(1, 5)

def generate_estimated_price():
    """Generates an estimated price for the car."""
    return random.randint(4000, 120000)

# Function to load base data and augment with new columns
def augment_data(base_path, output_path):
    """
    Loads the base CSV file, generates additional columns,
    and saves the augmented data to a new CSV.
    """
    logger.info("Loading base data")
    base_df = pd.read_csv(base_path)

    logger.info("Generating new columns")
    base_df["Color"] = [generate_color() for _ in range(len(base_df))]
    base_df["Body_style"] = [generate_body_style() for _ in range(len(base_df))]
    base_df["Powertrain"] = [generate_powertrain() for _ in range(len(base_df))]
    base_df["Num_of_prev_owners"] = [generate_num_of_prev_owners() for _ in range(len(base_df))]
    base_df["Estimated_price"] = [generate_estimated_price() for _ in range(len(base_df))]

    logger.info("Saving augmented data to CSV")
    base_df.to_csv(output_path, index=False)
    logger.info(f"Augmented data saved to {output_path}")
    return output_path
