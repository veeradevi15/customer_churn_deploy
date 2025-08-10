from fastapi import FastAPI
from pydantic import BaseModel
import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle

app = FastAPI()

MODEL_PATH=os.path.join(os.path.dirname(__file__),"bank_churn_model.h5")
SCALER_PATH=os.path.join(os.path.dirname(__file__),"scaler.pkl")
model=load_model(MODEL_PATH)
scaler=pickle.load(open(SCALER_PATH, 'rb'))

class CustomerDATA(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

geo_map = {'France': 0, 'Spain': 1, 'Germany': 2}
gender_map = {'Male': 1, 'Female': 0}

@app.post('/predict')
def predict_churn(features: CustomerDATA):
    try:
        data = features.dict()
        data['Geography'] = geo_map.get(data['Geography'], 0)
        data['Gender'] = gender_map.get(data['Gender'], 0)
        x = pd.DataFrame([data])
        print("Input DataFrame:", x)
        x_scaled = scaler.transform(x)
        pred = model.predict(x_scaled)[0][0]
        print("Prediction:", pred)
        return {'churn_probability': float(pred), 'churned': int(pred > 0.5)}
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}