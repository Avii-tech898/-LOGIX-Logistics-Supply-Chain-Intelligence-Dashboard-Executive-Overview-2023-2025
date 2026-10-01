-- ============================================================
-- LOGIX - Basic Business Analytics
-- Query Level: 01
-- Queries: 01 - 10
-- ============================================================

USE logix;


-- ============================================================
-- Q01. Total Orders
-- ============================================================

SELECT
    COUNT(*) AS total_orders
FROM orders;


-- ============================================================
-- Q02. Total Customers
-- ============================================================

SELECT
    COUNT(*) AS total_customers
FROM customers;


-- ============================================================
-- Q03. Total Products
-- ============================================================

SELECT
    COUNT(*) AS total_products
FROM products;


-- ============================================================
-- Q04. Total Revenue
-- ============================================================

SELECT
    ROUND(SUM(line_total), 2) AS total_revenue
FROM order_items;


-- ============================================================
-- Q05. Total Logistics Cost
-- ============================================================

SELECT
    ROUND(SUM(shipping_cost), 2) AS total_logistics_cost
FROM shipments;


-- ============================================================
-- Q06. Average Order Value
-- ============================================================

SELECT
    ROUND(
        SUM(line_total) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM order_items;


-- ============================================================
-- Q07. Orders by Status
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- ============================================================
-- Q08. Orders by Delivery Type
-- ============================================================

SELECT
    delivery_type,
    COUNT(*) AS total_orders
FROM orders
GROUP BY delivery_type
ORDER BY total_orders DESC;


-- ============================================================
-- Q09. Revenue by Product Category
-- ============================================================

SELECT
    p.category,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================================
-- Q10. Monthly Revenue
-- ============================================================

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.line_total), 2) AS total_revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;