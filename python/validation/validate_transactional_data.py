import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


# ============================================================
# EXPECTED ROW COUNTS
# ============================================================

EXPECTED_ROWS = {
    "orders.csv": 100_000,
    "order_items.csv": 299_720,
    "payments.csv": 100_000,
    "shipments.csv": 100_000,
    "delivery_attempts.csv": 99_464,
    "inventory.csv": 150_000,
    "returns.csv": 15_000,
}


# ============================================================
# EXPECTED COLUMNS
# ============================================================

EXPECTED_COLUMNS = {

    "orders.csv": [
        "order_id",
        "customer_id",
        "address_id",
        "order_date",
        "expected_delivery_date",
        "delivery_type",
        "priority",
        "order_status",
    ],

    "order_items.csv": [
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "discount_percent",
        "discount_amount",
        "line_total",
    ],

    "payments.csv": [
        "payment_id",
        "order_id",
        "payment_date",
        "payment_method",
        "payment_status",
        "amount",
        "transaction_reference",
    ],

    "shipments.csv": [
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
        "distance_km",
    ],

    "delivery_attempts.csv": [
        "attempt_id",
        "shipment_id",
        "order_id",
        "attempt_number",
        "attempt_date",
        "attempt_outcome",
        "failure_reason",
        "notes",
    ],

    "inventory.csv": [
        "inventory_id",
        "warehouse_id",
        "product_id",
        "opening_stock",
        "current_stock",
        "reorder_level",
        "unit_cost",
        "inventory_value",
        "stock_status",
        "last_restock_date",
    ],

    "returns.csv": [
        "return_id",
        "order_id",
        "order_item_id",
        "product_id",
        "return_date",
        "return_quantity",
        "return_reason",
        "return_status",
        "return_amount",
        "refund_amount",
    ],
}


# ============================================================
# ALLOWED VALUES
# ============================================================

DELIVERY_TYPES = {
    "Standard",
    "Express",
    "Same Day",
}

ORDER_STATUSES = {
    "Pending",
    "Confirmed",
    "Processing",
    "Shipped",
    "Delivered",
    "Cancelled",
    "Returned",
}

PAYMENT_METHODS = {
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "COD",
    "Wallet",
}

PAYMENT_STATUSES = {
    "Paid",
    "Failed",
    "Pending",
    "Refunded",
}

SHIPMENT_STATUSES = {
    "Created",
    "Picked Up",
    "In Transit",
    "Out for Delivery",
    "Delivered",
    "Delayed",
    "Failed",
}

ATTEMPT_OUTCOMES = {
    "Delivered",
    "Customer Unavailable",
    "Rescheduled",
    "Failed",
    "Wrong Address",
}

RETURN_REASONS = {
    "Damaged Product",
    "Wrong Product",
    "Product Defective",
    "Not as Expected",
    "Size/Fit Issue",
    "Late Delivery",
    "Changed Mind",
    "Other",
}

RETURN_STATUSES = {
    "Requested",
    "Approved",
    "Picked Up",
    "Received",
    "Refunded",
    "Rejected",
}

STOCK_STATUSES = {
    "In Stock",
    "Low Stock",
    "Out of Stock",
}


# ============================================================
# COUNTERS
# ============================================================

TOTAL_CHECKS = 0
PASSED_CHECKS = 0
FAILED_CHECKS = 0


# ============================================================
# CHECK RESULT FUNCTIONS
# ============================================================

def pass_check(message):
    global TOTAL_CHECKS, PASSED_CHECKS

    TOTAL_CHECKS += 1
    PASSED_CHECKS += 1

    print(f"  [PASS] {message}")


def fail_check(message):
    global TOTAL_CHECKS, FAILED_CHECKS

    TOTAL_CHECKS += 1
    FAILED_CHECKS += 1

    print(f"  [FAIL] {message}")


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(filename):

    path = RAW_DATA_DIR / filename

    if not path.exists():
        fail_check(f"{filename}: file missing")
        return None

    try:
        df = pd.read_csv(path)
        return df

    except Exception as e:
        fail_check(f"{filename}: unable to read CSV - {e}")
        return None


# ============================================================
# BASIC CHECKS
# ============================================================

def check_row_count(df, filename, expected):

    if df is None:
        return

    actual = len(df)

    if actual == expected:
        pass_check(
            f"{filename}: row count = {actual:,}"
        )
    else:
        fail_check(
            f"{filename}: expected {expected:,}, found {actual:,}"
        )


def check_columns(df, filename, expected_columns):

    if df is None:
        return

    actual_columns = list(df.columns)

    missing = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    if not missing:
        pass_check(
            f"{filename}: required columns present"
        )
    else:
        fail_check(
            f"{filename}: missing columns {missing}"
        )


def check_primary_key(df, filename, column):

    if df is None or column not in df.columns:
        return

    null_count = df[column].isna().sum()
    duplicate_count = df[column].duplicated().sum()

    if null_count == 0 and duplicate_count == 0:
        pass_check(
            f"{filename}.{column}: primary key valid"
        )
    else:
        fail_check(
            f"{filename}.{column}: "
            f"{null_count:,} NULLs, "
            f"{duplicate_count:,} duplicates"
        )


def check_nulls(df, filename, columns):

    if df is None:
        return

    for column in columns:

        if column not in df.columns:
            continue

        null_count = df[column].isna().sum()

        if null_count == 0:
            pass_check(
                f"{filename}.{column}: no NULL values"
            )
        else:
            fail_check(
                f"{filename}.{column}: "
                f"{null_count:,} NULL values"
            )


def check_allowed_values(
    df,
    filename,
    column,
    allowed_values
):

    if df is None or column not in df.columns:
        return

    actual_values = set(
        df[column]
        .dropna()
        .unique()
    )

    invalid_values = (
        actual_values
        - set(allowed_values)
    )

    if not invalid_values:
        pass_check(
            f"{filename}.{column}: allowed values valid"
        )
    else:
        fail_check(
            f"{filename}.{column}: "
            f"invalid values = {sorted(invalid_values)}"
        )


def check_numeric_non_negative(
    df,
    filename,
    column
):

    if df is None or column not in df.columns:
        return

    numeric = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid = (
        numeric.isna()
        | (numeric < 0)
    ).sum()

    if invalid == 0:
        pass_check(
            f"{filename}.{column}: non-negative values valid"
        )
    else:
        fail_check(
            f"{filename}.{column}: "
            f"{invalid:,} invalid negative/non-numeric values"
        )


def check_positive(
    df,
    filename,
    column
):

    if df is None or column not in df.columns:
        return

    numeric = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid = (
        numeric.isna()
        | (numeric <= 0)
    ).sum()

    if invalid == 0:
        pass_check(
            f"{filename}.{column}: positive values valid"
        )
    else:
        fail_check(
            f"{filename}.{column}: "
            f"{invalid:,} invalid non-positive values"
        )


def check_foreign_key(
    child_df,
    parent_df,
    child_file,
    child_column,
    parent_file,
    parent_column
):

    if child_df is None or parent_df is None:
        return

    if (
        child_column not in child_df.columns
        or parent_column not in parent_df.columns
    ):
        return

    parent_values = set(
        parent_df[parent_column]
        .dropna()
    )

    invalid = (
        child_df[child_column]
        .dropna()
        .loc[
            ~child_df[child_column]
            .dropna()
            .isin(parent_values)
        ]
        .nunique()
    )

    if invalid == 0:
        pass_check(
            f"{child_file}.{child_column} -> "
            f"{parent_file}.{parent_column}: FK valid"
        )
    else:
        fail_check(
            f"{child_file}.{child_column} -> "
            f"{parent_file}.{parent_column}: "
            f"{invalid:,} invalid references"
        )


# ============================================================
# DATE CHECK
# ============================================================

def check_date_parse(df, filename, column):

    if df is None or column not in df.columns:
        return

    parsed = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    invalid = parsed.isna().sum()

    if invalid == 0:
        pass_check(
            f"{filename}.{column}: valid dates"
        )
    else:
        fail_check(
            f"{filename}.{column}: "
            f"{invalid:,} invalid dates"
        )


# ============================================================
# LOAD MASTER DATA
# ============================================================

def load_master_data():

    customers = load_csv("customers.csv")
    addresses = load_csv("addresses.csv")
    products = load_csv("products.csv")
    warehouses = load_csv("warehouses.csv")
    partners = load_csv("delivery_partners.csv")

    return (
        customers,
        addresses,
        products,
        warehouses,
        partners
    )


# ============================================================
# ORDERS VALIDATION
# ============================================================

def validate_orders(
    orders,
    customers,
    addresses
):

    filename = "orders.csv"

    print("\n[ ORDERS ]")

    check_row_count(
        orders,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        orders,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        orders,
        filename,
        "order_id"
    )

    check_nulls(
        orders,
        filename,
        [
            "order_id",
            "customer_id",
            "address_id",
            "order_date",
            "expected_delivery_date",
            "delivery_type",
            "priority",
            "order_status",
        ]
    )

    check_foreign_key(
        orders,
        customers,
        filename,
        "customer_id",
        "customers.csv",
        "customer_id"
    )

    check_foreign_key(
        orders,
        addresses,
        filename,
        "address_id",
        "addresses.csv",
        "address_id"
    )

    check_allowed_values(
        orders,
        filename,
        "delivery_type",
        DELIVERY_TYPES
    )

    check_allowed_values(
        orders,
        filename,
        "order_status",
        ORDER_STATUSES
    )

    check_date_parse(
        orders,
        filename,
        "order_date"
    )

    check_date_parse(
        orders,
        filename,
        "expected_delivery_date"
    )

    order_date = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    expected_date = pd.to_datetime(
        orders["expected_delivery_date"],
        errors="coerce"
    )

    invalid_dates = (
        expected_date.dt.normalize()
        < order_date.dt.normalize()
    ).sum()

    if invalid_dates == 0:
        pass_check(
            f"{filename}: expected delivery date "
            f"is not before order date"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_dates:,} expected delivery dates "
            f"before order date"
        )

    # Customer/address relationship
    if (
        orders is not None
        and customers is not None
        and addresses is not None
    ):

        address_customer = (
            addresses
            .set_index("address_id")["customer_id"]
            .to_dict()
        )

        mismatches = 0

        for customer_id, address_id in zip(
            orders["customer_id"],
            orders["address_id"]
        ):

            if address_customer.get(address_id) != customer_id:
                mismatches += 1

        if mismatches == 0:
            pass_check(
                f"{filename}: customer-address relationship valid"
            )
        else:
            fail_check(
                f"{filename}: "
                f"{mismatches:,} customer-address mismatches"
            )


# ============================================================
# ORDER ITEMS VALIDATION
# ============================================================

def validate_order_items(
    items,
    orders,
    products
):

    filename = "order_items.csv"

    print("\n[ ORDER ITEMS ]")

    check_row_count(
        items,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        items,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        items,
        filename,
        "order_item_id"
    )

    check_nulls(
        items,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_foreign_key(
        items,
        orders,
        filename,
        "order_id",
        "orders.csv",
        "order_id"
    )

    check_foreign_key(
        items,
        products,
        filename,
        "product_id",
        "products.csv",
        "product_id"
    )

    check_positive(
        items,
        filename,
        "quantity"
    )

    check_positive(
        items,
        filename,
        "unit_price"
    )

    discount = pd.to_numeric(
        items["discount_percent"],
        errors="coerce"
    )

    invalid_discount = (
        discount.isna()
        | (discount < 0)
        | (discount > 100)
    ).sum()

    if invalid_discount == 0:
        pass_check(
            f"{filename}.discount_percent: 0-100 valid"
        )
    else:
        fail_check(
            f"{filename}.discount_percent: "
            f"{invalid_discount:,} invalid values"
        )

    expected_discount = (
        items["quantity"]
        * items["unit_price"]
        * items["discount_percent"]
        / 100
    )

    discount_diff = (
        expected_discount
        - items["discount_amount"]
    ).abs()

    invalid_discount_amount = (
        discount_diff > 0.01
    ).sum()

    if invalid_discount_amount == 0:
        pass_check(
            f"{filename}: discount_amount formula valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_discount_amount:,} invalid discount calculations"
        )

    expected_line_total = (
        items["quantity"]
        * items["unit_price"]
        - items["discount_amount"]
    )

    line_diff = (
        expected_line_total
        - items["line_total"]
    ).abs()

    invalid_line_total = (
        line_diff > 0.01
    ).sum()

    if invalid_line_total == 0:
        pass_check(
            f"{filename}: line_total formula valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_line_total:,} invalid line_total calculations"
        )


# ============================================================
# PAYMENTS VALIDATION
# ============================================================

def validate_payments(
    payments,
    orders,
    items
):

    filename = "payments.csv"

    print("\n[ PAYMENTS ]")

    check_row_count(
        payments,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        payments,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        payments,
        filename,
        "payment_id"
    )

    check_nulls(
        payments,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_foreign_key(
        payments,
        orders,
        filename,
        "order_id",
        "orders.csv",
        "order_id"
    )

    check_allowed_values(
        payments,
        filename,
        "payment_method",
        PAYMENT_METHODS
    )

    check_allowed_values(
        payments,
        filename,
        "payment_status",
        PAYMENT_STATUSES
    )

    check_positive(
        payments,
        filename,
        "amount"
    )

    check_date_parse(
        payments,
        filename,
        "payment_date"
    )

    # Payment date >= order date
    order_dates = (
        orders
        .assign(
            order_date=pd.to_datetime(
                orders["order_date"]
            )
        )
        .set_index("order_id")["order_date"]
    )

    payment_dates = pd.to_datetime(
        payments["payment_date"],
        errors="coerce"
    )

    mapped_order_dates = (
        payments["order_id"]
        .map(order_dates)
    )

    invalid_dates = (
        payment_dates < mapped_order_dates
    ).sum()

    if invalid_dates == 0:
        pass_check(
            f"{filename}: payment dates valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_dates:,} payment dates "
            f"before order dates"
        )

    # Payment amount = order item revenue
    order_totals = (
        items
        .groupby("order_id")["line_total"]
        .sum()
    )

    payment_totals = (
        payments
        .groupby("order_id")["amount"]
        .sum()
    )

    comparison = pd.concat(
        [
            order_totals.rename("order_total"),
            payment_totals.rename("payment_total")
        ],
        axis=1
    ).fillna(0)

    amount_diff = (
        comparison["order_total"]
        - comparison["payment_total"]
    ).abs()

    mismatches = (
        amount_diff > 0.01
    ).sum()

    if mismatches == 0:
        pass_check(
            f"{filename}: payment totals match order revenue"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{mismatches:,} orders have payment/revenue mismatch"
        )


# ============================================================
# SHIPMENTS VALIDATION
# ============================================================

def validate_shipments(
    shipments,
    orders,
    warehouses,
    partners
):

    filename = "shipments.csv"

    print("\n[ SHIPMENTS ]")

    check_row_count(
        shipments,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        shipments,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        shipments,
        filename,
        "shipment_id"
    )

    check_nulls(
        shipments,
        filename,
        [
            "shipment_id",
            "order_id",
            "warehouse_id",
            "delivery_partner_id",
            "shipment_date",
            "expected_delivery_date",
            "delivery_type",
            "shipment_status",
            "sla_days",
            "shipping_cost",
            "distance_km",
        ]
    )

    check_foreign_key(
        shipments,
        orders,
        filename,
        "order_id",
        "orders.csv",
        "order_id"
    )

    check_foreign_key(
        shipments,
        warehouses,
        filename,
        "warehouse_id",
        "warehouses.csv",
        "warehouse_id"
    )

    check_foreign_key(
        shipments,
        partners,
        filename,
        "delivery_partner_id",
        "delivery_partners.csv",
        "partner_id"
    )

    check_allowed_values(
        shipments,
        filename,
        "delivery_type",
        DELIVERY_TYPES
    )

    check_allowed_values(
        shipments,
        filename,
        "shipment_status",
        SHIPMENT_STATUSES
    )

    check_positive(
        shipments,
        filename,
        "sla_days"
    )

    check_positive(
        shipments,
        filename,
        "shipping_cost"
    )

    check_positive(
        shipments,
        filename,
        "distance_km"
    )

    # SLA mapping
    expected_sla = (
        shipments["delivery_type"]
        .map(
            {
                "Standard": 5,
                "Express": 3,
                "Same Day": 1,
            }
        )
    )

    sla_invalid = (
        shipments["sla_days"]
        != expected_sla
    ).sum()

    if sla_invalid == 0:
        pass_check(
            f"{filename}: SLA mapping valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{sla_invalid:,} invalid SLA values"
        )

    shipment_date = pd.to_datetime(
        shipments["shipment_date"],
        errors="coerce"
    )

    expected_delivery = pd.to_datetime(
        shipments["expected_delivery_date"],
        errors="coerce"
    )

    invalid_expected = (
        expected_delivery.dt.normalize()
        < shipment_date.dt.normalize()
    ).sum()

    if invalid_expected == 0:
        pass_check(
            f"{filename}: expected delivery date valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_expected:,} expected dates "
            f"before shipment dates"
        )

    actual_delivery = pd.to_datetime(
        shipments["actual_delivery_date"],
        errors="coerce"
    )

    invalid_actual = (
        actual_delivery.notna()
        & (
            actual_delivery
            < shipment_date
        )
    ).sum()

    if invalid_actual == 0:
        pass_check(
            f"{filename}: actual delivery dates valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_actual:,} actual delivery dates "
            f"before shipment dates"
        )


# ============================================================
# DELIVERY ATTEMPTS VALIDATION
# ============================================================

def validate_delivery_attempts(
    attempts,
    shipments
):

    filename = "delivery_attempts.csv"

    print("\n[ DELIVERY ATTEMPTS ]")

    check_row_count(
        attempts,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        attempts,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        attempts,
        filename,
        "attempt_id"
    )

    check_nulls(
        attempts,
        filename,
        [
            "attempt_id",
            "shipment_id",
            "order_id",
            "attempt_number",
            "attempt_date",
            "attempt_outcome",
        ]
    )

    check_foreign_key(
        attempts,
        shipments,
        filename,
        "shipment_id",
        "shipments.csv",
        "shipment_id"
    )

    check_allowed_values(
        attempts,
        filename,
        "attempt_outcome",
        ATTEMPT_OUTCOMES
    )

    check_positive(
        attempts,
        filename,
        "attempt_number"
    )

    check_date_parse(
        attempts,
        filename,
        "attempt_date"
    )

    # Shipment/order relationship
    shipment_orders = (
        shipments
        .set_index("shipment_id")["order_id"]
        .to_dict()
    )

    mismatches = 0

    for shipment_id, order_id in zip(
        attempts["shipment_id"],
        attempts["order_id"]
    ):

        if shipment_orders.get(shipment_id) != order_id:
            mismatches += 1

    if mismatches == 0:
        pass_check(
            f"{filename}: shipment-order relationship valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{mismatches:,} shipment-order mismatches"
        )

    # Attempt sequence
    sequence_errors = 0

    grouped = attempts.sort_values(
        [
            "shipment_id",
            "attempt_number"
        ]
    )

    for shipment_id, group in grouped.groupby(
        "shipment_id"
    ):

        numbers = group["attempt_number"].tolist()

        expected = list(
            range(1, len(numbers) + 1)
        )

        if numbers != expected:
            sequence_errors += 1

    if sequence_errors == 0:
        pass_check(
            f"{filename}: attempt numbering sequence valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{sequence_errors:,} invalid attempt sequences"
        )


# ============================================================
# INVENTORY VALIDATION
# ============================================================

def validate_inventory(
    inventory,
    warehouses,
    products
):

    filename = "inventory.csv"

    print("\n[ INVENTORY ]")

    check_row_count(
        inventory,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        inventory,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        inventory,
        filename,
        "inventory_id"
    )

    check_nulls(
        inventory,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_foreign_key(
        inventory,
        warehouses,
        filename,
        "warehouse_id",
        "warehouses.csv",
        "warehouse_id"
    )

    check_foreign_key(
        inventory,
        products,
        filename,
        "product_id",
        "products.csv",
        "product_id"
    )

    for column in [
        "opening_stock",
        "current_stock",
        "reorder_level",
    ]:
        check_numeric_non_negative(
            inventory,
            filename,
            column
        )

    check_positive(
        inventory,
        filename,
        "unit_cost"
    )

    check_numeric_non_negative(
        inventory,
        filename,
        "inventory_value"
    )

    expected_value = (
        inventory["current_stock"]
        * inventory["unit_cost"]
    )

    difference = (
        expected_value
        - inventory["inventory_value"]
    ).abs()

    invalid_formula = (
        difference > 0.01
    ).sum()

    if invalid_formula == 0:
        pass_check(
            f"{filename}: inventory_value formula valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{invalid_formula:,} invalid inventory values"
        )

    check_allowed_values(
        inventory,
        filename,
        "stock_status",
        STOCK_STATUSES
    )

    expected_status = pd.Series(
        "In Stock",
        index=inventory.index
    )

    expected_status.loc[
        inventory["current_stock"] == 0
    ] = "Out of Stock"

    expected_status.loc[
        (
            inventory["current_stock"] > 0
        )
        & (
            inventory["current_stock"]
            <= inventory["reorder_level"]
        )
    ] = "Low Stock"

    status_errors = (
        inventory["stock_status"]
        != expected_status
    ).sum()

    if status_errors == 0:
        pass_check(
            f"{filename}: stock status logic valid"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{status_errors:,} invalid stock statuses"
        )


# ============================================================
# RETURNS VALIDATION
# ============================================================

def validate_returns(
    returns,
    orders,
    items
):

    filename = "returns.csv"

    print("\n[ RETURNS ]")

    check_row_count(
        returns,
        filename,
        EXPECTED_ROWS[filename]
    )

    check_columns(
        returns,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_primary_key(
        returns,
        filename,
        "return_id"
    )

    check_nulls(
        returns,
        filename,
        EXPECTED_COLUMNS[filename]
    )

    check_foreign_key(
        returns,
        orders,
        filename,
        "order_id",
        "orders.csv",
        "order_id"
    )

    check_foreign_key(
        returns,
        items,
        filename,
        "order_item_id",
        "order_items.csv",
        "order_item_id"
    )

    check_foreign_key(
        returns,
        items,
        filename,
        "product_id",
        "order_items.csv",
        "product_id"
    )

    check_allowed_values(
        returns,
        filename,
        "return_reason",
        RETURN_REASONS
    )

    check_allowed_values(
        returns,
        filename,
        "return_status",
        RETURN_STATUSES
    )

    check_positive(
        returns,
        filename,
        "return_quantity"
    )

    check_positive(
        returns,
        filename,
        "return_amount"
    )

    check_numeric_non_negative(
        returns,
        filename,
        "refund_amount"
    )

    refund_invalid = (
        returns["refund_amount"]
        > returns["return_amount"] + 0.01
    ).sum()

    if refund_invalid == 0:
        pass_check(
            f"{filename}: refund amount <= return amount"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{refund_invalid:,} refunds exceed return amount"
        )

    # Return product must match order item product
    item_product = (
        items
        .set_index("order_item_id")["product_id"]
        .to_dict()
    )

    product_mismatches = 0

    for item_id, product_id in zip(
        returns["order_item_id"],
        returns["product_id"]
    ):

        if item_product.get(item_id) != product_id:
            product_mismatches += 1

    if product_mismatches == 0:
        pass_check(
            f"{filename}: return product matches order item"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{product_mismatches:,} product mismatches"
        )

    # Return quantity <= purchased quantity
    item_quantity = (
        items
        .set_index("order_item_id")["quantity"]
        .to_dict()
    )

    quantity_errors = 0

    for item_id, return_qty in zip(
        returns["order_item_id"],
        returns["return_quantity"]
    ):

        purchased_qty = item_quantity.get(item_id)

        if (
            purchased_qty is not None
            and return_qty > purchased_qty
        ):
            quantity_errors += 1

    if quantity_errors == 0:
        pass_check(
            f"{filename}: return quantity <= purchased quantity"
        )
    else:
        fail_check(
            f"{filename}: "
            f"{quantity_errors:,} return quantities exceed purchased quantity"
        )


# ============================================================
# CROSS-TABLE CHECKS
# ============================================================

def validate_cross_table_relationships(
    orders,
    items,
    payments,
    shipments,
    attempts,
    returns
):

    print("\n[ CROSS-TABLE BUSINESS RULES ]")

    # One shipment per order
    shipment_counts = (
        shipments
        .groupby("order_id")
        .size()
    )

    duplicate_shipments = (
        shipment_counts > 1
    ).sum()

    if duplicate_shipments == 0:
        pass_check(
            "Orders -> Shipments: one shipment per order"
        )
    else:
        fail_check(
            f"Orders -> Shipments: "
            f"{duplicate_shipments:,} orders have multiple shipments"
        )

    # Every shipment order exists
    missing_orders = (
        ~shipments["order_id"]
        .isin(orders["order_id"])
    ).sum()

    if missing_orders == 0:
        pass_check(
            "Shipments -> Orders: all orders valid"
        )
    else:
        fail_check(
            f"Shipments -> Orders: "
            f"{missing_orders:,} invalid orders"
        )

    # Every attempt shipment exists
    missing_shipments = (
        ~attempts["shipment_id"]
        .isin(shipments["shipment_id"])
    ).sum()

    if missing_shipments == 0:
        pass_check(
            "Delivery Attempts -> Shipments: all shipments valid"
        )
    else:
        fail_check(
            f"Delivery Attempts -> Shipments: "
            f"{missing_shipments:,} invalid shipments"
        )

    # Every return item exists
    missing_items = (
        ~returns["order_item_id"]
        .isin(items["order_item_id"])
    ).sum()

    if missing_items == 0:
        pass_check(
            "Returns -> Order Items: all items valid"
        )
    else:
        fail_check(
            f"Returns -> Order Items: "
            f"{missing_items:,} invalid items"
        )

    # Return order must match order-item order
    item_order = (
        items
        .set_index("order_item_id")["order_id"]
        .to_dict()
    )

    mismatch = 0

    for order_id, item_id in zip(
        returns["order_id"],
        returns["order_item_id"]
    ):

        if item_order.get(item_id) != order_id:
            mismatch += 1

    if mismatch == 0:
        pass_check(
            "Returns: order_id matches order_item order_id"
        )
    else:
        fail_check(
            f"Returns: "
            f"{mismatch:,} order/order-item mismatches"
        )

    # Every payment order exists
    missing_payment_orders = (
        ~payments["order_id"]
        .isin(orders["order_id"])
    ).sum()

    if missing_payment_orders == 0:
        pass_check(
            "Payments -> Orders: all orders valid"
        )
    else:
        fail_check(
            f"Payments -> Orders: "
            f"{missing_payment_orders:,} invalid orders"
        )


# ============================================================
# DATASET SUMMARY
# ============================================================

def print_dataset_summary(datasets):

    print("\n")
    print("=" * 70)
    print("TRANSACTIONAL DATASET SUMMARY")
    print("=" * 70)

    for filename, df in datasets.items():

        if df is not None:

            print(
                f"{filename:<30}"
                f"{len(df):>12,} rows"
            )


# ============================================================
# FINAL REPORT
# ============================================================

def print_final_report():

    print("\n")
    print("=" * 70)
    print("LOGIX TRANSACTIONAL DATA VALIDATION REPORT")
    print("=" * 70)

    print(
        f"Total Checks : {TOTAL_CHECKS}"
    )

    print(
        f"Passed       : {PASSED_CHECKS}"
    )

    print(
        f"Failed       : {FAILED_CHECKS}"
    )

    print("-" * 70)

    if FAILED_CHECKS == 0:

        print(
            "STATUS       : VALIDATION PASSED"
        )

        print(
            "\nAll transactional datasets passed validation."
        )

        return True

    else:

        print(
            "STATUS       : VALIDATION FAILED"
        )

        print(
            "\nFix the failed checks before "
            "locking transactional data."
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("LOGIX TRANSACTIONAL DATA VALIDATION")
    print("=" * 70)

    print(
        f"\nData directory: {RAW_DATA_DIR}"
    )

    # --------------------------------------------------------
    # LOAD TRANSACTIONAL DATA
    # --------------------------------------------------------

    orders = load_csv("orders.csv")
    items = load_csv("order_items.csv")
    payments = load_csv("payments.csv")
    shipments = load_csv("shipments.csv")
    attempts = load_csv("delivery_attempts.csv")
    inventory = load_csv("inventory.csv")
    returns = load_csv("returns.csv")

    # --------------------------------------------------------
    # LOAD MASTER DATA
    # --------------------------------------------------------

    (
        customers,
        addresses,
        products,
        warehouses,
        partners
    ) = load_master_data()

    # --------------------------------------------------------
    # VALIDATE
    # --------------------------------------------------------

    validate_orders(
        orders,
        customers,
        addresses
    )

    validate_order_items(
        items,
        orders,
        products
    )

    validate_payments(
        payments,
        orders,
        items
    )

    validate_shipments(
        shipments,
        orders,
        warehouses,
        partners
    )

    validate_delivery_attempts(
        attempts,
        shipments
    )

    validate_inventory(
        inventory,
        warehouses,
        products
    )

    validate_returns(
        returns,
        orders,
        items
    )

    validate_cross_table_relationships(
        orders,
        items,
        payments,
        shipments,
        attempts,
        returns
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    datasets = {
        "orders.csv": orders,
        "order_items.csv": items,
        "payments.csv": payments,
        "shipments.csv": shipments,
        "delivery_attempts.csv": attempts,
        "inventory.csv": inventory,
        "returns.csv": returns,
    }

    print_dataset_summary(datasets)

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    validation_passed = print_final_report()

    if not validation_passed:
        sys.exit(1)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()