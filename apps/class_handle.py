__author__ = 'windy'
#coding: utf-8
import traceback
import httplib
import ujson
from collections import OrderedDict
from datetime import timedelta

import tornado.web
from torndb import Row
from utils import route


class TimeStatus(object):
    """
      课程状态：0可预约，1已经支付，2完成，3请假，4退课，5补课, 6试听课程
    """
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
        pass

    def get_error_html(self, status_code, **kwargs):

        try:
            template = "404.html"
            msg = httplib.responses[status_code]
            exception = "%s\n\n%s" % (kwargs["exception"], traceback.format_exc())
            return self.render_string(template,
                                      code=status_code,
                                      message=msg,
                                      exception=exception)
        except:
            return self.write("Server error")

    def initialize(self):
        pass


#====================== Commons Methods ==========
def message(rlt=True, code=200, msg="Success"):
    ms = Row()
    ms["rlt"] = rlt
    ms["code"] = code
    ms["msg"] = msg
    ms["data"] = None
    return ms


def select_class(db, course_id, class_id, student_id, status_new, status_old):
    """
    选课操作：
    插入学生ID到数据库， 更新课程状态为1
    """
    return db.execute_rowcount("UPDATE timetable SET student_id=%s, class_status=%s "
                               "WHERE course_id=%s AND class_id=%s AND class_status=%s",
                               student_id, status_new, course_id, class_id, status_old)


format_date = lambda x, y: "%s %s" % (x, y)


def check_params(args, lens, keys):
    if len(args) > lens:
        return False
    for p in args.keys():
        if not p in keys:
            return False
    return True


def args_value(args):
    _value = {}
    for k in args:
        _value[k] = args.get(k)[0]
    return _value


def set_response(dc, value):
    """
       设置聚合的课程返回信息给 speiyou.com
    """
    old = dc.get(value.class_id)
    classes = OrderedDict()
    #result["courseName"] = row.course_name
    classes["timeId"] = value.time_id
    classes["teacherId"] = value.teacher_id
    # classes["teacherName"] = value.teacher_name
    classes["classRoom"] = value.class_room
    classes["classDate"] = str(value.class_date)
    classes["startTime"] = str(value.start_time)
    classes["endTime"] = str(value.start_time + timedelta(minutes=value.period))
    # classes["timeStatus"] = TimeStatus.NAME.get(value.time_status)
    # classes["checkRoll"] = value.check_roll

    if old:
        data_list = old.get("classes")
        data_list.append(classes)
        old["classes"] = data_list
    else:
        result = OrderedDict()
        result["claId"] = value.course_id
        result["planId"] = value.class_id
        result["uid"] = value.student_id
        result["classes"] = [classes]
        dc[value.class_id] = result


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
        new["classes"] = [clazz]
        dc[value.class_id] = new


def set_for_my(dc, value):
    """
        设置聚合信息给选课列表
    """
    old = dc.get(value.class_id)
    clazz = Row()
    clazz["time_id"] = value.time_id
    clazz["date"] = str(value.class_date)
    clazz["time"] = str(value.start_time)
    clazz["period"] = value.period
    clazz["time_status"] = value.time_status
    clazz["teacher_id"] = value.teacher_id
    clazz["teacher_name"] = value.teacher_name
    clazz["check_roll"] = value.check_roll

    if old:
        classes = old.classes
        classes.append(clazz)
    else:
        new = Row()
        new["course_id"] = value.course_id
        new["course_name"] = value.course_name
        new["class_id"] = value.class_id
        new["class_room"] = value.class_room
        new["student_id"] = value.student_id
        new["teacher_name"] = value.teacher_name
        new["class_status"] = value.class_status
        new["time_desc"] = value.time_desc
        new["time_changed"] = value.time_changed
        new["class_changed"] = value.class_changed
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


def update_class_status(db, course_id, class_id, student_id, old_status, new_status):
    return db.execute_rowcount("UPDATE timetable SET class_status=%s "
                               "WHERE course_id=%s AND class_id=%s AND student_id=%s AND class_status=%s",
                               new_status, course_id, class_id, student_id, old_status)


def get_query_where(course_id, teacher_name, time_interval):
    where = "WHERE class_status=0 AND course_id=%s " % course_id
    if teacher_name:
        where += " AND teacher_name='%s' " % teacher_name
    if time_interval and "-" in time_interval:
        t1, t2 = time_interval.split('-')
        where += " AND start_time BETWEEN '%s' AND '%s' " % (t1, t2)
    return where


def query_timetables(db, course_id, where, page_no, page_size):
    sql = "SELECT distinct class_id FROM timetable "
    limit = " LIMIT %s, %s " % ((page_no - 1) * page_size, page_size)
    class_ids = db.query(sql + where + limit)
    if class_ids:
        ids = ','.join(map(lambda x: str(x.class_id), class_ids))
        query_sql = "SELECT * FROM timetable WHERE class_status=0 AND course_id=%s " \
                    "AND class_id IN(%s) ORDER BY start_time" % (course_id, ids)
        rows = db.query(query_sql)
        return aggregate_by_grade(rows, set_for_list)
    else:
        return {}
#=======================Api to speiyou.com=============

@route("/api/class/add", name="Ask For Timetable")
class APIAddClassHandle(BaseHandler):
    """
        开课请求接口
        调用方式：post 参数，json格式
    """
    def post(self, *args, **kwargs):
        data = self.request.body
        try:
            data = ujson.loads(data)
        except:
            self.write(message(False, 400, "请求参数异常"))
            return
        try:
            p = Row(data)
            self.db.execute_rowcount("INSERT INTO course(id, class_count, every_hours,"
                                     "start_date, end_date, frequency, year, term_name,"
                                     " max_person, create_date, finished) "
                                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)",
                                     p.id, p.classCount, p.everyHours, p.startDate, p.endDate,
                                     p.frequency, p.year, p.termName, p.maxPersons)
            self.write(message())
        except:
            self.write(message(False, 400, "请求失败:" + traceback.format_exc()))


@route("/api/class/timetable/list", name="List TimeTables ")
class TimeTableListHandle(BaseHandler):
    """
     请求课表页面
    /api/class/timetable/list?claId=&uid=
    oldPlanId是可选的，有值表示转班
    /api/class/timetable/list?claId=&uid=&oldPlanId

    """
    def get(self):
        args = self.request.query_arguments
        checked = check_params(args, 6, ["claId", "uid", "oldPlanId", "status", "teacherName", "timeInterval", "pageNo"])
        if not checked:
            self.write(message(False, 400, "Bad Request"))
            #TODO BAD PAGE
            return

        course_id = self.get_argument("claId", None)
        student_id = self.get_argument("uid", None)
        # old_class_id = self.get_argument("oldPlanId", None)
        teacher_name = self.get_argument("teacherName", None)
        time_interval = self.get_argument("timeInterval", None)
        page_no = int(self.get_argument("pageNo", 1))
        page_size = 10
        if course_id and student_id:
            where = get_query_where(course_id, teacher_name, time_interval)
            total_count = self.db.get("SELECT COUNT(DISTINCT class_id) as total FROM timetable %s " % where).total
            page_count = (total_count + page_size - 1)/page_size
            if page_no > page_count:
                page_no = page_count
            if page_no < 1:
                page_no = 1
            timetable = query_timetables(self.db, course_id, where, page_no, page_size)
            self.render("timetable_list.html", entries=timetable.values(),
                        args=args_value(args), page_count=page_count, page_no=page_no)
        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/api/class/manage", name="Timetable Manage")
class MyClassHandler(BaseHandler):
    """
    学生课程管理页面
    /api/class/manage?uid=&claId=&planId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 3, ["uid", "claId", "planId"])
        if not checked:
            self.write(message(False, 400, "Bad Request"))
            #TODO BAD PAGE
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        if student_id and course_id and class_id:
            rows = self.db.query("SELECT * FROM timetable WHERE student_id=%s AND course_id=%s AND class_id=%s "
                                 "ORDER BY class_date", student_id, course_id, class_id)
            class_time = aggregate_by_grade(rows, set_for_my)
            self.render("my_timetable.html", entries=class_time.values(), studentId=student_id)
        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/timetable/select", name="select class Timetable")
class TimetableSelectHandle(BaseHandler):
    """
    学生选课
    /timetable/select?uid=&claId=&planId=&oldPlanId=
    如果oldPlanId 不为空表示转班
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 4, ["uid", "claId", "planId", "oldPlanId"])
        if not checked:
            self.write(message(False, 400, "Bad Request"))
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        old_class_id = self.get_argument("oldPlanId", None)
        if student_id and course_id and class_id:
            if old_class_id:
                #TODO 转班
                #.记录
                #. 跟新原来的
                #. 插入新的
                #. 返回数据
                try:
                    self.auto_commit(False)
                    record = self.db.query("SELECT class_changed, time_changed FROM timetable "
                                           "WHERE course_id=%s AND class_id=%s AND student_id=%s LIMIT 1",
                                           course_id, old_class_id, student_id)

                    class_changed, time_changed = record[0].class_changed, record[0].time_changed
                    if class_changed > 2:
                        self.write(message(False, 403, "不能再转班了"))
                        return
                    self.db.execute_rowcount("INSERT INTO timetable_record SELECT * FROM timetable "
                                             "WHERE course_id=%s AND class_id=%s AND student_id=%s",
                                             course_id, old_class_id, student_id)
                    self.db.execute_rowcount("UPDATE timetable SET student_id=NULL "
                                             "WHERE course_id=%s AND class_id=%s AND student_id=%s",
                                             course_id, old_class_id, student_id)
                    rs = self.db.execute_rowcount("UPDATE timetable SET student_id=%s, class_status=%s, time_status=%s,"
                                                  "time_changed=%s, class_changed=%s "
                                                  "WHERE course_id=%s AND class_id=%s AND class_status=%s",
                                                  student_id, TimeStatus.PAYED, TimeStatus.PAYED, time_changed,
                                                  class_changed + 1, course_id, class_id, TimeStatus.NORMAL)
                    if rs:
                        new_class = self.db.query("SELECT * FROM timetable "
                                                  "WHERE course_id=%s AND class_id=%s AND student_id=%s",
                                                  course_id, class_id, student_id)
                        self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s "
                                                 "WHERE course_id=%s AND class_id=%s AND student_id=%s "
                                                 "AND class_date < NOW()", TimeStatus.FINISHED, TimeStatus.FINISHED,
                                                 course_id, class_id, student_id)
                        new_dates = aggregate_by_grade(new_class, set_response).values()[0]
                        result = OrderedDict()
                        result["oldPlan"] = {"claId": course_id, "planId": old_class_id, "uid": student_id}
                        result["newPlan"] = new_dates
                        self.write(result)
                        #TODO SEND DATA TO SPEIYOU.COM
                        self.commit()
                    else:
                        self.rollback()
                        self.write(message(False, 403, "非法操作,没有可转班级"))
                except:
                    self.rollback()
                    print traceback.format_exc()
                    self.write(message(False, 500, traceback.format_exc()))
                finally:
                    self.auto_commit()

            else:
                exists = self.db.query("SELECT class_id, class_status FROM timetable"
                                       " WHERE student_id=%s LIMIT 1", student_id)
                #如果只是预约状态，可以重新选课
                if exists:
                    cid = exists[0].class_id
                    status = exists[0].class_status
                    if status == 1:
                        try:
                            self.auto_commit(False)
                            rs1 = self.db.execute_rowcount("UPDATE timetable SET student_id=null, class_status=0 "
                                                           "WHERE class_id=%s AND student_id=%s", cid, student_id)
                            if rs1:
                                rs = select_class(self.db, course_id, class_id, student_id,
                                                  TimeStatus.APPOINTED, TimeStatus.NORMAL)
                                if rs:
                                    self.commit()
                                else:
                                    self.rollback()
                                    class_id = cid
                            self.auto_commit()
                        except:
                            self.rollback()
                            self.write(message(False, 500, traceback.format_exc()))
                        finally:
                            self.auto_commit()

                    else:
                        class_id = cid
                else:
                    rs = select_class(self.db, course_id, class_id, student_id,
                                      TimeStatus.APPOINTED, TimeStatus.NORMAL)
                    if not rs:
                        self.write(message(False, 403, "该课程不能选了"))
                        return

                self.redirect("/api/class/manage?uid=%s&claId=%s&planId=%s" % (student_id, course_id, class_id))
                #TODO 跳转到培优网页面
                #TODO 调用培优系统，修改报课的排课，可能多次

        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/timetable/change", name="Change class")
class TimetableClassChangeHandle(BaseHandler):
    """
    学生转班
    /timetable/change?planId=&uid=&claId=&newPlanId
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 4, ["uid", "claId", "planId", "oldPlanId"])
        if not checked:
            self.write(message(False, 400, "Bad Request"))
            #TODO BAD PAGE
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        if student_id and course_id and class_id:
            select_class(self.db, course_id, class_id, student_id, TimeStatus.APPOINTED, TimeStatus.NORMAL)
            rows = self.db.query("SELECT * FROM timetable "
                                 "WHERE class_status=%s AND course_id=%s AND class_id=%s AND student_id=%s",
                                 TimeStatus.APPOINTED, course_id, class_id, student_id)
            timetable = aggregate_by_grade(rows, set_for_list)
            self.write(timetable)
            #TODO 返回数据到培优网
        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/timetable/change/time/list", name="class time list")
class BakTimeListHandle(BaseHandler):
    """
    查询可调课列表
    /timetable/change/time/list?planId=&uid=&claId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 7,
                               ["uid", "claId", "planId", "timeId", "teacherName", "timeInterval", "pageNo"])
        if not checked:
            self.write(message(False, 403, "参数不对"))
            return
        else:
            student_id = self.get_argument("uid", None)
            course_id = self.get_argument("claId", None)
            class_id = self.get_argument("planId", None)
            time_id = self.get_argument("timeId", None)

            if student_id and course_id and class_id and time_id:
                old_row = self.db.get("SELECT * FROM timetable "
                                      "WHERE time_id=%s AND student_id=%s AND class_id=%s",
                                      time_id, student_id, class_id)

                teacher_name = self.get_argument("teacherName", None)
                time_interval = self.get_argument("timeInterval", None)
                page_no = int(self.get_argument("pageNo", 1))
                where = "WHERE flag=0 "
                if teacher_name:
                    where += " AND teacher_name='%s' " % teacher_name
                if time_interval and "-" in time_interval:
                    t1, t2 = time_interval.split('-')
                    where += " AND start_time BETWEEN '%s' AND '%s' " % (t1, t2)
                total_count = self.db.get("SELECT COUNT(*) as total FROM timetable_bak %s " % where).total
                page_size = 10
                page_count = (total_count + page_size - 1)/page_size
                if page_no > page_count:
                    page_no = page_count
                if page_no < 1:
                    page_no = 1
                limit = " LIMIT %s, %s " % ((page_no - 1) * page_size, page_size)
                rows = self.db.query("SELECT * FROM timetable_bak %s ORDER BY start_time %s" % (where, limit))
                self.render("bak_time.html", entries=rows, old_entry=old_row,
                            args=args_value(self.request.query_arguments), page_no=page_no,
                            page_count=page_count)
            else:
                self.write(message(False, 400, "请求参数不对"))


@route("/timetable/change/time", name="change class time")
class TimetableTimeChangeHandle(BaseHandler):
    """
    调课
    /timetable/change/time?planId=&uid=&claId=&timeId&newTimeId
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 5, ["uid", "claId", "planId", "timeId", "newTimeId"])
        if not checked:
            self.write("Bad Request")
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        time_id = self.get_argument("timeId", None)
        time_id_new = self.get_argument("newTimeId", None)
        if student_id and course_id and class_id and time_id and time_id_new:
            old_row = self.db.get("SELECT * FROM timetable WHERE time_id=%s "
                                  "AND student_id=%s AND course_id=%s AND class_id=%s",
                                  time_id, student_id, course_id, class_id)
            row = self.db.get("SELECT * FROM timetable_bak WHERE id=%s AND flag=0 ", time_id_new)
            if old_row and row:
                try:
                    self.auto_commit(False)
                    #进攻式SQL,如果更新成功，表明没有调过课程
                    rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s, time_changed=1 "
                                                  "WHERE time_id=%s AND class_id=%s "
                                                  "AND student_id=%s AND time_changed=%s", TimeStatus.CHANGED,
                                                  TimeStatus.CHANGED, time_id, class_id, student_id, 0)
                    if rs:
                        last_time_id = \
                            self.db.execute_lastrowid("INSERT INTO timetable (course_id, course_name, class_id,"
                                                      "class_room, teacher_id, teacher_name, student_id, start_time,"
                                                      "period, class_date, class_status, time_status, time_desc, "
                                                      "check_roll, class_changed) VALUES"
                                                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                                      course_id, old_row.course_name, class_id, row.class_room,
                                                      row.teacher_id, row.teacher_name, student_id, row.start_time,
                                                      row.period, row.class_date, TimeStatus.PAYED, TimeStatus.PAYED,
                                                      old_row.time_desc, old_row.check_roll, old_row.class_changed)
                        self.db.execute_rowcount("UPDATE timetable_bak SET flag=1 WHERE id=%s", time_id_new)
                        self.db.execute_rowcount("UPDATE timetable SET time_changed=1 "
                                                 "WHERE course_id=%s AND class_id=%s AND student_id=%s",
                                                 course_id, class_id, student_id)
                        #TODO notify speiyou.com

                        result = OrderedDict()

                        result["uid"] = student_id
                        result["claId"] = course_id
                        result["cucId"] = class_id
                        result["sourceTimeId"] = time_id
                        result["sourceTeacherId"] = old_row.teacher_id
                        result["sourceCourseDate"] = str(old_row.class_date)
                        result["sourceStartTime"] = str(old_row.start_time)
                        result["sourceEndTime"] = str(old_row.start_time + timedelta(minutes=old_row.period))
                        result["sourceClassRoomName"] = old_row.class_room
                        result["targetTimeId"] = last_time_id
                        result["targetTeacherId"] = row.teacher_id
                        result["targetCourseDate"] = str(row.class_date)
                        result["targetStartTime"] = str(row.start_time)
                        result["targetEndTime"] = str(row.start_time + timedelta(minutes=row.period))
                        result["targetClassRoomName"] = row.class_room

                        self.write(result)
                        #TODO invoke speiyou 1
                        self.commit()
                    else:
                        self.write(message(False, 403, "不能调课了"))
                    self.auto_commit()
                except:
                    print traceback.format_exc()
                    self.rollback()
                finally:
                    self.auto_commit()
            else:
                self.write(message(False, 400, "请求错误， 没有查询到调课信息"))
        else:
            self.write(message(False, 400, "请求参数不对"))




@route("/api/class/release", name="Release Timetable")
class APIClassReleaseHandle(BaseHandler):
    """
    撤销课表锁定-消息互通接口
    /api/class/release?claId=&uid=&plaId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 3, ["uid", "claId", "planId"])
        if not checked:
            self.write(message(False, 400, "请求参数不对"))
            return
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        student_id = self.get_argument("uid", None)
        if course_id and class_id and student_id:
            rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, student_id=Null "
                                          "WHERE course_id=%s AND class_id=%s AND student_id=%s"
                                          " AND class_status=%s", TimeStatus.NORMAL, course_id,
                                          class_id, student_id, TimeStatus.APPOINTED)
            if rs:
                self.write(message())
            else:
                self.write(message(False, 400, "没有任何更新"))
        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/api/class/payed", name="Get payed notify")
class APIClassPayedHandle(BaseHandler):
    """
    学生支付课程-消息互通接口
    /api/class/payed?claId=&uid=&plaId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 3, ["uid", "claId", "planId"])
        if not checked:
            self.write(message(False, 400, "请求参数不对"))
            return
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        student_id = self.get_argument("uid", None)
        if course_id and class_id and student_id:
            try:
                self.auto_commit(False)
                rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s "
                                              "WHERE course_id=%s AND class_id=%s AND student_id=%s "
                                              "AND class_status=%s", TimeStatus.PAYED, TimeStatus.PAYED,
                                              course_id, class_id, student_id, TimeStatus.APPOINTED)

                if rs:
                    rows = self.db.query("SELECT * FROM timetable "
                                         "WHERE course_id=%s AND class_id=%s AND student_id=%s",
                                         course_id, class_id, student_id)
                    data = aggregate_by_grade(rows, set_response).values()[0]
                    self.write({"rlt": True, "code": 200, "msg": "Success", "data": data})
                    self.commit()
                    #TODO invoke by speiyou2
                else:
                    self.write(message(False, 400, "更新失败"))
            except:
                self.rollback()
            finally:
                self.auto_commit()
        else:
            self.write(message(False, 400, "请求参数不对"))


@route("/api/class/refund", name="Get refunded notify")
class APIClassRefundHandle(BaseHandler):
    """
     学生退费-消息互通接口
    /api/class/refund?claId=&uid=&plaId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 3, ["uid", "claId", "planId"])
        if not checked:
            self.write(message(False, 400, "请求参数不对"))
            return
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        student_id = self.get_argument("uid", None)
        if course_id and class_id and student_id:
            rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s "
                                          "WHERE course_id=%s AND class_id=%s AND student_id=%s "
                                          "AND class_status=%s", TimeStatus.REFUND, TimeStatus.REFUND,
                                          course_id, class_id, student_id, TimeStatus.PAYED)

            if rs:
                self.write(message())
            else:
                self.write(message(False, 400, "更新失败"))

        else:
            self.write(message(False, 400, "请求参数不对"))


#===============================后台管理=====================
@route("/admin", name="Admin Manager")
class AdminClassHandle(BaseHandler):
    def get(self):
        self.render("admin/base.html")


@route("/admin/course/tasks", name="class Tasks")
class CourseTasksClassHandle(BaseHandler):
    def get(self):
        rows = self.db.query("select * from course ")
        self.render("admin/list_course_task.html", entries=rows)

