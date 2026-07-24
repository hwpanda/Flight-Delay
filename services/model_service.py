import pickle
import pandas as pd
import xgboost as xgb

class ModelService:
    def __init__(self, model_path='model/xgb_final_model_26.pkl'):
        self.model_path = model_path
        self.model = None
        self.model_type = None
        self.load_model()

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.model_type = 'xgboost'
            print("Loaded XGBoost model from pickle.")
        except ImportError:
            print("XGBoost not installed. Falling back to mock prediction.")
            self.model = None
        except Exception as e:
            print(f"Error loading pickle model: {e}")
            self.model = None

    def predict(self, features):
        if not self.model:
            return 0.0, False

        try:
            # Convert to DataFrame
            df = pd.DataFrame([features])
            dtest = xgb.DMatrix(df)
            
            # Predict
            pred_prob = self.model.predict(dtest)[0]
            print(f"Prediction probability: {pred_prob}")

            probability = float(pred_prob)
            delayed = probability > 0.5
            return probability, delayed
        except Exception as e:
            print(f"Prediction error: {e}")
            return 0.0, False
