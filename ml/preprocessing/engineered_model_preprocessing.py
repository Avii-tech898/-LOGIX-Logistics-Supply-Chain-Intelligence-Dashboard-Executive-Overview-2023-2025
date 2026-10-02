"""
LOGIX - Engineered Delivery Delay Model Preprocessing
Phase 3

Creates leakage-safe train/test datasets from:
delivery_delay_engineered.csv
"""

from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

INPUT_FILE = (
    OUTPUT_DIR / "delivery_delay_engineered.csv"
)

TRAIN_FILE = (
    OUTPUT_DIR / "delivery_delay_engineered_train.csv"
)

TEST_FILE = (
    OUTPUT_DIR / "delivery_delay_engineered_test.csv"
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
# LOAD
# ============================================================

print("=" * 70)
print("LOGIX - ENGINEERED MODEL PREPROCESSING")
print("=" * 70)

print("\n📂 Loading engineered dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset shape: {df.shape}"
)


# ============================================================
# VALIDATE COLUMNS
# ============================================================

required_columns = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
    + [TARGET]
)

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:

    raise ValueError(
        f"Missing columns: {missing}"
    )


# ============================================================
# FEATURES / TARGET
# ============================================================

X = df[
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
].copy()

y = df[TARGET].copy()


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n✂️ Creating train/test split...")

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )
)


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
# FIT ONLY ON TRAIN
# ============================================================

print(
    "\n⚙️ Fitting preprocessing on training data only..."
)

X_train_transformed = (
    preprocessor.fit_transform(X_train)
)

X_test_transformed = (
    preprocessor.transform(X_test)
)


# ============================================================
# SAVE RAW TRAIN / TEST DATA
# ============================================================

train_output = X_train.copy()
train_output[TARGET] = y_train.values

test_output = X_test.copy()
test_output[TARGET] = y_test.values

train_output.to_csv(
    TRAIN_FILE,
    index=False,
)

test_output.to_csv(
    TEST_FILE,
    index=False,
)


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PREPROCESSING SUMMARY")
print("=" * 70)

print(
    f"Original dataset : {len(df):,}"
)

print(
    f"Training records : {len(X_train):,}"
)

print(
    f"Testing records  : {len(X_test):,}"
)

print(
    f"Training target distribution:"
)

print(
    y_train.value_counts()
    .sort_index()
)

print(
    f"\nTesting target distribution:"
)

print(
    y_test.value_counts()
    .sort_index()
)

print(
    f"\nNumeric features     : "
    f"{len(NUMERIC_FEATURES)}"
)

print(
    f"Categorical features : "
    f"{len(CATEGORICAL_FEATURES)}"
)

print(
    f"Transformed train shape: "
    f"{X_train_transformed.shape}"
)

print(
    f"Transformed test shape : "
    f"{X_test_transformed.shape}"
)

print("\n" + "=" * 70)
print("✅ ENGINEERED PREPROCESSING COMPLETED")
print("=" * 70)

print(
    f"\n📄 Train file:\n{TRAIN_FILE}"
)

print(
    f"\n📄 Test file:\n{TEST_FILE}"
)

print(
    "\n🔒 Baseline dataset untouched."
)

print(
    "🔒 Baseline models untouched."
)