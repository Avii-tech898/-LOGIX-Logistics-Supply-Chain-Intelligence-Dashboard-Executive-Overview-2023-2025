# Power BI

## Current Status
**HOLD / LOCKED**

The Power BI report is connected to the LOGIX MySQL database and analytical views have been loaded.

## Loaded Views
- vw_customer_analysis
- vw_delivery_performance
- vw_executive_kpi
- vw_fleet_analysis
- vw_inventory_analysis
- vw_monthly_sales
- vw_payment_analysis
- vw_returns_analysis
- vw_sales_analysis
- vw_warehouse_performance

## Current Executive Overview
The current report page contains the first KPI row: Total Orders, Total Customers, Total Revenue, Logistics Cost, Failed Shipments, and Total Returns.

The report will be resumed after Documentation and ML work is completed.

## KPI Principle
Executive KPI values should use the dedicated executive KPI view or correctly isolated aggregations rather than multi-table joins that can multiply records.
