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
  `check_roll` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`time_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;


CREATE TABLE `course` (
  `id` varchar(45) NOT NULL COMMENT '班级id',
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*
-- Query: SELECT * FROM schedule.timetable
LIMIT 0, 1000

-- Date: 2014-05-08 22:08
*/
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (52,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (53,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (54,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (55,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (56,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (57,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (58,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (59,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (60,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-20',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (61,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-08-21',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (62,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-08-23',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (63,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-08-25',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (64,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-08-27',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (65,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-08-29',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (66,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-09-01',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (67,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-09-03',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (68,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-09-05',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (69,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-09-07',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (70,1,'英语口语,少儿提高班',7,'MN0007',7,'Justin Bobo',NULL,'15:30:00',25,'2014-09-09',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (1,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-01',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (2,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-03',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (3,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-05',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (4,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-07',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (5,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-09',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (6,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (7,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (8,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (9,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (10,1,'英语口语',1,'MN0001',1,'Anna',NULL,'09:00:00',25,'2014-07-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (11,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-03',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (12,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-05',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (13,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-07',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (14,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-09',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (15,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (16,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (17,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (18,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (19,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (20,1,'英语口语',2,'MN0002',2,'Katherlin',NULL,'09:30:00',30,'2014-07-21',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (21,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-03',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (22,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-05',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (23,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-07',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (24,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-09',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (25,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (26,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (27,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (28,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (29,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (30,1,'英语口语',3,'MN0003',3,'Bob',NULL,'10:30:00',40,'2014-07-21',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (31,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (32,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (33,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (34,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (35,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (36,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (37,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (38,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (39,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (40,1,'英语口语',4,'MN0004',4,'Jorney',NULL,'18:30:00',40,'2014-07-20',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (41,1,'英语口语',6,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (42,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (43,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (44,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (45,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-11',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (46,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-13',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (47,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-15',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (48,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-17',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (49,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-19',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (50,1,'英语口语',5,'MN0005',5,'Brian jack',NULL,'14:00:00',20,'2014-06-20',0,0,NULL);
INSERT INTO `timetable` (`time_id`,`course_id`,`course_name`,`class_id`,`class_room`,`teacher_id`,`teacher_name`,`student_id`,`start_time`,`period`,`class_date`,`class_status`,`time_status`,`check_roll`) VALUES (51,1,'英语口语,少儿提高班',6,'MN0006',6,'Steffen Solomen',NULL,'16:10:00',25,'2014-05-13',0,0,NULL);
