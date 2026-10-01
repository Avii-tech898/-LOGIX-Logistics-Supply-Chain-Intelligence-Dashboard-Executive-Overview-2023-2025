-- ============================================================
-- LOGIX - Delivery & Logistics Analytics
-- Query Level: 04
-- Queries: 31 - 40
-- ============================================================

USE logix;


-- ============================================================
-- Q31. Shipment Status Distribution
-- ============================================================

SELECT
    shipment_status,
    COUNT(*) AS total_shipments
FROM shipments
GROUP BY shipment_status
ORDER BY total_shipments DESC;


-- ============================================================
-- Q32. Delivery Type Performance
-- ============================================================

SELECT
    delivery_type,
    COUNT(*) AS total_shipments,
    SUM(
        CASE
            WHEN shipment_status = 'Delivered'
            THEN 1
            ELSE 0
        END
    ) AS delivered_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN shipment_status = 'Delivered'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS delivery_success_rate
FROM shipments
GROUP BY delivery_type
ORDER BY delivery_success_rate DESC;


-- ============================================================
-- Q33. On-Time vs Delayed Shipments
-- ============================================================

SELECT
    CASE
        WHEN actual_delivery_date IS NULL THEN 'Not Delivered'
        WHEN actual_delivery_date <= expected_delivery_date
            THEN 'On Time'
        ELSE 'Delayed'
    END AS delivery_performance,
    COUNT(*) AS total_shipments
FROM shipments
GROUP BY
    CASE
        WHEN actual_delivery_date IS NULL THEN 'Not Delivered'
        WHEN actual_delivery_date <= expected_delivery_date
            THEN 'On Time'
        ELSE 'Delayed'
    END
ORDER BY total_shipments DESC;


-- ============================================================
-- Q34. Average Delivery Time by Delivery Type
-- ============================================================

SELECT
    delivery_type,
    ROUND(
        AVG(
            DATEDIFF(
                actual_delivery_date,
                shipment_date
            )
        ),
        2
    ) AS average_delivery_days
FROM shipments
WHERE actual_delivery_date IS NOT NULL
GROUP BY delivery_type
ORDER BY average_delivery_days;


-- ============================================================
-- Q35. Average Delivery Distance by Delivery Type
-- ============================================================

SELECT
    delivery_type,
    ROUND(AVG(distance_km), 2) AS average_distance_km,
    ROUND(SUM(distance_km), 2) AS total_distance_km
FROM shipments
GROUP BY delivery_type
ORDER BY average_distance_km DESC;


-- ============================================================
-- Q36. Shipping Cost by Delivery Type
-- ============================================================

SELECT
    delivery_type,
    COUNT(*) AS total_shipments,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
    ROUND(AVG(shipping_cost), 2) AS average_shipping_cost
FROM shipments
GROUP BY delivery_type
ORDER BY total_shipping_cost DESC;


-- ============================================================
-- Q37. Cost per Kilometer
-- ============================================================

SELECT
    delivery_type,
    ROUND(
        SUM(shipping_cost) / NULLIF(SUM(distance_km), 0),
        2
    ) AS cost_per_km
FROM shipments
GROUP BY delivery_type
ORDER BY cost_per_km DESC;


-- ============================================================
-- Q38. Delivery Partner Performance
-- ============================================================

SELECT
    dp.partner_id,
    dp.partner_name,
    COUNT(s.shipment_id) AS total_shipments,
    SUM(
        CASE
            WHEN s.shipment_status = 'Delivered'
            THEN 1
            ELSE 0
        END
    ) AS delivered_shipments,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN s.actual_delivery_date IS NOT NULL
                 AND s.actual_delivery_date <= s.expected_delivery_date
                THEN 1
                ELSE 0
            END
        ) / COUNT(s.shipment_id),
        2
    ) AS on_time_rate,
    ROUND(SUM(s.shipping_cost), 2) AS total_shipping_cost
FROM delivery_partners dp
JOIN shipments s
    ON dp.partner_id = s.delivery_partner_id
GROUP BY
    dp.partner_id,
    dp.partner_name
ORDER BY on_time_rate DESC;


-- ============================================================
-- Q39. Failed Delivery Analysis
-- ============================================================

SELECT
    da.failure_reason,
    COUNT(*) AS total_failures
FROM delivery_attempts da
WHERE da.attempt_outcome <> 'Delivered'
GROUP BY da.failure_reason
ORDER BY total_failures DESC;


-- ============================================================
-- Q40. Delivery Attempts per Shipment
-- ============================================================

SELECT
    da.shipment_id,
    COUNT(*) AS total_attempts,
    MAX(da.attempt_number) AS maximum_attempt_number,
    SUM(
        CASE
            WHEN da.attempt_outcome = 'Delivered'
            THEN 1
            ELSE 0
        END
    ) AS successful_attempts
FROM delivery_attempts da
GROUP BY da.shipment_id
ORDER BY total_attempts DESC
LIMIT 20;