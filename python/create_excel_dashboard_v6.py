
import os
import getpass
import mysql.connector

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.axis import ChartLines


# ============================================================
# LOGIX V6 — FINAL EXECUTIVE DASHBOARD
# Direct MySQL -> Excel Dashboard
# ============================================================

OUTPUT_FILE = os.path.join(
    "excel",
    "LOGIX_Executive_Dashboard_v6.xlsx"
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "database": "logix"
}


# ============================================================
# THEME
# ============================================================

DARK_BLUE = "17365D"
BLUE = "1F4E78"
MID_BLUE = "2F75B5"
LIGHT_BLUE = "D9EAF7"
WHITE = "FFFFFF"
LIGHT_GRAY = "F3F6F9"
BORDER_BLUE = "B4C7E7"
GREEN = "E2F0D9"
GOLD = "FFF2CC"
RED = "F4CCCC"


# ============================================================
# STYLES
# ============================================================

title_fill = PatternFill("solid", fgColor=DARK_BLUE)
section_fill = PatternFill("solid", fgColor=BLUE)
kpi_fill = PatternFill("solid", fgColor=LIGHT_BLUE)
white_font = Font(color=WHITE, bold=True)
title_font = Font(color=WHITE, bold=True, size=20)
subtitle_font = Font(color="666666", italic=True, size=10)
kpi_label_font = Font(bold=True, size=11)
kpi_value_font = Font(bold=True, size=14)
small_font = Font(size=9, color="666666")

thin_side = Side(style="thin", color=BORDER_BLUE)
thin_border = Border(
    left=thin_side,
    right=thin_side,
    top=thin_side,
    bottom=thin_side
)


# ============================================================
# MYSQL HELPERS
# ============================================================

def fetch_all(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def get_connection():
    # Replace only the value below with your existing MySQL root password.
    # Do not share the password in chat.
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="avanish@123",
        database="logix"
    )


# ============================================================
# CHART HELPERS
# ============================================================

def configure_chart(chart, title, width=12.8, height=7.2):
    chart.title = title
    chart.style = 10
    chart.width = width
    chart.height = height

    # Keep charts clean: categories belong on the axis,
    # not in a legend or as overlapping data labels.
    chart.legend = None
    chart.display_blanks = "gap"

    if chart.y_axis:
        chart.y_axis.majorGridlines = ChartLines()
        chart.y_axis.tickLblPos = "nextTo"
        chart.y_axis.delete = False

    if chart.x_axis:
        chart.x_axis.delete = False

    return chart


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("LOGIX — PROFESSIONAL EXECUTIVE DASHBOARD V4")
    print("=" * 70)

    os.makedirs("excel", exist_ok=True)

    # ========================================================
    # MYSQL CONNECTION
    # ========================================================

    print("\nConnecting to MySQL...")

    connection = get_connection()
    cursor = connection.cursor()

    print("MySQL connection successful.")

    try:

        # ====================================================
        # 1. EXECUTIVE KPI
        # ====================================================

        print("\nFetching Executive KPIs...")

        kpi_query = """
        SELECT
            total_orders,
            total_customers,
            total_revenue,
            total_logistics_cost,
            failed_shipments,
            total_returns,
            total_refunds,
            on_time_rate
        FROM vw_executive_kpi
        """

        cursor.execute(kpi_query)
        kpi = cursor.fetchone()

        if not kpi:
            raise ValueError(
                "No data returned from vw_executive_kpi."
            )

        (
            total_orders,
            total_customers,
            total_revenue,
            total_logistics_cost,
            failed_shipments,
            total_returns,
            total_refunds,
            on_time_rate
        ) = kpi

        # ====================================================
        # 2. MONTHLY SALES
        # ====================================================

        print("Fetching monthly sales...")

        monthly_query = """
        SELECT
            order_month,
            total_orders,
            revenue
        FROM vw_monthly_sales
        ORDER BY order_month
        """

        monthly_data = fetch_all(
            cursor,
            monthly_query
        )

        # ====================================================
        # 3. CUSTOMER SEGMENT REVENUE
        # ====================================================

        print("Fetching customer segment revenue...")

        segment_query = """
        SELECT
            customer_segment,
            ROUND(SUM(line_total), 2) AS revenue
        FROM vw_sales_analysis
        GROUP BY customer_segment
        ORDER BY revenue DESC
        """

        segment_data = fetch_all(
            cursor,
            segment_query
        )

        # ====================================================
        # 4. CATEGORY REVENUE
        # ====================================================

        print("Fetching category revenue...")

        category_query = """
        SELECT
            category,
            ROUND(SUM(line_total), 2) AS revenue
        FROM vw_sales_analysis
        GROUP BY category
        ORDER BY revenue DESC
        """

        category_data = fetch_all(
            cursor,
            category_query
        )

        # ====================================================
        # 5. DELIVERY PERFORMANCE
        # ====================================================

        print("Fetching delivery performance...")

        delivery_query = """
        SELECT
            delivery_performance,
            COUNT(*) AS shipment_count
        FROM vw_delivery_performance
        GROUP BY delivery_performance
        ORDER BY shipment_count DESC
        """

        delivery_data = fetch_all(
            cursor,
            delivery_query
        )

        # ====================================================
        # 6. WAREHOUSE PERFORMANCE
        # ====================================================

        print("Fetching warehouse performance...")

        warehouse_query = """
        SELECT
            warehouse_name,
            total_shipments,
            total_shipping_cost,
            on_time_rate
        FROM vw_warehouse_performance
        ORDER BY total_shipments DESC
        """

        warehouse_data = fetch_all(
            cursor,
            warehouse_query
        )

    finally:

        cursor.close()
        connection.close()

        print("MySQL connection closed.")

    # ========================================================
    # CREATE WORKBOOK
    # ========================================================

    print("\nCreating professional dashboard workbook...")

    wb = Workbook()

    dashboard = wb.active
    dashboard.title = "Executive_Dashboard"

    data_ws = wb.create_sheet("Chart_Data")

    dashboard.sheet_view.showGridLines = False

    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    widths = {
        "A": 13, "B": 13, "C": 13, "D": 13,
        "E": 13, "F": 13, "G": 13,
        "H": 13, "I": 13, "J": 13,
        "K": 13, "L": 13, "M": 13, "N": 13
    }

    for column, width in widths.items():
        dashboard.column_dimensions[column].width = width

    # ========================================================
    # TITLE
    # ========================================================

    dashboard.merge_cells("A1:N2")

    dashboard["A1"] = (
        "LOGIX — LOGISTICS & SUPPLY CHAIN "
        "INTELLIGENCE DASHBOARD"
    )

    dashboard["A1"].fill = title_fill
    dashboard["A1"].font = title_font
    dashboard["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    dashboard.row_dimensions[1].height = 30
    dashboard.row_dimensions[2].height = 30

    # ========================================================
    # SUBTITLE
    # ========================================================

    dashboard.merge_cells("A3:N3")

    dashboard["A3"] = (
        "Executive Business Performance Overview | "
        "LOGIX Analytics Platform"
    )

    dashboard["A3"].font = subtitle_font
    dashboard["A3"].alignment = Alignment(
        horizontal="center"
    )

    # ========================================================
    # KPI CARDS
    # ========================================================

    kpis = [
        ("A5:B7", "Total Orders", f"{total_orders:,}"),
        ("C5:D7", "Total Customers", f"{total_customers:,}"),
        ("E5:G7", "Total Revenue", f"₹{total_revenue:,.2f}"),
        ("H5:J7", "Logistics Cost", f"₹{total_logistics_cost:,.2f}"),
        ("K5:L7", "Failed Shipments", f"{failed_shipments:,}"),
        ("M5:N7", "Total Returns", f"{total_returns:,}"),

        ("A9:B11", "Total Refunds", f"₹{total_refunds:,.2f}"),
        ("C9:D11", "On-Time Delivery", f"{on_time_rate:.2f}%"),
        ("E9:G11", "Revenue / Order",
         f"₹{(float(total_revenue) / total_orders):,.2f}"
         if total_orders else "₹0.00"),
        ("H9:J11", "Logistics Cost / Order",
         f"₹{(float(total_logistics_cost) / total_orders):,.2f}"
         if total_orders else "₹0.00"),
        ("K9:L11", "Return Rate",
         f"{(total_returns / total_orders * 100):.2f}%"
         if total_orders else "0.00%"),
        ("M9:N11", "Shipment Failure Rate",
         f"{(failed_shipments / total_orders * 100):.2f}%"
         if total_orders else "0.00%")
    ]

    for cell_range, label, value in kpis:

        dashboard.merge_cells(cell_range)

        start_cell = cell_range.split(":")[0]
        cell = dashboard[start_cell]

        cell.value = f"{label}\n{value}"
        cell.fill = kpi_fill
        cell.font = kpi_label_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )
        cell.border = thin_border

    # ========================================================
    # SECTION HEADERS
    # ========================================================

    sections = [
        ("A13:G13", "SALES PERFORMANCE"),
        ("H13:N13", "DELIVERY PERFORMANCE"),
        ("A29:G29", "CUSTOMER & REVENUE"),
        ("H29:N29", "OPERATIONS"),
        ("A45:G45", "SHIPMENT ANALYSIS"),
        ("H45:N45", "WAREHOUSE ANALYSIS")
    ]

    for cell_range, title in sections:

        dashboard.merge_cells(cell_range)

        cell = dashboard[
            cell_range.split(":")[0]
        ]

        cell.value = title
        cell.fill = section_fill
        cell.font = white_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    # ========================================================
    # CHART DATA SHEET
    # ========================================================

    # Monthly
    data_ws["A1"] = "Month"
    data_ws["B1"] = "Orders"
    data_ws["C1"] = "Revenue"

    for i, row in enumerate(monthly_data, start=2):

        month_value = row[0]

        if hasattr(month_value, "strftime"):
            month_value = month_value.strftime("%b-%y")
        else:
            raw_month = str(month_value)[:7]
            try:
                from datetime import datetime
                month_value = datetime.strptime(
                    raw_month, "%Y-%m"
                ).strftime("%b-%y")
            except ValueError:
                month_value = raw_month

        data_ws.cell(i, 1, month_value)
        data_ws.cell(i, 2, int(row[1]))
        data_ws.cell(i, 3, float(row[2]) / 10_000_000)

    # Segment
    data_ws["E1"] = "Customer Segment"
    data_ws["F1"] = "Revenue"

    for i, row in enumerate(segment_data, start=2):
        data_ws.cell(i, 5, row[0])
        data_ws.cell(i, 6, float(row[1]) / 10_000_000)

    # Category
    data_ws["H1"] = "Category"
    data_ws["I1"] = "Revenue"

    for i, row in enumerate(category_data, start=2):
        data_ws.cell(i, 8, row[0])
        data_ws.cell(i, 9, float(row[1]) / 10_000_000)

    # Delivery
    data_ws["K1"] = "Delivery Performance"
    data_ws["L1"] = "Shipments"

    for i, row in enumerate(delivery_data, start=2):
        data_ws.cell(i, 11, row[0])
        data_ws.cell(i, 12, int(row[1]))

    # Top warehouses
    top_warehouses = warehouse_data[:10]

    data_ws["N1"] = "Warehouse"
    data_ws["O1"] = "Shipments"
    data_ws["P1"] = "Shipping Cost"

    for i, row in enumerate(top_warehouses, start=2):
        data_ws.cell(i, 14, row[0])
        data_ws.cell(i, 15, int(row[1]))
        data_ws.cell(i, 16, float(row[2]))

    # ========================================================
    # CHART 1 — MONTHLY REVENUE
    # ========================================================

    revenue_chart = LineChart()

    configure_chart(
        revenue_chart,
        "Monthly Revenue Trend"
    )

    revenue_chart.y_axis.title = "Revenue (₹ Crore)"
    revenue_chart.x_axis.title = "Month"
    revenue_chart.x_axis.tickLblSkip = 3
    revenue_chart.x_axis.tickMarkSkip = 3
    revenue_chart.x_axis.tickLblPos = "low"
    revenue_chart.x_axis.textRotation = 0

    revenue_values = Reference(
        data_ws,
        min_col=3,
        min_row=1,
        max_row=len(monthly_data) + 1
    )

    month_categories = Reference(
        data_ws,
        min_col=1,
        min_row=2,
        max_row=len(monthly_data) + 1
    )

    revenue_chart.add_data(
        revenue_values,
        titles_from_data=True
    )

    revenue_chart.set_categories(
        month_categories
    )

    revenue_chart.series[0].graphicalProperties.line.width = 28000
    revenue_chart.series[0].graphicalProperties.line.solidFill = MID_BLUE
    revenue_chart.series[0].graphicalProperties.noFill = False

    dashboard.add_chart(
        revenue_chart,
        "A14"
    )

    # ========================================================
    # CHART 2 — MONTHLY ORDERS
    # ========================================================

    orders_chart = LineChart()

    configure_chart(
        orders_chart,
        "Monthly Orders Trend"
    )

    orders_chart.y_axis.title = "Orders"
    orders_chart.x_axis.title = "Month"
    orders_chart.x_axis.tickLblSkip = 3
    orders_chart.x_axis.tickMarkSkip = 3
    orders_chart.x_axis.tickLblPos = "low"
    orders_chart.x_axis.textRotation = 0

    orders_values = Reference(
        data_ws,
        min_col=2,
        min_row=1,
        max_row=len(monthly_data) + 1
    )

    orders_chart.add_data(
        orders_values,
        titles_from_data=True
    )

    orders_chart.set_categories(
        month_categories
    )

    orders_chart.series[0].graphicalProperties.line.width = 28000
    orders_chart.series[0].graphicalProperties.line.solidFill = MID_BLUE
    orders_chart.series[0].graphicalProperties.noFill = False

    dashboard.add_chart(
        orders_chart,
        "H14"
    )

    # ========================================================
    # CHART 3 — CUSTOMER SEGMENT
    # Horizontal bars keep category names readable.
    # ========================================================

    segment_chart = BarChart()
    segment_chart.type = "bar"

    configure_chart(
        segment_chart,
        "Revenue by Customer Segment",
        width=13.2,
        height=7.2
    )

    segment_chart.x_axis.title = "Revenue (₹ Crore)"
    segment_chart.y_axis.title = None
    segment_chart.y_axis.tickLblPos = "nextTo"
    segment_chart.y_axis.delete = False
    segment_chart.x_axis.delete = False

    segment_values = Reference(
        data_ws,
        min_col=6,
        min_row=1,
        max_row=len(segment_data) + 1
    )

    segment_categories = Reference(
        data_ws,
        min_col=5,
        min_row=2,
        max_row=len(segment_data) + 1
    )

    segment_chart.add_data(
        segment_values,
        titles_from_data=True
    )

    segment_chart.set_categories(
        segment_categories
    )

    # Remove series legend; the category names are on the axis.
    segment_chart.legend = None

    dashboard.add_chart(
        segment_chart,
        "A30"
    )

    # ========================================================
    # CHART 4 — PRODUCT CATEGORY
    # Horizontal bars make all eight category names readable.
    # ========================================================

    category_chart = BarChart()
    category_chart.type = "bar"

    configure_chart(
        category_chart,
        "Revenue by Product Category",
        width=13.2,
        height=7.2
    )

    category_chart.x_axis.title = "Revenue (₹ Crore)"
    category_chart.y_axis.title = None
    category_chart.y_axis.tickLblPos = "nextTo"
    category_chart.y_axis.delete = False
    category_chart.x_axis.delete = False

    category_values = Reference(
        data_ws,
        min_col=9,
        min_row=1,
        max_row=len(category_data) + 1
    )

    category_categories = Reference(
        data_ws,
        min_col=8,
        min_row=2,
        max_row=len(category_data) + 1
    )

    category_chart.add_data(
        category_values,
        titles_from_data=True
    )

    category_chart.set_categories(
        category_categories
    )

    category_chart.legend = None

    dashboard.add_chart(
        category_chart,
        "H30"
    )

    # ========================================================
    # CHART 5 — DELIVERY PERFORMANCE
    # Horizontal bars make Late / Not Delivered / On Time clear.
    # ========================================================

    delivery_chart = BarChart()
    delivery_chart.type = "bar"

    configure_chart(
        delivery_chart,
        "Shipment Performance",
        width=13.2,
        height=7.2
    )

    delivery_chart.x_axis.title = "Shipments"
    delivery_chart.y_axis.title = None
    delivery_chart.y_axis.tickLblPos = "nextTo"
    delivery_chart.y_axis.delete = False
    delivery_chart.x_axis.delete = False

    delivery_values = Reference(
        data_ws,
        min_col=12,
        min_row=1,
        max_row=len(delivery_data) + 1
    )

    delivery_categories = Reference(
        data_ws,
        min_col=11,
        min_row=2,
        max_row=len(delivery_data) + 1
    )

    delivery_chart.add_data(
        delivery_values,
        titles_from_data=True
    )

    delivery_chart.set_categories(
        delivery_categories
    )

    delivery_chart.legend = None

    dashboard.add_chart(
        delivery_chart,
        "A46"
    )

    # ========================================================
    # CHART 6 — TOP 10 WAREHOUSES
    # Horizontal bars + visible Y-axis category names.
    # ========================================================

    warehouse_chart = BarChart()
    warehouse_chart.type = "bar"

    configure_chart(
        warehouse_chart,
        "Top 10 Warehouses by Shipment Volume",
        width=13.2,
        height=7.2
    )

    warehouse_chart.x_axis.title = "Shipments"
    warehouse_chart.y_axis.title = None
    warehouse_chart.y_axis.tickLblPos = "nextTo"
    warehouse_chart.y_axis.delete = False
    warehouse_chart.x_axis.delete = False

    warehouse_values = Reference(
        data_ws,
        min_col=15,
        min_row=1,
        max_row=len(top_warehouses) + 1
    )

    warehouse_categories = Reference(
        data_ws,
        min_col=14,
        min_row=2,
        max_row=len(top_warehouses) + 1
    )

    warehouse_chart.add_data(
        warehouse_values,
        titles_from_data=True
    )

    warehouse_chart.set_categories(
        warehouse_categories
    )

    warehouse_chart.legend = None

    dashboard.add_chart(
        warehouse_chart,
        "H46"
    )

    # ========================================================
    # CHART DATA FORMATTING
    # ========================================================

    for cell in data_ws[1]:
        cell.font = Font(bold=True)

    for column in ["C", "F", "I", "P"]:
        for cell in data_ws[column][1:]:
            cell.number_format = '₹0.00'

    data_ws.sheet_state = "hidden"

    # ========================================================
    # DASHBOARD FORMATTING
    # ========================================================

    for row in range(1, 65):
        dashboard.row_dimensions[row].height = 20

    dashboard.row_dimensions[1].height = 30
    dashboard.row_dimensions[2].height = 30
    dashboard.row_dimensions[3].height = 22

    for row in [13, 29, 45]:
        dashboard.row_dimensions[row].height = 23

    dashboard.freeze_panes = "A4"
    dashboard.sheet_view.zoomScale = 85

    dashboard.sheet_properties.pageSetUpPr.fitToPage = True
    dashboard.page_setup.orientation = "landscape"
    dashboard.page_setup.paperSize = dashboard.PAPERSIZE_A4
    dashboard.page_setup.fitToWidth = 1
    dashboard.page_setup.fitToHeight = 0

    dashboard.page_margins.left = 0.2
    dashboard.page_margins.right = 0.2
    dashboard.page_margins.top = 0.3
    dashboard.page_margins.bottom = 0.3

    # ========================================================
    # SAVE
    # ========================================================

    print("\nSaving dashboard...")

    wb.save(OUTPUT_FILE)

    print("\n" + "=" * 70)
    print("LOGIX EXECUTIVE DASHBOARD V4 CREATED SUCCESSFULLY")
    print("=" * 70)

    print("\nFile:")
    print(os.path.abspath(OUTPUT_FILE))

    print("\nDashboard improvements:")
    print("  [OK] Compact Mon-YY monthly labels")
    print("  [OK] No month-by-month legend")
    print("  [OK] Top 10 warehouses only")
    print("  [OK] Additional executive KPIs")
    print("  [OK] No overlapping data labels")
    print("  [OK] Readable category and warehouse axes")
    print("  [OK] Hidden chart-data sheet")
    print("  [OK] Print/page setup optimized")


if __name__ == "__main__":
    main()
