__author__ = 'windy'
#coding: utf-8
from base import *

#===============================后台管理=====================
@Route("/user/add", name="Admin Manager")
class UserHandle(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        user = self.get_argument("user")
        password = self.get_argument("passwd")
        self.db.execute("INSERT INTO user (username, password) values(%s, %s)", user, mk_md5(password))
        self.redirect("/login")


@Route("/admin", name="Admin Manager")
class AdminClassHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/base.html")


@Route("/admin/course/tasks", name="class Tasks")
class CourseTasksClassHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        rows = self.db.query("select * from course ")
        self.render("admin/list_course_task.html", entries=rows)


@Route("/admin/query/student/class", name="Student select class")
class QueryStudentClassHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable "
                             "WHERE student_id IS NOT NULL")
        results = aggregate_by_grade(rows, set_for_list)
        self.render("admin/list_student_class.html", entries=results.values())


@Route("/admin/query/records/class", name="class change records")
class QueryRecordsHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM records WHERE flag = -2 ORDER BY uid, cla_id")
        self.render("admin/list_records.html", entries=rows)


@Route("/admin/query/records/time", name="time change records")
class QueryRecordsHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM records WHERE flag=-1 ORDER BY uid")
        self.render("admin/list_records.html", entries=rows)


@Route("/admin/query/change/time", name="Query teacher's time changed")
class QueryRecordsHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable WHERE class_id=-1")
        self.render("admin/list_class_teachers.html", entries=rows)


@Route("/admin/query/change/class", name="Query teacher's class changed")
class QueryRecordsHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # course_id = self.get_argument("cid")
        rows = self.db.query("SELECT * FROM timetable WHERE class_id=-2")
        self.render("admin/list_class_teachers.html", entries=rows)


@Route("/admin/kq", name="Kao qi")
class KqHandle(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        dt = datetime.today() + timedelta(days=1)
        rows = self.db.query("SELECT * FROM timetable where class_date < %s ", str(dt))
        self.render("admin/list_class_teachers.html", entries=rows)




