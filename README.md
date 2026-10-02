🚚 LOGIX
Logistics & Supply Chain Intelligence Platform

From synthetic logistics data to business intelligence, operational analytics & predictive modeling

Python → Pandas → Data Validation → MySQL → SQL Analytics → Excel → Power BI → Streamlit → Machine Learning


















End-to-end Logistics Analytics • Supply Chain Intelligence • SQL • BI • Machine Learning • Executive Dashboard

📊 Dashboard Preview

LOGIX Executive Dashboard — Logistics & Supply Chain Performance Overview

<!-- Add your final dashboard screenshot here --> <!-- ![LOGIX Executive Dashboard](powerbi/LOGIX_DASHBOARD.png) -->
⚡ At a Glance
📦 Data Scale	📊 Analytics	🧩 Platform
100K Orders	Sales & Revenue Analytics	MySQL
100K Shipments	Delivery Performance	SQL
20K Customers	Warehouse & Inventory	Python
150K Inventory Records	Customer & Returns	Excel
299,720 Order Items	Fleet & Logistics	Power BI
14 Core Tables	Predictive ML	Streamlit
100 SQL Queries	Executive KPIs	Git + GitHub
🧭 Table of Contents
📌 Project Overview
🎯 Project Objectives
💼 Business Problem
🏗️ Project Architecture
🔄 Complete Data Journey
🛠️ Technology Stack
📊 Dataset
🗂️ Dataset Details
🔍 Data Validation
🗄️ MySQL Database
🧮 SQL Analytics
🐍 Python Analytics
📗 Excel Analytics
📊 Power BI Dashboard
🖥️ Streamlit Dashboard
🤖 Machine Learning
📈 Core Business KPIs
❓ Business Questions Answered
📁 Project Structure
🎓 Skills Demonstrated
⚙️ How to Run
🔁 Reproducible Pipeline
⚠️ Project Limitations
🚀 Future Enhancements
🗣️ Interview Explanation
🧩 Architecture Explanation for HR
🏆 Project Highlights
🎯 Project Outcome
👨‍💻 Author
📌 Project Overview

LOGIX is an end-to-end Logistics & Supply Chain Intelligence Platform designed to simulate a realistic logistics ecosystem and transform raw operational data into business-ready insights.

The platform covers the complete analytics journey:

Business Problem → Data Generation → Data Validation → MySQL → SQL Analytics → Python Analytics → Excel → Power BI → Streamlit → Machine Learning → Business Insights

LOGIX models interconnected logistics operations involving:

Customers
Addresses
Products
Warehouses
Inventory
Orders
Order Items
Payments
Shipments
Delivery Attempts
Drivers
Vehicles
Delivery Partners
Returns

The project is designed around an Indian logistics environment with data spanning 2023–2025.

🎯 Project Objectives
#	Objective
01	Generate a realistic logistics and supply-chain ecosystem
02	Build interconnected operational datasets
03	Validate data quality and relational integrity
04	Store structured data in MySQL
05	Develop analytical SQL queries and views
06	Perform business analytics using Python
07	Build Excel-based operational analysis
08	Develop an executive Power BI dashboard
09	Create an interactive Streamlit analytics platform
10	Implement machine-learning experiments
11	Measure logistics and operational KPIs
12	Convert raw operational data into business insights
💼 Business Problem

Logistics companies generate large amounts of operational data across orders, customers, warehouses, inventory, shipments, delivery partners, payments and returns.

Without a unified analytics system, it becomes difficult to:

Monitor delivery performance
Identify shipment delays
Track logistics costs
Monitor warehouse operations
Identify inventory risk
Understand customer behavior
Analyze returns and refunds
Compare delivery partners
Monitor fleet-related information
Support operational decision-making
LOGIX addresses this by creating a unified analytical ecosystem:
Raw Operational Data
        ↓
Data Validation
        ↓
Relational Database
        ↓
SQL Analytics
        ↓
Business KPIs
        ↓
Dashboards
        ↓
Predictive Analytics
🏗️ Project Architecture
┌─────────────────────────────────────────────┐
│              BUSINESS PROBLEM               │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│          PYTHON DATA GENERATION             │
│          Pandas • NumPy • Faker             │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│             DATA VALIDATION                 │
│       PK • FK • Dates • Status • QA         │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                RAW DATA                     │
│              14 DATASETS                    │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│                MySQL                        │
│          Relational Database                │
└───────────────┬──────────────┬──────────────┘
                ↓              ↓
        ┌──────────────┐ ┌──────────────┐
        │ SQL Analytics│ │Python Analytics│
        └──────┬───────┘ └──────┬───────┘
               └─────────┬──────┘
                         ↓
              ┌─────────────────────┐
              │   Excel Analytics   │
              └──────────┬──────────┘
                         ↓
               ┌──────────────────┐
               │ Visualization    │
               │ Power BI         │
               │ Streamlit        │
               └────────┬─────────┘
                        ↓
               ┌──────────────────┐
               │ Machine Learning │
               └────────┬─────────┘
                        ↓
               ┌──────────────────┐
               │ Business Insights│
               └──────────────────┘
One-Line Architecture
Python → Validation → MySQL → SQL → Python Analytics → Excel → Power BI → Streamlit → ML → Business Insights
🔄 Complete Data Journey
01. Define Logistics Business Requirements
                ↓
02. Generate Synthetic Logistics Data
                ↓
03. Validate Data Quality
                ↓
04. Store Raw CSV Datasets
                ↓
05. Load Data into MySQL
                ↓
06. Build Relational Database Schema
                ↓
07. Create Analytical SQL Views
                ↓
08. Execute Business Analytics Queries
                ↓
09. Perform Python Analytics
                ↓
10. Build Excel Analysis
                ↓
11. Develop Power BI Dashboard
                ↓
12. Develop Streamlit Dashboard
                ↓
13. Build Machine Learning Pipeline
                ↓
14. Evaluate Models
                ↓
15. Extract Business Insights
🛠️ Technology Stack
Technology	Role in LOGIX
🐍 Python	Data generation, validation & analytics
🐼 Pandas	Data processing & analysis
🔢 NumPy	Numerical operations
🗄️ MySQL	Relational data storage
🧮 SQL	Business & operational analytics
📗 Excel	Business analysis & reporting
📊 Power BI	Executive BI dashboard
🖥️ Streamlit	Interactive analytics application
🤖 Scikit-learn	Machine Learning
🌿 Git	Version control
🐙 GitHub	Portfolio & project hosting
📊 Dataset

LOGIX contains 14 interconnected operational datasets.

Dataset Period
2023-01-01 → 2025-12-31
Geography
India
Data Scale
Dataset	Records	Purpose
customers.csv	20,000	Customer master data
addresses.csv	30,000	Customer addresses
products.csv	5,000	Product catalog
warehouses.csv	30	Warehouse master
inventory.csv	150,000	Warehouse-product inventory
orders.csv	100,000	Order transactions
order_items.csv	299,720	Product-level transactions
payments.csv	100,000	Payment transactions
shipments.csv	100,000	Shipment operations
delivery_attempts.csv	147,513	Delivery attempt history
drivers.csv	1,000	Driver master
vehicles.csv	1,200	Fleet master
delivery_partners.csv	25	Delivery partner master
returns.csv	15,000	Returns & refunds
🗂️ Dataset Details
👥 Customers

Includes:

Customer ID
Customer Name
Email
Phone
Gender
Customer Segment
Registration Date
State
City
Pincode
Preferred Payment Method
Active Status
🏠 Addresses

Includes:

Address ID
Customer ID
Address Type
Address
City
State
Pincode
Default Address Flag
📦 Products

Includes:

Product ID
Product Name
Category
Brand
Unit Price
Weight
Supplier
Reorder Level
Active Status
🏭 Warehouses

Includes:

Warehouse ID
Warehouse Name
Warehouse Type
City
State
Pincode
Capacity
Manager
Operating Hours
Active Status
📦 Inventory

Tracks:

Warehouse
Product
Opening Stock
Current Stock
Reorder Level
Unit Cost
Inventory Value
Stock Status
Last Restock Date
🛒 Orders

Tracks:

Order
Customer
Address
Order Date
Expected Delivery Date
Delivery Type
Priority
Order Status
🧾 Order Items

Tracks:

Order Item
Order
Product
Quantity
Unit Price
Discount
Discount Amount
Line Total
💳 Payments

Tracks:

Payment
Order
Payment Date
Payment Method
Payment Status
Amount
Transaction Reference
🚚 Shipments

Tracks:

Shipment
Order
Warehouse
Delivery Partner
Shipment Date
Expected Delivery Date
Actual Delivery Date
Delivery Type
Shipment Status
SLA
Shipping Cost
Distance
🔄 Returns

Tracks:

Return
Order
Order Item
Product
Return Date
Return Quantity
Return Reason
Return Status
Return Amount
Refund Amount
🔍 Data Validation

Before analytics, LOGIX performs comprehensive validation using Python and Pandas.

Validation Areas
✅ Primary-key uniqueness
✅ Foreign-key integrity
✅ Missing values
✅ Date consistency
✅ Status consistency
✅ Quantity validation
✅ Price validation
✅ Customer-address relationships
✅ Order-item relationships
✅ Shipment relationships
✅ Payment relationships
✅ Return relationships
✅ Cross-table consistency
Final Raw Data Audit
PASS : 124
FAIL : 0

ALL FINAL CROSS-TABLE AUDITS PASSED
🗄️ MySQL Database

LOGIX uses MySQL as the central relational database.

14 Core Tables
customers
addresses
products
warehouses
drivers
delivery_partners
vehicles
inventory
orders
order_items
payments
shipments
delivery_attempts
returns
Database Flow
Master Data
     ↓
Transactions
     ↓
Operational Tables
     ↓
MySQL Relationships
     ↓
Analytical Views
     ↓
BI / Analytics
🧮 SQL Analytics

LOGIX contains 100 analytical SQL queries organized into 10 analytical levels.

01 Basic Analytics
02 Customer Analytics
03 Sales Analytics
04 Delivery Analytics
05 Warehouse & Inventory
06 Payment & Returns
07 Fleet Analytics
08 Advanced SQL
09 Business KPIs
10 Management Insights
SQL Concepts
SELECT
WHERE
GROUP BY
HAVING
INNER JOIN
LEFT JOIN
Subqueries
CTEs
Window Functions
Aggregations
Ranking
Running Totals
Business KPI calculations
Operational analytics
Analytical Views

LOGIX contains 10 analytical MySQL views:

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
🐍 Python Analytics

Dedicated Python modules analyze:

Executive Performance
Sales Performance
Customer Analytics
Delivery Performance
Warehouse & Inventory
Fleet Analytics

The Python layer is connected directly to the MySQL analytical environment.

📗 Excel Analytics

The Excel layer provides business-friendly reporting for:

Executive KPIs
Sales Analysis
Customer Analysis
Delivery Analysis
Warehouse Analysis
Inventory Analysis
Returns Analysis
Payment Analysis
Monthly Sales
Fleet Analysis
Excel Dashboard KPIs
Total Orders
Total Customers
Total Revenue
Logistics Cost
Failed Shipments
Total Returns
Total Refunds
On-Time Delivery
Revenue per Order
Logistics Cost per Order
📊 Power BI Dashboard

The LOGIX Executive Dashboard provides a business-level view of logistics and supply-chain performance.

KPI Cards
💰 Total Revenue
🛒 Total Orders
👥 Total Customers
🚚 Logistics Cost
❌ Failed Shipments
↩️ Total Returns
💸 Total Refunds
⏱️ On-Time Delivery
Dashboard Areas
Visualization	Purpose
📈 Monthly Revenue	Revenue trend
📊 Monthly Orders	Order trend
👥 Customer Segment	Customer composition
📦 Product Category	Category performance
🚚 Shipment Performance	Delivery monitoring
🏭 Warehouse Performance	Warehouse comparison

Power BI is connected to the LOGIX MySQL analytical views.

🖥️ Streamlit Dashboard

LOGIX includes an interactive Streamlit analytics application.

Dashboard Sections
Executive Overview
        ↓
Delivery & Logistics
        ↓
Warehouse & Inventory
        ↓
Customer & Sales
        ↓
Returns & Payments
        ↓
Fleet Performance
Interactive Filters
Date Range
Warehouse
Delivery Partner
Order Status

The application retrieves analytical data from the LOGIX MySQL database.

🤖 Machine Learning

LOGIX includes a dedicated Machine Learning layer for predictive logistics analytics.

Experiment 01 — Delivery Delay Prediction
Objective

Predict whether a shipment will be delivered after its expected delivery date.

Shipment Data
      ↓
Feature Engineering
      ↓
Historical Operational Features
      ↓
Time-Based Train/Test Split
      ↓
Machine Learning
      ↓
Delay Prediction
Models
Logistic Regression
Decision Tree
Random Forest
Feature Categories

Operational

Distance
Shipping Cost
SLA Days
Processing Days

Delivery

Delivery Type
Priority
Warehouse
Delivery Partner

Historical

Warehouse Prior Delay Rate
Partner Prior Delay Rate
Historical Shipment Counts
Historical Operational Risk

Temporal

Month
Day of Week
Shipment Week
Weekend Indicators
Time-Based Validation

Instead of randomly mixing historical and future records, LOGIX uses chronological evaluation:

Historical Data
       ↓
TRAIN
       ↓
2025-05-27
       ↓
2025-05-28
       ↓
TEST
       ↓
Future Data

Historical warehouse and partner performance is constructed using information available before the prediction period.

Important ML Finding

The current synthetic dataset shows relatively weak predictive signal for delivery-delay classification.

Therefore, the ML experiment is treated as an analytical experiment and methodology demonstration, not as a production-ready prediction system.

📈 Core Business KPIs
Executive KPIs
KPI	Current Value
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

Metrics are calculated from the current synthetic LOGIX dataset.

❓ Business Questions Answered
💰 Sales & Revenue
What is total revenue?
How does revenue change over time?
What is revenue per order?
Which product categories contribute to revenue?
How does order volume change monthly?
🚚 Delivery
How many shipments are delivered?
What is the delivery success rate?
What is the shipment failure rate?
What is the delay rate?
How does delivery type affect performance?
How much does logistics cost?
🏭 Warehouse
Which warehouses handle the highest shipment volume?
What is the warehouse shipping cost?
Which warehouses have inventory risk?
How much inventory value is being held?
📦 Inventory
How much inventory exists?
How many items are low stock?
How many items are out of stock?
What is the inventory risk rate?
Which categories have inventory exposure?
👥 Customers
How many customers are represented?
Which customer segments exist?
What is average order value?
How many orders are generated by customers?
↩️ Returns
How many returns occur?
What are the major return reasons?
What is the refund amount?
What is the return rate?
💳 Payments
Which payment methods are used?
What is the payment value?
How many transactions fail?
How much is refunded?
📁 Project Structure
LOGIX/
│
├── 📂 data/
│   ├── raw/
│   └── cleaned/
│
├── 📂 python/
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
├── 📂 sql/
│   ├── 01_database_setup/
│   ├── 02_schema/
│   ├── 03_views/
│   ├── 04_analytics_queries/
│   └── 05_advanced_analytics/
│
├── 📂 dashboard/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   └── .env.example
│
├── 📂 powerbi/
│
├── 📂 excel/
│
├── 📂 ml/
│   ├── config/
│   ├── preprocessing/
│   ├── models/
│   ├── evaluation/
│   ├── notebooks/
│   └── outputs/
│
├── 📂 documentation/
│
├── .gitignore
├── README.md
└── requirements.txt
📊 Key Project Metrics
Metric	Value
👥 Customers	20,000
🏠 Addresses	30,000
📦 Products	5,000
🏭 Warehouses	30
📦 Inventory Records	150,000
🛒 Orders	100,000
🧾 Order Items	299,720
💳 Payments	100,000
🚚 Shipments	100,000
📍 Delivery Attempts	147,513
👨‍✈️ Drivers	1,000
🚗 Vehicles	1,200
🤝 Delivery Partners	25
↩️ Returns	15,000
🎓 Skills Demonstrated
📊 Data & Analytics	📈 BI & Modeling	💻 Development
Data Generation	Power BI	Python
Data Cleaning	Data Modeling	Pandas
Data Validation	Analytical Views	NumPy
KPI Development	DAX / BI Analytics	MySQL
Sales Analytics	Dashboard Development	Streamlit
Logistics Analytics	Executive Reporting	Git
Inventory Analytics	Time-Based ML	GitHub
Customer Analytics	Predictive Analytics	Documentation
⚙️ How to Run the Project
1️⃣ Clone Repository
git clone https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025.git
2️⃣ Navigate
cd -LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025
3️⃣ Create Virtual Environment
python -m venv .venv
Windows
.venv\Scripts\activate
4️⃣ Install Dependencies
pip install -r requirements.txt
5️⃣ Configure MySQL

Create:

CREATE DATABASE logix;

Configure environment variables:

LOGIX_DB_HOST=localhost
LOGIX_DB_PORT=3306
LOGIX_DB_USER=root
LOGIX_DB_PASSWORD=YOUR_PASSWORD
LOGIX_DB_NAME=logix

Never commit .env or database credentials.

6️⃣ Run Streamlit
cd dashboard
streamlit run app.py
🔁 Reproducible Pipeline
Python Generators
       │
       ├── Customers
       ├── Addresses
       ├── Products
       ├── Warehouses
       ├── Inventory
       ├── Orders
       ├── Order Items
       ├── Payments
       ├── Shipments
       ├── Delivery Attempts
       ├── Drivers
       ├── Vehicles
       ├── Delivery Partners
       └── Returns
              │
              ▼
       Data Validation
              │
              ▼
          CSV Layer
              │
              ▼
        MySQL Database
              │
       ┌──────┼──────┐
       ↓      ↓      ↓
      SQL   Python  Excel
       │      │      │
       └──────┼──────┘
              ↓
        Power BI
              +
        Streamlit
              ↓
      Machine Learning
              ↓
      Business Insights
⚠️ Project Limitations

LOGIX is a synthetic-data portfolio project designed to demonstrate an end-to-end analytics architecture.

Important limitations:

Data is synthetic rather than production company data.
ML performance depends on relationships generated in the synthetic dataset.
The current shipment schema does not directly contain vehicle_id.
Therefore, unsupported vehicle-level shipment attribution is intentionally avoided.
Some KPI definitions may require additional business-specific definitions before production deployment.
Power BI depends on the configured local MySQL environment.
🚀 Future Enhancements

Potential future development includes:

🔮 Demand Forecasting
📦 Inventory Stockout Prediction
🚚 Delivery Failure Prediction
👥 Customer Churn Prediction
🎯 Customer Segmentation
🗺️ Route Optimization
📍 Geospatial Logistics Analytics
🚨 Operational Anomaly Detection
💰 Logistics Cost Optimization
☁️ Cloud Database Deployment
🔄 Automated ETL Pipelines
⚡ Real-Time Shipment Tracking
🤖 MLOps
📊 Automated Reporting
🌐 Power BI Service Deployment
🗣️ Interview Explanation
"Tell me about your LOGIX project."

LOGIX is an end-to-end Logistics and Supply Chain Intelligence Platform. I designed a synthetic logistics ecosystem containing customers, addresses, products, warehouses, inventory, orders, payments, shipments, delivery attempts, drivers, vehicles, delivery partners and returns. I generated and validated the datasets using Python and Pandas, then loaded the data into MySQL and created analytical SQL views and business queries. I used Python for operational analytics, Excel for business reporting, and Power BI for executive dashboarding. I also developed a Streamlit application connected to MySQL and implemented a Machine Learning pipeline for delivery-delay prediction using time-based validation. The overall objective was to transform raw logistics data into structured KPIs, operational insights and predictive analytics.

🧩 Architecture Explanation for HR
Layer	What Happens
🐍 Data Generation	Python generates the logistics ecosystem
🔍 Validation	Pandas validates data quality and relationships
📄 Storage	Validated datasets are maintained as CSV
🗄️ Database	MySQL stores relational operational data
🧮 SQL Analytics	Queries and analytical views generate business metrics
🐍 Python Analytics	Operational and statistical analysis
📗 Excel	Business reporting and analysis
📊 Power BI	Executive visualization and KPI reporting
🖥️ Streamlit	Interactive analytics application
🤖 ML	Predictive experimentation
💡 Business Insight	Data converted into decision-support information
🏆 Project Highlights
✅ Generated a multi-table logistics ecosystem using Python
✅ Created 100,000 orders
✅ Created 100,000 shipments
✅ Created 299,720 order-item records
✅ Created 150,000 inventory records
✅ Built 14 interconnected operational tables
✅ Implemented 124 PASS / 0 FAIL final raw data audit
✅ Built a MySQL relational database
✅ Created 10 analytical SQL views
✅ Developed 100 analytical SQL queries
✅ Built dedicated Python analytics modules
✅ Created professional Excel analytics
✅ Developed an Executive Power BI dashboard
✅ Built an interactive Streamlit application
✅ Implemented Machine Learning experiments
✅ Implemented time-based ML validation
✅ Created comprehensive project documentation
✅ Structured the project for Git/GitHub portfolio presentation
🎯 Project Outcome

LOGIX demonstrates the complete journey from synthetic logistics data to business intelligence and predictive analytics.

             Python
                +
          Data Validation
                +
              MySQL
                +
               SQL
                +
          Python Analytics
                +
              Excel
                +
            Power BI
                +
           Streamlit
                +
        Machine Learning
                ↓
        Business Insights

The project demonstrates how a Data Analyst / BI workflow can connect:

Data Engineering → Data Analytics → SQL → Business Intelligence → Visualization → Machine Learning

📌 Project Status
🟢 ANALYTICS PLATFORM — COMPLETED
Python Data Generation       ✅
Data Validation              ✅
MySQL Database               ✅
SQL Analytics                ✅
Python Analytics             ✅
Excel Analytics              ✅
Power BI Dashboard           🔒 HOLD
Streamlit Dashboard          ✅
ML Delivery Delay Pipeline   ✅
Time-Based ML Validation     ✅
Documentation                ✅
Git/GitHub 
🚀

👨‍💻 Author
Avanish Tripathi

BCA — Data Science & Artificial Intelligence

Focus Areas

Data Analytics · Business Intelligence · Data Science · Machine Learning · Python · SQL · Power BI · Excel · Supply Chain Analytics
