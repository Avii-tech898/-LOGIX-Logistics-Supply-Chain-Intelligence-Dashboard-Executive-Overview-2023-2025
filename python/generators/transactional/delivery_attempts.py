"""
LOGIX — DELIVERY ATTEMPTS DATA GENERATION

Generates delivery_attempts.csv from the current shipments.csv.

Business rules:
- Created / Picked Up / In Transit -> 0 attempts
- Failed -> 1-2 attempts, NEVER Delivered
- Delivered / Delayed -> 1-3 attempts, exactly one final Delivered attempt
- Out for Delivery -> 1-3 attempts; may remain undelivered
- Attempt numbers are sequential per shipment
- Attempt dates never precede shipment_date
- Delivered attempt date matches actual_delivery_date
- File is saved only after all integrity checks pass
"""

import random
import sys
from pathlib import Path

import pandas as pd

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from python.config import RAW_DATA_DIR, RANDOM_SEED


random.seed(RANDOM_SEED)

OUTPUT_FILE = RAW_DATA_DIR / "delivery_attempts.csv"
SHIPMENTS_FILE = RAW_DATA_DIR / "shipments.csv"


ATTEMPT_OUTCOMES = [
    "Delivered",
    "Customer Unavailable",
    "Wrong Address",
    "Rescheduled",
    "Failed",
]

FAILURE_REASONS = [
    "Customer Unavailable",
    "Wrong Address",
    "Vehicle Breakdown",
    "Traffic Delay",
    "Customer Requested Reschedule",
    "Address Issue",
    "Operational Issue",
    "Other",
]

ZERO_ATTEMPT_STATUSES = {
    "Created",
    "Picked Up",
    "In Transit",
}

DELIVERED_STATUSES = {
    "Delivered",
    "Delayed",
}

FAILED_STATUS = "Failed"
OUT_FOR_DELIVERY_STATUS = "Out for Delivery"


def choose_attempt_count(minimum=1, maximum=3):
    return random.randint(minimum, maximum)


def choose_non_delivered_outcome():
    return random.choice(
        [
            "Customer Unavailable",
            "Wrong Address",
            "Rescheduled",
            "Failed",
        ]
    )


def choose_non_final_outcome():
    return random.choice(
        [
            "Customer Unavailable",
            "Wrong Address",
            "Rescheduled",
            "Failed",
        ]
    )


def choose_final_non_delivered_outcome():
    return random.choice(
        [
            "Customer Unavailable",
            "Wrong Address",
            "Rescheduled",
            "Failed",
        ]
    )


def choose_failure_reason():
    return random.choice(FAILURE_REASONS)


def load_shipments():
    if not SHIPMENTS_FILE.exists():
        raise FileNotFoundError(f"Missing file: {SHIPMENTS_FILE}")

    shipments = pd.read_csv(SHIPMENTS_FILE)

    required = {
        "shipment_id",
        "order_id",
        "shipment_date",
        "actual_delivery_date",
        "shipment_status",
    }

    missing = required - set(shipments.columns)

    if missing:
        raise ValueError(
            f"shipments.csv missing columns: {sorted(missing)}"
        )

    shipments["shipment_date"] = pd.to_datetime(
        shipments["shipment_date"],
        errors="coerce",
    )

    shipments["actual_delivery_date"] = pd.to_datetime(
        shipments["actual_delivery_date"],
        errors="coerce",
    )

    return shipments


def build_attempts(shipments):
    rows = []

    for index, shipment in enumerate(
        shipments.itertuples(index=False),
        start=1,
    ):
        shipment_id = str(shipment.shipment_id)
        order_id = str(shipment.order_id)
        status = str(shipment.shipment_status)

        shipment_date = shipment.shipment_date
        actual_delivery_date = shipment.actual_delivery_date

        if pd.isna(shipment_date):
            raise ValueError(
                f"Shipment {shipment_id} has invalid shipment_date."
            )

        # --------------------------------------------------------
        # ZERO ATTEMPTS
        # --------------------------------------------------------
        if status in ZERO_ATTEMPT_STATUSES:
            attempt_count = 0

        # --------------------------------------------------------
        # FAILED SHIPMENT
        # IMPORTANT: NEVER generate Delivered here.
        # --------------------------------------------------------
        elif status == FAILED_STATUS:
            attempt_count = choose_attempt_count(1, 2)

            for attempt_number in range(1, attempt_count + 1):
                if attempt_number < attempt_count:
                    outcome = choose_non_final_outcome()
                else:
                    outcome = choose_final_non_delivered_outcome()

                offset_days = random.randint(0, 3)
                attempt_date = shipment_date + pd.Timedelta(
                    days=offset_days
                )

                rows.append(
                    {
                        "attempt_id": None,
                        "shipment_id": shipment_id,
                        "order_id": order_id,
                        "attempt_number": attempt_number,
                        "attempt_date": attempt_date.strftime("%Y-%m-%d"),
                        "attempt_outcome": outcome,
                        "failure_reason": choose_failure_reason(),
                        "notes": "Delivery attempt recorded",
                    }
                )

        # --------------------------------------------------------
        # DELIVERED / DELAYED
        # Exactly one final Delivered attempt.
        # --------------------------------------------------------
        elif status in DELIVERED_STATUSES:
            if pd.isna(actual_delivery_date):
                raise ValueError(
                    f"{status} shipment {shipment_id} has no "
                    "actual_delivery_date."
                )

            attempt_count = choose_attempt_count(1, 3)

            for attempt_number in range(1, attempt_count + 1):
                is_final = attempt_number == attempt_count

                if is_final:
                    outcome = "Delivered"
                    attempt_date = actual_delivery_date
                    failure_reason = None
                    notes = "Delivery completed successfully"
                else:
                    outcome = choose_non_final_outcome()

                    earliest = shipment_date.normalize()
                    latest = actual_delivery_date.normalize()

                    if latest < earliest:
                        raise ValueError(
                            f"Shipment {shipment_id} has actual delivery "
                            "date before shipment date."
                        )

                    days_available = max(
                        0,
                        (latest - earliest).days,
                    )

                    offset_days = random.randint(
                        0,
                        min(3, days_available),
                    )

                    attempt_date = earliest + pd.Timedelta(
                        days=offset_days
                    )

                    if attempt_date.normalize() > latest.normalize():
                        attempt_date = latest

                    failure_reason = choose_failure_reason()
                    notes = "Previous delivery attempt"

                rows.append(
                    {
                        "attempt_id": None,
                        "shipment_id": shipment_id,
                        "order_id": order_id,
                        "attempt_number": attempt_number,
                        "attempt_date": attempt_date.strftime("%Y-%m-%d"),
                        "attempt_outcome": outcome,
                        "failure_reason": failure_reason,
                        "notes": notes,
                    }
                )

        # --------------------------------------------------------
        # OUT FOR DELIVERY
        # May be delivered or remain unsuccessful.
        # If actual_delivery_date exists, final attempt is Delivered.
        # Otherwise all attempts remain non-delivered.
        # --------------------------------------------------------
        elif status == OUT_FOR_DELIVERY_STATUS:
            attempt_count = choose_attempt_count(1, 3)

            if pd.notna(actual_delivery_date):
                final_outcome = "Delivered"
            else:
                final_outcome = choose_final_non_delivered_outcome()

            for attempt_number in range(1, attempt_count + 1):
                is_final = attempt_number == attempt_count

                if is_final and final_outcome == "Delivered":
                    outcome = "Delivered"
                    attempt_date = actual_delivery_date
                    failure_reason = None
                    notes = "Delivery completed successfully"
                else:
                    outcome = (
                        choose_non_final_outcome()
                        if not is_final
                        else final_outcome
                    )

                    attempt_date = shipment_date + pd.Timedelta(
                        days=random.randint(0, 2)
                    )

                    if (
                        pd.notna(actual_delivery_date)
                        and attempt_date.normalize()
                        > actual_delivery_date.normalize()
                    ):
                        attempt_date = actual_delivery_date

                    failure_reason = choose_failure_reason()
                    notes = "Delivery attempt recorded"

                rows.append(
                    {
                        "attempt_id": None,
                        "shipment_id": shipment_id,
                        "order_id": order_id,
                        "attempt_number": attempt_number,
                        "attempt_date": attempt_date.strftime("%Y-%m-%d"),
                        "attempt_outcome": outcome,
                        "failure_reason": failure_reason,
                        "notes": notes,
                    }
                )

        else:
            # Defensive handling for any future shipment status.
            # Generate a normal 1-attempt non-delivered record rather
            # than silently creating an invalid Delivered event.
            attempt_date = shipment_date

            rows.append(
                {
                    "attempt_id": None,
                    "shipment_id": shipment_id,
                    "order_id": order_id,
                    "attempt_number": 1,
                    "attempt_date": attempt_date.strftime("%Y-%m-%d"),
                    "attempt_outcome": choose_final_non_delivered_outcome(),
                    "failure_reason": choose_failure_reason(),
                    "notes": "Delivery attempt recorded",
                }
            )

        if index % 10_000 == 0:
            print(
                f"  Processed {index:,}/{len(shipments):,} shipments..."
            )

    # Assign IDs only after all rows have been created.
    for number, row in enumerate(rows, start=1):
        row["attempt_id"] = f"ATT{number:06d}"

    return pd.DataFrame(rows)


def validate_attempts(attempts, shipments):
    print()
    print("-" * 70)
    print("DELIVERY ATTEMPTS INTEGRITY VALIDATION")
    print("-" * 70)

    errors = []

    shipment_ids = set(shipments["shipment_id"].astype(str))
    attempt_shipment_ids = set(attempts["shipment_id"].astype(str))

    if attempts["attempt_id"].duplicated().any():
        errors.append("Duplicate attempt IDs found.")
    else:
        print("✓ Attempt IDs are unique.")

    orphan_shipments = attempt_shipment_ids - shipment_ids
    if orphan_shipments:
        errors.append(
            f"{len(orphan_shipments):,} orphan shipment IDs."
        )
    else:
        print("✓ Shipment foreign keys are valid.")

    shipment_order_map = (
        shipments.set_index("shipment_id")["order_id"]
        .astype(str)
        .to_dict()
    )

    mismatch = 0

    for row in attempts[["shipment_id", "order_id"]].itertuples(
        index=False
    ):
        expected_order = shipment_order_map.get(str(row.shipment_id))
        if expected_order != str(row.order_id):
            mismatch += 1

    if mismatch:
        errors.append(
            f"{mismatch:,} shipment → order relationship mismatches."
        )
    else:
        print("✓ Shipment → order relationships are valid.")

    # Attempt numbers: 1,2,3... per shipment.
    sequence_errors = 0

    grouped = (
        attempts.groupby("shipment_id")["attempt_number"]
        .apply(list)
    )

    for numbers in grouped:
        sorted_numbers = sorted(int(x) for x in numbers)
        expected = list(range(1, len(sorted_numbers) + 1))

        if sorted_numbers != expected:
            sequence_errors += 1

    if sequence_errors:
        errors.append(
            f"{sequence_errors:,} shipments have invalid attempt sequences."
        )
    else:
        print("✓ Attempt numbers are sequential.")

    # Attempt dates.
    shipment_dates = (
        shipments.set_index("shipment_id")["shipment_date"]
    )

    attempts_work = attempts.copy()
    attempts_work["attempt_date_dt"] = pd.to_datetime(
        attempts_work["attempt_date"],
        errors="coerce",
    )

    invalid_dates = 0

    for row in attempts_work[
        ["shipment_id", "attempt_date_dt"]
    ].itertuples(index=False):
        shipment_date = shipment_dates.get(row.shipment_id)

        if pd.isna(row.attempt_date_dt):
            invalid_dates += 1
        elif pd.isna(shipment_date):
            invalid_dates += 1
        elif row.attempt_date_dt.normalize() < shipment_date.normalize():
            invalid_dates += 1

    if invalid_dates:
        errors.append(
            f"{invalid_dates:,} attempts occur before shipment date."
        )
    else:
        print("✓ Attempt dates are valid.")

    # Vocabulary.
    invalid_outcomes = set(
        attempts["attempt_outcome"].dropna().astype(str)
    ) - set(ATTEMPT_OUTCOMES)

    if invalid_outcomes:
        errors.append(
            f"Invalid attempt outcomes: {sorted(invalid_outcomes)}"
        )
    else:
        print("✓ Attempt outcome vocabulary is valid.")

    # Delivered must have no failure reason.
    delivered_with_reason = (
        (attempts["attempt_outcome"] == "Delivered")
        & attempts["failure_reason"].notna()
        & attempts["failure_reason"].astype(str).ne("")
    ).sum()

    if delivered_with_reason:
        errors.append(
            f"{delivered_with_reason:,} Delivered attempts have failure reasons."
        )
    else:
        print("✓ Delivered attempts have no failure reason.")

    # Non-delivered must have a failure reason.
    non_delivered_missing_reason = (
        (attempts["attempt_outcome"] != "Delivered")
        & (
            attempts["failure_reason"].isna()
            | attempts["failure_reason"].astype(str).eq("")
        )
    ).sum()

    if non_delivered_missing_reason:
        errors.append(
            f"{non_delivered_missing_reason:,} non-delivered attempts "
            "have no failure reason."
        )
    else:
        print("✓ Non-delivered attempts have failure reasons.")

    # ------------------------------------------------------------
    # STATUS-LEVEL BUSINESS RULES
    # ------------------------------------------------------------

    shipment_status = (
        shipments.set_index("shipment_id")["shipment_status"]
        .astype(str)
        .to_dict()
    )

    attempts["shipment_status_for_validation"] = (
        attempts["shipment_id"].map(shipment_status)
    )

    # Failed shipments MUST NEVER have Delivered.
    failed_delivered = (
        (attempts["shipment_status_for_validation"] == FAILED_STATUS)
        & (attempts["attempt_outcome"] == "Delivered")
    ).sum()

    if failed_delivered:
        errors.append(
            f"{failed_delivered:,} Delivered attempts found for Failed shipments."
        )
    else:
        print("✓ Failed shipments never have Delivered attempts.")

    # Created / Picked Up / In Transit must have zero attempts.
    attempt_counts = attempts.groupby("shipment_id").size()

    zero_attempt_mismatches = 0

    for sid, status in shipment_status.items():
        if status in ZERO_ATTEMPT_STATUSES:
            if int(attempt_counts.get(sid, 0)) != 0:
                zero_attempt_mismatches += 1

    if zero_attempt_mismatches:
        errors.append(
            f"{zero_attempt_mismatches:,} zero-attempt shipment status mismatches."
        )
    else:
        print(
            "✓ Created/Picked Up/In Transit shipments have zero attempts."
        )

    # Delivered / Delayed must have exactly one Delivered attempt.
    delivered_attempt_counts = (
        attempts[
            attempts["attempt_outcome"] == "Delivered"
        ]
        .groupby("shipment_id")
        .size()
    )

    delivered_status_mismatches = 0

    for sid, status in shipment_status.items():
        if status in DELIVERED_STATUSES:
            if int(delivered_attempt_counts.get(sid, 0)) != 1:
                delivered_status_mismatches += 1

    if delivered_status_mismatches:
        errors.append(
            f"{delivered_status_mismatches:,} Delivered/Delayed shipments "
            "do not have exactly one Delivered attempt."
        )
    else:
        print(
            "✓ Delivered/Delayed shipments have exactly one Delivered attempt."
        )

    # Delivered attempt must match actual delivery date.
    delivery_dates = (
        shipments.set_index("shipment_id")["actual_delivery_date"]
    )

    delivered_date_mismatches = 0

    for row in attempts[
        attempts["attempt_outcome"] == "Delivered"
    ][["shipment_id", "attempt_date"]].itertuples(index=False):

        expected_date = delivery_dates.get(row.shipment_id)

        if pd.isna(expected_date):
            delivered_date_mismatches += 1
            continue

        actual_attempt_date = pd.to_datetime(
            row.attempt_date,
            errors="coerce",
        )

        if (
            pd.isna(actual_attempt_date)
            or actual_attempt_date.normalize()
            != expected_date.normalize()
        ):
            delivered_date_mismatches += 1

    if delivered_date_mismatches:
        errors.append(
            f"{delivered_date_mismatches:,} Delivered attempts "
            "do not match actual delivery date."
        )
    else:
        print("✓ Delivered attempt dates match actual delivery dates.")

    # Out for Delivery with an actual delivery date must have Delivered.
    ofd = shipments[
        (shipments["shipment_status"] == OUT_FOR_DELIVERY_STATUS)
        & shipments["actual_delivery_date"].notna()
    ]

    ofd_missing_delivered = 0

    for sid in ofd["shipment_id"].astype(str):
        count = int(delivered_attempt_counts.get(sid, 0))
        if count != 1:
            ofd_missing_delivered += 1

    if ofd_missing_delivered:
        errors.append(
            f"{ofd_missing_delivered:,} Out for Delivery shipments "
            "with actual delivery dates lack exactly one Delivered attempt."
        )
    else:
        print(
            "✓ Out for Delivery shipments with actual delivery dates "
            "have Delivered attempts."
        )

    if errors:
        print()
        print("FAILED VALIDATIONS:")
        for error in errors:
            print(f"✗ {error}")

        raise ValueError(
            f"Delivery attempt integrity validation failed with "
            f"{len(errors)} error(s)."
        )

    print("✓ All delivery attempt integrity checks passed.")


def print_summary(attempts):
    print()
    print("-" * 70)
    print("DELIVERY ATTEMPTS GENERATION SUMMARY")
    print("-" * 70)

    print(f"Attempts generated : {len(attempts):,}")
    print(
        f"Unique shipments   : "
        f"{attempts['shipment_id'].nunique():,}"
    )
    print(
        f"Unique orders      : "
        f"{attempts['order_id'].nunique():,}"
    )

    print()
    print("Attempt Outcome Distribution:")
    print(
        attempts["attempt_outcome"]
        .value_counts()
        .to_string()
    )

    print()
    print("Attempt Number Distribution:")
    print(
        attempts["attempt_number"]
        .value_counts()
        .sort_index()
        .to_string()
    )


def main():
    print()
    print("=" * 70)
    print("LOGIX — DELIVERY ATTEMPTS DATA GENERATION")
    print("=" * 70)

    shipments = load_shipments()

    print()
    print(f"Shipments loaded : {len(shipments):,}")

    attempts = build_attempts(shipments)

    validate_attempts(attempts, shipments)

    # Sort for clean deterministic output.
    attempts = (
        attempts.sort_values(
            by=["shipment_id", "attempt_number"]
        )
        .reset_index(drop=True)
    )

    # Re-number IDs after sorting.
    attempts["attempt_id"] = [
        f"ATT{number:06d}"
        for number in range(1, len(attempts) + 1)
    ]

    # Remove temporary validation column if present.
    if "shipment_status_for_validation" in attempts.columns:
        attempts = attempts.drop(
            columns=["shipment_status_for_validation"]
        )

    # Final column order.
    attempts = attempts[
        [
            "attempt_id",
            "shipment_id",
            "order_id",
            "attempt_number",
            "attempt_date",
            "attempt_outcome",
            "failure_reason",
            "notes",
        ]
    ]

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    attempts.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print_summary(attempts)

    print()
    print(f"✓ Saved: {OUTPUT_FILE}")
    print()
    print("=" * 70)
    print("DELIVERY ATTEMPTS DATA GENERATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()

