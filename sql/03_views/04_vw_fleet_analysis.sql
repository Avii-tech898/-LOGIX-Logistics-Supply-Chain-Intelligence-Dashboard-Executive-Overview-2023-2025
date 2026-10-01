-- ============================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- Analytical View
-- ============================================================

USE logix;

DROP VIEW IF EXISTS `vw_fleet_analysis`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_fleet_analysis` AS select `v`.`vehicle_id` AS `vehicle_id`,`v`.`vehicle_number` AS `vehicle_number`,`v`.`vehicle_type` AS `vehicle_type`,`v`.`capacity_kg` AS `capacity_kg`,`v`.`fuel_type` AS `fuel_type`,`v`.`model_year` AS `model_year`,`v`.`status` AS `vehicle_status`,`d`.`driver_id` AS `driver_id`,`d`.`driver_name` AS `driver_name`,`d`.`experience_years` AS `experience_years`,`d`.`rating` AS `driver_rating`,`d`.`employment_type` AS `employment_type`,`d`.`status` AS `driver_status` from (`vehicles` `v` left join `drivers` `d` on((`v`.`driver_id` = `d`.`driver_id`)));

