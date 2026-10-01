import random
import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[3]

sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from python.config import (
    RAW_DATA_DIR,
    START_DATE,
    END_DATE,
    SHIPMENT_STATUSES,
    DELIVERY_TYPES,
    RANDOM_SEED,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = RAW_DATA_DIR / "shipments.csv"


# ============================================================
# HELPERS
# ============================================================

def choose_shipment_status(order_status):

    order_status = str(order_status).lower()

    if order_status == "cancelled":
        return "Failed"

    if order_status == "pending":
        return random.choices(
            ["Created", "Failed"],
            weights=[90, 10],
            k=1
        )[0]

    if order_status == "confirmed":
        return random.choices(
            ["Created", "Picked Up"],
            weights=[65, 35],
            k=1
        )[0]

    if order_status == "processing":
        return random.choices(
            ["Picked Up", "In Transit"],
            weights=[45, 55],
            k=1
        )[0]

    if order_status == "shipped":
        return random.choices(
            ["In Transit", "Out for Delivery", "Delayed"],
            weights=[55, 30, 15],
            k=1
        )[0]

    if order_status == "delivered":
        return random.choices(
            ["Delivered", "Delayed"],
            weights=[92, 8],
            k=1
        )[0]

    if order_status == "returned":
        return random.choices(
            ["Delivered", "Delayed"],
            weights=[90, 10],
            k=1
        )[0]

    return random.choice(
        SHIPMENT_STATUSES
    )


def choose_delivery_type(order_delivery_type):

    if order_delivery_type in DELIVERY_TYPES:
        return order_delivery_type

    return random.choice(
        DELIVERY_TYPES
    )


def sla_days(delivery_type):

    value = str(delivery_type).lower()

    if "same" in value:
        return 1

    if "express" in value:
        return 3

    return 5


def generate_distance():

    return round(
        random.uniform(
            5,
            1500
        ),
        2
    )


def generate_shipping_cost(
    distance_km,
    base_cost_per_km
):

    handling_charge = random.uniform(
        30,
        150
    )

    cost = (
        distance_km
        * base_cost_per_km
        + handling_charge
    )

    return round(
        cost,
        2
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    orders_file = RAW_DATA_DIR / "orders.csv"
    warehouses_file = RAW_DATA_DIR / "warehouses.csv"
    partners_file = (
        RAW_DATA_DIR
        / "delivery_partners.csv"
    )

    if not orders_file.exists():
        raise FileNotFoundError(
            f"Missing file: {orders_file}"
        )

    if not warehouses_file.exists():
        raise FileNotFoundError(
            f"Missing file: {warehouses_file}"
        )

    if not partners_file.exists():
        raise FileNotFoundError(
            f"Missing file: {partners_file}"
        )

    orders = pd.read_csv(
        orders_file
    )

    warehouses = pd.read_csv(
        warehouses_file
    )

    partners = pd.read_csv(
        partners_file
    )

    return (
        orders,
        warehouses,
        partners
    )


# ============================================================
# GENERATE SHIPMENTS
# ============================================================

def generate_shipments():

    print()
    print("=" * 70)
    print("LOGIX — SHIPMENT DATA GENERATION")
    print("=" * 70)

    orders, warehouses, partners = load_data()

    print()
    print(
        f"Orders loaded     : {len(orders):,}"
    )

    print(
        f"Warehouses loaded : {len(warehouses):,}"
    )

    print(
        f"Partners loaded   : {len(partners):,}"
    )

    # --------------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # --------------------------------------------------------

    required_order_columns = {
        "order_id",
        "order_date",
        "expected_delivery_date",
        "delivery_type",
        "order_status",
    }

    required_warehouse_columns = {
        "warehouse_id"
    }

    required_partner_columns = {
        "partner_id",
        "base_cost_per_km",
    }

    missing_order_columns = (
        required_order_columns
        - set(orders.columns)
    )

    missing_warehouse_columns = (
        required_warehouse_columns
        - set(warehouses.columns)
    )

    missing_partner_columns = (
        required_partner_columns
        - set(partners.columns)
    )

    if missing_order_columns:
        raise ValueError(
            "orders.csv missing columns: "
            f"{sorted(missing_order_columns)}"
        )

    if missing_warehouse_columns:
        raise ValueError(
            "warehouses.csv missing columns: "
            f"{sorted(missing_warehouse_columns)}"
        )

    if missing_partner_columns:
        raise ValueError(
            "delivery_partners.csv missing columns: "
            f"{sorted(missing_partner_columns)}"
        )

    # --------------------------------------------------------
    # MASTER ID LISTS
    # --------------------------------------------------------

    warehouse_ids = (
        warehouses["warehouse_id"]
        .dropna()
        .tolist()
    )

    partner_records = partners[
        ["partner_id", "base_cost_per_km"]
    ].copy()

    partner_records[
        "base_cost_per_km"
    ] = pd.to_numeric(
        partner_records["base_cost_per_km"],
        errors="coerce"
    )

    partner_records = partner_records.dropna(
        subset=[
            "partner_id",
            "base_cost_per_km"
        ]
    )

    if not warehouse_ids:
        raise ValueError(
            "No valid warehouse IDs found."
        )

    if partner_records.empty:
        raise ValueError(
            "No valid delivery partners found."
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    shipments = []

    for shipment_number, row in enumerate(
        orders.itertuples(index=False),
        start=1
    ):

        shipment_id = (
            f"SHIP{shipment_number:06d}"
        )

        order_date = pd.to_datetime(
            row.order_date
        )

        order_expected_date = pd.to_datetime(
            row.expected_delivery_date
        )

        delivery_type = choose_delivery_type(
            row.delivery_type
        )

        status = choose_shipment_status(
            row.order_status
        )

        sla = sla_days(
            delivery_type
        )

        # ----------------------------------------------------
        # SHIPMENT DATE
        # ----------------------------------------------------

        pickup_delay = random.randint(
            0,
            2
        )

        shipment_date = (
            order_date
            + pd.Timedelta(
                days=pickup_delay
            )
        )

        # ----------------------------------------------------
        # EXPECTED DELIVERY
        # ----------------------------------------------------

        sla_expected_date = (
            shipment_date
            + pd.Timedelta(
                days=sla
            )
        )

        # Use the later of order expected date and SLA date
        expected_delivery_date = max(
            order_expected_date,
            sla_expected_date
        )

        # ----------------------------------------------------
        # ACTUAL DELIVERY
        # ----------------------------------------------------

        actual_delivery_date = None

        if status in {
            "Delivered",
            "Delayed"
        }:

            if status == "Delivered":

                delivery_delay = random.randint(
                    0,
                    2
                )

            else:

                delivery_delay = random.randint(
                    3,
                    8
                )

            actual_delivery_date = (
                shipment_date
                + pd.Timedelta(
                    days=sla
                    + delivery_delay
                )
            )

            # Never allow actual delivery before shipment.
            if actual_delivery_date < shipment_date:
                actual_delivery_date = shipment_date

        # ----------------------------------------------------
        # DISTANCE
        # ----------------------------------------------------

        distance_km = generate_distance()

        # ----------------------------------------------------
        # DELIVERY PARTNER
        # ----------------------------------------------------

        partner_row = partner_records.sample(
            n=1,
            random_state=random.randint(
                1,
                1_000_000
            )
        ).iloc[0]

        partner_id = partner_row[
            "partner_id"
        ]

        base_cost_per_km = float(
            partner_row[
                "base_cost_per_km"
            ]
        )

        # ----------------------------------------------------
        # SHIPPING COST
        # ----------------------------------------------------

        shipping_cost = (
            generate_shipping_cost(
                distance_km,
                base_cost_per_km
            )
        )

        # ----------------------------------------------------
        # RECORD
        # ----------------------------------------------------

        shipments.append(
            {
                "shipment_id": shipment_id,
                "order_id": row.order_id,
                "warehouse_id": random.choice(
                    warehouse_ids
                ),
                "delivery_partner_id": partner_id,
                "shipment_date": shipment_date.strftime(
                    "%Y-%m-%d"
                ),
                "expected_delivery_date":
                    expected_delivery_date.strftime(
                        "%Y-%m-%d"
                    ),
                "actual_delivery_date": (
                    actual_delivery_date.strftime(
                        "%Y-%m-%d"
                    )
                    if actual_delivery_date
                    is not None
                    else None
                ),
                "delivery_type": delivery_type,
                "shipment_status": status,
                "sla_days": sla,
                "shipping_cost": shipping_cost,
                "distance_km": distance_km,
            }
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        if shipment_number % 10_000 == 0:

            print(
                f"  Generated "
                f"{shipment_number:,}/"
                f"{len(orders):,} shipments..."
            )

    # --------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------

    shipments_df = pd.DataFrame(
        shipments
    )

    # --------------------------------------------------------
    # INTEGRITY VALIDATION
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("SHIPMENT INTEGRITY VALIDATION")
    print("-" * 70)

    # Count
    if len(shipments_df) != len(orders):
        raise ValueError(
            "Shipment count does not match order count."
        )
    print("✓ Shipment count matches order count.")

    # Shipment IDs
    if shipments_df["shipment_id"].isna().any():
        raise ValueError("Missing shipment_id detected.")

    if shipments_df["shipment_id"].duplicated().any():
        raise ValueError("Duplicate shipment_id detected.")

    print("✓ Shipment IDs are unique.")

    # One shipment per order and exact order coverage
    if shipments_df["order_id"].isna().any():
        raise ValueError("Missing order_id detected.")

    if shipments_df["order_id"].duplicated().any():
        raise ValueError(
            "Multiple shipments found for the same order."
        )

    order_ids = set(orders["order_id"].astype(str))
    shipment_order_ids = set(shipments_df["order_id"].astype(str))

    if order_ids != shipment_order_ids:
        raise ValueError(
            "Shipment order relationship mismatch."
        )

    print("✓ Every order has exactly one shipment.")

    # Foreign keys
    warehouse_ids_set = set(
        warehouses["warehouse_id"].dropna().astype(str)
    )
    invalid_warehouses = (
        set(shipments_df["warehouse_id"].astype(str))
        - warehouse_ids_set
    )
    if invalid_warehouses:
        raise ValueError(
            f"Invalid warehouse IDs found: "
            f"{list(invalid_warehouses)[:10]}"
        )
    print("✓ Warehouse foreign keys valid.")

    partner_ids_set = set(
        partners["partner_id"].dropna().astype(str)
    )
    invalid_partners = (
        set(shipments_df["delivery_partner_id"].astype(str))
        - partner_ids_set
    )
    if invalid_partners:
        raise ValueError(
            f"Invalid delivery partner IDs found: "
            f"{list(invalid_partners)[:10]}"
        )
    print("✓ Delivery partner foreign keys valid.")

    # Date validation using direct order_id mapping.
    # No DataFrame merge is used.
    order_date_map = dict(
        zip(
            orders["order_id"].astype(str),
            pd.to_datetime(
                orders["order_date"],
                errors="coerce"
            ).dt.normalize()
        )
    )

    shipment_order_date = (
        shipments_df["order_id"]
        .astype(str)
        .map(order_date_map)
    )

    shipment_dates = pd.to_datetime(
        shipments_df["shipment_date"],
        errors="coerce"
    ).dt.normalize()

    expected_dates = pd.to_datetime(
        shipments_df["expected_delivery_date"],
        errors="coerce"
    ).dt.normalize()

    actual_dates = pd.to_datetime(
        shipments_df["actual_delivery_date"],
        errors="coerce"
    ).dt.normalize()

    if shipment_dates.isna().any():
        raise ValueError("Invalid shipment_date detected.")

    if expected_dates.isna().any():
        raise ValueError(
            "Invalid expected_delivery_date detected."
        )

    if shipment_order_date.isna().any():
        raise ValueError(
            "Could not match shipment orders to order dates."
        )

    if (shipment_dates < shipment_order_date).any():
        raise ValueError(
            "Shipment date occurs before order date."
        )

    print("✓ Shipment dates are valid.")

    if (expected_dates < shipment_dates).any():
        raise ValueError(
            "Expected delivery date occurs before shipment date."
        )

    print("✓ Expected delivery dates are valid.")

    # Delivery type and SLA
    invalid_delivery_types = (
        set(shipments_df["delivery_type"])
        - set(DELIVERY_TYPES)
    )
    if invalid_delivery_types:
        raise ValueError(
            f"Invalid delivery types: {invalid_delivery_types}"
        )

    expected_sla = {
        "Standard": 5,
        "Express": 3,
        "Same Day": 1,
    }

    invalid_sla = shipments_df.apply(
        lambda row: row["sla_days"] != expected_sla.get(
            row["delivery_type"], -1
        ),
        axis=1
    )

    if invalid_sla.any():
        raise ValueError("Invalid SLA mapping detected.")

    print("✓ SLA mapping is valid.")

    # Shipment status
    invalid_statuses = (
        set(shipments_df["shipment_status"])
        - set(SHIPMENT_STATUSES)
    )
    if invalid_statuses:
        raise ValueError(
            f"Invalid shipment statuses: {invalid_statuses}"
        )

    print("✓ Shipment statuses are valid.")

    # Actual delivery date/status relationship
    delivered_mask = shipments_df["shipment_status"].isin(
        {"Delivered", "Delayed"}
    )

    if (
        delivered_mask
        & actual_dates.isna()
    ).any():
        raise ValueError(
            "Delivered/Delayed shipments contain "
            "missing actual_delivery_date."
        )

    if (
        ~delivered_mask
        & actual_dates.notna()
    ).any():
        raise ValueError(
            "Non-delivered shipments contain "
            "actual_delivery_date."
        )

    if (
        delivered_mask
        & (actual_dates < shipment_dates)
    ).any():
        raise ValueError(
            "Actual delivery date occurs before shipment date."
        )

    print(
        "✓ Actual delivery date/status relationship valid."
    )

    # Numeric validation
    if (shipments_df["distance_km"] <= 0).any():
        raise ValueError("Non-positive distance detected.")

    if (shipments_df["shipping_cost"] <= 0).any():
        raise ValueError("Non-positive shipping cost detected.")

    print("✓ Distance and shipping costs are valid.")
    print("✓ All shipment integrity checks passed.")

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    shipments_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("SHIPMENT GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Shipments generated : "
        f"{len(shipments_df):,}"
    )

    print(
        f"Unique shipments    : "
        f"{shipments_df['shipment_id'].nunique():,}"
    )

    print(
        f"Unique orders       : "
        f"{shipments_df['order_id'].nunique():,}"
    )

    print(
        f"Total distance      : "
        f"{shipments_df['distance_km'].sum():,.2f} km"
    )

    print(
        f"Total shipping cost : ₹"
        f"{shipments_df['shipping_cost'].sum():,.2f}"
    )

    print()
    print("Shipment Status Distribution:")

    print(
        shipments_df[
            "shipment_status"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print("Delivery Type Distribution:")

    print(
        shipments_df[
            "delivery_type"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(f"✓ Saved: {OUTPUT_FILE}")

    print()
    print("=" * 70)
    print("SHIPMENT DATA GENERATION COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_shipments()