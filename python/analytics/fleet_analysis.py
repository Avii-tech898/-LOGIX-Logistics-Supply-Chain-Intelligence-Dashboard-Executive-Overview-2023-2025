import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Fleet Analytics
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
    print("LOGIX - FLEET PYTHON ANALYTICS")
    print("=" * 70)

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # ========================================================
    # 1. Fleet Overview
    # ========================================================

    fleet_overview_query = """
        SELECT
            vehicle_type,
            fuel_type,
            COUNT(*) AS vehicles,
            SUM(
                CASE
                    WHEN status = 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_vehicles,
            SUM(
                CASE
                    WHEN status != 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS inactive_vehicles,
            ROUND(AVG(capacity_kg), 2) AS avg_capacity_kg,
            ROUND(AVG(model_year), 0) AS avg_model_year
        FROM vehicles
        GROUP BY
            vehicle_type,
            fuel_type
        ORDER BY vehicles DESC
    """

    fleet_overview = pd.read_sql(
        fleet_overview_query,
        connection
    )

    print("🚛 FLEET OVERVIEW")
    print("-" * 70)

    print(
        fleet_overview.to_string(index=False)
    )

    # ========================================================
    # 2. Driver Master Analysis
    # ========================================================

    driver_query = """
        SELECT
            driver_id,
            driver_name,
            city,
            experience_years,
            rating,
            employment_type,
            status
        FROM drivers
        ORDER BY
            rating DESC,
            experience_years DESC
    """

    driver_analysis = pd.read_sql(
        driver_query,
        connection
    )

    print("\n👨‍✈️ DRIVER MASTER ANALYSIS")
    print("-" * 70)

    print(
        driver_analysis.head(30).to_string(index=False)
    )

    # ========================================================
    # 3. Vehicle Master Analysis
    # ========================================================

    vehicle_query = """
        SELECT
            vehicle_id,
            vehicle_number,
            vehicle_type,
            capacity_kg,
            fuel_type,
            model_year,
            driver_id,
            status
        FROM vehicles
        ORDER BY
            vehicle_type,
            vehicle_id
    """

    vehicle_analysis = pd.read_sql(
        vehicle_query,
        connection
    )

    print("\n🚚 VEHICLE MASTER ANALYSIS")
    print("-" * 70)

    print(
        vehicle_analysis.head(30).to_string(index=False)
    )

    # ========================================================
    # 4. Fleet by Fuel Type
    # ========================================================

    fuel_query = """
        SELECT
            fuel_type,
            COUNT(*) AS vehicles,
            SUM(
                CASE
                    WHEN status = 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_vehicles,
            SUM(
                CASE
                    WHEN status != 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS inactive_vehicles,
            ROUND(AVG(capacity_kg), 2) AS avg_capacity_kg
        FROM vehicles
        GROUP BY fuel_type
        ORDER BY vehicles DESC
    """

    fuel_analysis = pd.read_sql(
        fuel_query,
        connection
    )

    print("\n⛽ FLEET BY FUEL TYPE")
    print("-" * 70)

    print(
        fuel_analysis.to_string(index=False)
    )

    # ========================================================
    # 5. Fleet by Vehicle Type
    # ========================================================

    vehicle_type_query = """
        SELECT
            vehicle_type,
            COUNT(*) AS vehicles,
            SUM(
                CASE
                    WHEN status = 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_vehicles,
            SUM(
                CASE
                    WHEN status != 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS inactive_vehicles,
            ROUND(AVG(capacity_kg), 2) AS avg_capacity_kg
        FROM vehicles
        GROUP BY vehicle_type
        ORDER BY vehicles DESC
    """

    vehicle_type_analysis = pd.read_sql(
        vehicle_type_query,
        connection
    )

    print("\n🚛 FLEET BY VEHICLE TYPE")
    print("-" * 70)

    print(
        vehicle_type_analysis.to_string(index=False)
    )

    # ========================================================
    # 6. Driver Experience Analysis
    # ========================================================

    experience_query = """
        SELECT
            CASE
                WHEN experience_years < 2
                    THEN '0-1 Years'
                WHEN experience_years < 5
                    THEN '2-4 Years'
                WHEN experience_years < 10
                    THEN '5-9 Years'
                ELSE '10+ Years'
            END AS experience_band,

            COUNT(*) AS drivers,

            ROUND(
                AVG(rating),
                2
            ) AS avg_rating,

            ROUND(
                AVG(experience_years),
                2
            ) AS avg_experience_years

        FROM drivers

        GROUP BY
            CASE
                WHEN experience_years < 2
                    THEN '0-1 Years'
                WHEN experience_years < 5
                    THEN '2-4 Years'
                WHEN experience_years < 10
                    THEN '5-9 Years'
                ELSE '10+ Years'
            END

        ORDER BY
            MIN(experience_years)
    """

    experience_analysis = pd.read_sql(
        experience_query,
        connection
    )

    print("\n👨‍✈️ DRIVER EXPERIENCE ANALYSIS")
    print("-" * 70)

    print(
        experience_analysis.to_string(index=False)
    )

    # ========================================================
    # 7. Driver Employment Type
    # ========================================================

    employment_query = """
        SELECT
            employment_type,
            COUNT(*) AS drivers,
            SUM(
                CASE
                    WHEN status = 'Active'
                    THEN 1
                    ELSE 0
                END
            ) AS active_drivers,
            ROUND(
                AVG(rating),
                2
            ) AS avg_rating,
            ROUND(
                AVG(experience_years),
                2
            ) AS avg_experience_years
        FROM drivers
        GROUP BY employment_type
        ORDER BY drivers DESC
    """

    employment_analysis = pd.read_sql(
        employment_query,
        connection
    )

    print("\n👥 DRIVER EMPLOYMENT ANALYSIS")
    print("-" * 70)

    print(
        employment_analysis.to_string(index=False)
    )

    # ========================================================
    # 8. Overall Logistics Metrics
    #
    # NOTE:
    # shipments table does NOT contain vehicle_id.
    # Therefore these are overall logistics metrics and
    # are NOT attributed to individual vehicles/drivers.
    # ========================================================

    logistics_query = """
        SELECT
            COUNT(*) AS total_shipments,

            SUM(
                CASE
                    WHEN shipment_status = 'Delivered'
                    THEN 1
                    ELSE 0
                END
            ) AS delivered_shipments,

            SUM(
                CASE
                    WHEN shipment_status = 'Failed'
                    THEN 1
                    ELSE 0
                END
            ) AS failed_shipments,

            SUM(
                CASE
                    WHEN shipment_status = 'Delayed'
                    THEN 1
                    ELSE 0
                END
            ) AS delayed_shipments,

            ROUND(
                SUM(distance_km),
                2
            ) AS total_distance_km,

            ROUND(
                SUM(shipping_cost),
                2
            ) AS total_shipping_cost,

            ROUND(
                AVG(distance_km),
                2
            ) AS avg_distance_km,

            ROUND(
                AVG(shipping_cost),
                2
            ) AS avg_shipping_cost

        FROM shipments
    """

    logistics_analysis = pd.read_sql(
        logistics_query,
        connection
    )

    print("\n📦 OVERALL LOGISTICS METRICS")
    print("-" * 70)

    print(
        logistics_analysis.to_string(index=False)
    )

    # ========================================================
    # 9. Python Fleet Master Metrics
    # ========================================================

    total_vehicles = len(
        vehicle_analysis
    )

    active_vehicles = (
        vehicle_analysis["status"] == "Active"
    ).sum()

    inactive_vehicles = (
        vehicle_analysis["status"] != "Active"
    ).sum()

    total_drivers = len(
        driver_analysis
    )

    active_drivers = (
        driver_analysis["status"] == "Active"
    ).sum()

    inactive_drivers = (
        driver_analysis["status"] != "Active"
    ).sum()

    total_capacity = vehicle_analysis[
        "capacity_kg"
    ].sum()

    average_vehicle_capacity = vehicle_analysis[
        "capacity_kg"
    ].mean()

    average_driver_rating = driver_analysis[
        "rating"
    ].mean()

    average_driver_experience = driver_analysis[
        "experience_years"
    ].mean()

    vehicle_driver_assignment = (
        vehicle_analysis["driver_id"]
        .notna()
        .sum()
    )

    # ========================================================
    # 10. Python Logistics Metrics
    # ========================================================

    total_shipments = int(
        logistics_analysis.loc[
            0,
            "total_shipments"
        ]
    )

    delivered_shipments = int(
        logistics_analysis.loc[
            0,
            "delivered_shipments"
        ]
    )

    failed_shipments = int(
        logistics_analysis.loc[
            0,
            "failed_shipments"
        ]
    )

    delayed_shipments = int(
        logistics_analysis.loc[
            0,
            "delayed_shipments"
        ]
    )

    total_distance = float(
        logistics_analysis.loc[
            0,
            "total_distance_km"
        ]
    )

    total_shipping_cost = float(
        logistics_analysis.loc[
            0,
            "total_shipping_cost"
        ]
    )

    delivery_rate = (
        delivered_shipments /
        total_shipments *
        100
        if total_shipments > 0
        else 0
    )

    failure_rate = (
        failed_shipments /
        total_shipments *
        100
        if total_shipments > 0
        else 0
    )

    delay_rate = (
        delayed_shipments /
        total_shipments *
        100
        if total_shipments > 0
        else 0
    )

    cost_per_km = (
        total_shipping_cost /
        total_distance
        if total_distance > 0
        else 0
    )

    # ========================================================
    # 11. Fleet Summary
    # ========================================================

    print("\n" + "=" * 70)
    print("🚛 FLEET SUMMARY")
    print("=" * 70)

    print(
        f"🚚 Total Vehicles          : "
        f"{total_vehicles:,.0f}"
    )

    print(
        f"✅ Active Vehicles         : "
        f"{active_vehicles:,.0f}"
    )

    print(
        f"⏸️ Inactive Vehicles       : "
        f"{inactive_vehicles:,.0f}"
    )

    print(
        f"👨‍✈️ Total Drivers           : "
        f"{total_drivers:,.0f}"
    )

    print(
        f"✅ Active Drivers          : "
        f"{active_drivers:,.0f}"
    )

    print(
        f"⏸️ Inactive Drivers        : "
        f"{inactive_drivers:,.0f}"
    )

    print(
        f"⚖️ Total Fleet Capacity    : "
        f"{total_capacity:,.2f} kg"
    )

    print(
        f"⚖️ Avg Vehicle Capacity    : "
        f"{average_vehicle_capacity:,.2f} kg"
    )

    print(
        f"⭐ Avg Driver Rating       : "
        f"{average_driver_rating:.2f}"
    )

    print(
        f"📅 Avg Driver Experience   : "
        f"{average_driver_experience:.2f} years"
    )

    print(
        f"🔗 Assigned Vehicles       : "
        f"{vehicle_driver_assignment:,.0f}"
    )

    print("\n📦 OVERALL LOGISTICS")
    print("-" * 70)

    print(
        f"📦 Total Shipments         : "
        f"{total_shipments:,.0f}"
    )

    print(
        f"✅ Delivered Shipments     : "
        f"{delivered_shipments:,.0f}"
    )

    print(
        f"❌ Failed Shipments        : "
        f"{failed_shipments:,.0f}"
    )

    print(
        f"⚠️ Delayed Shipments       : "
        f"{delayed_shipments:,.0f}"
    )

    print(
        f"📈 Delivery Rate           : "
        f"{delivery_rate:.2f}%"
    )

    print(
        f"❌ Failure Rate            : "
        f"{failure_rate:.2f}%"
    )

    print(
        f"⚠️ Delay Rate              : "
        f"{delay_rate:.2f}%"
    )

    print(
        f"📍 Total Distance          : "
        f"{total_distance:,.2f} km"
    )

    print(
        f"💰 Total Shipping Cost     : "
        f"₹{total_shipping_cost:,.2f}"
    )

    print(
        f"💵 Shipping Cost / KM      : "
        f"₹{cost_per_km:,.2f}"
    )

    # ========================================================
    # 12. Python Vehicle Capacity Bands
    # ========================================================

    vehicle_analysis["capacity_band"] = pd.cut(
        vehicle_analysis["capacity_kg"],
        bins=[
            -1,
            100,
            1000,
            5000,
            float("inf")
        ],
        labels=[
            "Light",
            "Medium",
            "Heavy",
            "Very Heavy"
        ]
    )

    capacity_summary = (
        vehicle_analysis["capacity_band"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    capacity_summary.columns = [
        "capacity_band",
        "vehicles"
    ]

    print("\n⚖️ VEHICLE CAPACITY DISTRIBUTION")
    print("-" * 70)

    print(
        capacity_summary.to_string(index=False)
    )

    # ========================================================
    # 13. Python Driver Rating Bands
    # ========================================================

    driver_analysis["rating_band"] = pd.cut(
        driver_analysis["rating"],
        bins=[
            -1,
            3,
            4,
            4.5,
            float("inf")
        ],
        labels=[
            "Below 3",
            "3-4",
            "4-4.5",
            "Above 4.5"
        ]
    )

    rating_summary = (
        driver_analysis["rating_band"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_summary.columns = [
        "rating_band",
        "drivers"
    ]

    print("\n⭐ DRIVER RATING DISTRIBUTION")
    print("-" * 70)

    print(
        rating_summary.to_string(index=False)
    )

    # ========================================================
    # 14. Important Data Model Note
    # ========================================================

    print("\n" + "=" * 70)
    print("ℹ️ FLEET DATA MODEL NOTE")
    print("=" * 70)

    print(
        "Shipments are not directly linked to vehicles/drivers "
        "in the current LOGIX schema."
    )

    print(
        "Therefore vehicle-level shipment counts, driver-level "
        "delivery rates and vehicle-level shipping costs are "
        "not calculated in this module."
    )

    print(
        "This avoids creating unsupported or duplicated "
        "fleet-performance metrics."
    )

    # ========================================================
    # Close Connection
    # ========================================================

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)
    print("✅ FLEET ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()