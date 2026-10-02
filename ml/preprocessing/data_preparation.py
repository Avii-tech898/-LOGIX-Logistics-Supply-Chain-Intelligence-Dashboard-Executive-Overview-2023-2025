from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ml.config.ml_config import (
    ORDERS_FILE,
    SHIPMENTS_FILE,
    OUTPUT_DIR,
    TARGET_COLUMN,
    MODEL_FEATURES,
)


def load_data():
    orders = pd.read_csv(ORDERS_FILE)
    shipments = pd.read_csv(SHIPMENTS_FILE)

    return orders, shipments


def prepare_delivery_delay_dataset():
    orders, shipments = load_data()

    print("Loading LOGIX data...")
    print(f"Orders: {len(orders):,}")
    print(f"Shipments: {len(shipments):,}")

    # Convert dates
    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    shipments["shipment_date"] = pd.to_datetime(
        shipments["shipment_date"],
        errors="coerce"
    )

    shipments["expected_delivery_date"] = pd.to_datetime(
        shipments["expected_delivery_date"],
        errors="coerce"
    )

    shipments["actual_delivery_date"] = pd.to_datetime(
        shipments["actual_delivery_date"],
        errors="coerce"
    )

    # Select only order information that is useful before delivery.
    order_features = orders[
        [
            "order_id",
            "order_date",
            "priority",
        ]
    ].copy()

    # Merge shipment and order information.
    # delivery_type is intentionally taken from shipments because
    # shipment-level delivery_type already exists there.
    df = shipments.merge(
        order_features,
        on="order_id",
        how="left",
    )

    # A supervised delay target requires an actual delivery date.
    # Undelivered shipments cannot reliably provide an on-time/late label.
    df = df[
        df["actual_delivery_date"].notna()
        & df["expected_delivery_date"].notna()
    ].copy()

    # Target:
    # 1 = delivered after expected delivery date
    # 0 = delivered on or before expected delivery date
    df[TARGET_COLUMN] = (
        df["actual_delivery_date"] > df["expected_delivery_date"]
    ).astype(int)

    # Date-based features
    df["order_month"] = df["order_date"].dt.month
    df["order_day_of_week"] = df["order_date"].dt.dayofweek
    df["shipment_day_of_week"] = df["shipment_date"].dt.dayofweek

    # Processing time available before shipment.
    df["processing_days"] = (
        df["shipment_date"] - df["order_date"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Remove impossible date relationships.
    df = df[df["processing_days"] >= 0].copy()

    # Check required columns.
    required_columns = MODEL_FEATURES + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    model_df = df[required_columns].copy()

    # Remove incomplete feature rows.
    model_df = model_df.dropna().reset_index(drop=True)

    # Categorical features
    categorical_columns = [
        "delivery_type",
        "priority",
        "warehouse_id",
        "delivery_partner_id",
    ]

    for column in categorical_columns:
        model_df[column] = model_df[column].astype(str)

    # Numeric safety
    numeric_columns = [
        "distance_km",
        "shipping_cost",
        "sla_days",
        "processing_days",
        "order_month",
        "order_day_of_week",
        "shipment_day_of_week",
    ]

    for column in numeric_columns:
        model_df[column] = pd.to_numeric(
            model_df[column],
            errors="coerce"
        )

    model_df = model_df.dropna().reset_index(drop=True)

    # Save prepared dataset
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "delivery_delay_dataset.csv"
    model_df.to_csv(output_file, index=False)

    print("\n===== DELIVERY DELAY DATASET =====")
    print(f"Prepared rows: {len(model_df):,}")
    print(f"Features: {len(MODEL_FEATURES)}")
    print(f"Target: {TARGET_COLUMN}")

    print("\nColumns:")
    print(model_df.columns.tolist())

    print("\nTarget distribution:")
    print(model_df[TARGET_COLUMN].value_counts().sort_index())

    print("\nTarget percentage:")
    print(
        model_df[TARGET_COLUMN]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    print("\nMissing values:")
    print(model_df.isna().sum())

    print("\nSaved to:")
    print(output_file)

    return model_df


if __name__ == "__main__":
    prepare_delivery_delay_dataset()
