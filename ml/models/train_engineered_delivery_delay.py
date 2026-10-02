"""
LOGIX - Engineered Delivery Delay Prediction
Phase 4: Engineered Model Training

Models:
1. Logistic Regression
2. Decision Tree
3. Random Forest

Purpose:
Compare engineered feature performance against
the original baseline models.

Baseline model files are NOT modified.
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

TRAIN_FILE = (
    OUTPUT_DIR
    / "delivery_delay_engineered_train.csv"
)

TEST_FILE = (
    OUTPUT_DIR
    / "delivery_delay_engineered_test.csv"
)

MODEL_DIR = (
    OUTPUT_DIR
    / "models_engineered"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

RESULT_FILE = (
    OUTPUT_DIR
    / "engineered_delivery_delay_model_results.csv"
)


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
    "distance_per_sla_day",
    "shipping_cost_per_km",
    "processing_to_sla_ratio",
    "sla_buffer_days",
    "is_express",
    "is_same_day",
    "is_high_priority",
    "order_month_sin",
    "order_month_cos",
    "order_day_sin",
    "order_day_cos",
    "shipment_day_sin",
    "shipment_day_cos",
    "warehouse_prior_delay_rate",
    "partner_prior_delay_rate",
    "warehouse_prior_shipments",
    "partner_prior_shipments",
    "historical_operational_risk",
    "network_distance_pressure",
]

CATEGORICAL_FEATURES = [
    "delivery_type",
    "priority",
    "warehouse_id",
    "delivery_partner_id",
]

TARGET = "is_delayed"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOGIX - ENGINEERED DELIVERY DELAY PREDICTION")
print("PHASE 4: ENGINEERED MODEL TRAINING")
print("=" * 70)

print("\n📂 Loading engineered train/test datasets...")

train_df = pd.read_csv(
    TRAIN_FILE
)

test_df = pd.read_csv(
    TEST_FILE
)

print(
    f"Training dataset: {train_df.shape}"
)

print(
    f"Testing dataset : {test_df.shape}"
)


# ============================================================
# VALIDATE COLUMNS
# ============================================================

required_columns = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
    + [TARGET]
)

missing_train = [
    column
    for column in required_columns
    if column not in train_df.columns
]

missing_test = [
    column
    for column in required_columns
    if column not in test_df.columns
]

if missing_train:
    raise ValueError(
        f"Missing training columns: {missing_train}"
    )

if missing_test:
    raise ValueError(
        f"Missing testing columns: {missing_test}"
    )


# ============================================================
# X / Y
# ============================================================

feature_columns = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)

X_train = train_df[
    feature_columns
].copy()

y_train = train_df[
    TARGET
].copy()

X_test = test_df[
    feature_columns
].copy()

y_test = test_df[
    TARGET
].copy()


# ============================================================
# PREPROCESSOR
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

    print(
        f"🤖 Training engineered model: "
        f"{model_name}"
    )

    print("=" * 70)

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    # --------------------------------------------------------
    # TRAIN
    # --------------------------------------------------------

    pipeline.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------------
    # PREDICTIONS
    # --------------------------------------------------------

    y_pred = pipeline.predict(
        X_test
    )

    y_proba = pipeline.predict_proba(
        X_test
    )[:, 1]

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

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

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1-Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )

    # --------------------------------------------------------
    # SAVE MODEL
    # --------------------------------------------------------

    model_filename = (
        model_name
        .lower()
        .replace(" ", "_")
        + "_engineered.joblib"
    )

    model_path = (
        MODEL_DIR
        / model_filename
    )

    joblib.dump(
        pipeline,
        model_path,
    )

    print(
        f"💾 Saved: {model_path}"
    )

    # --------------------------------------------------------
    # STORE RESULTS
    # --------------------------------------------------------

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
# RESULTS TABLE
# ============================================================

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    by="roc_auc",
    ascending=False,
)

results_df.to_csv(
    RESULT_FILE,
    index=False,
)


# ============================================================
# DISPLAY COMPARISON
# ============================================================

print("\n" + "=" * 70)
print("📊 ENGINEERED MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("✅ ENGINEERED MODEL TRAINING COMPLETED")
print("=" * 70)

print(
    f"\n📄 Results:"
)

print(
    RESULT_FILE
)

print(
    f"\n📁 Models:"
)

print(
    MODEL_DIR
)

print(
    "\n🔒 Original baseline models were NOT modified."
)