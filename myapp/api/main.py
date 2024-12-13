import pandas as pd
from Database.models import CarMake, Model, FuelType, Color, BodyStyle, Transmission, Option, Damage, Cars
from Database.database import get_db
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import os
import numpy as np

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Fixed final_features_template matching the model's expected features
final_features_template: List[str] = [
    'Mileage', 'Year', 'Horsepower', 'Num_of_prev_owners',
    'Car_make_BMW', 'Car_make_Chevrolet', 'Car_make_Ford',
    'Car_make_Mercedes-Benz', 'Car_make_Toyota',
    'Model_5 Series', 'Model_A4', 'Model_A6', 'Model_C-Class',
    'Model_Camry', 'Model_Corolla', 'Model_E-Class',
    'Model_Equinox', 'Model_Explorer', 'Model_F-150',
    'Model_Fusion', 'Model_GLC', 'Model_Impala', 'Model_Malibu',
    'Model_Mustang', 'Model_Prius', 'Model_Q5', 'Model_Q7',
    'Model_RAV4', 'Model_S-Class', 'Model_Silverado',
    'Model_X3', 'Model_X5', 'Transmission_Manual',
    'Options_Base', 'Options_Full', 'Options_Luxe',
    'Color_black', 'Color_blue', 'Color_red', 'Color_silver',
    'Color_white', 'Damage_Medium', 'Damage_Total',
    'Body_style_Coupe', 'Body_style_Hatchback', 'Body_style_SUV',
    'Body_style_Sedan', 'Body_style_Truck', 'Body_style_Van',
    'Body_style_Wagon', 'Fuel_type_Electric', 'Fuel_type_Gasoline',
    'Fuel_type_Hybrid', 'Fuel_type_Plug-in Hybrid'
]

# Global mapping dictionaries
make_mapping: Dict[int, str] = {}
model_mapping: Dict[int, str] = {}
transmission_mapping: Dict[int, str] = {}
fuel_mapping: Dict[int, str] = {}
body_style_mapping: Dict[int, str] = {}
color_mapping: Dict[int, str] = {}
option_mapping: Dict[int, str] = {}
damage_mapping: Dict[int, str] = {}

# Numerical features (fixed)
numerical_features = ['Mileage', 'Year', 'Horsepower', 'Num_of_prev_owners']

# Function to initialize mappings based on the fixed final_features_template
def initialize_mappings(db: Session):
    global make_mapping, model_mapping, transmission_mapping, fuel_mapping
    global body_style_mapping, color_mapping, option_mapping, damage_mapping

    # Car Makes
    makes = db.query(CarMake).all()
    make_mapping = {make.ID: f"Car_make_{make.car_make.replace(' ', '_')}" 
                   for make in makes 
                   if f"Car_make_{make.car_make.replace(' ', '_')}" in final_features_template}

    # Models
    models = db.query(Model).all()
    model_mapping = {model.ID: f"Model_{model.model.replace(' ', '_')}" 
                    for model in models 
                    if f"Model_{model.model.replace(' ', '_')}" in final_features_template}

    # Transmissions
    transmissions = db.query(Transmission).all()
    transmission_mapping = {trans.ID: f"Transmission_{trans.transmission.replace(' ', '_')}" 
                            for trans in transmissions 
                            if f"Transmission_{trans.transmission.replace(' ', '_')}" in final_features_template}

    # Fuel Types
    fuels = db.query(FuelType).all()
    fuel_mapping = {fuel.ID: f"Fuel_type_{fuel.fuel_type.replace(' ', '_')}" 
                   for fuel in fuels 
                   if f"Fuel_type_{fuel.fuel_type.replace(' ', '_')}" in final_features_template}

    # Body Styles
    body_styles = db.query(BodyStyle).all()
    body_style_mapping = {body.ID: f"Body_style_{body.body_style.replace(' ', '_')}" 
                          for body in body_styles 
                          if f"Body_style_{body.body_style.replace(' ', '_')}" in final_features_template}

    # Colors
    colors = db.query(Color).all()
    color_mapping = {color.ID: f"Color_{color.color.replace(' ', '_')}" 
                     for color in colors 
                     if f"Color_{color.color.replace(' ', '_')}" in final_features_template}

    # Options
    options = db.query(Option).all()
    option_mapping = {opt.ID: f"Options_{opt.option.replace(' ', '_')}" 
                     for opt in options 
                     if f"Options_{opt.option.replace(' ', '_')}" in final_features_template}

    # Damages
    damages = db.query(Damage).all()
    damage_mapping = {dam.ID: f"Damage_{dam.damage.replace(' ', '_')}" 
                      for dam in damages 
                      if f"Damage_{dam.damage.replace(' ', '_')}" in final_features_template}

# Dependency to initialize mappings once at startup
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    initialize_mappings(db)

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

# Define the data model for prediction input
class PricePredictionRequest(BaseModel):
    features: list

class DaysToSellPredictionRequest(BaseModel):
    price: int

# Load models
MODEL_DIR = os.getenv("MODEL_STORAGE_PATH", "myapp\\model\\models")
price_model_path = os.path.join(MODEL_DIR, "elastic_net_price_model.pkl")
sell_time_model_path = os.path.join(MODEL_DIR, "catboost_sell_time_model.pkl")

try:
    with open(price_model_path, "rb") as f:
        price_model = pickle.load(f)
    with open(sell_time_model_path, "rb") as f:
        sell_time_model = pickle.load(f)
except FileNotFoundError:
    price_model = None
    sell_time_model = None  # Ensure sell_time_model is also set to None

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
    transformed_features = {feature: 0 for feature in final_features_template}

    # Assign numerical features
    transformed_features['Mileage'] = data.mileage
    transformed_features['Year'] = data.year
    transformed_features['Horsepower'] = data.horsepower
    transformed_features['Num_of_prev_owners'] = data.numPrevOwners

    # Assign one-hot encoded features using dynamic mappings
    # Only set features if they exist in the mapping
    make_feature = make_mapping.get(data.makeId)
    if make_feature:
        transformed_features[make_feature] = 1

    model_feature = model_mapping.get(data.modelId)
    if model_feature:
        transformed_features[model_feature] = 1

    transmission_feature = transmission_mapping.get(data.transmissionId)
    if transmission_feature:
        transformed_features[transmission_feature] = 1

    fuel_feature = fuel_mapping.get(data.fueltypeId)
    if fuel_feature:
        transformed_features[fuel_feature] = 1

    body_style_feature = body_style_mapping.get(data.bodyStyleId)
    if body_style_feature:
        transformed_features[body_style_feature] = 1

    color_feature = color_mapping.get(data.colorId)
    if color_feature:
        transformed_features[color_feature] = 1

    option_feature = option_mapping.get(data.optionId)
    if option_feature:
        transformed_features[option_feature] = 1

    damage_feature = damage_mapping.get(data.damageId)
    if damage_feature:
        transformed_features[damage_feature] = 1

    # Convert transformed features to the input format expected by the model
    try:
        final_features = [transformed_features[feature] for feature in final_features_template]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Feature missing in final_features_template: {str(e)}")

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
        # Append the log-transformed predicted price as a feature
        features_for_sell_time = final_features.copy()
        features_for_sell_time.append(np.log1p(predicted_price))
        predicted_time = sell_time_model.predict([features_for_sell_time])[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting days to sell: {str(e)}")

    # Return the prediction along with the names of the fields
    return {
        "price": float(predicted_price),  # Assuming the model outputs the actual price
        "time": float(predicted_time),
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
