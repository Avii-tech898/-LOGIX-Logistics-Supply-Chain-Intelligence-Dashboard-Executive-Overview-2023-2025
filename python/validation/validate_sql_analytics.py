import os
import re
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# ============================================================
# LOGIX - SQL Analytics Validator
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

DB_HOST = os.getenv("LOGIX_DB_HOST", "localhost")
DB_PORT = int(os.getenv("LOGIX_DB_PORT", "3306"))
DB_USER = os.getenv("LOGIX_DB_USER", "root")
DB_PASSWORD = os.getenv("LOGIX_DB_PASSWORD", "")
DB_NAME = os.getenv("LOGIX_DB_NAME", "logix")

SQL_DIR = BASE_DIR / "sql" / "04_analytics_queries"


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def split_queries(sql_text):
    """
    Split SQL file into individual statements.
    Comments are retained for identifying query numbers.
    """
    statements = []
    current = []

    for line in sql_text.splitlines():

        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        current.append(line)

        if stripped.endswith(";"):
            statement = "\n".join(current).strip()

            if statement:
                statements.append(statement)

            current = []

    if current:
        statement = "\n".join(current).strip()

        if statement:
            statements.append(statement)

    return statements


def extract_query_number(statement):
    match = re.search(
        r"Q(\d+)\.",
        statement,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


def clean_sql(statement):
    """
    Remove SQL comments before execution.
    """

    lines = []

    for line in statement.splitlines():

        stripped = line.strip()

        if stripped.startswith("--"):
            continue

        lines.append(line)

    return "\n".join(lines).strip()


def main():

    print("=" * 70)
    print("LOGIX - SQL ANALYTICS VALIDATION")
    print("=" * 70)

    print(f"📁 Project: {BASE_DIR}")
    print(f"📄 SQL Directory: {SQL_DIR}")
    print(f"🗄️ Database: {DB_NAME}")

    if not SQL_DIR.exists():

        print("\n❌ SQL analytics directory not found.")
        return

    sql_files = sorted(SQL_DIR.glob("*.sql"))

    print(f"\n📄 SQL files found: {len(sql_files)}")

    if len(sql_files) != 10:

        print("⚠️ Expected 10 analytics SQL files.")

    print("\n🔄 Connecting to MySQL...")

    try:

        connection = get_connection()

        if not connection.is_connected():
            print("❌ MySQL connection failed.")
            return

        print("✅ MySQL connected successfully!\n")

    except mysql.connector.Error as error:

        print(f"❌ MySQL connection error: {error}")
        return

    cursor = connection.cursor()

    total_queries = 0
    successful_queries = 0
    failed_queries = 0

    results = []

    # ========================================================
    # Validate SQL files
    # ========================================================

    for sql_file in sql_files:

        print("\n" + "-" * 70)
        print(f"📄 {sql_file.name}")
        print("-" * 70)

        sql_text = sql_file.read_text(
            encoding="utf-8"
        )

        statements = split_queries(sql_text)

        file_queries = 0

        for statement in statements:

            query_number = extract_query_number(statement)

            # Ignore USE statements
            cleaned = clean_sql(statement)

            if not cleaned:
                continue

            if cleaned.upper().startswith("USE LOGIX"):
                continue

            # Ignore comments-only blocks
            if not re.search(
                r"\b(SELECT|WITH|SHOW|DESCRIBE|DESC)\b",
                cleaned,
                re.IGNORECASE
            ):
                continue

            total_queries += 1
            file_queries += 1

            label = (
                f"Q{query_number:02d}"
                if query_number
                else f"Query-{total_queries}"
            )

            try:

                cursor.execute(cleaned)

                # Fetch results if available
                if cursor.with_rows:
                    cursor.fetchall()

                successful_queries += 1

                results.append({
                    "query": label,
                    "file": sql_file.name,
                    "status": "PASS",
                    "error": ""
                })

                print(f"   ✅ {label} PASS")

            except mysql.connector.Error as error:

                failed_queries += 1

                results.append({
                    "query": label,
                    "file": sql_file.name,
                    "status": "FAIL",
                    "error": str(error)
                })

                print(f"   ❌ {label} FAIL")
                print(f"      {error}")

                # Reset cursor state if needed
                try:
                    connection.rollback()
                except Exception:
                    pass

        print(f"\n   Queries detected: {file_queries}")

    # ========================================================
    # Summary
    # ========================================================

    print("\n")
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    print(f"📊 Total queries detected : {total_queries}")
    print(f"✅ Successful             : {successful_queries}")
    print(f"❌ Failed                 : {failed_queries}")

    if total_queries:
        success_rate = (
            successful_queries / total_queries
        ) * 100
    else:
        success_rate = 0

    print(f"📈 Success rate           : {success_rate:.2f}%")

    # ========================================================
    # Failed query report
    # ========================================================

    failed_results = [
        result
        for result in results
        if result["status"] == "FAIL"
    ]

    if failed_results:

        print("\n" + "=" * 70)
        print("FAILED QUERIES")
        print("=" * 70)

        for result in failed_results:

            print(
                f"\n❌ {result['query']} "
                f"({result['file']})"
            )

            print(
                f"   Error: {result['error']}"
            )

    else:

        print("\n🎉 ALL DETECTED SQL QUERIES PASSED!")

    # ========================================================
    # Save validation report
    # ========================================================

    report_file = (
        BASE_DIR
        / "documentation"
        / "SQL_VALIDATION_REPORT.txt"
    )

    report_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "LOGIX SQL ANALYTICS VALIDATION REPORT\n"
        )

        file.write(
            "=" * 60 + "\n\n"
        )

        file.write(
            f"Database: {DB_NAME}\n"
        )

        file.write(
            f"Total Queries: {total_queries}\n"
        )

        file.write(
            f"Successful: {successful_queries}\n"
        )

        file.write(
            f"Failed: {failed_queries}\n"
        )

        file.write(
            f"Success Rate: {success_rate:.2f}%\n\n"
        )

        file.write(
            "QUERY RESULTS\n"
        )

        file.write(
            "-" * 60 + "\n"
        )

        for result in results:

            file.write(
                f"{result['query']} | "
                f"{result['file']} | "
                f"{result['status']}\n"
            )

            if result["error"]:

                file.write(
                    f"ERROR: {result['error']}\n"
                )

    cursor.close()
    connection.close()

    print("\n📄 Validation report:")
    print(report_file)

    print("\n🔒 MySQL connection closed.")

    print("\n" + "=" * 70)

    if failed_queries == 0:
        print("🎉 LOGIX SQL VALIDATION PASSED")
    else:
        print("⚠️ LOGIX SQL VALIDATION COMPLETED WITH FAILURES")

    print("=" * 70)


if __name__ == "__main__":
    main()