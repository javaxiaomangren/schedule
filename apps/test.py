__author__ = 'windy'
#coding: utf-8
import traceback
import httplib
import ujson
from collections import OrderedDict

import tornado.web
from torndb import Row
from utils import route
import datetime




class TimeStatus(object):
    """
      课程状态：0可预约，1已经支付，2完成，3请假，4退课，5补课, 6试听课程
    """
    NORMAL = 0
    PAYED = 1
    FINISHED = 2
    ABSENT = 3
    REFUND = 4
    CHANGED = 5
    TRAIL = 6
    NAME = {
        0: "可预约",
        1: "未开始",
        2: "完成",
        3: "请假",
        4: "退课",
        5: "补课",
        6: "试听课程"
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
        pass

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

    def initialize(self):
        print "please define your initialize..............."


#====================== Commons Methods ==========
def message(rlt=True, code=200, msg="Success"):
    ms = Row()
    ms["rlt"] = rlt
    ms["code"] = code
    ms["msg"] = msg
    return ms


#===============================后台管理=====================
@route("/test", name="test")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        rows = self.db.query("SELECT distinct(class_id) , "
                             "course_id, course_name, student_id, class_status FROM timetable")
        for r in rows:
            print r
        self.render("test.html", entries=rows, students=range(10000, 10010))


@route("/test/time", name="test time")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        rows = self.db.query("SELECT start_time  from timetable limit 1")
        for r in rows:
            print r, r + datetime.timedelta(minutes=30)
        self.write("hello")


course = """
        INSERT INTO schedule.course
        (id,
        class_count,
        every_hours,
        start_date,
        end_date,
        frequency,
        year,
        term_name,
        max_person,
        finished)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

timetable = """
            INSERT INTO schedule.timetable
                (
                course_id,
                course_name,
                class_id,
                class_room,
                teacher_id,
                teacher_name,
                start_time,
                period,
                class_date,
                class_status,
                time_status,
                time_desc
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

timetable_bak = """
        INSERT INTO schedule.timetable_bak
        (teacher_id,
        teacher_name,
        class_room,
        class_date,
        start_time,
        period,
        flag)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
"""

teacher = """
    INSERT INTO schedule.teacher
    (teacherId,
    firstName,
    lastName,
    description,
    pic_url)
    VALUES(%s, %s, %s, %s, %s)
"""


@route("/test/init", name="init data")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        self.db.execute("truncate table course")
        self.db.execute("truncate table teacher")
        self.db.execute("truncate table timetable")
        self.db.execute("truncate table timetable_bak")

        courses = [(course_id, 10, 30, '2014-07-01', '2014-07-20', 2, '2014', course_id, 20 + course_id, 0)
                   for course_id in range(1, 10)]
        self.db.executemany(course, courses)

        teachers = [(tid, chr(tid) + 'Windy-' + str(tid), 'Yang', 'Good Teacher', 'xxx.img') for tid in range(65, 91)]
        self.db.executemany(teacher, teachers)

        timetables = []
        for th in teachers:
            t = th[0] - 55
            if t > 20:
                t -= 14
            class_time = str(t) + ':00'
            for c in range(1, 20, 2):
                if c < 10:
                    class_date = "2014-07-0" + str(c)
                else:
                    class_date = "2014-07-" + str(c)

                timetables.append(
                    (1, "Let you speak to England People",
                    th[0] - 64, "MN000" + str(c) + str(th[0] - 63),
                    th[0], th[1],
                    class_time,30,class_date,0, 0,
                    "2014-07-01 到 2014-07-20 " + class_time + " 隔天上课"
                    ))
        self.db.executemany(timetable, timetables)

        timetable_baks = [(th1[0], th1[1], "MN001" + str(th1[0]), "2014-08-" + str(th1[0] - 60), "10:00", 30, 0) for th1 in teachers]

        self.db.executemany(timetable_bak, timetable_baks)

        self.redirect("/test")


