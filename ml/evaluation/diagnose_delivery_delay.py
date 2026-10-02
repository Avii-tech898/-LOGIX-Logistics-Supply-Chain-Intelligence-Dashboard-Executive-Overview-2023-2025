"""
LOGIX - Delivery Delay Prediction
Phase 2: Feature Signal & Data Diagnostic

Purpose:
- Analyze target distribution
- Check numeric feature statistics
- Measure numeric feature correlation with target
- Calculate categorical delay rates
- Detect constant / near-constant features
- Identify potential predictive signal
- Preserve baseline ML models
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

DATA_FILE = OUTPUT_DIR / "delivery_delay_dataset.csv"

REPORT_FILE = OUTPUT_DIR / "delivery_delay_diagnostic_report.txt"


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

TARGET = "is_delayed"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("LOGIX - DELIVERY DELAY PREDICTION")
print("PHASE 2: FEATURE SIGNAL & DATA DIAGNOSTIC")
print("=" * 70)

print("\n📂 Loading dataset...")

df = pd.read_csv(DATA_FILE)

print(f"✅ Dataset shape: {df.shape}")

required_columns = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
    + [TARGET]
)

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ============================================================
# REPORT STORAGE
# ============================================================

report = []

def add(text=""):
    print(text)
    report.append(str(text))


# ============================================================
# 1. BASIC INFORMATION
# ============================================================

add("\n" + "=" * 70)
add("1. BASIC DATASET INFORMATION")
add("=" * 70)

add(f"Rows: {len(df):,}")
add(f"Columns: {len(df.columns)}")

add("\nColumns:")
for column in df.columns:
    add(f"  - {column}")


# ============================================================
# 2. TARGET DISTRIBUTION
# ============================================================

add("\n" + "=" * 70)
add("2. TARGET DISTRIBUTION")
add("=" * 70)

target_counts = df[TARGET].value_counts().sort_index()
target_percent = (
    df[TARGET]
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

for value in target_counts.index:
    label = "Delayed" if value == 1 else "On-Time"

    add(
        f"{label}: "
        f"{target_counts[value]:,} "
        f"({target_percent[value]:.2f}%)"
    )


# ============================================================
# 3. MISSING VALUES
# ============================================================

add("\n" + "=" * 70)
add("3. MISSING VALUE CHECK")
add("=" * 70)

missing = df.isnull().sum()

if missing.sum() == 0:
    add("✅ No missing values found.")
else:
    for column, count in missing[missing > 0].items():
        add(f"{column}: {count:,}")


# ============================================================
# 4. CONSTANT / NEAR-CONSTANT FEATURES
# ============================================================

add("\n" + "=" * 70)
add("4. CONSTANT / NEAR-CONSTANT FEATURE CHECK")
add("=" * 70)

for column in NUMERIC_FEATURES + CATEGORICAL_FEATURES:

    unique_count = df[column].nunique()

    top_frequency = (
        df[column]
        .value_counts(normalize=True)
        .iloc[0]
        * 100
    )

    add(
        f"{column:25s} | "
        f"Unique: {unique_count:6d} | "
        f"Most common: {top_frequency:6.2f}%"
    )


# ============================================================
# 5. NUMERIC FEATURE STATISTICS
# ============================================================

add("\n" + "=" * 70)
add("5. NUMERIC FEATURE STATISTICS")
add("=" * 70)

numeric_stats = df[NUMERIC_FEATURES].describe().T

for feature in NUMERIC_FEATURES:

    row = numeric_stats.loc[feature]

    add(
        f"{feature:25s} | "
        f"Mean: {row['mean']:.4f} | "
        f"Std: {row['std']:.4f} | "
        f"Min: {row['min']:.4f} | "
        f"Max: {row['max']:.4f}"
    )


# ============================================================
# 6. NUMERIC FEATURE CORRELATION
# ============================================================

add("\n" + "=" * 70)
add("6. NUMERIC FEATURE CORRELATION WITH TARGET")
add("=" * 70)

correlations = (
    df[NUMERIC_FEATURES + [TARGET]]
    .corr(numeric_only=True)[TARGET]
    .drop(TARGET)
    .sort_values(
        key=lambda x: x.abs(),
        ascending=False,
    )
)

for feature, correlation in correlations.items():

    add(
        f"{feature:25s} | "
        f"Correlation: {correlation:.6f}"
    )


# ============================================================
# 7. CATEGORICAL DELAY RATES
# ============================================================

add("\n" + "=" * 70)
add("7. CATEGORICAL FEATURE DELAY RATES")
add("=" * 70)

for feature in CATEGORICAL_FEATURES:

    add(f"\n--- {feature} ---")

    grouped = (
        df.groupby(feature, observed=True)[TARGET]
        .agg(
            records="count",
            delayed="sum",
            delay_rate="mean",
        )
        .sort_values(
            "delay_rate",
            ascending=False,
        )
    )

    for category, row in grouped.iterrows():

        add(
            f"{str(category):25s} | "
            f"Records: {int(row['records']):6d} | "
            f"Delayed: {int(row['delayed']):6d} | "
            f"Delay Rate: {row['delay_rate'] * 100:6.2f}%"
        )


# ============================================================
# 8. NUMERIC FEATURE BY TARGET
# ============================================================

add("\n" + "=" * 70)
add("8. NUMERIC FEATURES BY TARGET CLASS")
add("=" * 70)

for feature in NUMERIC_FEATURES:

    grouped = (
        df.groupby(TARGET)[feature]
        .agg(
            mean="mean",
            median="median",
            std="std",
        )
    )

    add(f"\n--- {feature} ---")

    for target_value, row in grouped.iterrows():

        label = (
            "Delayed"
            if target_value == 1
            else "On-Time"
        )

        add(
            f"{label:10s} | "
            f"Mean: {row['mean']:.4f} | "
            f"Median: {row['median']:.4f} | "
            f"Std: {row['std']:.4f}"
        )


# ============================================================
# 9. TARGET RELATIONSHIP CHECKS
# ============================================================

add("\n" + "=" * 70)
add("9. POTENTIAL PREDICTIVE SIGNAL")
add("=" * 70)

signal_found = False

for feature, correlation in correlations.items():

    if abs(correlation) >= 0.10:
        signal_found = True
        add(
            f"Potential numeric signal: "
            f"{feature} "
            f"(correlation={correlation:.4f})"
        )

if not signal_found:
    add(
        "⚠️ No numeric feature has absolute "
        "correlation >= 0.10 with the target."
    )


# ============================================================
# 10. DATA QUALITY CHECKS
# ============================================================

add("\n" + "=" * 70)
add("10. DATA QUALITY CHECKS")
add("=" * 70)

checks = {}

checks["negative_distance"] = (
    (df["distance_km"] < 0).sum()
)

checks["negative_shipping_cost"] = (
    (df["shipping_cost"] < 0).sum()
)

checks["negative_processing_days"] = (
    (df["processing_days"] < 0).sum()
)

checks["invalid_sla_days"] = (
    (df["sla_days"] <= 0).sum()
)

checks["invalid_target"] = (
    (~df[TARGET].isin([0, 1])).sum()
)

for check_name, count in checks.items():

    status = "PASS" if count == 0 else "FAIL"

    add(
        f"{status:5s} | "
        f"{check_name:30s} | "
        f"Count: {count:,}"
    )


# ============================================================
# 11. OVERALL DIAGNOSTIC CONCLUSION
# ============================================================

add("\n" + "=" * 70)
add("11. DIAGNOSTIC CONCLUSION")
add("=" * 70)

max_correlation = correlations.abs().max()

if max_correlation < 0.05:

    add(
        "⚠️ Very weak numeric relationship detected."
    )

    add(
        "Feature engineering is required before "
        "retraining the predictive models."
    )

elif max_correlation < 0.10:

    add(
        "⚠️ Weak numeric relationship detected."
    )

    add(
        "Additional feature engineering and "
        "categorical signal analysis are recommended."
    )

else:

    add(
        "✅ Some numeric predictive signal detected."
    )

    add(
        "Feature engineering can be used to "
        "strengthen the model."
    )


add(
    "\nBaseline models remain preserved. "
    "No existing model files were modified."
)


# ============================================================
# SAVE REPORT
# ============================================================

REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8",
)

print("\n" + "=" * 70)
print("✅ DIAGNOSTIC COMPLETED")
print("=" * 70)

print(f"\n📄 Diagnostic report:")
print(REPORT_FILE)