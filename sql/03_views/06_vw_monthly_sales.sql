-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_monthly_sales`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_monthly_sales` AS select date_format(`o`.`order_date`,'%Y-%m') AS `order_month`,count(distinct `o`.`order_id`) AS `total_orders`,count(distinct `o`.`customer_id`) AS `unique_customers`,round(sum(`oi`.`line_total`),2) AS `revenue`,round((sum(`oi`.`line_total`) / count(distinct `o`.`order_id`)),2) AS `average_order_value` from (`orders` `o` join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by date_format(`o`.`order_date`,'%Y-%m');

