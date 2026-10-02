# Machine Learning Architecture

## Purpose
The ML layer extends LOGIX from descriptive and diagnostic analytics toward predictive analytics.

## Planned Use Cases
### 1. Delivery Delay Prediction
Predict whether a shipment is likely to be delayed.

Candidate features: delivery type, priority, distance, warehouse, delivery partner, shipping cost, SLA days, and order/shipment timing.

### 2. Demand Forecasting
Estimate future product/category demand from historical order and quantity patterns.

### 3. Inventory Stockout Risk
Identify products or warehouse-product combinations with elevated stockout risk.

### 4. Return Prediction
Estimate the probability that an order may be returned.

## ML Pipeline
```text
MySQL / CSV
    ↓
Data Selection
    ↓
Cleaning
    ↓
Feature Engineering
    ↓
Train / Validation Split
    ↓
Model Training
    ↓
Evaluation
    ↓
Model Comparison
    ↓
Business Interpretation
```

## Principle
ML should complement the existing SQL, Python, Excel, Power BI, and Streamlit layers rather than replace them.
