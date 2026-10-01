"""
LOGIX — FINAL RAW DATA CROSS-TABLE AUDIT
Read-only audit. Does NOT modify or regenerate any CSV.

Run from project root:
    python ./python/validation/final_data_audit.py
"""

from pathlib import Path
import sys
import pandas as pd


CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

FILES = {
    "customers": "customers.csv",
    "addresses": "addresses.csv",
    "products": "products.csv",
    "warehouses": "warehouses.csv",
    "inventory": "inventory.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "shipments": "shipments.csv",
    "delivery_attempts": "delivery_attempts.csv",
    "drivers": "drivers.csv",
    "vehicles": "vehicles.csv",
    "delivery_partners": "delivery_partners.csv",
    "returns": "returns.csv",
}

EXPECTED_COLUMNS = {
    "customers": [
        "customer_id", "customer_name", "email", "phone", "gender",
        "customer_segment", "registration_date", "state", "city",
        "pincode", "preferred_payment_method", "is_active",
    ],
    "addresses": [
        "address_id", "customer_id", "address_type", "address_line",
        "city", "state", "pincode", "is_default",
    ],
    "products": [
        "product_id", "product_name", "category", "brand", "unit_price",
        "weight_kg", "supplier", "reorder_level", "is_active",
    ],
    "warehouses": [
        "warehouse_id", "warehouse_name", "warehouse_type", "city",
        "state", "pincode", "capacity_units", "manager_name",
        "operating_hours", "is_active",
    ],
    "inventory": [
        "inventory_id", "warehouse_id", "product_id", "opening_stock",
        "current_stock", "reorder_level", "unit_cost", "inventory_value",
        "stock_status", "last_restock_date",
    ],
    "orders": [
        "order_id", "customer_id", "address_id", "order_date",
        "expected_delivery_date", "delivery_type", "priority",
        "order_status",
    ],
    "order_items": [
        "order_item_id", "order_id", "product_id", "quantity",
        "unit_price", "discount_percent", "discount_amount", "line_total",
    ],
    "payments": [
        "payment_id", "order_id", "payment_date", "payment_method",
        "payment_status", "amount", "transaction_reference",
    ],
    "shipments": [
        "shipment_id", "order_id", "warehouse_id", "delivery_partner_id",
        "shipment_date", "expected_delivery_date", "actual_delivery_date",
        "delivery_type", "shipment_status", "sla_days", "shipping_cost",
        "distance_km",
    ],
    "delivery_attempts": [
        "attempt_id", "shipment_id", "order_id", "attempt_number",
        "attempt_date", "attempt_outcome", "failure_reason", "notes",
    ],
    "drivers": [
        "driver_id", "driver_name", "phone", "license_number",
        "experience_years", "rating", "city", "employment_type", "status",
    ],
    "vehicles": [
        "vehicle_id", "vehicle_number", "vehicle_type", "capacity_kg",
        "fuel_type", "model_year", "driver_id", "status",
    ],
    "delivery_partners": [
        "partner_id", "partner_name", "service_type", "coverage_type",
        "base_cost_per_km", "rating", "contact_phone", "status",
    ],
    "returns": [
        "return_id", "order_id", "order_item_id", "product_id",
        "return_date", "return_quantity", "return_reason",
        "return_status", "return_amount", "refund_amount",
    ],
}

EXPECTED_COUNTS = {
    "customers": 20_000,
    "addresses": 30_000,
    "products": 5_000,
    "warehouses": 30,
    "inventory": 150_000,
    "orders": 100_000,
    "order_items": 299_720,
    "payments": 100_000,
    "shipments": 100_000,
    "drivers": 1_000,
    "vehicles": 1_200,
    "delivery_partners": 25,
    "returns": 15_000,
}

PKS = {
    "customers": "customer_id",
    "addresses": "address_id",
    "products": "product_id",
    "warehouses": "warehouse_id",
    "inventory": "inventory_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "payments": "payment_id",
    "shipments": "shipment_id",
    "delivery_attempts": "attempt_id",
    "drivers": "driver_id",
    "vehicles": "vehicle_id",
    "delivery_partners": "partner_id",
    "returns": "return_id",
}

errors = []
passes = []


def check(name, condition, detail=""):
    if condition:
        passes.append(name)
        print(f"✓ {name}")
    else:
        msg = f"✗ {name}"
        if detail:
            msg += f" — {detail}"
        errors.append(msg)
        print(msg)


def load_all():
    data = {}
    print("\n[1] FILES & SCHEMAS")
    print("-" * 70)

    for table, filename in FILES.items():
        path = RAW_DIR / filename

        if not path.exists():
            check(f"{table}: file exists", False, str(path))
            continue

        try:
            df = pd.read_csv(path)
            data[table] = df
            check(
                f"{table}: file exists and loads",
                True,
                f"{len(df):,} rows",
            )
            missing = set(EXPECTED_COLUMNS[table]) - set(df.columns)
            extra = set(df.columns) - set(EXPECTED_COLUMNS[table])

            check(
                f"{table}: required columns present",
                not missing,
                f"missing={sorted(missing)}" if missing else "",
            )

            if extra:
                print(f"  Note: extra columns = {sorted(extra)}")

        except Exception as exc:
            check(f"{table}: CSV readable", False, repr(exc))

    return data


def validate_counts_and_keys(data):
    print("\n[2] ROW COUNTS & PRIMARY KEYS")
    print("-" * 70)

    for table, expected in EXPECTED_COUNTS.items():
        if table not in data:
            continue
        df = data[table]
        check(
            f"{table}: expected row count",
            len(df) == expected,
            f"expected={expected:,}, actual={len(df):,}",
        )

    for table, pk in PKS.items():
        if table not in data:
            continue
        df = data[table]
        if pk not in df.columns:
            continue

        nulls = df[pk].isna().sum()
        dups = df[pk].duplicated().sum()

        check(
            f"{table}: primary key has no NULLs",
            nulls == 0,
            f"{nulls:,} NULLs",
        )
        check(
            f"{table}: primary key is unique",
            dups == 0,
            f"{dups:,} duplicates",
        )


def validate_master_relationships(data):
    print("\n[3] MASTER-DATA RELATIONSHIPS")
    print("-" * 70)

    customers = data["customers"]
    addresses = data["addresses"]
    products = data["products"]
    warehouses = data["warehouses"]
    inventory = data["inventory"]
    drivers = data["drivers"]
    vehicles = data["vehicles"]
    partners = data["delivery_partners"]

    customer_ids = set(customers["customer_id"].astype(str))
    address_customer_ids = set(addresses["customer_id"].astype(str))
    warehouse_ids = set(warehouses["warehouse_id"].astype(str))
    product_ids = set(products["product_id"].astype(str))
    driver_ids = set(drivers["driver_id"].astype(str))
    partner_ids = set(partners["partner_id"].astype(str))

    orphan_address_customers = address_customer_ids - customer_ids
    missing_customer_addresses = customer_ids - address_customer_ids

    check(
        "addresses → customers foreign keys valid",
        not orphan_address_customers,
        f"{len(orphan_address_customers):,} orphan customer IDs",
    )
    check(
        "every customer has at least one address",
        not missing_customer_addresses,
        f"{len(missing_customer_addresses):,} customers without address",
    )

    inv_warehouse = set(inventory["warehouse_id"].astype(str))
    inv_product = set(inventory["product_id"].astype(str))

    check(
        "inventory → warehouses foreign keys valid",
        inv_warehouse <= warehouse_ids,
        f"{len(inv_warehouse - warehouse_ids):,} orphan warehouse IDs",
    )
    check(
        "inventory → products foreign keys valid",
        inv_product <= product_ids,
        f"{len(inv_product - product_ids):,} orphan product IDs",
    )

    vehicle_driver = set(vehicles["driver_id"].dropna().astype(str))
    check(
        "vehicles → drivers foreign keys valid",
        vehicle_driver <= driver_ids,
        f"{len(vehicle_driver - driver_ids):,} orphan driver IDs",
    )


def validate_transactions(data):
    print("\n[4] TRANSACTIONAL FOREIGN KEYS")
    print("-" * 70)

    customers = data["customers"]
    addresses = data["addresses"]
    products = data["products"]
    warehouses = data["warehouses"]
    orders = data["orders"]
    items = data["order_items"]
    payments = data["payments"]
    shipments = data["shipments"]
    attempts = data["delivery_attempts"]
    returns = data["returns"]
    partners = data["delivery_partners"]

    customer_ids = set(customers["customer_id"].astype(str))
    address_ids = set(addresses["address_id"].astype(str))
    product_ids = set(products["product_id"].astype(str))
    warehouse_ids = set(warehouses["warehouse_id"].astype(str))
    order_ids = set(orders["order_id"].astype(str))
    item_ids = set(items["order_item_id"].astype(str))
    shipment_ids = set(shipments["shipment_id"].astype(str))
    partner_ids = set(partners["partner_id"].astype(str))

    def orphan_count(series, valid):
        return len(set(series.dropna().astype(str)) - valid)

    check(
        "orders → customers",
        orphan_count(orders["customer_id"], customer_ids) == 0,
        f"{orphan_count(orders['customer_id'], customer_ids):,} orphan customer IDs",
    )
    check(
        "orders → addresses",
        orphan_count(orders["address_id"], address_ids) == 0,
        f"{orphan_count(orders['address_id'], address_ids):,} orphan address IDs",
    )
    check(
        "order_items → orders",
        orphan_count(items["order_id"], order_ids) == 0,
        f"{orphan_count(items['order_id'], order_ids):,} orphan order IDs",
    )
    check(
        "order_items → products",
        orphan_count(items["product_id"], product_ids) == 0,
        f"{orphan_count(items['product_id'], product_ids):,} orphan product IDs",
    )
    check(
        "payments → orders",
        orphan_count(payments["order_id"], order_ids) == 0,
        f"{orphan_count(payments['order_id'], order_ids):,} orphan order IDs",
    )
    check(
        "shipments → orders",
        orphan_count(shipments["order_id"], order_ids) == 0,
        f"{orphan_count(shipments['order_id'], order_ids):,} orphan order IDs",
    )
    check(
        "shipments → warehouses",
        orphan_count(shipments["warehouse_id"], warehouse_ids) == 0,
        f"{orphan_count(shipments['warehouse_id'], warehouse_ids):,} orphan warehouse IDs",
    )
    check(
        "shipments → delivery partners",
        orphan_count(shipments["delivery_partner_id"], partner_ids) == 0,
        f"{orphan_count(shipments['delivery_partner_id'], partner_ids):,} orphan partner IDs",
    )
    check(
        "delivery_attempts → shipments",
        orphan_count(attempts["shipment_id"], shipment_ids) == 0,
        f"{orphan_count(attempts['shipment_id'], shipment_ids):,} orphan shipment IDs",
    )
    check(
        "delivery_attempts → orders",
        orphan_count(attempts["order_id"], order_ids) == 0,
        f"{orphan_count(attempts['order_id'], order_ids):,} orphan order IDs",
    )
    check(
        "returns → orders",
        orphan_count(returns["order_id"], order_ids) == 0,
        f"{orphan_count(returns['order_id'], order_ids):,} orphan order IDs",
    )
    check(
        "returns → order_items",
        orphan_count(returns["order_item_id"], item_ids) == 0,
        f"{orphan_count(returns['order_item_id'], item_ids):,} orphan order item IDs",
    )
    check(
        "returns → products",
        orphan_count(returns["product_id"], product_ids) == 0,
        f"{orphan_count(returns['product_id'], product_ids):,} orphan product IDs",
    )


def validate_order_address_customer(data):
    print("\n[5] ORDER → CUSTOMER → ADDRESS CONSISTENCY")
    print("-" * 70)

    orders = data["orders"]
    addresses = data["addresses"]

    address_map = (
        addresses.drop_duplicates("address_id")
        .set_index("address_id")["customer_id"]
        .astype(str)
        .to_dict()
    )

    mismatches = 0
    for row in orders[["customer_id", "address_id"]].itertuples(index=False):
        if str(address_map.get(row.address_id, "")) != str(row.customer_id):
            mismatches += 1

    check(
        "every order address belongs to its order customer",
        mismatches == 0,
        f"{mismatches:,} mismatches",
    )


def validate_revenue_payments(data):
    print("\n[6] REVENUE & PAYMENT RECONCILIATION")
    print("-" * 70)

    orders = data["orders"]
    items = data["order_items"]
    payments = data["payments"]

    item_amounts = (
        items.assign(
            order_id=items["order_id"].astype(str),
            line_total_num=pd.to_numeric(
                items["line_total"], errors="coerce"
            ),
        )
        .groupby("order_id")["line_total_num"]
        .sum()
    )

    payment_amounts = (
        payments.assign(
            order_id=payments["order_id"].astype(str),
            amount_num=pd.to_numeric(
                payments["amount"], errors="coerce"
            ),
        )
        .groupby("order_id")["amount_num"]
        .sum()
    )

    order_ids = orders["order_id"].astype(str)

    missing_item_orders = set(order_ids) - set(item_amounts.index)
    missing_payment_orders = set(order_ids) - set(payment_amounts.index)

    check(
        "every order has order items",
        not missing_item_orders,
        f"{len(missing_item_orders):,} orders without items",
    )
    check(
        "every order has exactly one payment",
        len(payments) == len(orders)
        and payments["order_id"].nunique() == len(orders),
        f"payments={len(payments):,}, unique payment orders={payments['order_id'].nunique():,}",
    )

    common = set(item_amounts.index) & set(payment_amounts.index)
    differences = []

    for oid in common:
        a = round(float(item_amounts.loc[oid]), 2)
        b = round(float(payment_amounts.loc[oid]), 2)
        if abs(a - b) > 0.01:
            differences.append((oid, a, b))

    check(
        "payment amount equals order-item revenue",
        len(differences) == 0,
        f"{len(differences):,} mismatched orders",
    )

    total_items = round(pd.to_numeric(items["line_total"], errors="coerce").sum(), 2)
    total_payments = round(pd.to_numeric(payments["amount"], errors="coerce").sum(), 2)

    check(
        "total payment value equals total line revenue",
        abs(total_items - total_payments) <= 0.01,
        f"items=₹{total_items:,.2f}, payments=₹{total_payments:,.2f}",
    )


def validate_dates(data):
    print("\n[7] DATE CONSISTENCY")
    print("-" * 70)

    orders = data["orders"].copy()
    payments = data["payments"].copy()
    shipments = data["shipments"].copy()
    attempts = data["delivery_attempts"].copy()
    returns = data["returns"].copy()

    for df, cols in [
        (orders, ["order_date", "expected_delivery_date"]),
        (payments, ["payment_date"]),
        (shipments, ["shipment_date", "expected_delivery_date", "actual_delivery_date"]),
        (attempts, ["attempt_date"]),
        (returns, ["return_date"]),
    ]:
        for col in cols:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    invalid_order_dates = (
        orders["order_date"].isna()
        | orders["expected_delivery_date"].isna()
        | (orders["expected_delivery_date"] < orders["order_date"].dt.normalize())
    ).sum()

    check(
        "orders: expected delivery date valid",
        invalid_order_dates == 0,
        f"{invalid_order_dates:,} invalid rows",
    )

    order_dates = orders.set_index("order_id")["order_date"]
    invalid_payment_dates = 0
    for row in payments[["order_id", "payment_date"]].itertuples(index=False):
        od = order_dates.get(row.order_id)
        if pd.isna(od) or pd.isna(row.payment_date):
            invalid_payment_dates += 1
        elif row.payment_date.normalize() < od.normalize():
            invalid_payment_dates += 1

    check(
        "payments: payment date not before order date",
        invalid_payment_dates == 0,
        f"{invalid_payment_dates:,} invalid rows",
    )

    shipment_order_dates = orders.set_index("order_id")["order_date"]
    invalid_ship_dates = 0

    for row in shipments[
        ["order_id", "shipment_date", "actual_delivery_date"]
    ].itertuples(index=False):
        od = shipment_order_dates.get(row.order_id)

        if pd.isna(od) or pd.isna(row.shipment_date):
            invalid_ship_dates += 1
            continue

        if row.shipment_date.normalize() < od.normalize():
            invalid_ship_dates += 1

        if pd.notna(row.actual_delivery_date):
            if row.actual_delivery_date.normalize() < row.shipment_date.normalize():
                invalid_ship_dates += 1

    check(
        "shipments: shipment/actual delivery dates valid",
        invalid_ship_dates == 0,
        f"{invalid_ship_dates:,} invalid rows",
    )

    shipment_dates = shipments.set_index("shipment_id")["shipment_date"]
    invalid_attempt_dates = 0

    for row in attempts[["shipment_id", "attempt_date"]].itertuples(index=False):
        sd = shipment_dates.get(row.shipment_id)
        if pd.isna(sd) or pd.isna(row.attempt_date):
            invalid_attempt_dates += 1
        elif row.attempt_date.normalize() < sd.normalize():
            invalid_attempt_dates += 1

    check(
        "delivery attempts: attempt date not before shipment date",
        invalid_attempt_dates == 0,
        f"{invalid_attempt_dates:,} invalid rows",
    )

    shipment_delivery_dates = shipments.set_index("order_id")["actual_delivery_date"]
    invalid_return_dates = 0

    for row in returns[["order_id", "return_date"]].itertuples(index=False):
        dd = shipment_delivery_dates.get(row.order_id)
        if pd.isna(dd) or pd.isna(row.return_date):
            invalid_return_dates += 1
        elif row.return_date.normalize() <= dd.normalize():
            invalid_return_dates += 1

    check(
        "returns: return date after actual delivery date",
        invalid_return_dates == 0,
        f"{invalid_return_dates:,} invalid rows",
    )


def validate_shipments_attempts(data):
    print("\n[8] SHIPMENT & DELIVERY-ATTEMPT CONSISTENCY")
    print("-" * 70)

    shipments = data["shipments"].copy()
    attempts = data["delivery_attempts"].copy()

    shipments["shipment_id"] = shipments["shipment_id"].astype(str)
    shipments["shipment_status"] = shipments["shipment_status"].astype(str)
    attempts["shipment_id"] = attempts["shipment_id"].astype(str)
    attempts["attempt_outcome"] = attempts["attempt_outcome"].astype(str)
    attempts["attempt_number_num"] = pd.to_numeric(
        attempts["attempt_number"], errors="coerce"
    )

    shipment_ids = set(shipments["shipment_id"])
    attempt_shipments = set(attempts["shipment_id"])

    # Aggregate once; never scan the attempts table inside a shipment loop.
    attempt_summary = (
        attempts.assign(
            delivered=attempts["attempt_outcome"].eq("Delivered")
        )
        .groupby("shipment_id")
        .agg(
            attempt_count=("attempt_number_num", "size"),
            delivered_count=("delivered", "sum"),
        )
    )

    shipment_check = shipments[["shipment_id", "shipment_status"]].copy()
    shipment_check = shipment_check.join(attempt_summary, on="shipment_id")
    shipment_check["attempt_count"] = shipment_check["attempt_count"].fillna(0).astype(int)
    shipment_check["delivered_count"] = shipment_check["delivered_count"].fillna(0).astype(int)

    zero_attempt_statuses = {"Created", "Picked Up", "In Transit"}
    delivered_statuses = {"Delivered", "Delayed"}

    zero_mask = shipment_check["shipment_status"].isin(zero_attempt_statuses)
    zero_attempt_mismatch = int(
        (zero_mask & shipment_check["attempt_count"].ne(0)).sum()
    )

    delivered_mask = shipment_check["shipment_status"].isin(delivered_statuses)
    delivered_attempt_mismatch = int(
        (delivered_mask & shipment_check["delivered_count"].ne(1)).sum()
    )

    failed_mask = shipment_check["shipment_status"].eq("Failed")
    failed_delivered_mismatch = int(
        (failed_mask & shipment_check["delivered_count"].gt(0)).sum()
    )

    check(
        "Created/Picked Up/In Transit shipments have zero attempts",
        zero_attempt_mismatch == 0,
        f"{zero_attempt_mismatch:,} mismatches",
    )
    check(
        "Delivered/Delayed shipments have exactly one Delivered attempt",
        delivered_attempt_mismatch == 0,
        f"{delivered_attempt_mismatch:,} mismatches",
    )
    check(
        "Failed shipments never have Delivered attempt",
        failed_delivered_mismatch == 0,
        f"{failed_delivered_mismatch:,} mismatches",
    )

    # Fully vectorized sequence validation.
    # For each shipment, after sorting by attempt number, expected values are 1..N.
    sequence_check = attempts[["shipment_id", "attempt_number_num"]].copy()
    sequence_check = sequence_check.sort_values(
        ["shipment_id", "attempt_number_num"], kind="stable"
    )
    sequence_check["expected_number"] = (
        sequence_check.groupby("shipment_id", sort=False).cumcount() + 1
    )

    invalid_sequence_rows = (
        sequence_check["attempt_number_num"].isna()
        | sequence_check["attempt_number_num"].ne(sequence_check["expected_number"])
    )

    invalid_sequence_shipments = int(
        sequence_check.loc[invalid_sequence_rows, "shipment_id"].nunique()
    )

    check(
        "delivery attempt numbers are sequential per shipment",
        invalid_sequence_shipments == 0,
        f"{invalid_sequence_shipments:,} shipments with invalid sequences",
    )

    orphan_shipments = attempt_shipments - shipment_ids
    check(
        "delivery attempts reference valid shipments",
        not orphan_shipments,
        f"{len(orphan_shipments):,} orphan shipment references",
    )


def validate_returns(data):
    print("\n[9] RETURNS CONSISTENCY")
    print("-" * 70)

    orders = data["orders"]
    items = data["order_items"]
    shipments = data["shipments"]
    returns = data["returns"]

    item_map = items.set_index("order_item_id")[
        ["order_id", "product_id", "quantity", "unit_price"]
    ]

    invalid_relation = 0
    invalid_qty = 0
    invalid_amount = 0

    for row in returns.itertuples(index=False):
        try:
            item = item_map.loc[row.order_item_id]

            if str(item["order_id"]) != str(row.order_id):
                invalid_relation += 1

            if str(item["product_id"]) != str(row.product_id):
                invalid_relation += 1

            qty = int(row.return_quantity)
            purchased = int(item["quantity"])

            if qty < 1 or qty > purchased:
                invalid_qty += 1

            expected = round(qty * float(item["unit_price"]), 2)
            actual = round(float(row.return_amount), 2)

            if abs(expected - actual) > 0.01:
                invalid_amount += 1

        except KeyError:
            invalid_relation += 1

    check(
        "return order-item-product relationships valid",
        invalid_relation == 0,
        f"{invalid_relation:,} invalid relationships",
    )
    check(
        "return quantity does not exceed purchased quantity",
        invalid_qty == 0,
        f"{invalid_qty:,} invalid quantities",
    )
    check(
        "return amounts match quantity × unit price",
        invalid_amount == 0,
        f"{invalid_amount:,} invalid amounts",
    )

    duplicate_items = returns["order_item_id"].duplicated().sum()
    check(
        "each order item has at most one return",
        duplicate_items == 0,
        f"{duplicate_items:,} duplicate returned order items",
    )

    refund = pd.to_numeric(returns["refund_amount"], errors="coerce")
    amount = pd.to_numeric(returns["return_amount"], errors="coerce")

    invalid_refunds = ((refund < 0) | (refund > amount)).sum()

    check(
        "refund amount is between zero and return amount",
        invalid_refunds == 0,
        f"{invalid_refunds:,} invalid refunds",
    )


def validate_values(data):
    print("\n[10] VALUE & DOMAIN CHECKS")
    print("-" * 70)

    products = data["products"]
    items = data["order_items"]
    payments = data["payments"]
    shipments = data["shipments"]
    inventory = data["inventory"]
    attempts = data["delivery_attempts"]

    checks = [
        (
            "products: unit price non-negative",
            (pd.to_numeric(products["unit_price"], errors="coerce") >= 0).all(),
        ),
        (
            "order items: quantity positive",
            (pd.to_numeric(items["quantity"], errors="coerce") > 0).all(),
        ),
        (
            "order items: unit price non-negative",
            (pd.to_numeric(items["unit_price"], errors="coerce") >= 0).all(),
        ),
        (
            "order items: discount percent 0-100",
            pd.to_numeric(items["discount_percent"], errors="coerce").between(0, 100).all(),
        ),
        (
            "payments: amount non-negative",
            (pd.to_numeric(payments["amount"], errors="coerce") >= 0).all(),
        ),
        (
            "shipments: distance non-negative",
            (pd.to_numeric(shipments["distance_km"], errors="coerce") >= 0).all(),
        ),
        (
            "shipments: shipping cost non-negative",
            (pd.to_numeric(shipments["shipping_cost"], errors="coerce") >= 0).all(),
        ),
        (
            "inventory: current stock non-negative",
            (pd.to_numeric(inventory["current_stock"], errors="coerce") >= 0).all(),
        ),
        (
            "delivery attempts: attempt number positive",
            (pd.to_numeric(attempts["attempt_number"], errors="coerce") > 0).all(),
        ),
    ]

    for name, condition in checks:
        check(name, bool(condition))


def validate_domains(data):
    print("\n[11] STATUS / DOMAIN CONSISTENCY")
    print("-" * 70)

    orders = data["orders"]
    shipments = data["shipments"]
    attempts = data["delivery_attempts"]
    returns = data["returns"]
    payments = data["payments"]

    expected_order_status = {
        "Pending", "Confirmed", "Processing", "Shipped",
        "Delivered", "Cancelled", "Returned",
    }
    expected_delivery_types = {"Standard", "Express", "Same Day"}
    expected_shipment_status = {
        "Created", "Picked Up", "In Transit", "Out for Delivery",
        "Delivered", "Delayed", "Failed",
    }
    expected_attempt_outcomes = {
        "Delivered", "Customer Unavailable", "Wrong Address",
        "Rescheduled", "Failed",
    }
    expected_return_status = {
        "Requested", "Approved", "Picked Up",
        "Received", "Refunded", "Rejected",
    }
    expected_payment_methods = {
        "UPI", "Credit Card", "Debit Card",
        "Net Banking", "Cash on Delivery", "Wallet",
    }
    expected_payment_status = {
        "Paid", "Pending", "Failed", "Refunded",
    }

    def domain_check(df, col, allowed, label):
        actual = set(df[col].dropna().astype(str).unique())
        invalid = actual - allowed
        check(
            label,
            not invalid,
            f"invalid values={sorted(invalid)}",
        )

    domain_check(
        orders, "order_status", expected_order_status,
        "orders: status vocabulary valid",
    )
    domain_check(
        orders, "delivery_type", expected_delivery_types,
        "orders: delivery type vocabulary valid",
    )
    domain_check(
        shipments, "shipment_status", expected_shipment_status,
        "shipments: status vocabulary valid",
    )
    domain_check(
        shipments, "delivery_type", expected_delivery_types,
        "shipments: delivery type vocabulary valid",
    )
    domain_check(
        attempts, "attempt_outcome", expected_attempt_outcomes,
        "delivery attempts: outcome vocabulary valid",
    )
    domain_check(
        returns, "return_status", expected_return_status,
        "returns: status vocabulary valid",
    )
    domain_check(
        payments, "payment_method", expected_payment_methods,
        "payments: method vocabulary valid",
    )
    domain_check(
        payments, "payment_status", expected_payment_status,
        "payments: status vocabulary valid",
    )


def main():
    print("=" * 70)
    print("LOGIX — FINAL RAW DATA CROSS-TABLE AUDIT")
    print("=" * 70)
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Raw data     : {RAW_DIR}")

    data = load_all()

    required_tables = set(FILES)
    missing_tables = required_tables - set(data)

    if missing_tables:
        print("\nAudit cannot continue.")
        print("Missing tables:", sorted(missing_tables))
        sys.exit(1)

    validate_counts_and_keys(data)
    validate_master_relationships(data)
    validate_transactions(data)
    validate_order_address_customer(data)
    validate_revenue_payments(data)
    validate_dates(data)
    validate_shipments_attempts(data)
    validate_returns(data)
    validate_values(data)
    validate_domains(data)

    print("\n" + "=" * 70)
    print("FINAL AUDIT RESULT")
    print("=" * 70)

    print(f"PASS checks : {len(passes)}")
    print(f"FAIL checks : {len(errors)}")

    if errors:
        print("\nFAILED CHECKS:")
        for error in errors:
            print(error)

        print("\n⚠ LOGIX RAW DATASET IS NOT LOCKED.")
        print("Fix the failed checks before moving to MySQL.")
        sys.exit(1)

    print("\n✓ ALL FINAL CROSS-TABLE AUDITS PASSED.")
    print("✓ LOGIX RAW DATASET IS FINAL AND LOCKED.")
    print("✓ Ready for MySQL schema + data loading.")
    print("=" * 70)


if __name__ == "__main__":
    main()
