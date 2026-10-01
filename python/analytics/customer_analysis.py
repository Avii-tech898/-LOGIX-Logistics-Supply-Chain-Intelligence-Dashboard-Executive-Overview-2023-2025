import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Customer Analytics
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
    print("LOGIX - CUSTOMER PYTHON ANALYTICS")
    print("=" * 70)

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # ========================================================
    # 1. Customer Segment Analysis
    # ========================================================

    segment_query = """
        SELECT
            c.customer_segment,
            COUNT(DISTINCT c.customer_id) AS customers,
            COUNT(DISTINCT o.order_id) AS orders,
            ROUND(SUM(oi.line_total), 2) AS revenue,
            ROUND(
                SUM(oi.line_total) /
                NULLIF(COUNT(DISTINCT o.order_id), 0),
                2
            ) AS revenue_per_order
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY c.customer_segment
        ORDER BY revenue DESC
    """

    segment_analysis = pd.read_sql(
        segment_query,
        connection
    )

    print("👥 CUSTOMER SEGMENT ANALYSIS")
    print("-" * 70)

    print(
        segment_analysis.to_string(index=False)
    )

    # ========================================================
    # 2. Customer Order Frequency
    # ========================================================

    frequency_query = """
        SELECT
            c.customer_id,
            c.customer_name,
            c.customer_segment,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(
                COALESCE(SUM(oi.line_total), 0),
                2
            ) AS total_revenue
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            c.customer_segment
        ORDER BY total_orders DESC
    """

    customer_frequency = pd.read_sql(
        frequency_query,
        connection
    )

    print("\n📊 CUSTOMER ORDER FREQUENCY")
    print("-" * 70)

    print(
        customer_frequency.head(20).to_string(index=False)
    )

    # ========================================================
    # 3. Top 10 Customers by Revenue
    # ========================================================

    top_customer_query = """
        SELECT
            c.customer_id,
            c.customer_name,
            c.customer_segment,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(oi.line_total), 2) AS total_revenue
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY
            c.customer_id,
            c.customer_name,
            c.customer_segment
        ORDER BY total_revenue DESC
        LIMIT 10
    """

    top_customers = pd.read_sql(
        top_customer_query,
        connection
    )

    print("\n🏆 TOP 10 CUSTOMERS BY REVENUE")
    print("-" * 70)

    print(
        top_customers.to_string(index=False)
    )

    # ========================================================
    # 4. Repeat Customer Analysis
    # ========================================================

    repeat_query = """
        SELECT
            customer_id,
            COUNT(DISTINCT order_id) AS total_orders
        FROM orders
        GROUP BY customer_id
    """

    customer_orders = pd.read_sql(
        repeat_query,
        connection
    )

    customer_orders["customer_type"] = customer_orders[
        "total_orders"
    ].apply(
        lambda x: "Repeat Customer"
        if x > 1
        else "One-Time Customer"
    )

    repeat_summary = (
        customer_orders["customer_type"]
        .value_counts()
        .reset_index()
    )

    repeat_summary.columns = [
        "customer_type",
        "customers"
    ]

    print("\n🔁 CUSTOMER REPEAT ANALYSIS")
    print("-" * 70)

    print(
        repeat_summary.to_string(index=False)
    )

    # ========================================================
    # 5. Python Customer Metrics
    # ========================================================

    total_customers = len(customer_frequency)

    active_customers = (
        customer_frequency["total_orders"] > 0
    ).sum()

    repeat_customers = (
        customer_frequency["total_orders"] > 1
    ).sum()

    one_time_customers = (
        customer_frequency["total_orders"] == 1
    ).sum()

    total_revenue = customer_frequency[
        "total_revenue"
    ].sum()

    total_orders = customer_frequency[
        "total_orders"
    ].sum()

    average_revenue_per_customer = (
        total_revenue / active_customers
        if active_customers > 0
        else 0
    )

    average_orders_per_customer = (
        total_orders / active_customers
        if active_customers > 0
        else 0
    )

    repeat_customer_rate = (
        repeat_customers / active_customers * 100
        if active_customers > 0
        else 0
    )

    # ========================================================
    # 6. Customer Summary
    # ========================================================

    print("\n" + "=" * 70)
    print("👥 CUSTOMER SUMMARY")
    print("=" * 70)

    print(
        f"👤 Total Customers          : "
        f"{total_customers:,.0f}"
    )

    print(
        f"🛒 Active Customers         : "
        f"{active_customers:,.0f}"
    )

    print(
        f"🔁 Repeat Customers         : "
        f"{repeat_customers:,.0f}"
    )

    print(
        f"1️⃣ One-Time Customers      : "
        f"{one_time_customers:,.0f}"
    )

    print(
        f"💰 Total Customer Revenue   : "
        f"₹{total_revenue:,.2f}"
    )

    print(
        f"📦 Total Customer Orders    : "
        f"{total_orders:,.0f}"
    )

    print(
        f"💵 Avg Revenue / Customer   : "
        f"₹{average_revenue_per_customer:,.2f}"
    )

    print(
        f"🛍️ Avg Orders / Customer    : "
        f"{average_orders_per_customer:,.2f}"
    )

    print(
        f"🔄 Repeat Customer Rate     : "
        f"{repeat_customer_rate:.2f}%"
    )

    # ========================================================
    # 7. Python Customer Segmentation
    # ========================================================

    customer_frequency["revenue_per_order"] = (
        customer_frequency["total_revenue"]
        / customer_frequency["total_orders"].replace(
            0,
            pd.NA
        )
    )

    customer_frequency["revenue_per_order"] = (
        customer_frequency["revenue_per_order"]
        .fillna(0)
    )

    customer_frequency["customer_value_band"] = pd.cut(
        customer_frequency["total_revenue"],
        bins=[
            -1,
            100000,
            300000,
            600000,
            float("inf")
        ],
        labels=[
            "Low Value",
            "Medium Value",
            "High Value",
            "Very High Value"
        ]
    )

    value_band_summary = (
        customer_frequency[
            "customer_value_band"
        ]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    value_band_summary.columns = [
        "customer_value_band",
        "customers"
    ]

    print("\n💎 CUSTOMER VALUE BANDS")
    print("-" * 70)

    print(
        value_band_summary.to_string(index=False)
    )

    # ========================================================
    # Close connection
    # ========================================================

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)
    print("✅ CUSTOMER ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()