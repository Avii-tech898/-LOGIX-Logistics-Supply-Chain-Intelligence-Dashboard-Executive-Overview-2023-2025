🚚 LOGIX — Logistics & Supply Chain Intelligence Platform
From synthetic logistics data to business-ready insights

LOGIX is an end-to-end Logistics & Supply Chain Analytics Platform built using Python, MySQL/SQL, Excel, Power BI, and Machine Learning.
Business Problem → Data Generation → Validation → MySQL → SQL Analytics → Python Analytics → Excel → Power BI → Business Insights → ML Experimentation
📊 Project Overview
LOGIX simulates logistics operations across India for the period 2023–2025.
The platform integrates:
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
The objective is to transform operational data into reliable KPIs, analytical insights, dashboards, recommendations, and ML experiments.
🎯 Business Problem
A logistics organization generates large amounts of operational data, but fragmented data makes it difficult to monitor delivery performance, logistics costs, warehouse efficiency, inventory risk, customer behavior, failed shipments, returns, and delivery-partner performance.
Core Question
How can logistics data be integrated and analyzed to improve operational efficiency, control costs, understand customers, optimize inventory, and support data-driven management decisions?

🎯 Project Objectives
- Generate realistic large-scale logistics data
- Maintain primary-key and foreign-key integrity
- Validate business rules before analytics
- Build a relational MySQL database
- Create reusable analytical SQL views
- Perform business analysis using Python
- Build Excel analytical reports
- Develop an executive Power BI dashboard
- Calculate operational and financial KPIs
- Identify business insights and risks
- Experiment with delivery-delay prediction
- Document the complete analytics lifecycle
🔄 Complete Data Journey
Business Problem
       ↓
Synthetic Data Generation
       ↓
Data Validation
       ↓
Raw CSV Datasets
       ↓
MySQL Database
       ↓
SQL Queries + Analytical Views
       ↓
Python Analytics
       ↓
Excel Analysis
       ↓
Power BI Dashboard
       ↓
Business Insights
       ↓
ML Experimentation
🏗️ System Architecture
┌───────────────────────────────────────────────┐
│                  LOGIX                        │
├───────────────────────────────────────────────┤
│ Python Data Generator                         │
│          ↓                                    │
│ Raw CSV Data                                  │
│          ↓                                    │
│ Validation Layer                              │
│          ↓                                    │
│ MySQL Database                                │
│          ↓                                    │
│ SQL Analytics + Views                         │
│       ↙          ↘                            │
│ Python        Power BI                        │
│ Analytics      Dashboard                      │
│                    ↓                          │
│             Business Insights                 │
│                    +                          │
│             ML Experiment                     │
└───────────────────────────────────────────────┘
🛠️ Technology Stack
Area	Technology
Programming	Python
Data Processing	Pandas, NumPy
Data Generation	Faker, Python
Database	MySQL
Query Language	MySQL 8+ / SQL
Spreadsheet	Microsoft Excel
BI	Microsoft Power BI
Visualization	Matplotlib, Seaborn
Machine Learning	Scikit-learn
Version Control	Git / GitHub
IDE	VS Code
Dashboard	Power BI / Streamlit


📦 Dataset
LOGIX uses a synthetically generated dataset for portfolio and analytics demonstration.
Period: 2023-01-01 to 2025-12-31
Geography: India
Random seed: 42
The data-generation process uses configuration-driven generation, controlled relationships, business rules, and cross-table validation.
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


Total generated records: 1M+
🗄️ Data Model
Customers
    │
    ├── Addresses
    │
    └── Orders
          │
          ├── Order Items ─── Products
          ├── Payments
          ├── Shipments
          │      └── Delivery Attempts
          └── Returns

Warehouses ─── Inventory ─── Products

Drivers ─── Vehicles

Delivery Partners ─── Shipments
MySQL Tables
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
✅ Data Validation
The final raw-data audit completed with:
124 PASS
0 FAIL
Validation covers:
- Primary-key uniqueness
- Foreign-key integrity
- Duplicate detection
- Missing values
- Date consistency
- Status transitions
- Quantity validation
- Price validation
- Revenue reconciliation
- Payment reconciliation
- Shipment validation
- Return validation
- Cross-table business rules
Important checks include:
- 100,000 unique orders
- 100,000 unique shipments
- 100,000 payments
- Payment value reconciles with order-item revenue
- Delivery attempts reference valid shipments
- Returns reference valid order items
- Inventory references valid products and warehouses
🗃️ MySQL & SQL Analytics
Database:
logix
SQL structure:
sql/
├── 01_database_setup/
├── 02_schema/
├── 03_views/
├── 04_analytics_queries/
└── 05_advanced_analytics/
Analytical Views
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
SQL Skills
- SELECT
- WHERE
- GROUP BY
- HAVING
- JOINs
- CASE
- Subqueries
- CTEs
- Window Functions
- ROW_NUMBER
- RANK
- LAG
- Running Totals
- Revenue Contribution
- Customer Analytics
- KPI Analysis
The project contains 100 analytical SQL queries plus an advanced business-analysis layer.
🐍 Python Analytics
Python is used for data generation, validation, database connectivity, KPI analysis, and analytical reporting.
python/
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
Main workbooks:
LOGIX_Excel_Analysis.xlsx
LOGIX_Excel_Analysis_Professional.xlsx
LOGIX_Executive_Dashboard_v7.xlsx
Main sheets:
- Executive KPI
- Sales Analysis
- Customer Analysis
- Delivery Analysis
- Warehouse Analysis
- Inventory Analysis
- Returns Analysis
- Payment Analysis
- Monthly Sales
- Fleet Analysis
📈 Power BI Dashboard
The Power BI layer provides an executive-level view of logistics operations.
Executive Overview
KPI Cards
- Total Orders
- Total Customers
- Total Revenue
- Total Logistics Cost
- Failed Shipments
- Total Returns
- On-Time Delivery
Visualizations
- Monthly Revenue Trend
- Monthly Orders Trend
- Shipment Status Distribution
- Shipments by Delivery Type
- Revenue by State / Geographic Analysis
- Operational KPI cards
Dashboard period: 2023–2025

💰 Key Business KPIs
KPI	Value
Total Orders	100,000
Total Customers	20,000
Total Revenue	₹22,079,571,906.06
Logistics Cost	₹1,424,595,971.71
Failed Shipments	4,432
Total Returns	15,000
Total Refunds	₹840,527,131.70
On-Time Delivery	30.05%
Revenue / Order	₹220,795.72
Logistics Cost / Order	₹14,245.96
Return Rate	15.00%
Shipment Failure Rate	4.43%


🚚 Delivery Analytics
- Total shipments: 100,000
- Delivered: 59,818
- Failed: 4,432
- Delayed: 6,882
- Delivery success rate: 59.82%
- Shipment failure rate: 4.43%
- Delay rate: 6.88%
- Total distance: 75,296,143.11 km
- Shipping cost: ₹1,424,595,971.71
- Average distance: 753.31 km
- Shipping cost/km: ₹18.92
Delivery attempts:
- Delivered: 66,700
- Failed: 20,321
- Customer Unavailable: 20,291
- Wrong Address: 20,141
- Rescheduled: 20,060
📦 Inventory Analytics
- 150,000 inventory records
- Current stock: 29,258,214
- Inventory value: ₹1,021,576,222,353.55
- Low stock: 28,271
- Out of stock: 739
- Total stock-risk records: 29,010
- Stock-risk rate: 19.34%
👥 Customer Analytics
Customer analytics covers:
- Customer revenue
- Order frequency
- Repeat customers
- Customer segments
- Average order value
- Customer lifetime value
- Revenue contribution
Customer base:
20,000 customers
🔄 Returns & Payments
Returns:
15,000 returns
Major return reasons:
- Late Delivery
- Changed Mind
- Damaged Product
- Wrong Product
- Size Issue
- Quality Issue
- Other
- Product Defective
Payment methods:
- UPI
- Credit Card
- Debit Card
- Cash on Delivery
- Net Banking
- Wallet
Payment statuses:
- Paid
- Pending
- Failed
- Refunded
🚛 Fleet Analytics
Fleet data includes:
1,200 vehicles
1,000 drivers
25 delivery partners
Vehicle attributes:
- Vehicle type
- Capacity
- Fuel type
- Model year
- Driver assignment
- Status
Driver attributes:
- Experience
- Rating
- Employment type
- Status
Schema Limitation
The current shipments table does not contain vehicle_id.
Therefore, LOGIX does not fabricate vehicle-level shipment performance. Vehicle and driver analytics remain separate unless an explicit vehicle-to-shipment mapping is introduced.
🤖 Machine Learning
LOGIX includes a Delivery Delay Prediction experiment.
Objective
Predict whether a shipment will experience a delivery delay.
Models
- Logistic Regression
- Decision Tree
- Random Forest
Evaluation
- Random split baseline
- Feature-engineered evaluation
- Time-based evaluation
Final Time-Based Results
Model	Accuracy	Precision	Recall	F1	ROC-AUC
Decision Tree	69.58%	70.03%	98.84%	81.98%	0.5051
Random Forest	70.00%	70.00%	100%	82.35%	0.4962
Logistic Regression	70.00%	70.00%	100%	82.35%	0.4947


ML Conclusion
The current synthetic dataset contains weak predictive signal for delivery delay. ROC-AUC values close to 0.50 indicate that the current features do not provide strong predictive discrimination.
This is documented honestly as an experimental result, not as a production-ready model.
Future models could use:
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
Clone
git clone https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025.git
cd -LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025
Create environment
python -m venv .venv
Windows PowerShell:
.\.venv\Scripts\Activate.ps1
Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn faker mysql-connector-python
🗄️ MySQL Setup
CREATE DATABASE logix
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
Then:
1. Create the schema
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
📈 Power BI Connection
Power BI
   ↓
MySQL
   ↓
logix
   ↓
Analytical Views
   ↓
Executive Dashboard
Recommended reporting views:
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
Model Evaluation
          ↓
Model Comparison
Outputs:
ml/outputs/
🔁 Reproducibility
LOGIX follows reproducible analytics principles:
- Fixed random seed
- Configuration-driven generation
- Controlled synthetic data
- Data validation before loading
- Relational integrity
- Reusable SQL views
- Modular Python scripts
- Separate ML preprocessing
- Time-aware ML evaluation
- Git version control
💡 Business Insights
Delivery Performance
The dataset shows a substantial gap between total shipments and successfully delivered shipments, making delivery operations an important improvement area.
Failed Shipments
A 4.43% shipment failure rate represents a measurable operational risk that can be investigated by delivery partner, region, delivery type, and failure reason.
Inventory Risk
A 19.34% stock-risk rate indicates that inventory optimization is an important operational focus.
Returns
A 15% return rate creates opportunities to analyze product quality, delivery experience, product mismatch, and customer behavior.
Logistics Cost
Approximately ₹1.42B logistics cost makes cost-to-serve analysis a significant management opportunity.
ML Opportunity
Weak ML performance indicates that richer operational features are required before deploying a production delivery-delay model.
⚠️ Data Quality & Limitations
Synthetic Dataset
The dataset is synthetic and should not be interpreted as actual company performance.
ML Limitation
The current features do not provide strong predictive signal for delivery delays.
Vehicle Mapping
shipments currently does not contain vehicle_id, so vehicle-level shipment attribution is not claimed.
KPI Definition
Operational KPIs such as on-time delivery require clear denominator definitions.
Future versions should distinguish:
All Shipments
Delivered Shipments
SLA-Eligible Shipments
🔮 Future Enhancements
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
- Inventory-risk dashboard
- Customer 360 dashboard
Machine Learning
- Demand forecasting
- ETA prediction
- Improved delivery-delay prediction
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
The project converts operational logistics data into management-ready insights for monitoring delivery performance, controlling logistics costs, identifying inventory risks, understanding customer behavior, and supporting data-driven decisions.

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
1M+ Total Records
124 Validation Checks Passed
100 SQL Analytics Queries
10 Analytical SQL Views
📌 Project Status
Component	Status
Data Generation	✅ Complete
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
Areas of Interest
- Data Analytics
- Data Science
- Machine Learning
- Business Intelligence
- Python
- SQL
- Power BI
⭐ Repository
LOGIX — Logistics & Supply Chain Intelligence Platform
https://github.com/Avii-tech898/-LOGIX-Logistics-Supply-Chain-Intelligence-Dashboard-Executive-Overview-2023-2025
LOGIX — Turning Logistics Data into Business Intelligence.
