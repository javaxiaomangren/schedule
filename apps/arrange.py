__author__ = 'windy'
#coding: utf-8

from utils import get_mysql
from db_model import *
import traceback
import string
import sys

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
                for cid in cla_id.split(','):
                    c_w.append((cid, wr_name))

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

# select w.id mid_workroom w
#     join mid_course_workroom cd on cd.workroom=w.id
#    where cd.cla_id='ff808081480e8a3d0148112893e00be3' and w.status='normal'
#
# 1616,1618,1619,1620,1621,1622,1623,1624,1625,1626,1627,1658,1659,1660,1661,1662,1673,1674,,1675,1676
# ('B-0900-M202','B-0930-M202','B-1000-M202','B-1030-M202','B-1100-M202','B-1330-C105','B-1330-C109','B-1400-C109','B-1430-C105','B-1430-C109','B-1500-C105','B-1500-C109','B-1530-C105','B-1600-C105','B-1630-C105','B-1700-C105','B-1730-C105','B-1800-C105','B-1830-C105','B-1900-C105')
#
#

#
# K5-27
# ff8080814815034601481573eb9d030b
# select group_concat(wd.time_id), group_concat(w.id) from mid_course_workroom cw
#    join mid_workroom w on w.id=cw.workroom
#    join mid_workroom_dates wd on wd.workroom=w.id
#    where cw.cla_id='ff808081480e8a3d01481120a3500b87' and w.status='normal'
#  1799,1800,1801,1802,1803,1804,1805,1806,1807,1809
# 'B-ANGEL-M206-17','B-ANGEL-M206-18','B-ANGEL-M206-19','B-ANGEL-M206-20','B-ANGEL-M206-21','B-ANGEL-M206-22','B-ANGEL-M206-23','B-ANGEL-M206-24','B-ANGEL-M206-25','B-ANGEL-M206-27',
#
# delete from mid_workroom_dates where time_id in(1799,1800,1801,1802,1803,1804,1805,1806,1807,1809);
# delete from mid_workroom where id in ('B-ANGEL-M206-17','B-ANGEL-M206-18','B-ANGEL-M206-19','B-ANGEL-M206-20','B-ANGEL-M206-21','B-ANGEL-M206-22','B-ANGEL-M206-23','B-ANGEL-M206-24','B-ANGEL-M206-25','B-ANGEL-M206-27');
# delete from mid_course_workroom where workroom in('B-ANGEL-M206-17','B-ANGEL-M206-18','B-ANGEL-M206-19','B-ANGEL-M206-20','B-ANGEL-M206-21','B-ANGEL-M206-22','B-ANGEL-M206-23','B-ANGEL-M206-24','B-ANGEL-M206-25','B-ANGEL-M206-27',);


if __name__ == "__main__":
    arrange(sys.argv[1])