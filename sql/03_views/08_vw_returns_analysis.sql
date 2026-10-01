-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_returns_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_returns_analysis` AS select `r`.`return_id` AS `return_id`,`r`.`order_id` AS `order_id`,`r`.`order_item_id` AS `order_item_id`,`r`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`r`.`return_date` AS `return_date`,`r`.`return_quantity` AS `return_quantity`,`r`.`return_reason` AS `return_reason`,`r`.`return_status` AS `return_status`,`r`.`return_amount` AS `return_amount`,`r`.`refund_amount` AS `refund_amount` from (`returns` `r` join `products` `p` on((`r`.`product_id` = `p`.`product_id`)));

