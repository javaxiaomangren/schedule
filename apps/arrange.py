__author__ = 'windy'
#coding: utf-8

from utils import get_mysql
from db_model import *
import traceback
import string

db = get_mysql()
db_model = BaseDBModel(db)
course_wr_model = MidCourseWorkRoom(db)
workroom_model = MidWorkRoom(db)
workroom_single = MidWorkRoomSingle(db)
selected = MidStudentSelected(db)
workroom_dates_model = MidWorkRoomDates(db)
student_classes = MidStudentClasses(db)
stu_date_change = MidStudentDateChanged(db)
stu_class_changed = MidStudentClassChanged(db)
stu_refund = MidStudentRefund(db)
task = MidTask(db)

logic_model = LogicModel(db)
logic_model.initial(mwr=workroom_model, mcwr=course_wr_model,
                    mss=selected, mwrd=workroom_dates_model,
                    msc=student_classes, msdc=stu_date_change,
                    mwrs=workroom_single, mscc=stu_class_changed,
                    msr=stu_refund)


def auto_commit(flag=True):
    db._db.autocommit(flag)


def commit():
    db._db.commit()


def rollback():
    db._db.rollback()


def transaction(func):
    try:
        auto_commit(False)
        ms = func()
        if ms.rlt:
            commit()
        else:
            print "rollback"
            print traceback.format_exc()
            rollback()
    except:
        rollback()
    finally:
        auto_commit()


#ff808081480e8a3d014810b349e003b1^B-1330-C105^c105^2014-08-27 %s^13:30^2014-08-27,
def arrange(f):
    try:
        auto_commit(flag=False)
        #为那个课程排课
        workroom = []
        wr_dates = []
        c_w = []
        with open(f, "r") as f:
            for l in f:
                cla_id, wr_name, tid, desc, tm, dts = l.strip().split("^")
                #设置workroom参数
                workroom.append((wr_name, "X", tid, tm, "unassigned", "normal", desc % tm))
                #设置workroom_dates 参数
                dt_list = dts.split(",")
                for d in dt_list:
                    wr_dates.append((wr_name, d, 2))
                #设置workroom 和class_id的关系
                c_w.append((cla_id, wr_name))

            if workroom and wr_dates and c_w:
                #保存workroom
                workroom_model.add(workroom)
                #保存workroom date
                workroom_dates_model.add(wr_dates)
                #保存workroom class
                course_wr_model.add_by(c_w)
        commit()
    except:
        print traceback.format_exc()
        rollback()

#TODO Reset Unused
arrange('table')