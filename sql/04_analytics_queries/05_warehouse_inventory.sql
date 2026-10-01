-- ============================================================
-- LOGIX - Warehouse & Inventory Analytics
-- Query Level: 05
-- Queries: 41 - 50
-- ============================================================

USE logix;


-- ============================================================
-- Q41. Warehouse Shipment Volume
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.state,
    COUNT(s.shipment_id) AS total_shipments
FROM warehouses w
LEFT JOIN shipments s
    ON w.warehouse_id = s.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name,
    w.city,
    w.state
ORDER BY total_shipments DESC;


-- ============================================================
-- Q42. Warehouse Logistics Cost
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    ROUND(SUM(s.shipping_cost), 2) AS total_shipping_cost,
    ROUND(AVG(s.shipping_cost), 2) AS average_shipping_cost
FROM warehouses w
JOIN shipments s
    ON w.warehouse_id = s.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY total_shipping_cost DESC;


-- ============================================================
-- Q43. Warehouse Average Delivery Distance
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    ROUND(AVG(s.distance_km), 2) AS average_distance_km,
    ROUND(SUM(s.distance_km), 2) AS total_distance_km
FROM warehouses w
JOIN shipments s
    ON w.warehouse_id = s.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY average_distance_km DESC;


-- ============================================================
-- Q44. Warehouse On-Time Delivery Rate
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    COUNT(s.shipment_id) AS total_shipments,
    SUM(
        CASE
            WHEN s.actual_delivery_date IS NOT NULL
             AND s.actual_delivery_date <= s.expected_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS on_time_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN s.actual_delivery_date IS NOT NULL
                 AND s.actual_delivery_date <= s.expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(s.shipment_id), 0),
        2
    ) AS on_time_rate
FROM warehouses w
JOIN shipments s
    ON w.warehouse_id = s.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY on_time_rate DESC;


-- ============================================================
-- Q45. Inventory Stock Status
-- ============================================================

SELECT
    stock_status,
    COUNT(*) AS inventory_records,
    SUM(current_stock) AS total_current_stock,
    ROUND(SUM(inventory_value), 2) AS total_inventory_value
FROM inventory
GROUP BY stock_status
ORDER BY inventory_records DESC;


-- ============================================================
-- Q46. Warehouse Inventory Value
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    COUNT(i.inventory_id) AS inventory_records,
    SUM(i.current_stock) AS current_stock_units,
    ROUND(SUM(i.inventory_value), 2) AS inventory_value
FROM warehouses w
JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY inventory_value DESC;


-- ============================================================
-- Q47. Low Stock Products
-- ============================================================

SELECT
    i.inventory_id,
    i.warehouse_id,
    i.product_id,
    i.current_stock,
    i.reorder_level,
    i.stock_status
FROM inventory i
WHERE i.current_stock <= i.reorder_level
ORDER BY
    i.current_stock ASC,
    i.reorder_level DESC;


-- ============================================================
-- Q48. Top Products by Inventory Value
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(i.current_stock) AS total_stock,
    ROUND(SUM(i.inventory_value), 2) AS total_inventory_value
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_inventory_value DESC
LIMIT 20;


-- ============================================================
-- Q49. Inventory Value by Product Category
-- ============================================================

SELECT
    p.category,
    SUM(i.current_stock) AS total_stock_units,
    ROUND(SUM(i.inventory_value), 2) AS total_inventory_value,
    ROUND(AVG(i.unit_cost), 2) AS average_unit_cost
FROM inventory i
JOIN products p
    ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY total_inventory_value DESC;


-- ============================================================
-- Q50. Warehouse Stock Health
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    COUNT(i.inventory_id) AS total_inventory_records,
    SUM(
        CASE
            WHEN i.current_stock <= i.reorder_level
            THEN 1
            ELSE 0
        END
    ) AS low_stock_records,
    SUM(
        CASE
            WHEN i.current_stock > i.reorder_level
            THEN 1
            ELSE 0
        END
    ) AS healthy_stock_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN i.current_stock <= i.reorder_level
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(i.inventory_id), 0),
        2
    ) AS low_stock_rate
FROM warehouses w
JOIN inventory i
    ON w.warehouse_id = i.warehouse_id
GROUP BY
    w.warehouse_id,
    w.warehouse_name
ORDER BY low_stock_rate DESC;