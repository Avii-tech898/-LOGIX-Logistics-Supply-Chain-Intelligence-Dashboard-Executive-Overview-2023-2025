-- ============================================================
-- LOGIX - Sales & Revenue Analytics
-- Query Level: 03
-- Queries: 21 - 30
-- ============================================================

USE logix;


-- ============================================================
-- Q21. Total Revenue by Year
-- ============================================================

SELECT
    YEAR(o.order_date) AS order_year,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_date)
ORDER BY order_year;


-- ============================================================
-- Q22. Total Revenue by Month
-- ============================================================

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;


-- ============================================================
-- Q23. Revenue by Delivery Type
-- ============================================================

SELECT
    o.delivery_type,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.delivery_type
ORDER BY total_revenue DESC;


-- ============================================================
-- Q24. Revenue by Order Status
-- ============================================================

SELECT
    o.order_status,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY o.order_status
ORDER BY total_revenue DESC;


-- ============================================================
-- Q25. Revenue by Product Category
-- ============================================================

SELECT
    p.category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================================
-- Q26. Top 20 Products by Revenue
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY total_revenue DESC
LIMIT 20;


-- ============================================================
-- Q27. Top 20 Products by Units Sold
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY units_sold DESC
LIMIT 20;


-- ============================================================
-- Q28. Average Selling Price by Category
-- ============================================================

SELECT
    p.category,
    ROUND(AVG(oi.unit_price), 2) AS average_selling_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY average_selling_price DESC;


-- ============================================================
-- Q29. Discount Analysis by Category
-- ============================================================

SELECT
    p.category,
    ROUND(SUM(oi.discount_amount), 2) AS total_discount,
    ROUND(AVG(oi.discount_percent), 2) AS average_discount_percent,
    ROUND(SUM(oi.line_total), 2) AS net_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_discount DESC;


-- ============================================================
-- Q30. Monthly Sales Growth
-- ============================================================

WITH monthly_sales AS (
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
    ROUND(revenue, 2) AS revenue,
    ROUND(
        LAG(revenue) OVER (ORDER BY month),
        2
    ) AS previous_month_revenue,
    ROUND(
        (
            (revenue - LAG(revenue) OVER (ORDER BY month))
            / NULLIF(LAG(revenue) OVER (ORDER BY month), 0)
        ) * 100,
        2
    ) AS growth_percent
FROM monthly_sales
ORDER BY month;