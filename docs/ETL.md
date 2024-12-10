# ETL Service Documentation

## Overview
This ETL (Extract, Transform, Load) service is designed to manage the pipeline for handling car sales data. It performs the following operations:

1. **Data Augmentation:** Enhances the base CSV data with simulated data to expand the dataset.

2. **Dimension Table Population:** Populates predefined dimension tables with categorical data such as car makes, models, fuel types, and more.

3. **Data Transformation:** Transforms the augmented dataset into a structured fact table format.

4. **Data Loading:** Inserts the transformed fact table into a PostgreSQL database.

---

## Features
### Data Augmentation
The `augment_data` function in the `data_simulation` module expands the base dataset located at `./Database/csv/Wheel Data Final.csv`. The augmented dataset is saved as `./Database/csv/car_sales_augmented.csv`.

### Predefined Dimension Table Population
Populates the following dimension tables with predefined values:

- **CarMake**: Includes car brands like Audi, BMW, Toyota, etc.

- **Model**: Lists specific models associated with car makes.

- **FuelType**: Captures types of fuel like Gasoline, Diesel, Electric, etc.

- **Color**: Lists car colors such as black, white, silver, etc.

- **BodyStyle**: Includes styles like Sedan, SUV, Hatchback, etc.

- **Transmission**: Captures transmission types such as Automatic and Manual.

- **Option**: Lists option packages like Base, Advanced, Luxe, etc.

- **Damage**: Categorizes damage levels such as None, Low, Medium, Total.

Dimension tables are populated using SQLAlchemy models, handling potential integrity errors for duplicate entries.

### Data Transformation
Transforms the augmented dataset to a fact table format. The steps include:

1. Mapping categorical values (e.g., CarMake, Model) to their respective IDs using dimension tables.
2. Selecting relevant columns for the fact table, including attributes like mileage, year, horsepower, and estimated price.
3. Saving the transformed data to `./Database/csv/car_sales_fact.csv`.

### Data Loading
The `load_to_database` function uses PostgreSQL and `psycopg2` to efficiently insert the transformed fact table into the database. Key features include:

- Batch insertion for optimized performance.
- Data type validation to handle numeric, string, and datetime fields.

---

## ETL Workflow
### Full Process
The `etl_process` function orchestrates the entire ETL workflow:

1. Augments the base dataset.
2. Populates dimension tables with predefined data.
3. Transforms the augmented dataset into a structured fact table.
4. Loads the fact table into the PostgreSQL database.

### Key Functions
#### `populate_predefined_dimension_tables(session)`
Populates dimension tables for categorical variables. Handles duplicates using SQLAlchemy's `IntegrityError`.

#### `transform_to_fact_table(augmented_csv_path, fact_csv_path, session)`
Transforms augmented data into a fact table format, mapping categorical values to their IDs.

#### `load_to_database(df, table_name, engine)`
Loads data into the database using batch insertion for efficiency.

---

## How to Run the ETL Process
1. Ensure the PostgreSQL database is running and accessible with the following credentials:
   - **Database Name**: `cars`
   - **User**: `postgres`
   - **Password**: `postgrespostgres`
   - **Host**: `postgresql_db`
   - **Port**: `5432`

2. Place the base CSV file (`Wheel Data Final.csv`) in the `./Database/csv/` directory.

3. Run the `ETL` process:
   ```bash
   python etl_service.py
