-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_customer_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_customer_analysis` AS select `c`.`customer_id` AS `customer_id`,`c`.`customer_name` AS `customer_name`,`c`.`customer_segment` AS `customer_segment`,`c`.`state` AS `state`,`c`.`city` AS `city`,count(distinct `o`.`order_id`) AS `total_orders`,round(sum(`oi`.`line_total`),2) AS `total_revenue`,round((sum(`oi`.`line_total`) / count(distinct `o`.`order_id`)),2) AS `average_order_value`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `latest_order_date` from ((`customers` `c` join `orders` `o` on((`c`.`customer_id` = `o`.`customer_id`))) join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by `c`.`customer_id`,`c`.`customer_name`,`c`.`customer_segment`,`c`.`state`,`c`.`city`;

