from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

TRAIN_FILE = OUTPUT_DIR / "delivery_delay_temporal_train.csv"
TEST_FILE = OUTPUT_DIR / "delivery_delay_temporal_test.csv"

MODEL_DIR = OUTPUT_DIR / "models_temporal"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


train = pd.read_csv(TRAIN_FILE)
test = pd.read_csv(TEST_FILE)


TARGET = "is_delayed"

X_train = train.drop(
    columns=[TARGET]
)

y_train = train[TARGET]

X_test = test.drop(
    columns=[TARGET]
)

y_test = test[TARGET]


# ============================================================
# Feature Groups
# ============================================================

numeric_features = X_train.select_dtypes(
    include=["int64", "float64", "int32", "float32"]
).columns.tolist()

categorical_features = X_train.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()


print("=" * 70)
print("LOGIX - TEMPORAL MODEL PREPROCESSING")
print("=" * 70)

print(f"Train rows       : {len(X_train):,}")
print(f"Test rows        : {len(X_test):,}")
print(f"Numeric features : {len(numeric_features)}")
print(f"Categorical      : {len(categorical_features)}")


# ============================================================
# Preprocessor
# ============================================================

try:

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=True
    )

except TypeError:

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse=True
    )


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            numeric_features
        ),
        (
            "categorical",
            encoder,
            categorical_features
        ),
    ]
)


# ============================================================
# FIT ONLY ON TRAIN
# ============================================================

X_train_processed = preprocessor.fit_transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)


# ============================================================
# Save
# ============================================================

joblib.dump(
    preprocessor,
    MODEL_DIR / "temporal_preprocessor.pkl"
)

joblib.dump(
    X_train_processed,
    MODEL_DIR / "X_train_processed.pkl"
)

joblib.dump(
    X_test_processed,
    MODEL_DIR / "X_test_processed.pkl"
)

joblib.dump(
    y_train,
    MODEL_DIR / "y_train.pkl"
)

joblib.dump(
    y_test,
    MODEL_DIR / "y_test.pkl"
)


print()
print(
    f"Processed train shape : "
    f"{X_train_processed.shape}"
)

print(
    f"Processed test shape  : "
    f"{X_test_processed.shape}"
)

print()
print("✓ Temporal preprocessing complete")
print("=" * 70)