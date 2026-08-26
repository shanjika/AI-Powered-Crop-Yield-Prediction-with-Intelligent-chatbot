import os
import json
import time
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.ml.dataset_generator import generate_tamil_nadu_agri_dataset

CATEGORICAL_FEATURES = ["district", "crop", "pattam", "soil_type", "irrigation_type"]
NUMERICAL_FEATURES = [
    "temperature", "humidity", "rainfall_mm",
    "soil_ph", "soil_n", "soil_p", "soil_k",
    "soil_ec", "soil_organic_carbon"
]
TARGET_FEATURE = "yield_per_acre"

def train_and_evaluate_models():
    artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    csv_path = os.path.join(data_dir, "tamil_nadu_crop_yield_dataset.csv")

    if os.path.exists(csv_path):
        print(f"Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        print("Generating fresh Tamil Nadu agricultural dataset...")
        os.makedirs(data_dir, exist_ok=True)
        df = generate_tamil_nadu_agri_dataset(15000)
        df.to_csv(csv_path, index=False)

    print(f"Total dataset size: {df.shape[0]} records, {df.shape[1]} columns")

    X = df[CATEGORICAL_FEATURES + NUMERICAL_FEATURES]
    y = df[TARGET_FEATURE]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ]
    )

    candidate_models = {
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=120, max_depth=20, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting Regressor": GradientBoostingRegressor(
            n_estimators=120, learning_rate=0.1, max_depth=6, random_state=42
        ),
        "XGBoost Regressor": XGBRegressor(
            n_estimators=150, learning_rate=0.08, max_depth=6, random_state=42, n_jobs=-1
        )
    }

    results = {}
    trained_pipelines = {}

    print("\n--- Model Training & Comparison ---")
    for name, model in candidate_models.items():
        print(f"Training {name}...")
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", model)
        ])

        start_time = time.time()
        pipeline.fit(X_train, y_train)
        train_duration = round(time.time() - start_time, 2)

        y_pred = pipeline.predict(X_test)

        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))

        results[name] = {
            "mae": round(mae, 2),
            "mse": round(mse, 2),
            "rmse": round(rmse, 2),
            "r2_score": round(r2, 4),
            "training_time_seconds": train_duration
        }
        trained_pipelines[name] = pipeline

        print(f"  > {name} -> R²: {round(r2, 4)}, MAE: {round(mae, 2)} kg/acre, RMSE: {round(rmse, 2)} kg/acre ({train_duration}s)")

    # Select champion based on highest R2 score
    best_model_name = max(results, key=lambda k: results[k]["r2_score"])
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = results[best_model_name]

    print(f"\nChampion Model Selected: {best_model_name} (R²: {best_metrics['r2_score']})")

    # Serialize artifacts
    model_path = os.path.join(artifacts_dir, "best_model.joblib")
    metrics_path = os.path.join(artifacts_dir, "model_metrics.json")
    meta_path = os.path.join(artifacts_dir, "model_meta.json")

    joblib.dump(best_pipeline, model_path)

    metadata = {
        "best_model_name": best_model_name,
        "metrics": best_metrics,
        "all_models_evaluated": results,
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "target_feature": TARGET_FEATURE,
        "training_records": len(df),
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Serialized model pipeline to {model_path}")
    print(f"Serialized model evaluation metrics to {metrics_path}")
    return metadata

if __name__ == "__main__":
    train_and_evaluate_models()
