__author__ = 'windy'
from base import *


def get_class_by_tid(db, tid, date_str):
    sql = """SELECT t.fullname, t.shortname, w.teacher, w.description, sc.class_date,
                    w.start_time , sc.check_roll, ss.uid, ss.uname, ss.cla_id, sc.time_id, ci.course as courseId
                FROM schedule.mid_teacher t
                    join mid_workroom w on t.id=w.teacher
                    join mid_student_classes sc on sc.workroom = w.id
                    join mid_student_selected ss on ss.workroom = w.id
                    join mid_course_ids ci on w.id = ci.workroom
                where w.teacher=%s and w.status='used'
                and ss.deal='payed' and sc.class_date=%s
                and sc.check_roll in(0, 2, 6) order by w.start_time
          """
    return db.query(sql, tid, date_str)


@Route("/admin/teacher/my", name="Get class times by tid")
class TeacherMyClass(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        tid = self.get_argument("tid", '')
        date_str = self.get_argument("date", "")
        if not date_str:
            date = datetime.today()
            date_str = "%s-%s-%s" % (date.year, date.month, date.day)
        entries = get_class_by_tid(self.db, tid, date_str)
        self.render("admin/teacher_my.html", entries=entries, tid=tid)
