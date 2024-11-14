import pandas as pd
import random
from faker import Faker

fake = Faker()

base_df = cars = pd.read_csv("WHeel Data Final.csv")

def generate_color():
    return random.choice(["black", "white", "silver", "red", "blue", "beige"])

def generate_body_style():
    return random.choice(["Sedan", "SUV", "Hatchback", "Convertible", "Coupe", "Wagon", "Van", "Truck"])

def generate_fuel_type():
    return random.choice(["Gasoline", "Diesel", "Electric", "Hybrid", "Plug-in Hybrid"])

def generate_num_of_prev_owners():
    return random.randint(1, 5)

def generate_estimated_price():
    return random.randint(4000, 120000)


base_df["Color"] = [generate_color() for _ in range(len(base_df))]
base_df["Body_style"] = [generate_body_style() for _ in range(len(base_df))]
base_df["Powertrain"] = [generate_fuel_type() for _ in range(len(base_df))]
base_df["Num_of_prev_owners"] = [generate_num_of_prev_owners() for _ in range(len(base_df))]


output_path = "augmented_car_sales_data_v4.csv"
base_df.to_csv(output_path, index=False)

print(f"Augmented data saved to {output_path}")
