import joblib
import numpy as np
import pandas as pd

# Paths to model and preprocessing tools
MODEL_PATH = r'C:\Users\swath\pawsitivehealth\healthapp\models\activity_model.pkl'
ENCODERS_PATH = r'C:\Users\swath\pawsitivehealth\healthapp\models\label_encoders.pkl'
SCALER_PATH = r'C:\Users\swath\pawsitivehealth\healthapp\models\scaler.pkl'
DATASET_PATH = r'C:\Users\swath\pawsitivehealth\healthapp\data\dog_activity_data.csv'

def load_model():
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, encoders, scaler

def predict_recommendation(breed, age, health_condition, walk_minutes, playtime_minutes, mental_stimulation_minutes):
    model, encoders, scaler = load_model()

    # Encode input
    breed_encoded = encoders['Breed'].transform([breed])[0]
    health_condition_encoded = encoders['Health Condition'].transform([health_condition])[0]
    
    # Prepare input data
    input_data = np.array([[breed_encoded, age, health_condition_encoded, walk_minutes, playtime_minutes, mental_stimulation_minutes]])
    
    # Scale input data
    input_data_scaled = scaler.transform(input_data)
    
    # Predict
    recommendation_encoded = model.predict(input_data_scaled)[0]
    recommendation = encoders['Recommendation'].inverse_transform([recommendation_encoded])[0]
    
    return recommendation

# For testing purposes
if __name__ == "__main__":
    # Test data
    print(predict_recommendation("Golden Retriever", 5, "Normal", 30, 20, 15))
