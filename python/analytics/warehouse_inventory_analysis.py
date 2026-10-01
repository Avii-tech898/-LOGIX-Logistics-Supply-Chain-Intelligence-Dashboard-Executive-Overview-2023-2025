import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Warehouse & Inventory Analytics
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


DB_CONFIG = {
    "host": os.getenv("LOGIX_DB_HOST", "localhost"),
    "port": int(os.getenv("LOGIX_DB_PORT", "3306")),
    "user": os.getenv("LOGIX_DB_USER", "root"),
    "password": os.getenv("LOGIX_DB_PASSWORD", ""),
    "database": os.getenv("LOGIX_DB_NAME", "logix"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def main():

    print("=" * 70)
    print("LOGIX - WAREHOUSE & INVENTORY PYTHON ANALYTICS")
    print("=" * 70)

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # ========================================================
    # 1. Warehouse Performance
    # ========================================================

    warehouse_query = """
        SELECT
            warehouse_id,
            warehouse_name,
            city,
            state,
            total_shipments,
            total_shipping_cost,
            average_distance_km,
            on_time_rate
        FROM vw_warehouse_performance
        ORDER BY total_shipments DESC
    """

    warehouse_analysis = pd.read_sql(
        warehouse_query,
        connection
    )

    print("🏭 WAREHOUSE PERFORMANCE")
    print("-" * 70)

    print(
        warehouse_analysis.to_string(index=False)
    )

    # ========================================================
    # 2. Inventory by Warehouse
    # ========================================================

    inventory_warehouse_query = """
        SELECT
            w.warehouse_id,
            w.warehouse_name,
            w.city,
            w.state,
            COUNT(i.inventory_id) AS inventory_records,
            SUM(i.opening_stock) AS opening_stock,
            SUM(i.current_stock) AS current_stock,
            SUM(i.inventory_value) AS inventory_value,
            SUM(
                CASE
                    WHEN i.stock_status = 'Out of Stock'
                    THEN 1 ELSE 0
                END
            ) AS out_of_stock_items,
            SUM(
                CASE
                    WHEN i.stock_status = 'Low Stock'
                    THEN 1 ELSE 0
                END
            ) AS low_stock_items
        FROM warehouses w
        LEFT JOIN inventory i
            ON w.warehouse_id = i.warehouse_id
        GROUP BY
            w.warehouse_id,
            w.warehouse_name,
            w.city,
            w.state
        ORDER BY inventory_value DESC
    """

    inventory_warehouse = pd.read_sql(
        inventory_warehouse_query,
        connection
    )

    print("\n📦 INVENTORY BY WAREHOUSE")
    print("-" * 70)

    print(
        inventory_warehouse.to_string(index=False)
    )

    # ========================================================
    # 3. Stock Status Analysis
    # ========================================================

    stock_status_query = """
        SELECT
            stock_status,
            COUNT(*) AS inventory_records,
            SUM(current_stock) AS current_stock,
            ROUND(SUM(inventory_value), 2) AS inventory_value
        FROM inventory
        GROUP BY stock_status
        ORDER BY inventory_records DESC
    """

    stock_status = pd.read_sql(
        stock_status_query,
        connection
    )

    print("\n📊 STOCK STATUS ANALYSIS")
    print("-" * 70)

    print(
        stock_status.to_string(index=False)
    )

    # ========================================================
    # 4. Product Category Inventory
    # ========================================================

    category_inventory_query = """
        SELECT
            p.category,
            COUNT(i.inventory_id) AS inventory_records,
            SUM(i.current_stock) AS current_stock,
            ROUND(SUM(i.inventory_value), 2) AS inventory_value
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        GROUP BY p.category
        ORDER BY inventory_value DESC
    """

    category_inventory = pd.read_sql(
        category_inventory_query,
        connection
    )

    print("\n🛍️ INVENTORY BY PRODUCT CATEGORY")
    print("-" * 70)

    print(
        category_inventory.to_string(index=False)
    )

    # ========================================================
    # 5. Low Stock Products
    # ========================================================

    low_stock_query = """
        SELECT
            i.inventory_id,
            i.warehouse_id,
            i.product_id,
            p.product_name,
            p.category,
            i.current_stock,
            i.reorder_level,
            i.stock_status,
            ROUND(i.inventory_value, 2) AS inventory_value
        FROM inventory i
        JOIN products p
            ON i.product_id = p.product_id
        WHERE i.stock_status IN ('Low Stock', 'Out of Stock')
        ORDER BY
            i.current_stock ASC,
            i.inventory_value DESC
        LIMIT 20
    """

    low_stock = pd.read_sql(
        low_stock_query,
        connection
    )

    print("\n⚠️ LOW / OUT-OF-STOCK PRODUCTS")
    print("-" * 70)

    print(
        low_stock.to_string(index=False)
    )

    # ========================================================
    # 6. Restocking Analysis
    # ========================================================

    restock_query = """
        SELECT
            DATE_FORMAT(last_restock_date, '%Y-%m') AS restock_month,
            COUNT(*) AS restock_records,
            SUM(current_stock) AS current_stock,
            ROUND(SUM(inventory_value), 2) AS inventory_value
        FROM inventory
        GROUP BY
            DATE_FORMAT(last_restock_date, '%Y-%m')
        ORDER BY restock_month
    """

    restock_analysis = pd.read_sql(
        restock_query,
        connection
    )

    print("\n🔄 MONTHLY RESTOCK ANALYSIS")
    print("-" * 70)

    print(
        restock_analysis.to_string(index=False)
    )

    # ========================================================
    # 7. Python Inventory Metrics
    # ========================================================

    total_inventory_records = len(
        pd.read_sql(
            "SELECT inventory_id FROM inventory",
            connection
        )
    )

    total_current_stock = inventory_warehouse[
        "current_stock"
    ].sum()

    total_inventory_value = inventory_warehouse[
        "inventory_value"
    ].sum()

    total_out_of_stock = inventory_warehouse[
        "out_of_stock_items"
    ].sum()

    total_low_stock = inventory_warehouse[
        "low_stock_items"
    ].sum()

    total_stock_risk = (
        total_out_of_stock +
        total_low_stock
    )

    stock_risk_rate = (
        total_stock_risk /
        total_inventory_records *
        100
        if total_inventory_records > 0
        else 0
    )

    average_inventory_value = (
        total_inventory_value /
        total_inventory_records
        if total_inventory_records > 0
        else 0
    )

    # ========================================================
    # 8. Overall Inventory Summary
    # ========================================================

    print("\n" + "=" * 70)
    print("📦 INVENTORY SUMMARY")
    print("=" * 70)

    print(
        f"📋 Inventory Records       : "
        f"{total_inventory_records:,.0f}"
    )

    print(
        f"📦 Current Stock           : "
        f"{total_current_stock:,.0f}"
    )

    print(
        f"💰 Inventory Value         : "
        f"₹{total_inventory_value:,.2f}"
    )

    print(
        f"⚠️ Low Stock Items         : "
        f"{total_low_stock:,.0f}"
    )

    print(
        f"🚫 Out of Stock Items      : "
        f"{total_out_of_stock:,.0f}"
    )

    print(
        f"⚠️ Total Stock Risk Items  : "
        f"{total_stock_risk:,.0f}"
    )

    print(
        f"📊 Stock Risk Rate         : "
        f"{stock_risk_rate:.2f}%"
    )

    print(
        f"💵 Avg Inventory Value     : "
        f"₹{average_inventory_value:,.2f}"
    )

    # ========================================================
    # 9. Python Warehouse Metrics
    # ========================================================

    if not inventory_warehouse.empty:

        inventory_warehouse["stock_per_record"] = (
            inventory_warehouse["current_stock"]
            / inventory_warehouse["inventory_records"]
        )

        inventory_warehouse["inventory_value_per_record"] = (
            inventory_warehouse["inventory_value"]
            / inventory_warehouse["inventory_records"]
        )

        print("\n🏭 PYTHON-CALCULATED WAREHOUSE METRICS")
        print("-" * 70)

        print(
            inventory_warehouse[
                [
                    "warehouse_id",
                    "warehouse_name",
                    "inventory_records",
                    "current_stock",
                    "inventory_value",
                    "stock_per_record",
                    "inventory_value_per_record"
                ]
            ].to_string(index=False)
        )

    # ========================================================
    # 10. Python Stock Risk Classification
    # ========================================================

    if not inventory_warehouse.empty:

        inventory_warehouse["risk_level"] = "Normal"

        inventory_warehouse.loc[
            inventory_warehouse["out_of_stock_items"] > 0,
            "risk_level"
        ] = "High"

        inventory_warehouse.loc[
            (
                inventory_warehouse["low_stock_items"] > 0
            ) &
            (
                inventory_warehouse["out_of_stock_items"] == 0
            ),
            "risk_level"
        ] = "Medium"

        risk_summary = (
            inventory_warehouse["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_summary.columns = [
            "risk_level",
            "warehouses"
        ]

        print("\n🚨 WAREHOUSE INVENTORY RISK")
        print("-" * 70)

        print(
            risk_summary.to_string(index=False)
        )

    # ========================================================
    # Close Connection
    # ========================================================

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)
    print("✅ WAREHOUSE & INVENTORY ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()