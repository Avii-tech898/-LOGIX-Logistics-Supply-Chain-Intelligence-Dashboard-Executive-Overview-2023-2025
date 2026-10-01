-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_warehouse_performance`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_warehouse_performance` AS select `w`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `city`,`w`.`state` AS `state`,count(`s`.`shipment_id`) AS `total_shipments`,round(sum(`s`.`shipping_cost`),2) AS `total_shipping_cost`,round(avg(`s`.`distance_km`),2) AS `average_distance_km`,round(((100.0 * sum((case when (`s`.`actual_delivery_date` <= `s`.`expected_delivery_date`) then 1 else 0 end))) / count(`s`.`shipment_id`)),2) AS `on_time_rate` from (`warehouses` `w` left join `shipments` `s` on((`w`.`warehouse_id` = `s`.`warehouse_id`))) group by `w`.`warehouse_id`,`w`.`warehouse_name`,`w`.`city`,`w`.`state`;

