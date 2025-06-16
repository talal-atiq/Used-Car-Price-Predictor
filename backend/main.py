from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import gdown
import os

app = FastAPI(title="Used Car Price Prediction API 🚗")

# Google Drive file ID from your link
FILE_ID = "1Ty8u2nOSlO0eF-FjDh8nrFuU8WbA-38p"
MODEL_FILENAME = "random_forest_model.pkl"

def download_model():
    if not os.path.exists(MODEL_FILENAME):
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        try:
            gdown.download(url, MODEL_FILENAME, quiet=False)
        except Exception as e:
            print("❌ Failed to download model:", e)
            raise RuntimeError("Model download failed")

    try:
        model = joblib.load(MODEL_FILENAME)
        print("✅ Model loaded successfully.")
        return model
    except Exception as e:
        print("❌ Failed to load model:", e)
        raise RuntimeError("Model could not be loaded from downloaded file")

# Load model
model = download_model()
expected_features = model.feature_names_in_
print("✅ Model expects:", expected_features)


# Input schema
class CarFeatures(BaseModel):
    car_age: int
    mileage_kmpl: float
    engine_cc: int
    owner_count: int
    brand: int
    accidents_reported: int
    fuel_type_Electric: int
    fuel_type_Petrol: int
    transmission_Manual: int
    color_Blue: int
    color_Gray: int
    color_Red: int
    color_Silver: int
    color_White: int
    service_history_None: int
    service_history_Partial: int
    insurance_valid_Yes: int


@app.get("/")
def home():
    return {"message": "Welcome to the Used Car Price Prediction API 🚗"}


@app.post("/predict")
def predict_price(data: CarFeatures):
    try:
        input_df = pd.DataFrame([data.dict()])
        input_df = input_df[expected_features]
        prediction = model.predict(input_df)[0]
        return {"predicted_price": round(prediction, 2)}
    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))
