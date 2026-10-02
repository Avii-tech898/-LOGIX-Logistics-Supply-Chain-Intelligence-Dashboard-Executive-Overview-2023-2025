from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# LOGIX - Phase 5
# Time-Aware Delivery Delay Dataset Builder
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

ORDERS_FILE = DATA_DIR / "orders.csv"
SHIPMENTS_FILE = DATA_DIR / "shipments.csv"
WAREHOUSES_FILE = DATA_DIR / "warehouses.csv"
PARTNERS_FILE = DATA_DIR / "delivery_partners.csv"

OUTPUT_FULL = OUTPUT_DIR / "delivery_delay_temporal_dataset.csv"
OUTPUT_TRAIN = OUTPUT_DIR / "delivery_delay_temporal_train.csv"
OUTPUT_TEST = OUTPUT_DIR / "delivery_delay_temporal_test.csv"

RANDOM_STATE = 42


# ============================================================
# Utility
# ============================================================

def safe_divide(a, b, default=0.0):
    result = np.where(b != 0, a / b, default)
    return result


# ============================================================
# Load Data
# ============================================================

print("=" * 70)
print("LOGIX - TIME-AWARE DELIVERY DELAY DATASET")
print("=" * 70)

orders = pd.read_csv(ORDERS_FILE)
shipments = pd.read_csv(SHIPMENTS_FILE)
warehouses = pd.read_csv(WAREHOUSES_FILE)
partners = pd.read_csv(PARTNERS_FILE)

print(f"Orders loaded       : {len(orders):,}")
print(f"Shipments loaded    : {len(shipments):,}")
print(f"Warehouses loaded   : {len(warehouses):,}")
print(f"Partners loaded     : {len(partners):,}")


# ============================================================
# Date Conversion
# ============================================================

date_columns_orders = [
    "order_date",
    "expected_delivery_date",
]

date_columns_shipments = [
    "shipment_date",
    "expected_delivery_date",
    "actual_delivery_date",
]

for col in date_columns_orders:
    if col in orders.columns:
        orders[col] = pd.to_datetime(
            orders[col],
            errors="coerce"
        )

for col in date_columns_shipments:
    if col in shipments.columns:
        shipments[col] = pd.to_datetime(
            shipments[col],
            errors="coerce"
        )


# ============================================================
# Keep only required order-level information
# ============================================================

orders_small = orders[
    [
        "order_id",
        "order_date",
        "priority",
    ]
].copy()


# ============================================================
# Merge Orders + Shipments
# ============================================================

df = shipments.merge(
    orders_small,
    on="order_id",
    how="inner",
    validate="one_to_one"
)

print(f"Merged records      : {len(df):,}")


# ============================================================
# Target Preparation
# ============================================================

required_dates = [
    "order_date",
    "shipment_date",
    "expected_delivery_date",
    "actual_delivery_date",
]

before_date_filter = len(df)

df = df.dropna(
    subset=required_dates
).copy()

print(
    f"Removed missing-date rows : "
    f"{before_date_filter - len(df):,}"
)


# ============================================================
# Processing Time
# ============================================================

df["processing_days"] = (
    df["shipment_date"] - df["order_date"]
).dt.days


# ============================================================
# Data Quality Rule
# ============================================================
# Shipment cannot happen before order.
# Invalid records are removed instead of clipped.

invalid_processing = (
    df["processing_days"] < 0
).sum()

print(
    f"Invalid processing rows    : "
    f"{invalid_processing:,}"
)

df = df[
    df["processing_days"] >= 0
].copy()

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# LOGIX - PHASE 5
# TIME-AWARE DELIVERY DELAY DATASET
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

ORDERS_FILE = DATA_DIR / "orders.csv"
SHIPMENTS_FILE = DATA_DIR / "shipments.csv"
WAREHOUSES_FILE = DATA_DIR / "warehouses.csv"
PARTNERS_FILE = DATA_DIR / "delivery_partners.csv"

TRAIN_FILE = OUTPUT_DIR / "delivery_delay_temporal_train.csv"
TEST_FILE = OUTPUT_DIR / "delivery_delay_temporal_test.csv"
FULL_FILE = OUTPUT_DIR / "delivery_delay_temporal_dataset.csv"

RANDOM_STATE = 42


def safe_divide(a, b, default=0.0):
    return np.where(
        b != 0,
        a / b,
        default
    )


print("=" * 70)
print("LOGIX - TIME-AWARE DELIVERY DELAY DATASET")
print("=" * 70)


# ============================================================
# LOAD
# ============================================================

orders = pd.read_csv(ORDERS_FILE)
shipments = pd.read_csv(SHIPMENTS_FILE)
warehouses = pd.read_csv(WAREHOUSES_FILE)
partners = pd.read_csv(PARTNERS_FILE)

print(f"Orders loaded       : {len(orders):,}")
print(f"Shipments loaded    : {len(shipments):,}")
print(f"Warehouses loaded   : {len(warehouses):,}")
print(f"Partners loaded     : {len(partners):,}")


# ============================================================
# DATE CONVERSION
# ============================================================

for col in [
    "order_date",
    "expected_delivery_date",
]:
    orders[col] = pd.to_datetime(
        orders[col],
        errors="coerce"
    )

for col in [
    "shipment_date",
    "expected_delivery_date",
    "actual_delivery_date",
]:
    shipments[col] = pd.to_datetime(
        shipments[col],
        errors="coerce"
    )


# ============================================================
# ORDER INFORMATION
# ============================================================

orders_small = orders[
    [
        "order_id",
        "order_date",
        "priority",
    ]
].copy()


# ============================================================
# MERGE
# ============================================================

df = shipments.merge(
    orders_small,
    on="order_id",
    how="inner",
    validate="one_to_one"
)

print(f"Merged records      : {len(df):,}")


# ============================================================
# VALID DATE RECORDS
# ============================================================

required_dates = [
    "order_date",
    "shipment_date",
    "expected_delivery_date",
    "actual_delivery_date",
]

before = len(df)

df = df.dropna(
    subset=required_dates
).copy()

print(
    f"Removed missing-date rows : "
    f"{before - len(df):,}"
)


# ============================================================
# PROCESSING DAYS
# ============================================================

df["processing_days"] = (
    df["shipment_date"] -
    df["order_date"]
).dt.days


invalid_processing = (
    df["processing_days"] < 0
).sum()

print(
    f"Invalid processing rows    : "
    f"{invalid_processing:,}"
)

# Do NOT clip invalid values.
# Remove them because they represent impossible chronology.

df = df[
    df["processing_days"] >= 0
].copy()


# ============================================================
# TARGET
# ============================================================

df["is_delayed"] = (
    df["actual_delivery_date"] >
    df["expected_delivery_date"]
).astype(int)


# ============================================================
# CALENDAR FEATURES
# ============================================================

df["order_month"] = (
    df["order_date"].dt.month
)

df["order_day_of_week"] = (
    df["order_date"].dt.dayofweek
)

df["shipment_day_of_week"] = (
    df["shipment_date"].dt.dayofweek
)

df["shipment_month"] = (
    df["shipment_date"].dt.month
)

df["shipment_day_of_month"] = (
    df["shipment_date"].dt.day
)

df["shipment_week_of_year"] = (
    df["shipment_date"]
    .dt.isocalendar()
    .week
    .astype(int)
)

df["is_weekend_shipment"] = (
    df["shipment_day_of_week"] >= 5
).astype(int)


# ============================================================
# OPERATIONAL FEATURES
# ============================================================

df["distance_per_sla_day"] = safe_divide(
    df["distance_km"],
    df["sla_days"]
)

df["shipping_cost_per_km"] = safe_divide(
    df["shipping_cost"],
    df["distance_km"]
)

df["processing_to_sla_ratio"] = safe_divide(
    df["processing_days"],
    df["sla_days"]
)

df["sla_buffer_days"] = (
    df["sla_days"] -
    df["processing_days"]
)

df["is_express"] = (
    df["delivery_type"]
    .astype(str)
    .str.lower()
    .eq("express")
    .astype(int)
)

df["is_same_day"] = (
    df["delivery_type"]
    .astype(str)
    .str.lower()
    .eq("same day")
    .astype(int)
)

df["is_high_priority"] = (
    df["priority"]
    .astype(str)
    .str.lower()
    .eq("high")
    .astype(int)
)


# ============================================================
# WAREHOUSE ENRICHMENT
# ============================================================

warehouse_cols = [
    "warehouse_id",
    "warehouse_type",
    "capacity_units",
    "is_active",
]

warehouse_cols = [
    c for c in warehouse_cols
    if c in warehouses.columns
]

warehouse_info = (
    warehouses[warehouse_cols]
    .drop_duplicates("warehouse_id")
)

df = df.merge(
    warehouse_info,
    on="warehouse_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# PARTNER ENRICHMENT
# ============================================================

partner_cols = [
    "partner_id",
    "service_type",
    "coverage_type",
    "base_cost_per_km",
    "rating",
    "status",
]

partner_cols = [
    c for c in partner_cols
    if c in partners.columns
]

partner_info = (
    partners[partner_cols]
    .drop_duplicates("partner_id")
    .rename(
        columns={
            "partner_id": "delivery_partner_id",
            "service_type": "partner_service_type",
            "coverage_type": "partner_coverage_type",
            "base_cost_per_km":
                "partner_base_cost_per_km",
            "rating": "partner_rating",
            "status": "partner_status",
        }
    )
)

df = df.merge(
    partner_info,
    on="delivery_partner_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# CHRONOLOGICAL SORT
# ============================================================

df = df.sort_values(
    [
        "shipment_date",
        "shipment_id",
    ]
).reset_index(drop=True)


# ============================================================
# TEMPORAL SPLIT
# ============================================================

unique_dates = (
    df["shipment_date"]
    .dt.normalize()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

cutoff_index = (
    int(len(unique_dates) * 0.80) - 1
)

cutoff_date = unique_dates.iloc[
    cutoff_index
]

train_mask = (
    df["shipment_date"].dt.normalize()
    <= cutoff_date
)

test_mask = ~train_mask

train = df.loc[train_mask].copy()
test = df.loc[test_mask].copy()

print()
print("-" * 70)
print("TEMPORAL SPLIT")
print("-" * 70)

print(
    f"Unique shipment dates : "
    f"{len(unique_dates):,}"
)

print(
    f"Cutoff date           : "
    f"{cutoff_date.date()}"
)

print(
    f"Train rows            : "
    f"{len(train):,}"
)

print(
    f"Test rows             : "
    f"{len(test):,}"
)


# ============================================================
# GLOBAL TRAINING RATE
# ============================================================

global_delay_rate = (
    train["is_delayed"].mean()
)


# ============================================================
# TRAIN HISTORICAL WAREHOUSE FEATURES
# ============================================================

train["_date"] = (
    train["shipment_date"].dt.normalize()
)

warehouse_daily = (
    train
    .groupby(
        ["_date", "warehouse_id"],
        observed=True
    )
    .agg(
        daily_delayed=(
            "is_delayed",
            "sum"
        ),
        daily_shipments=(
            "is_delayed",
            "count"
        ),
    )
    .reset_index()
    .sort_values(
        [
            "warehouse_id",
            "_date",
        ]
    )
)

warehouse_daily["prior_delayed"] = (
    warehouse_daily
    .groupby("warehouse_id")
    ["daily_delayed"]
    .cumsum()
    - warehouse_daily["daily_delayed"]
)

warehouse_daily["prior_shipments"] = (
    warehouse_daily
    .groupby("warehouse_id")
    ["daily_shipments"]
    .cumsum()
    - warehouse_daily["daily_shipments"]
)

warehouse_daily[
    "warehouse_prior_delay_rate"
] = safe_divide(
    warehouse_daily["prior_delayed"],
    warehouse_daily["prior_shipments"],
    global_delay_rate
)

warehouse_history = warehouse_daily[
    [
        "_date",
        "warehouse_id",
        "warehouse_prior_delay_rate",
        "prior_shipments",
    ]
]

train = train.merge(
    warehouse_history,
    on=["_date", "warehouse_id"],
    how="left"
)

train[
    "warehouse_prior_delay_rate"
] = train[
    "warehouse_prior_delay_rate"
].fillna(global_delay_rate)

train["prior_shipments"] = (
    train["prior_shipments"]
    .fillna(0)
)


# ============================================================
# TRAIN HISTORICAL PARTNER FEATURES
# ============================================================

partner_daily = (
    train
    .groupby(
        ["_date", "delivery_partner_id"],
        observed=True
    )
    .agg(
        daily_delayed=(
            "is_delayed",
            "sum"
        ),
        daily_shipments=(
            "is_delayed",
            "count"
        ),
    )
    .reset_index()
    .sort_values(
        [
            "delivery_partner_id",
            "_date",
        ]
    )
)

partner_daily["prior_delayed"] = (
    partner_daily
    .groupby("delivery_partner_id")
    ["daily_delayed"]
    .cumsum()
    - partner_daily["daily_delayed"]
)

partner_daily["prior_shipments"] = (
    partner_daily
    .groupby("delivery_partner_id")
    ["daily_shipments"]
    .cumsum()
    - partner_daily["daily_shipments"]
)

partner_daily[
    "partner_prior_delay_rate"
] = safe_divide(
    partner_daily["prior_delayed"],
    partner_daily["prior_shipments"],
    global_delay_rate
)

partner_history = partner_daily[
    [
        "_date",
        "delivery_partner_id",
        "partner_prior_delay_rate",
        "prior_shipments",
    ]
].rename(
    columns={
        "prior_shipments":
            "partner_prior_shipments"
    }
)

train = train.merge(
    partner_history,
    on=[
        "_date",
        "delivery_partner_id"
    ],
    how="left"
)

train[
    "partner_prior_delay_rate"
] = train[
    "partner_prior_delay_rate"
].fillna(global_delay_rate)

train["partner_prior_shipments"] = (
    train["partner_prior_shipments"]
    .fillna(0)
)


# ============================================================
# FROZEN TRAIN HISTORY FOR TEST
# ============================================================

warehouse_train_history = (
    train
    .groupby("warehouse_id")
    .agg(
        delayed=(
            "is_delayed",
            "sum"
        ),
        shipments=(
            "is_delayed",
            "count"
        ),
    )
    .reset_index()
)

warehouse_train_history[
    "warehouse_prior_delay_rate"
] = safe_divide(
    warehouse_train_history["delayed"],
    warehouse_train_history["shipments"],
    global_delay_rate
)

warehouse_train_history = (
    warehouse_train_history[
        [
            "warehouse_id",
            "warehouse_prior_delay_rate",
            "shipments",
        ]
    ]
    .rename(
        columns={
            "shipments":
                "prior_shipments"
        }
    )
)

test = test.merge(
    warehouse_train_history,
    on="warehouse_id",
    how="left"
)

test[
    "warehouse_prior_delay_rate"
] = test[
    "warehouse_prior_delay_rate"
].fillna(global_delay_rate)

test["prior_shipments"] = (
    test["prior_shipments"]
    .fillna(0)
)


partner_train_history = (
    train
    .groupby("delivery_partner_id")
    .agg(
        delayed=(
            "is_delayed",
            "sum"
        ),
        shipments=(
            "is_delayed",
            "count"
        ),
    )
    .reset_index()
)

partner_train_history[
    "partner_prior_delay_rate"
] = safe_divide(
    partner_train_history["delayed"],
    partner_train_history["shipments"],
    global_delay_rate
)

partner_train_history = (
    partner_train_history[
        [
            "delivery_partner_id",
            "partner_prior_delay_rate",
            "shipments",
        ]
    ]
    .rename(
        columns={
            "shipments":
                "partner_prior_shipments"
        }
    )
)

test = test.merge(
    partner_train_history,
    on="delivery_partner_id",
    how="left"
)

test[
    "partner_prior_delay_rate"
] = test[
    "partner_prior_delay_rate"
].fillna(global_delay_rate)

test["partner_prior_shipments"] = (
    test["partner_prior_shipments"]
    .fillna(0)
)


# ============================================================
# COMBINED RISK FEATURES
# ============================================================

for frame in [train, test]:

    frame[
        "historical_operational_risk"
    ] = (
        frame[
            "warehouse_prior_delay_rate"
        ] * 0.5
        +
        frame[
            "partner_prior_delay_rate"
        ] * 0.5
    )

    frame[
        "network_distance_pressure"
    ] = safe_divide(
        frame["distance_km"],
        frame["sla_days"]
    )


# ============================================================
# CLEAN INTERNAL COLUMNS
# ============================================================

for frame in [train, test]:

    frame.drop(
        columns=["_date"],
        inplace=True,
        errors="ignore"
    )


# ============================================================
# REMOVE LEAKAGE / IDENTIFIER COLUMNS
# ============================================================

DROP_COLUMNS = [
    "shipment_id",
    "order_id",
    "shipment_date",
    "order_date",
    "actual_delivery_date",
    "expected_delivery_date",
    "shipment_status",
]

train_target = train["is_delayed"].copy()
test_target = test["is_delayed"].copy()

train = train.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)

test = test.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)

train["is_delayed"] = train_target.values
test["is_delayed"] = test_target.values


# ============================================================
# CLEANING
# ============================================================

train = train.dropna().copy()
test = test.dropna().copy()


# ============================================================
# SAFETY CHECKS
# ============================================================

assert len(train) > 0
assert len(test) > 0

assert set(
    train["is_delayed"].unique()
).issubset({0, 1})

assert set(
    test["is_delayed"].unique()
).issubset({0, 1})


# ============================================================
# SAVE
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

train.to_csv(
    TRAIN_FILE,
    index=False
)

test.to_csv(
    TEST_FILE,
    index=False
)

combined = pd.concat(
    [
        train.assign(dataset="train"),
        test.assign(dataset="test"),
    ],
    ignore_index=True
)

combined.to_csv(
    FULL_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print()
print("=" * 70)
print("TIME-AWARE DATASET COMPLETE")
print("=" * 70)

print()
print("TRAIN")
print(f"Rows       : {len(train):,}")
print(
    f"Delay rate : "
    f"{train['is_delayed'].mean():.4f}"
)

print()
print("TEST")
print(f"Rows       : {len(test):,}")
print(
    f"Delay rate : "
    f"{test['is_delayed'].mean():.4f}"
)

print()
print("TRAINING DATE RANGE")
print(
    "2023-01-01 -> "
    f"{cutoff_date.date()}"
)

print()
print("TESTING DATE RANGE")
print(
    f"{test['shipment_date'].min().date() if 'shipment_date' in test.columns else 'future period'}"
)

print()
print("Output:")
print(f"✓ {TRAIN_FILE}")
print(f"✓ {TEST_FILE}")
print(f"✓ {FULL_FILE}")

print()
print("PHASE 5.1 COMPLETE")
print("=" * 70)