import pickle
import sys
import pandas as pd

try:
    with open('model/xgb_quick_model_woe.pkl', 'rb') as f:
        model = pickle.load(f)
    
    print("Model type:", type(model))
    if hasattr(model, 'feature_names_in_'):
        print("Feature names:", model.feature_names_in_)
    elif hasattr(model, 'get_booster'):
        print("Feature names:", model.get_booster().feature_names)
    else:
        print("Could not determine feature names directly.")
        
except Exception as e:
    print(f"Error loading model: {e}")
