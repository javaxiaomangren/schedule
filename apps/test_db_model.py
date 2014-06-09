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

logic_model = LogicModel(db)
logic_model.initial(mwr=workroom_model, mcwr=course_wr_model,
                    mss=selected, mwrd=workroom_dates_model,
                    msc=student_classes, msdc=stu_date_change,
                    mwrs=workroom_single, mscc=stu_class_changed,
                    msr=stu_refund)

uid = "1211222"
cla_id = "ff80808146463d430146476fad76003d"


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


def test_where():
    return db_model.get_and_where(*("order by id desc ", " limit 1, 20"), **{"a": 1, "b": 2, "c": [2, 3, 4, 56]})
# print test_where()


def test_get_one():
    return db_model.get_one(MidCourse.TABLE, *db_model.get_and_where(claId="ff80808146463d430146476fad76003d"))
# print test_get_one()


def test_get_all_simple():
    return db_model.get_all_simple(MidWorkRoom.TABLE)
# print test_get_all_simple()


def test_add_workroom_and_dates():
    f_time = lambda _x: _x[0:2] + ":" + _x[2:]
    term = "A"
    desc = u'2014年7月23 到 8月4号, 周一至周六, %s 上课'
    status = "normal"
    teacher = "c101"
    times = ["1200", "1230", "1300", "1330", "1400",
             "1430", "1500", "1530", "1600", "1630",
             "1800", "1830", "1900", "1930", "2000",
             "2030"]
    w_datas = []
    wd_datas = []
    class_type = 2
    for t in times:
        room = "-".join([term, t, teacher])
        wr = (room, term, teacher, f_time(t), "-".join([term.lower(), t, teacher]), status, desc % f_time(t))
        w_datas.append(wr)
        for dt in a_dates:
            if dt == "2014-07-23":
                class_type = 7
            wd_datas.append((room, dt, class_type))

    print workroom_model.add(w_datas)
    print workroom_dates_model.add(wd_datas)
# test_add_workroom_and_dates()


def test_load_from_text():
    with open("class_table.txt") as src:
        workroom = []
        desc = u'2014年7月23 到 8月4号, 周一至周六, %s 上课'
        wd_datas = []
        teacher = {}
        for l in src:
            term, time, t_id, tname, grade = l[:-1].split("\t")
            if len(time) == 4:
                time = '0' + time
            # A-1200-K1-c101
            # a-1200-k1-c101
            tt = str(string.replace(time, ":", ''))
            room_id = term + "-" + tt + "-" + grade + "-" + t_id
            l_term = term.lower()
            u_id = l_term + "-" + tt + "-" + grade.lower() + "-" + t_id
            workroom.append((room_id, term, t_id, time, u_id, "normal", desc % time))
            teacher[t_id] = tname
            for dt in a_dates:
                class_type = 2
                if dt == "2014-07-23":
                    class_type = 7
                wd_datas.append((room_id, dt, class_type))

        print workroom_model.add(workroom)
        print workroom_dates_model.add(wd_datas)
        print db.executemany_rowcount("insert into mid_teacher (id, shortname, fullname) values(%s, %s, %s)"
        ,map(lambda _x: (_x, teacher.get(_x)[:-2], teacher.get(_x)), teacher))

# test_load_from_text()


def auto_insert_date(cla_id='1211212'):
    try:
        workroom = []
        workroom_s = []
        wd_datas = []
        wr_course = []
        t_count = 1
        desc = u'%s年%s月%s 到 %s月%s号, 周一至周六, %s 上课'
        times = ["09:00", "09:30", "10:00", "11:00", "12:30", "13:00", "13:30", "14:00",
                 "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:30", "19:30",
                 "20:00", "20:30"]
        c = db.get("select count(*) as counts from mid_teacher")
        t_time_id = db.get("select max(time_id) as time_id from mid_workroom_single")
        if c:
            t_count = c.counts + 1
        if t_time_id and t_time_id.time_id:
            t_time_id = t_time_id.time_id
        else:
            t_time_id = 1
        course = db.query("select * from mid_course where finished=0 and claId=%s", cla_id)
        if course:
            check = db.query("select * from mid_course_workroom where cla_id=%s limit 1", cla_id)
            if check:
                return msg(False, "已经开过班了")
            if len(course) > 1:
                return msg(False, "有重复的班级ID")
            else:
                course = course[0]
            start = datetime(*map(lambda _x: int(_x), course.start_date.split("-")))
            end = datetime(*map(lambda _x: int(_x), course.end_date.split("-")))
            max_person = course.max_person
            dates = [(start + timedelta(days=d)) for d in range(0, (end - start).days + 1)]
            teachers = [("test" + str(c), "test" + str(c), "test" + str(c) + "full name")
                        for c in range(t_count + 1, t_count + max_person + 1)]
            teachers_1 = [("TKtest" + str(c), "TKtest" + str(c), "TKtest" + str(c) + "full name")
                          for c in range(t_count + 1, t_count + max_person + 1)]
            for ttm in times:
                for t1 in teachers_1:
                    wr_id_s = "T-" + string.replace(ttm, ":", '') + "-K1-" + t1[0]
                    wr_course.append((cla_id, wr_id_s))
                    stu_id_s = "t-" + string.replace(ttm, ":", '') + "-k1-" + t1[0]
                    t_time_id += 1
                    workroom_s.append((wr_id_s, cla_id, t_time_id, "A", t1[0],
                                       "2014-08-25", ttm, 2, stu_id_s,
                                       "normal", "2014年8月25日 %s 上课" % ttm))
            for i in workroom_s:
                print i
            for tm in times:
                for tc in teachers:
                    wr_id = "A-" + string.replace(tm, ":", '') + "-K1-" + tc[0]
                    wr_course.append((cla_id, wr_id))
                    stu_id = "a-" + string.replace(tm, ":", '') + "-k1-" + tc[0]
                    workroom.append((wr_id, "A", tc[0], tm, stu_id, "normal",
                                     desc % (dates[0].year, dates[0].month, dates[0].day,
                                             dates[-1:][0].month, dates[-1:][0].day, tm)))
                    class_type = 1
                    for dt in dates:
                        if class_type == 1:
                            class_type = 7
                        elif class_type == 7:
                            class_type = 2
                        wd_datas.append((wr_id, dt, class_type))
            auto_commit(False)
            for te in teachers + teachers_1:
                print te
            for wr in workroom:
                print wr
            for wrs in workroom_s:
                print wrs
            r_t = db.executemany_rowcount("insert into mid_teacher (id, shortname, fullname) values(%s, %s, %s)",
                                          teachers + teachers_1)
            if r_t:
                r_t1 = workroom_model.add(workroom)
                if r_t1:
                    r_t2 = workroom_dates_model.add(wd_datas)
                    if r_t2:
                        r_t3 = course_wr_model.add_by(wr_course)
                        if r_t3:
                            r_t4 = workroom_single.add(workroom_s)
                            if r_t4:
                                commit()
                                auto_commit()
                                return msg()
            rollback()
            return msg(False, "数据插入失败")
    except:
        print traceback.format_exc()
        rollback()
    finally:
        auto_commit()


def test_relation_class():
    db.execute("insert into mid_course_workroom (cla_id, workroom) "
               "select %s, id from mid_workroom where term=%s", "ff80808146463d430146476fad76003d", "A")

# test_relation_class()

def test_add_course_workroom():
    cla_id = "ff80808146463d430146476fad76003d"
    return course_wr_model.add(cla_id, "A")
# print test_add_course_workroom()


def test_list_class():
    return logic_model.list_class(cla_id, teacher='Sumi', t_interval='12:00:00-14:00:00', p_no=1)
# counts, results = test_list_class()
# for r in results:
#     print r.id_dates


def test_select_class():
    return logic_model.select_class(uid=uid, cla_id=cla_id, workroom="A-1230-c101")
# print transaction(test_select_class())


def test_get_selected():
    return selected.check_select(uid, cla_id)
# print test_get_selected()


def test_pay():
    return logic_model.pay(uid="1234", cla_id=cla_id)
# print test_pay()


def test_get_classes():
    return student_classes.full_query(uid=uid+"refund", cla_id=cla_id)
# for r in test_get_classes():
#     print r


def test_query_single():
    return workroom_single.query_all(1, 10, cla_id=cla_id, status="normal")
# print test_query_single()


def test_change_date():
    return logic_model.change_date(cla_id=cla_id, uid=uid, src_time_id=13, target_time_id=1000001)
# print test_change_date()


def test_change_class():
    return logic_model.change_class(cla_id=cla_id, uid=uid, target_wr='A-1430-c101')
# transaction(test_change_class)


def test_refund():
    return logic_model.refund(cla_id=cla_id, uid=uid)
# transaction(test_refund)
