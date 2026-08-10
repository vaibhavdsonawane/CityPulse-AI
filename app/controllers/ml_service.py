import os
import joblib
import pandas as pd
import logging
from typing import Dict, Any

# Configure paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', '..', 'saved_models', 'ml_models')
PIPELINE_PATH = os.path.join(MODEL_DIR, 'severity_pipeline.joblib')
ENCODER_PATH = os.path.join(MODEL_DIR, 'target_encoder.joblib')

class SeverityPredictor:
    """Singleton class to load the ML model once and serve predictions."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SeverityPredictor, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.encoder = None
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        try:
            self.model = joblib.load(PIPELINE_PATH)
            self.encoder = joblib.load(ENCODER_PATH)
            logging.info("ML Pipeline and Label Encoder loaded successfully.")
        except FileNotFoundError:
            logging.error("ML Model files not found. Please run train_severity.py first.")
            self.model = None

    def predict(self, issue_data: Dict[str, Any]) -> str:
        """
        Takes raw issue dictionary, formats it as a DataFrame, and returns the severity string.
        """
        if self.model is None or self.encoder is None:
            return "Pending AI Analysis" # Fallback if model isn't trained yet
            
        try:
            # Convert dictionary to DataFrame for the scikit-learn pipeline
            df = pd.DataFrame([issue_data])
            
            # Predict returns the encoded integer (0, 1, 2, 3)
            prediction_encoded = self.model.predict(df)
            
            # Inverse transform to get string (Low, Medium, High, Critical)
            prediction_label = self.encoder.inverse_transform(prediction_encoded)[0]
            
            return prediction_label
            
        except Exception as e:
            logging.error(f"Prediction failed: {str(e)}")
            return "Error calculating severity"

# Expose a ready-to-use instance
severity_ai = SeverityPredictor()