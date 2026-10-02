"""
LOGIX - Delivery Delay Prediction
Model Training Pipeline

Models:
1. Logistic Regression
2. Decision Tree
3. Random Forest

Evaluation:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

TRAIN_FILE = OUTPUT_DIR / "delivery_delay_train.csv"
TEST_FILE = OUTPUT_DIR / "delivery_delay_test.csv"

MODEL_DIR = OUTPUT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

RESULT_FILE = OUTPUT_DIR / "delivery_delay_model_results.csv"


# ============================================================
# FEATURES
# ============================================================

NUMERIC_FEATURES = [
    "distance_km",
    "shipping_cost",
    "sla_days",
    "processing_days",
    "order_month",
    "order_day_of_week",
    "shipment_day_of_week",
]

CATEGORICAL_FEATURES = [
    "delivery_type",
    "priority",
    "warehouse_id",
    "delivery_partner_id",
]

TARGET_COLUMN = "is_delayed"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOGIX - DELIVERY DELAY PREDICTION")
print("MODEL TRAINING")
print("=" * 70)

print("\n📂 Loading training and testing datasets...")

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

print(f"✅ Training dataset: {train_df.shape}")
print(f"✅ Testing dataset : {test_df.shape}")


# ============================================================
# SPLIT FEATURES / TARGET
# ============================================================

X_train = train_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y_train = train_df[TARGET_COLUMN]

X_test = test_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y_test = test_df[TARGET_COLUMN]

print("\n🎯 Target distribution - Training:")
print(y_train.value_counts())

print("\n🎯 Target distribution - Testing:")
print(y_test.value_counts())


# ============================================================
# PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=True,
            ),
            CATEGORICAL_FEATURES,
        ),
    ]
)


# ============================================================
# MODELS
# ============================================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42,
    ),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=12,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
    ),
}


# ============================================================
# TRAIN + EVALUATE
# ============================================================

results = []

for model_name, model in models.items():

    print("\n" + "=" * 70)
    print(f"🤖 Training: {model_name}")
    print("=" * 70)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    # Train
    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Probability for ROC-AUC
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )
    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )
    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )
    roc_auc = roc_auc_score(
        y_test,
        y_proba,
    )

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")

    # Save model
    model_filename = (
        model_name.lower()
        .replace(" ", "_")
        + ".joblib"
    )

    model_path = MODEL_DIR / model_filename

    joblib.dump(
        pipeline,
        model_path,
    )

    print(f"💾 Model saved: {model_path}")

    results.append(
        {
            "model": model_name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc,
        }
    )


# ============================================================
# SAVE RESULTS
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="roc_auc",
    ascending=False,
)

results_df.to_csv(
    RESULT_FILE,
    index=False,
)

print("\n" + "=" * 70)
print("📊 MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)

print("\n" + "=" * 70)
print("✅ MODEL TRAINING COMPLETED")
print("=" * 70)

print(f"\n📄 Results saved:")
print(RESULT_FILE)

print(f"\n📁 Models saved in:")
print(MODEL_DIR)