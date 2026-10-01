import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# ============================================================
# LOGIX - MySQL Schema Exporter
# ============================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load project .env
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE, override=True)

# Database configuration
DB_HOST = os.getenv("LOGIX_DB_HOST", "localhost")
DB_PORT = int(os.getenv("LOGIX_DB_PORT", "3306"))
DB_USER = os.getenv("LOGIX_DB_USER", "root")
DB_PASSWORD = os.getenv("LOGIX_DB_PASSWORD", "")
DB_NAME = os.getenv("LOGIX_DB_NAME", "logix")

# Output SQL file
OUTPUT_FILE = BASE_DIR / "sql" / "02_schema" / "01_logix_schema.sql"


def get_connection():
    """Create MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def main():

    print("=" * 60)
    print("LOGIX - MySQL Schema Export")
    print("=" * 60)

    print(f"📁 Project: {BASE_DIR}")
    print(f"📄 .env: {ENV_FILE}")
    print(f"🗄️ Database: {DB_NAME}")

    connection = get_connection()

    if not connection.is_connected():
        print("❌ MySQL connection failed.")
        return

    print("✅ MySQL connected successfully!\n")

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Get tables
    # --------------------------------------------------------

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
    """, (DB_NAME,))

    tables = [row[0] for row in cursor.fetchall()]

    print(f"📊 Tables found: {len(tables)}")

    # --------------------------------------------------------
    # Start SQL documentation
    # --------------------------------------------------------

    sql_output = []

    sql_output.append("-- =========================================================")
    sql_output.append("-- LOGIX - Logistics & Supply Chain Intelligence Platform")
    sql_output.append("-- MySQL Database Schema")
    sql_output.append("-- Generated automatically from the existing database")
    sql_output.append("-- =========================================================")
    sql_output.append("")
    sql_output.append("CREATE DATABASE IF NOT EXISTS logix")
    sql_output.append("CHARACTER SET utf8mb4")
    sql_output.append("COLLATE utf8mb4_unicode_ci;")
    sql_output.append("")
    sql_output.append("USE logix;")
    sql_output.append("")

    # --------------------------------------------------------
    # Export each table
    # --------------------------------------------------------

    for table in tables:

        print(f"   ✔ Exporting: {table}")

        sql_output.append("")
        sql_output.append("-- =========================================================")
        sql_output.append(f"-- TABLE: {table}")
        sql_output.append("-- =========================================================")
        sql_output.append("")

        # Get CREATE TABLE statement
        cursor.execute(f"SHOW CREATE TABLE `{table}`")

        result = cursor.fetchone()

        if result:
            create_statement = result[1]

            sql_output.append(create_statement + ";")
            sql_output.append("")

    # --------------------------------------------------------
    # Foreign Keys
    # --------------------------------------------------------

    sql_output.append("")
    sql_output.append("-- =========================================================")
    sql_output.append("-- FOREIGN KEY RELATIONSHIPS")
    sql_output.append("-- =========================================================")
    sql_output.append("")

    cursor.execute("""
        SELECT
            TABLE_NAME,
            COLUMN_NAME,
            CONSTRAINT_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s
          AND REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY TABLE_NAME, COLUMN_NAME
    """, (DB_NAME,))

    foreign_keys = cursor.fetchall()

    if foreign_keys:

        for row in foreign_keys:

            table_name = row[0]
            column_name = row[1]
            constraint_name = row[2]
            referenced_table = row[3]
            referenced_column = row[4]

            sql_output.append(
                f"-- {table_name}.{column_name} "
                f"-> {referenced_table}.{referenced_column} "
                f"[{constraint_name}]"
            )

    else:
        sql_output.append("-- No foreign key relationships found.")

    sql_output.append("")

    # --------------------------------------------------------
    # Analytical Views
    # --------------------------------------------------------

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
    """, (DB_NAME,))

    views = [row[0] for row in cursor.fetchall()]

    sql_output.append("-- =========================================================")
    sql_output.append("-- ANALYTICAL VIEWS")
    sql_output.append("-- =========================================================")
    sql_output.append("")

    for view in views:

        print(f"   ✔ Found view: {view}")

        cursor.execute(f"SHOW CREATE VIEW `{view}`")

        result = cursor.fetchone()

        if result:

            view_definition = result[1]

            sql_output.append("")
            sql_output.append(f"-- VIEW: {view}")
            sql_output.append("")
            sql_output.append(view_definition + ";")
            sql_output.append("")

    # --------------------------------------------------------
    # Write file
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(sql_output))

    # --------------------------------------------------------
    # Close connection
    # --------------------------------------------------------

    cursor.close()
    connection.close()

    print("\n" + "=" * 60)
    print("✅ SCHEMA EXPORT COMPLETED")
    print("=" * 60)

    print(f"\n📄 Output file:")
    print(OUTPUT_FILE)

    print(f"\n📊 Tables exported: {len(tables)}")
    print(f"👁️ Views exported: {len(views)}")

    print("\n🔒 MySQL connection closed.")


if __name__ == "__main__":
    main()