# ETL Service Documentation

## ETL Workflow
This ETL (Extract, Transform, Load) service is designed to manage the pipeline for handling car sales data. It performs the following operations. The `etl_process` function orchestrates the entire ETL workflow:

1. **Data Augmentation:** Enhances the base CSV data with simulated data to expand the dataset.

2. **Dimension Table Population:** Populates predefined dimension tables with categorical data such as car makes, models, fuel types, and more.

3. **Data Transformation:** Transforms the augmented dataset into a structured fact table format.

4. **Data Loading:** Inserts the transformed fact table into a PostgreSQL database.

---

## Features

### Data Augmentation
As our product is related to car sales, we wanted to have a relatively realistic dataset (e.g., car models correspond to their respective makes). That’s why we asked ChatGPT to generate a relatively meaningful dataset and then generated additional columns on top of it. 

While we could have used ChatGPT to generate the entire dataset, we opted to generate data ourselves to enhance our skills, despite the additional complexity of training the model on that data.

The `augment_data` function in the `data_simulation` module expands the base dataset located at `./Database/csv/Wheel Data Final.csv`. 

#### Base Dataset (Wheel Data Final.csv)
The base dataset includes the following columns:
- `Car_make`
- `Model`
- `Milage`
- `Transmission`
- `Year`
- `Website_post_date`
- `Sell_date`
- `Options`
- `Horsepower`

#### Generated Columns
The `augment_data` function generates the following additional columns:
- `Color`
- `Damage`
- `Body_style`
- `Fuel_type`
- `Num_of_prev_owners`
- `Estimated_price`

The augmented dataset is saved as `./Database/csv/car_sales_augmented.csv`.

---

### Predefined Dimension Table Population
The `populate_predefined_dimension_tables` function populates the following dimension tables with predefined values. These tables are saved to the database using the `load_to_database` function:

- **CarMake**: Includes car brands like Audi, BMW, Toyota, etc.
- **Model**: Lists specific models associated with car makes.
- **FuelType**: Captures types of fuel like Gasoline, Diesel, Electric, etc.
- **Color**: Lists car colors such as Black, White, Silver, etc.
- **BodyStyle**: Includes styles like Sedan, SUV, Hatchback, etc.
- **Transmission**: Captures transmission types such as Automatic and Manual.
- **Option**: Lists option packages like Base, Advanced, Luxe, etc.
- **Damage**: Categorizes damage levels such as None, Low, Medium, Total.

---

### Data Transformation
The transformation process includes the following steps:

1. **Mapping Categorical Values:** Maps categorical values (e.g., `CarMake`, `Model`) to their respective IDs using dimension tables via the `get_mapping` function.
2. **Fact Table Creation:** The `transform_to_fact_table` function uses the augmented dataset and the mapped categorical variables to create the fact table.
3. **Saving Transformed Data:** The transformed data is saved as `./Database/csv/car_sales_fact.csv`.

---

### Data Loading
The `load_to_database` function uses PostgreSQL and `psycopg2` to efficiently insert the transformed fact table into the database. Key features include:

- **Batch Insertion:** Optimizes performance by inserting data in batches.
- **Data Type Validation:** Ensures numeric, string, and datetime fields are correctly handled.

---

## Database ERD
The obtained database has the following Entity-Relationship Diagram (ERD):

*(Include or reference the ERD image or diagram here)*

---
