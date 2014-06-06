__author__ = 'windy'
#coding: utf-8
from base import *
from http_msg import cla_build_status


#===============================后台管理=====================
@Route("/user/add", name="Add User Manager")
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
        rows = self.db.query("select * from mid_course ")
        self.render("admin/list_course_task.html", entries=rows)


@Route("/course/added", name="Notify class has added")
class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        cla_id = self.get_argument("claId")
        if cla_id:
            rs = cla_build_status(cla_id)
            if rs.rlt:
                self.db.execute_rowcount("update mid_course set finished=1 where claId=%s", cla_id)

        self.redirect("/admin/course/tasks")


@Route("/admin/workroom", name="workroom")
class WorkRoomHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        workrooms = self.db_model.models.mwr.list_all()
        self.render("admin/list_workroom.html", entries=workrooms)


@Route("/admin/workroom/single", name="workroom Single")
class WorkRoomSingeHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        counts, workrooms = self.db_model.models.mwrs.query_all(1, 100)
        self.render("admin/list_workroom_single.html", entries=workrooms)


@Route("/admin/query/student/class", name="Student select class")
class QueryStudentSelectedHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        select_list = self.db_model.models.mss.list_selected()
        self.render("admin/list_student_class.html", entries=select_list)


@Route("/admin/query/student/classtable", name="Student Class Table")
class QueryStudentClassTable(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uid = self.get_argument("uid")
        cla_id = self.get_argument("cla_id")
        class_table = self.db_model.models.msc.full_query(uid=uid, cla_id=cla_id)
        self.render("admin/list_class_table.html", entries=class_table)


@Route("/admin/student/change/date", name="change date")
class QueryStudentDateChangedHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        select_id = self.get_argument("select_id", 0)
        date_change = self.db_model.models.msdc.get_by_selected_id(select_id=select_id)
        self.render("admin/list_student_date_change.html", entries=date_change)


@Route("/admin/student/change/class", name="change class")
class StudentClassChangedHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        select_id = self.get_argument("select_id", 0)
        date_change = self.db_model.models.mscc.get_by_select_id(select_id=select_id)
        self.render("admin/list_student_class_change.html", entries=date_change)