# System Architecture

```text
                    LOGIX
                      |
        +-------------+-------------+
        |                           |
   Data Engineering            Analytics
        |                           |
 Python Generators             SQL / Python
        |                           |
 CSV Raw Data --------------> MySQL
        |                           |
 Validation                     Views / Queries
        |                           |
        +-------------+-------------+
                      |
             +--------+--------+
             |                 |
          Excel            Power BI
             |                 |
             +--------+--------+
                      |
                 Streamlit
                      |
                 ML Layer
                      |
       Prediction / Forecasting / Risk
```

## Technology Responsibilities
### Python
Synthetic data generation, validation, analytics, database connectivity, Excel exports.

### MySQL
Data storage, relational integrity, SQL views, business analytics queries.

### Excel
Operational analysis and executive reporting.

### Power BI
Interactive BI reporting and KPI visualization.

### Streamlit
Python-native interactive analytics application.

### ML
Predictive and risk-oriented analytics.
