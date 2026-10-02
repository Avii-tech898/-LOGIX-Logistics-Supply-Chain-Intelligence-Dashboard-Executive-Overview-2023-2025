# Database Schema

## Database
**MySQL database:** `logix`

## Tables
1. customers
2. addresses
3. products
4. warehouses
5. drivers
6. delivery_partners
7. vehicles
8. inventory
9. orders
10. order_items
11. payments
12. shipments
13. delivery_attempts
14. returns

## Schema Files
Executable schema definitions are maintained under `sql/02_schema/`.

## Design Principles
- Primary keys identify records uniquely.
- Foreign keys maintain relational integrity.
- Transaction tables reference master data.
- Monetary fields use decimal-compatible values.
- Operational statuses follow defined business states.
