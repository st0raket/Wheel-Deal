from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

class Car(BaseModel):
    id: Optional[int] 
    car_make_id: str
    model: str
    year: int
    milage: int
    fuel_type_id: str
    color_id: str
    body_style_id: str
    horsepower: int
    transmission_id: str
    website_post_date: Optional[datetime] = None
    sell_date: Optional[datetime] = None
    damage_id: str
    num_of_prev_owners: int
    options_id: str
    estimated_price: int

car_list: List[Car] = []

@app.get("/cars", response_model=Car)
async def get_first_car():
    if not car_list:
        raise HTTPException(status_code=404, detail="No cars available.")
    return car_list[0]

@app.post("/cars", response_model=Car)
async def add_car(car: Car):
    if any(existing_car.id == car.id for existing_car in car_list if car.id is not None):
        raise HTTPException(status_code=400, detail="Car with this ID already exists.")
    car_list.append(car)
    return car

@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, updated_car: Car):
    for i, car in enumerate(car_list):
        if car.id == car_id:
            car_list[i] = updated_car
            return updated_car
    raise HTTPException(status_code=404, detail="Car not found.")

@app.delete("/cars/{car_id}", response_model=Car)
async def delete_car(car_id: int):
    for i, car in enumerate(car_list):
        if car.id == car_id:
            removed_car = car_list.pop(i)
            return removed_car
    raise HTTPException(status_code=404, detail="Car not found.")

