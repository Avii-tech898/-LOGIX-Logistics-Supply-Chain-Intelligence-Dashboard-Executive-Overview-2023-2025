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
    PAYMENT_METHODS,
    PAYMENT_STATUSES,
    RANDOM_SEED,
)


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(RANDOM_SEED)


# ============================================================
# OUTPUT
# ============================================================

OUTPUT_FILE = RAW_DATA_DIR / "payments.csv"


# ============================================================
# PAYMENT METHOD
# ============================================================

def choose_payment_method():

    weights = []

    for method in PAYMENT_METHODS:

        value = str(method).lower()

        if "upi" in value:
            weights.append(35)

        elif "credit" in value:
            weights.append(20)

        elif "debit" in value:
            weights.append(15)

        elif "net" in value:
            weights.append(10)

        elif "cod" in value or "cash on delivery" in value:
            weights.append(15)

        elif "wallet" in value:
            weights.append(5)

        else:
            weights.append(1)

    return random.choices(
        PAYMENT_METHODS,
        weights=weights,
        k=1
    )[0]


# ============================================================
# PAYMENT STATUS
# ============================================================

def choose_payment_status(
    order_status,
    payment_method
):

    status_names = {
        str(status).lower(): status
        for status in PAYMENT_STATUSES
    }

    order_status_lower = str(
        order_status
    ).lower()

    payment_method_lower = str(
        payment_method
    ).lower()

    # --------------------------------------------------------
    # CANCELLED ORDERS
    # --------------------------------------------------------

    if order_status_lower == "cancelled":

        choices = []

        if "refunded" in status_names:
            choices.append(
                (
                    status_names["refunded"],
                    55
                )
            )

        if "failed" in status_names:
            choices.append(
                (
                    status_names["failed"],
                    25
                )
            )

        if "pending" in status_names:
            choices.append(
                (
                    status_names["pending"],
                    20
                )
            )

        if choices:

            values = [
                item[0]
                for item in choices
            ]

            weights = [
                item[1]
                for item in choices
            ]

            return random.choices(
                values,
                weights=weights,
                k=1
            )[0]

    # --------------------------------------------------------
    # RETURNED ORDERS
    # --------------------------------------------------------

    if order_status_lower == "returned":

        if "refunded" in status_names:
            return status_names["refunded"]

    # --------------------------------------------------------
    # NORMAL ORDERS
    # --------------------------------------------------------

    choices = []

    if "paid" in status_names:

        choices.append(
            (
                status_names["paid"],
                88
            )
        )

    if "pending" in status_names:

        choices.append(
            (
                status_names["pending"],
                5
            )
        )

    if "failed" in status_names:

        choices.append(
            (
                status_names["failed"],
                7
            )
        )

    if choices:

        values = [
            item[0]
            for item in choices
        ]

        weights = [
            item[1]
            for item in choices
        ]

        return random.choices(
            values,
            weights=weights,
            k=1
        )[0]

    return random.choice(
        PAYMENT_STATUSES
    )


# ============================================================
# TRANSACTION REFERENCE
# ============================================================

def generate_transaction_reference(
    payment_number
):

    return (
        f"TXN{payment_number:010d}"
    )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    orders_file = (
        RAW_DATA_DIR / "orders.csv"
    )

    items_file = (
        RAW_DATA_DIR / "order_items.csv"
    )

    if not orders_file.exists():

        raise FileNotFoundError(
            f"Missing file: {orders_file}"
        )

    if not items_file.exists():

        raise FileNotFoundError(
            f"Missing file: {items_file}"
        )

    orders = pd.read_csv(
        orders_file
    )

    order_items = pd.read_csv(
        items_file
    )

    required_order_columns = {
        "order_id",
        "order_date",
        "order_status"
    }

    required_item_columns = {
        "order_id",
        "line_total"
    }

    missing_order_columns = (
        required_order_columns
        - set(orders.columns)
    )

    missing_item_columns = (
        required_item_columns
        - set(order_items.columns)
    )

    if missing_order_columns:

        raise ValueError(
            "orders.csv missing columns: "
            f"{sorted(missing_order_columns)}"
        )

    if missing_item_columns:

        raise ValueError(
            "order_items.csv missing columns: "
            f"{sorted(missing_item_columns)}"
        )

    return orders, order_items


# ============================================================
# GENERATE PAYMENTS
# ============================================================

def generate_payments():

    print()
    print("=" * 70)
    print("LOGIX — PAYMENT DATA GENERATION")
    print("=" * 70)

    orders, order_items = load_data()

    print()
    print(
        f"Orders loaded      : "
        f"{len(orders):,}"
    )

    print(
        f"Order items loaded : "
        f"{len(order_items):,}"
    )

    # ========================================================
    # ORDER VALIDATION
    # ========================================================

    if orders["order_id"].isna().any():

        raise ValueError(
            "orders.csv contains missing order_id values."
        )

    if orders["order_id"].duplicated().any():

        raise ValueError(
            "orders.csv contains duplicate order_id values."
        )

    # ========================================================
    # ORDER ITEM VALIDATION
    # ========================================================

    order_items["line_total"] = pd.to_numeric(
        order_items["line_total"],
        errors="coerce"
    )

    if order_items["line_total"].isna().any():

        raise ValueError(
            "order_items.csv contains invalid line_total values."
        )

    if (
        order_items["line_total"] < 0
    ).any():

        raise ValueError(
            "Negative line_total detected."
        )

    # ========================================================
    # VALID ORDER RELATIONSHIP
    # ========================================================

    valid_order_ids = set(
        orders["order_id"]
    )

    invalid_item_orders = (
        set(order_items["order_id"])
        - valid_order_ids
    )

    if invalid_item_orders:

        raise ValueError(
            f"order_items.csv contains "
            f"{len(invalid_item_orders):,} "
            f"invalid order IDs."
        )

    # ========================================================
    # CALCULATE ORDER TOTALS
    # ========================================================
    #
    # Work in paise to avoid floating-point issues.
    #
    # ========================================================

    order_items["line_total_paise"] = (
        (
            order_items["line_total"]
            * 100
        )
        .round()
        .astype("int64")
    )

    order_totals = (
        order_items
        .groupby(
            "order_id",
            as_index=False
        )["line_total_paise"]
        .sum()
        .rename(
            columns={
                "line_total_paise":
                    "amount_paise"
            }
        )
    )

    # ========================================================
    # MERGE ORDERS + AMOUNT
    # ========================================================

    orders_payment = orders.merge(
        order_totals,
        on="order_id",
        how="left",
        validate="one_to_one"
    )

    # ========================================================
    # EVERY ORDER MUST HAVE ITEMS
    # ========================================================

    missing_amount_orders = (
        orders_payment[
            "amount_paise"
        ]
        .isna()
    )

    if missing_amount_orders.any():

        missing_orders = (
            orders_payment.loc[
                missing_amount_orders,
                "order_id"
            ]
            .tolist()
        )

        raise ValueError(
            f"{len(missing_orders):,} orders "
            "have no order-item total."
        )

    orders_payment[
        "amount_paise"
    ] = (
        orders_payment[
            "amount_paise"
        ]
        .astype("int64")
    )

    if (
        orders_payment["amount_paise"] < 0
    ).any():

        raise ValueError(
            "Negative payment amount detected."
        )

    # ========================================================
    # GENERATE PAYMENTS
    # ========================================================

    payments = []

    for payment_number, row in enumerate(
        orders_payment.itertuples(
            index=False
        ),
        start=1
    ):

        payment_id = (
            f"PAY{payment_number:06d}"
        )

        # ----------------------------------------------------
        # PAYMENT METHOD
        # ----------------------------------------------------

        payment_method = (
            choose_payment_method()
        )

        # ----------------------------------------------------
        # PAYMENT STATUS
        # ----------------------------------------------------

        payment_status = (
            choose_payment_status(
                row.order_status,
                payment_method
            )
        )

        # ----------------------------------------------------
        # PAYMENT DATE
        # ----------------------------------------------------

        order_date = pd.to_datetime(
            row.order_date
        )

        delay_hours = random.randint(
            0,
            48
        )

        payment_date = (
            order_date
            + pd.Timedelta(
                hours=delay_hours
            )
        )

        # ----------------------------------------------------
        # COD LOGIC
        # ----------------------------------------------------

        method_lower = str(
            payment_method
        ).lower()

        is_cod = (
            "cod" in method_lower
            or
            "cash on delivery"
            in method_lower
        )

        if is_cod:

            pending_status = next(
                (
                    status
                    for status in PAYMENT_STATUSES
                    if str(status).lower()
                    == "pending"
                ),
                None
            )

            if (
                pending_status is not None
                and str(
                    row.order_status
                ).lower()
                in {
                    "pending",
                    "confirmed",
                    "processing",
                    "shipped"
                }
            ):

                payment_status = (
                    pending_status
                )

        # ----------------------------------------------------
        # PAYMENT RECORD
        # ----------------------------------------------------

        amount = (
            row.amount_paise / 100
        )

        payments.append(
            {
                "payment_id":
                    payment_id,

                "order_id":
                    row.order_id,

                "payment_date":
                    payment_date.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "payment_method":
                    payment_method,

                "payment_status":
                    payment_status,

                "amount":
                    round(
                        amount,
                        2
                    ),

                "transaction_reference":
                    generate_transaction_reference(
                        payment_number
                    ),
            }
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        if payment_number % 10_000 == 0:

            print(
                f"  Generated "
                f"{payment_number:,}/"
                f"{len(orders_payment):,} "
                f"payments..."
            )

    # ========================================================
    # DATAFRAME
    # ========================================================

    payments_df = pd.DataFrame(
        payments
    )

    # ========================================================
    # PAYMENT ID VALIDATION
    # ========================================================

    if payments_df[
        "payment_id"
    ].isna().any():

        raise ValueError(
            "Missing payment_id detected."
        )

    if payments_df[
        "payment_id"
    ].duplicated().any():

        raise ValueError(
            "Duplicate payment_id detected."
        )

    # ========================================================
    # TRANSACTION REFERENCE VALIDATION
    # ========================================================

    if payments_df[
        "transaction_reference"
    ].isna().any():

        raise ValueError(
            "Missing transaction_reference detected."
        )

    if payments_df[
        "transaction_reference"
    ].duplicated().any():

        raise ValueError(
            "Duplicate transaction_reference detected."
        )

    # ========================================================
    # PAYMENT COUNT VALIDATION
    # ========================================================

    if len(payments_df) != len(orders):

        raise ValueError(
            f"Expected {len(orders):,} payments, "
            f"generated {len(payments_df):,}."
        )

    # ========================================================
    # ONE PAYMENT PER ORDER
    # ========================================================

    if (
        payments_df["order_id"]
        .nunique()
        != len(orders)
    ):

        raise ValueError(
            "Every order must have exactly "
            "one payment record."
        )

    # ========================================================
    # PAYMENT ORDER RELATIONSHIP
    # ========================================================

    payment_order_ids = set(
        payments_df["order_id"]
    )

    missing_payment_orders = (
        valid_order_ids
        - payment_order_ids
    )

    invalid_payment_orders = (
        payment_order_ids
        - valid_order_ids
    )

    if missing_payment_orders:

        raise ValueError(
            f"{len(missing_payment_orders):,} "
            "orders have no payment."
        )

    if invalid_payment_orders:

        raise ValueError(
            f"{len(invalid_payment_orders):,} "
            "payments reference invalid orders."
        )

    # ========================================================
    # PAYMENT AMOUNT VALIDATION
    # ========================================================

    payments_df["amount"] = pd.to_numeric(
        payments_df["amount"],
        errors="coerce"
    )

    if payments_df["amount"].isna().any():

        raise ValueError(
            "Invalid payment amount detected."
        )

    if (
        payments_df["amount"] < 0
    ).any():

        raise ValueError(
            "Negative payment amount detected."
        )

    # ========================================================
    # PAYMENT AMOUNT MUST MATCH ORDER TOTAL
    # ========================================================

    expected_amounts = (
        orders_payment[
            [
                "order_id",
                "amount_paise"
            ]
        ]
        .copy()
    )

    actual_amounts = (
        payments_df[
            [
                "order_id",
                "amount"
            ]
        ]
        .copy()
    )

    actual_amounts[
        "amount_paise"
    ] = (
        (
            actual_amounts["amount"]
            * 100
        )
        .round()
        .astype("int64")
    )

    amount_check = actual_amounts.merge(
        expected_amounts,
        on="order_id",
        how="left",
        validate="one_to_one"
    )

    amount_mismatch = (
        amount_check["amount_paise_x"]
        != amount_check["amount_paise_y"]
    )

    if amount_mismatch.any():

        raise ValueError(
            "Payment amount mismatch detected "
            f"in {amount_mismatch.sum():,} orders."
        )

    # ========================================================
    # PAYMENT DATE VALIDATION
    # ========================================================

    payments_df["payment_date"] = (
        pd.to_datetime(
            payments_df["payment_date"],
            errors="coerce"
        )
    )

    if payments_df[
        "payment_date"
    ].isna().any():

        raise ValueError(
            "Invalid payment_date detected."
        )

    order_dates = (
        orders[
            [
                "order_id",
                "order_date"
            ]
        ]
        .copy()
    )

    order_dates["order_date"] = (
        pd.to_datetime(
            order_dates["order_date"],
            errors="coerce"
        )
    )

    date_check = payments_df.merge(
        order_dates,
        on="order_id",
        how="left",
        validate="one_to_one"
    )

    invalid_payment_dates = (
        date_check["payment_date"]
        < date_check["order_date"]
    )

    if invalid_payment_dates.any():

        raise ValueError(
            "Payment date before order date "
            f"detected in "
            f"{invalid_payment_dates.sum():,} rows."
        )

    # ========================================================
    # PAYMENT METHOD VALIDATION
    # ========================================================

    valid_methods = set(
        str(method)
        for method in PAYMENT_METHODS
    )

    invalid_methods = (
        set(
            payments_df[
                "payment_method"
            ]
            .astype(str)
        )
        - valid_methods
    )

    if invalid_methods:

        raise ValueError(
            f"Invalid payment methods found: "
            f"{sorted(invalid_methods)}"
        )

    # ========================================================
    # PAYMENT STATUS VALIDATION
    # ========================================================

    valid_statuses = set(
        str(status)
        for status in PAYMENT_STATUSES
    )

    invalid_statuses = (
        set(
            payments_df[
                "payment_status"
            ]
            .astype(str)
        )
        - valid_statuses
    )

    if invalid_statuses:

        raise ValueError(
            f"Invalid payment statuses found: "
            f"{sorted(invalid_statuses)}"
        )

    # ========================================================
    # RESTORE PAYMENT DATE FORMAT
    # ========================================================

    payments_df["payment_date"] = (
        payments_df[
            "payment_date"
        ]
        .dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    # ========================================================
    # SORT
    # ========================================================

    payments_df = (
        payments_df
        .sort_values(
            by="payment_date"
        )
        .reset_index(
            drop=True
        )
    )

    # ========================================================
    # SAVE
    # ========================================================

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    payments_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("-" * 70)
    print("PAYMENT GENERATION SUMMARY")
    print("-" * 70)

    print(
        f"Payments generated : "
        f"{len(payments_df):,}"
    )

    print(
        f"Unique payments    : "
        f"{payments_df['payment_id'].nunique():,}"
    )

    print(
        f"Unique orders      : "
        f"{payments_df['order_id'].nunique():,}"
    )

    print(
        f"Total payment value: ₹"
        f"{payments_df['amount'].sum():,.2f}"
    )

    print()
    print(
        "Payment Method Distribution:"
    )

    print(
        payments_df[
            "payment_method"
        ]
        .value_counts()
        .to_string()
    )

    print()
    print(
        "Payment Status Distribution:"
    )

    print(
        payments_df[
            "payment_status"
        ]
        .value_counts()
        .to_string()
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
        "PAYMENT DATA GENERATION COMPLETED"
    )
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generate_payments()