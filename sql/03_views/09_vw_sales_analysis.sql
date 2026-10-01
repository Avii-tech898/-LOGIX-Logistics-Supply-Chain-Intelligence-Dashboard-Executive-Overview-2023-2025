-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_sales_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_sales_analysis` AS select `o`.`order_id` AS `order_id`,`o`.`order_date` AS `order_date`,`o`.`customer_id` AS `customer_id`,`c`.`customer_segment` AS `customer_segment`,`c`.`state` AS `customer_state`,`c`.`city` AS `customer_city`,`oi`.`order_item_id` AS `order_item_id`,`oi`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`oi`.`quantity` AS `quantity`,`oi`.`unit_price` AS `unit_price`,`oi`.`discount_percent` AS `discount_percent`,`oi`.`discount_amount` AS `discount_amount`,`oi`.`line_total` AS `line_total` from (((`orders` `o` join `customers` `c` on((`o`.`customer_id` = `c`.`customer_id`))) join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) join `products` `p` on((`oi`.`product_id` = `p`.`product_id`)));

