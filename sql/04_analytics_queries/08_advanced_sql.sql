-- ============================================================
-- LOGIX - Advanced SQL Analytics
-- Query Level: 08
-- Queries: 71 - 80
-- ============================================================

USE logix;


-- ============================================================
-- Q71. Rank Customers by Revenue
-- ============================================================

WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.customer_segment,
        ROUND(SUM(oi.line_total), 2) AS total_revenue
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
    total_revenue,
    DENSE_RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM customer_revenue
ORDER BY revenue_rank
LIMIT 20;


-- ============================================================
-- Q72. Rank Products Within Each Category
-- ============================================================

WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(oi.line_total), 2) AS total_revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,
    total_revenue,
    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS category_rank
FROM product_sales
ORDER BY category, category_rank;


-- ============================================================
-- Q73. Monthly Running Revenue
-- ============================================================

WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)

SELECT
    month,
    ROUND(revenue, 2) AS monthly_revenue,
    ROUND(
        SUM(revenue) OVER (
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cumulative_revenue
FROM monthly_revenue
ORDER BY month;


-- ============================================================
-- Q74. Month-over-Month Revenue Change
-- ============================================================

WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
),

revenue_comparison AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_revenue
    FROM monthly_revenue
)

SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        revenue - previous_revenue,
        2
    ) AS revenue_change,
    ROUND(
        100 * (revenue - previous_revenue)
        / NULLIF(previous_revenue, 0),
        2
    ) AS growth_percent
FROM revenue_comparison
ORDER BY month;


-- ============================================================
-- Q75. Top 3 Products in Each Category
-- ============================================================

WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.line_total), 2) AS total_revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
),

ranked_products AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS product_rank
    FROM product_sales
)

SELECT
    product_id,
    product_name,
    category,
    units_sold,
    total_revenue,
    product_rank
FROM ranked_products
WHERE product_rank <= 3
ORDER BY category, product_rank;


-- ============================================================
-- Q76. Warehouse Performance Ranking
-- ============================================================

WITH warehouse_performance AS (
    SELECT
        w.warehouse_id,
        w.warehouse_name,
        COUNT(s.shipment_id) AS total_shipments,
        ROUND(SUM(s.shipping_cost), 2) AS total_cost,
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
)

SELECT
    warehouse_id,
    warehouse_name,
    total_shipments,
    total_cost,
    on_time_rate,
    DENSE_RANK() OVER (
        ORDER BY on_time_rate DESC
    ) AS warehouse_rank
FROM warehouse_performance
ORDER BY warehouse_rank;


-- ============================================================
-- Q77. Customer Revenue Quartiles
-- ============================================================

WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        ROUND(SUM(oi.line_total), 2) AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    GROUP BY
        c.customer_id,
        c.customer_name
)

SELECT
    customer_id,
    customer_name,
    total_revenue,
    NTILE(4) OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_quartile
FROM customer_revenue
ORDER BY revenue_quartile, total_revenue DESC;


-- ============================================================
-- Q78. Monthly Orders with Previous Month Comparison
-- ============================================================

WITH monthly_orders AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        COUNT(*) AS total_orders
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)

SELECT
    month,
    total_orders,
    LAG(total_orders) OVER (
        ORDER BY month
    ) AS previous_month_orders,
    total_orders
        - LAG(total_orders) OVER (
            ORDER BY month
        ) AS order_change
FROM monthly_orders
ORDER BY month;


-- ============================================================
-- Q79. Delivery Partner Ranking by On-Time Rate
-- ============================================================

WITH partner_performance AS (
    SELECT
        dp.partner_id,
        dp.partner_name,
        COUNT(s.shipment_id) AS total_shipments,
        SUM(
            CASE
                WHEN s.actual_delivery_date IS NOT NULL
                 AND s.actual_delivery_date <= s.expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) AS on_time_shipments
    FROM delivery_partners dp
    JOIN shipments s
        ON dp.partner_id = s.delivery_partner_id
    GROUP BY
        dp.partner_id,
        dp.partner_name
)

SELECT
    partner_id,
    partner_name,
    total_shipments,
    on_time_shipments,
    ROUND(
        100 * on_time_shipments
        / NULLIF(total_shipments, 0),
        2
    ) AS on_time_rate,
    DENSE_RANK() OVER (
        ORDER BY
            100 * on_time_shipments
            / NULLIF(total_shipments, 0) DESC
    ) AS partner_rank
FROM partner_performance
ORDER BY partner_rank;


-- ============================================================
-- Q80. Revenue Contribution Percentage by Category
-- ============================================================

WITH category_revenue AS (
    SELECT
        p.category,
        SUM(oi.line_total) AS revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.category
)

SELECT
    category,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100 * revenue / SUM(revenue) OVER (),
        2
    ) AS revenue_contribution_percent
FROM category_revenue
ORDER BY revenue DESC;