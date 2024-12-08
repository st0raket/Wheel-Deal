import pandas as pd
from Database.models import CarMake, Model, FuelType, Color,BodyStyle,Transmission, Option, Damage, Cars
from Database.database import get_db
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import pickle
import os
import numpy as np

# Initialize FastAPI app
app = FastAPI()

def get_name_from_database(db: Session, table, id_value: int):
    """
    Retrieve the name corresponding to the given ID from the specified table.
    """
    record = db.query(table).filter(table.ID == id_value).first()
    if record:
        return record.car_make if table == CarMake else record.model if table == Model else \
               record.transmission if table == Transmission else record.fuel_type if table == FuelType else \
               record.body_style if table == BodyStyle else record.color if table == Color else \
               record.option if table == Option else record.damage if table == Damage else None
    return None

#Define the data model for prediction input
class PricePredictionRequest(BaseModel):
    features: list

class DaysToSellPredictionRequest(BaseModel):
    price: int

# Load models
MODEL_DIR = os.getenv("MODEL_STORAGE_PATH", "myapp\model\models")
price_model_path = os.path.join(MODEL_DIR, "elastic_net_price_model.pkl")
sell_time_model_path = os.path.join(MODEL_DIR, "catboost_sell_time_model.pkl")

try:
    with open(price_model_path, "rb") as f:
        price_model = pickle.load(f)
    with open(sell_time_model_path, "rb") as f:
        sell_time_model = pickle.load(f)
except FileNotFoundError:
    price_model = None

class OptionResponse(BaseModel):
    id: int
    name: str

class PredictionRequest(BaseModel):
    makeId: int
    modelId: int
    transmissionId: int
    fueltypeId: int
    bodyStyleId: int
    colorId: int
    optionId: int
    damageId: int
    year: int = Field(..., ge=1886, le=2024, description="Car year must be between 1886 (first car) and the current year.")  # Valid car production years
    mileage: int = Field(..., ge=0, le=1_000_000, description="Mileage must be a positive integer up to 1,000,000.")  # Reasonable max mileage
    horsepower: int = Field(..., ge=0, le=2000, description="Horsepower must be between 0 and 2000.")  # Extreme upper limit for high-performance cars
    numPrevOwners: int = Field(..., ge=0, le=20, description="Number of previous owners must be between 0 and 20.")  # Reasonable max for used cars
    

# Define the response model for the prediction
class Prediction(BaseModel):
    price: float
    time: float
    make: str
    model: str
    transmission: str
    fueltype: str
    bodyStyle: str
    color: str
    option: str
    damage: str
    year: int
    mileage: int
    horsepower: int
    numPrevOwners: int

# Define GET endpoints for each array with documentation

@app.get("/make-options", response_model=List[OptionResponse])
async def get_make_options(db: Session = Depends(get_db)):
    makes = db.query(CarMake).all()
    if not makes:
        raise HTTPException(status_code=404, detail="No Make Options available.")
    return [{"id": make.ID, "name": make.car_make} for make in makes]

@app.get("/model-options/{makeId}", response_model=List[OptionResponse])
async def get_model_options(makeId: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of car models for a specific make by makeId.
    """
    models = db.query(Model).filter(Model.Car_make_id == makeId).all()
    
    if not models:
        raise HTTPException(
            status_code=404, detail=f"No models available for makeId {makeId}."
        )
        
    return [{"id": model.ID, "name": model.model} for model in models]


@app.get("/fuel-type-options", response_model=List[OptionResponse])
async def get_fuel_type_options(db: Session = Depends(get_db)):
    fuel_types = db.query(FuelType).all()
    if not fuel_types:
        raise HTTPException(status_code=404, detail="No Fuel Type Options available.")
    return [{"id": fuel_type.ID, "name": fuel_type.fuel_type} for fuel_type in fuel_types]

@app.get("/color-options", response_model=List[OptionResponse])
async def get_color_options(db: Session = Depends(get_db)):
    colors = db.query(Color).all()
    if not colors:
        raise HTTPException(status_code=404, detail="No Color Options available.")
    return [{"id": color.ID, "name": color.color} for color in colors]

@app.get("/body-style-options", response_model=List[OptionResponse])
async def get_body_style_options(db: Session = Depends(get_db)):
    body_styles = db.query(BodyStyle).all()
    if not body_styles:
        raise HTTPException(status_code=404, detail="No Body Style Options available.")
    return [{"id": body_style.ID, "name": body_style.body_style} for body_style in body_styles]

@app.get("/transmission-options", response_model=List[OptionResponse])
async def get_transmission_options(db: Session = Depends(get_db)):
    transmissions = db.query(Transmission).all()
    if not transmissions:
        raise HTTPException(status_code=404, detail="No Transmission Options available.")
    return [{"id": transmission.ID, "name": transmission.transmission} for transmission in transmissions]

@app.get("/car-option-options", response_model=List[OptionResponse])
async def get_car_option_options(db: Session = Depends(get_db)):
    options = db.query(Option).all()
    if not options:
        raise HTTPException(status_code=404, detail="No Car Option Options available.")
    return [{"id": option.ID, "name": option.option} for option in options]

@app.get("/damage-options", response_model=List[OptionResponse])
async def get_damage_options(db: Session = Depends(get_db)):
    damages = db.query(Damage).all()
    if not damages:
        raise HTTPException(status_code=404, detail="No Damage Options available.")
    return [{"id": damage.ID, "name": damage.damage} for damage in damages]


@app.post("/predict", response_model=Prediction)
async def make_prediction(data: PredictionRequest, db: Session = Depends(get_db)):
    """
    Make a prediction based on the provided data and return the predicted price and time.
    The endpoint raises a 401 error if any of the required fields are missing.
    """
    # Check for missing fields
    missing_fields = []
    for field, value in data.dict().items():
        if value is None:
            missing_fields.append(field)

    if missing_fields:
        raise HTTPException(status_code=401, detail=f"Missing fields: {', '.join(missing_fields)}")

    # Get the corresponding names from the database
    make_name = get_name_from_database(db, CarMake, data.makeId)
    model_name = get_name_from_database(db, Model, data.modelId)
    transmission_name = get_name_from_database(db, Transmission, data.transmissionId)
    fueltype_name = get_name_from_database(db, FuelType, data.fueltypeId)
    bodyStyle_name = get_name_from_database(db, BodyStyle, data.bodyStyleId)
    color_name = get_name_from_database(db, Color, data.colorId)
    option_name = get_name_from_database(db, Option, data.optionId)
    damage_name = get_name_from_database(db, Damage, data.damageId)

    # If any ID is invalid or not found, raise an error
    if not all([make_name, model_name, transmission_name, fueltype_name, bodyStyle_name, color_name, option_name, damage_name]):
        raise HTTPException(status_code=400, detail="Invalid ID provided for one or more fields.")

    # Prepare the features for prediction models
    final_features_template = ['Mileage', 'Year', 'Horsepower', 'Num_of_prev_owners', 'Car_make_BMW',
       'Car_make_Chevrolet', 'Car_make_Ford', 'Car_make_Mercedes-Benz',
       'Car_make_Toyota', 'Model_5 Series', 'Model_A4', 'Model_A6',
       'Model_C-Class', 'Model_Camry', 'Model_Corolla', 'Model_E-Class',
       'Model_Equinox', 'Model_Explorer', 'Model_F-150', 'Model_Fusion',
       'Model_GLC', 'Model_Impala', 'Model_Malibu', 'Model_Mustang',
       'Model_Prius', 'Model_Q5', 'Model_Q7', 'Model_RAV4', 'Model_S-Class',
       'Model_Silverado', 'Model_X3', 'Model_X5', 'Transmission_Manual',
       'Options_Base', 'Options_Full', 'Options_Luxe', 'Color_black',
       'Color_blue', 'Color_red', 'Color_silver', 'Color_white',
       'Damage_Medium', 'Damage_Total', 'Body_style_Coupe',
       'Body_style_Hatchback', 'Body_style_SUV', 'Body_style_Sedan',
       'Body_style_Truck', 'Body_style_Van', 'Body_style_Wagon',
       'Fuel_type_Electric', 'Fuel_type_Gasoline', 'Fuel_type_Hybrid',
       'Fuel_type_Plug-in Hybrid']
    


    transformed_features = {feature: 0 for feature in final_features_template}

    # Assign numerical features
    transformed_features['Mileage'] = data.mileage
    transformed_features['Year'] = data.year
    transformed_features['Horsepower'] = data.horsepower
    transformed_features['Num_of_prev_owners'] = data.numPrevOwners

    # Map categorical features to their one-hot encoded counterparts
    make_mapping = {1: 'Car_make_BMW', 2: 'Car_make_Chevrolet', 3: 'Car_make_Ford', 4: 'Car_make_Mercedes-Benz', 5: 'Car_make_Toyota'}
    model_mapping = {1: 'Model_5 Series', 2: 'Model_A4', 3: 'Model_A6', 4: 'Model_C-Class', 5: 'Model_Camry'}
    transmission_mapping = {1: 'Transmission_Manual'}
    fuel_mapping = {1: 'Fuel_type_Electric', 2: 'Fuel_type_Gasoline', 3: 'Fuel_type_Hybrid'}
    body_style_mapping = {1: 'Body_style_Coupe', 2: 'Body_style_Hatchback', 3: 'Body_style_SUV'}
    color_mapping = {1: 'Color_black', 2: 'Color_blue', 3: 'Color_red'}
    option_mapping = {1: 'Options_Base', 2: 'Options_Full'}
    damage_mapping = {1: 'Damage_Medium', 2: 'Damage_Total'}

    # Update one-hot encoded fields based on input IDs
    transformed_features[make_mapping.get(data.makeId, '')] = 1
    transformed_features[model_mapping.get(data.modelId, '')] = 1
    transformed_features[transmission_mapping.get(data.transmissionId, '')] = 1
    transformed_features[fuel_mapping.get(data.fueltypeId, '')] = 1
    transformed_features[body_style_mapping.get(data.bodyStyleId, '')] = 1
    transformed_features[color_mapping.get(data.colorId, '')] = 1
    transformed_features[option_mapping.get(data.optionId, '')] = 1
    transformed_features[damage_mapping.get(data.damageId, '')] = 1

    # Convert transformed features to the input format expected by the model
    final_features = [transformed_features[feature] for feature in final_features_template]


    # Predict price using the ElasticNet model
    if not price_model:
        raise HTTPException(status_code=500, detail="Price model not loaded")
    try:
        predicted_price = price_model.predict([final_features])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting price: {str(e)}")

    # Predict days to sell using the CatBoost model
    if not sell_time_model:
        raise HTTPException(status_code=500, detail="Days to sell model not loaded")
    try:
        final_features.append(np.log1p(predicted_price))
        predicted_time = sell_time_model.predict([final_features])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting days to sell: {str(e)}")

    # Return the prediction along with the names of the fields
    return {
        "price": np.exp(predicted_price),
        "time": predicted_time,
        "make": make_name,
        "model": model_name,
        "transmission": transmission_name,
        "fueltype": fueltype_name,
        "bodyStyle": bodyStyle_name,
        "color": color_name,
        "option": option_name,
        "damage": damage_name,
        "year": data.year,
        "mileage": data.mileage,
        "horsepower": data.horsepower,
        "numPrevOwners": data.numPrevOwners
    }

