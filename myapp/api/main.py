# from Database.models import CarMake, Model, FuelType, Color,BodyStyle,Transmission,Option, Damage, Cars
# from Database.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

class Option(BaseModel):
    id: int
    name: str

class MakeOption(Option):
    pass

class ModelOption(Option):
    pass

class TransmissionOption(Option):
    pass

class FuelTypeOption(Option):
    pass

class BodyStyleOption(Option):
    pass

class ColorOption(Option):
    pass

class CarOption(Option):
    pass

class DamageOption(Option):
    pass

# Define the options for each category
make_options = [
    {"id": 0, "name": "Ford"},
    {"id": 1, "name": "Mercedes-Benz"},
    {"id": 2, "name": "Chevrolet"}
]

model_options = [
    {"id": 0, "name": "Focus"},
    {"id": 1, "name": "C-class"},
    {"id": 2, "name": "Volt"}
]

transmission_options = [
    {"id": 0, "name": "Automatic"},
    {"id": 1, "name": "Manual"},
    {"id": 2, "name": "CVT"}
]

fuel_type_options = [
    {"id": 0, "name": "Petrol"},
    {"id": 1, "name": "Diesel"},
    {"id": 2, "name": "Electric"},
    {"id": 3, "name": "Hybrid"}
]

body_style_options = [
    {"id": 0, "name": "Sedan"},
    {"id": 1, "name": "SUV"},
    {"id": 2, "name": "Coupe"},
    {"id": 3, "name": "Convertible"},
    {"id": 4, "name": "Hatchback"},
    {"id": 5, "name": "Wagon"}
]

color_options = [
    {"id": 0, "name": "Black"},
    {"id": 1, "name": "White"},
    {"id": 2, "name": "Red"},
    {"id": 3, "name": "Blue"},
    {"id": 4, "name": "Silver"},
    {"id": 5, "name": "Grey"},
    {"id": 6, "name": "Green"}
]

car_option_options = [
    {"id": 0, "name": "Sunroof"},
    {"id": 1, "name": "Leather Seats"},
    {"id": 2, "name": "Navigation System"},
    {"id": 3, "name": "Bluetooth Connectivity"},
    {"id": 4, "name": "Rearview Camera"},
    {"id": 5, "name": "Heated Seats"}
]

damage_options = [
    {"id": 0, "name": "No Damage"},
    {"id": 1, "name": "Minor Scratch"},
    {"id": 2, "name": "Dent"},
    {"id": 3, "name": "Broken Window"},
    {"id": 4, "name": "Engine Damage"},
    {"id": 5, "name": "Frame Damage"}
]

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

app = FastAPI()

def get_name_from_list(options_list, id_value):
    for option in options_list:
        if option['id'] == id_value:
            return option['name']
    return None

# Define GET endpoints for each array with documentation

@app.get("/make-options", response_model=List[MakeOption])
async def get_make_options():
    """
    Retrieve the list of available car make options.
    
    Returns a list of car makes like Ford, Mercedes-Benz, and Chevrolet.
    """
    if not make_options:
        raise HTTPException(status_code=404, detail="No Make Options available.")
    return make_options


@app.get("/model-options", response_model=List[ModelOption])
async def get_model_options():
    """
    Retrieve the list of available car model options.
    
    Returns a list of car models like Focus, C-class, and Volt.
    """
    if not model_options:
        raise HTTPException(status_code=404, detail="No Model Options available.")
    return model_options


@app.get("/transmission-options", response_model=List[TransmissionOption])
async def get_transmission_options():
    """
    Retrieve the list of available car transmission options.
    
    Returns transmission options like Automatic, Manual, and CVT.
    """
    if not transmission_options:
        raise HTTPException(status_code=404, detail="No Transmission Options available.")
    return transmission_options


@app.get("/fuel-type-options", response_model=List[FuelTypeOption])
async def get_fuel_type_options():
    """
    Retrieve the list of available car fuel type options.
    
    Returns fuel types like Petrol, Diesel, Electric, and Hybrid.
    """
    if not fuel_type_options:
        raise HTTPException(status_code=404, detail="No Fuel Type Options available.")
    return fuel_type_options


@app.get("/body-style-options", response_model=List[BodyStyleOption])
async def get_body_style_options():
    """
    Retrieve the list of available car body style options.
    
    Returns body styles like Sedan, SUV, and Coupe.
    """
    if not body_style_options:
        raise HTTPException(status_code=404, detail="No Body Style Options available.")
    return body_style_options


@app.get("/color-options", response_model=List[ColorOption])
async def get_color_options():
    """
    Retrieve the list of available car color options.
    
    Returns color options like Black, White, Red, and Blue.
    """
    if not color_options:
        raise HTTPException(status_code=404, detail="No Color Options available.")
    return color_options


@app.get("/car-option-options", response_model=List[CarOption])
async def get_car_option_options():
    """
    Retrieve the list of available car additional options.
    
    Returns car options like Sunroof, Leather Seats, and Navigation System.
    """
    if not car_option_options:
        raise HTTPException(status_code=404, detail="No Car Option Options available.")
    return car_option_options


@app.get("/damage-options", response_model=List[DamageOption])
async def get_damage_options():
    """
    Retrieve the list of available car damage options.
    
    Returns damage options like No Damage, Minor Scratch, and Engine Damage.
    """
    if not damage_options:
        raise HTTPException(status_code=404, detail="No Damage Options available.")
    return damage_options

@app.post("/predict", response_model=Prediction)
async def make_prediction(data: PredictionRequest):
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

    # Get the corresponding names from the options lists
    make_name = get_name_from_list(make_options, data.makeId)
    model_name = get_name_from_list(model_options, data.modelId)
    transmission_name = get_name_from_list(transmission_options, data.transmissionId)
    fueltype_name = get_name_from_list(fuel_type_options, data.fueltypeId)
    bodyStyle_name = get_name_from_list(body_style_options, data.bodyStyleId)
    color_name = get_name_from_list(color_options, data.colorId)
    option_name = get_name_from_list(car_option_options, data.optionId)
    damage_name = get_name_from_list(damage_options, data.damageId)

    # If any ID is invalid or not found, raise an error
    if not all([make_name, model_name, transmission_name, fueltype_name, bodyStyle_name, color_name, option_name, damage_name]):
        raise HTTPException(status_code=400, detail="Invalid ID provided for one or more fields.")

    # Simulate the logic of prediction (price and time can be calculated here)
    predicted_price = 25000  # Just a placeholder value, replace with your logic
    predicted_time = 2.5     # Just a placeholder value, replace with your logic

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


