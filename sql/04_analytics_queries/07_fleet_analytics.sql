-- ============================================================
-- LOGIX - Fleet & Driver Analytics
-- Query Level: 07
-- Queries: 61 - 70
-- ============================================================

USE logix;


-- ============================================================
-- Q61. Vehicle Status Distribution
-- ============================================================

SELECT
    status,
    COUNT(*) AS total_vehicles
FROM vehicles
GROUP BY status
ORDER BY total_vehicles DESC;


-- ============================================================
-- Q62. Vehicle Type Distribution
-- ============================================================

SELECT
    vehicle_type,
    COUNT(*) AS total_vehicles,
    ROUND(AVG(capacity_kg), 2) AS average_capacity_kg
FROM vehicles
GROUP BY vehicle_type
ORDER BY total_vehicles DESC;


-- ============================================================
-- Q63. Fuel Type Distribution
-- ============================================================

SELECT
    fuel_type,
    COUNT(*) AS total_vehicles
FROM vehicles
GROUP BY fuel_type
ORDER BY total_vehicles DESC;


-- ============================================================
-- Q64. Driver Employment Type
-- ============================================================

SELECT
    employment_type,
    COUNT(*) AS total_drivers,
    ROUND(AVG(experience_years), 2) AS average_experience_years,
    ROUND(AVG(rating), 2) AS average_rating
FROM drivers
GROUP BY employment_type
ORDER BY total_drivers DESC;


-- ============================================================
-- Q65. Driver Performance
-- ============================================================

SELECT
    d.driver_id,
    d.driver_name,
    d.experience_years,
    d.rating,
    d.status,
    COUNT(v.vehicle_id) AS assigned_vehicles
FROM drivers d
LEFT JOIN vehicles v
    ON d.driver_id = v.driver_id
GROUP BY
    d.driver_id,
    d.driver_name,
    d.experience_years,
    d.rating,
    d.status
ORDER BY d.rating DESC, d.experience_years DESC
LIMIT 20;


-- ============================================================
-- Q66. Driver Rating Distribution
-- ============================================================

SELECT
    CASE
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 4.0 THEN 'Good'
        WHEN rating >= 3.0 THEN 'Average'
        ELSE 'Needs Improvement'
    END AS rating_category,
    COUNT(*) AS total_drivers
FROM drivers
GROUP BY
    CASE
        WHEN rating >= 4.5 THEN 'Excellent'
        WHEN rating >= 4.0 THEN 'Good'
        WHEN rating >= 3.0 THEN 'Average'
        ELSE 'Needs Improvement'
    END
ORDER BY total_drivers DESC;


-- ============================================================
-- Q67. Vehicles Assigned to Drivers
-- ============================================================

SELECT
    d.driver_id,
    d.driver_name,
    COUNT(v.vehicle_id) AS total_vehicles,
    GROUP_CONCAT(
        v.vehicle_number
        ORDER BY v.vehicle_number
        SEPARATOR ', '
    ) AS vehicle_numbers
FROM drivers d
LEFT JOIN vehicles v
    ON d.driver_id = v.driver_id
GROUP BY
    d.driver_id,
    d.driver_name
ORDER BY total_vehicles DESC;


-- ============================================================
-- Q68. Driver & Vehicle Capacity Analysis
-- ============================================================

SELECT
    d.driver_id,
    d.driver_name,
    d.experience_years,
    d.rating,
    COUNT(v.vehicle_id) AS total_vehicles,
    ROUND(SUM(v.capacity_kg), 2) AS total_capacity_kg,
    ROUND(AVG(v.capacity_kg), 2) AS average_capacity_kg
FROM drivers d
LEFT JOIN vehicles v
    ON d.driver_id = v.driver_id
GROUP BY
    d.driver_id,
    d.driver_name,
    d.experience_years,
    d.rating
ORDER BY total_capacity_kg DESC;


-- ============================================================
-- Q69. Vehicle Model Year Analysis
-- ============================================================

SELECT
    model_year,
    COUNT(*) AS total_vehicles,
    ROUND(AVG(capacity_kg), 2) AS average_capacity_kg
FROM vehicles
GROUP BY model_year
ORDER BY model_year DESC;


-- ============================================================
-- Q70. Driver Experience & Rating Analysis
-- ============================================================

SELECT
    CASE
        WHEN experience_years < 2 THEN '0-1 Years'
        WHEN experience_years < 5 THEN '2-4 Years'
        WHEN experience_years < 10 THEN '5-9 Years'
        ELSE '10+ Years'
    END AS experience_group,
    COUNT(*) AS total_drivers,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(AVG(experience_years), 2) AS average_experience
FROM drivers
GROUP BY
    CASE
        WHEN experience_years < 2 THEN '0-1 Years'
        WHEN experience_years < 5 THEN '2-4 Years'
        WHEN experience_years < 10 THEN '5-9 Years'
        ELSE '10+ Years'
    END
ORDER BY average_experience;