import pandas as pd
import os
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Paths
DATA_PATH = os.path.join('dataset', 'processed', 'real_complaints_derived.csv')
MODEL_DIR = os.path.join('saved_models', 'ml_models')

def train_severity_model() -> None:
    """Trains, evaluates, and saves the best model for severity prediction."""
    logging.info("Loading dataset...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        logging.error(f"Dataset not found at {DATA_PATH}. Run data generator first.")
        return

    # ==========================================
    # SAFETY NET: Auto-Augment Rare Classes
    # Ensures no class has fewer than 5 instances so stratify doesn't crash
    # ==========================================
    target_counts = df['severity'].value_counts()
    for severity_class, count in target_counts.items():
        if count < 5:
            logging.warning(f"Rare class detected: '{severity_class}' ({count} instances). Auto-augmenting...")
            rare_rows = df[df['severity'] == severity_class]
            # Duplicate the rare rows until we have at least 5
            num_copies = 5 - count
            copies = rare_rows.sample(n=num_copies, replace=True, random_state=42)
            df = pd.concat([df, copies], ignore_index=True)

    # Define features (X) and target (y)
    X = df.drop('severity', axis=1)
    y = df['severity']

    # XGBoost requires targets to be strictly numeric (0, 1, 2, 3)
    target_encoder = LabelEncoder()
    y_encoded = target_encoder.fit_transform(y)
    
    # Save the label encoder to map predictions back to strings later
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(target_encoder, os.path.join(MODEL_DIR, 'target_encoder.joblib'))

    # Split the data (Stratified to maintain balanced class proportions)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # ==========================================
    # 1. Build Preprocessing Steps
    # ==========================================
    categorical_features = ['category', 'weather', 'traffic_density', 'road_importance']
    numeric_features = [
        'latitude', 'longitude', 'hour_of_day', 'month', 
        'distance_to_hospital_km', 'distance_to_school_km', 'historical_incidents_30d'
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    # ==========================================
    # 2. Define Candidate Models
    # ==========================================
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
    }

    best_model = None
    best_accuracy = 0.0
    best_model_name = ""

    # ==========================================
    # 3. Train and Evaluate
    # ==========================================
    for name, model in models.items():
        logging.info(f"Training {name}...")
        
        # Create full pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        logging.info(f"{name} Accuracy: {acc:.4f}")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model = pipeline
            best_model_name = name

    logging.info(f"--- Best Model Selected: {best_model_name} (Acc: {best_accuracy:.4f}) ---")
    
    # Print detailed report for the best model
    y_pred_best = best_model.predict(X_test)
    logging.info("\n" + classification_report(y_test, y_pred_best, target_names=target_encoder.classes_))

    # ==========================================
    # 4. Serialize the Best Pipeline
    # ==========================================
    model_path = os.path.join(MODEL_DIR, 'severity_pipeline.joblib')
    joblib.dump(best_model, model_path)
    logging.info(f"Model saved successfully to {model_path}")

if __name__ == "__main__":
    train_severity_model()