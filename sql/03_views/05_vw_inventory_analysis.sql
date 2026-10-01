-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_inventory_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_inventory_analysis` AS select `i`.`inventory_id` AS `inventory_id`,`i`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `warehouse_city`,`i`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`i`.`opening_stock` AS `opening_stock`,`i`.`current_stock` AS `current_stock`,`i`.`reorder_level` AS `reorder_level`,`i`.`unit_cost` AS `unit_cost`,`i`.`inventory_value` AS `inventory_value`,`i`.`stock_status` AS `stock_status`,`i`.`last_restock_date` AS `last_restock_date` from ((`inventory` `i` join `warehouses` `w` on((`i`.`warehouse_id` = `w`.`warehouse_id`))) join `products` `p` on((`i`.`product_id` = `p`.`product_id`)));

