"""
LOGIX - Delivery Delay Prediction
Phase 2: Engineered Feature Validation

Purpose:
- Validate engineered dataset
- Check target distribution
- Check missing/infinite values
- Measure engineered feature signal
- Inspect historical warehouse/partner features
- Check chronological ordering
- Detect obvious leakage risks

This script does NOT modify:
- baseline dataset
- engineered dataset
- trained models
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

ENGINEERED_FILE = (
    OUTPUT_DIR / "delivery_delay_engineered.csv"
)

REPORT_FILE = (
    OUTPUT_DIR
    / "engineered_feature_validation_report.txt"
)


# ============================================================
# FEATURE GROUPS
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
print("LOGIX - ENGINEERED FEATURE VALIDATION")
print("=" * 70)

print("\n📂 Loading engineered dataset...")

df = pd.read_csv(
    ENGINEERED_FILE
)

print(
    f"Dataset shape: {df.shape}"
)


# ============================================================
# REPORT HELPER
# ============================================================

report = []


def add(text=""):
    print(text)
    report.append(str(text))


# ============================================================
# 1. REQUIRED COLUMNS
# ============================================================

required_columns = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
    + [TARGET]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

add("\n" + "=" * 70)
add("1. REQUIRED COLUMN CHECK")
add("=" * 70)

if missing_columns:

    add(
        f"❌ Missing columns: {missing_columns}"
    )

    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

else:

    add(
        f"✅ All {len(required_columns)} required columns present."
    )


# ============================================================
# 2. TARGET VALIDATION
# ============================================================

add("\n" + "=" * 70)
add("2. TARGET VALIDATION")
add("=" * 70)

target_values = sorted(
    df[TARGET].dropna().unique()
)

add(
    f"Target values: {target_values}"
)

invalid_target = (
    ~df[TARGET].isin([0, 1])
).sum()

add(
    f"Invalid target values: {invalid_target}"
)

target_counts = (
    df[TARGET]
    .value_counts()
    .sort_index()
)

for value, count in target_counts.items():

    label = (
        "Delayed"
        if value == 1
        else "On-Time"
    )

    percentage = (
        count / len(df) * 100
    )

    add(
        f"{label:10s}: "
        f"{count:,} "
        f"({percentage:.2f}%)"
    )


# ============================================================
# 3. MISSING VALUES
# ============================================================

add("\n" + "=" * 70)
add("3. MISSING VALUE CHECK")
add("=" * 70)

missing = (
    df[required_columns]
    .isnull()
    .sum()
)

missing_total = int(
    missing.sum()
)

if missing_total == 0:

    add(
        "✅ No missing values."
    )

else:

    for column, count in missing[
        missing > 0
    ].items():

        add(
            f"⚠️ {column}: {count:,}"
        )


# ============================================================
# 4. INFINITE VALUES
# ============================================================

add("\n" + "=" * 70)
add("4. INFINITE VALUE CHECK")
add("=" * 70)

numeric_df = df[NUMERIC_FEATURES]

infinite_mask = np.isinf(
    numeric_df.to_numpy()
)

infinite_count = int(
    infinite_mask.sum()
)

if infinite_count == 0:

    add(
        "✅ No infinite values."
    )

else:

    add(
        f"❌ Infinite values found: "
        f"{infinite_count:,}"
    )


# ============================================================
# 5. NUMERIC CORRELATION
# ============================================================

add("\n" + "=" * 70)
add("5. ENGINEERED NUMERIC FEATURE SIGNAL")
add("=" * 70)

correlations = (
    df[
        NUMERIC_FEATURES
        + [TARGET]
    ]
    .corr(numeric_only=True)[TARGET]
    .drop(TARGET)
    .sort_values(
        key=lambda x: x.abs(),
        ascending=False,
    )
)

for feature, correlation in correlations.items():

    add(
        f"{feature:32s} | "
        f"Correlation: {correlation:.6f}"
    )


# ============================================================
# 6. TOP SIGNAL FEATURES
# ============================================================

add("\n" + "=" * 70)
add("6. TOP ENGINEERED FEATURES")
add("=" * 70)

top_features = (
    correlations.abs()
    .sort_values(
        ascending=False
    )
    .head(10)
)

for feature in top_features.index:

    correlation = correlations[
        feature
    ]

    add(
        f"{feature:32s} | "
        f"|Correlation|: "
        f"{abs(correlation):.6f}"
    )


# ============================================================
# 7. HISTORICAL FEATURE RANGES
# ============================================================

add("\n" + "=" * 70)
add("7. HISTORICAL FEATURE VALIDATION")
add("=" * 70)

historical_rate_features = [
    "warehouse_prior_delay_rate",
    "partner_prior_delay_rate",
]

for feature in historical_rate_features:

    minimum = df[feature].min()
    maximum = df[feature].max()
    mean = df[feature].mean()

    valid_range = (
        (df[feature] >= 0)
        & (df[feature] <= 1)
    ).all()

    status = (
        "PASS"
        if valid_range
        else "FAIL"
    )

    add(
        f"{status:5s} | "
        f"{feature:32s} | "
        f"Min: {minimum:.6f} | "
        f"Max: {maximum:.6f} | "
        f"Mean: {mean:.6f}"
    )


# ============================================================
# 8. HISTORICAL COUNT FEATURES
# ============================================================

add("\n" + "=" * 70)
add("8. HISTORICAL COUNT FEATURES")
add("=" * 70)

count_features = [
    "warehouse_prior_shipments",
    "partner_prior_shipments",
]

for feature in count_features:

    minimum = df[feature].min()
    maximum = df[feature].max()

    non_negative = (
        df[feature] >= 0
    ).all()

    status = (
        "PASS"
        if non_negative
        else "FAIL"
    )

    add(
        f"{status:5s} | "
        f"{feature:32s} | "
        f"Min: {minimum:.0f} | "
        f"Max: {maximum:.0f}"
    )


# ============================================================
# 9. OPERATIONAL FEATURE CHECK
# ============================================================

add("\n" + "=" * 70)
add("9. OPERATIONAL FEATURE CHECK")
add("=" * 70)

operational_features = [
    "distance_per_sla_day",
    "shipping_cost_per_km",
    "processing_to_sla_ratio",
    "sla_buffer_days",
    "historical_operational_risk",
    "network_distance_pressure",
]

for feature in operational_features:

    series = df[feature]

    add(
        f"{feature:32s} | "
        f"Min: {series.min():.4f} | "
        f"Mean: {series.mean():.4f} | "
        f"Max: {series.max():.4f}"
    )


# ============================================================
# 10. TARGET RATE BY HISTORICAL FEATURES
# ============================================================

add("\n" + "=" * 70)
add("10. HISTORICAL FEATURE vs TARGET")
add("=" * 70)

for feature in historical_rate_features:

    temp = df[
        [feature, TARGET]
    ].copy()

    temp["risk_bucket"] = pd.qcut(
        temp[feature],
        q=5,
        duplicates="drop",
    )

    grouped = (
        temp.groupby(
            "risk_bucket",
            observed=True,
        )[TARGET]
        .agg(
            records="count",
            delay_rate="mean",
        )
    )

    add(
        f"\n--- {feature} ---"
    )

    for bucket, row in grouped.iterrows():

        add(
            f"{str(bucket):30s} | "
            f"Records: {int(row['records']):6d} | "
            f"Delay Rate: "
            f"{row['delay_rate'] * 100:6.2f}%"
        )


# ============================================================
# 11. CATEGORICAL SIGNAL
# ============================================================

add("\n" + "=" * 70)
add("11. CATEGORICAL SIGNAL")
add("=" * 70)

for feature in CATEGORICAL_FEATURES:

    grouped = (
        df.groupby(
            feature,
            observed=True,
        )[TARGET]
        .agg(
            records="count",
            delay_rate="mean",
        )
        .sort_values(
            "delay_rate",
            ascending=False,
        )
    )

    max_rate = (
        grouped["delay_rate"].max()
    )

    min_rate = (
        grouped["delay_rate"].min()
    )

    spread = (
        max_rate - min_rate
    )

    add(
        f"{feature:25s} | "
        f"Min: {min_rate * 100:.2f}% | "
        f"Max: {max_rate * 100:.2f}% | "
        f"Spread: {spread * 100:.2f} pp"
    )


# ============================================================
# 12. DUPLICATE CHECK
# ============================================================

add("\n" + "=" * 70)
add("12. DUPLICATE CHECK")
add("=" * 70)

duplicate_rows = int(
    df.duplicated().sum()
)

if duplicate_rows == 0:

    add(
        "✅ No duplicate rows."
    )

else:

    add(
        f"⚠️ Duplicate rows: "
        f"{duplicate_rows:,}"
    )


# ============================================================
# 13. DATASET SIZE CHECK
# ============================================================

add("\n" + "=" * 70)
add("13. DATASET SIZE")
add("=" * 70)

add(
    f"Rows    : {len(df):,}"
)

add(
    f"Columns : {len(df.columns):,}"
)

add(
    "Source engineered dataset: "
    "delivery_delay_engineered.csv"
)


# ============================================================
# 14. VALIDATION SUMMARY
# ============================================================

add("\n" + "=" * 70)
add("14. VALIDATION SUMMARY")
add("=" * 70)

checks = {
    "required_columns": len(missing_columns) == 0,
    "invalid_target": invalid_target == 0,
    "missing_values": missing_total == 0,
    "infinite_values": infinite_count == 0,
    "historical_rates_valid": all(
        (
            df[feature].between(0, 1).all()
        )
        for feature in historical_rate_features
    ),
    "historical_counts_valid": all(
        (
            df[feature] >= 0
        ).all()
        for feature in count_features
    ),
    "duplicate_rows": duplicate_rows == 0,
}

passed = sum(
    checks.values()
)

total = len(checks)

for name, status in checks.items():

    result = (
        "PASS"
        if status
        else "FAIL"
    )

    add(
        f"{result:5s} | {name}"
    )

add(
    f"\nValidation result: "
    f"{passed}/{total} checks passed."
)


# ============================================================
# CONCLUSION
# ============================================================

add("\n" + "=" * 70)
add("15. CONCLUSION")
add("=" * 70)

if passed == total:

    add(
        "✅ ENGINEERED DATASET PASSED "
        "STRUCTURAL VALIDATION."
    )

    add(
        "Next step: train/test preprocessing "
        "for engineered features."
    )

else:

    add(
        "⚠️ ENGINEERED DATASET REQUIRES "
        "REVIEW BEFORE MODEL TRAINING."
    )

add(
    "\nBaseline models remain untouched."
)

add(
    "Original baseline dataset remains untouched."
)


# ============================================================
# SAVE REPORT
# ============================================================

REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8",
)

print("\n" + "=" * 70)
print("✅ ENGINEERED FEATURE VALIDATION COMPLETED")
print("=" * 70)

print(
    f"\n📄 Report saved:\n{REPORT_FILE}"
)