__author__ = 'windy'
#coding: utf-8
import traceback
import httplib
import ujson
from collections import OrderedDict

import tornado.web
from torndb import Row
from utils import Route, cla_build_status
import datetime




class TimeStatus(object):
    """
      课程状态：0可预约,1已经支付,2完成,3请假,4退课,5补课, 6试听课程
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

#====================== Commons Methods ==========
def message(rlt=True, code=200, msg="Success"):
    ms = Row()
    ms["rlt"] = rlt
    ms["code"] = code
    ms["msg"] = msg
    return ms


#===============================后台管理=====================
@Route("/test", name="test")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        rows = self.db.query("SELECT distinct(class_id) , "
                             "course_id, course_name, student_id, class_status FROM timetable")
        for r in rows:
            print r
        self.render("test.html", entries=rows, students=range(10000, 10010))


@Route("/test/base", name="test base")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("base.html")


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


@Route("/test/init", name="init data")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        # self.db.execute("truncate table course")
        self.db.execute("truncate table teacher")
        self.db.execute("truncate table timetable")
        self.db.execute("truncate table timetable_bak")
        self.db.execute("truncate table records")

        # courses = [(course_id, 10, 30, '2014-07-01', '2014-07-20', 2, '2014', course_id, 20 + course_id, 0)
        #            for course_id in range(1, 10)]
        # self.db.executemany(course, courses)

        teachers = [(tid, 'Windy-' + str(tid), 'Yang', 'Good Teacher', 'xxx.img') for tid in range(1, 101)]
        self.db.executemany(teacher, teachers)

        timetables = []
        for th in teachers:
            for t in ['2014-05-20','2014-05-21','2014-05-22','2014-05-23','2014-05-24','2014-05-25','2014-05-26','2014-05-27','2014-05-28','2014-05-29','2014-05-30','2014-05-31','2014-06-01','2014-06-02','2014-06-03','2014-06-04','2014-06-05','2014-06-06']:
                pass
                timetables.append(
                    ("8a8185ce4613b5b6014613cb4fcc0017", "在线外教寒假班",
                    th[0], "MN000" + str(th[0]),
                    th[0], th[1],
                    "09:00:00", 30, t ,0, 0,
                    "2014-05-20,2014-06-06 "
                    ))

        self.db.executemany(timetable, timetables)

        timetable_baks = [(th1[0], th1[1], "MN001" + str(th1[0]), "2014-08-20", "10:00", 30, 0) for th1 in teachers]

        self.db.executemany(timetable_bak, timetable_baks)
        data = cla_build_status("8a8185ce4613b5b6014613cb4fcc0017")
        print data.data
        self.redirect("/test")



@Route("/test/course", name="init course")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        course_id = self.get_argument("claId", None)
        if not course_id:
            return self.write("need a course Id ")
        row = self.db.get("SELECT * FROM course WHERE claId=%s AND finished=0", course_id)
        if not row:
            self.render("200.html", entry=Row({"msg": "No data"}))
            return

        max_class = self.db.get("SELECT MAX(class_id) as max_id FROM timetable").max_id
        start = datetime.datetime(*map(lambda x: int(x), row.start_date.split("-")))
        end = datetime.datetime(*map(lambda x: int(x), row.end_date.split("-")))
        persons = row.max_person
        freq = row.frequency
        counts = (end - start).days
        params = []
        for tid in range(10000, 10000 + persons, freq):
            for c in range(0, counts + 1):
                params.append((course_id,
                               row.class_name,
                               max_class,
                               "ClassRoom" + str(max_class),
                               tid,
                               "Test-Teacher-" + str(tid),
                               "09:00",
                               30,
                               start + datetime.timedelta(days=c),
                               0,
                               0,
                               row.start_date + " to " + row.end_date))

                max_class += 1
        self.db.executemany_rowcount(timetable, params)
        self.db.execute("UPDATE course SET finished=1 WHERE claId=%s", course_id)
        self.render("200.html", entry=Row({"msg": "success"}))
