-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_payment_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_payment_analysis` AS select `p`.`payment_id` AS `payment_id`,`p`.`order_id` AS `order_id`,`p`.`payment_date` AS `payment_date`,`p`.`payment_method` AS `payment_method`,`p`.`payment_status` AS `payment_status`,`p`.`amount` AS `amount`,`p`.`transaction_reference` AS `transaction_reference`,`o`.`customer_id` AS `customer_id`,`o`.`order_date` AS `order_date`,`o`.`order_status` AS `order_status` from (`payments` `p` join `orders` `o` on((`p`.`order_id` = `o`.`order_id`)));

