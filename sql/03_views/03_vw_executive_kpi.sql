-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_executive_kpi`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_executive_kpi` AS select (select count(0) from `orders`) AS `total_orders`,(select count(0) from `customers`) AS `total_customers`,(select round(sum(`order_items`.`line_total`),2) from `order_items`) AS `total_revenue`,(select round(sum(`shipments`.`shipping_cost`),2) from `shipments`) AS `total_logistics_cost`,(select count(0) from `shipments` where (`shipments`.`shipment_status` = 'Failed')) AS `failed_shipments`,(select count(0) from `returns`) AS `total_returns`,(select round(sum(`returns`.`refund_amount`),2) from `returns`) AS `total_refunds`,(select round(((100.0 * sum((case when (`shipments`.`actual_delivery_date` <= `shipments`.`expected_delivery_date`) then 1 else 0 end))) / count(0)),2) from `shipments` where (`shipments`.`actual_delivery_date` is not null)) AS `on_time_rate`;

