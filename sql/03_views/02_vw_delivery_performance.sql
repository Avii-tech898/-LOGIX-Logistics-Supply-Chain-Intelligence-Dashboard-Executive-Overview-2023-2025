-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_delivery_performance`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_delivery_performance` AS select `s`.`shipment_id` AS `shipment_id`,`s`.`order_id` AS `order_id`,`s`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `warehouse_city`,`s`.`delivery_partner_id` AS `delivery_partner_id`,`dp`.`partner_name` AS `partner_name`,`s`.`shipment_date` AS `shipment_date`,`s`.`expected_delivery_date` AS `expected_delivery_date`,`s`.`actual_delivery_date` AS `actual_delivery_date`,`s`.`delivery_type` AS `delivery_type`,`s`.`shipment_status` AS `shipment_status`,`s`.`sla_days` AS `sla_days`,`s`.`shipping_cost` AS `shipping_cost`,`s`.`distance_km` AS `distance_km`,(case when (`s`.`actual_delivery_date` is null) then 'Not Delivered' when (`s`.`actual_delivery_date` <= `s`.`expected_delivery_date`) then 'On Time' else 'Late' end) AS `delivery_performance`,(case when (`s`.`actual_delivery_date` is not null) then (to_days(`s`.`actual_delivery_date`) - to_days(`s`.`shipment_date`)) else NULL end) AS `delivery_days` from ((`shipments` `s` join `warehouses` `w` on((`s`.`warehouse_id` = `w`.`warehouse_id`))) join `delivery_partners` `dp` on((`s`.`delivery_partner_id` = `dp`.`partner_id`)));

