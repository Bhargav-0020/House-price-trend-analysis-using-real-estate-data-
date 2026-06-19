"""Train and save all house price prediction models."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

MODEL_DIR = Path("model")
FEATURES = [
    "area",
    "bedrooms",
    "bathrooms",
    "stories",
    "parking",
    "mainroad",
    "guestroom",
    "basement",
    "hotwaterheating",
    "airconditioning",
    "location",
]

MODEL_LABELS = {
    "linear_regression": "Linear Regression",
    "random_forest": "Random Forest",
    "gradient_boosting": "Gradient Boosting",
    "decision_tree": "Decision Tree",
}


def prepare_data():
    df = pd.read_csv("dataset/housing.csv")

    binary_cols = [
        "mainroad",
        "guestroom",
        "basement",
        "hotwaterheating",
        "airconditioning",
    ]
    for col in binary_cols:
        df[col] = df[col].map({"yes": 1, "no": 0})

    df["location"] = df["location"].map({"Rural": 0, "Semi-Urban": 1, "Urban": 2})

    x = df[FEATURES]
    y = df["price"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    return x_train_scaled, x_test_scaled, y_train, y_test, scaler


def build_models():
    """Train all models in memory. Safe across Python/sklearn versions."""
    x_train, x_test, y_train, y_test, scaler = prepare_data()

    model_defs = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=200, random_state=42, max_depth=8
        ),
        "gradient_boosting": GradientBoostingRegressor(
            n_estimators=200, random_state=42, max_depth=4
        ),
        "decision_tree": DecisionTreeRegressor(random_state=42, max_depth=8),
    }

    models = {}
    metrics = {}

    for name, model in model_defs.items():
        model.fit(x_train, y_train)
        models[name] = model
        predictions = model.predict(x_test)
        metrics[name] = {
            "r2": round(float(r2_score(y_test, predictions)), 4),
            "mae": round(float(mean_absolute_error(y_test, predictions)), 2),
        }

    return models, scaler, metrics


def train_and_save():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    models, scaler, metrics = build_models()

    for name, model in models.items():
        joblib.dump(model, MODEL_DIR / f"{name}.pkl")

    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    joblib.dump(models["linear_regression"], MODEL_DIR / "model.pkl")

    with (MODEL_DIR / "model_metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print("Models trained and saved:")
    for name, scores in metrics.items():
        print(f"  {name}: R2={scores['r2']}, MAE={scores['mae']}")


if __name__ == "__main__":
    train_and_save()
