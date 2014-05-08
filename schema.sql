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
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8