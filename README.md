🚚 LOGIX

Logistics & Supply Chain Intelligence Platform

From Synthetic Logistics Data to Business Intelligence, Operational Analytics & Predictive Modeling

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white"/>
<img src="https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/Git-181717?style=for-the-badge&logo=git&logoColor=white"/>
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>

</p>

End-to-End Logistics Analytics • Supply Chain Intelligence • SQL • Python • Excel • Power BI • Streamlit • Machine Learning

📊 Dashboard Preview

LOGIX Executive Dashboard — Logistics & Supply Chain Performance Overview

<!--
Add your final dashboard screenshot here:

![LOGIX Executive Dashboard](dashboard/LOGIX_DASHBOARD.png)
-->

⚡ At a Glance

📦 Data Scale

📊 Analytics

🧩 Platform

100K Orders

Sales & Revenue Analytics

MySQL

299,720 Order Items

Delivery Performance

SQL

20K Customers

Warehouse & Inventory

Python

150K Inventory Records

Customer Analytics

Excel

100K Shipments

Returns & Payments

Power BI

147,513 Delivery Attempts

Fleet Analytics

Streamlit

14 Core Tables

Predictive Analytics

Scikit-learn

10 Analytical Views

Executive KPIs

Git + GitHub

100 SQL Queries

ML Experiments

Documentation

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

🗄️ Database Architecture

🔗 Data Model

🔄 ETL & Data Processing

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

⚙️ How to Run the Project

🔁 Reproducible Data Pipeline

⚠️ Project Limitations

🚀 Future Enhancements

🗣️ Interview Explanation

🧩 Architecture Explanation for HR

🏆 Project Highlights

🎯 Project Outcome

📌 Project Status

👨‍💻 Author

🔗 Repository

📌 Project Overview

LOGIX is an end-to-end Logistics & Supply Chain Intelligence Platform designed to simulate a realistic logistics ecosystem and transform raw operational data into business-ready intelligence.

The project follows a complete analytics lifecycle:

Business Problem → Data Generation → Data Validation → MySQL → SQL Analytics → Python Analytics → Excel → Power BI → Streamlit → Machine Learning → Business Insights

LOGIX models multiple operational areas:

Customer Management

Address Management

Product Management

Warehouse Operations

Inventory Management

Order Management

Payment Processing

Shipment Operations

Delivery Attempts

Driver Management

Vehicle Management

Delivery Partners

Returns & Refunds

The project uses a synthetic Indian logistics environment covering:

January 2023 → December 2025

The objective is to demonstrate how operational logistics data can be transformed into:

Executive KPIs

Sales intelligence

Delivery intelligence

Warehouse intelligence

Inventory intelligence

Customer intelligence

Financial analytics

Returns analysis

Fleet analytics

Predictive analytics

🎯 Project Objectives

#

Objective

01

Generate a realistic logistics ecosystem

02

Build interconnected operational datasets

03

Validate data quality and relationships

04

Store validated data in MySQL

05

Develop analytical SQL queries and views

06

Perform business analytics using Python

07

Build Excel-based business analysis

08

Develop an executive Power BI analytics layer

09

Build an interactive Streamlit analytics application

10

Develop a Machine Learning pipeline

11

Implement time-aware model evaluation

12

Generate business KPIs and operational insights

13

Create a reproducible end-to-end analytics workflow

14

Document the complete project for portfolio and interview use

💼 Business Problem

Logistics companies generate large volumes of data across different operational systems.

Typical sources include:

Customers
Products
Orders
Warehouses
Inventory
Payments
Shipments
Delivery Attempts
Drivers
Vehicles
Delivery Partners
Returns

When these datasets are isolated, management may face difficulty answering:

How many orders are being processed?

What is the overall delivery performance?

Which shipments are delayed?

Which warehouses handle the highest volume?

Where is inventory at risk?

What is the total logistics cost?

Which delivery partners perform differently?

What percentage of shipments fail?

What is the return and refund exposure?

Can delivery delays be predicted?

LOGIX Solution

LOGIX creates a unified analytical environment:

Raw Logistics Data
        ↓
Data Validation
        ↓
MySQL Database
        ↓
SQL Analytics
        ↓
Python / Excel Analytics
        ↓
Power BI / Streamlit
        ↓
Machine Learning
        ↓
Business Insights

🏗️ Project Architecture

┌──────────────────────────────────────────────────────┐
│                 BUSINESS REQUIREMENTS                │
└──────────────────────────────┬───────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────┐
│                PYTHON DATA GENERATION                │
│          Pandas • NumPy • Faker • Random             │
└──────────────────────────────┬───────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────┐
│                  DATA VALIDATION                      │
│       Primary Keys • Foreign Keys • Dates • QA       │
└──────────────────────────────┬───────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────┐
│                     RAW DATA                         │
│                   14 DATASETS                        │
└──────────────────────────────┬───────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────┐
│                       MySQL                          │
│                RELATIONAL DATABASE                   │
└─────────────────────┬────────────────┬───────────────┘
                      ↓                ↓
              ┌──────────────┐  ┌───────────────┐
              │ SQL Analytics│  │ Python Layer  │
              │ 100 Queries  │  │ 6 Modules     │
              │ 10 Views     │  │ Pandas/NumPy  │
              └──────┬───────┘  └───────┬───────┘
                     └────────┬─────────┘
                              ↓
                     ┌─────────────────┐
                     │ Excel Analytics │
                     └────────┬────────┘
                              ↓
                   ┌──────────┴──────────┐
                   ↓                     ↓
             ┌──────────────┐     ┌──────────────┐
             │   Power BI   │     │   Streamlit  │
             │ BI Analytics │     │ Application  │
             └──────┬───────┘     └──────┬───────┘
                    └──────────┬─────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Machine Learning   │
                    │ Delivery Prediction │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │  Business Insights  │
                    └─────────────────────┘

One-Line Architecture

Python → Validation → CSV → MySQL → SQL → Python Analytics → Excel → Power BI → Streamlit → ML → Insights

🔄 Complete Data Journey

01. Define Logistics Business Requirements
                    ↓
02. Generate Synthetic Logistics Data
                    ↓
03. Validate Data Quality
                    ↓
04. Store Validated CSV Data
                    ↓
05. Load Data into MySQL
                    ↓
06. Create Relational Database Schema
                    ↓
07. Build Analytical SQL Views
                    ↓
08. Execute Business Analytics Queries
                    ↓
09. Perform Python Analytics
                    ↓
10. Generate Excel Analysis
                    ↓
11. Connect MySQL with Power BI
                    ↓
12. Build Executive BI Layer
                    ↓
13. Build Streamlit Analytics Application
                    ↓
14. Build Machine Learning Dataset
                    ↓
15. Perform Time-Aware Model Evaluation
                    ↓
16. Generate Business Insights

🛠️ Technology Stack

Technology

Role in LOGIX

🐍 Python

Data generation, validation and analytics

🐼 Pandas

Data manipulation and analysis

🔢 NumPy

Numerical operations

🏭 Faker

Synthetic data generation

🗄️ MySQL

Relational database

🧮 SQL

Business analytics

📗 Microsoft Excel

Business reporting

📊 Power BI

Executive BI and visualization

🖥️ Streamlit

Interactive analytics application

🤖 Scikit-learn

Machine Learning

🌿 Git

Version control

🐙 GitHub

Repository and portfolio

📝 Markdown

Technical documentation

📊 Dataset

LOGIX contains 14 interconnected datasets.

Dataset Overview

Dataset

Records

Purpose

customers.csv

20,000

Customer master

addresses.csv

30,000

Customer addresses

products.csv

5,000

Product catalog

warehouses.csv

30

Warehouse master

inventory.csv

150,000

Inventory records

orders.csv

100,000

Order transactions

order_items.csv

299,720

Product-level orders

payments.csv

100,000

Payment transactions

shipments.csv

100,000

Shipment transactions

delivery_attempts.csv

147,513

Delivery attempt history

drivers.csv

1,000

Driver master

vehicles.csv

1,200

Vehicle master

delivery_partners.csv

25

Delivery partners

returns.csv

15,000

Returns and refunds

Dataset Period

2023-01-01 → 2025-12-31

Geography

India

🗂️ Dataset Details

👥 Customers

customer_id
customer_name
email
phone
gender
customer_segment
registration_date
state
city
pincode
preferred_payment_method
is_active

Customer segments:

Standard
Premium
VIP

🏠 Addresses

address_id
customer_id
address_type
address_line
city
state
pincode
is_default

📦 Products

product_id
product_name
category
brand
unit_price
weight_kg
supplier
reorder_level
is_active

Categories:

Electronics
Fashion
Home & Kitchen
Beauty
Grocery
Sports
Books
Accessories

🏭 Warehouses

warehouse_id
warehouse_name
warehouse_type
city
state
pincode
capacity_units
manager_name
operating_hours
is_active

Total Warehouses: 30

📦 Inventory

inventory_id
warehouse_id
product_id
opening_stock
current_stock
reorder_level
unit_cost
inventory_value
stock_status
last_restock_date

Inventory status:

In Stock
Low
Out

Total Inventory Records: 150,000

🛒 Orders

order_id
customer_id
address_id
order_date
expected_delivery_date
delivery_type
priority
order_status

Order lifecycle:

Pending
   ↓
Confirmed
   ↓
Processing
   ↓
Shipped
   ↓
Delivered

Alternative outcomes:

Cancelled
Returned

Total Orders: 100,000

🧾 Order Items

order_item_id
order_id
product_id
quantity
unit_price
discount_percent
discount_amount
line_total

Total Order Items: 299,720

💳 Payments

payment_id
order_id
payment_date
payment_method
payment_status
amount
transaction_reference

Payment methods:

UPI
Credit Card
Debit Card
Cash on Delivery
Net Banking
Wallet

Payment statuses:

Paid
Pending
Failed
Refunded

🚚 Shipments

shipment_id
order_id
warehouse_id
delivery_partner_id
shipment_date
expected_delivery_date
actual_delivery_date
delivery_type
shipment_status
sla_days
shipping_cost
distance_km

Shipment lifecycle:

Created
   ↓
Picked Up
   ↓
In Transit
   ↓
Out for Delivery
   ↓
Delivered

Alternative states:

Delayed
Failed

Total Shipments: 100,000

📍 Delivery Attempts

attempt_id
shipment_id
order_id
attempt_number
attempt_date
attempt_outcome
failure_reason
notes

Total Delivery Attempts: 147,513

👨‍✈️ Drivers

driver_id
driver_name
phone
license_number
experience_years
rating
city
employment_type
status

Total Drivers: 1,000

🚗 Vehicles

vehicle_id
vehicle_number
vehicle_type
capacity_kg
fuel_type
model_year
driver_id
status

Total Vehicles: 1,200

🤝 Delivery Partners

partner_id
partner_name
service_type
coverage_type
base_cost_per_km
rating
contact_phone
status

Total Delivery Partners: 25

↩️ Returns

return_id
order_id
order_item_id
product_id
return_date
return_quantity
return_reason
return_status
return_amount
refund_amount

Total Returns: 15,000

🔍 Data Validation

LOGIX performs validation before analytical consumption.

Validation Areas

Primary Key Validation
        ↓
Foreign Key Validation
        ↓
Duplicate Detection
        ↓
Missing Value Validation
        ↓
Date Validation
        ↓
Status Validation
        ↓
Quantity Validation
        ↓
Price Validation
        ↓
Financial Validation
        ↓
Cross-Table Validation

Final Raw Dataset Audit

PASS CHECKS : 124
FAIL CHECKS : 0

STATUS:
ALL FINAL CROSS-TABLE AUDITS PASSED

🗄️ Database Architecture

LOGIX uses MySQL as the central relational data layer.

Database Name: logix
Character Set: utf8mb4

Core Tables

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

Dependency-Aware Loading Order

01. customers
02. addresses
03. products
04. warehouses
05. drivers
06. delivery_partners
07. vehicles
08. inventory
09. orders
10. order_items
11. payments
12. shipments
13. delivery_attempts
14. returns

🔗 Data Model

CUSTOMERS
   │
   ├──────────────► ADDRESSES
   │
   └──────────────► ORDERS
                         │
                         ├──────────────► ORDER_ITEMS
                         │                    │
                         │                    ▼
                         │                PRODUCTS
                         │
                         ├──────────────► PAYMENTS
                         │
                         ├──────────────► SHIPMENTS
                         │                    │
                         │                    ├──► WAREHOUSES
                         │                    │
                         │                    └──► DELIVERY_PARTNERS
                         │
                         └──────────────► RETURNS
                                              │
                                              └──► ORDER_ITEMS

WAREHOUSES
     │
     └──────────────► INVENTORY ◄──────── PRODUCTS

DRIVERS
     │
     └──────────────► VEHICLES

Schema Design Note

The current shipments table does not contain a vehicle_id.

Therefore, LOGIX intentionally avoids claiming direct shipment-level vehicle attribution.

🔄 ETL & Data Processing

EXTRACT
   ↓
Synthetic CSV Data
   ↓
VALIDATE
   ↓
Python / Pandas QA
   ↓
LOAD
   ↓
MySQL
   ↓
TRANSFORM / ANALYZE
   ↓
SQL Views + Python Analytics
   ↓
REPORT
   ↓
Excel / Power BI / Streamlit

Processing Stages

Generate synthetic master data

Generate transactional data

Validate data quality

Store validated CSV datasets

Load data into MySQL

Create relational schema

Create analytical views

Execute SQL analytics

Run Python analytics

Export Excel analysis

Connect Power BI

Run Streamlit application

Build ML datasets

Evaluate predictive models

🧮 SQL Analytics

LOGIX contains 100 analytical SQL queries.

Query Modules

01_basic_analytics.sql
02_customer_analytics.sql
03_sales_analytics.sql
04_delivery_analytics.sql
05_warehouse_inventory.sql
06_payment_returns.sql
07_fleet_analytics.sql
08_advanced_sql.sql
09_business_kpi.sql
10_management_insights.sql

SQL Concepts

SELECT

WHERE

GROUP BY

HAVING

ORDER BY

CASE

INNER JOIN

LEFT JOIN

Subqueries

CTEs

Window Functions

Ranking

Running Totals

Conditional Aggregation

KPI Calculations

Management Analytics

👁️ Analytical SQL Views

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

These views provide reusable business datasets for:

Python

Excel

Power BI

Streamlit

Management reporting

🐍 Python Analytics

The Python analytics layer contains:

python/analytics/
│
├── executive_analysis.py
├── sales_analysis.py
├── customer_analysis.py
├── delivery_analysis.py
├── warehouse_inventory_analysis.py
└── fleet_analysis.py

Executive Analytics

Measures:

Total Orders

Total Customers

Total Revenue

Logistics Cost

Failed Shipments

Returns

Refunds

On-Time Delivery

Sales Analytics

Measures:

Monthly revenue

Monthly orders

Unique customers

Revenue per order

Sales trends

Customer Analytics

Measures:

Customer activity

Customer segments

Order behavior

Customer distribution

Delivery Analytics

Measures:

Shipment volume

Delivery success

Shipment failure

Delay rate

Distance

Shipping cost

Delivery attempts

Warehouse & Inventory Analytics

Measures:

Inventory value

Current stock

Low stock

Out of stock

Inventory risk

Warehouse performance

Fleet Analytics

Measures:

Vehicle capacity

Vehicle status

Driver status

Driver rating

Driver experience

Fleet distribution

📗 Excel Analytics

The Excel layer provides business-oriented reporting.

Analysis Sheets

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

Executive Dashboard KPIs

Total Orders

Total Customers

Total Revenue

Logistics Cost

Failed Shipments

Total Returns

Total Refunds

On-Time Delivery

Revenue / Order

Logistics Cost / Order

Return Rate

Shipment Failure Rate

📊 Power BI Dashboard

The Power BI layer connects to the LOGIX MySQL analytical environment.

Executive KPI Layer

┌─────────────────┬─────────────────┬─────────────────┐
│  Total Orders   │ Total Customers │ Total Revenue   │
│     100K        │      20K        │    ₹22.08B     │
├─────────────────┼─────────────────┼─────────────────┤
│ Logistics Cost  │ Failed Shipments│ Total Returns   │
│    ₹1.42B       │      4,432      │      15K        │
└─────────────────┴─────────────────┴─────────────────┘

Dashboard Areas

Executive Overview

Orders

Customers

Revenue

Logistics Cost

Failed Shipments

Returns

Refunds

On-Time Delivery

Sales Analytics

Monthly Revenue

Monthly Orders

Customer Segments

Product Categories

Delivery Analytics

Shipment Status

Delivery Performance

Delivery Type

Delay Analysis

Failure Analysis

Warehouse Analytics

Shipment Volume

Shipping Cost

Warehouse Performance

Inventory Risk

🖥️ Streamlit Dashboard

LOGIX includes an interactive Streamlit application.

Navigation

🚚 LOGIX
│
├── Executive Overview
├── Delivery & Logistics
├── Warehouse & Inventory
├── Customer & Sales
├── Returns & Payments
└── Fleet Performance

Interactive Filters

Date Range
Warehouse
Delivery Partner
Order Status

Application Architecture

Streamlit
    ↓
Python Application
    ↓
MySQL Connector
    ↓
LOGIX Database
    ↓
Analytical SQL Queries / Views
    ↓
Interactive Visualizations

🤖 Machine Learning

LOGIX includes a dedicated Machine Learning architecture:

ml/
├── config/
├── preprocessing/
├── models/
├── evaluation/
├── notebooks/
└── outputs/

🚚 ML Experiment 01 — Delivery Delay Prediction

Objective

Predict whether a shipment will be delivered after its expected delivery date.

Target

is_delayed

0 → On Time
1 → Delayed

Feature Groups

Numeric

distance_km
shipping_cost
sla_days
processing_days
order_month
order_day_of_week
shipment_day_of_week

Categorical

delivery_type
priority
warehouse_id
delivery_partner_id

Historical

warehouse_prior_delay_rate
partner_prior_delay_rate

⏱️ Time-Aware ML Validation

The final ML pipeline uses chronological train/test evaluation.

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

Historical warehouse and partner features are generated using prior information to reduce temporal leakage.

Models

Logistic Regression

Decision Tree

Random Forest

Metrics

Accuracy

Precision

Recall

F1 Score

ROC-AUC

ML Finding

The current synthetic dataset shows relatively weak predictive signal for delivery-delay classification.

Therefore, the ML layer is treated as an experimentation and methodology layer rather than a production prediction service.

📈 Core Business KPIs

KPI

Current Value

👥 Total Customers

20,000

🛒 Total Orders

100,000

💰 Total Revenue

₹22.08B

🚚 Logistics Cost

₹1.42B

❌ Failed Shipments

4,432

↩️ Total Returns

15,000

💸 Total Refunds

₹840.53M

⏱️ On-Time Delivery

30.05%

💰 Revenue / Order

₹220,795.72

🚚 Logistics Cost / Order

₹14,245.96

↩️ Return Rate

15.00%

❌ Shipment Failure Rate

4.43%

🚚 Delivery Performance

Total Shipments        : 100,000
Delivered              : 59,818
Failed                 : 4,432
Delayed                : 6,882

Delivery Success Rate  : 59.82%
Failure Rate            : 4.43%
Delay Rate              : 6.88%

Logistics Metrics

Total Distance         : 75,296,143.11 km
Average Distance       : 753.31 km
Shipping Cost          : ₹1,424,595,971.71
Cost per KM            : ₹18.92

📦 Inventory Performance

Inventory Records      : 150,000
Current Stock          : 29,258,214
Inventory Value        : ₹1,021,576,222,353.55
Low Stock Records      : 28,271
Out of Stock Records   : 739
Inventory Risk Records : 29,010
Inventory Risk Rate    : 19.34%

↩️ Returns Performance

Return Records         : 15,000
Unique Orders Returned : 13,430
Return Quantity        : 19,709
Return Value           : ₹983,844,172.61
Refund Amount          : ₹840,527,131.70

Return Status

Refunded    : 8,561
Approved    : 1,838
Received    : 1,473
Requested   : 1,199
Picked Up  : 1,151
Rejected    : 778

💳 Payment Analytics

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

Total Payment Value

₹22,079,571,906.06

❓ Business Questions Answered

💰 Sales

What is total revenue?

How does revenue change over time?

What is revenue per order?

Which product categories contribute to revenue?

How does monthly order volume change?

🚚 Delivery

How many shipments are delivered?

What is the delivery success rate?

What is the failure rate?

What is the delay rate?

Which delivery types perform differently?

What is average delivery distance?

What is logistics cost per kilometer?

🏭 Warehouse

Which warehouses process more shipments?

What is shipping cost by warehouse?

Which warehouses have inventory risk?

How much inventory value is held?

📦 Inventory

How much stock exists?

How many products are low stock?

How many are out of stock?

What is inventory risk?

Which warehouses require attention?

👥 Customers

How many customers exist?

Which customer segments are represented?

How many orders are generated?

What is the average order value?

↩️ Returns

How many returns occur?

What are the major return reasons?

How much is refunded?

What is the return rate?

💳 Payments

Which payment methods are used?

What is payment value by method?

How many payments fail?

How much has been refunded?

🤖 Machine Learning

Can delivery delays be predicted?

Which operational features provide useful signal?

Does warehouse history provide predictive information?

Does partner history provide predictive information?

How can future shipments be evaluated without temporal leakage?

📁 Project Structure

LOGIX/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── python/
│   ├── __init__.py
│   │
│   ├── analytics/
│   │   ├── executive_analysis.py
│   │   ├── sales_analysis.py
│   │   ├── customer_analysis.py
│   │   ├── delivery_analysis.py
│   │   ├── warehouse_inventory_analysis.py
│   │   └── fleet_analysis.py
│   │
│   ├── generators/
│   ├── validation/
│   │
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
│   ├── README.md
│   └── .env.example
│
├── powerbi/
│
├── excel/
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
├── README.md
└── requirements.txt

📊 Key Project Metrics

Metric

Value

👥 Customers

20,000

🏠 Addresses

30,000

📦 Products

5,000

🏭 Warehouses

30

📦 Inventory Records

150,000

🛒 Orders

100,000

🧾 Order Items

299,720

💳 Payments

100,000

🚚 Shipments

100,000

📍 Delivery Attempts

147,513

👨‍✈️ Drivers

1,000

🚗 Vehicles

1,200

🤝 Delivery Partners

25

↩️ Returns

15,000

👁️ SQL Views

10

🧮 SQL Queries

100

🔍 Validation Checks

124 PASS / 0 FAIL

🎓 Skills Demonstrated

📊 Data & Analytics

📈 BI & Modeling

💻 Development

Data Generation

Power BI

Python

Data Cleaning

Data Modeling

Pandas

Data Validation

SQL Views

NumPy

KPI Development

Dashboard Development

MySQL

Sales Analytics

Executive Reporting

Streamlit

Delivery Analytics

ML Evaluation

Git

Inventory Analytics

Time-Based Validation

GitHub

Customer Analytics

Predictive Analytics

Documentation

Logistics Analytics

Business Storytelling

Reproducible Pipelines

⚙️ How to Run the Project

1️⃣ Clone Repository

git clone https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025.git

2️⃣ Navigate to Project

cd -LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025

3️⃣ Create Virtual Environment

python -m venv .venv

Windows

.venv\Scripts\activate

4️⃣ Install Dependencies

pip install pandas numpy openpyxl mysql-connector-python scikit-learn streamlit python-dotenv joblib

5️⃣ Create MySQL Database

CREATE DATABASE logix
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

6️⃣ Configure Environment Variables

Create .env locally:

LOGIX_DB_HOST=localhost
LOGIX_DB_PORT=3306
LOGIX_DB_USER=root
LOGIX_DB_PASSWORD=YOUR_PASSWORD
LOGIX_DB_NAME=logix

Never commit database credentials to GitHub.

7️⃣ Setup Database Schema

Run SQL scripts from:

sql/
├── 01_database_setup/
├── 02_schema/
└── 03_views/

8️⃣ Load Data

Load validated datasets from:

data/raw/

into the corresponding MySQL tables.

9️⃣ Run Python Analytics

Analytics modules are located under:

python/analytics/

🔟 Run Streamlit

cd dashboard
streamlit run app.py

🔁 Reproducible Data Pipeline

                 BUSINESS REQUIREMENTS
                         │
                         ▼
                PYTHON DATA GENERATION
                         │
                         ▼
                  14 RAW DATASETS
                         │
                         ▼
                   DATA VALIDATION
                         │
                         ▼
                    CSV DATA LAYER
                         │
                         ▼
                    MySQL DATABASE
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
             SQL       Python     Excel
           Analytics   Analytics   Reports
              │          │          │
              └──────────┼──────────┘
                         ↓
                     Power BI
                         ↓
                    Streamlit
                         ↓
                Machine Learning
                         ↓
                 Business Insights

⚠️ Project Limitations

LOGIX is a synthetic-data portfolio project.

Data

Data is synthetically generated.

It does not represent confidential company data.

Real-world logistics distributions may differ.

Machine Learning

ML performance depends on the synthetic data-generating process.

The current delivery-delay experiment shows relatively weak predictive signal.

More real-world operational features would be required for production deployment.

Vehicle Analytics

The current shipments table does not contain vehicle_id.

Therefore:

LOGIX does not claim direct shipment-level vehicle performance attribution.

Business Definitions

Some KPI definitions may require organization-specific business rules before production deployment.

🚀 Future Enhancements

Predictive Analytics

🔮 Demand Forecasting

🚚 Delivery Failure Prediction

📦 Stockout Prediction

👥 Customer Churn Prediction

🎯 Customer Segmentation

🚨 Anomaly Detection

Optimization

🗺️ Route Optimization

🚚 Fleet Optimization

📦 Inventory Optimization

🏭 Warehouse Optimization

💰 Logistics Cost Optimization

Engineering

☁️ Cloud Database

⚡ Real-Time Shipment Tracking

🔄 Automated ETL

📡 Streaming Pipelines

🤖 MLOps

🌐 Power BI Service

🔐 Authentication

📊 Automated Reporting

🗣️ Interview Explanation

"Tell me about your LOGIX project."

LOGIX is an end-to-end Logistics and Supply Chain Intelligence Platform. I built a synthetic logistics ecosystem containing customers, addresses, products, warehouses, inventory, orders, payments, shipments, delivery attempts, drivers, vehicles, delivery partners and returns. I generated the datasets using Python and Pandas and implemented validation checks for primary keys, foreign keys, dates, statuses and cross-table relationships. After validation, I loaded the data into MySQL and created analytical SQL views and queries for sales, delivery, warehouse, inventory, customer, payment and return analysis. I then built Python analytics modules, Excel reports, a Power BI analytics layer and a Streamlit dashboard. For predictive analytics, I implemented a delivery-delay prediction pipeline using Logistic Regression, Decision Tree and Random Forest, along with a time-based train-test methodology to reduce temporal leakage. The main objective was to transform raw logistics data into structured KPIs, operational intelligence and predictive analytics.

🧩 Architecture Explanation for HR

Layer

Responsibility

🐍 Data Generation

Python generates synthetic logistics data

🔍 Validation

Pandas validates quality and relationships

📄 Data Layer

Validated CSV datasets

🗄️ Database

MySQL stores structured operational data

🧮 SQL Analytics

Queries and views generate analytical datasets

🐍 Python Analytics

Operational and statistical analysis

📗 Excel

Business reporting

📊 Power BI

Executive visualization

🖥️ Streamlit

Interactive analytics application

🤖 Machine Learning

Predictive experimentation

💡 Business Insights

Decision-support information

🏆 Project Highlights

✅ Built an end-to-end logistics analytics platform

✅ Generated 14 interconnected datasets

✅ Created 20,000 customers

✅ Created 30,000 addresses

✅ Created 5,000 products

✅ Created 150,000 inventory records

✅ Created 100,000 orders

✅ Created 299,720 order items

✅ Created 100,000 payments

✅ Created 100,000 shipments

✅ Created 147,513 delivery attempts

✅ Created 15,000 returns

✅ Created 1,000 drivers

✅ Created 1,200 vehicles

✅ Created 25 delivery partners

✅ Implemented 124 validation checks

✅ Achieved 124 PASS / 0 FAIL

✅ Built MySQL relational database

✅ Created 10 analytical SQL views

✅ Developed 100 analytical SQL queries

✅ Developed dedicated Python analytics modules

✅ Created professional Excel analysis

✅ Connected MySQL with Power BI

✅ Built Streamlit analytics application

✅ Implemented Delivery Delay Prediction

✅ Implemented time-aware ML validation

✅ Added historical operational features

✅ Created technical documentation

✅ Structured project for GitHub portfolio presentation

🎯 Project Outcome

LOGIX demonstrates the complete journey from raw operational data to business intelligence and predictive analytics.

              RAW LOGISTICS DATA
                       │
                       ▼
              DATA VALIDATION
                       │
                       ▼
                  MySQL DB
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
         SQL         Python       Excel
          │            │            │
          └────────────┼────────────┘
                       ↓
                   Power BI
                       ↓
                   Streamlit
                       ↓
              Machine Learning
                       ↓
              BUSINESS INSIGHTS

The project combines:

Data Generation + Data Quality + SQL + Python + Excel + Business Intelligence + Visualization + Machine Learning

into one integrated portfolio project.

📌 Project Status

Component

Status

Python Data Generation

✅ Completed

Data Validation

✅ Completed

MySQL Database

✅ Completed

Database Schema

✅ Completed

Analytical Views

✅ Completed

SQL Analytics

✅ Completed

Python Analytics

✅ Completed

Excel Analytics

✅ Completed

Streamlit Dashboard

✅ Completed

Power BI MySQL Connection

✅ Completed

Power BI Executive Layer

🔒 On Hold

Delivery Delay ML

✅ Completed

Time-Aware ML Pipeline

✅ Completed

Documentation

✅ Completed

Git Repository

🚀 Active

👨‍💻 Author

Avanish Tripathi

BCA — Data Science & Artificial Intelligence

Technical Focus

Data Analytics
Business Intelligence
Data Science
Machine Learning
Python
SQL
MySQL
Power BI
Excel
Streamlit
Supply Chain Analytics

🔗 Repository



<p align="center">

🚚 LOGIX

Logistics & Supply Chain Intelligence Platform

Turning Logistics Data into Business Intelligence

Built with:

Python • Pandas • MySQL • SQL • Excel • Power BI • Streamlit • Scikit-learn

</p>

<p align="center">

⭐ If you find this project useful, consider giving the repository a star.

</p>
