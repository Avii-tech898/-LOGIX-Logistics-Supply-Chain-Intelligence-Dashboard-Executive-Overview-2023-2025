-- ============================================================
-- LOGIX - Business KPI Analytics
-- Query Level: 09
-- Queries: 81 - 90
-- ============================================================

USE logix;


-- ============================================================
-- Q81. Executive KPI Summary
-- ============================================================

SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(
        SUM(oi.line_total) / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS revenue_per_order,
    ROUND(SUM(s.shipping_cost), 2) AS total_logistics_cost,
    COUNT(DISTINCT r.return_id) AS total_returns
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN shipments s
    ON o.order_id = s.order_id
LEFT JOIN returns r
    ON o.order_id = r.order_id;


-- ============================================================
-- Q82. Revenue vs Logistics Cost
-- ============================================================

WITH revenue AS (
    SELECT
        SUM(line_total) AS total_revenue
    FROM order_items
),

logistics AS (
    SELECT
        SUM(shipping_cost) AS total_logistics_cost
    FROM shipments
)

SELECT
    ROUND(r.total_revenue, 2) AS total_revenue,
    ROUND(l.total_logistics_cost, 2) AS total_logistics_cost,
    ROUND(
        100 * l.total_logistics_cost
        / NULLIF(r.total_revenue, 0),
        2
    ) AS logistics_cost_percent
FROM revenue r
CROSS JOIN logistics l;


-- ============================================================
-- Q83. Delivery Success KPI
-- ============================================================

SELECT
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN shipment_status = 'Delivered'
            THEN 1
            ELSE 0
        END
    ) AS delivered_shipments,
    SUM(
        CASE
            WHEN shipment_status = 'Failed'
            THEN 1
            ELSE 0
        END
    ) AS failed_shipments,
    ROUND(
        100 * SUM(
            CASE
                WHEN shipment_status = 'Delivered'
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS delivery_success_rate,
    ROUND(
        100 * SUM(
            CASE
                WHEN shipment_status = 'Failed'
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS shipment_failure_rate
FROM shipments;


-- ============================================================
-- Q84. On-Time Delivery KPI
-- ============================================================

SELECT
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN actual_delivery_date IS NOT NULL
             AND actual_delivery_date <= expected_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS on_time_shipments,
    SUM(
        CASE
            WHEN actual_delivery_date IS NOT NULL
             AND actual_delivery_date > expected_delivery_date
            THEN 1
            ELSE 0
        END
    ) AS delayed_shipments,
    ROUND(
        100 * SUM(
            CASE
                WHEN actual_delivery_date IS NOT NULL
                 AND actual_delivery_date <= expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS on_time_delivery_rate
FROM shipments;


-- ============================================================
-- Q85. Return & Refund KPI
-- ============================================================

SELECT
    COUNT(*) AS total_returns,
    SUM(return_quantity) AS returned_units,
    ROUND(SUM(return_amount), 2) AS total_return_value,
    ROUND(SUM(refund_amount), 2) AS total_refund_value,
    ROUND(
        100 * SUM(refund_amount)
        / NULLIF(SUM(return_amount), 0),
        2
    ) AS refund_percentage
FROM returns;


-- ============================================================
-- Q86. Customer Value KPI
-- ============================================================

WITH customer_metrics AS (
    SELECT
        c.customer_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.line_total) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY c.customer_id
)

SELECT
    COUNT(*) AS active_buying_customers,
    ROUND(AVG(total_orders), 2) AS average_orders_per_customer,
    ROUND(AVG(total_revenue), 2) AS average_customer_revenue,
    ROUND(MAX(total_revenue), 2) AS highest_customer_revenue
FROM customer_metrics;


-- ============================================================
-- Q87. Revenue Concentration
-- ============================================================

WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY o.customer_id
),

ranked_customers AS (
    SELECT
        customer_id,
        revenue,
        ROW_NUMBER() OVER (
            ORDER BY revenue DESC
        ) AS customer_rank
    FROM customer_revenue
)

SELECT
    ROUND(
        SUM(
            CASE
                WHEN customer_rank <= 100
                THEN revenue
                ELSE 0
            END
        ),
        2
    ) AS top_100_customer_revenue,
    ROUND(SUM(revenue), 2) AS total_customer_revenue,
    ROUND(
        100 * SUM(
            CASE
                WHEN customer_rank <= 100
                THEN revenue
                ELSE 0
            END
        ) / NULLIF(SUM(revenue), 0),
        2
    ) AS top_100_revenue_share_percent
FROM ranked_customers;


-- ============================================================
-- Q88. Average Logistics Cost per Shipment
-- ============================================================

SELECT
    COUNT(*) AS total_shipments,
    ROUND(SUM(shipping_cost), 2) AS total_logistics_cost,
    ROUND(AVG(shipping_cost), 2) AS average_cost_per_shipment,
    ROUND(
        SUM(shipping_cost) / NULLIF(SUM(distance_km), 0),
        2
    ) AS average_cost_per_km
FROM shipments;


-- ============================================================
-- Q89. Operational Efficiency KPI
-- ============================================================

SELECT
    COUNT(*) AS total_shipments,
    ROUND(AVG(distance_km), 2) AS average_distance_km,
    ROUND(AVG(shipping_cost), 2) AS average_shipping_cost,
    ROUND(
        AVG(
            CASE
                WHEN actual_delivery_date IS NOT NULL
                THEN DATEDIFF(
                    actual_delivery_date,
                    shipment_date
                )
            END
        ),
        2
    ) AS average_delivery_days,
    ROUND(
        100 * SUM(
            CASE
                WHEN actual_delivery_date IS NOT NULL
                 AND actual_delivery_date <= expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS on_time_rate
FROM shipments;


-- ============================================================
-- Q90. LOGIX Management KPI Dashboard
-- ============================================================

WITH revenue AS (
    SELECT
        SUM(line_total) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders
    FROM order_items
),

customers AS (
    SELECT
        COUNT(*) AS total_customers
    FROM customers
),

shipments AS (
    SELECT
        COUNT(*) AS total_shipments,
        SUM(shipping_cost) AS logistics_cost,
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

returns_data AS (
    SELECT
        COUNT(*) AS total_returns,
        SUM(refund_amount) AS total_refunds
    FROM returns
)

SELECT
    r.total_orders,
    c.total_customers,
    ROUND(r.total_revenue, 2) AS total_revenue,
    ROUND(s.logistics_cost, 2) AS total_logistics_cost,

    ROUND(
        r.total_revenue / NULLIF(r.total_orders, 0),
        2
    ) AS revenue_per_order,

    ROUND(
        s.logistics_cost / NULLIF(r.total_orders, 0),
        2
    ) AS logistics_cost_per_order,

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

    rd.total_returns,

    ROUND(
        100 * rd.total_returns
        / NULLIF(r.total_orders, 0),
        2
    ) AS return_rate,

    ROUND(rd.total_refunds, 2) AS total_refunds

FROM revenue r
CROSS JOIN customers c
CROSS JOIN shipments s
CROSS JOIN returns_data rd;