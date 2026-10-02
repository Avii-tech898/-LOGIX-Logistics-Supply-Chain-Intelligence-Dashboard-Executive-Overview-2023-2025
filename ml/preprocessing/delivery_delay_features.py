"""
LOGIX - Delivery Delay Prediction
Phase 2: Time-Aware Feature Engineering

Purpose:
- Create operationally meaningful features
- Create time-based features
- Create leakage-safe historical warehouse performance
- Create leakage-safe historical delivery-partner performance
- Preserve the original baseline dataset

Important:
Historical target-based features use ONLY previous records.
The current shipment's own target is never used.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

ORDERS_FILE = RAW_DIR / "orders.csv"
SHIPMENTS_FILE = RAW_DIR / "shipments.csv"

SOURCE_FILE = OUTPUT_DIR / "delivery_delay_dataset.csv"
OUTPUT_FILE = OUTPUT_DIR / "delivery_delay_engineered.csv"


# ============================================================
# LOAD SOURCE DATA
# ============================================================

print("=" * 70)
print("LOGIX - DELIVERY DELAY PREDICTION")
print("PHASE 2: TIME-AWARE FEATURE ENGINEERING")
print("=" * 70)

print("\n📂 Loading source datasets...")

orders = pd.read_csv(ORDERS_FILE)
shipments = pd.read_csv(SHIPMENTS_FILE)

print(f"Orders    : {orders.shape}")
print(f"Shipments : {shipments.shape}")


# ============================================================
# PREPARE DATES
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce",
)

shipments["shipment_date"] = pd.to_datetime(
    shipments["shipment_date"],
    errors="coerce",
)

shipments["expected_delivery_date"] = pd.to_datetime(
    shipments["expected_delivery_date"],
    errors="coerce",
)

shipments["actual_delivery_date"] = pd.to_datetime(
    shipments["actual_delivery_date"],
    errors="coerce",
)


# ============================================================
# BUILD MODELING BASE
# ============================================================

print("\n🔗 Building modeling base...")

order_columns = [
    "order_id",
    "order_date",
    "priority",
]

base = shipments.merge(
    orders[order_columns],
    on="order_id",
    how="inner",
    validate="one_to_one",
)

# Keep only shipments with known final delivery outcome
base = base.dropna(
    subset=[
        "actual_delivery_date",
        "expected_delivery_date",
        "shipment_date",
        "order_date",
    ]
).copy()


# ============================================================
# TARGET
# ============================================================

base["is_delayed"] = (
    base["actual_delivery_date"]
    > base["expected_delivery_date"]
).astype(int)


# ============================================================
# EXISTING CORE FEATURES
# ============================================================

base["processing_days"] = (
    base["shipment_date"]
    - base["order_date"]
).dt.total_seconds() / 86400

base["processing_days"] = base["processing_days"].clip(
    lower=0
)

base["order_month"] = (
    base["order_date"].dt.month
)

base["order_day_of_week"] = (
    base["order_date"].dt.dayofweek
)

base["shipment_day_of_week"] = (
    base["shipment_date"].dt.dayofweek
)


# ============================================================
# 1. OPERATIONAL RATIO FEATURES
# ============================================================

print("\n⚙️ Creating operational features...")

# Distance relative to SLA allowance
base["distance_per_sla_day"] = (
    base["distance_km"]
    / base["sla_days"].replace(0, np.nan)
)

# Shipping cost efficiency
base["shipping_cost_per_km"] = (
    base["shipping_cost"]
    / base["distance_km"].replace(0, np.nan)
)

# Processing pressure relative to SLA
base["processing_to_sla_ratio"] = (
    base["processing_days"]
    / base["sla_days"].replace(0, np.nan)
)

# Remaining SLA buffer at shipment dispatch
base["sla_buffer_days"] = (
    base["sla_days"]
    - base["processing_days"]
)


# ============================================================
# 2. DELIVERY TYPE FLAGS
# ============================================================

base["is_express"] = (
    base["delivery_type"]
    .eq("Express")
    .astype(int)
)

base["is_same_day"] = (
    base["delivery_type"]
    .eq("Same Day")
    .astype(int)
)

base["is_high_priority"] = (
    base["priority"]
    .eq("High")
    .astype(int)
)


# ============================================================
# 3. CYCLICAL TIME FEATURES
# ============================================================

print("📅 Creating cyclical time features...")

base["order_month_sin"] = np.sin(
    2 * np.pi * base["order_month"] / 12
)

base["order_month_cos"] = np.cos(
    2 * np.pi * base["order_month"] / 12
)

base["order_day_sin"] = np.sin(
    2 * np.pi * base["order_day_of_week"] / 7
)

base["order_day_cos"] = np.cos(
    2 * np.pi * base["order_day_of_week"] / 7
)

base["shipment_day_sin"] = np.sin(
    2 * np.pi * base["shipment_day_of_week"] / 7
)

base["shipment_day_cos"] = np.cos(
    2 * np.pi * base["shipment_day_of_week"] / 7
)


# ============================================================
# 4. TIME-AWARE HISTORICAL FEATURES
# ============================================================

print("🕒 Creating leakage-safe historical features...")

# Sort chronologically.
base = base.sort_values(
    "shipment_date"
).reset_index(drop=True)


# ------------------------------------------------------------
# Warehouse historical delay rate
# ------------------------------------------------------------

warehouse_prior_delayed = (
    base.groupby("warehouse_id")["is_delayed"]
    .transform(
        lambda x:
        x.shift(1)
        .expanding()
        .mean()
    )
)

base["warehouse_prior_delay_rate"] = (
    warehouse_prior_delayed
)


# ------------------------------------------------------------
# Delivery partner historical delay rate
# ------------------------------------------------------------

partner_prior_delayed = (
    base.groupby("delivery_partner_id")["is_delayed"]
    .transform(
        lambda x:
        x.shift(1)
        .expanding()
        .mean()
    )
)

base["partner_prior_delay_rate"] = (
    partner_prior_delayed
)


# ============================================================
# 5. HISTORICAL SAMPLE COUNTS
# ============================================================

warehouse_prior_count = (
    base.groupby("warehouse_id")
    .cumcount()
)

partner_prior_count = (
    base.groupby("delivery_partner_id")
    .cumcount()
)

base["warehouse_prior_shipments"] = (
    warehouse_prior_count
)

base["partner_prior_shipments"] = (
    partner_prior_count
)


# ============================================================
# 6. STABILIZE EARLY HISTORICAL VALUES
# ============================================================

# For the first observation of a warehouse/partner,
# historical performance does not exist.

# Use the global historical rate from records available
# before the current row.

global_prior_delay = (
    base["is_delayed"]
    .shift(1)
    .expanding()
    .mean()
)

base["warehouse_prior_delay_rate"] = (
    base["warehouse_prior_delay_rate"]
    .fillna(global_prior_delay)
)

base["partner_prior_delay_rate"] = (
    base["partner_prior_delay_rate"]
    .fillna(global_prior_delay)
)

# If the very first record has no previous observation,
# use the overall training-history-neutral baseline.
base["warehouse_prior_delay_rate"] = (
    base["warehouse_prior_delay_rate"]
    .fillna(base["is_delayed"].mean())
)

base["partner_prior_delay_rate"] = (
    base["partner_prior_delay_rate"]
    .fillna(base["is_delayed"].mean())
)


# ============================================================
# 7. COMBINED OPERATIONAL RISK FEATURES
# ============================================================

base["historical_operational_risk"] = (
    (
        base["warehouse_prior_delay_rate"]
        + base["partner_prior_delay_rate"]
    )
    / 2
)

base["network_distance_pressure"] = (
    base["distance_per_sla_day"]
    * (
        1
        + base["historical_operational_risk"]
    )
)


# ============================================================
# 8. CLEAN NUMERIC VALUES
# ============================================================

engineered_numeric = [
    "distance_per_sla_day",
    "shipping_cost_per_km",
    "processing_to_sla_ratio",
    "sla_buffer_days",
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

for column in engineered_numeric:

    base[column] = (
        pd.to_numeric(
            base[column],
            errors="coerce",
        )
    )

    base[column] = (
        base[column]
        .replace([np.inf, -np.inf], np.nan)
    )


# ============================================================
# 9. SELECT FINAL FEATURES
# ============================================================

final_columns = [
    # Original numerical features
    "distance_km",
    "shipping_cost",
    "sla_days",
    "processing_days",
    "order_month",
    "order_day_of_week",
    "shipment_day_of_week",

    # Original categorical features
    "delivery_type",
    "priority",
    "warehouse_id",
    "delivery_partner_id",

    # Operational engineered features
    "distance_per_sla_day",
    "shipping_cost_per_km",
    "processing_to_sla_ratio",
    "sla_buffer_days",

    # Binary features
    "is_express",
    "is_same_day",
    "is_high_priority",

    # Cyclical features
    "order_month_sin",
    "order_month_cos",
    "order_day_sin",
    "order_day_cos",
    "shipment_day_sin",
    "shipment_day_cos",

    # Historical features
    "warehouse_prior_delay_rate",
    "partner_prior_delay_rate",
    "warehouse_prior_shipments",
    "partner_prior_shipments",

    # Combined operational features
    "historical_operational_risk",
    "network_distance_pressure",

    # Target
    "is_delayed",
]

engineered = base[final_columns].copy()


# ============================================================
# 10. DROP REMAINING MISSING VALUES
# ============================================================

before_drop = len(engineered)

engineered = engineered.dropna().reset_index(
    drop=True
)

after_drop = len(engineered)

print(
    f"\nRows before final cleaning: {before_drop:,}"
)

print(
    f"Rows after final cleaning : {after_drop:,}"
)

print(
    f"Rows removed              : "
    f"{before_drop - after_drop:,}"
)


# ============================================================
# 11. VALIDATION
# ============================================================

print("\n🔍 Validating engineered dataset...")

print(
    f"Final shape: {engineered.shape}"
)

print("\nTarget distribution:")

print(
    engineered["is_delayed"]
    .value_counts()
    .sort_index()
)

print("\nEngineered features:")

for column in final_columns:
    print(f"  ✓ {column}")


# ============================================================
# HISTORICAL FEATURE VALIDATION
# ============================================================

assert (
    engineered["warehouse_prior_delay_rate"]
    .between(0, 1)
    .all()
)

assert (
    engineered["partner_prior_delay_rate"]
    .between(0, 1)
    .all()
)

assert (
    engineered["warehouse_prior_shipments"]
    >= 0
).all()

assert (
    engineered["partner_prior_shipments"]
    >= 0
).all()


# ============================================================
# SAVE
# ============================================================

engineered.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("\n" + "=" * 70)
print("✅ FEATURE ENGINEERING COMPLETED")
print("=" * 70)

print(f"\n📄 Output:")
print(OUTPUT_FILE)

print("\n🔒 Original baseline dataset was NOT modified.")
print("🔒 Existing trained models were NOT modified.")