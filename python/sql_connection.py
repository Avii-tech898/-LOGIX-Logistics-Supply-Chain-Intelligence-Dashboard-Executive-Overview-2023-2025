import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

print("🔄 Connecting to LOGIX MySQL...")

connection = mysql.connector.connect(
    host=os.getenv("LOGIX_DB_HOST", "localhost"),
    port=int(os.getenv("LOGIX_DB_PORT", "3306")),
    user=os.getenv("LOGIX_DB_USER", "root"),
    password=os.getenv("LOGIX_DB_PASSWORD", ""),
    database=os.getenv("LOGIX_DB_NAME", "logix")
)

print("Connection object created.")

if connection.is_connected():
    print("✅ MySQL Connected Successfully!")
    print("📊 Database:", os.getenv("LOGIX_DB_NAME", "logix"))

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")

    print("\n📋 LOGIX Tables:")
    for table in cursor.fetchall():
        print("   ✔", table[0])

    cursor.close()
    connection.close()

    print("\n🔒 Connection closed.")
else:
    print("❌ MySQL connection failed.")