from Database.models import CarMake, Model, FuelType, Color,BodyStyle,Transmission, Option, Damage, Cars
from Database.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import pickle
import os

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

# Define the data model for prediction input
# class PricePredictionRequest(BaseModel):
#     features: list

# class DaysToSellPredictionRequest(BaseModel):
#     price: int

# # Load models
# MODEL_DIR = os.getenv("MODEL_STORAGE_PATH", ".myapp\model\models")
# price_model_path = os.path.join(MODEL_DIR, "elastic_net_price_model.pkl")
# sell_time_model_path = os.path.join(MODEL_DIR, "catboost_sell_time_model.pkl")

# try:
#     with open(price_model_path, "rb") as f:
#         price_model = pickle.load(f)
#     with open(sell_time_model_path, "rb") as f:
#         sell_time_model = pickle.load(f)
# except FileNotFoundError:
#     price_model = None

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
    year: int
    mileage: int
    horsepower: int

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

# Define GET endpoints for each array with documentation

@app.get("/make-options", response_model=List[OptionResponse])
async def get_make_options(db: Session = Depends(get_db)):
    makes = db.query(CarMake).all()
    if not makes:
        raise HTTPException(status_code=404, detail="No Make Options available.")
    return [{"id": make.ID, "name": make.car_make} for make in makes]

@app.get("/model-options", response_model=List[OptionResponse])
async def get_model_options(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    if not models:
        raise HTTPException(status_code=404, detail="No Model Options available.")
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

    # Simulate the logic of prediction (price and time can be calculated here)
    predicted_price = 25000  # Replace with your actual prediction logic
    predicted_time = 2.5     # Replace with your actual prediction logic

    # Return the prediction along with the names of the fields
    return {
        "price": predicted_price,
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
        "horsepower": data.horsepower
    }

# @app.post("/predict", response_model=Prediction)
# async def make_prediction(data: PredictionRequest):
#     """
#     Make a prediction based on the provided data and return the predicted price and time.
#     The endpoint raises a 401 error if any of the required fields are missing.
#     """
#     # Check for missing fields
#     missing_fields = []
#     for field, value in data.dict().items():
#         if value is None:
#             missing_fields.append(field)

#     if missing_fields:
#         raise HTTPException(status_code=401, detail=f"Missing fields: {', '.join(missing_fields)}")

#     # Get the corresponding names from the options lists
#     make_name = get_name_from_list(make_options, data.makeId)
#     model_name = get_name_from_list(model_options, data.modelId)
#     transmission_name = get_name_from_list(transmission_options, data.transmissionId)
#     fueltype_name = get_name_from_list(fuel_type_options, data.fueltypeId)
#     bodyStyle_name = get_name_from_list(body_style_options, data.bodyStyleId)
#     color_name = get_name_from_list(color_options, data.colorId)
#     option_name = get_name_from_list(car_option_options, data.optionId)
#     damage_name = get_name_from_list(damage_options, data.damageId)

#     # If any ID is invalid or not found, raise an error
#     if not all([make_name, model_name, transmission_name, fueltype_name, bodyStyle_name, color_name, option_name, damage_name]):
#         raise HTTPException(status_code=400, detail="Invalid ID provided for one or more fields.")

#     # Prepare the features for prediction models
#     features = [
#         data.year,
#         data.mileage,
#         data.horsepower,
#         data.makeId,
#         data.modelId,
#         data.transmissionId,
#         data.fueltypeId,
#         data.bodyStyleId,
#         data.colorId,
#         data.optionId,
#         data.damageId
#     ]

#     # Predict price using the ElasticNet model
#     if not price_model:
#         raise HTTPException(status_code=500, detail="Price model not loaded")
#     try:
#         predicted_price = price_model.predict([features])[0]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error predicting price: {str(e)}")

#     # Predict days to sell using the CatBoost model
#     if not sell_time_model:
#         raise HTTPException(status_code=500, detail="Days to sell model not loaded")
#     try:
#         predicted_time = sell_time_model.predict([features])[0]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error predicting days to sell: {str(e)}")

#     # Return the prediction along with the names of the fields
#     return {
#         "price": predicted_price,
#         "time": predicted_time,
#         "make": make_name,
#         "model": model_name,
#         "transmission": transmission_name,
#         "fueltype": fueltype_name,
#         "bodyStyle": bodyStyle_name,
#         "color": color_name,
#         "option": option_name,
#         "damage": damage_name,
#         "year": data.year,
#         "mileage": data.mileage,
#         "horsepower": data.horsepower
#     }

