-- ============================================================
-- LOGIX - Management Insights & Decision Support
-- Query Level: 10
-- Queries: 91 - 100
-- ============================================================

USE logix;


-- ============================================================
-- Q91. Monthly Revenue and Order Trend
-- ============================================================

WITH monthly_data AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)

SELECT
    month,
    total_orders,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        revenue / NULLIF(total_orders, 0),
        2
    ) AS revenue_per_order
FROM monthly_data
ORDER BY month;


-- ============================================================
-- Q92. Customer Segment Business Performance
-- ============================================================

SELECT
    c.customer_segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.line_total), 2) AS revenue,
    ROUND(
        SUM(oi.line_total)
        / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS revenue_per_order
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_segment
ORDER BY revenue DESC;


-- ============================================================
-- Q93. Product Category Business Performance
-- ============================================================

SELECT
    p.category,
    COUNT(DISTINCT oi.order_id) AS orders,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.line_total), 2) AS revenue,
    ROUND(SUM(oi.discount_amount), 2) AS discounts,
    ROUND(
        100 * SUM(oi.discount_amount)
        / NULLIF(
            SUM(oi.discount_amount) + SUM(oi.line_total),
            0
        ),
        2
    ) AS discount_rate
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- ============================================================
-- Q94. Warehouse Operational Scorecard
-- ============================================================

SELECT
    w.warehouse_id,
    w.warehouse_name,
    COUNT(s.shipment_id) AS shipments,
    ROUND(SUM(s.shipping_cost), 2) AS logistics_cost,
    ROUND(AVG(s.distance_km), 2) AS average_distance_km,
    ROUND(
        100 * SUM(
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
-- Q95. Delivery Partner Scorecard
-- ============================================================

SELECT
    dp.partner_id,
    dp.partner_name,
    dp.service_type,
    COUNT(s.shipment_id) AS shipments,
    ROUND(AVG(s.distance_km), 2) AS average_distance_km,
    ROUND(AVG(s.shipping_cost), 2) AS average_shipping_cost,
    ROUND(
        100 * SUM(
            CASE
                WHEN s.actual_delivery_date IS NOT NULL
                 AND s.actual_delivery_date <= s.expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(s.shipment_id), 0),
        2
    ) AS on_time_rate
FROM delivery_partners dp
JOIN shipments s
    ON dp.partner_id = s.delivery_partner_id
GROUP BY
    dp.partner_id,
    dp.partner_name,
    dp.service_type
ORDER BY on_time_rate DESC;


-- ============================================================
-- Q96. High-Value Customers
-- ============================================================

WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.customer_segment,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.line_total) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name,
        c.customer_segment
)

SELECT
    customer_id,
    customer_name,
    customer_segment,
    total_orders,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        total_revenue / NULLIF(total_orders, 0),
        2
    ) AS average_order_value
FROM customer_revenue
WHERE total_revenue >= (
    SELECT AVG(total_revenue)
    FROM customer_revenue
)
ORDER BY total_revenue DESC;


-- ============================================================
-- Q97. Inventory Risk Analysis
-- ============================================================

SELECT
    w.warehouse_name,
    p.category,
    COUNT(i.inventory_id) AS inventory_records,
    SUM(i.current_stock) AS current_stock,
    SUM(
        CASE
            WHEN i.current_stock <= i.reorder_level
            THEN 1
            ELSE 0
        END
    ) AS low_stock_records,
    ROUND(SUM(i.inventory_value), 2) AS inventory_value
FROM inventory i
JOIN warehouses w
    ON i.warehouse_id = w.warehouse_id
JOIN products p
    ON i.product_id = p.product_id
GROUP BY
    w.warehouse_name,
    p.category
HAVING low_stock_records > 0
ORDER BY low_stock_records DESC;


-- ============================================================
-- Q98. Return Risk by Product Category
-- ============================================================

WITH category_sales AS (
    SELECT
        p.category,
        SUM(oi.quantity) AS sold_units
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.category
),

category_returns AS (
    SELECT
        p.category,
        SUM(r.return_quantity) AS returned_units,
        COUNT(r.return_id) AS return_count
    FROM returns r
    JOIN products p
        ON r.product_id = p.product_id
    GROUP BY p.category
)

SELECT
    s.category,
    s.sold_units,
    COALESCE(r.returned_units, 0) AS returned_units,
    COALESCE(r.return_count, 0) AS return_count,
    ROUND(
        100 * COALESCE(r.returned_units, 0)
        / NULLIF(s.sold_units, 0),
        2
    ) AS unit_return_rate
FROM category_sales s
LEFT JOIN category_returns r
    ON s.category = r.category
ORDER BY unit_return_rate DESC;


-- ============================================================
-- Q99. Delivery Failure Risk Analysis
-- ============================================================

SELECT
    da.failure_reason,
    COUNT(*) AS failed_attempts,
    COUNT(DISTINCT da.shipment_id) AS affected_shipments,
    ROUND(
        100 * COUNT(*)
        / NULLIF(
            (SELECT COUNT(*) FROM delivery_attempts),
            0
        ),
        2
    ) AS percentage_of_attempts
FROM delivery_attempts da
WHERE da.attempt_outcome <> 'Delivered'
GROUP BY da.failure_reason
ORDER BY affected_shipments DESC;


-- ============================================================
-- Q100. LOGIX Overall Management Summary
-- ============================================================

WITH order_metrics AS (
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS total_customers,
        ROUND(SUM(oi.line_total), 2) AS total_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
),

shipment_metrics AS (
    SELECT
        COUNT(*) AS total_shipments,
        ROUND(SUM(shipping_cost), 2) AS total_logistics_cost,
        SUM(
            CASE
                WHEN shipment_status = 'Failed'
                THEN 1
                ELSE 0
            END
        ) AS failed_shipments,
        SUM(
            CASE
                WHEN actual_delivery_date IS NOT NULL
                 AND actual_delivery_date <= expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) AS on_time_shipments
    FROM shipments
),

return_metrics AS (
    SELECT
        COUNT(*) AS total_returns,
        ROUND(SUM(refund_amount), 2) AS total_refunds
    FROM returns
)

SELECT
    o.total_orders,
    o.total_customers,
    o.total_revenue,
    s.total_shipments,
    s.total_logistics_cost,

    ROUND(
        o.total_revenue
        / NULLIF(o.total_orders, 0),
        2
    ) AS revenue_per_order,

    ROUND(
        s.total_logistics_cost
        / NULLIF(s.total_shipments, 0),
        2
    ) AS logistics_cost_per_shipment,

    s.failed_shipments,

    ROUND(
        100 * s.failed_shipments
        / NULLIF(s.total_shipments, 0),
        2
    ) AS shipment_failure_rate,

    ROUND(
        100 * s.on_time_shipments
        / NULLIF(s.total_shipments, 0),
        2
    ) AS on_time_delivery_rate,

    r.total_returns,
    r.total_refunds,

    ROUND(
        100 * r.total_returns
        / NULLIF(o.total_orders, 0),
        2
    ) AS return_rate

FROM order_metrics o
CROSS JOIN shipment_metrics s
CROSS JOIN return_metrics r;