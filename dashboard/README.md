# LOGIX Python Interactive Dashboard

Power BI-style interactive logistics dashboard using Python, Streamlit, Plotly, Pandas and the existing MySQL `logix` database.

## Run on Windows
1. Copy `.env.example` to `.env`.
2. Put your existing MySQL password in `.env` (do not put it in `app.py`).
3. In PowerShell, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The browser will open the dashboard.

## Pages
- Executive Overview
- Delivery & Logistics
- Warehouse & Inventory
- Customer & Sales
- Returns & Payments
- Fleet Performance

## Executive Overview
Includes 12 live KPIs, date/warehouse/partner/status filters, monthly revenue & orders, shipment performance, product category revenue, top warehouses, customer segments and delivery partners.
