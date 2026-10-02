from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"

ORDERS_FILE = DATA_DIR / "orders.csv"
SHIPMENTS_FILE = DATA_DIR / "shipments.csv"
WAREHOUSES_FILE = DATA_DIR / "warehouses.csv"
DELIVERY_PARTNERS_FILE = DATA_DIR / "delivery_partners.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.20

TARGET_COLUMN = "is_delayed"

NUMERIC_FEATURES = [
    "distance_km",
    "shipping_cost",
    "sla_days",
    "processing_days",
    "order_month",
    "order_day_of_week",
    "shipment_day_of_week",
]

CATEGORICAL_FEATURES = [
    "delivery_type",
    "priority",
    "warehouse_id",
    "delivery_partner_id",
]

MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
