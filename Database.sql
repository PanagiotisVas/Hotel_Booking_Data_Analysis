CREATE DATABASE  IF NOT EXISTS `Hotel_booking_analysis`
	CHARACTER SET utf8mb4
	COLLATE utf8mb4_unicode_ci;
USE `Hotel_booking_analysis`;



DROP TABLE IF EXISTS `booking_statistics`;
CREATE TABLE `booking_statistics` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `avg_weekend_nights` float DEFAULT NULL,
  `avg_week_nights` float DEFAULT NULL,
  `cancellation_rate` float DEFAULT NULL
) ENGINE=InnoDB;


--
-- Table structure for table `booking_trends_over_time`
--

DROP TABLE IF EXISTS `booking_trends_over_time`;
CREATE TABLE `booking_trends_over_time` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `guest_type_distribution`
--

DROP TABLE IF EXISTS `guest_type_distribution`;
CREATE TABLE `guest_type_distribution` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `guest_type` varchar(20) DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `monthly_bookings`
--

DROP TABLE IF EXISTS `monthly_bookings`;
CREATE TABLE `monthly_bookings` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `month` varchar(20) DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `room_type_distribution`
--

DROP TABLE IF EXISTS `room_type_distribution`;
CREATE TABLE `room_type_distribution` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `room_type` varchar(10) DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `seasonal_booking_trends`
--

DROP TABLE IF EXISTS `seasonal_booking_trends`;
CREATE TABLE `seasonal_booking_trends` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `month` varchar(20) DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `seasonal_bookings`
--

DROP TABLE IF EXISTS `seasonal_bookings`;
CREATE TABLE `seasonal_bookings` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `season` varchar(20) DEFAULT NULL,
  `number_of_bookings` int DEFAULT NULL
) ENGINE=InnoDB;

--
-- Table structure for table `seasonal_cancellation_trends`
--

DROP TABLE IF EXISTS `seasonal_cancellation_trends`;
CREATE TABLE `seasonal_cancellation_trends` (
  `hotel_name` varchar(255) DEFAULT NULL,
  `month` varchar(20) DEFAULT NULL,
  `number_of_cancellations` int DEFAULT NULL
) ENGINE=InnoDB;

