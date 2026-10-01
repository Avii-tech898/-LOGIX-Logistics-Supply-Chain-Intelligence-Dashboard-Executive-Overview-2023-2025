import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# ============================================================
# LOGIX - MySQL View Exporter
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

DB_HOST = os.getenv("LOGIX_DB_HOST", "localhost")
DB_PORT = int(os.getenv("LOGIX_DB_PORT", "3306"))
DB_USER = os.getenv("LOGIX_DB_USER", "root")
DB_PASSWORD = os.getenv("LOGIX_DB_PASSWORD", "")
DB_NAME = os.getenv("LOGIX_DB_NAME", "logix")

OUTPUT_DIR = BASE_DIR / "sql" / "03_views"


def main():

    print("=" * 60)
    print("LOGIX - MySQL View Export")
    print("=" * 60)

    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if not connection.is_connected():
        print("❌ MySQL connection failed.")
        return

    print("✅ MySQL connected successfully!")
    print(f"🗄️ Database: {DB_NAME}\n")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
    """, (DB_NAME,))

    views = [row[0] for row in cursor.fetchall()]

    print(f"👁️ Views found: {len(views)}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for index, view in enumerate(views, start=1):

        print(f"   ✔ Exporting {view}")

        cursor.execute(f"SHOW CREATE VIEW `{view}`")

        result = cursor.fetchone()

        if not result:
            continue

        view_definition = result[1]

        file_name = f"{index:02d}_{view}.sql"
        output_file = OUTPUT_DIR / file_name

        content = f"""-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `{view}`;

{view_definition};

"""

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)

    cursor.close()
    connection.close()

    print("\n" + "=" * 60)
    print("✅ VIEW EXPORT COMPLETED")
    print("=" * 60)

    print(f"📁 Output directory:")
    print(OUTPUT_DIR)

    print(f"\n👁️ Views exported: {len(views)}")
    print("🔒 MySQL connection closed.")


if __name__ == "__main__":
    main()