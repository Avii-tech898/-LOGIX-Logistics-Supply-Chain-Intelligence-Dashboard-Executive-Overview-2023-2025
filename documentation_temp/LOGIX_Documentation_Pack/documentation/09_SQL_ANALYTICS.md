# SQL Analytics

## SQL Layers
```text
sql/
├── 01_database_setup/
├── 02_schema/
├── 03_views/
├── 04_analytics_queries/
└── 05_advanced_analytics/
```

## Analytical Views
10 reusable views cover customer, delivery, executive KPI, fleet, inventory, monthly sales, payment, returns, sales, and warehouse analysis.

## Query Library
The project contains 10 SQL analytics modules covering 100 documented query slots across basic analytics, customer analytics, sales analytics, delivery analytics, warehouse/inventory, payments/returns, fleet analytics, advanced SQL, business KPIs, and management insights.

## Important Query Note
The documented Q81 executive KPI query has an aggregation-multiplication risk when joining multiple one-to-many tables. Executive KPI reporting should use the dedicated `vw_executive_kpi` view instead.
