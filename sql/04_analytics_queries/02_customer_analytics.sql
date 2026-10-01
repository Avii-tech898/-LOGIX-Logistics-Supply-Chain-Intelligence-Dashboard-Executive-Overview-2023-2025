-- ============================================================
-- LOGIX - Customer Analytics
-- Query Level: 02
-- Queries: 11 - 20
-- ============================================================

USE logix;


-- ============================================================
-- Q11. Customers by Segment
-- ============================================================

SELECT
    customer_segment,
    COUNT(*) AS total_customers
FROM customers
GROUP BY customer_segment
ORDER BY total_customers DESC;


-- ============================================================
-- Q12. Active vs Inactive Customers
-- ============================================================

SELECT
    is_active,
    COUNT(*) AS total_customers
FROM customers
GROUP BY is_active
ORDER BY is_active DESC;


-- ============================================================
-- Q13. Customers by State
-- ============================================================

SELECT
    state,
    COUNT(*) AS total_customers
FROM customers
GROUP BY state
ORDER BY total_customers DESC;


-- ============================================================
-- Q14. Customers by City
-- ============================================================

SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC
LIMIT 20;


-- ============================================================
-- Q15. Revenue by Customer Segment
-- ============================================================

SELECT
    c.customer_segment,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_segment
ORDER BY total_revenue DESC;


-- ============================================================
-- Q16. Orders by Customer Segment
-- ============================================================

SELECT
    c.customer_segment,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_segment
ORDER BY total_orders DESC;


-- ============================================================
-- Q17. Average Order Value by Customer Segment
-- ============================================================

SELECT
    c.customer_segment,
    ROUND(
        SUM(oi.line_total) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_segment
ORDER BY average_order_value DESC;


-- ============================================================
-- Q18. Top 10 Customers by Revenue
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
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
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- Q19. Top 10 Customers by Number of Orders
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment
ORDER BY total_orders DESC
LIMIT 10;


-- ============================================================
-- Q20. Customer Lifetime Value
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.line_total), 2) AS lifetime_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment
ORDER BY lifetime_value DESC
LIMIT 20;