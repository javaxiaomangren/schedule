__author__ = 'windy'
from base import *


def get_class_by_tid(db, tid):
    sql = """SELECT t.fullname, t.shortname, w.teacher, w.description, sc.class_date,
                    w.start_time , sc.check_roll, ss.uid, ss.uname, ss.cla_id, sc.time_id
                FROM schedule.mid_teacher t
                    join mid_workroom w on t.id=w.teacher
                    join mid_student_classes sc on sc.workroom = w.id
                    join mid_student_selected ss on ss.workroom = w.id
                where w.teacher=%s and w.status='used' and ss.deal='payed'
          """

    return db.query(sql, tid)


@Route("/admin/teacher/my", name="Get class times by tid")
class TeacherMyClass(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        tid = self.get_argument("tid", '')
        entries = get_class_by_tid(self.db, tid)
        self.render("admin/teacher_my.html", entries=entries, tid=tid)
