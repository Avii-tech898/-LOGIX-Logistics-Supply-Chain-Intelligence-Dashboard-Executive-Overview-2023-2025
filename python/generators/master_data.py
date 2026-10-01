"""
LOGIX - Master Data Generator
Phase 04.1

Generates:
    1. customers.csv
    2. addresses.csv
    3. products.csv
    4. warehouses.csv
    5. drivers.csv
    6. vehicles.csv
    7. delivery_partners.csv
"""

from pathlib import Path
import sys
import random

import pandas as pd


# ============================================================
# PATH SETUP
# ============================================================

CURRENT_FILE = Path(__file__).resolve()

PYTHON_DIR = CURRENT_FILE.parents[1]
PROJECT_ROOT = CURRENT_FILE.parents[2]

if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from config import (
    RAW_DATA_DIR,
    NUM_CUSTOMERS,
    NUM_ADDRESSES,
    NUM_PRODUCTS,
    NUM_WAREHOUSES,
    NUM_DRIVERS,
    NUM_VEHICLES,
    NUM_DELIVERY_PARTNERS,
    PRODUCT_CATEGORIES,
    INDIAN_STATES,
    INDIAN_CITIES,
)

from utils import (
    random_name,
    random_email,
    random_phone,
    random_pincode,
    random_float,
    random_int,
    weighted_choice,
)


# ============================================================
# SAVE HELPER
# ============================================================

def save_dataframe(df: pd.DataFrame, filename: str) -> None:
    """
    Save dataframe into data/raw.
    """

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = RAW_DATA_DIR / filename

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"✓ Saved {filename:<25} | "
        f"Rows: {len(df):,}"
    )


# ============================================================
# CUSTOMERS
# ============================================================

def generate_customers() -> pd.DataFrame:

    rows = []

    segments = [
        "Standard",
        "Premium",
        "VIP"
    ]

    payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Cash on Delivery",
        "Wallet"
    ]

    payment_weights = [
        0.30,
        0.20,
        0.18,
        0.10,
        0.15,
        0.07
    ]

    for i in range(1, NUM_CUSTOMERS + 1):

        customer_name = random_name()

        customer_email = random_email(
            customer_name
        )

        rows.append({
            "customer_id":
                f"CUST{i:06d}",

            "customer_name":
                customer_name,

            "email":
                customer_email,

            "phone":
                random_phone(),

            "gender":
                weighted_choice(
                    ["Male", "Female", "Other"],
                    [0.48, 0.48, 0.04]
                ),

            "customer_segment":
                weighted_choice(
                    segments,
                    [0.70, 0.25, 0.05]
                ),

            "registration_date":
                (
                    f"2023-"
                    f"{random_int(1, 12):02d}-"
                    f"{random_int(1, 28):02d}"
                ),

            "state":
                weighted_choice(
                    INDIAN_STATES,
                    [1 / len(INDIAN_STATES)]
                    * len(INDIAN_STATES)
                ),

            "city":
                weighted_choice(
                    INDIAN_CITIES,
                    [1 / len(INDIAN_CITIES)]
                    * len(INDIAN_CITIES)
                ),

            "pincode":
                random_pincode(),

            "preferred_payment_method":
                weighted_choice(
                    payment_methods,
                    payment_weights
                ),

            "is_active":
                weighted_choice(
                    [True, False],
                    [0.95, 0.05]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# ADDRESSES
# ============================================================

def generate_addresses() -> pd.DataFrame:

    rows = []

    address_types = [
        "Home",
        "Office",
        "Other"
    ]

    street_names = [
        "MG Road",
        "Station Road",
        "Main Market",
        "Civil Lines",
        "Gandhi Nagar",
        "Ring Road",
        "Model Town",
        "Industrial Area"
    ]

    # --------------------------------------------------------
    # STEP 1: GUARANTEE AT LEAST ONE ADDRESS PER CUSTOMER
    # --------------------------------------------------------

    address_number = 1

    for customer_number in range(1, NUM_CUSTOMERS + 1):

        rows.append({
            "address_id":
                f"ADDR{address_number:06d}",

            "customer_id":
                f"CUST{customer_number:06d}",

            "address_type":
                weighted_choice(
                    address_types,
                    [0.65, 0.25, 0.10]
                ),

            "address_line":
                (
                    f"{random_int(1, 999)}, "
                    f"{random.choice(street_names)}"
                ),

            "city":
                weighted_choice(
                    INDIAN_CITIES,
                    [1 / len(INDIAN_CITIES)]
                    * len(INDIAN_CITIES)
                ),

            "state":
                weighted_choice(
                    INDIAN_STATES,
                    [1 / len(INDIAN_STATES)]
                    * len(INDIAN_STATES)
                ),

            "pincode":
                random_pincode(),

            "is_default":
                True
        })

        address_number += 1

    # --------------------------------------------------------
    # STEP 2: GENERATE REMAINING ADDRESSES
    # --------------------------------------------------------

    remaining_addresses = (
        NUM_ADDRESSES - NUM_CUSTOMERS
    )

    customer_ids = [
        f"CUST{i:06d}"
        for i in range(1, NUM_CUSTOMERS + 1)
    ]

    for _ in range(remaining_addresses):

        customer_id = random.choice(customer_ids)

        rows.append({
            "address_id":
                f"ADDR{address_number:06d}",

            "customer_id":
                customer_id,

            "address_type":
                weighted_choice(
                    address_types,
                    [0.65, 0.25, 0.10]
                ),

            "address_line":
                (
                    f"{random_int(1, 999)}, "
                    f"{random.choice(street_names)}"
                ),

            "city":
                weighted_choice(
                    INDIAN_CITIES,
                    [1 / len(INDIAN_CITIES)]
                    * len(INDIAN_CITIES)
                ),

            "state":
                weighted_choice(
                    INDIAN_STATES,
                    [1 / len(INDIAN_STATES)]
                    * len(INDIAN_STATES)
                ),

            "pincode":
                random_pincode(),

            "is_default":
                False
        })

        address_number += 1

    # --------------------------------------------------------
    # STEP 3: CREATE DATAFRAME
    # --------------------------------------------------------

    addresses_df = pd.DataFrame(rows)

    return addresses_df

# ============================================================
# PRODUCTS
# ============================================================

def generate_products() -> pd.DataFrame:

    rows = []

    product_names = {
        "Electronics": [
            "Smartphone",
            "Laptop",
            "Tablet",
            "Wireless Earbuds",
            "Smart Watch",
            "Bluetooth Speaker"
        ],

        "Fashion": [
            "T-Shirt",
            "Jeans",
            "Jacket",
            "Sneakers",
            "Formal Shirt",
            "Kurta"
        ],

        "Home & Kitchen": [
            "Mixer Grinder",
            "Cookware Set",
            "Bedsheet",
            "Air Fryer",
            "Water Bottle",
            "Storage Box"
        ],

        "Beauty": [
            "Face Wash",
            "Moisturizer",
            "Shampoo",
            "Perfume",
            "Sunscreen"
        ],

        "Grocery": [
            "Rice",
            "Wheat Flour",
            "Cooking Oil",
            "Tea",
            "Coffee",
            "Dry Fruits"
        ],

        "Sports": [
            "Cricket Bat",
            "Football",
            "Yoga Mat",
            "Running Shoes",
            "Dumbbells"
        ],

        "Books": [
            "Data Science Book",
            "Programming Book",
            "Business Book",
            "Fiction Novel",
            "Exam Preparation Book"
        ],

        "Accessories": [
            "Backpack",
            "Wallet",
            "Belt",
            "Sunglasses",
            "Phone Case"
        ]
    }

    category_weights = [
        0.18,
        0.15,
        0.14,
        0.10,
        0.15,
        0.10,
        0.08,
        0.10
    ]

    brands = [
        "Nova",
        "Prime",
        "Urban",
        "Elite",
        "Max",
        "Pro",
        "Value"
    ]

    for i in range(1, NUM_PRODUCTS + 1):

        category = weighted_choice(
            PRODUCT_CATEGORIES,
            category_weights
        )

        names = product_names[category]

        product_name = weighted_choice(
            names,
            [1 / len(names)] * len(names)
        )

        rows.append({
            "product_id":
                f"PROD{i:06d}",

            "product_name":
                product_name,

            "category":
                category,

            "brand":
                weighted_choice(
                    brands,
                    [0.15, 0.15, 0.15,
                     0.15, 0.15, 0.15, 0.10]
                ),

            "unit_price":
                random_float(
                    50,
                    100000,
                    2
                ),

            "weight_kg":
                random_float(
                    0.1,
                    30,
                    2
                ),

            "supplier":
                f"SUP{random_int(1, 500):04d}",

            "reorder_level":
                random_int(5, 100),

            "is_active":
                weighted_choice(
                    [True, False],
                    [0.97, 0.03]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# WAREHOUSES
# ============================================================

def generate_warehouses() -> pd.DataFrame:

    rows = []

    warehouse_types = [
        "Regional",
        "Central",
        "Fulfillment",
        "Distribution"
    ]

    for i in range(1, NUM_WAREHOUSES + 1):

        rows.append({
            "warehouse_id":
                f"WH{i:03d}",

            "warehouse_name":
                f"LOGIX Warehouse {i:02d}",

            "warehouse_type":
                weighted_choice(
                    warehouse_types,
                    [0.30, 0.20, 0.30, 0.20]
                ),

            "city":
                weighted_choice(
                    INDIAN_CITIES,
                    [1 / len(INDIAN_CITIES)]
                    * len(INDIAN_CITIES)
                ),

            "state":
                weighted_choice(
                    INDIAN_STATES,
                    [1 / len(INDIAN_STATES)]
                    * len(INDIAN_STATES)
                ),

            "pincode":
                random_pincode(),

            "capacity_units":
                random_int(
                    10000,
                    100000
                ),

            "manager_name":
                random_name(),

            "operating_hours":
                weighted_choice(
                    [
                        "8-16",
                        "9-17",
                        "10-18",
                        "24x7"
                    ],
                    [0.20, 0.30, 0.20, 0.30]
                ),

            "is_active":
                weighted_choice(
                    [True, False],
                    [0.95, 0.05]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# DRIVERS
# ============================================================

def generate_drivers() -> pd.DataFrame:

    rows = []

    statuses = [
        "Active",
        "Inactive",
        "On Leave"
    ]

    employment_types = [
        "Full Time",
        "Contract",
        "Partner"
    ]

    for i in range(1, NUM_DRIVERS + 1):

        rows.append({
            "driver_id":
                f"DRV{i:05d}",

            "driver_name":
                random_name(),

            "phone":
                random_phone(),

            "license_number":
                f"DL{random_int(10000000, 99999999)}",

            "experience_years":
                random_int(1, 20),

            "rating":
                random_float(
                    2.5,
                    5.0,
                    2
                ),

            "city":
                weighted_choice(
                    INDIAN_CITIES,
                    [1 / len(INDIAN_CITIES)]
                    * len(INDIAN_CITIES)
                ),

            "employment_type":
                weighted_choice(
                    employment_types,
                    [0.50, 0.30, 0.20]
                ),

            "status":
                weighted_choice(
                    statuses,
                    [0.90, 0.05, 0.05]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# VEHICLES
# ============================================================

def generate_vehicles() -> pd.DataFrame:

    rows = []

    vehicle_types = [
        "Bike",
        "Van",
        "Mini Truck",
        "Truck",
        "Heavy Truck"
    ]

    vehicle_type_weights = [
        0.20,
        0.25,
        0.25,
        0.20,
        0.10
    ]

    fuel_types = [
        "Diesel",
        "Petrol",
        "CNG",
        "Electric"
    ]

    for i in range(1, NUM_VEHICLES + 1):

        vehicle_type = weighted_choice(
            vehicle_types,
            vehicle_type_weights
        )

        capacity_ranges = {
            "Bike": (5, 30),
            "Van": (100, 500),
            "Mini Truck": (500, 1500),
            "Truck": (1500, 5000),
            "Heavy Truck": (5000, 15000)
        }

        minimum, maximum = capacity_ranges[
            vehicle_type
        ]

        vehicle_number = (
            f"UP{random_int(10, 99)}"
            f"{random.choice(['A', 'B', 'C', 'D', 'E'])}"
            f"{random_int(1000, 9999)}"
        )

        rows.append({
            "vehicle_id":
                f"VEH{i:05d}",

            "vehicle_number":
                vehicle_number,

            "vehicle_type":
                vehicle_type,

            "capacity_kg":
                random_float(
                    minimum,
                    maximum,
                    2
                ),

            "fuel_type":
                weighted_choice(
                    fuel_types,
                    [0.40, 0.25, 0.20, 0.15]
                ),

            "model_year":
                random_int(2018, 2026),

            "driver_id":
                f"DRV{random_int(1, NUM_DRIVERS):05d}",

            "status":
                weighted_choice(
                    [
                        "Active",
                        "Maintenance",
                        "Inactive"
                    ],
                    [0.85, 0.10, 0.05]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# DELIVERY PARTNERS
# ============================================================

def generate_delivery_partners() -> pd.DataFrame:

    partner_names = [
        "Delhivery",
        "Blue Dart",
        "DTDC",
        "Ecom Express",
        "XpressBees",
        "Shadowfax",
        "Ekart",
        "Shiprocket",
        "India Post",
        "DHL India",
        "FedEx India",
        "Amazon Logistics",
        "Flipkart Logistics",
        "Professional Couriers",
        "Gati",
        "Safexpress",
        "Rivigo",
        "Loadshare",
        "Porter",
        "Borzo",
        "Trackon",
        "First Flight",
        "Aramex India",
        "Ekart Logistics",
        "TCI Express"
    ]

    rows = []

    for i in range(
        1,
        NUM_DELIVERY_PARTNERS + 1
    ):

        rows.append({
            "partner_id":
                f"PART{i:03d}",

            "partner_name":
                partner_names[i - 1],

            "service_type":
                weighted_choice(
                    [
                        "Standard",
                        "Express",
                        "Same Day",
                        "Hyperlocal"
                    ],
                    [0.45, 0.30, 0.15, 0.10]
                ),

            "coverage_type":
                weighted_choice(
                    [
                        "Local",
                        "Regional",
                        "National"
                    ],
                    [0.20, 0.30, 0.50]
                ),

            "base_cost_per_km":
                random_float(
                    5,
                    30,
                    2
                ),

            "rating":
                random_float(
                    3.0,
                    5.0,
                    2
                ),

            "contact_phone":
                random_phone(),

            "status":
                weighted_choice(
                    ["Active", "Inactive"],
                    [0.95, 0.05]
                )
        })

    return pd.DataFrame(rows)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("LOGIX - MASTER DATA GENERATION")
    print("=" * 70)

    print()
    print(f"Project Root : {PROJECT_ROOT}")
    print(f"Output Path  : {RAW_DATA_DIR}")

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("Generating master datasets...")
    print()

    # --------------------------------------------------------
    # 1. CUSTOMERS
    # --------------------------------------------------------

    customers = generate_customers()

    save_dataframe(
        customers,
        "customers.csv"
    )

    # --------------------------------------------------------
    # 2. ADDRESSES
    # --------------------------------------------------------

    addresses = generate_addresses()

    save_dataframe(
        addresses,
        "addresses.csv"
    )

    # --------------------------------------------------------
    # 3. PRODUCTS
    # --------------------------------------------------------

    products = generate_products()

    save_dataframe(
        products,
        "products.csv"
    )

    # --------------------------------------------------------
    # 4. WAREHOUSES
    # --------------------------------------------------------

    warehouses = generate_warehouses()

    save_dataframe(
        warehouses,
        "warehouses.csv"
    )

    # --------------------------------------------------------
    # 5. DRIVERS
    # --------------------------------------------------------

    drivers = generate_drivers()

    save_dataframe(
        drivers,
        "drivers.csv"
    )

    # --------------------------------------------------------
    # 6. VEHICLES
    # --------------------------------------------------------

    vehicles = generate_vehicles()

    save_dataframe(
        vehicles,
        "vehicles.csv"
    )

    # --------------------------------------------------------
    # 7. DELIVERY PARTNERS
    # --------------------------------------------------------

    delivery_partners = (
        generate_delivery_partners()
    )

    save_dataframe(
        delivery_partners,
        "delivery_partners.csv"
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("MASTER DATA GENERATION COMPLETED")
    print("=" * 70)

    print()
    print("Generated files:")

    generated_files = sorted(
        RAW_DATA_DIR.glob("*.csv")
    )

    for file in generated_files:
        print(
            f"  ✓ {file.name}"
        )

    print()
    print(
        f"Total CSV files generated: "
        f"{len(generated_files)}"
    )

    print()
    print(
        "Next step: Run master-data validation."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()

