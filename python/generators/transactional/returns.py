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
    RETURN_REASONS,
    RANDOM_SEED,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = RAW_DATA_DIR / "returns.csv"


# ============================================================
# RETURN STATUS
# ============================================================

RETURN_STATUSES = [
    "Requested",
    "Approved",
    "Picked Up",
    "Received",
    "Refunded",
    "Rejected",
]

RETURN_STATUS_WEIGHTS = [
    8,
    12,
    8,
    10,
    57,
    5,
]


# ============================================================
# RETURN QUANTITY
# ============================================================

def choose_return_quantity(purchased_quantity: int) -> int:
    if purchased_quantity <= 1:
        return 1
    return random.randint(1, purchased_quantity)


# ============================================================
# RETURN STATUS
# ============================================================

def choose_return_status() -> str:
    return random.choices(
        RETURN_STATUSES,
        weights=RETURN_STATUS_WEIGHTS,
        k=1,
    )[0]


# ============================================================
# RETURN REASON
# ============================================================

def choose_return_reason() -> str:
    if not RETURN_REASONS:
        return "Other"
    return random.choice(RETURN_REASONS)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    orders_file = RAW_DATA_DIR / "orders.csv"
    items_file = RAW_DATA_DIR / "order_items.csv"
    shipments_file = RAW_DATA_DIR / "shipments.csv"

    for file_path in (orders_file, items_file, shipments_file):
        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

    orders = pd.read_csv(orders_file)
    order_items = pd.read_csv(items_file)
    shipments = pd.read_csv(shipments_file)

    return orders, order_items, shipments


# ============================================================
# VALIDATE INPUT DATA
# ============================================================

def validate_input_data(orders, order_items, shipments):

    required_order_columns = {
        "order_id",
        "order_status",
    }

    required_item_columns = {
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "line_total",
    }

    required_shipment_columns = {
        "shipment_id",
        "order_id",
        "shipment_status",
        "shipment_date",
        "actual_delivery_date",
    }

    missing_orders = required_order_columns - set(orders.columns)
    missing_items = required_item_columns - set(order_items.columns)
    missing_shipments = required_shipment_columns - set(shipments.columns)

    if missing_orders:
        raise ValueError(
            f"orders.csv missing columns: {sorted(missing_orders)}"
        )

    if missing_items:
        raise ValueError(
            f"order_items.csv missing columns: {sorted(missing_items)}"
        )

    if missing_shipments:
        raise ValueError(
            f"shipments.csv missing columns: {sorted(missing_shipments)}"
        )

    if orders["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id found in orders.csv.")

    if order_items["order_item_id"].duplicated().any():
        raise ValueError("Duplicate order_item_id found in order_items.csv.")

    if shipments["shipment_id"].duplicated().any():
        raise ValueError("Duplicate shipment_id found in shipments.csv.")

    if shipments["order_id"].duplicated().any():
        raise ValueError(
            "shipments.csv contains multiple shipments for the same order. "
            "Current LOGIX model expects one shipment per order."
        )

    if order_items["order_id"].isin(orders["order_id"]).all() is False:
        raise ValueError(
            "order_items.csv contains order_id values missing from orders.csv."
        )

    if shipments["order_id"].isin(orders["order_id"]).all() is False:
        raise ValueError(
            "shipments.csv contains order_id values missing from orders.csv."
        )

    if (pd.to_numeric(order_items["quantity"], errors="coerce") <= 0).any():
        raise ValueError("order_items.csv contains non-positive quantities.")

    if (
        pd.to_numeric(order_items["unit_price"], errors="coerce")
        < 0
    ).any():
        raise ValueError("order_items.csv contains negative unit_price values.")

    if (
        pd.to_numeric(order_items["line_total"], errors="coerce")
        < 0
    ).any():
        raise ValueError("order_items.csv contains negative line_total values.")


# ============================================================
# BUILD ELIGIBLE RETURN ITEMS
# ============================================================

def build_eligible_items(orders, order_items, shipments):

    orders_status = (
        orders["order_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    shipment_status = (
        shipments["shipment_status"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # A return is generated only from an actually delivered shipment.
    eligible_shipments = shipments[
        shipment_status.eq("delivered")
        & shipments["actual_delivery_date"].notna()
    ].copy()

    # Returned orders are also allowed only when their shipment is
    # actually delivered. This keeps the delivery event authoritative.
    eligible_orders = orders[
        orders_status.eq("delivered") | orders_status.eq("returned")
    ].copy()

    eligible_order_ids = (
        set(eligible_orders["order_id"])
        & set(eligible_shipments["order_id"])
    )

    eligible_items = order_items[
        order_items["order_id"].isin(eligible_order_ids)
    ].copy()

    if eligible_items.empty:
        raise ValueError("No eligible delivered order items found.")

    # One shipment per order, so this merge gives each item its
    # corresponding actual delivery date.
    delivery_lookup = eligible_shipments[
        ["order_id", "actual_delivery_date"]
    ].copy()

    delivery_lookup["actual_delivery_date"] = pd.to_datetime(
        delivery_lookup["actual_delivery_date"],
        errors="coerce",
    )

    eligible_items = eligible_items.merge(
        delivery_lookup,
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    if eligible_items["actual_delivery_date"].isna().any():
        raise ValueError(
            "Eligible return items contain missing actual delivery dates."
        )

    return eligible_items


# ============================================================
# GENERATE RETURNS
# ============================================================

def generate_returns():

    print()
    print("=" * 70)
    print("LOGIX — RETURNS DATA GENERATION")
    print("=" * 70)

    orders, order_items, shipments = load_data()

    print()
    print(f"Orders loaded       : {len(orders):,}")
    print(f"Order items loaded  : {len(order_items):,}")
    print(f"Shipments loaded    : {len(shipments):,}")

    # --------------------------------------------------------
    # INPUT VALIDATION
    # --------------------------------------------------------

    validate_input_data(
        orders,
        order_items,
        shipments,
    )

    # --------------------------------------------------------
    # ELIGIBLE ITEMS
    # --------------------------------------------------------

    eligible_items = build_eligible_items(
        orders,
        order_items,
        shipments,
    )

    print()
    print(
        f"Eligible orders     : "
        f"{eligible_items['order_id'].nunique():,}"
    )

    print(
        f"Eligible order items: "
        f"{len(eligible_items):,}"
    )

    # --------------------------------------------------------
    # RETURN TARGET
    # --------------------------------------------------------

    target_returns = min(
        15_000,
        len(eligible_items),
    )

    # --------------------------------------------------------
    # SAMPLE UNIQUE ITEMS
    # --------------------------------------------------------

    # Each order item can receive at most one return record.
    selected_items = eligible_items.sample(
        n=target_returns,
        random_state=RANDOM_SEED,
    ).copy()

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    returns = []

    for return_number, row in enumerate(
        selected_items.itertuples(index=False),
        start=1,
    ):

        return_id = f"RET{return_number:06d}"

        # ----------------------------------------------------
        # DELIVERY DATE
        # ----------------------------------------------------

        delivery_date = pd.Timestamp(
            row.actual_delivery_date
        ).normalize()

        # Return must occur after delivery.
        return_delay = random.randint(1, 30)

        return_date = (
            delivery_date
            + pd.Timedelta(days=return_delay)
        )

        # ----------------------------------------------------
        # RETURN QUANTITY
        # ----------------------------------------------------

        purchased_quantity = int(row.quantity)

        return_quantity = choose_return_quantity(
            purchased_quantity
        )

        # ----------------------------------------------------
        # MONEY
        # ----------------------------------------------------

        # Integer-paise calculation avoids floating-point
        # inconsistencies in return amounts.
        unit_price_paise = int(
            round(float(row.unit_price) * 100)
        )

        return_amount_paise = (
            return_quantity
            * unit_price_paise
        )

        return_amount = (
            return_amount_paise / 100
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        return_status = choose_return_status()

        # ----------------------------------------------------
        # REFUND
        # ----------------------------------------------------

        if return_status == "Refunded":
            refund_amount_paise = return_amount_paise

        elif return_status in {
            "Received",
            "Picked Up",
            "Approved",
        }:
            refund_percentage = random.randint(
                90,
                100,
            )

            refund_amount_paise = (
                return_amount_paise
                * refund_percentage
                // 100
            )

        else:
            refund_amount_paise = 0

        refund_amount = (
            refund_amount_paise / 100
        )

        # ----------------------------------------------------
        # RECORD
        # ----------------------------------------------------

        returns.append(
            {
                "return_id": return_id,
                "order_id": row.order_id,
                "order_item_id": row.order_item_id,
                "product_id": row.product_id,
                "return_date": return_date.strftime(
                    "%Y-%m-%d"
                ),
                "return_quantity": return_quantity,
                "return_reason": choose_return_reason(),
                "return_status": return_status,
                "return_amount": round(
                    return_amount,
                    2,
                ),
                "refund_amount": round(
                    refund_amount,
                    2,
                ),
            }
        )

        if return_number % 2_000 == 0:
            print(
                f"  Generated "
                f"{return_number:,}/"
                f"{target_returns:,} returns..."
            )

    returns_df = pd.DataFrame(returns)

    if returns_df.empty:
        raise ValueError("No returns were generated.")

    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    returns_df = (
        returns_df
        .sort_values(
            by=[
                "return_date",
                "return_id",
            ]
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # FINAL INTEGRITY VALIDATION
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("RETURN INTEGRITY VALIDATION")
    print("-" * 70)

    # 1. Return count
    if len(returns_df) != target_returns:
        raise ValueError(
            "Return count does not match target."
        )
    print("✓ Return count matches target.")

    # 2. Return IDs
    if returns_df["return_id"].duplicated().any():
        raise ValueError("Duplicate return_id found.")
    print("✓ Return IDs are unique.")

    # 3. Order FK
    order_ids = set(orders["order_id"])

    if not returns_df["order_id"].isin(order_ids).all():
        raise ValueError(
            "Invalid order_id found in returns."
        )
    print("✓ Order foreign keys are valid.")

    # 4. Item FK
    item_lookup = order_items[
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "line_total",
        ]
    ].copy()

    if item_lookup["order_item_id"].duplicated().any():
        raise ValueError(
            "Duplicate order_item_id found in source data."
        )

    if not returns_df["order_item_id"].isin(
        item_lookup["order_item_id"]
    ).all():
        raise ValueError(
            "Invalid order_item_id found in returns."
        )
    print("✓ Order-item foreign keys are valid.")

    # 5. Product / item relationship
    item_map = item_lookup.set_index("order_item_id")

    expected_products = returns_df[
        "order_item_id"
    ].map(item_map["product_id"])

    if not (
        returns_df["product_id"].astype(str).values
        == expected_products.astype(str).values
    ).all():
        raise ValueError(
            "product_id does not match order_item_id."
        )
    print("✓ Product-to-order-item relationships are valid.")

    # 6. No duplicate returned item
    if returns_df["order_item_id"].duplicated().any():
        raise ValueError(
            "An order_item_id has been returned more than once."
        )
    print("✓ Each order item has at most one return.")

    # 7. Quantity
    source_qty = returns_df[
        "order_item_id"
    ].map(item_map["quantity"])

    if (
        returns_df["return_quantity"] <= 0
    ).any():
        raise ValueError(
            "Return quantity must be greater than zero."
        )

    if (
        returns_df["return_quantity"].values
        > source_qty.values
    ).any():
        raise ValueError(
            "Return quantity exceeds purchased quantity."
        )
    print("✓ Return quantities are valid.")

    # 8. Delivered shipment relationship
    delivered_shipments = shipments[
        shipments["shipment_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("delivered")
        & shipments["actual_delivery_date"].notna()
    ].copy()

    delivered_orders = set(
        delivered_shipments["order_id"]
    )

    if not returns_df["order_id"].isin(
        delivered_orders
    ).all():
        raise ValueError(
            "Return found for an order without a delivered shipment."
        )
    print("✓ All returned orders have delivered shipments.")

    # 9. Return date after delivery
    delivery_map = (
        delivered_shipments
        .set_index("order_id")["actual_delivery_date"]
    )

    delivery_dates = pd.to_datetime(
        returns_df["order_id"].map(delivery_map),
        errors="coerce",
    ).dt.normalize()

    return_dates = pd.to_datetime(
        returns_df["return_date"],
        errors="coerce",
    ).dt.normalize()

    if delivery_dates.isna().any():
        raise ValueError(
            "Missing delivery date for a returned order."
        )

    if (return_dates <= delivery_dates).any():
        raise ValueError(
            "Return date must be after actual delivery date."
        )
    print("✓ Return dates are after delivery dates.")

    # 10. Status vocabulary
    invalid_statuses = set(
        returns_df["return_status"]
    ) - set(RETURN_STATUSES)

    if invalid_statuses:
        raise ValueError(
            f"Invalid return statuses: {sorted(invalid_statuses)}"
        )
    print("✓ Return statuses are valid.")

    # 11. Reason vocabulary
    if RETURN_REASONS:
        invalid_reasons = set(
            returns_df["return_reason"]
        ) - set(RETURN_REASONS)

        if invalid_reasons:
            raise ValueError(
                f"Invalid return reasons: "
                f"{sorted(invalid_reasons)}"
            )

    print("✓ Return reasons are valid.")

    # 12. Money validation using integer paise
    source_unit_price = returns_df[
        "order_item_id"
    ].map(item_map["unit_price"])

    expected_return_amount_paise = (
        returns_df["return_quantity"].astype(int)
        * (
            pd.to_numeric(
                source_unit_price,
                errors="raise",
            ).round(2) * 100
        ).round()
    ).astype("int64")

    actual_return_amount_paise = (
        pd.to_numeric(
            returns_df["return_amount"],
            errors="raise",
        ).round(2) * 100
    ).round().astype("int64")

    if not (
        expected_return_amount_paise.values
        == actual_return_amount_paise.values
    ).all():
        raise ValueError(
            "Return amount does not match "
            "return_quantity × unit_price."
        )
    print("✓ Return amounts are mathematically valid.")

    # 13. Refund validation
    refund_paise = (
        pd.to_numeric(
            returns_df["refund_amount"],
            errors="raise",
        ).round(2) * 100
    ).round().astype("int64")

    return_paise = actual_return_amount_paise

    if (refund_paise < 0).any():
        raise ValueError(
            "Negative refund amount found."
        )

    if (refund_paise > return_paise).any():
        raise ValueError(
            "Refund amount cannot exceed return amount."
        )

    refunded_mask = returns_df[
        "return_status"
    ].eq("Refunded")

    if not (
        refund_paise[refunded_mask].values
        == return_paise[refunded_mask].values
    ).all():
        raise ValueError(
            "Refunded returns must have a full refund."
        )

    non_refunded_mask = ~refunded_mask

    if (
        refund_paise[non_refunded_mask].values
        > return_paise[non_refunded_mask].values
    ).any():
        raise ValueError(
            "Invalid refund amount detected."
        )

    print("✓ Refund amounts are valid.")

    # 14. Numeric sanity
    if (
        pd.to_numeric(
            returns_df["return_amount"],
            errors="coerce",
        ).isna().any()
    ):
        raise ValueError(
            "Invalid return_amount values found."
        )

    if (
        pd.to_numeric(
            returns_df["refund_amount"],
            errors="coerce",
        ).isna().any()
    ):
        raise ValueError(
            "Invalid refund_amount values found."
        )

    print("✓ Numeric values are valid.")

    print("✓ All return integrity checks passed.")

    # --------------------------------------------------------
    # SAVE ONLY AFTER ALL VALIDATIONS PASS
    # --------------------------------------------------------

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    returns_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("RETURNS GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Returns generated : "
        f"{len(returns_df):,}"
    )

    print(
        f"Unique orders     : "
        f"{returns_df['order_id'].nunique():,}"
    )

    print(
        f"Unique products   : "
        f"{returns_df['product_id'].nunique():,}"
    )

    print(
        f"Total return qty  : "
        f"{returns_df['return_quantity'].sum():,}"
    )

    print(
        f"Total return value: ₹"
        f"{returns_df['return_amount'].sum():,.2f}"
    )

    print(
        f"Total refunds     : ₹"
        f"{returns_df['refund_amount'].sum():,.2f}"
    )

    print()
    print("Return Status Distribution:")
    print(
        returns_df[
            "return_status"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print("Return Reason Distribution:")
    print(
        returns_df[
            "return_reason"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(f"✓ Saved: {OUTPUT_FILE}")

    print()
    print("=" * 70)
    print("RETURNS DATA GENERATION COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_returns()
