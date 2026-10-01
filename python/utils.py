import random
import string
from datetime import datetime, timedelta

import numpy as np
from faker import Faker


# ============================================================
# INITIALIZATION
# ============================================================

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)


# ============================================================
# ID GENERATOR
# ============================================================

def generate_id(prefix: str, number: int) -> str:
    """
    Generate a formatted business ID.

    Example:
        generate_id("CUS", 1)
        -> CUS000001
    """

    return f"{prefix}{number:06d}"


# ============================================================
# DATE FUNCTIONS
# ============================================================

def random_date(start_date: str, end_date: str) -> datetime:
    """
    Generate a random date between start_date and end_date.
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    delta = end - start

    random_days = random.randint(0, delta.days)

    return start + timedelta(days=random_days)


def random_datetime(start_date: str, end_date: str) -> datetime:
    """
    Generate a random datetime between two dates.
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    delta = end - start

    random_seconds = random.randint(
        0,
        int(delta.total_seconds())
    )

    return start + timedelta(seconds=random_seconds)


# ============================================================
# TEXT FUNCTIONS
# ============================================================

def random_name() -> str:
    """Generate an Indian-style name."""

    return fake.name()


def random_email(name: str) -> str:
    """
    Generate an email based on a name.
    """

    clean_name = (
        name.lower()
        .replace(" ", ".")
        .replace("'", "")
    )

    domains = [
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "example.com",
    ]

    return f"{clean_name}{random.randint(1, 999)}@{random.choice(domains)}"


# ============================================================
# PHONE NUMBER
# ============================================================

def random_phone() -> str:
    """
    Generate an Indian mobile number.
    """

    first_digit = random.choice(["6", "7", "8", "9"])

    remaining = "".join(
        random.choices(string.digits, k=9)
    )

    return first_digit + remaining


# ============================================================
# PINCODE
# ============================================================

def random_pincode() -> str:
    """
    Generate a valid 6-digit Indian-style pincode.
    """

    first_digit = random.choice("123456")
    remaining = "".join(
        random.choices(string.digits, k=5)
    )

    return first_digit + remaining


# ============================================================
# NUMERIC HELPERS
# ============================================================

def random_float(
    minimum: float,
    maximum: float,
    decimals: int = 2
) -> float:
    """
    Generate a random floating-point number.
    """

    value = random.uniform(minimum, maximum)

    return round(value, decimals)


def random_int(minimum: int, maximum: int) -> int:
    """Generate a random integer."""

    return random.randint(minimum, maximum)


# ============================================================
# WEIGHTED CHOICE
# ============================================================

def weighted_choice(values, weights):
    """
    Select a value based on probability weights.

    Example:
        weighted_choice(
            ["Active", "Inactive"],
            [0.9, 0.1]
        )
    """

    return random.choices(
        values,
        weights=weights,
        k=1
    )[0]


# ============================================================
# FILE NAME HELPER
# ============================================================

def safe_filename(name: str) -> str:
    """
    Convert a name into a safe filename.
    """

    return (
        name.lower()
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
    )
