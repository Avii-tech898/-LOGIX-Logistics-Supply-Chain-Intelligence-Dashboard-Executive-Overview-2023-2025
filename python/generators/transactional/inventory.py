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
    RANDOM_SEED,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = (
    RAW_DATA_DIR
    / "inventory.csv"
)


# ============================================================
# STOCK STATUS
# ============================================================

def get_stock_status(
    current_stock,
    reorder_level
):

    if current_stock == 0:
        return "Out of Stock"

    if current_stock <= reorder_level:
        return "Low Stock"

    return "In Stock"


# ============================================================
# RANDOM DATE
# ============================================================

def random_date():

    start = pd.Timestamp(
        START_DATE
    )

    end = pd.Timestamp(
        END_DATE
    )

    days = (
        end - start
    ).days

    random_days = random.randint(
        0,
        days
    )

    return (
        start
        + pd.Timedelta(
            days=random_days
        )
    )


# ============================================================
# LOAD MASTER DATA
# ============================================================

def load_data():

    products_file = (
        RAW_DATA_DIR
        / "products.csv"
    )

    warehouses_file = (
        RAW_DATA_DIR
        / "warehouses.csv"
    )

    if not products_file.exists():

        raise FileNotFoundError(
            f"Missing file: {products_file}"
        )

    if not warehouses_file.exists():

        raise FileNotFoundError(
            f"Missing file: {warehouses_file}"
        )

    products = pd.read_csv(
        products_file
    )

    warehouses = pd.read_csv(
        warehouses_file
    )

    required_product_columns = {
        "product_id",
        "unit_price",
    }

    required_warehouse_columns = {
        "warehouse_id",
    }

    missing_product_columns = (
        required_product_columns
        - set(products.columns)
    )

    missing_warehouse_columns = (
        required_warehouse_columns
        - set(warehouses.columns)
    )

    if missing_product_columns:

        raise ValueError(
            "products.csv missing columns: "
            f"{sorted(missing_product_columns)}"
        )

    if missing_warehouse_columns:

        raise ValueError(
            "warehouses.csv missing columns: "
            f"{sorted(missing_warehouse_columns)}"
        )

    return products, warehouses


# ============================================================
# GENERATE INVENTORY
# ============================================================

def generate_inventory():

    print()
    print("=" * 70)
    print("LOGIX — INVENTORY DATA GENERATION")
    print("=" * 70)

    products, warehouses = load_data()

    print()
    print(
        f"Products loaded   : "
        f"{len(products):,}"
    )

    print(
        f"Warehouses loaded : "
        f"{len(warehouses):,}"
    )

    # --------------------------------------------------------
    # PREPARE PRODUCTS
    # --------------------------------------------------------

    products["unit_price"] = pd.to_numeric(
        products["unit_price"],
        errors="coerce"
    )

    products = products.dropna(
        subset=[
            "product_id",
            "unit_price"
        ]
    )

    products = products[
        products["unit_price"] > 0
    ].copy()

    product_records = (
        products[
            [
                "product_id",
                "unit_price"
            ]
        ]
        .to_dict("records")
    )

    warehouse_ids = (
        warehouses["warehouse_id"]
        .dropna()
        .tolist()
    )

    if not product_records:

        raise ValueError(
            "No valid products found."
        )

    if not warehouse_ids:

        raise ValueError(
            "No valid warehouses found."
        )

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    inventory = []

    inventory_number = 1

    total_records = (
        len(product_records)
        * len(warehouse_ids)
    )

    print()
    print(
        f"Target inventory records : "
        f"{total_records:,}"
    )

    # --------------------------------------------------------
    # WAREHOUSE × PRODUCT
    # --------------------------------------------------------

    for warehouse_index, warehouse_id in enumerate(
        warehouse_ids,
        start=1
    ):

        for product in product_records:

            product_id = product[
                "product_id"
            ]

            unit_price = float(
                product[
                    "unit_price"
                ]
            )

            # ------------------------------------------------
            # STOCK
            # ------------------------------------------------

            opening_stock = random.randint(
                20,
                500
            )

            reorder_level = random.randint(
                10,
                min(
                    100,
                    opening_stock
                )
            )

            # ------------------------------------------------
            # CURRENT STOCK
            # ------------------------------------------------

            stock_change = random.randint(
                -opening_stock,
                int(
                    opening_stock * 0.50
                )
            )

            current_stock = max(
                0,
                opening_stock
                + stock_change
            )

            # ------------------------------------------------
            # UNIT COST
            # ------------------------------------------------

            cost_factor = random.uniform(
                0.55,
                0.85
            )

            unit_cost = round(
                unit_price
                * cost_factor,
                2
            )

            # ------------------------------------------------
            # INVENTORY VALUE
            # ------------------------------------------------

            inventory_value = round(
                current_stock
                * unit_cost,
                2
            )

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            stock_status = get_stock_status(
                current_stock,
                reorder_level
            )

            # ------------------------------------------------
            # RESTOCK DATE
            # ------------------------------------------------

            last_restock_date = random_date()

            # ------------------------------------------------
            # RECORD
            # ------------------------------------------------

            inventory.append(
                {
                    "inventory_id": (
                        f"INV{inventory_number:07d}"
                    ),
                    "warehouse_id": warehouse_id,
                    "product_id": product_id,
                    "opening_stock": opening_stock,
                    "current_stock": current_stock,
                    "reorder_level": reorder_level,
                    "unit_cost": unit_cost,
                    "inventory_value": inventory_value,
                    "stock_status": stock_status,
                    "last_restock_date":
                        last_restock_date.strftime(
                            "%Y-%m-%d"
                        ),
                }
            )

            inventory_number += 1

        if warehouse_index % 5 == 0:

            generated = (
                warehouse_index
                * len(product_records)
            )

            print(
                f"  Processed "
                f"{warehouse_index:,}/"
                f"{len(warehouse_ids):,} warehouses "
                f"— {generated:,} records..."
            )

    # --------------------------------------------------------
    # DATAFRAME
    # --------------------------------------------------------

    inventory_df = pd.DataFrame(
        inventory
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    inventory_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("INVENTORY GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Inventory records : "
        f"{len(inventory_df):,}"
    )

    print(
        f"Unique warehouses : "
        f"{inventory_df['warehouse_id'].nunique():,}"
    )

    print(
        f"Unique products   : "
        f"{inventory_df['product_id'].nunique():,}"
    )

    print(
        f"Total stock units : "
        f"{inventory_df['current_stock'].sum():,}"
    )

    print(
        f"Total inventory value : ₹"
        f"{inventory_df['inventory_value'].sum():,.2f}"
    )

    print()
    print("Stock Status Distribution:")

    print(
        inventory_df[
            "stock_status"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(f"✓ Saved: {OUTPUT_FILE}")

    print()
    print("=" * 70)
    print("INVENTORY DATA GENERATION COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_inventory()

