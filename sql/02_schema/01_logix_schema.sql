-- =========================================================
-- LOGIX - Logistics & Supply Chain Intelligence Platform
-- MySQL Database Schema
-- Generated automatically from the existing database
-- =========================================================

CREATE DATABASE IF NOT EXISTS logix
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE logix;


-- =========================================================
-- TABLE: addresses
-- =========================================================

CREATE TABLE `addresses` (
  `address_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address_type` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address_line` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pincode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_default` tinyint(1) NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `fk_addresses_customer` (`customer_id`),
  CONSTRAINT `fk_addresses_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: customers
-- =========================================================

CREATE TABLE `customers` (
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `customer_segment` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registration_date` date NOT NULL,
  `state` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pincode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `preferred_payment_method` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: delivery_attempts
-- =========================================================

CREATE TABLE `delivery_attempts` (
  `attempt_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipment_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `attempt_number` int NOT NULL,
  `attempt_date` datetime NOT NULL,
  `attempt_outcome` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `failure_reason` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`attempt_id`),
  UNIQUE KEY `uq_shipment_attempt` (`shipment_id`,`attempt_number`),
  KEY `idx_attempts_shipment` (`shipment_id`),
  KEY `idx_attempts_order` (`order_id`),
  KEY `idx_attempts_outcome` (`attempt_outcome`),
  CONSTRAINT `fk_attempts_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `fk_attempts_shipment` FOREIGN KEY (`shipment_id`) REFERENCES `shipments` (`shipment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: delivery_partners
-- =========================================================

CREATE TABLE `delivery_partners` (
  `partner_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `partner_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `service_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coverage_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `base_cost_per_km` decimal(10,2) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `contact_phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`partner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: drivers
-- =========================================================

CREATE TABLE `drivers` (
  `driver_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `driver_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `license_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `experience_years` int DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `employment_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`driver_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: inventory
-- =========================================================

CREATE TABLE `inventory` (
  `inventory_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `warehouse_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `opening_stock` int NOT NULL,
  `current_stock` int NOT NULL,
  `reorder_level` int NOT NULL,
  `unit_cost` decimal(15,2) NOT NULL,
  `inventory_value` decimal(18,2) NOT NULL,
  `stock_status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_restock_date` date DEFAULT NULL,
  PRIMARY KEY (`inventory_id`),
  KEY `fk_inventory_warehouse` (`warehouse_id`),
  KEY `fk_inventory_product` (`product_id`),
  CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  CONSTRAINT `fk_inventory_warehouse` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouses` (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: order_items
-- =========================================================

CREATE TABLE `order_items` (
  `order_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(15,2) NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `discount_amount` decimal(15,2) NOT NULL,
  `line_total` decimal(18,2) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `idx_order_items_order` (`order_id`),
  KEY `idx_order_items_product` (`product_id`),
  CONSTRAINT `fk_order_items_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `fk_order_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: orders
-- =========================================================

CREATE TABLE `orders` (
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_date` datetime NOT NULL,
  `expected_delivery_date` datetime NOT NULL,
  `delivery_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `priority` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `fk_orders_address` (`address_id`),
  KEY `idx_orders_customer` (`customer_id`),
  KEY `idx_orders_date` (`order_date`),
  KEY `idx_orders_status` (`order_status`),
  CONSTRAINT `fk_orders_address` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`),
  CONSTRAINT `fk_orders_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: payments
-- =========================================================

CREATE TABLE `payments` (
  `payment_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_date` datetime NOT NULL,
  `payment_method` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(18,2) NOT NULL,
  `transaction_reference` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE KEY `uq_payment_order` (`order_id`),
  UNIQUE KEY `uq_transaction_reference` (`transaction_reference`),
  KEY `idx_payments_date` (`payment_date`),
  KEY `idx_payments_status` (`payment_status`),
  CONSTRAINT `fk_payments_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: products
-- =========================================================

CREATE TABLE `products` (
  `product_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `brand` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_price` decimal(15,2) NOT NULL,
  `weight_kg` decimal(10,3) DEFAULT NULL,
  `supplier` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reorder_level` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: returns
-- =========================================================

CREATE TABLE `returns` (
  `return_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_item_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_date` datetime NOT NULL,
  `return_quantity` int NOT NULL,
  `return_reason` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_amount` decimal(18,2) NOT NULL,
  `refund_amount` decimal(18,2) NOT NULL,
  PRIMARY KEY (`return_id`),
  UNIQUE KEY `uq_return_order_item` (`order_item_id`),
  KEY `idx_returns_order` (`order_id`),
  KEY `idx_returns_product` (`product_id`),
  KEY `idx_returns_status` (`return_status`),
  KEY `idx_returns_date` (`return_date`),
  CONSTRAINT `fk_returns_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `fk_returns_order_item` FOREIGN KEY (`order_item_id`) REFERENCES `order_items` (`order_item_id`),
  CONSTRAINT `fk_returns_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: shipments
-- =========================================================

CREATE TABLE `shipments` (
  `shipment_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `warehouse_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `delivery_partner_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipment_date` datetime NOT NULL,
  `expected_delivery_date` datetime NOT NULL,
  `actual_delivery_date` datetime DEFAULT NULL,
  `delivery_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipment_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sla_days` int NOT NULL,
  `shipping_cost` decimal(18,2) NOT NULL,
  `distance_km` decimal(12,2) NOT NULL,
  PRIMARY KEY (`shipment_id`),
  UNIQUE KEY `uq_shipments_order` (`order_id`),
  KEY `idx_shipments_status` (`shipment_status`),
  KEY `idx_shipments_date` (`shipment_date`),
  KEY `idx_shipments_warehouse` (`warehouse_id`),
  KEY `idx_shipments_partner` (`delivery_partner_id`),
  CONSTRAINT `fk_shipments_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `fk_shipments_partner` FOREIGN KEY (`delivery_partner_id`) REFERENCES `delivery_partners` (`partner_id`),
  CONSTRAINT `fk_shipments_warehouse` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouses` (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: vehicles
-- =========================================================

CREATE TABLE `vehicles` (
  `vehicle_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `vehicle_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `vehicle_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacity_kg` decimal(10,2) DEFAULT NULL,
  `fuel_type` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `model_year` int DEFAULT NULL,
  `driver_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`),
  KEY `fk_vehicles_driver` (`driver_id`),
  CONSTRAINT `fk_vehicles_driver` FOREIGN KEY (`driver_id`) REFERENCES `drivers` (`driver_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- TABLE: warehouses
-- =========================================================

CREATE TABLE `warehouses` (
  `warehouse_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `warehouse_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `warehouse_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pincode` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `capacity_units` int DEFAULT NULL,
  `manager_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `operating_hours` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`warehouse_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =========================================================
-- FOREIGN KEY RELATIONSHIPS
-- =========================================================

-- addresses.customer_id -> customers.customer_id [fk_addresses_customer]
-- delivery_attempts.order_id -> orders.order_id [fk_attempts_order]
-- delivery_attempts.shipment_id -> shipments.shipment_id [fk_attempts_shipment]
-- inventory.product_id -> products.product_id [fk_inventory_product]
-- inventory.warehouse_id -> warehouses.warehouse_id [fk_inventory_warehouse]
-- order_items.order_id -> orders.order_id [fk_order_items_order]
-- order_items.product_id -> products.product_id [fk_order_items_product]
-- orders.address_id -> addresses.address_id [fk_orders_address]
-- orders.customer_id -> customers.customer_id [fk_orders_customer]
-- payments.order_id -> orders.order_id [fk_payments_order]
-- returns.order_id -> orders.order_id [fk_returns_order]
-- returns.order_item_id -> order_items.order_item_id [fk_returns_order_item]
-- returns.product_id -> products.product_id [fk_returns_product]
-- shipments.delivery_partner_id -> delivery_partners.partner_id [fk_shipments_partner]
-- shipments.order_id -> orders.order_id [fk_shipments_order]
-- shipments.warehouse_id -> warehouses.warehouse_id [fk_shipments_warehouse]
-- vehicles.driver_id -> drivers.driver_id [fk_vehicles_driver]

-- =========================================================
-- ANALYTICAL VIEWS
-- =========================================================


-- VIEW: vw_customer_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_customer_analysis` AS select `c`.`customer_id` AS `customer_id`,`c`.`customer_name` AS `customer_name`,`c`.`customer_segment` AS `customer_segment`,`c`.`state` AS `state`,`c`.`city` AS `city`,count(distinct `o`.`order_id`) AS `total_orders`,round(sum(`oi`.`line_total`),2) AS `total_revenue`,round((sum(`oi`.`line_total`) / count(distinct `o`.`order_id`)),2) AS `average_order_value`,min(`o`.`order_date`) AS `first_order_date`,max(`o`.`order_date`) AS `latest_order_date` from ((`customers` `c` join `orders` `o` on((`c`.`customer_id` = `o`.`customer_id`))) join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by `c`.`customer_id`,`c`.`customer_name`,`c`.`customer_segment`,`c`.`state`,`c`.`city`;


-- VIEW: vw_delivery_performance

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_delivery_performance` AS select `s`.`shipment_id` AS `shipment_id`,`s`.`order_id` AS `order_id`,`s`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `warehouse_city`,`s`.`delivery_partner_id` AS `delivery_partner_id`,`dp`.`partner_name` AS `partner_name`,`s`.`shipment_date` AS `shipment_date`,`s`.`expected_delivery_date` AS `expected_delivery_date`,`s`.`actual_delivery_date` AS `actual_delivery_date`,`s`.`delivery_type` AS `delivery_type`,`s`.`shipment_status` AS `shipment_status`,`s`.`sla_days` AS `sla_days`,`s`.`shipping_cost` AS `shipping_cost`,`s`.`distance_km` AS `distance_km`,(case when (`s`.`actual_delivery_date` is null) then 'Not Delivered' when (`s`.`actual_delivery_date` <= `s`.`expected_delivery_date`) then 'On Time' else 'Late' end) AS `delivery_performance`,(case when (`s`.`actual_delivery_date` is not null) then (to_days(`s`.`actual_delivery_date`) - to_days(`s`.`shipment_date`)) else NULL end) AS `delivery_days` from ((`shipments` `s` join `warehouses` `w` on((`s`.`warehouse_id` = `w`.`warehouse_id`))) join `delivery_partners` `dp` on((`s`.`delivery_partner_id` = `dp`.`partner_id`)));


-- VIEW: vw_executive_kpi

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_executive_kpi` AS select (select count(0) from `orders`) AS `total_orders`,(select count(0) from `customers`) AS `total_customers`,(select round(sum(`order_items`.`line_total`),2) from `order_items`) AS `total_revenue`,(select round(sum(`shipments`.`shipping_cost`),2) from `shipments`) AS `total_logistics_cost`,(select count(0) from `shipments` where (`shipments`.`shipment_status` = 'Failed')) AS `failed_shipments`,(select count(0) from `returns`) AS `total_returns`,(select round(sum(`returns`.`refund_amount`),2) from `returns`) AS `total_refunds`,(select round(((100.0 * sum((case when (`shipments`.`actual_delivery_date` <= `shipments`.`expected_delivery_date`) then 1 else 0 end))) / count(0)),2) from `shipments` where (`shipments`.`actual_delivery_date` is not null)) AS `on_time_rate`;


-- VIEW: vw_fleet_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_fleet_analysis` AS select `v`.`vehicle_id` AS `vehicle_id`,`v`.`vehicle_number` AS `vehicle_number`,`v`.`vehicle_type` AS `vehicle_type`,`v`.`capacity_kg` AS `capacity_kg`,`v`.`fuel_type` AS `fuel_type`,`v`.`model_year` AS `model_year`,`v`.`status` AS `vehicle_status`,`d`.`driver_id` AS `driver_id`,`d`.`driver_name` AS `driver_name`,`d`.`experience_years` AS `experience_years`,`d`.`rating` AS `driver_rating`,`d`.`employment_type` AS `employment_type`,`d`.`status` AS `driver_status` from (`vehicles` `v` left join `drivers` `d` on((`v`.`driver_id` = `d`.`driver_id`)));


-- VIEW: vw_inventory_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_inventory_analysis` AS select `i`.`inventory_id` AS `inventory_id`,`i`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `warehouse_city`,`i`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`i`.`opening_stock` AS `opening_stock`,`i`.`current_stock` AS `current_stock`,`i`.`reorder_level` AS `reorder_level`,`i`.`unit_cost` AS `unit_cost`,`i`.`inventory_value` AS `inventory_value`,`i`.`stock_status` AS `stock_status`,`i`.`last_restock_date` AS `last_restock_date` from ((`inventory` `i` join `warehouses` `w` on((`i`.`warehouse_id` = `w`.`warehouse_id`))) join `products` `p` on((`i`.`product_id` = `p`.`product_id`)));


-- VIEW: vw_monthly_sales

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_monthly_sales` AS select date_format(`o`.`order_date`,'%Y-%m') AS `order_month`,count(distinct `o`.`order_id`) AS `total_orders`,count(distinct `o`.`customer_id`) AS `unique_customers`,round(sum(`oi`.`line_total`),2) AS `revenue`,round((sum(`oi`.`line_total`) / count(distinct `o`.`order_id`)),2) AS `average_order_value` from (`orders` `o` join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) group by date_format(`o`.`order_date`,'%Y-%m');


-- VIEW: vw_payment_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_payment_analysis` AS select `p`.`payment_id` AS `payment_id`,`p`.`order_id` AS `order_id`,`p`.`payment_date` AS `payment_date`,`p`.`payment_method` AS `payment_method`,`p`.`payment_status` AS `payment_status`,`p`.`amount` AS `amount`,`p`.`transaction_reference` AS `transaction_reference`,`o`.`customer_id` AS `customer_id`,`o`.`order_date` AS `order_date`,`o`.`order_status` AS `order_status` from (`payments` `p` join `orders` `o` on((`p`.`order_id` = `o`.`order_id`)));


-- VIEW: vw_returns_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_returns_analysis` AS select `r`.`return_id` AS `return_id`,`r`.`order_id` AS `order_id`,`r`.`order_item_id` AS `order_item_id`,`r`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`r`.`return_date` AS `return_date`,`r`.`return_quantity` AS `return_quantity`,`r`.`return_reason` AS `return_reason`,`r`.`return_status` AS `return_status`,`r`.`return_amount` AS `return_amount`,`r`.`refund_amount` AS `refund_amount` from (`returns` `r` join `products` `p` on((`r`.`product_id` = `p`.`product_id`)));


-- VIEW: vw_sales_analysis

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_sales_analysis` AS select `o`.`order_id` AS `order_id`,`o`.`order_date` AS `order_date`,`o`.`customer_id` AS `customer_id`,`c`.`customer_segment` AS `customer_segment`,`c`.`state` AS `customer_state`,`c`.`city` AS `customer_city`,`oi`.`order_item_id` AS `order_item_id`,`oi`.`product_id` AS `product_id`,`p`.`product_name` AS `product_name`,`p`.`category` AS `category`,`p`.`brand` AS `brand`,`oi`.`quantity` AS `quantity`,`oi`.`unit_price` AS `unit_price`,`oi`.`discount_percent` AS `discount_percent`,`oi`.`discount_amount` AS `discount_amount`,`oi`.`line_total` AS `line_total` from (((`orders` `o` join `customers` `c` on((`o`.`customer_id` = `c`.`customer_id`))) join `order_items` `oi` on((`o`.`order_id` = `oi`.`order_id`))) join `products` `p` on((`oi`.`product_id` = `p`.`product_id`)));


-- VIEW: vw_warehouse_performance

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_warehouse_performance` AS select `w`.`warehouse_id` AS `warehouse_id`,`w`.`warehouse_name` AS `warehouse_name`,`w`.`city` AS `city`,`w`.`state` AS `state`,count(`s`.`shipment_id`) AS `total_shipments`,round(sum(`s`.`shipping_cost`),2) AS `total_shipping_cost`,round(avg(`s`.`distance_km`),2) AS `average_distance_km`,round(((100.0 * sum((case when (`s`.`actual_delivery_date` <= `s`.`expected_delivery_date`) then 1 else 0 end))) / count(`s`.`shipment_id`)),2) AS `on_time_rate` from (`warehouses` `w` left join `shipments` `s` on((`w`.`warehouse_id` = `s`.`warehouse_id`))) group by `w`.`warehouse_id`,`w`.`warehouse_name`,`w`.`city`,`w`.`state`;
