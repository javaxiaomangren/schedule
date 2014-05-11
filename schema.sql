CREATE DATABASE `schedule` /*!40100 DEFAULT CHARACTER SET utf8 */;

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
  `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '请求时间',
  `finished` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否完成',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `teacher` (
  `teacherId` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(45) DEFAULT NULL,
  `lastName` varchar(45) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `pic_url` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`teacherId`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8 ;

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
) ENGINE=InnoDB AUTO_INCREMENT=264 DEFAULT CHARSET=utf8;

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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;