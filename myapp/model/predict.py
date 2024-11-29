from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os

# Initialize FastAPI app
app = FastAPI()

# Define the data model for prediction input
class PricePredictionRequest(BaseModel):
    features: list

class DaysToSellPredictionRequest(BaseModel):
    price: int


# Load models
MODEL_DIR = os.getenv("MODEL_STORAGE_PATH", "./models")
price_model_path = os.path.join(MODEL_DIR, "elastic_net_price_model.pkl")
sell_time_model_path = os.path.join(MODEL_DIR, "catboost_sell_time_model.pkl")

try:
    with open(price_model_path, "rb") as f:
        price_model = pickle.load(f)
    with open(sell_time_model_path, "rb") as f:
        sell_time_model = pickle.load(f)
except FileNotFoundError:
    price_model = None
    sell_time_model = None

@app.get("/health")
def health_check():
    """Health check endpoint."""
    if price_model and sell_time_model:
        return {"status": "healthy"}
    return {"status": "unhealthy", "error": "Models not loaded"}

@app.post("/predict_price")
def predict_price(request: PricePredictionRequest):
    """Predict the price using the ElasticNet model."""
    if not price_model:
        raise HTTPException(status_code=500, detail="Price model not loaded")
    try:
        prediction = price_model.predict([request.features])
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_days_to_sell")
def predict_days_to_sell(request: DaysToSellPredictionRequest):
    """Predict days to sell using the CatBoost model."""
    if not sell_time_model:
        raise HTTPException(status_code=500, detail="Days to sell model not loaded")
    try:
        prediction = sell_time_model.predict([request.features])
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
