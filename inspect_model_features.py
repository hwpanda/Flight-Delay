import pickle
import pandas as pd
import xgboost as xgb
import numpy as np

model_path = 'model/xgb_final_model_26.pkl'

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"Model loaded: {type(model)}")
    
    if hasattr(model, 'feature_names'):
        print("Feature names found directly on model:")
        print(model.feature_names)
    elif hasattr(model, 'get_booster'):
        print("Feature names found via get_booster():")
        print(model.get_booster().feature_names)
    else:
        print("Could not find feature names directly.")

    # Define features as per app.py
    features = {
        "Year": 2023,
        "Quarter": 4,
        "Month": 11,
        "DayofMonth": 22,
        "DayOfWeek": 3,
        "CRSDepTime": 1200,
        "CRSArrTime": 1400,
        "CRSElapsedTime": 120,
        "Distance": 500.0,
        "origin_temp_c": 20.0,
        "origin_dewpt_c": 10.0,
        "origin_slp_hpa": 1013.0,
        "origin_precip_mm": 0.0,
        "NUMBER_OF_SEATS": 150,
        "Reporting_Airline_woe": 0.0,
        "Origin_woe": 0.0,
        "Dest_woe": 0.0
    }

    print("\nAttempting prediction with current app features...")
    try:
        df = pd.DataFrame([features])
        # Check if model expects DMatrix or DataFrame
        if isinstance(model, xgb.Booster):
            dtest = xgb.DMatrix(df)
            pred = model.predict(dtest)
        else:
            pred = model.predict(df)
        print(f"Prediction successful: {pred}")
    except Exception as e:
        print(f"Prediction failed: {e}")
        
        # find out what features are expected
        if "feature_names" in str(e) or "feature mismatch" in str(e).lower():
            print("Error suggests feature mismatch.")

except Exception as e:
    print(f"Error: {e}")
