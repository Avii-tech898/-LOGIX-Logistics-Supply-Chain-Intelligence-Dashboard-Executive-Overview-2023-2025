# 🚚 LOGIX
## Logistics & Supply Chain Intelligence Platform

<p align="center">

### 📊 From Raw Logistics Data to Business Intelligence

An end-to-end analytics platform built with **Python, MySQL, SQL, Excel, Power BI and Machine Learning** to analyze logistics operations, delivery performance, inventory risk, customer behavior, costs and returns.

</p>

---

## 🏆 Project Highlights

| Metric | Value |
|---|---:|
| 📦 Orders | **100,000** |
| 👥 Customers | **20,000** |
| 🏭 Warehouses | **30** |
| 📋 Inventory Records | **150,000** |
| 🚚 Shipments | **100,000** |
| 📍 Delivery Attempts | **147,513** |
| 🔄 Returns | **15,000** |
| 🚗 Vehicles | **1,200** |
| 👨‍✈️ Drivers | **1,000** |
| 🤝 Delivery Partners | **25** |
| 🧮 SQL Analytics Queries | **100** |
| 👁️ SQL Analytical Views | **10** |
| ✅ Validation Checks | **124 PASS / 0 FAIL** |

---

# 📊 Dashboard

> **LOGIX Executive Overview — 2023–2025**

<!-- Replace this image with your Power BI dashboard screenshot -->

![LOGIX Executive Dashboard](powerbi/dashboard_preview.png)

### Executive Dashboard Covers

- Total Orders
- Total Customers
- Total Revenue
- Logistics Cost
- Failed Shipments
- Total Returns
- On-Time Delivery
- Monthly Revenue Trend
- Monthly Orders Trend
- Shipment Status
- Delivery Type Analysis
- Geographic Revenue Analysis

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Business Problem](#-business-problem)
- [Project Objectives](#-project-objectives)
- [Business Questions](#-business-questions)
- [Data Journey](#-data-journey)
- [System Architecture](#️-system-architecture)
- [Technology Stack](#️-technology-stack)
- [Dataset](#-dataset)
- [Data Model](#️-data-model)
- [Data Validation](#-data-validation)
- [SQL Analytics](#️-sql-analytics)
- [Python Analytics](#-python-analytics)
- [Excel Analytics](#-excel-analytics)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Machine Learning](#-machine-learning)
- [Key KPIs](#-key-kpis)
- [Business Insights](#-business-insights)
- [Project Structure](#-project-structure)
- [How to Run](#️-how-to-run)
- [Skills Demonstrated](#-skills-demonstrated)
- [Limitations](#️-limitations)
- [Future Scope](#-future-scope)
- [Interview Explanation](#-interview-explanation)
- [Project Status](#-project-status)
- [Author](#-author)

---

# 🚀 Project Overview

**LOGIX** is an end-to-end **Logistics & Supply Chain Intelligence Platform** created to demonstrate a complete Data Analytics workflow.

The project simulates a large logistics organization operating across India and analyzes data from:

- Customers
- Addresses
- Products
- Warehouses
- Inventory
- Orders
- Order Items
- Payments
- Shipments
- Delivery Attempts
- Drivers
- Vehicles
- Delivery Partners
- Returns

The platform transforms raw operational data into:

> **Validated Data → Relational Database → SQL Analytics → Python Analytics → Excel Reporting → Power BI Dashboard → Business Insights → ML Experimentation**

---

# 🎯 Business Problem

Logistics organizations generate large amounts of operational data across multiple business functions.

Without a unified analytics platform, management may face difficulty in understanding:

- Delivery performance
- Shipment failures
- Logistics costs
- Warehouse efficiency
- Inventory risk
- Customer behavior
- Returns and refunds
- Delivery partner performance
- Operational bottlenecks

### Core Business Question

> **How can integrated logistics data be used to improve operational efficiency, reduce delivery failures, control costs, optimize inventory and support data-driven business decisions?**

---

# 🎯 Project Objectives

The main objectives of LOGIX are:

- Generate realistic large-scale logistics data
- Maintain relational data integrity
- Validate generated data using business rules
- Build a MySQL relational database
- Create analytical SQL views
- Develop 100+ SQL analytics queries
- Perform business analysis using Python
- Build Excel analytical reports
- Create an executive Power BI dashboard
- Identify operational KPIs
- Analyze customers, sales, delivery and inventory
- Analyze returns and payments
- Experiment with Machine Learning
- Document the complete analytics lifecycle

---

# ❓ Business Questions

LOGIX is designed to answer questions such as:

### 💰 Sales

- How much revenue is generated?
- What is the average order value?
- How does revenue change over time?
- Which products generate the highest revenue?
- Which categories perform best?

### 👥 Customers

- Who are the highest-value customers?
- Which customer segments contribute the most revenue?
- How many customers are repeat customers?
- What is customer lifetime value?

### 🚚 Delivery

- What is the delivery success rate?
- What percentage of shipments fail?
- What percentage are delayed?
- Which delivery types perform best?
- Which delivery partners perform better?

### 🏭 Warehouse & Inventory

- Which warehouses handle the most shipments?
- Where is inventory risk highest?
- Which products require replenishment?
- What is the current inventory value?

### 🔄 Returns

- What is the return rate?
- What are the major return reasons?
- How much money has been refunded?
- Which products/categories have higher return exposure?

### 💳 Payments

- Which payment methods are most frequently used?
- What is the payment-status distribution?
- How much revenue is paid, pending, failed or refunded?

---

# 🔄 Data Journey

```text
                  BUSINESS PROBLEM
                         │
                         ▼
              SYNTHETIC DATA GENERATION
                         │
                         ▼
                  DATA VALIDATION
                         │
                         ▼
                    RAW CSVs
                         │
                         ▼
                  MYSQL DATABASE
                         │
                         ▼
               SQL ANALYTICS + VIEWS
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       PYTHON ANALYTICS        EXCEL ANALYSIS
              │                     │
              └──────────┬──────────┘
                         ▼
                  POWER BI
                  DASHBOARD
                         │
                         ▼
                BUSINESS INSIGHTS
                         │
                         ▼
               ML EXPERIMENTATION

System Architecture

┌──────────────────────────────────────────────────┐
│                     LOGIX                        │
├──────────────────────────────────────────────────┤
│                                                  │
│              Python Data Generator               │
│                        │                         │
│                        ▼                         │
│                   Raw CSV Data                   │
│                        │                         │
│                        ▼                         │
│                 Validation Layer                 │
│                        │                         │
│                        ▼                         │
│                 MySQL Database                  │
│                        │                         │
│              ┌─────────┴─────────┐               │
│              ▼                   ▼               │
│        SQL Analytics        Python Analytics     │
│              │                   │               │
│              └─────────┬─────────┘               │
│                        ▼                         │
│                   Power BI                       │
│                  Dashboard                       │
│                        │                         │
│                        ▼                         │
│                Business Insights                 │
│                        │                         │
│                        ▼                         │
│              Machine Learning Layer              │
│                                                  │
└──────────────────────────────────────────────────┘

🛠️ Technology Stack
Category	Technology
Programming	Python
Data Processing	Pandas, NumPy
Data Generation	Faker
Database	MySQL
Query Language	SQL
Spreadsheet Analytics	Microsoft Excel
Business Intelligence	Power BI
Visualization	Matplotlib, Seaborn
Machine Learning	Scikit-learn
Development	VS Code
Version Control	Git
Repository	GitHub
Dashboard	Power BI / Streamlit

Dataset
LOGIX uses a synthetically generated logistics dataset for portfolio and analytics purposes.
Dataset Configuration
Country       : India
Period        : 2023–2025
Random Seed   : 42
Currency      : INR
Database      : MySQL

The dataset was designed with realistic relationships, operational statuses, business rules and cross-table dependencies.

📈 Dataset Scale
Dataset	Rows
Customers	20,000
Addresses	30,000
Products	5,000
Warehouses	30
Inventory	150,000
Orders	100,000
Order Items	299,720
Payments	100,000
Shipments	100,000
Delivery Attempts	147,513
Drivers	1,000
Vehicles	1,200
Delivery Partners	25
Returns	15,000


Dataset Scale
1M+ operational records

Data Model

Customers
    │
    ├──────── Addresses
    │
    └──────── Orders
                 │
                 ├──── Order Items ───── Products
                 │
                 ├──── Payments
                 │
                 ├──── Shipments
                 │          │
                 │          └──── Delivery Attempts
                 │
                 └──── Returns


Warehouses ───── Inventory ───── Products

Drivers ───── Vehicles

Delivery Partners ───── Shipments

Database Tables
The MySQL database contains 14 operational tables:

1.  customers
2.  addresses
3.  products
4.  warehouses
5.  drivers
6.  delivery_partners
7.  vehicles
8.  inventory
9.  orders
10. order_items
11. payments
12. shipments
13. delivery_attempts
14. returns

Data Validation
Data validation was treated as a core component of the project.
Final Validation Result

╔══════════════════════════════╗
║       FINAL RAW AUDIT        ║
╠══════════════════════════════╣
║ PASS : 124                   ║
║ FAIL : 0                     ║
╚══════════════════════════════╝

Validation Categories
- Primary Key validation
- Foreign Key validation
- Duplicate detection
- Missing-value validation
- Date validation
- Status validation
- Quantity validation
- Price validation
- Revenue reconciliation
- Payment reconciliation
- Shipment validation
- Return validation
- Cross-table validation

Major Integrity Checks

✓ 100,000 unique orders
✓ 100,000 unique shipments
✓ 100,000 payments
✓ Payment value reconciles with order-item revenue
✓ Valid shipment → order relationships
✓ Valid delivery attempt → shipment relationships
✓ Valid return → order item relationships
✓ Valid inventory → product/warehouse relationships

SQL Analytics
SQL is one of the major analytical layers of LOGIX.
SQL Structure

sql/
│
├── 01_database_setup/
├── 02_schema/
├── 03_views/
├── 04_analytics_queries/
└── 05_advanced_analytics/

Analytical Views

vw_customer_analysis
vw_delivery_performance
vw_executive_kpi
vw_fleet_analysis
vw_inventory_analysis
vw_monthly_sales
vw_payment_analysis
vw_returns_analysis
vw_sales_analysis
vw_warehouse_performance


SQL Concepts Demonstrated
SELECT
WHERE
GROUP BY
HAVING
JOIN
CASE
Subqueries
CTEs
Window Functions
ROW_NUMBER
RANK
LAG
Running Totals
Revenue Contribution
Customer Analytics
KPI Analytics

SQL Portfolio
100 analytical SQL queries
plus an advanced business-analysis layer.
🐍 Python Analytics
Python is used for:
- Data generation
- Data validation
- Data processing
- KPI calculation
- Business analysis
- MySQL connectivity
- Excel export
- ML preprocessing
- Model training
- Model evaluation
Python Analytics Modules
python/
│
├── analytics/
│   ├── executive_analysis.py
│   ├── sales_analysis.py
│   ├── customer_analysis.py
│   ├── delivery_analysis.py
│   ├── warehouse_inventory_analysis.py
│   └── fleet_analysis.py
│
├── generators/
├── validation/
├── config.py
├── utils.py
├── sql_connection.py
├── export_mysql_schema.py
├── export_mysql_views.py
└── export_to_excel.py

📊 Excel Analytics
Excel is used as a business-friendly reporting layer.
Workbooks
LOGIX_Excel_Analysis.xlsx
LOGIX_Excel_Analysis_Professional.xlsx
LOGIX_Executive_Dashboard_v7.xlsx

Analytical Sheets
Executive_KPI
Sales_Analysis
Customer_Analysis
Delivery_Analysis
Warehouse_Analysis
Inventory_Analysis
Returns_Analysis
Payment_Analysis
Monthly_Sales
Fleet_Analysis

Excel demonstrates:
- KPI reporting
- Business analysis
- Trend analysis
- Operational reporting
- Management reporting
- Spreadsheet-based decision support
📈 Power BI Dashboard
Executive Overview
The Power BI dashboard is designed for management-level decision making.
KPI Cards
100K Orders
20K Customers
₹22.08B Revenue
₹1.42B Logistics Cost
4,432 Failed Shipments
15K Returns
30.05% On-Time Delivery

Current Visuals
- Monthly Revenue Trend
- Monthly Orders Trend
- Shipment Status Distribution
- Shipments by Delivery Type
- On-Time Delivery
- Failed Shipments
- Total Returns
- Revenue by State / Geographic Analysis
Dashboard Goal
Provide a single executive view of revenue, logistics cost, delivery performance, shipment failures, returns and operational trends.

💰 Key KPIs
KPI	Value
Total Orders	100,000
Total Customers	20,000
Total Revenue	₹22.08B
Logistics Cost	₹1.42B
Failed Shipments	4,432
Total Returns	15,000
Total Refunds	₹840.53M
On-Time Delivery	30.05%
Revenue / Order	₹220,795.72
Logistics Cost / Order	₹14,245.96
Return Rate	15.00%
Shipment Failure Rate	4.43%


🚚 Delivery Performance
Total Shipments       : 100,000
Delivered             : 59,818
Failed                : 4,432
Delayed               : 6,882
Delivery Success      : 59.82%
Failure Rate          : 4.43%
Delay Rate            : 6.88%
Total Distance        : 75,296,143.11 km
Shipping Cost         : ₹1,424,595,971.71
Average Distance      : 753.31 km
Shipping Cost / KM    : ₹18.92

Delivery Attempts
Outcome	Count
Delivered	66,700
Failed	20,321
Customer Unavailable	20,291
Wrong Address	20,141
Rescheduled	20,060


📦 Inventory Analytics
Inventory Records       : 150,000
Current Stock           : 29,258,214
Inventory Value         : ₹1,021,576,222,353.55
Low Stock Records       : 28,271
Out of Stock            : 739
Stock Risk Records      : 29,010
Stock Risk Rate         : 19.34%

Inventory analysis supports:
- Stock-risk monitoring
- Reorder analysis
- Warehouse comparison
- Stockout detection
- Inventory-value analysis
👥 Customer Analytics
Customer analytics includes:
- Customer revenue
- Order frequency
- Repeat customer analysis
- Customer segmentation
- Average Order Value
- Customer Lifetime Value
- Revenue contribution
Customer Base: 20,000

🔄 Returns & Payments
Returns
Total Returns : 15,000
Refunds       : ₹840,527,131.70
Return Rate   : 15.00%

Major Return Reasons
- Late Delivery
- Changed Mind
- Damaged Product
- Wrong Product
- Size Issue
- Quality Issue
- Other
- Product Defective
Payment Methods
UPI
Credit Card
Debit Card
Cash on Delivery
Net Banking
Wallet

Payment Status
Paid
Pending
Failed
Refunded

🚛 Fleet Analytics
Vehicles          : 1,200
Drivers           : 1,000
Delivery Partners : 25

Fleet analysis includes:
Vehicles
- Vehicle type
- Capacity
- Fuel type
- Model year
- Driver assignment
- Status
Drivers
- Experience
- Rating
- Employment type
- Status
Important Schema Limitation
The current shipments table does not contain vehicle_id.
Therefore, LOGIX does not create unsupported vehicle-level shipment performance.
Vehicle and driver analytics are maintained separately unless a future version introduces an explicit vehicle-to-shipment relationship.
🤖 Machine Learning
LOGIX includes an experimental Delivery Delay Prediction pipeline.
Objective
Predict whether a shipment will experience a delivery delay.
Models
Logistic Regression
Decision Tree
Random Forest

Evaluation Strategies
Random Split Baseline
Feature-Engineered Evaluation
Time-Based Evaluation

Final Time-Based Results
Model	Accuracy	Precision	Recall	F1	ROC-AUC
Decision Tree	69.58%	70.03%	98.84%	81.98%	0.5051
Random Forest	70.00%	70.00%	100%	82.35%	0.4962
Logistic Regression	70.00%	70.00%	100%	82.35%	0.4947


ML Finding
The current synthetic dataset contains weak predictive signal for delivery delay.
ROC-AUC values around 0.50 indicate that the current features do not provide meaningful predictive discrimination.
This is intentionally documented as an ML experiment rather than falsely presenting it as a production-ready predictive model.
Future ML Features
A stronger model could incorporate:
- Historical route delay
- Traffic
- Weather
- Holiday calendars
- Driver workload
- Warehouse processing time
- Delivery-partner reliability
- Regional congestion
- Customer availability
- Route-level historical performance
📁 Project Structure
LOGIX/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── python/
│   ├── analytics/
│   ├── generators/
│   ├── validation/
│   ├── config.py
│   ├── utils.py
│   ├── sql_connection.py
│   ├── export_mysql_schema.py
│   ├── export_mysql_views.py
│   └── export_to_excel.py
│
├── sql/
│   ├── 01_database_setup/
│   ├── 02_schema/
│   ├── 03_views/
│   ├── 04_analytics_queries/
│   └── 05_advanced_analytics/
│
├── dashboard/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── powerbi/
│
├── ml/
│   ├── config/
│   ├── preprocessing/
│   ├── models/
│   ├── evaluation/
│   ├── notebooks/
│   └── outputs/
│
├── documentation/
│
├── .gitignore
└── README.md

▶️ How to Run
1. Clone Repository
git clone https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025.git
cd -LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025

2. Create Virtual Environment
python -m venv .venv

Windows PowerShell
.\.venv\Scripts\Activate.ps1

3. Install Dependencies
pip install pandas numpy scikit-learn matplotlib seaborn faker mysql-connector-python

🗄️ MySQL Setup
Create the database:
CREATE DATABASE logix
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

Then:
1. Create schema
2. Load CSV datasets
3. Create analytical views
4. Run SQL analytics

🐍 Run Python Analytics
From the project root:
python python\analytics\executive_analysis.py
python python\analytics\sales_analysis.py
python python\analytics\customer_analysis.py
python python\analytics\delivery_analysis.py
python python\analytics\warehouse_inventory_analysis.py
python python\analytics\fleet_analysis.py

📊 Power BI Connection
Power BI
    ↓
MySQL
    ↓
logix
    ↓
Analytical Views
    ↓
Executive Dashboard

Primary reporting views:
vw_executive_kpi
vw_monthly_sales
vw_delivery_performance
vw_sales_analysis
vw_customer_analysis
vw_inventory_analysis
vw_warehouse_performance
vw_payment_analysis
vw_returns_analysis
vw_fleet_analysis

🤖 ML Pipeline
Raw Orders + Shipments
          ↓
Temporal Feature Engineering
          ↓
Time-Based Train/Test Split
          ↓
Train-Only Historical Features
          ↓
Preprocessing
          ↓
Model Training
          ↓
Evaluation
          ↓
Model Comparison

ML outputs:
ml/outputs/

🔁 Reproducibility
The project follows reproducible analytics principles:
- Fixed random seed
- Configuration-driven data generation
- Controlled synthetic data
- Validation before database loading
- Relational integrity
- Reusable SQL views
- Modular Python scripts
- Separate ML preprocessing
- Time-aware ML evaluation
- Git version control
💡 Business Insights
1. Delivery Performance
Delivery performance is a major operational area for improvement based on the generated shipment metrics.
2. Failed Shipments
A 4.43% shipment failure rate creates a measurable operational risk.
Further analysis can identify whether failures are concentrated by:
- Delivery type
- Delivery partner
- Region
- Failure reason
3. Inventory Risk
A 19.34% stock-risk rate indicates a significant opportunity for inventory optimization.
4. Returns
A 15% return rate creates opportunities to investigate:
- Product quality
- Wrong-product issues
- Delivery experience
- Customer behavior
5. Logistics Cost
With approximately ₹1.42B logistics cost, cost-to-serve analysis is an important management opportunity.
6. Machine Learning
The weak predictive signal demonstrates the importance of feature quality in machine learning.
⚠️ Limitations
Synthetic Data
LOGIX uses synthetic data.
Therefore, KPI values represent a portfolio simulation and should not be interpreted as actual company performance.
ML Limitation
Current features do not provide strong predictive signal for delivery-delay prediction.
Vehicle Mapping
The shipment table currently does not contain vehicle_id.
Therefore, unsupported vehicle-level shipment attribution is intentionally avoided.
KPI Definition
Operational KPIs such as on-time delivery depend on denominator definitions.
Future versions should explicitly distinguish:
All Shipments
Delivered Shipments
SLA-Eligible Shipments

🔮 Future Scope
Analytics
- Advanced customer segmentation
- Route profitability
- Cost-to-serve analysis
- Supplier analytics
- Demand forecasting
- Warehouse optimization
Power BI
- Drill-through pages
- Dynamic KPI selectors
- Bookmarks
- Advanced tooltips
- Regional maps
- Partner scorecards
- Inventory risk dashboard
- Customer 360 dashboard
Machine Learning
- Demand forecasting
- ETA prediction
- Improved delay prediction
- Return prediction
- Customer churn prediction
- Inventory forecasting
Data Engineering
- Automated ETL
- Incremental loading
- Data warehouse
- Airflow orchestration
- Cloud deployment
💼 Interview Explanation
30-Second Version
LOGIX is an end-to-end logistics analytics platform I developed using Python, MySQL, Excel and Power BI. I generated and validated a large synthetic logistics dataset containing customers, orders, inventory, warehouses, shipments, delivery attempts, payments, returns and fleet data. I loaded the data into MySQL, created analytical views and SQL queries, performed business analysis using Python and Excel, and built an executive Power BI dashboard for revenue, logistics cost, delivery performance, failures and returns. I also developed a time-based machine-learning experiment for delivery-delay prediction.

Business Value
The project converts operational logistics data into management-ready insights for monitoring delivery performance, controlling logistics costs, identifying inventory risks, understanding customer behavior and supporting data-driven decisions.

ML Result
The synthetic dataset had weak predictive signal. Instead of hiding the result, I evaluated it honestly and documented what additional real-world features would be required for a stronger production model.

🏆 Project Highlights
100K Orders
20K Customers
150K Inventory Records
100K Shipments
147K Delivery Attempts
15K Returns
1,200 Vehicles
1,000 Drivers
25 Delivery Partners
1M+ Records
124 Validation Checks Passed
100 SQL Analytics Queries
10 Analytical SQL Views

📌 Project Status
Component	Status
Synthetic Data Generation	✅ Complete
Data Validation	✅ Complete
MySQL Database	✅ Complete
SQL Schema	✅ Complete
SQL Views	✅ Complete
SQL Analytics	✅ Complete
Python Analytics	✅ Complete
Excel Analytics	✅ Complete
Power BI Executive Dashboard	🚧 In Progress
Streamlit Dashboard	✅ Complete
ML Delivery Delay Pipeline	✅ Complete
ML Evaluation	✅ Complete
Documentation	✅ Complete
GitHub Repository	🚀 Active


👨‍💻 Author
Avanish Tripathi
BCA — Data Science & Artificial Intelligence
Interests
Data Analytics
Data Science
Machine Learning
Business Intelligence
Python
SQL
Power BI

🔗 Repository
LOGIX — Logistics & Supply Chain Intelligence Platform
https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025
⭐ Support
If you find this project useful, consider giving the repository a ⭐.
<p align="center">

🚚 LOGIX
Turning Logistics Data into Business Intelligence.
</p>
```

