from pathlib import Path
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

TRAIN_FILE = OUTPUT_DIR / "delivery_delay_temporal_train.csv"
TEST_FILE = OUTPUT_DIR / "delivery_delay_temporal_test.csv"


print("=" * 70)
print("LOGIX - TEMPORAL DATASET VALIDATION")
print("=" * 70)


train = pd.read_csv(TRAIN_FILE)
test = pd.read_csv(TEST_FILE)


passed = 0
failed = 0


def check(name, condition):
    global passed, failed

    if condition:
        print(f"PASS | {name}")
        passed += 1
    else:
        print(f"FAIL | {name}")
        failed += 1


# ============================================================
# Basic
# ============================================================

check("Train is not empty", len(train) > 0)
check("Test is not empty", len(test) > 0)

check(
    "Train target contains only 0/1",
    set(train["is_delayed"].unique()).issubset({0, 1})
)

check(
    "Test target contains only 0/1",
    set(test["is_delayed"].unique()).issubset({0, 1})
)

check(
    "Train has both classes",
    train["is_delayed"].nunique() == 2
)

check(
    "Test has both classes",
    test["is_delayed"].nunique() == 2
)


# ============================================================
# Historical Features
# ============================================================

history_features = [
    "warehouse_prior_delay_rate",
    "partner_prior_delay_rate",
    "prior_shipments",
    "partner_prior_shipments",
    "historical_operational_risk",
]

for feature in history_features:

    check(
        f"Train contains {feature}",
        feature in train.columns
    )

    check(
        f"Test contains {feature}",
        feature in test.columns
    )


# ============================================================
# Missing / Infinite
# ============================================================

check(
    "Train has no missing values",
    not train.isna().any().any()
)

check(
    "Test has no missing values",
    not test.isna().any().any()
)

numeric_train = train.select_dtypes(
    include=np.number
)

numeric_test = test.select_dtypes(
    include=np.number
)

check(
    "Train has no infinite values",
    np.isfinite(numeric_train).all().all()
)

check(
    "Test has no infinite values",
    np.isfinite(numeric_test).all().all()
)


# ============================================================
# Historical Ranges
# ============================================================

for name in [
    "warehouse_prior_delay_rate",
    "partner_prior_delay_rate",
]:

    check(
        f"Train {name} in 0-1",
        train[name].between(0, 1).all()
    )

    check(
        f"Test {name} in 0-1",
        test[name].between(0, 1).all()
    )


# ============================================================
# Leakage
# ============================================================

for column in [
    "actual_delivery_date",
    "shipment_status",
    "expected_delivery_date",
]:

    check(
        f"Train excludes {column}",
        column not in train.columns
    )

    check(
        f"Test excludes {column}",
        column not in test.columns
    )


# ============================================================
# Target
# ============================================================

check(
    "Train target is separate",
    "is_delayed" in train.columns
)

check(
    "Test target is separate",
    "is_delayed" in test.columns
)


# ============================================================
# Same Columns
# ============================================================

check(
    "Train and Test have same columns",
    list(train.columns) == list(test.columns)
)


# ============================================================
# Summary
# ============================================================

print()
print("=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)

print(f"PASS : {passed}")
print(f"FAIL : {failed}")

if failed == 0:
    print()
    print("✅ TEMPORAL DATASET PASSED VALIDATION")
else:
    print()
    print("❌ TEMPORAL DATASET VALIDATION FAILED")

print("=" * 70)