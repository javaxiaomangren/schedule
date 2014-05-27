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
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '请求时间',
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
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `src_id` int(11) DEFAULT NULL,
  `tar_id` int(11) DEFAULT NULL,
  `cla_id` int(11) DEFAULT NULL,
  `course_id` varchar(45) DEFAULT NULL,
  `uid` varchar(45) DEFAULT NULL,
  `create_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `flag` tinyint(4) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=200101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES (200001,'Windy-1','Yang','Good Teacher','xxx.img'),(200002,'Windy-2','Yang','Good Teacher','xxx.img'),(200003,'Windy-3','Yang','Good Teacher','xxx.img'),(200004,'Windy-4','Yang','Good Teacher','xxx.img'),(200005,'Windy-5','Yang','Good Teacher','xxx.img'),(200006,'Windy-6','Yang','Good Teacher','xxx.img'),(200007,'Windy-7','Yang','Good Teacher','xxx.img'),(200008,'Windy-8','Yang','Good Teacher','xxx.img'),(200009,'Windy-9','Yang','Good Teacher','xxx.img'),(200010,'Windy-10','Yang','Good Teacher','xxx.img'),(200011,'Windy-11','Yang','Good Teacher','xxx.img'),(200012,'Windy-12','Yang','Good Teacher','xxx.img'),(200013,'Windy-13','Yang','Good Teacher','xxx.img'),(200014,'Windy-14','Yang','Good Teacher','xxx.img'),(200015,'Windy-15','Yang','Good Teacher','xxx.img'),(200016,'Windy-16','Yang','Good Teacher','xxx.img'),(200017,'Windy-17','Yang','Good Teacher','xxx.img'),(200018,'Windy-18','Yang','Good Teacher','xxx.img'),(200019,'Windy-19','Yang','Good Teacher','xxx.img'),(200020,'Windy-20','Yang','Good Teacher','xxx.img'),(200021,'Windy-21','Yang','Good Teacher','xxx.img'),(200022,'Windy-22','Yang','Good Teacher','xxx.img'),(200023,'Windy-23','Yang','Good Teacher','xxx.img'),(200024,'Windy-24','Yang','Good Teacher','xxx.img'),(200025,'Windy-25','Yang','Good Teacher','xxx.img'),(200026,'Windy-26','Yang','Good Teacher','xxx.img'),(200027,'Windy-27','Yang','Good Teacher','xxx.img'),(200028,'Windy-28','Yang','Good Teacher','xxx.img'),(200029,'Windy-29','Yang','Good Teacher','xxx.img'),(200030,'Windy-30','Yang','Good Teacher','xxx.img'),(200031,'Windy-31','Yang','Good Teacher','xxx.img'),(200032,'Windy-32','Yang','Good Teacher','xxx.img'),(200033,'Windy-33','Yang','Good Teacher','xxx.img'),(200034,'Windy-34','Yang','Good Teacher','xxx.img'),(200035,'Windy-35','Yang','Good Teacher','xxx.img'),(200036,'Windy-36','Yang','Good Teacher','xxx.img'),(200037,'Windy-37','Yang','Good Teacher','xxx.img'),(200038,'Windy-38','Yang','Good Teacher','xxx.img'),(200039,'Windy-39','Yang','Good Teacher','xxx.img'),(200040,'Windy-40','Yang','Good Teacher','xxx.img'),(200041,'Windy-41','Yang','Good Teacher','xxx.img'),(200042,'Windy-42','Yang','Good Teacher','xxx.img'),(200043,'Windy-43','Yang','Good Teacher','xxx.img'),(200044,'Windy-44','Yang','Good Teacher','xxx.img'),(200045,'Windy-45','Yang','Good Teacher','xxx.img'),(200046,'Windy-46','Yang','Good Teacher','xxx.img'),(200047,'Windy-47','Yang','Good Teacher','xxx.img'),(200048,'Windy-48','Yang','Good Teacher','xxx.img'),(200049,'Windy-49','Yang','Good Teacher','xxx.img'),(200050,'Windy-50','Yang','Good Teacher','xxx.img'),(200051,'Windy-51','Yang','Good Teacher','xxx.img'),(200052,'Windy-52','Yang','Good Teacher','xxx.img'),(200053,'Windy-53','Yang','Good Teacher','xxx.img'),(200054,'Windy-54','Yang','Good Teacher','xxx.img'),(200055,'Windy-55','Yang','Good Teacher','xxx.img'),(200056,'Windy-56','Yang','Good Teacher','xxx.img'),(200057,'Windy-57','Yang','Good Teacher','xxx.img'),(200058,'Windy-58','Yang','Good Teacher','xxx.img'),(200059,'Windy-59','Yang','Good Teacher','xxx.img'),(200060,'Windy-60','Yang','Good Teacher','xxx.img'),(200061,'Windy-61','Yang','Good Teacher','xxx.img'),(200062,'Windy-62','Yang','Good Teacher','xxx.img'),(200063,'Windy-63','Yang','Good Teacher','xxx.img'),(200064,'Windy-64','Yang','Good Teacher','xxx.img'),(200065,'Windy-65','Yang','Good Teacher','xxx.img'),(200066,'Windy-66','Yang','Good Teacher','xxx.img'),(200067,'Windy-67','Yang','Good Teacher','xxx.img'),(200068,'Windy-68','Yang','Good Teacher','xxx.img'),(200069,'Windy-69','Yang','Good Teacher','xxx.img'),(200070,'Windy-70','Yang','Good Teacher','xxx.img'),(200071,'Windy-71','Yang','Good Teacher','xxx.img'),(200072,'Windy-72','Yang','Good Teacher','xxx.img'),(200073,'Windy-73','Yang','Good Teacher','xxx.img'),(200074,'Windy-74','Yang','Good Teacher','xxx.img'),(200075,'Windy-75','Yang','Good Teacher','xxx.img'),(200076,'Windy-76','Yang','Good Teacher','xxx.img'),(200077,'Windy-77','Yang','Good Teacher','xxx.img'),(200078,'Windy-78','Yang','Good Teacher','xxx.img'),(200079,'Windy-79','Yang','Good Teacher','xxx.img'),(200080,'Windy-80','Yang','Good Teacher','xxx.img'),(200081,'Windy-81','Yang','Good Teacher','xxx.img'),(200082,'Windy-82','Yang','Good Teacher','xxx.img'),(200083,'Windy-83','Yang','Good Teacher','xxx.img'),(200084,'Windy-84','Yang','Good Teacher','xxx.img'),(200085,'Windy-85','Yang','Good Teacher','xxx.img'),(200086,'Windy-86','Yang','Good Teacher','xxx.img'),(200087,'Windy-87','Yang','Good Teacher','xxx.img'),(200088,'Windy-88','Yang','Good Teacher','xxx.img'),(200089,'Windy-89','Yang','Good Teacher','xxx.img'),(200090,'Windy-90','Yang','Good Teacher','xxx.img'),(200091,'Windy-91','Yang','Good Teacher','xxx.img'),(200092,'Windy-92','Yang','Good Teacher','xxx.img'),(200093,'Windy-93','Yang','Good Teacher','xxx.img'),(200094,'Windy-94','Yang','Good Teacher','xxx.img'),(200095,'Windy-95','Yang','Good Teacher','xxx.img'),(200096,'Windy-96','Yang','Good Teacher','xxx.img'),(200097,'Windy-97','Yang','Good Teacher','xxx.img'),(200098,'Windy-98','Yang','Good Teacher','xxx.img'),(200099,'Windy-99','Yang','Good Teacher','xxx.img'),(200100,'Windy-100','Yang','Good Teacher','xxx.img');
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
  `course_id` varchar(45) NOT NULL,
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
-- Table structure for table `timetable2`
--

DROP TABLE IF EXISTS `timetable2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable2` (
  `time_id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` varchar(45) NOT NULL,
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
-- Dumping data for table `timetable2`
--

LOCK TABLES `timetable2` WRITE;
/*!40000 ALTER TABLE `timetable2` DISABLE KEYS */;
/*!40000 ALTER TABLE `timetable2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable_bak`
--

DROP TABLE IF EXISTS `timetable_bak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable_bak` (
  `id` int(11) NOT NULL,
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
INSERT INTO `timetable_bak` VALUES (1200001,200001,'Windy-1','MN001200001','2014-08-20','10:00:00',30,0),(1200002,200002,'Windy-2','MN001200002','2014-08-20','10:00:00',30,0),(1200003,200003,'Windy-3','MN001200003','2014-08-20','10:00:00',30,0),(1200004,200004,'Windy-4','MN001200004','2014-08-20','10:00:00',30,0),(1200005,200005,'Windy-5','MN001200005','2014-08-20','10:00:00',30,0),(1200006,200006,'Windy-6','MN001200006','2014-08-20','10:00:00',30,0),(1200007,200007,'Windy-7','MN001200007','2014-08-20','10:00:00',30,0),(1200008,200008,'Windy-8','MN001200008','2014-08-20','10:00:00',30,0),(1200009,200009,'Windy-9','MN001200009','2014-08-20','10:00:00',30,0),(1200010,200010,'Windy-10','MN001200010','2014-08-20','10:00:00',30,0),(1200011,200011,'Windy-11','MN001200011','2014-08-20','10:00:00',30,0),(1200012,200012,'Windy-12','MN001200012','2014-08-20','10:00:00',30,0),(1200013,200013,'Windy-13','MN001200013','2014-08-20','10:00:00',30,0),(1200014,200014,'Windy-14','MN001200014','2014-08-20','10:00:00',30,0),(1200015,200015,'Windy-15','MN001200015','2014-08-20','10:00:00',30,0),(1200016,200016,'Windy-16','MN001200016','2014-08-20','10:00:00',30,0),(1200017,200017,'Windy-17','MN001200017','2014-08-20','10:00:00',30,0),(1200018,200018,'Windy-18','MN001200018','2014-08-20','10:00:00',30,0),(1200019,200019,'Windy-19','MN001200019','2014-08-20','10:00:00',30,0),(1200020,200020,'Windy-20','MN001200020','2014-08-20','10:00:00',30,0),(1200021,200021,'Windy-21','MN001200021','2014-08-20','10:00:00',30,0),(1200022,200022,'Windy-22','MN001200022','2014-08-20','10:00:00',30,0),(1200023,200023,'Windy-23','MN001200023','2014-08-20','10:00:00',30,0),(1200024,200024,'Windy-24','MN001200024','2014-08-20','10:00:00',30,0),(1200025,200025,'Windy-25','MN001200025','2014-08-20','10:00:00',30,0),(1200026,200026,'Windy-26','MN001200026','2014-08-20','10:00:00',30,0),(1200027,200027,'Windy-27','MN001200027','2014-08-20','10:00:00',30,0),(1200028,200028,'Windy-28','MN001200028','2014-08-20','10:00:00',30,0),(1200029,200029,'Windy-29','MN001200029','2014-08-20','10:00:00',30,0),(1200030,200030,'Windy-30','MN001200030','2014-08-20','10:00:00',30,0),(1200031,200031,'Windy-31','MN001200031','2014-08-20','10:00:00',30,0),(1200032,200032,'Windy-32','MN001200032','2014-08-20','10:00:00',30,0),(1200033,200033,'Windy-33','MN001200033','2014-08-20','10:00:00',30,0),(1200034,200034,'Windy-34','MN001200034','2014-08-20','10:00:00',30,0),(1200035,200035,'Windy-35','MN001200035','2014-08-20','10:00:00',30,0),(1200036,200036,'Windy-36','MN001200036','2014-08-20','10:00:00',30,0),(1200037,200037,'Windy-37','MN001200037','2014-08-20','10:00:00',30,0),(1200038,200038,'Windy-38','MN001200038','2014-08-20','10:00:00',30,0),(1200039,200039,'Windy-39','MN001200039','2014-08-20','10:00:00',30,0),(1200040,200040,'Windy-40','MN001200040','2014-08-20','10:00:00',30,0),(1200041,200041,'Windy-41','MN001200041','2014-08-20','10:00:00',30,0),(1200042,200042,'Windy-42','MN001200042','2014-08-20','10:00:00',30,0),(1200043,200043,'Windy-43','MN001200043','2014-08-20','10:00:00',30,0),(1200044,200044,'Windy-44','MN001200044','2014-08-20','10:00:00',30,0),(1200045,200045,'Windy-45','MN001200045','2014-08-20','10:00:00',30,0),(1200046,200046,'Windy-46','MN001200046','2014-08-20','10:00:00',30,0),(1200047,200047,'Windy-47','MN001200047','2014-08-20','10:00:00',30,0),(1200048,200048,'Windy-48','MN001200048','2014-08-20','10:00:00',30,0),(1200049,200049,'Windy-49','MN001200049','2014-08-20','10:00:00',30,0),(1200050,200050,'Windy-50','MN001200050','2014-08-20','10:00:00',30,0),(1200051,200051,'Windy-51','MN001200051','2014-08-20','10:00:00',30,0),(1200052,200052,'Windy-52','MN001200052','2014-08-20','10:00:00',30,0),(1200053,200053,'Windy-53','MN001200053','2014-08-20','10:00:00',30,0),(1200054,200054,'Windy-54','MN001200054','2014-08-20','10:00:00',30,0),(1200055,200055,'Windy-55','MN001200055','2014-08-20','10:00:00',30,0),(1200056,200056,'Windy-56','MN001200056','2014-08-20','10:00:00',30,0),(1200057,200057,'Windy-57','MN001200057','2014-08-20','10:00:00',30,0),(1200058,200058,'Windy-58','MN001200058','2014-08-20','10:00:00',30,0),(1200059,200059,'Windy-59','MN001200059','2014-08-20','10:00:00',30,0),(1200060,200060,'Windy-60','MN001200060','2014-08-20','10:00:00',30,0),(1200061,200061,'Windy-61','MN001200061','2014-08-20','10:00:00',30,0),(1200062,200062,'Windy-62','MN001200062','2014-08-20','10:00:00',30,0),(1200063,200063,'Windy-63','MN001200063','2014-08-20','10:00:00',30,0),(1200064,200064,'Windy-64','MN001200064','2014-08-20','10:00:00',30,0),(1200065,200065,'Windy-65','MN001200065','2014-08-20','10:00:00',30,0),(1200066,200066,'Windy-66','MN001200066','2014-08-20','10:00:00',30,0),(1200067,200067,'Windy-67','MN001200067','2014-08-20','10:00:00',30,0),(1200068,200068,'Windy-68','MN001200068','2014-08-20','10:00:00',30,0),(1200069,200069,'Windy-69','MN001200069','2014-08-20','10:00:00',30,0),(1200070,200070,'Windy-70','MN001200070','2014-08-20','10:00:00',30,0),(1200071,200071,'Windy-71','MN001200071','2014-08-20','10:00:00',30,0),(1200072,200072,'Windy-72','MN001200072','2014-08-20','10:00:00',30,0),(1200073,200073,'Windy-73','MN001200073','2014-08-20','10:00:00',30,0),(1200074,200074,'Windy-74','MN001200074','2014-08-20','10:00:00',30,0),(1200075,200075,'Windy-75','MN001200075','2014-08-20','10:00:00',30,0),(1200076,200076,'Windy-76','MN001200076','2014-08-20','10:00:00',30,0),(1200077,200077,'Windy-77','MN001200077','2014-08-20','10:00:00',30,0),(1200078,200078,'Windy-78','MN001200078','2014-08-20','10:00:00',30,0),(1200079,200079,'Windy-79','MN001200079','2014-08-20','10:00:00',30,0),(1200080,200080,'Windy-80','MN001200080','2014-08-20','10:00:00',30,0),(1200081,200081,'Windy-81','MN001200081','2014-08-20','10:00:00',30,0),(1200082,200082,'Windy-82','MN001200082','2014-08-20','10:00:00',30,0),(1200083,200083,'Windy-83','MN001200083','2014-08-20','10:00:00',30,0),(1200084,200084,'Windy-84','MN001200084','2014-08-20','10:00:00',30,0),(1200085,200085,'Windy-85','MN001200085','2014-08-20','10:00:00',30,0),(1200086,200086,'Windy-86','MN001200086','2014-08-20','10:00:00',30,0),(1200087,200087,'Windy-87','MN001200087','2014-08-20','10:00:00',30,0),(1200088,200088,'Windy-88','MN001200088','2014-08-20','10:00:00',30,0),(1200089,200089,'Windy-89','MN001200089','2014-08-20','10:00:00',30,0),(1200090,200090,'Windy-90','MN001200090','2014-08-20','10:00:00',30,0),(1200091,200091,'Windy-91','MN001200091','2014-08-20','10:00:00',30,0),(1200092,200092,'Windy-92','MN001200092','2014-08-20','10:00:00',30,0),(1200093,200093,'Windy-93','MN001200093','2014-08-20','10:00:00',30,0),(1200094,200094,'Windy-94','MN001200094','2014-08-20','10:00:00',30,0),(1200095,200095,'Windy-95','MN001200095','2014-08-20','10:00:00',30,0),(1200096,200096,'Windy-96','MN001200096','2014-08-20','10:00:00',30,0),(1200097,200097,'Windy-97','MN001200097','2014-08-20','10:00:00',30,0),(1200098,200098,'Windy-98','MN001200098','2014-08-20','10:00:00',30,0),(1200099,200099,'Windy-99','MN001200099','2014-08-20','10:00:00',30,0),(1200100,200100,'Windy-100','MN001200100','2014-08-20','10:00:00',30,0);
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
  `course_id` varchar(45) NOT NULL,
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

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `create_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','7e1076e82c7dd958b82a501096d2685a','2014-05-22 17:02:57');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-05-28  7:10:16
