import random
import sys
from pathlib import Path

import pandas as pd


# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[3]

sys.path.insert(0, str(PROJECT_ROOT))


# ------------------------------------------------------------
# PROJECT IMPORTS
# ------------------------------------------------------------

from python.config import (
    RAW_DATA_DIR,
    START_DATE,
    END_DATE,
    NUM_ORDERS,
    ORDER_STATUSES,
    DELIVERY_TYPES,
    RANDOM_SEED,
)


# ------------------------------------------------------------
# REPRODUCIBILITY
# ------------------------------------------------------------

random.seed(RANDOM_SEED)


# ------------------------------------------------------------
# CONSTANTS
# ------------------------------------------------------------

OUTPUT_FILE = RAW_DATA_DIR / "orders.csv"


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def random_datetime(start_date: str, end_date: str) -> pd.Timestamp:
    """
    Generate a random datetime between start_date and end_date.
    """

    start = pd.Timestamp(start_date)

    end = (
        pd.Timestamp(end_date)
        + pd.Timedelta(days=1)
        - pd.Timedelta(seconds=1)
    )

    total_seconds = int(
        (end - start).total_seconds()
    )

    random_seconds = random.randint(
        0,
        total_seconds
    )

    return start + pd.Timedelta(
        seconds=random_seconds
    )


def choose_order_status() -> str:
    """
    Choose order status using realistic business probabilities.
    """

    weights = []

    for status in ORDER_STATUSES:

        status_lower = status.lower()

        if status_lower == "delivered":
            weights.append(62)

        elif status_lower == "shipped":
            weights.append(12)

        elif status_lower == "processing":
            weights.append(8)

        elif status_lower == "confirmed":
            weights.append(7)

        elif status_lower == "pending":
            weights.append(4)

        elif status_lower == "cancelled":
            weights.append(4)

        elif status_lower == "returned":
            weights.append(3)

        else:
            weights.append(1)

    return random.choices(
        ORDER_STATUSES,
        weights=weights,
        k=1
    )[0]


def choose_delivery_type() -> str:
    """
    Choose delivery type.
    """

    weights = []

    for delivery_type in DELIVERY_TYPES:

        value = delivery_type.lower()

        if "standard" in value:
            weights.append(70)

        elif "express" in value:
            weights.append(25)

        elif "same" in value:
            weights.append(5)

        else:
            weights.append(1)

    return random.choices(
        DELIVERY_TYPES,
        weights=weights,
        k=1
    )[0]


def delivery_days(delivery_type: str) -> int:
    """
    Expected delivery duration based on delivery type.
    """

    value = delivery_type.lower()

    if "same" in value:
        return 1

    if "express" in value:
        return 3

    return 5


# ------------------------------------------------------------
# LOAD MASTER DATA
# ------------------------------------------------------------

def load_master_data():

    customers_file = RAW_DATA_DIR / "customers.csv"
    addresses_file = RAW_DATA_DIR / "addresses.csv"

    if not customers_file.exists():
        raise FileNotFoundError(
            f"Missing master file: {customers_file}"
        )

    if not addresses_file.exists():
        raise FileNotFoundError(
            f"Missing master file: {addresses_file}"
        )

    customers = pd.read_csv(
        customers_file
    )

    addresses = pd.read_csv(
        addresses_file
    )

    required_customer_columns = {
        "customer_id"
    }

    required_address_columns = {
        "address_id",
        "customer_id"
    }

    missing_customer_columns = (
        required_customer_columns
        - set(customers.columns)
    )

    missing_address_columns = (
        required_address_columns
        - set(addresses.columns)
    )

    if missing_customer_columns:
        raise ValueError(
            f"customers.csv missing columns: "
            f"{sorted(missing_customer_columns)}"
        )

    if missing_address_columns:
        raise ValueError(
            f"addresses.csv missing columns: "
            f"{sorted(missing_address_columns)}"
        )

    return customers, addresses


# ------------------------------------------------------------
# GENERATE ORDERS
# ------------------------------------------------------------

def generate_orders():

    print()
    print("=" * 70)
    print("LOGIX — ORDER DATA GENERATION")
    print("=" * 70)

    customers, addresses = load_master_data()

    print()
    print(
        f"Customers loaded : {len(customers):,}"
    )

    print(
        f"Addresses loaded : {len(addresses):,}"
    )

    print(
        f"Orders required  : {NUM_ORDERS:,}"
    )

    # --------------------------------------------------------
    # CUSTOMER → ADDRESS MAPPING
    # --------------------------------------------------------

    valid_addresses = addresses[
        addresses["customer_id"].isin(
            customers["customer_id"]
        )
    ].copy()

    if valid_addresses.empty:
        raise ValueError(
            "No valid customer-address relationships found."
        )

    customer_address_map = (
        valid_addresses
        .groupby("customer_id")["address_id"]
        .apply(list)
        .to_dict()
    )

    customer_ids = customers[
        "customer_id"
    ].tolist()

    # --------------------------------------------------------
    # IMPORTANT INTEGRITY CHECK
    # --------------------------------------------------------

    customers_without_address = [
        customer_id
        for customer_id in customer_ids
        if customer_id not in customer_address_map
    ]

    if customers_without_address:

        sample = customers_without_address[:10]

        raise ValueError(
            f"{len(customers_without_address):,} customers "
            f"have no address. Sample: {sample}"
        )

    print(
        f"Customers with address : "
        f"{len(customer_address_map):,}"
    )

    # --------------------------------------------------------
    # GENERATE ROWS
    # --------------------------------------------------------

    orders = []

    for order_number in range(
        1,
        NUM_ORDERS + 1
    ):

        order_id = (
            f"ORD{order_number:06d}"
        )

        # ----------------------------------------------------
        # CUSTOMER
        # ----------------------------------------------------

        customer_id = random.choice(
            customer_ids
        )

        # ----------------------------------------------------
        # CUSTOMER ADDRESS
        # ----------------------------------------------------

        customer_addresses = (
            customer_address_map[customer_id]
        )

        address_id = random.choice(
            customer_addresses
        )

        # ----------------------------------------------------
        # ORDER DATE
        # ----------------------------------------------------

        order_datetime = random_datetime(
            START_DATE,
            END_DATE
        )

        # ----------------------------------------------------
        # DELIVERY TYPE
        # ----------------------------------------------------

        delivery_type = choose_delivery_type()

        # ----------------------------------------------------
        # ORDER STATUS
        # ----------------------------------------------------

        order_status = choose_order_status()

        # ----------------------------------------------------
        # EXPECTED DELIVERY
        # ----------------------------------------------------

        expected_days = delivery_days(
            delivery_type
        )

        expected_delivery_date = (
            order_datetime.normalize()
            + pd.Timedelta(days=expected_days)
        )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        if "same" in delivery_type.lower():

            priority = "High"

        elif "express" in delivery_type.lower():

            priority = random.choices(
                ["Medium", "High"],
                weights=[60, 40],
                k=1
            )[0]

        else:

            priority = random.choices(
                ["Low", "Medium"],
                weights=[70, 30],
                k=1
            )[0]

        # ----------------------------------------------------
        # APPEND
        # ----------------------------------------------------

        orders.append(
            {
                "order_id":
                    order_id,

                "customer_id":
                    customer_id,

                "address_id":
                    address_id,

                "order_date":
                    order_datetime.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "expected_delivery_date":
                    expected_delivery_date.strftime(
                        "%Y-%m-%d"
                    ),

                "delivery_type":
                    delivery_type,

                "priority":
                    priority,

                "order_status":
                    order_status,
            }
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        if order_number % 10_000 == 0:

            print(
                f"  Generated "
                f"{order_number:,} orders..."
            )

    # --------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------

    orders_df = pd.DataFrame(
        orders
    )

    # --------------------------------------------------------
    # INTEGRITY CHECKS
    # --------------------------------------------------------

    if len(orders_df) != NUM_ORDERS:

        raise ValueError(
            f"Expected {NUM_ORDERS:,} orders, "
            f"generated {len(orders_df):,}"
        )

    if orders_df["order_id"].nunique() != NUM_ORDERS:

        raise ValueError(
            "Duplicate order IDs detected."
        )

    # Verify every order's address belongs to its customer

    address_lookup = (
        valid_addresses
        .set_index("address_id")["customer_id"]
        .to_dict()
    )

    mismatches = (
        orders_df["address_id"]
        .map(address_lookup)
        != orders_df["customer_id"]
    )

    if mismatches.any():

        raise ValueError(
            f"Customer-address integrity failed: "
            f"{mismatches.sum():,} mismatches."
        )

    # Verify expected delivery date is never before order date

    order_dates = pd.to_datetime(
        orders_df["order_date"]
    )

    expected_dates = pd.to_datetime(
        orders_df["expected_delivery_date"]
    )

    invalid_dates = (
        expected_dates.dt.normalize()
        < order_dates.dt.normalize()
    )

    if invalid_dates.any():

        raise ValueError(
            f"Invalid expected delivery dates: "
            f"{invalid_dates.sum():,} rows."
        )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    orders_df = orders_df.sort_values(
        by="order_date"
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    orders_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ORDER GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Orders generated : "
        f"{len(orders_df):,}"
    )

    print(
        f"Unique orders    : "
        f"{orders_df['order_id'].nunique():,}"
    )

    print(
        f"Unique customers : "
        f"{orders_df['customer_id'].nunique():,}"
    )

    print()
    print("Order Status Distribution:")

    print(
        orders_df[
            "order_status"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print("Delivery Type Distribution:")

    print(
        orders_df[
            "delivery_type"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(
        f"✓ Saved: {OUTPUT_FILE}"
    )

    print()
    print("=" * 70)
    print("ORDER DATA GENERATION COMPLETED")
    print("=" * 70)


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    generate_orders()