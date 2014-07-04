__author__ = 'windy'
#coding: utf-8
from base import *
from http_msg import cla_build_status
from test_db_model import *
from config import *


#===============================后台管理=====================

@Route("/user/add", name="Add User Add")
class UserHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/add_user.html")


@Route("/user/add/save", name="Add User Add")
class UserHandle(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_argument("username")
        password = self.get_argument("passwd")
        role = self.get_argument("role")
        self.db.execute("INSERT INTO user (username, password, role) values(%s, %s, %s)", user, mk_md5(password), role)
        self.redirect("/user/list")


@Route("/user/list", name="List User")
class UserHandle(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        entries = self.db.query("select * from user")
        self.render("admin/list_user.html", entries=entries)



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
            if debug:
                rs = auto_insert_date(cla_id=cla_id)
                if rs.rlt:
                    rs = cla_build_status(cla_id)
                    if rs.rlt:
                        self.db.execute_rowcount("update mid_course set finished=1 where claId=%s", cla_id)
                        self.redirect("/admin/course/tasks")
                    else:
                        self.render("200.html", entry=msg(False, "接口调用失败"))
                else:
                    self.render("200.html", entry=rs)
            else:
                rs = cla_build_status(cla_id)
                if rs.rlt:
                    self.db.execute_rowcount("update mid_course set finished=1 where claId=%s", cla_id)
                    self.redirect("/admin/course/tasks")
                else:
                    self.render("200.html", entry=msg(False, "接口调用失败"))


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
        self.render("admin/list_student_class.html", entries=select_list, login_url=config.moodle_url)


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
        uid = self.get_argument("uid", None)
        cla_id = self.get_argument("cla_id", None)
        deal = self.get_argument("deal", "changed")
        if select_id:
            date_change = self.db_model.models.mscc.get_by_select_id(select_id=select_id)
            self.render("admin/list_student_class_change.html", entries=date_change)
        else:
            date_change = self.db_model.get_changed_history(uid=uid, cla_id=cla_id, deal=deal)
            self.render("admin/list_student_class_change.html", entries=date_change)
