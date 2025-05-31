-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (x86_64)
--
-- Host: localhost    Database: attendance_system
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `attended` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`attendance_id`),
  KEY `employee_id` (`employee_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (2,2,2,0,'2025-05-29 00:45:16'),(3,3,3,1,'2025-05-29 00:45:16'),(4,1,1,1,'2025-05-29 21:14:33'),(5,2,1,1,'2025-05-29 21:14:33'),(6,3,1,0,'2025-05-29 21:14:33'),(7,4,2,1,'2025-05-29 21:14:33'),(8,5,2,1,'2025-05-29 21:14:33'),(9,6,3,0,'2025-05-29 21:14:33'),(10,7,3,1,'2025-05-29 21:14:33'),(11,8,4,1,'2025-05-29 21:14:33'),(12,9,5,1,'2025-05-29 21:14:33'),(13,10,5,0,'2025-05-29 21:14:33'),(14,11,6,1,'2025-05-29 21:14:33'),(15,12,6,1,'2025-05-29 21:14:33'),(16,13,7,0,'2025-05-29 21:14:33'),(17,14,7,1,'2025-05-29 21:14:33'),(18,15,8,1,'2025-05-29 21:14:33'),(19,16,8,1,'2025-05-29 21:14:33'),(20,17,9,1,'2025-05-29 21:14:33'),(21,18,10,0,'2025-05-29 21:14:33'),(22,19,10,1,'2025-05-29 21:14:33'),(23,20,9,1,'2025-05-29 21:14:33'),(24,21,2,0,'2025-05-29 21:14:33'),(25,22,3,1,'2025-05-29 21:14:33'),(26,23,4,1,'2025-05-29 21:14:33'),(27,24,5,0,'2025-05-29 21:14:33'),(28,25,6,1,'2025-05-29 21:14:33'),(29,26,7,1,'2025-05-29 21:14:33'),(30,27,8,0,'2025-05-29 21:14:33'),(31,28,9,1,'2025-05-29 21:14:33');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  PRIMARY KEY (`employee_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'John','Smith','Sales','John.smith@example.com','2022-02-15'),(2,'Maria','Lopez','HR','maria.lopez@example.com','2021-06-30'),(3,'David','Chen','IT','david.chen@example.com','2023-03-01'),(4,'Ava','Brown','Engineering','ava.brown@example.com','2023-01-10'),(5,'Ethan','Davis','HR','ethan.davis@example.com','2022-06-14'),(6,'Olivia','Miller','Finance','olivia.miller@example.com','2021-03-28'),(7,'Liam','Wilson','IT','liam.wilson@example.com','2020-07-22'),(8,'Mia','Taylor','Marketing','mia.taylor@example.com','2022-11-30'),(9,'Noah','Anderson','Sales','noah.anderson@example.com','2024-02-01'),(10,'Emma','Thomas','Engineering','emma.thomas@example.com','2023-05-13'),(11,'Logan','Moore','HR','logan.moore@example.com','2021-09-08'),(12,'Sophia','Jackson','IT','sophia.jackson@example.com','2020-04-12'),(13,'Lucas','Martin','Finance','lucas.martin@example.com','2021-01-19'),(14,'Isabella','White','Sales','isabella.white@example.com','2023-08-25'),(15,'Aiden','Harris','Marketing','aiden.harris@example.com','2024-01-07'),(16,'Charlotte','Thompson','HR','charlotte.thompson@example.com','2022-03-03'),(17,'Elijah','Garcia','IT','elijah.garcia@example.com','2021-06-16'),(18,'Amelia','Martinez','Finance','amelia.martinez@example.com','2020-10-10'),(19,'Benjamin','Clark','Engineering','benjamin.clark@example.com','2022-08-01'),(20,'Harper','Rodriguez','Sales','harper.rodriguez@example.com','2023-12-02'),(21,'Jackson','Lewis','Marketing','jackson.lewis@example.com','2024-03-11'),(22,'Evelyn','Lee','IT','evelyn.lee@example.com','2020-09-06'),(23,'Sebastian','Walker','Finance','sebastian.walker@example.com','2021-12-22'),(24,'Abigail','Hall','HR','abigail.hall@example.com','2023-07-15'),(25,'Henry','Allen','Engineering','henry.allen@example.com','2022-05-18'),(26,'Emily','Young','IT','emily.young@example.com','2021-04-29'),(27,'Daniel','King','Sales','daniel.king@example.com','2020-11-03'),(28,'Ella','Scott','Marketing','ella.scott@example.com','2023-06-05');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `event_id` int NOT NULL AUTO_INCREMENT,
  `event_name` varchar(100) DEFAULT NULL,
  `event_type` varchar(50) DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'Annual Meeting','Meeting','2025-06-15','Main Conference Room'),(2,'Safety Training','Training','2025-07-01','Room 101'),(3,'Team Building','Workshop','2025-08-20','Outdoor Area'),(4,'Quarterly Review','Meeting','2025-09-10','Room 204'),(5,'Compliance Training','Training','2025-10-05','Training Center A'),(6,'Holiday Party','Social','2025-12-18','Main Hall'),(7,'Product Launch','Corporate Event','2025-11-01','Auditorium'),(8,'Leadership Workshop','Workshop','2025-10-22','Room 305'),(9,'Cybersecurity Seminar','Training','2025-09-25','IT Lab'),(10,'Wellness Fair','Health','2025-10-12','Outdoor Area'),(11,'Annual Strategy Session','Meeting','2025-11-15','Executive Room'),(12,'New Software Training','Training','2025-11-20','IT Training Room'),(13,'Diversity Workshop','Workshop','2025-12-03','Room 110'),(14,'Budget Planning','Meeting','2025-12-10','Finance Conference Room'),(15,'First Aid Training','Training','2026-01-05','Medical Bay'),(16,'Employee Recognition Day','Social','2026-01-20','Main Auditorium'),(17,'New Year Kickoff','Corporate Event','2026-01-10','Main Hall'),(18,'Mental Health Awareness','Health','2026-02-15','Room 215'),(19,'Cloud Migration Update','Meeting','2026-02-22','Room 401'),(20,'Conflict Resolution Workshop','Workshop','2026-03-05','HR Lab');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29 21:56:53
