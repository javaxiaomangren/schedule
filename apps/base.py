__author__ = 'windy'
#coding: utf-8
import traceback
import ujson
import json
from collections import OrderedDict
from datetime import datetime, timedelta
import utils
from utils import *

import tornado.web
from torndb import Row
from tornado.log import gen_log as logger


class TimeStatus(object):
    NORMAL = 0
    APPOINTED = 1
    PAYED = 2
    FINISHED = 3
    ABSENT = 4
    REFUND = 5
    CHANGED = 6
    TRAIL = 7
    NAME = {
        0: "可预约",
        1: "预约,待支付",
        2: "等待上课",
        3: "完成",
        4: "请假",
        5: "退课",
        6: "已调课",
        7: "试听课程"
    }


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def auto_commit(self, flag=True):
        self.db._db.autocommit(flag)

    def commit(self):
        self.db._db.commit()

    def rollback(self):
        self.db._db.rollback()

    def get_template_namespace(self):
        ns = super(BaseHandler, self).get_template_namespace()
        ns.update({
            'TimeStatus': TimeStatus,
        })

        return ns

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_error(self, status_code, **kwargs):

        print 'In get_error_html. status_code: ', status_code
        if status_code in [403, 404, 500, 503]:
            filename = '%d.html' % status_code
            print 'rendering filename: ', filename
            return self.render_string(filename, title="TITLE")

        return "<html><title>%(code)d: %(message)s</title>" \
                "<body class='bodyErrorPage'>%(code)d: %(message)s</body>"\
                "</html>" % {
                "code": status_code,
                "message": httplib.responses[status_code],
                }


@Route("/login", name="Login")
class LoginHandle(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("login.html", msg=None)

    def post(self, *args, **kwargs):
        user = self.get_argument("username")
        passwd = self.get_argument("passwd")
        row = self.db.get("SELECT password FROM user where username=%s", user)
        md5 = mk_md5(passwd)
        if row and row.password == unicode(md5):
            self.set_secure_cookie("user", user)
            self.render("admin/base.html")
        else:
            self.render("login.html", entry=Row({"msg": "Wrong login"}))


@Route("/logout", name="Log Out")
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/login"))


def authorization(summary, headers):
    """头部信息加密验证"""
    plat = headers.get("plat", None)
    sys = headers.get("sys", None)
    md5 = headers.get("md5", None)
    if summary and plat and sys and md5:
        m_md5 = utils.mk_md5(summary, plat, sys)
        return md5 == m_md5
    return None


def message(rlt=True, msg="Success"):
    ms = Row()
    ms["rlt"] = rlt
    ms["msg"] = msg
    return ms


def args_value(args):
    _value = {}
    for k in args:
        _value[k] = args.get(k)[0]
    return _value


def set_for_list(dc, value):
    """
        设置聚合信息给选课列表
    """
    old = dc.get(value.class_id)
    clazz = Row()
    clazz["time_id"] = value.time_id
    clazz["date"] = str(value.class_date)
    clazz["time"] = str(value.start_time)
    clazz["time_status"] = value.time_status
    if old:
        classes = old.classes
        classes.append(clazz)
    else:
        new = Row()
        new["course_id"] = value.course_id
        new["course_name"] = value.course_name
        new["class_id"] = value.class_id
        new["class_room"] = value.class_room
        new["teacher_id"] = value.teacher_id
        new["teacher_name"] = value.teacher_name
        new["student_id"] = value.student_id
        new["period"] = value.period
        new["start_time"] = str(value.start_time)
        new["class_status"] = value.class_status
        new["time_desc"] = value.time_desc
        new["class_changed"] = value.class_changed
        new["time_changed"] = value.time_changed
        new["classes"] = [clazz]
        dc[value.class_id] = new


def aggregate_by_grade(rows, set_method):
    """
        聚合课程信息，聚合同一班级下的课程
    """
    grade_dic = Row()
    for value in rows:
        set_method(grade_dic, value)
    return grade_dic


####### db query
def get_by_id(db=None, course_id=0, student_id=0, class_id=0):
    sql = "SELECT * FROM timetable WHERE course_id='%s' " % course_id
    if student_id:
        sql += " AND student_id=%s" % student_id
    elif class_id:
        sql += " AND class_id=%s" % class_id
    sql += " ORDER BY class_date, start_time "
    return db.query(sql)


def get_query_where(course_id, teacher_name, time_interval, **kwargs):
    where = "WHERE class_id > 0 AND class_status=0 AND course_id='%s' AND time_status <> %s " \
            % (course_id, TimeStatus.TRAIL)
    if teacher_name:
        where += " AND teacher_name='%s' " % teacher_name.rstrip()
    if time_interval and "-" in time_interval:
        t1, t2 = time_interval.split('-')
        where += " AND start_time BETWEEN '%s' AND '%s' " % (t1, t2)
    for k in kwargs:
        if kwargs.get(k):
            where += " AND %s='%s'" % (k, kwargs.get(k))
    return where


def get_page_count(db, where, page_size):
    total_count = db.get("SELECT COUNT(DISTINCT class_id) as total FROM timetable %s " % where).total
    return (total_count + page_size - 1) / page_size


def query_timetables(db, course_id, where, page_no, page_size):
    sql = "SELECT distinct class_id FROM timetable "
    limit = " LIMIT %s, %s " % ((page_no - 1) * page_size, page_size)
    class_ids = db.query(sql + where + limit)
    if class_ids:
        ids = ','.join(map(lambda x: str(x.class_id), class_ids))
        query_sql = "SELECT * FROM timetable WHERE class_status=0 AND course_id='%s' " \
                    "AND class_id IN(%s) ORDER BY start_time" % (course_id, ids)
        rows = db.query(query_sql)
        return aggregate_by_grade(rows, set_for_list)
    else:
        return {}

