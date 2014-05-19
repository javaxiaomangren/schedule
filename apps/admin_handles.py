__author__ = 'windy'
#coding: utf-8
from base import *

#===============================后台管理=====================
@Route("/admin", name="Admin Manager")
class AdminClassHandle(BaseHandler):
    def get(self):
        self.render("admin/base.html")


@Route("/admin/course/tasks", name="class Tasks")
class CourseTasksClassHandle(BaseHandler):
    def get(self):
        rows = self.db.query("select * from course ")
        self.render("admin/list_course_task.html", entries=rows)


@Route("/admin/query/student/class", name="Student select class")
class QueryStudentClassHandle(BaseHandler):
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable "
                             "WHERE student_id IS NOT NULL")
        results = aggregate_by_grade(rows, set_for_list)
        self.render("admin/list_student_class.html", entries=results.values())


@Route("/admin/query/records/class", name="class change records")
class QueryRecordsHandle(BaseHandler):
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM records WHERE flag = -2 ORDER BY uid, cla_id")
        self.render("admin/list_records.html", entries=rows)


@Route("/admin/query/records/time", name="time change records")
class QueryRecordsHandle(BaseHandler):
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM records WHERE flag=-1 ORDER BY uid")
        self.render("admin/list_records.html", entries=rows)


@Route("/admin/query/change/time", name="Query teacher's time changed")
class QueryRecordsHandle(BaseHandler):
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable WHERE class_id=-1")
        self.render("admin/list_class_teachers.html", entries=rows)



@Route("/admin/query/change/class", name="Query teacher's class changed")
class QueryRecordsHandle(BaseHandler):
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable WHERE class_id=-2")
        self.render("admin/list_class_teachers.html", entries=rows)



