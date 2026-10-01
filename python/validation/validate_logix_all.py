import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]

sys.path.insert(0, str(PROJECT_ROOT))

from python.config import RAW_DATA_DIR


# ============================================================
# VALIDATION RESULT STORAGE
# ============================================================

checks = []
failures = []


def add_check(name, passed, details=""):
    passed = bool(passed)

    checks.append({
        "check": name,
        "status": "PASS" if passed else "FAIL",
        "details": details
    })

    if not passed:
        failures.append({
            "check": name,
            "details": details
        })


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(filename):

    path = RAW_DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}"
        )

    return pd.read_csv(path)


# ============================================================
# COLUMN VALIDATION
# ============================================================

def check_columns(df, filename, required):

    missing = set(required) - set(df.columns)

    add_check(
        f"{filename} schema",
        len(missing) == 0,
        (
            f"Missing: {sorted(missing)}"
            if missing
            else "All required columns present"
        )
    )


# ============================================================
# PRIMARY KEY
# ============================================================

def check_pk(df, filename, column):

    if column not in df.columns:
        add_check(
            f"{filename} PK {column}",
            False,
            "Column missing"
        )
        return

    nulls = df[column].isna().sum()
    duplicates = df[column].duplicated().sum()

    add_check(
        f"{filename} PK NULL",
        nulls == 0,
        f"NULLs: {nulls:,}"
    )

    add_check(
        f"{filename} PK duplicate",
        duplicates == 0,
        f"Duplicates: {duplicates:,}"
    )


# ============================================================
# FOREIGN KEY
# ============================================================

def check_fk(
    child,
    parent,
    child_column,
    parent_column,
    name
):

    invalid = (
        ~child[child_column].isin(
            parent[parent_column]
        )
    ).sum()

    add_check(
        name,
        invalid == 0,
        f"Invalid references: {invalid:,}"
    )


# ============================================================
# POSITIVE VALUE
# ============================================================

def check_positive(df, column, name):

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid = (values <= 0).sum()

    add_check(
        name,
        invalid == 0,
        f"Invalid rows: {invalid:,}"
    )


# ============================================================
# NON-NEGATIVE VALUE
# ============================================================

def check_non_negative(df, column, name):

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid = (values < 0).sum()

    add_check(
        name,
        invalid == 0,
        f"Invalid rows: {invalid:,}"
    )


# ============================================================
# DATE VALIDATION
# ============================================================

def check_date_column(df, column, name):

    converted = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    invalid = (
        converted.isna()
        & df[column].notna()
    ).sum()

    add_check(
        name,
        invalid == 0,
        f"Invalid dates: {invalid:,}"
    )


# ============================================================
# START
# ============================================================

print()
print("=" * 78)
print("LOGIX — COMPREHENSIVE DATA VALIDATION")
print("=" * 78)
print()


# ============================================================
# LOAD ALL DATA
# ============================================================

data = {

    "customers":
        load_csv("customers.csv"),

    "addresses":
        load_csv("addresses.csv"),

    "products":
        load_csv("products.csv"),

    "warehouses":
        load_csv("warehouses.csv"),

    "drivers":
        load_csv("drivers.csv"),

    "vehicles":
        load_csv("vehicles.csv"),

    "delivery_partners":
        load_csv("delivery_partners.csv"),

    "orders":
        load_csv("orders.csv"),

    "order_items":
        load_csv("order_items.csv"),

    "payments":
        load_csv("payments.csv"),

    "shipments":
        load_csv("shipments.csv"),

    "delivery_attempts":
        load_csv("delivery_attempts.csv"),

    "inventory":
        load_csv("inventory.csv"),

    "returns":
        load_csv("returns.csv"),
}


for name, df in data.items():

    print(
        f"Loaded: "
        f"{name + '.csv':<28}"
        f"{len(df):>10,} rows"
    )


# ============================================================
# 1. SCHEMA VALIDATION
# ============================================================

print()
print("-" * 78)
print("1. SCHEMA VALIDATION")
print("-" * 78)


schemas = {

    "customers": [
        "customer_id",
        "customer_name",
        "email",
        "phone",
        "gender",
        "customer_segment",
        "registration_date",
        "state",
        "city",
        "pincode",
        "preferred_payment_method",
        "is_active"
    ],

    "addresses": [
        "address_id",
        "customer_id",
        "address_type",
        "address_line",
        "city",
        "state",
        "pincode",
        "is_default"
    ],

    "products": [
        "product_id",
        "product_name",
        "category",
        "brand",
        "unit_price",
        "weight_kg",
        "supplier",
        "reorder_level",
        "is_active"
    ],

    "warehouses": [
        "warehouse_id",
        "warehouse_name",
        "warehouse_type",
        "city",
        "state",
        "pincode",
        "capacity_units",
        "manager_name",
        "operating_hours",
        "is_active"
    ],

    "drivers": [
        "driver_id",
        "driver_name",
        "phone",
        "license_number",
        "experience_years",
        "rating",
        "city",
        "employment_type",
        "status"
    ],

    "vehicles": [
        "vehicle_id",
        "vehicle_number",
        "vehicle_type",
        "capacity_kg",
        "fuel_type",
        "model_year",
        "driver_id",
        "status"
    ],

    "delivery_partners": [
        "partner_id",
        "partner_name",
        "service_type",
        "coverage_type",
        "base_cost_per_km",
        "rating",
        "contact_phone",
        "status"
    ],

    "orders": [
        "order_id",
        "customer_id",
        "address_id",
        "order_date",
        "expected_delivery_date",
        "delivery_type",
        "priority",
        "order_status"
    ],

    "order_items": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_percent",
        "discount_amount",
        "line_total"
    ],

    "payments": [
        "payment_id",
        "order_id",
        "payment_date",
        "payment_method",
        "payment_status",
        "amount",
        "transaction_reference"
    ],

    "shipments": [
        "shipment_id",
        "order_id",
        "warehouse_id",
        "delivery_partner_id",
        "shipment_date",
        "expected_delivery_date",
        "actual_delivery_date",
        "delivery_type",
        "shipment_status",
        "sla_days",
        "shipping_cost",
        "distance_km"
    ],

    "delivery_attempts": [
        "attempt_id",
        "shipment_id",
        "order_id",
        "attempt_number",
        "attempt_date",
        "attempt_outcome",
        "failure_reason",
        "notes"
    ],

    "inventory": [
        "inventory_id",
        "warehouse_id",
        "product_id",
        "opening_stock",
        "current_stock",
        "reorder_level",
        "unit_cost",
        "inventory_value",
        "stock_status",
        "last_restock_date"
    ],

    "returns": [
        "return_id",
        "order_id",
        "order_item_id",
        "product_id",
        "return_date",
        "return_quantity",
        "return_reason",
        "return_status",
        "return_amount",
        "refund_amount"
    ]
}


for name, columns in schemas.items():

    check_columns(
        data[name],
        name + ".csv",
        columns
    )


# ============================================================
# 2. PRIMARY KEY VALIDATION
# ============================================================

print()
print("-" * 78)
print("2. PRIMARY KEY VALIDATION")
print("-" * 78)


primary_keys = {

    "customers": "customer_id",
    "addresses": "address_id",
    "products": "product_id",
    "warehouses": "warehouse_id",
    "drivers": "driver_id",
    "vehicles": "vehicle_id",
    "delivery_partners": "partner_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "payments": "payment_id",
    "shipments": "shipment_id",
    "delivery_attempts": "attempt_id",
    "inventory": "inventory_id",
    "returns": "return_id"
}


for name, column in primary_keys.items():

    check_pk(
        data[name],
        name + ".csv",
        column
    )


# ============================================================
# 3. FOREIGN KEY VALIDATION
# ============================================================

print()
print("-" * 78)
print("3. FOREIGN KEY VALIDATION")
print("-" * 78)


check_fk(
    data["addresses"],
    data["customers"],
    "customer_id",
    "customer_id",
    "addresses → customers"
)

check_fk(
    data["orders"],
    data["customers"],
    "customer_id",
    "customer_id",
    "orders → customers"
)

check_fk(
    data["orders"],
    data["addresses"],
    "address_id",
    "address_id",
    "orders → addresses"
)

check_fk(
    data["order_items"],
    data["orders"],
    "order_id",
    "order_id",
    "order_items → orders"
)

check_fk(
    data["order_items"],
    data["products"],
    "product_id",
    "product_id",
    "order_items → products"
)

check_fk(
    data["payments"],
    data["orders"],
    "order_id",
    "order_id",
    "payments → orders"
)

check_fk(
    data["shipments"],
    data["orders"],
    "order_id",
    "order_id",
    "shipments → orders"
)

check_fk(
    data["shipments"],
    data["warehouses"],
    "warehouse_id",
    "warehouse_id",
    "shipments → warehouses"
)

check_fk(
    data["shipments"],
    data["delivery_partners"],
    "delivery_partner_id",
    "partner_id",
    "shipments → delivery_partners"
)

check_fk(
    data["delivery_attempts"],
    data["shipments"],
    "shipment_id",
    "shipment_id",
    "delivery_attempts → shipments"
)

check_fk(
    data["delivery_attempts"],
    data["orders"],
    "order_id",
    "order_id",
    "delivery_attempts → orders"
)

check_fk(
    data["inventory"],
    data["warehouses"],
    "warehouse_id",
    "warehouse_id",
    "inventory → warehouses"
)

check_fk(
    data["inventory"],
    data["products"],
    "product_id",
    "product_id",
    "inventory → products"
)

check_fk(
    data["vehicles"],
    data["drivers"],
    "driver_id",
    "driver_id",
    "vehicles → drivers"
)

check_fk(
    data["returns"],
    data["orders"],
    "order_id",
    "order_id",
    "returns → orders"
)

check_fk(
    data["returns"],
    data["order_items"],
    "order_item_id",
    "order_item_id",
    "returns → order_items"
)

check_fk(
    data["returns"],
    data["products"],
    "product_id",
    "product_id",
    "returns → products"
)


# ============================================================
# 4. NULL VALIDATION
# ============================================================

print()
print("-" * 78)
print("4. NULL VALIDATION")
print("-" * 78)


for name, df in data.items():

    null_count = int(
        df.isna().sum().sum()
    )

    if name in ["shipments", "delivery_attempts"]:

        passed = True

    else:

        passed = (
            null_count == 0
        )

    add_check(
        f"{name}.csv NULL validation",
        passed,
        f"NULL values: {null_count:,}"
    )


# ============================================================
# 5. NUMERIC VALIDATION
# ============================================================

print()
print("-" * 78)
print("5. NUMERIC VALIDATION")
print("-" * 78)


check_positive(
    data["products"],
    "unit_price",
    "products.unit_price > 0"
)

check_positive(
    data["products"],
    "weight_kg",
    "products.weight_kg > 0"
)

check_non_negative(
    data["drivers"],
    "experience_years",
    "drivers.experience_years >= 0"
)

check_positive(
    data["drivers"],
    "rating",
    "drivers.rating > 0"
)

check_positive(
    data["delivery_partners"],
    "base_cost_per_km",
    "delivery_partners.base_cost_per_km > 0"
)

check_positive(
    data["delivery_partners"],
    "rating",
    "delivery_partners.rating > 0"
)

check_positive(
    data["order_items"],
    "quantity",
    "order_items.quantity > 0"
)

check_positive(
    data["order_items"],
    "unit_price",
    "order_items.unit_price > 0"
)

check_non_negative(
    data["order_items"],
    "discount_percent",
    "order_items.discount_percent >= 0"
)

check_non_negative(
    data["order_items"],
    "discount_amount",
    "order_items.discount_amount >= 0"
)

check_non_negative(
    data["order_items"],
    "line_total",
    "order_items.line_total >= 0"
)

check_positive(
    data["payments"],
    "amount",
    "payments.amount > 0"
)

check_positive(
    data["shipments"],
    "distance_km",
    "shipments.distance_km > 0"
)

check_positive(
    data["shipments"],
    "shipping_cost",
    "shipments.shipping_cost > 0"
)

check_positive(
    data["shipments"],
    "sla_days",
    "shipments.sla_days > 0"
)

check_non_negative(
    data["inventory"],
    "opening_stock",
    "inventory.opening_stock >= 0"
)

check_non_negative(
    data["inventory"],
    "current_stock",
    "inventory.current_stock >= 0"
)

check_non_negative(
    data["inventory"],
    "reorder_level",
    "inventory.reorder_level >= 0"
)

check_positive(
    data["inventory"],
    "unit_cost",
    "inventory.unit_cost > 0"
)

check_non_negative(
    data["inventory"],
    "inventory_value",
    "inventory.inventory_value >= 0"
)

check_positive(
    data["returns"],
    "return_quantity",
    "returns.return_quantity > 0"
)

check_non_negative(
    data["returns"],
    "return_amount",
    "returns.return_amount >= 0"
)

check_non_negative(
    data["returns"],
    "refund_amount",
    "returns.refund_amount >= 0"
)


# ============================================================
# 6. ORDER ITEM BUSINESS LOGIC
# ============================================================

print()
print("-" * 78)
print("6. ORDER ITEM BUSINESS LOGIC")
print("-" * 78)


items = data["order_items"].copy()


invalid_discount_percent = (
    (items["discount_percent"] < 0)
    |
    (items["discount_percent"] > 100)
).sum()


add_check(
    "discount_percent between 0 and 100",
    invalid_discount_percent == 0,
    f"Invalid rows: {invalid_discount_percent:,}"
)


expected_discount = (
    items["quantity"]
    * items["unit_price"]
    * items["discount_percent"]
    / 100
)


discount_difference = (
    expected_discount
    - items["discount_amount"]
).abs()


discount_errors = (
    discount_difference > 0.02
).sum()


add_check(
    "discount_amount formula",
    discount_errors == 0,
    f"Mismatches: {discount_errors:,}"
)


expected_line_total = (
    items["quantity"]
    * items["unit_price"]
    - items["discount_amount"]
)


line_total_difference = (
    expected_line_total
    - items["line_total"]
).abs()


line_total_errors = (
    line_total_difference > 0.02
).sum()


add_check(
    "line_total formula",
    line_total_errors == 0,
    f"Mismatches: {line_total_errors:,}"
)


# ============================================================
# 7. PAYMENT TOTAL VALIDATION
# ============================================================

print()
print("-" * 78)
print("7. PAYMENT / ORDER TOTAL VALIDATION")
print("-" * 78)


payments = data["payments"]


order_totals = (
    items
    .groupby("order_id")["line_total"]
    .sum()
    .reset_index()
)


order_totals.columns = [
    "order_id",
    "order_total"
]


payment_totals = (
    payments
    .groupby("order_id")["amount"]
    .sum()
    .reset_index()
)


payment_totals.columns = [
    "order_id",
    "payment_total"
]


payment_check = order_totals.merge(
    payment_totals,
    on="order_id",
    how="left"
)


payment_check["payment_total"] = (
    payment_check["payment_total"]
    .fillna(0)
)


payment_difference = (
    payment_check["order_total"]
    - payment_check["payment_total"]
).abs()


payment_errors = (
    payment_difference > 0.02
).sum()


add_check(
    "payment total matches order total",
    payment_errors == 0,
    f"Mismatched orders: {payment_errors:,}"
)


# ============================================================
# 8. INVENTORY VALUE
# ============================================================

print()
print("-" * 78)
print("8. INVENTORY VALUE VALIDATION")
print("-" * 78)


inventory = data["inventory"]


expected_inventory_value = (
    inventory["current_stock"]
    * inventory["unit_cost"]
)


inventory_difference = (
    expected_inventory_value
    - inventory["inventory_value"]
).abs()


inventory_errors = (
    inventory_difference > 0.02
).sum()


add_check(
    "inventory_value = current_stock × unit_cost",
    inventory_errors == 0,
    f"Mismatches: {inventory_errors:,}"
)


# ============================================================
# 9. RETURN VALIDATION
# ============================================================

print()
print("-" * 78)
print("9. RETURN BUSINESS LOGIC")
print("-" * 78)


returns = data["returns"]


return_items = items[
    [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price"
    ]
]


return_check = returns.merge(
    return_items,
    on="order_item_id",
    how="left",
    suffixes=(
        "_return",
        "_item"
    )
)


order_errors = (
    return_check["order_id_return"]
    != return_check["order_id_item"]
).sum()


product_errors = (
    return_check["product_id_return"]
    != return_check["product_id_item"]
).sum()


quantity_errors = (
    return_check["return_quantity"]
    > return_check["quantity"]
).sum()


expected_return_amount = (
    return_check["return_quantity"]
    * return_check["unit_price"]
)


return_amount_difference = (
    expected_return_amount
    - return_check["return_amount"]
).abs()


return_amount_errors = (
    return_amount_difference > 0.02
).sum()


refund_errors = (
    returns["refund_amount"]
    > returns["return_amount"]
).sum()


add_check(
    "return order consistency",
    order_errors == 0,
    f"Mismatches: {order_errors:,}"
)

add_check(
    "return product consistency",
    product_errors == 0,
    f"Mismatches: {product_errors:,}"
)

add_check(
    "return quantity <= purchased quantity",
    quantity_errors == 0,
    f"Invalid rows: {quantity_errors:,}"
)

add_check(
    "return amount formula",
    return_amount_errors == 0,
    f"Mismatches: {return_amount_errors:,}"
)

add_check(
    "refund <= return amount",
    refund_errors == 0,
    f"Invalid rows: {refund_errors:,}"
)


# ============================================================
# 10. SHIPMENT VALIDATION
# ============================================================

print()
print("-" * 78)
print("10. SHIPMENT VALIDATION")
print("-" * 78)


shipments = data["shipments"]


duplicate_shipment_orders = (
    shipments["order_id"]
    .duplicated()
).sum()


add_check(
    "one shipment per order",
    duplicate_shipment_orders == 0,
    f"Duplicate orders: {duplicate_shipment_orders:,}"
)


shipment_date = pd.to_datetime(
    shipments["shipment_date"],
    errors="coerce"
)


shipment_expected = pd.to_datetime(
    shipments["expected_delivery_date"],
    errors="coerce"
)


shipment_actual = pd.to_datetime(
    shipments["actual_delivery_date"],
    errors="coerce"
)


expected_before_shipment = (
    shipment_expected
    < shipment_date
).sum()


actual_before_shipment = (
    shipment_actual.notna()
    &
    (
        shipment_actual
        < shipment_date
    )
).sum()


add_check(
    "shipment expected date >= shipment date",
    expected_before_shipment == 0,
    f"Invalid rows: {expected_before_shipment:,}"
)

add_check(
    "shipment actual date >= shipment date",
    actual_before_shipment == 0,
    f"Invalid rows: {actual_before_shipment:,}"
)


# ============================================================
# 11. DELIVERY ATTEMPTS
# ============================================================

print()
print("-" * 78)
print("11. DELIVERY ATTEMPT VALIDATION")
print("-" * 78)


attempts = data["delivery_attempts"]


invalid_attempt_number = (
    attempts["attempt_number"] <= 0
).sum()


add_check(
    "attempt_number > 0",
    invalid_attempt_number == 0,
    f"Invalid rows: {invalid_attempt_number:,}"
)


sequence_errors = 0


for shipment_id, group in attempts.groupby(
    "shipment_id"
):

    numbers = sorted(
        group["attempt_number"].tolist()
    )

    expected = list(
        range(
            1,
            len(numbers) + 1
        )
    )

    if numbers != expected:
        sequence_errors += 1


add_check(
    "delivery attempt sequence",
    sequence_errors == 0,
    f"Invalid sequences: {sequence_errors:,}"
)


# ============================================================
# 12. DATE VALIDATION
# ============================================================

print()
print("-" * 78)
print("12. DATE VALIDATION")
print("-" * 78)


check_date_column(
    data["customers"],
    "registration_date",
    "customer registration dates"
)

check_date_column(
    data["orders"],
    "order_date",
    "order dates"
)

check_date_column(
    data["orders"],
    "expected_delivery_date",
    "order expected delivery dates"
)

check_date_column(
    data["payments"],
    "payment_date",
    "payment dates"
)

check_date_column(
    data["shipments"],
    "shipment_date",
    "shipment dates"
)

check_date_column(
    data["shipments"],
    "expected_delivery_date",
    "shipment expected dates"
)

check_date_column(
    data["shipments"],
    "actual_delivery_date",
    "shipment actual dates"
)

check_date_column(
    data["delivery_attempts"],
    "attempt_date",
    "attempt dates"
)

check_date_column(
    data["inventory"],
    "last_restock_date",
    "inventory restock dates"
)

check_date_column(
    data["returns"],
    "return_date",
    "return dates"
)


# ============================================================
# 13. ORDER DATE LOGIC
# ============================================================

print()
print("-" * 78)
print("13. ORDER DATE BUSINESS LOGIC")
print("-" * 78)


orders = data["orders"]


order_date = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)


expected_order_date = pd.to_datetime(
    orders["expected_delivery_date"],
    errors="coerce"
)


invalid_order_dates = (
    expected_order_date
    < order_date
).sum()


add_check(
    "order expected date >= order date",
    invalid_order_dates == 0,
    f"Invalid orders: {invalid_order_dates:,}"
)


# ============================================================
# 14. PAYMENT DATE LOGIC
# ============================================================

print()
print("-" * 78)
print("14. PAYMENT DATE BUSINESS LOGIC")
print("-" * 78)


payment_dates = payments.merge(
    orders[
        [
            "order_id",
            "order_date"
        ]
    ],
    on="order_id",
    how="left"
)


payment_date_values = pd.to_datetime(
    payment_dates["payment_date"],
    errors="coerce"
)


order_date_values = pd.to_datetime(
    payment_dates["order_date"],
    errors="coerce"
)


invalid_payment_dates = (
    payment_date_values
    < order_date_values
).sum()


add_check(
    "payment date >= order date",
    invalid_payment_dates == 0,
    f"Invalid payments: {invalid_payment_dates:,}"
)


# ============================================================
# 15. DATASET SIZE
# ============================================================

print()
print("-" * 78)
print("15. DATASET SIZE VALIDATION")
print("-" * 78)


minimum_rows = {

    "customers": 20_000,
    "addresses": 30_000,
    "products": 5_000,
    "warehouses": 30,
    "drivers": 1_000,
    "vehicles": 1_200,
    "delivery_partners": 25,
    "orders": 100_000,
    "order_items": 250_000,
    "payments": 100_000,
    "shipments": 100_000,
    "delivery_attempts": 1,
    "inventory": 100_000,
    "returns": 15_000
}


for name, minimum in minimum_rows.items():

    actual = len(
        data[name]
    )

    add_check(
        f"{name}.csv minimum rows",
        actual >= minimum,
        (
            f"Actual: {actual:,}; "
            f"Minimum: {minimum:,}"
        )
    )


# ============================================================
# FINAL RESULT
# ============================================================

results = pd.DataFrame(
    checks
)


total_checks = len(results)

passed_checks = (
    results["status"] == "PASS"
).sum()

failed_checks = (
    results["status"] == "FAIL"
).sum()


print()
print("=" * 78)
print("FINAL VALIDATION RESULT")
print("=" * 78)

print()

print(
    f"Total Checks : {total_checks}"
)

print(
    f"Passed       : {passed_checks}"
)

print(
    f"Failed       : {failed_checks}"
)

print()


if failed_checks == 0:

    print(
        "STATUS: VALIDATION PASSED"
    )

else:

    print(
        "STATUS: VALIDATION FAILED"
    )

    print()
    print(
        "FAILED CHECKS"
    )

    print(
        "-" * 78
    )

    for failure in failures:

        print(
            f"FAIL: {failure['check']}"
        )

        print(
            f"      {failure['details']}"
        )


# ============================================================
# SAVE REPORT
# ============================================================

report_path = (
    RAW_DATA_DIR
    / "logix_validation_report.csv"
)


results.to_csv(
    report_path,
    index=False
)


print()
print(
    "Validation report:"
)

print(
    report_path
)

print()
print("=" * 78)
print(
    "LOGIX VALIDATION COMPLETE"
)
print("=" * 78)

