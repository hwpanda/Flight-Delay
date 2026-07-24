import pickle
import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

try:
    import xgboost as xgb
    print(f"XGBoost version: {xgb.__version__}")
except ImportError as e:
    print(f"Failed to import xgboost: {e}")

try:
    import pandas as pd
    print(f"Pandas version: {pd.__version__}")
except ImportError as e:
    print(f"Failed to import pandas: {e}")

try:
    import sklearn
    print(f"Scikit-learn version: {sklearn.__version__}")
except ImportError as e:
    print(f"Failed to import sklearn: {e}")

model_path = 'model/xgb_quick_model_woe.pkl'
if not os.path.exists(model_path):
    print(f"Model file not found at {model_path}")
else:
    print(f"Model file found at {model_path}")
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Successfully loaded model!")
        print(f"Model type: {type(model)}")
        
        # Test prediction
        import pandas as pd
        # Create dummy features matching the model's expectation
        # Features: ["Year","Quarter","Month","DayofMonth","DayOfWeek","CRSDepTime","CRSArrTime","CRSElapsedTime","Distance",...]
        features = {
            "Year": 2025, "Quarter": 4, "Month": 12, "DayofMonth": 25, "DayOfWeek": 4,
            "CRSDepTime": 1200, "CRSArrTime": 1600, "CRSElapsedTime": 240, "Distance": 800,
            "origin_temp_c": 15.0, "origin_dewpt_c": 10.0, "origin_slp_hpa": 1013.0,
            "origin_wind_ms": 5.0, "origin_precip_mm": 0.0,
            "NUMBER_OF_SEATS": 150, "CAPACITY_IN_POUNDS": 40000,
            "Reporting_Airline_woe": 0.0, "Origin_woe": 0.0, "Dest_woe": 0.0,
            "origin_rain_missing": 0, "origin_rain_num": 0.0
        }
        df = pd.DataFrame([features])
        
        print("Attempting prediction with predict_proba...")
        try:
            pred = model.predict_proba(df)
            print(f"predict_proba result: {pred}")
        except AttributeError:
            print("Model does not have predict_proba method.")
            print("Attempting prediction with predict...")
            try:
                # XGBoost Booster might need DMatrix
                import xgboost as xgb
                dtest = xgb.DMatrix(df)
                pred = model.predict(dtest)
                print(f"predict result (DMatrix): {pred}")
            except Exception as e:
                print(f"predict (DMatrix) failed: {e}")
                # Try predict with DataFrame directly (some versions support it)
                try:
                    pred = model.predict(df)
                    print(f"predict result (DataFrame): {pred}")
                except Exception as e2:
                    print(f"predict (DataFrame) failed: {e2}")

    except Exception as e:
        print(f"ERROR loading/predicting: {e}")
        import traceback
        traceback.print_exc()
