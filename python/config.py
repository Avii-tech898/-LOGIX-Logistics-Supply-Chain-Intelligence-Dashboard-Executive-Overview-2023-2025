"""
LOGIX - Project Configuration
"""

from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"

SQL_DIR = BASE_DIR / "sql"
EXCEL_DIR = BASE_DIR / "excel"
POWERBI_DIR = BASE_DIR / "powerbi"
DOCUMENTATION_DIR = BASE_DIR / "documentation"
ML_DIR = BASE_DIR / "ml"


# ============================================================
# RANDOM SEED
# ============================================================

RANDOM_SEED = 42


# ============================================================
# DATA PERIOD
# ============================================================

START_DATE = "2023-01-01"
END_DATE = "2025-12-31"


# ============================================================
# MASTER DATA SIZES
# ============================================================

NUM_CUSTOMERS = 20_000
NUM_ADDRESSES = 30_000
NUM_PRODUCTS = 5_000
NUM_WAREHOUSES = 30
NUM_DRIVERS = 1_000
NUM_VEHICLES = 1_200
NUM_DELIVERY_PARTNERS = 25


# ============================================================
# TRANSACTIONAL DATA SIZES
# ============================================================

NUM_ORDERS = 100_000

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

NUM_SHIPMENTS = 100_000
NUM_DELIVERY_ATTEMPTS = 150_000
NUM_RETURNS = 15_000


# ============================================================
# PRODUCT CATEGORIES
# ============================================================

PRODUCT_CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Grocery",
    "Sports",
    "Books",
    "Accessories"
]


# ============================================================
# INDIAN STATES
# ============================================================

INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal"
]


# ============================================================
# INDIAN CITIES
# ============================================================

INDIAN_CITIES = [
    "Lucknow",
    "Kanpur",
    "Varanasi",
    "Agra",
    "Prayagraj",
    "Gorakhpur",
    "Noida",
    "Ghaziabad",
    "Delhi",
    "Jaipur",
    "Jodhpur",
    "Kota",
    "Mumbai",
    "Pune",
    "Nagpur",
    "Nashik",
    "Ahmedabad",
    "Surat",
    "Vadodara",
    "Bengaluru",
    "Mysuru",
    "Mangaluru",
    "Chennai",
    "Coimbatore",
    "Hyderabad",
    "Kochi",
    "Kolkata",
    "Bhubaneswar",
    "Patna",
    "Ranchi",
    "Bhopal",
    "Indore",
    "Raipur",
    "Chandigarh",
    "Ludhiana",
    "Amritsar",
    "Dehradun",
    "Haridwar",
    "Guwahati"
]


# ============================================================
# ORDER STATUS
# ============================================================

ORDER_STATUSES = [
    "Pending",
    "Confirmed",
    "Processing",
    "Shipped",
    "Delivered",
    "Cancelled",
    "Returned"
]


# ============================================================
# SHIPMENT STATUS
# ============================================================

SHIPMENT_STATUSES = [
    "Created",
    "Picked Up",
    "In Transit",
    "Out for Delivery",
    "Delivered",
    "Delayed",
    "Failed"
]


# ============================================================
# PAYMENT METHODS
# ============================================================

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
    "Wallet"
]


# ============================================================
# PAYMENT STATUS
# ============================================================

PAYMENT_STATUSES = [
    "Pending",
    "Paid",
    "Failed",
    "Refunded",
    "Partially Refunded"
]


# ============================================================
# DELIVERY TYPES
# ============================================================

DELIVERY_TYPES = [
    "Standard",
    "Express",
    "Same Day"
]


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

CUSTOMER_SEGMENTS = [
    "Standard",
    "Premium",
    "VIP"
]


# ============================================================
# RETURN REASONS
# ============================================================

RETURN_REASONS = [
    "Damaged Product",
    "Wrong Product",
    "Product Defective",
    "Size Issue",
    "Quality Issue",
    "Changed Mind",
    "Late Delivery",
    "Other"
]


# ============================================================
# CREATE DIRECTORIES
# ============================================================

def create_directories():

    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        CLEANED_DATA_DIR,
        SQL_DIR,
        EXCEL_DIR,
        POWERBI_DIR,
        DOCUMENTATION_DIR,
        ML_DIR
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )


if __name__ == "__main__":
    create_directories()

    print("=" * 60)
    print("LOGIX DIRECTORY CONFIGURATION")
    print("=" * 60)

    print(f"Base Directory : {BASE_DIR}")
    print(f"Raw Data       : {RAW_DATA_DIR}")
    print(f"Cleaned Data   : {CLEANED_DATA_DIR}")

    print("\nDirectories created successfully.")

