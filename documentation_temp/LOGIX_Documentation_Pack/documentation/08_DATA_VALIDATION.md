# Data Validation

## Validation Layers
1. Master-data validation
2. Transactional-data validation
3. Cross-table final audit
4. MySQL/SQL analytics validation

## Final Raw Data Audit
- PASS: 124
- FAIL: 0
- Result: all final cross-table audits passed

## Validation Examples
Unique IDs, required fields, foreign keys, date ordering, status relationships, quantity/price validation, shipment SLA validation, delivery-attempt consistency, return integrity, and customer-address consistency.

## Validation Scripts
```text
python/validation/validate_master_data.py
python/validation/validate_transactional_data.py
python/validation/final_data_audit.py
python/validation/validate_logix_all.py
python/validation/validate_sql_analytics.py
```
