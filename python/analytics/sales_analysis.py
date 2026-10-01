import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Sales Analytics
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
    print("LOGIX - SALES PYTHON ANALYTICS")
    print("=" * 70)

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # ========================================================
    # 1. Monthly Sales
    # ========================================================

    monthly_query = """
        SELECT
            order_month,
            total_orders,
            unique_customers,
            revenue,
            average_order_value
        FROM vw_monthly_sales
        ORDER BY order_month
    """

    monthly_sales = pd.read_sql(
        monthly_query,
        connection
    )

    print("📈 MONTHLY SALES")
    print("-" * 70)

    print(
        monthly_sales.to_string(index=False)
    )

    # ========================================================
    # 2. Sales by Product Category
    # ========================================================

    category_query = """
        SELECT
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.line_total), 2) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
    """

    category_sales = pd.read_sql(
        category_query,
        connection
    )

    print("\n📦 SALES BY PRODUCT CATEGORY")
    print("-" * 70)

    print(
        category_sales.to_string(index=False)
    )

    # ========================================================
    # 3. Top 10 Products by Revenue
    # ========================================================

    product_query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.line_total), 2) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name,
            p.category
        ORDER BY revenue DESC
        LIMIT 10
    """

    top_products = pd.read_sql(
        product_query,
        connection
    )

    print("\n🏆 TOP 10 PRODUCTS BY REVENUE")
    print("-" * 70)

    print(
        top_products.to_string(index=False)
    )

    # ========================================================
    # 4. Sales by Delivery Type
    # ========================================================

    delivery_query = """
        SELECT
            o.delivery_type,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.line_total), 2) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY o.delivery_type
        ORDER BY revenue DESC
    """

    delivery_sales = pd.read_sql(
        delivery_query,
        connection
    )

    print("\n🚚 SALES BY DELIVERY TYPE")
    print("-" * 70)

    print(
        delivery_sales.to_string(index=False)
    )

    # ========================================================
    # 5. Python Calculations
    # ========================================================

    if not monthly_sales.empty:

        monthly_sales["revenue"] = pd.to_numeric(
            monthly_sales["revenue"]
        )

        monthly_sales["total_orders"] = pd.to_numeric(
            monthly_sales["total_orders"]
        )

        monthly_sales["revenue_per_order"] = (
            monthly_sales["revenue"]
            / monthly_sales["total_orders"]
        )

        monthly_sales["revenue_growth_pct"] = (
            monthly_sales["revenue"]
            .pct_change()
            .mul(100)
        )

        print("\n📊 PYTHON-CALCULATED SALES METRICS")
        print("-" * 70)

        print(
            monthly_sales[
                [
                    "order_month",
                    "total_orders",
                    "revenue",
                    "revenue_per_order",
                    "revenue_growth_pct"
                ]
            ].to_string(index=False)
        )

    # ========================================================
    # 6. Overall Sales Summary
    # ========================================================

    if not monthly_sales.empty:

        total_orders = monthly_sales[
            "total_orders"
        ].sum()

        total_revenue = monthly_sales[
            "revenue"
        ].sum()

        average_revenue_per_order = (
            total_revenue / total_orders
            if total_orders > 0
            else 0
        )

        print("\n" + "=" * 70)
        print("💰 OVERALL SALES SUMMARY")
        print("=" * 70)

        print(
            f"📦 Total Orders       : "
            f"{total_orders:,.0f}"
        )

        print(
            f"💰 Total Revenue      : "
            f"₹{total_revenue:,.2f}"
        )

        print(
            f"🧾 Revenue / Order    : "
            f"₹{average_revenue_per_order:,.2f}"
        )

    # ========================================================
    # Close connection
    # ========================================================

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)
    print("✅ SALES ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()