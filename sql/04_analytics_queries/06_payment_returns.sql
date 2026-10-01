-- ============================================================
-- LOGIX - Payment & Returns Analytics
-- Query Level: 06
-- Queries: 51 - 60
-- ============================================================

USE logix;


-- ============================================================
-- Q51. Payment Method Distribution
-- ============================================================

SELECT
    payment_method,
    COUNT(*) AS total_payments,
    ROUND(SUM(amount), 2) AS total_payment_value
FROM payments
GROUP BY payment_method
ORDER BY total_payment_value DESC;


-- ============================================================
-- Q52. Payment Status Distribution
-- ============================================================

SELECT
    payment_status,
    COUNT(*) AS total_payments,
    ROUND(SUM(amount), 2) AS total_amount
FROM payments
GROUP BY payment_status
ORDER BY total_payments DESC;


-- ============================================================
-- Q53. Successful Payment Rate
-- ============================================================

SELECT
    COUNT(*) AS total_payments,
    SUM(
        CASE
            WHEN payment_status = 'Paid'
            THEN 1
            ELSE 0
        END
    ) AS successful_payments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN payment_status = 'Paid'
                THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS successful_payment_rate
FROM payments;


-- ============================================================
-- Q54. Payment Value by Payment Method
-- ============================================================

SELECT
    payment_method,
    ROUND(SUM(amount), 2) AS total_payment_value,
    ROUND(AVG(amount), 2) AS average_payment_value
FROM payments
GROUP BY payment_method
ORDER BY total_payment_value DESC;


-- ============================================================
-- Q55. Refund Value by Payment Status
-- ============================================================

SELECT
    payment_status,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount), 2) AS total_amount
FROM payments
WHERE payment_status = 'Refunded'
GROUP BY payment_status;


-- ============================================================
-- Q56. Return Status Distribution
-- ============================================================

SELECT
    return_status,
    COUNT(*) AS total_returns,
    ROUND(SUM(return_amount), 2) AS return_value,
    ROUND(SUM(refund_amount), 2) AS refund_value
FROM returns
GROUP BY return_status
ORDER BY total_returns DESC;


-- ============================================================
-- Q57. Return Reason Analysis
-- ============================================================

SELECT
    return_reason,
    COUNT(*) AS total_returns,
    SUM(return_quantity) AS returned_units,
    ROUND(SUM(return_amount), 2) AS return_value,
    ROUND(SUM(refund_amount), 2) AS refund_value
FROM returns
GROUP BY return_reason
ORDER BY total_returns DESC;


-- ============================================================
-- Q58. Return Rate by Product Category
-- ============================================================

SELECT
    p.category,
    COUNT(DISTINCT r.return_id) AS total_returns,
    SUM(r.return_quantity) AS returned_units,
    ROUND(SUM(r.return_amount), 2) AS return_value
FROM returns r
JOIN products p
    ON r.product_id = p.product_id
GROUP BY p.category
ORDER BY total_returns DESC;


-- ============================================================
-- Q59. Top Products by Return Value
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(r.return_id) AS total_returns,
    SUM(r.return_quantity) AS returned_units,
    ROUND(SUM(r.return_amount), 2) AS return_value,
    ROUND(SUM(r.refund_amount), 2) AS refund_value
FROM returns r
JOIN products p
    ON r.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY return_value DESC
LIMIT 20;


-- ============================================================
-- Q60. Monthly Returns & Refunds
-- ============================================================

SELECT
    DATE_FORMAT(return_date, '%Y-%m') AS month,
    COUNT(*) AS total_returns,
    SUM(return_quantity) AS returned_units,
    ROUND(SUM(return_amount), 2) AS return_value,
    ROUND(SUM(refund_amount), 2) AS refund_value
FROM returns
GROUP BY DATE_FORMAT(return_date, '%Y-%m')
ORDER BY month;