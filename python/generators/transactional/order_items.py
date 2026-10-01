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
    NUM_ORDERS,
    MIN_ITEMS_PER_ORDER,
    MAX_ITEMS_PER_ORDER,
    RANDOM_SEED,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = RAW_DATA_DIR / "order_items.csv"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def choose_quantity():
    """
    Generate realistic item quantity.
    """

    return random.choices(
        [1, 2, 3, 4, 5, 6],
        weights=[65, 20, 8, 4, 2, 1],
        k=1
    )[0]


def choose_discount():
    """
    Generate realistic discount percentage.
    """

    return random.choices(
        [0, 5, 10, 15, 20, 25, 30],
        weights=[35, 20, 18, 12, 8, 5, 2],
        k=1
    )[0]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    orders_file = RAW_DATA_DIR / "orders.csv"
    products_file = RAW_DATA_DIR / "products.csv"

    if not orders_file.exists():
        raise FileNotFoundError(
            f"Missing file: {orders_file}"
        )

    if not products_file.exists():
        raise FileNotFoundError(
            f"Missing file: {products_file}"
        )

    orders = pd.read_csv(
        orders_file
    )

    products = pd.read_csv(
        products_file
    )

    required_order_columns = {
        "order_id"
    }

    required_product_columns = {
        "product_id",
        "unit_price"
    }

    missing_order_columns = (
        required_order_columns
        - set(orders.columns)
    )

    missing_product_columns = (
        required_product_columns
        - set(products.columns)
    )

    if missing_order_columns:
        raise ValueError(
            "orders.csv missing columns: "
            f"{sorted(missing_order_columns)}"
        )

    if missing_product_columns:
        raise ValueError(
            "products.csv missing columns: "
            f"{sorted(missing_product_columns)}"
        )

    return orders, products


# ============================================================
# GENERATE ORDER ITEMS
# ============================================================

def generate_order_items():

    print()
    print("=" * 70)
    print("LOGIX — ORDER ITEMS DATA GENERATION")
    print("=" * 70)

    orders, products = load_data()

    print()
    print(
        f"Orders loaded   : "
        f"{len(orders):,}"
    )

    print(
        f"Products loaded : "
        f"{len(products):,}"
    )

    # --------------------------------------------------------
    # ORDER VALIDATION
    # --------------------------------------------------------

    if orders["order_id"].isna().any():
        raise ValueError(
            "orders.csv contains missing order_id values."
        )

    if orders["order_id"].duplicated().any():
        raise ValueError(
            "orders.csv contains duplicate order_id values."
        )

    if len(orders) != NUM_ORDERS:
        raise ValueError(
            f"Expected {NUM_ORDERS:,} orders, "
            f"but found {len(orders):,}."
        )

    # --------------------------------------------------------
    # PRODUCT DATA
    # --------------------------------------------------------

    product_records = products[
        ["product_id", "unit_price"]
    ].copy()

    product_records["unit_price"] = pd.to_numeric(
        product_records["unit_price"],
        errors="coerce"
    )

    product_records = product_records.dropna(
        subset=[
            "product_id",
            "unit_price"
        ]
    )

    product_records = product_records[
        product_records["unit_price"] > 0
    ]

    if product_records.empty:
        raise ValueError(
            "No valid products with positive "
            "unit_price found."
        )

    if product_records["product_id"].duplicated().any():
        raise ValueError(
            "Duplicate product_id values found "
            "in products.csv."
        )

    product_ids = (
        product_records["product_id"]
        .tolist()
    )

    # --------------------------------------------------------
    # PRICE MAP
    # --------------------------------------------------------
    # Store price as integer paise/cents.
    # This eliminates floating-point calculation issues.
    # --------------------------------------------------------

    product_price_map = {}

    for product_id, price in zip(
        product_records["product_id"],
        product_records["unit_price"]
    ):

        price_paise = int(
            round(float(price) * 100)
        )

        if price_paise <= 0:
            continue

        product_price_map[
            product_id
        ] = price_paise

    product_ids = list(
        product_price_map.keys()
    )

    if len(product_ids) < MIN_ITEMS_PER_ORDER:
        raise ValueError(
            "Number of valid products is smaller "
            "than MIN_ITEMS_PER_ORDER."
        )

    # --------------------------------------------------------
    # GENERATE ITEMS
    # --------------------------------------------------------

    order_items = []

    item_number = 1

    total_orders = len(orders)

    for order_index, order_id in enumerate(
        orders["order_id"],
        start=1
    ):

        # ----------------------------------------------------
        # NUMBER OF PRODUCTS
        # ----------------------------------------------------

        number_of_items = random.randint(
            MIN_ITEMS_PER_ORDER,
            MAX_ITEMS_PER_ORDER
        )

        number_of_items = min(
            number_of_items,
            len(product_ids)
        )

        selected_products = random.sample(
            product_ids,
            number_of_items
        )

        # ----------------------------------------------------
        # GENERATE EACH ITEM
        # ----------------------------------------------------

        for product_id in selected_products:

            quantity = choose_quantity()

            unit_price_paise = (
                product_price_map[
                    product_id
                ]
            )

            discount_percent = (
                choose_discount()
            )

            # ------------------------------------------------
            # FINANCIAL CALCULATIONS
            # ALL CALCULATIONS ARE IN PAISE
            # ------------------------------------------------

            gross_paise = (
                quantity
                * unit_price_paise
            )

            discount_paise = (
                gross_paise
                * discount_percent
                // 100
            )

            line_total_paise = (
                gross_paise
                - discount_paise
            )

            # ------------------------------------------------
            # CONVERT TO RUPEES ONLY FOR STORAGE
            # ------------------------------------------------

            unit_price = (
                unit_price_paise / 100
            )

            discount_amount = (
                discount_paise / 100
            )

            line_total = (
                line_total_paise / 100
            )

            # ------------------------------------------------
            # APPEND
            # ------------------------------------------------

            order_items.append(
                {
                    "order_item_id":
                        f"ITEM{item_number:07d}",

                    "order_id":
                        order_id,

                    "product_id":
                        product_id,

                    "quantity":
                        quantity,

                    "unit_price":
                        round(
                            unit_price,
                            2
                        ),

                    "discount_percent":
                        discount_percent,

                    "discount_amount":
                        round(
                            discount_amount,
                            2
                        ),

                    "line_total":
                        round(
                            line_total,
                            2
                        ),
                }
            )

            item_number += 1

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        if order_index % 10_000 == 0:

            print(
                f"  Processed "
                f"{order_index:,}/"
                f"{total_orders:,} "
                f"orders..."
            )

    # --------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------

    order_items_df = pd.DataFrame(
        order_items
    )

    if order_items_df.empty:
        raise ValueError(
            "No order items were generated."
        )

    # --------------------------------------------------------
    # ITEM ID VALIDATION
    # --------------------------------------------------------

    if (
        order_items_df["order_item_id"]
        .duplicated()
        .any()
    ):

        raise ValueError(
            "Duplicate order_item_id detected."
        )

    # --------------------------------------------------------
    # ORDER RELATIONSHIP VALIDATION
    # --------------------------------------------------------

    order_id_set = set(
        orders["order_id"]
    )

    invalid_orders = (
        set(
            order_items_df["order_id"]
        )
        - order_id_set
    )

    if invalid_orders:
        raise ValueError(
            f"Invalid order IDs found: "
            f"{len(invalid_orders):,}"
        )

    orders_with_items = (
        order_items_df["order_id"]
        .nunique()
    )

    if orders_with_items != len(orders):

        missing_orders = (
            order_id_set
            - set(
                order_items_df["order_id"]
            )
        )

        raise ValueError(
            f"{len(missing_orders):,} orders "
            f"have no order items."
        )

    # --------------------------------------------------------
    # PRODUCT RELATIONSHIP VALIDATION
    # --------------------------------------------------------

    invalid_products = (
        set(
            order_items_df["product_id"]
        )
        - set(product_ids)
    )

    if invalid_products:
        raise ValueError(
            f"Invalid product IDs found: "
            f"{len(invalid_products):,}"
        )

    # --------------------------------------------------------
    # QUANTITY VALIDATION
    # --------------------------------------------------------

    if (
        order_items_df["quantity"] <= 0
    ).any():

        raise ValueError(
            "Invalid quantity detected."
        )

    # --------------------------------------------------------
    # PRICE VALIDATION
    # --------------------------------------------------------

    if (
        order_items_df["unit_price"] <= 0
    ).any():

        raise ValueError(
            "Invalid unit_price detected."
        )

    # --------------------------------------------------------
    # DISCOUNT VALIDATION
    # --------------------------------------------------------

    if (
        (order_items_df["discount_percent"] < 0)
        |
        (order_items_df["discount_percent"] > 100)
    ).any():

        raise ValueError(
            "Invalid discount percentage detected."
        )

    # --------------------------------------------------------
    # FINANCIAL VALIDATION
    # --------------------------------------------------------
    # Recalculate in paise, exactly like generation.
    # --------------------------------------------------------

    validation_unit_price_paise = (
        (
            order_items_df["unit_price"]
            * 100
        )
        .round()
        .astype("int64")
    )

    validation_gross_paise = (
        order_items_df["quantity"]
        * validation_unit_price_paise
    )

    validation_discount_paise = (
        validation_gross_paise
        * order_items_df["discount_percent"]
        // 100
    )

    validation_line_total_paise = (
        validation_gross_paise
        - validation_discount_paise
    )

    stored_discount_paise = (
        (
            order_items_df[
                "discount_amount"
            ]
            * 100
        )
        .round()
        .astype("int64")
    )

    stored_line_total_paise = (
        (
            order_items_df[
                "line_total"
            ]
            * 100
        )
        .round()
        .astype("int64")
    )

    # --------------------------------------------------------
    # DISCOUNT CHECK
    # --------------------------------------------------------

    discount_mismatch = (
        validation_discount_paise
        != stored_discount_paise
    )

    if discount_mismatch.any():

        raise ValueError(
            "Discount calculation mismatch "
            f"detected in "
            f"{discount_mismatch.sum():,} rows."
        )

    # --------------------------------------------------------
    # LINE TOTAL CHECK
    # --------------------------------------------------------

    line_total_mismatch = (
        validation_line_total_paise
        != stored_line_total_paise
    )

    if line_total_mismatch.any():

        raise ValueError(
            "Line total calculation mismatch "
            f"detected in "
            f"{line_total_mismatch.sum():,} rows."
        )

    # --------------------------------------------------------
    # NEGATIVE FINANCIAL VALUE CHECK
    # --------------------------------------------------------

    if (
        validation_line_total_paise < 0
    ).any():

        raise ValueError(
            "Negative line_total detected."
        )

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    order_items_df = (
        order_items_df
        .sort_values(
            by=[
                "order_id",
                "order_item_id"
            ]
        )
        .reset_index(
            drop=True
        )
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    order_items_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ORDER ITEMS GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Order items generated : "
        f"{len(order_items_df):,}"
    )

    print(
        f"Unique order IDs      : "
        f"{order_items_df['order_id'].nunique():,}"
    )

    print(
        f"Unique product IDs    : "
        f"{order_items_df['product_id'].nunique():,}"
    )

    print(
        f"Total quantity        : "
        f"{order_items_df['quantity'].sum():,}"
    )

    total_gross = (
        order_items_df["quantity"]
        * order_items_df["unit_price"]
    ).sum()

    print(
        f"Total gross value     : ₹"
        f"{total_gross:,.2f}"
    )

    print(
        f"Total discount        : ₹"
        f"{order_items_df['discount_amount'].sum():,.2f}"
    )

    print(
        f"Total line revenue    : ₹"
        f"{order_items_df['line_total'].sum():,.2f}"
    )

    print()
    print(
        "Items per order distribution:"
    )

    items_per_order = (
        order_items_df
        .groupby("order_id")
        .size()
        .value_counts()
        .sort_index()
    )

    print(
        items_per_order.to_string()
    )

    print()
    print(
        "✓ All integrity checks passed."
    )

    print(
        f"✓ Saved: {OUTPUT_FILE}"
    )

    print()
    print("=" * 70)
    print(
        "ORDER ITEMS DATA GENERATION COMPLETED"
    )
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generate_order_items()