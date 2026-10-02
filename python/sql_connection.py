import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

# ============================================================
# LOAD PROJECT ROOT .ENV
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

print("🔄 Connecting to LOGIX MySQL...")
print("📁 .env:", ENV_FILE)
print("📄 .env exists:", ENV_FILE.exists())

# ============================================================
# READ DATABASE SETTINGS
# ============================================================

DB_HOST = os.getenv("LOGIX_DB_HOST", "localhost")
DB_PORT = int(os.getenv("LOGIX_DB_PORT", "3306"))
DB_USER = os.getenv("LOGIX_DB_USER", "root")
DB_PASSWORD = os.getenv("LOGIX_DB_PASSWORD", "")
DB_NAME = os.getenv("LOGIX_DB_NAME", "logix")

print("🖥️ Host:", DB_HOST)
print("🔌 Port:", DB_PORT)
print("👤 User:", DB_USER)
print("🔐 Password loaded:", "YES" if DB_PASSWORD else "NO")
print("📊 Database:", DB_NAME)

# ============================================================
# VALIDATE PASSWORD
# ============================================================

if not DB_PASSWORD:
    raise ValueError(
        "\n❌ MySQL password is missing!\n"
        f"Please check this file:\n{ENV_FILE}\n"
        "and make sure LOGIX_DB_PASSWORD is set."
    )

# ============================================================
# CONNECT MYSQL
# ============================================================

connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# ============================================================
# VERIFY CONNECTION
# ============================================================

if connection.is_connected():

    print("\n✅ MySQL Connected Successfully!")
    print("📊 Database:", DB_NAME)

    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")
    current_db = cursor.fetchone()[0]

    print("🗄️ Current Database:", current_db)

    cursor.execute("SHOW TABLES")

    print("\n📋 LOGIX Tables:")

    for table in cursor.fetchall():
        print("   ✔", table[0])

    cursor.close()
    connection.close()

    print("\n🔒 Connection closed.")