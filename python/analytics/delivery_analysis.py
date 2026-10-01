import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Delivery & Logistics Analytics
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
    print("LOGIX - DELIVERY & LOGISTICS PYTHON ANALYTICS")
    print("=" * 70)

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # ========================================================
    # 1. Shipment Performance
    # ========================================================

    shipment_query = """
        SELECT
            shipment_status,
            COUNT(*) AS shipments,
            ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
            ROUND(AVG(distance_km), 2) AS avg_distance_km
        FROM shipments
        GROUP BY shipment_status
        ORDER BY shipments DESC
    """

    shipment_analysis = pd.read_sql(
        shipment_query,
        connection
    )

    print("🚚 SHIPMENT PERFORMANCE")
    print("-" * 70)

    print(
        shipment_analysis.to_string(index=False)
    )

    # ========================================================
    # 2. Delivery Type Performance
    # ========================================================

    delivery_type_query = """
        SELECT
            delivery_type,
            COUNT(*) AS shipments,
            SUM(
                CASE
                    WHEN shipment_status = 'Delivered'
                    THEN 1 ELSE 0
                END
            ) AS delivered_shipments,
            SUM(
                CASE
                    WHEN shipment_status = 'Failed'
                    THEN 1 ELSE 0
                END
            ) AS failed_shipments,
            ROUND(AVG(distance_km), 2) AS avg_distance_km,
            ROUND(AVG(shipping_cost), 2) AS avg_shipping_cost
        FROM shipments
        GROUP BY delivery_type
        ORDER BY shipments DESC
    """

    delivery_type = pd.read_sql(
        delivery_type_query,
        connection
    )

    print("\n📦 DELIVERY TYPE PERFORMANCE")
    print("-" * 70)

    print(
        delivery_type.to_string(index=False)
    )

    # ========================================================
    # 3. Delivery Partner Performance
    # ========================================================

    partner_query = """
        SELECT
            dp.partner_id,
            dp.partner_name,
            COUNT(s.shipment_id) AS shipments,
            SUM(
                CASE
                    WHEN s.shipment_status = 'Delivered'
                    THEN 1 ELSE 0
                END
            ) AS delivered_shipments,
            SUM(
                CASE
                    WHEN s.shipment_status = 'Failed'
                    THEN 1 ELSE 0
                END
            ) AS failed_shipments,
            ROUND(SUM(s.shipping_cost), 2) AS total_shipping_cost,
            ROUND(AVG(s.distance_km), 2) AS avg_distance_km
        FROM delivery_partners dp
        LEFT JOIN shipments s
            ON dp.partner_id = s.delivery_partner_id
        GROUP BY
            dp.partner_id,
            dp.partner_name
        ORDER BY shipments DESC
    """

    partner_analysis = pd.read_sql(
        partner_query,
        connection
    )

    print("\n🏢 DELIVERY PARTNER PERFORMANCE")
    print("-" * 70)

    print(
        partner_analysis.to_string(index=False)
    )

    # ========================================================
    # 4. Warehouse Delivery Performance
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

    print("\n🏭 WAREHOUSE DELIVERY PERFORMANCE")
    print("-" * 70)

    print(
        warehouse_analysis.to_string(index=False)
    )

    # ========================================================
    # 5. Delivery Attempts
    # ========================================================

    attempt_query = """
        SELECT
            attempt_outcome,
            COUNT(*) AS attempts
        FROM delivery_attempts
        GROUP BY attempt_outcome
        ORDER BY attempts DESC
    """

    attempt_analysis = pd.read_sql(
        attempt_query,
        connection
    )

    print("\n📍 DELIVERY ATTEMPT ANALYSIS")
    print("-" * 70)

    print(
        attempt_analysis.to_string(index=False)
    )

    # ========================================================
    # 6. SLA Performance
    # ========================================================

    sla_query = """
        SELECT
            delivery_type,
            sla_days,
            COUNT(*) AS shipments,
            SUM(
                CASE
                    WHEN shipment_status = 'Delivered'
                         AND actual_delivery_date <= expected_delivery_date
                    THEN 1
                    ELSE 0
                END
            ) AS on_time_shipments,
            SUM(
                CASE
                    WHEN shipment_status = 'Delivered'
                         AND actual_delivery_date > expected_delivery_date
                    THEN 1
                    ELSE 0
                END
            ) AS late_shipments
        FROM shipments
        GROUP BY
            delivery_type,
            sla_days
        ORDER BY sla_days
    """

    sla_analysis = pd.read_sql(
        sla_query,
        connection
    )

    print("\n⏱️ SLA PERFORMANCE")
    print("-" * 70)

    print(
        sla_analysis.to_string(index=False)
    )

    # ========================================================
    # 7. Python Delivery Metrics
    # ========================================================

    total_shipments = len(
        pd.read_sql(
            "SELECT shipment_id FROM shipments",
            connection
        )
    )

    delivered_shipments = (
        shipment_analysis.loc[
            shipment_analysis["shipment_status"] == "Delivered",
            "shipments"
        ].sum()
    )

    failed_shipments = (
        shipment_analysis.loc[
            shipment_analysis["shipment_status"] == "Failed",
            "shipments"
        ].sum()
    )

    delayed_shipments = (
        shipment_analysis.loc[
            shipment_analysis["shipment_status"] == "Delayed",
            "shipments"
        ].sum()
    )

    total_shipping_cost = shipment_analysis[
        "total_shipping_cost"
    ].sum()

    avg_distance = shipment_analysis[
        "avg_distance_km"
    ].mean()

    delivery_success_rate = (
        delivered_shipments / total_shipments * 100
        if total_shipments > 0
        else 0
    )

    failure_rate = (
        failed_shipments / total_shipments * 100
        if total_shipments > 0
        else 0
    )

    delay_rate = (
        delayed_shipments / total_shipments * 100
        if total_shipments > 0
        else 0
    )

    # ========================================================
    # 8. Overall Delivery Summary
    # ========================================================

    print("\n" + "=" * 70)
    print("🚚 DELIVERY & LOGISTICS SUMMARY")
    print("=" * 70)

    print(
        f"📦 Total Shipments          : "
        f"{total_shipments:,.0f}"
    )

    print(
        f"✅ Delivered Shipments      : "
        f"{delivered_shipments:,.0f}"
    )

    print(
        f"❌ Failed Shipments         : "
        f"{failed_shipments:,.0f}"
    )

    print(
        f"⚠️ Delayed Shipments        : "
        f"{delayed_shipments:,.0f}"
    )

    print(
        f"📈 Delivery Success Rate    : "
        f"{delivery_success_rate:.2f}%"
    )

    print(
        f"❌ Shipment Failure Rate    : "
        f"{failure_rate:.2f}%"
    )

    print(
        f"⚠️ Shipment Delay Rate      : "
        f"{delay_rate:.2f}%"
    )

    print(
        f"💰 Total Shipping Cost      : "
        f"₹{total_shipping_cost:,.2f}"
    )

    print(
        f"📍 Avg Distance Metric      : "
        f"{avg_distance:,.2f} km"
    )

    # ========================================================
    # 9. Python SLA Metrics
    # ========================================================

    if not sla_analysis.empty:

        sla_analysis["on_time_rate"] = (
            sla_analysis["on_time_shipments"]
            / sla_analysis["shipments"]
            * 100
        ).fillna(0)

        sla_analysis["late_rate"] = (
            sla_analysis["late_shipments"]
            / sla_analysis["shipments"]
            * 100
        ).fillna(0)

        print("\n⏱️ PYTHON-CALCULATED SLA METRICS")
        print("-" * 70)

        print(
            sla_analysis[
                [
                    "delivery_type",
                    "sla_days",
                    "shipments",
                    "on_time_shipments",
                    "late_shipments",
                    "on_time_rate",
                    "late_rate"
                ]
            ].to_string(index=False)
        )

    # ========================================================
    # Close Connection
    # ========================================================

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)
    print("✅ DELIVERY ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()