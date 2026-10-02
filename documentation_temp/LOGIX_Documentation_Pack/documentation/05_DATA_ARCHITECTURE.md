# Data Architecture

## Master Tables
customers, addresses, products, warehouses, drivers, vehicles, delivery_partners, inventory.

## Transactional Tables
orders, order_items, payments, shipments, delivery_attempts, returns.

## Key Relationships
- customers → addresses
- customers → orders
- addresses → orders
- orders → order_items
- products → order_items
- orders → payments
- orders → shipments
- shipments → delivery_attempts
- orders / order_items / products → returns
- warehouses → inventory
- products → inventory
- drivers → vehicles
- warehouses / delivery_partners → shipments

## Important Data Model Note
The current `shipments` table does not contain `vehicle_id`. Vehicles contain `driver_id`, but shipments are not directly attributed to a vehicle or driver. Therefore vehicle-level and driver-level shipment performance should not be inferred without an explicit mapping table or schema change.
