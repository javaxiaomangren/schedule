-- MySQL dump 10.13  Distrib 5.6.17, for osx10.9 (x86_64)
--
-- Host: localhost    Database: schedule
-- ------------------------------------------------------
-- Server version	5.6.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `claId` varchar(45) NOT NULL COMMENT '班级id',
  `class_name` varchar(255) DEFAULT NULL,
  `class_count` int(11) NOT NULL COMMENT '总课次',
  `every_hours` int(11) NOT NULL COMMENT '课时',
  `start_date` varchar(32) NOT NULL COMMENT '开课时间',
  `end_date` varchar(32) NOT NULL COMMENT '结课时间',
  `frequency` int(11) NOT NULL COMMENT '上课频率(天为单位)',
  `year` varchar(10) NOT NULL COMMENT '年份',
  `term_name` varchar(45) NOT NULL COMMENT '学期类型',
  `max_person` int(11) NOT NULL COMMENT '班级最大人数',
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '请求时间',
  `finished` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否完成',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `claId` (`claId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher` (
  `teacherId` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `pic_url` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`teacherId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable` (
  `time_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `class_id` int(11) NOT NULL,
  `class_room` varchar(45) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `teacher_name` varchar(45) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `start_time` time NOT NULL,
  `period` int(11) NOT NULL,
  `class_date` date NOT NULL,
  `class_status` tinyint(4) NOT NULL DEFAULT '0',
  `time_status` tinyint(4) DEFAULT '0',
  `time_desc` varchar(255) DEFAULT NULL,
  `check_roll` varchar(45) DEFAULT NULL,
  `time_changed` tinyint(4) NOT NULL DEFAULT '0',
  `class_changed` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`time_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable_bak`
--

DROP TABLE IF EXISTS `timetable_bak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable_bak` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) DEFAULT NULL,
  `teacher_name` varchar(45) DEFAULT NULL,
  `class_room` varchar(45) DEFAULT NULL,
  `class_date` date DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `flag` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable_bak`
--

LOCK TABLES `timetable_bak` WRITE;
/*!40000 ALTER TABLE `timetable_bak` DISABLE KEYS */;
/*!40000 ALTER TABLE `timetable_bak` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable_record`
--

DROP TABLE IF EXISTS `timetable_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable_record` (
  `time_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `class_id` int(11) NOT NULL,
  `class_room` varchar(45) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `teacher_name` varchar(45) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `start_time` time NOT NULL,
  `period` int(11) NOT NULL,
  `class_date` date NOT NULL,
  `class_status` tinyint(4) NOT NULL DEFAULT '0',
  `time_status` tinyint(4) DEFAULT '0',
  `time_desc` varchar(255) DEFAULT NULL,
  `check_roll` varchar(45) DEFAULT NULL,
  `time_changed` tinyint(4) NOT NULL DEFAULT '0',
  `class_changed` tinyint(4) NOT NULL DEFAULT '0',
  `lastupdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable_record`
--

LOCK TABLES `timetable_record` WRITE;
/*!40000 ALTER TABLE `timetable_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `timetable_record` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-14 15:55:13
