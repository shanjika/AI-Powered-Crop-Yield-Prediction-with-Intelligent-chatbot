import os
import json
import time
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from app.ml.dataset_generator import generate_tamil_nadu_agri_dataset


# ==========================================================
# FEATURES
# ==========================================================

CATEGORICAL_FEATURES = [
    "district",
    "crop",
    "pattam",
    "soil_type",
    "irrigation_type"
]

NUMERICAL_FEATURES = [
    "temperature",
    "humidity",
    "rainfall_mm",
    "soil_ph",
    "soil_n",
    "soil_p",
    "soil_k",
    "soil_ec",
    "soil_organic_carbon"
]

TARGET_FEATURE = "yield_per_acre"


# ==========================================================
# MAIN TRAINING FUNCTION
# ==========================================================

def train_and_evaluate_models():

    print("\n")
    print("=" * 80)
    print("        AI POWERED CROP YIELD PREDICTION")
    print("        MODEL TRAINING AND COMPARISON")
    print("=" * 80)


    # ======================================================
    # DIRECTORIES
    # ======================================================

    base_dir = os.path.dirname(__file__)

    artifacts_dir = os.path.join(
        base_dir,
        "artifacts"
    )

    os.makedirs(
        artifacts_dir,
        exist_ok=True
    )

    data_dir = os.path.join(
        base_dir,
        "data"
    )

    os.makedirs(
        data_dir,
        exist_ok=True
    )

    csv_path = os.path.join(
        data_dir,
        "tamil_nadu_crop_yield_dataset.csv"
    )


    # ======================================================
    # LOAD DATASET
    # ======================================================

    if os.path.exists(csv_path):

        print("\n[1] Loading existing dataset...")
        print(f"    File: {csv_path}")

        df = pd.read_csv(csv_path)

    else:

        print("\n[1] Dataset not found.")
        print("    Generating Tamil Nadu agricultural dataset...")

        df = generate_tamil_nadu_agri_dataset(
            15000
        )

        df.to_csv(
            csv_path,
            index=False
        )

        print(
            f"    Dataset saved to: {csv_path}"
        )


    # ======================================================
    # DATASET INFORMATION
    # ======================================================

    print("\n[2] Dataset Information")
    print("-" * 80)

    print(
        f"    Total records : {df.shape[0]}"
    )

    print(
        f"    Total columns : {df.shape[1]}"
    )

    print(
        f"    Target        : {TARGET_FEATURE}"
    )


    # ======================================================
    # CHECK REQUIRED COLUMNS
    # ======================================================

    required_features = (
        CATEGORICAL_FEATURES
        + NUMERICAL_FEATURES
        + [TARGET_FEATURE]
    )

    missing_columns = [
        column
        for column in required_features
        if column not in df.columns
    ]

    if missing_columns:

        print("\nERROR: Missing columns detected:")

        for column in missing_columns:
            print(f"    - {column}")

        raise ValueError(
            "Dataset does not contain all required columns."
        )


    # ======================================================
    # REMOVE MISSING TARGET VALUES
    # ======================================================

    before_rows = len(df)

    df = df.dropna(
        subset=[TARGET_FEATURE]
    )

    after_rows = len(df)

    if before_rows != after_rows:

        print(
            f"\nRemoved {before_rows - after_rows} "
            "rows with missing target values."
        )


    # ======================================================
    # INPUT AND TARGET
    # ======================================================

    X = df[
        CATEGORICAL_FEATURES
        + NUMERICAL_FEATURES
    ]

    y = df[
        TARGET_FEATURE
    ]


    # ======================================================
    # TRAIN / TEST SPLIT
    # ======================================================

    print("\n[3] Splitting dataset")

    print("    Training : 80%")
    print("    Testing  : 20%")

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42
    )


    print(
        f"    Training records : {len(X_train)}"
    )

    print(
        f"    Testing records  : {len(X_test)}"
    )


    # ======================================================
    # PREPROCESSING
    # ======================================================

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "num",

                StandardScaler(),

                NUMERICAL_FEATURES
            ),

            (
                "cat",

                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                ),

                CATEGORICAL_FEATURES
            )
        ]
    )


    # ======================================================
    # MACHINE LEARNING MODELS
    # ======================================================

    candidate_models = {

        "Random Forest Regressor":

            RandomForestRegressor(

                n_estimators=120,

                max_depth=20,

                random_state=42,

                n_jobs=-1
            ),


        "Gradient Boosting Regressor":

            GradientBoostingRegressor(

                n_estimators=120,

                learning_rate=0.1,

                max_depth=6,

                random_state=42
            ),


        "XGBoost Regressor":

            XGBRegressor(

                n_estimators=150,

                learning_rate=0.08,

                max_depth=6,

                random_state=42,

                n_jobs=-1,

                objective="reg:squarederror"
            )
    }


    # ======================================================
    # STORAGE
    # ======================================================

    results = {}

    trained_pipelines = {}

    predictions = {}


    # ======================================================
    # MODEL TRAINING
    # ======================================================

    print("\n")
    print("=" * 80)
    print("              MODEL TRAINING STARTED")
    print("=" * 80)


    for name, model in candidate_models.items():

        print("\n")
        print("-" * 80)

        print(
            f"Training: {name}"
        )

        print("-" * 80)


        # Create pipeline

        pipeline = Pipeline(

            steps=[

                (
                    "preprocessor",
                    preprocessor
                ),

                (
                    "regressor",
                    model
                )
            ]
        )


        # Training start time

        start_time = time.time()


        # Train

        pipeline.fit(
            X_train,
            y_train
        )


        # Training duration

        train_duration = round(
            time.time() - start_time,
            2
        )


        # Prediction

        y_pred = pipeline.predict(
            X_test
        )


        # Store predictions

        predictions[name] = y_pred


        # ==================================================
        # EVALUATION
        # ==================================================

        mae = mean_absolute_error(
            y_test,
            y_pred
        )


        mse = mean_squared_error(
            y_test,
            y_pred
        )


        rmse = np.sqrt(
            mse
        )


        r2 = r2_score(
            y_test,
            y_pred
        )


        # ==================================================
        # STORE RESULTS
        # ==================================================

        results[name] = {

            "mae":
                round(
                    float(mae),
                    2
                ),

            "mse":
                round(
                    float(mse),
                    2
                ),

            "rmse":
                round(
                    float(rmse),
                    2
                ),

            "r2_score":
                round(
                    float(r2),
                    4
                ),

            "r2_percentage":
                round(
                    float(r2 * 100),
                    2
                ),

            "training_time_seconds":
                train_duration
        }


        trained_pipelines[name] = pipeline


        # ==================================================
        # TERMINAL RESULT
        # ==================================================

        print(
            f"R² Score  : {r2:.4f}"
        )

        print(
            f"R²        : {r2 * 100:.2f}%"
        )

        print(
            f"MAE       : {mae:.2f} kg/acre"
        )

        print(
            f"RMSE      : {rmse:.2f} kg/acre"
        )

        print(
            f"Train Time: {train_duration} seconds"
        )


    # ==========================================================
    # MODEL COMPARISON TABLE
    # ==========================================================

    results_df = pd.DataFrame(
        results
    ).T


    print("\n")
    print("=" * 100)
    print("                         MODEL COMPARISON")
    print("=" * 100)


    comparison_display = results_df[
        [
            "mae",
            "rmse",
            "r2_score",
            "r2_percentage",
            "training_time_seconds"
        ]
    ].copy()


    comparison_display.columns = [

        "MAE (kg/acre)",

        "RMSE (kg/acre)",

        "R² Score",

        "R² (%)",

        "Training Time (sec)"
    ]


    print(
        comparison_display.to_string()
    )


    print("=" * 100)


    # ==========================================================
    # SELECT BEST MODEL
    # ==========================================================

    best_model_name = max(

        results,

        key=lambda model_name:
        results[model_name]["r2_score"]
    )


    best_pipeline = trained_pipelines[
        best_model_name
    ]


    best_metrics = results[
        best_model_name
    ]


    print("\n")
    print("=" * 80)

    print(
        "                 FINAL MODEL SELECTION"
    )

    print("=" * 80)


    print(
        f"Best Model : {best_model_name}"
    )

    print(
        f"R² Score   : {best_metrics['r2_score']}"
    )

    print(
        f"R²         : {best_metrics['r2_percentage']}%"
    )

    print(
        f"MAE        : {best_metrics['mae']} kg/acre"
    )

    print(
        f"RMSE       : {best_metrics['rmse']} kg/acre"
    )

    print("=" * 80)


    # ==========================================================
    # SAVE COMPARISON CSV
    # ==========================================================

    comparison_path = os.path.join(

        artifacts_dir,

        "model_comparison.csv"
    )


    results_df.to_csv(

        comparison_path
    )


    print(
        f"\nComparison CSV saved to:"
    )

    print(
        comparison_path
    )


    # ==========================================================
    # VISUALIZATION 1
    # R² SCORE COMPARISON
    # ==========================================================

    print("\nGenerating R² comparison graph...")


    plt.figure(
        figsize=(10, 6)
    )


    models = results_df.index.tolist()

    r2_values = results_df[
        "r2_score"
    ].values


    bars = plt.bar(

        models,

        r2_values
    )


    plt.title(
        "R² Score Comparison of Machine Learning Models"
    )

    plt.xlabel(
        "Machine Learning Algorithm"
    )

    plt.ylabel(
        "R² Score"
    )


    plt.ylim(
        0,
        max(
            1,
            max(r2_values) + 0.1
        )
    )


    for bar, value in zip(
        bars,
        r2_values
    ):

        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            value + 0.02,

            f"{value:.4f}",

            ha="center"
        )


    plt.xticks(
        rotation=15
    )


    plt.tight_layout()


    r2_graph_path = os.path.join(

        artifacts_dir,

        "r2_comparison.png"
    )


    plt.savefig(

        r2_graph_path,

        dpi=300,

        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    print(
        f"R² graph saved to:"
    )

    print(
        r2_graph_path
    )


    # ==========================================================
    # VISUALIZATION 2
    # MAE AND RMSE COMPARISON
    # ==========================================================

    print(
        "\nGenerating error comparison graph..."
    )


    plt.figure(
        figsize=(10, 6)
    )


    x = np.arange(
        len(models)
    )


    width = 0.35


    mae_values = results_df[
        "mae"
    ].values


    rmse_values = results_df[
        "rmse"
    ].values


    plt.bar(

        x - width / 2,

        mae_values,

        width,

        label="MAE"
    )


    plt.bar(

        x + width / 2,

        rmse_values,

        width,

        label="RMSE"
    )


    plt.title(
        "MAE and RMSE Comparison"
    )

    plt.xlabel(
        "Machine Learning Algorithm"
    )

    plt.ylabel(
        "Error (kg/acre)"
    )


    plt.xticks(

        x,

        models,

        rotation=15
    )


    plt.legend()


    plt.tight_layout()


    error_graph_path = os.path.join(

        artifacts_dir,

        "error_comparison.png"
    )


    plt.savefig(

        error_graph_path,

        dpi=300,

        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    print(
        f"Error graph saved to:"
    )

    print(
        error_graph_path
    )


    # ==========================================================
    # VISUALIZATION 3
    # ACTUAL VS PREDICTED
    # ==========================================================

    print(
        "\nGenerating actual vs predicted graph..."
    )


    best_predictions = predictions[
        best_model_name
    ]


    plt.figure(
        figsize=(8, 6)
    )


    plt.scatter(

        y_test,

        best_predictions,

        alpha=0.5
    )


    min_value = min(

        y_test.min(),

        best_predictions.min()
    )


    max_value = max(

        y_test.max(),

        best_predictions.max()
    )


    # Perfect prediction line

    plt.plot(

        [min_value, max_value],

        [min_value, max_value],

        linestyle="--"
    )


    plt.title(

        f"Actual vs Predicted Yield\n"
        f"{best_model_name}"
    )


    plt.xlabel(
        "Actual Yield (kg/acre)"
    )


    plt.ylabel(
        "Predicted Yield (kg/acre)"
    )


    plt.tight_layout()


    actual_predicted_path = os.path.join(

        artifacts_dir,

        "actual_vs_predicted.png"
    )


    plt.savefig(

        actual_predicted_path,

        dpi=300,

        bbox_inches="tight"
    )


    plt.show()

    plt.close()


    print(
        f"Actual vs Predicted graph saved to:"
    )

    print(
        actual_predicted_path
    )


    # ==========================================================
    # SAVE BEST MODEL
    # ==========================================================

    model_path = os.path.join(

        artifacts_dir,

        "best_model.joblib"
    )


    joblib.dump(

        best_pipeline,

        model_path
    )


    print(
        f"\nBest model saved to:"
    )

    print(
        model_path
    )


    # ==========================================================
    # SAVE METADATA
    # ==========================================================

    metadata = {

        "best_model_name":
            best_model_name,

        "metrics":
            best_metrics,

        "all_models_evaluated":
            results,

        "categorical_features":
            CATEGORICAL_FEATURES,

        "numerical_features":
            NUMERICAL_FEATURES,

        "target_feature":
            TARGET_FEATURE,

        "training_records":
            len(df),

        "testing_records":
            len(X_test),

        "trained_at":
            time.strftime(
                "%Y-%m-%d %H:%M:%S UTC",
                time.gmtime()
            )
    }


    metrics_path = os.path.join(

        artifacts_dir,

        "model_metrics.json"
    )


    with open(

        metrics_path,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            metadata,

            f,

            indent=2
        )


    print(
        f"Model metrics saved to:"
    )

    print(
        metrics_path
    )


    # ==========================================================
    # FINAL SUMMARY
    # ==========================================================

    print("\n")
    print("=" * 80)
    print("                    TRAINING COMPLETED")
    print("=" * 80)

    print(
        f"Final Algorithm : {best_model_name}"
    )

    print(
        f"R² Score        : {best_metrics['r2_score']}"
    )

    print(
        f"R² Percentage   : {best_metrics['r2_percentage']}%"
    )

    print(
        f"MAE             : {best_metrics['mae']} kg/acre"
    )

    print(
        f"RMSE            : {best_metrics['rmse']} kg/acre"
    )

    print("\nGenerated Files:")

    print(
        "1. model_comparison.csv"
    )

    print(
        "2. r2_comparison.png"
    )

    print(
        "3. error_comparison.png"
    )

    print(
        "4. actual_vs_predicted.png"
    )

    print(
        "5. best_model.joblib"
    )

    print(
        "6. model_metrics.json"
    )

    print("=" * 80)


    return metadata


# ==========================================================
# RUN PROGRAM
# ==========================================================

if __name__ == "__main__":

    train_and_evaluate_models()