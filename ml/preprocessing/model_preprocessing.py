from pathlib import Path
import sys

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


DATA_FILE = (
    PROJECT_ROOT
    / "ml"
    / "outputs"
    / "delivery_delay_dataset.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

TARGET = "is_delayed"

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


def prepare_model_data():

    print("Loading prepared ML dataset...")

    df = pd.read_csv(DATA_FILE)

    print(f"Dataset shape: {df.shape}")

    X = df[
        NUMERIC_FEATURES + CATEGORICAL_FEATURES
    ].copy()

    y = df[TARGET].copy()

    print("\nFeature matrix:", X.shape)
    print("Target:", y.shape)

    print("\nTarget distribution:")
    print(y.value_counts())

    # Stratified split keeps the target proportion similar
    # in train and test datasets.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\n===== TRAIN / TEST SPLIT =====")
    print(f"Training rows: {len(X_train):,}")
    print(f"Testing rows:  {len(X_test):,}")

    print("\nTraining target distribution:")
    print(y_train.value_counts(normalize=True).round(4))

    print("\nTesting target distribution:")
    print(y_test.value_counts(normalize=True).round(4))

    # Numeric preprocessing
    numeric_transformer = StandardScaler()

    # Categorical preprocessing
    categorical_transformer = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=True,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_transformer,
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    # Fit only on training data.
    X_train_transformed = preprocessor.fit_transform(
        X_train
    )

    # Transform test data using the training-fitted transformer.
    X_test_transformed = preprocessor.transform(
        X_test
    )

    print("\n===== PREPROCESSING =====")
    print(
        "Transformed training shape:",
        X_train_transformed.shape,
    )

    print(
        "Transformed testing shape:",
        X_test_transformed.shape,
    )

    # Save split data for reproducibility.
    train_data = X_train.copy()
    train_data[TARGET] = y_train.values

    test_data = X_test.copy()
    test_data[TARGET] = y_test.values

    train_file = OUTPUT_DIR / "delivery_delay_train.csv"
    test_file = OUTPUT_DIR / "delivery_delay_test.csv"

    train_data.to_csv(train_file, index=False)
    test_data.to_csv(test_file, index=False)

    print("\nSaved:")
    print(train_file)
    print(test_file)

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_transformed,
        X_test_transformed,
    )


if __name__ == "__main__":
    prepare_model_data()
