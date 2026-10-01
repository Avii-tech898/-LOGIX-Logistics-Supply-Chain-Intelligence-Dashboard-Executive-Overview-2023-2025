import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# LOGIX - Executive Analytics
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


def load_executive_kpi(connection):
    query = """
        SELECT *
        FROM vw_executive_kpi
    """

    return pd.read_sql(query, connection)


def main():

    print("=" * 65)
    print("LOGIX - EXECUTIVE PYTHON ANALYTICS")
    print("=" * 65)

    print(f"🗄️ Database: {DB_CONFIG['database']}")

    connection = get_connection()

    print("✅ MySQL connected successfully!\n")

    # --------------------------------------------------------
    # Load executive KPI view
    # --------------------------------------------------------

    df = load_executive_kpi(connection)

    print("📊 Executive KPI Data")
    print("-" * 65)

    print(df.to_string(index=False))

    # --------------------------------------------------------
    # Basic KPI extraction
    # --------------------------------------------------------

    if not df.empty:

        row = df.iloc[0]

        print("\n" + "=" * 65)
        print("LOGIX EXECUTIVE KPIs")
        print("=" * 65)

        print(
            f"📦 Total Orders       : "
            f"{row['total_orders']:,}"
        )

        print(
            f"👥 Total Customers    : "
            f"{row['total_customers']:,}"
        )

        print(
            f"💰 Total Revenue      : "
            f"₹{row['total_revenue']:,.2f}"
        )

        print(
            f"🚚 Logistics Cost     : "
            f"₹{row['total_logistics_cost']:,.2f}"
        )

        print(
            f"❌ Failed Shipments   : "
            f"{row['failed_shipments']:,}"
        )

        print(
            f"↩️ Total Returns      : "
            f"{row['total_returns']:,}"
        )

        print(
            f"💸 Total Refunds      : "
            f"₹{row['total_refunds']:,.2f}"
        )

        print(
            f"⏱️ On-Time Delivery   : "
            f"{row['on_time_rate']:.2f}%"
        )

    connection.close()

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 65)
    print("✅ EXECUTIVE ANALYSIS COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()