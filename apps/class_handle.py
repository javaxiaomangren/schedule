__author__ = 'windy'
#coding: utf-8
import traceback
import httplib
import ujson
from collections import OrderedDict

import tornado.web
from torndb import Row
from tornado.log import gen_log as logger
from utils import route


class GRADEStatus(object):
    """
       班级状态：0表示可用，1预约，2已支付，3.退款
    """
    NORMAL = 0
    APPOINTED = 1
    PAYED = 2
    REFUND = 3
    CHANGED = 4


class ClassStatus(object):
    """
      课程状态：0可预约，1已经支付，2完成，3请假，4退课，5补课
    """
    NORMAL = 0
    PAYED = 1
    FINISHED = 2
    ABSENT = 3
    REFUND = 4
    CHANGED = 5


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

    def get_current_user(self):
        pass

    def get_error_html(self, status_code, **kwargs):

        try:
            template = "admin/404.html"
            msg = httplib.responses[status_code]
            exception = "%s\n\n%s" % (kwargs["exception"], traceback.format_exc())
            return self.render_string(template,
                                      code=status_code,
                                      message=msg,
                                      exception=exception)
        except:
            return self.write("Server error")

    def initialize(self):
        print "please define your initialize..............."


#====================== Commons Methods ==========
def message(flag="success", code=200, msg="Success"):
    ms = Row()
    ms["flag"] = flag
    ms["code"] = code
    ms["message"] = msg
    return ms


def update_grade_status(db, grade_id, status):
    """
        更新班级状态
    """
    return db.execute_rowcount("UPDATE grade SET status=%s WHERE grade_id=%s", status, grade_id)


def student_add_class(db, student_id, grade_id, status):
    """
    选课成功后：
       添加课程信息到学生课程表
    """
    return db.execute_rowcount("INSERT INTO student_class(student_id, class_id, status) "
                               "SELECT %s, g.class_id, %s FROM grade g "
                               "WHERE g.grade_id = %s", student_id, status, grade_id)

format_date = lambda x, y: "%s %s" % (x, y)


def set_value(dc, value):
    """
       设置聚合的课程返回信息给 speiyou.com
    """
    old = dc.get(value.grade_id)
    classes = OrderedDict()
    #result["courseName"] = row.course_name
    classes["classId"] = value.class_id
    classes["teacherId"] = value.teacher_id
    #result["teacherName"] = row.teacher_name
    classes["classRoom"] = value.class_room
    classes["classDate"] = str(value.class_date)
    classes["classTime"] = str(value.start_time)
    classes["period"] = value.period
    classes["classStatus"] = value.class_status

    if old:
        data_list = old.get("classes")
        data_list.append(classes)
        old["classes"] = data_list
    else:
        result = OrderedDict()
        result["gradeId"] = value.grade_id
        result["courseId"] = value.course_id
        result["studentId"] = None
        result["classes"] = [classes]
        result["status"] = value.status
        dc[value.grade_id] = result


def set_for_list(dc, value):
    """
        设置聚合信息给选课列表
    """
    old = dc.get(value.grade_id)
    clazz = Row()
    clazz["id"] = value.class_id
    clazz["date"] = str(value.class_date)
    clazz["time"] = str(value.start_time)

    if old:
        classes = old.classes
        classes.append(clazz)
    else:
        new = Row()
        new["teacher_id"] = value.teacher_id
        new["course_id"] = value.course_id
        new["grade_id"] = value.grade_id
        new["period"] = value.period
        new["classes"] = [clazz]
        dc[value.grade_id] = new


def aggregate_by_grade(rows, set_method):
    """
        聚合课程信息，聚合同一班级下的课程
    """
    grade_dic = Row()
    for value in rows:
        set_method(grade_dic, value)
    return grade_dic

#=======================Api to speiyou.com=============

@route("/api/course/add", name="Add Course")
class APIAddCourseHandle(BaseHandler):
    """
        开课请求接口
        调用方式：post 参数，json格式
    """
    def post(self, *args, **kwargs):
        data = self.request.body
        try:
            data = ujson.loads(data)
        except:
            self.write("Request Parameter Error")
            return
        try:
            p = Row(data)
            self.db.execute_rowcount("INSERT INTO course(id, class_count, every_hours,"
                                     "start_date, end_date, frequency, year, term_name,"
                                     " max_person, create_date, finished) "
                                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)",
                                     p.id, p.classCount, p.everyHours, p.startDate, p.endDate,
                                     p.frequency, p.year, p.termName, p.maxPersons)
            self.write({"rlt": True, "msg": "success"})
        except:
            self.write({"rlt": False, "msg": traceback.format_exc()})


@route("/api/class/cancel")
class APICancelClassHandle(BaseHandler):
    """
    撤销锁定课程
    """
    def get(self):
        pass


@route("/api/class/payed")
class APICancelClassHandle(BaseHandler):
    """
    订单支付，接收通知，写入学生－课程表
    """
    def get(self):
        pass


@route("/api/class/refund")
class APICancelClassHandle(BaseHandler):
    """
    接收退款通知
    """
    def get(self):
        pass


#======================== 调用speiyou.com的接口========
def notify_():
    pass


#======================== 选课调课logic ==============
@route("/grade")
class GradeHandle(BaseHandler):
    """
    选课列表
    """
    def get(self):
        #分页暂时不考虑和关联查询
        status = self.get_argument("status", GRADEStatus.NORMAL)
        rows = self.db.query("SELECT * FROM grade g JOIN class c ON(g.class_id=c.class_id) "
                             "WHERE g.status=%s", status)
        grades = aggregate_by_grade(rows, set_for_list)
        self.render("grade_list.html", grades=grades.values())



@route("/grade/(\d+)/order/(.*)$", name="Order class")
class GradeOrderHandle(BaseHandler):
    """
        Order class, It just lock this class. Disappear from the class list page.
        It will be released or ordered while get a notification from speiyou.com
        status: 0 means release, 2 payed, 3 refunded
        Invoke example:
            Lock class:
                http://host:port/grade/1/order/1
            Release or order Success:
                http://host:port/grade/1/order/1?status=2

    """

    def get(self, grade_id, student_id):

        try:
            status = int(self.get_argument("status"))
        except:
            self.write(message("Error", 400, "Request Parameter Error"))
            return

        #todo check permission, 401

        if student_id and grade_id:
            if status:
                #========== Release this Class ==================
                if status == GRADEStatus.NORMAL:
                    update_grade_status(self.db, grade_id, status)
                    #TODO update cache
                    # maybe there need a table to record student's operation. TODO
                    self.write(message(msg="release class %s success" % grade_id))
                elif status == GRADEStatus.APPOINTED:
                    update_grade_status(self.db, grade_id, status)
                    # TODO Update cache
                    # TODO notify speiyou.com
                    self.write("Jump to the pay page")

                #========= Class was payed ======================
                elif status == GRADEStatus.PAYED:
                    update_grade_status(self.db, grade_id, status)
                    #TODO INSERT INTO STUDENT_CLASS TABLE
                    self.write("Student %s has bout grade %s ", student_id, grade_id)

                #========= The student refunded this class =========
                elif status == GRADEStatus.REFUND:
                    update_grade_status(self.db, grade_id, status)
                    #TODO UPDATE CLASS STATUS

#========= Bad Request =========
                else:
                    self.write(message(flag="Error", code=402, msg="Bad Request unknown value of status"))
        else:
            self.write(message("Error", 400, "Request Parameter Error, Student and Grade must be specific"))


@route("/grade/(\d+)/change/(\d+)/(\d+)", name="Change Grade")
class ChangeGradeHandle(BaseHandler):
    """
    转班
    """
    def get(self, old_grade_id, student, new_grade_id):
        try:
            #TODO could his have permission to change grade.

            #TODO transaction(1.disable old class, 2.select a new class, 3.notify speiyou.com)
            self.auto_commit(False)
            #disable old class
            self.db.execute_rowcount("UPDATE student_class sc INNER JOIN grade g ON g.class_id = sc.class_id "
                                     "SET sc.status=%s WHERE g.grade_id=%s", GRADEStatus.CHANGED, old_grade_id)
            #disable his grade
            update_grade_status(self.db, GRADEStatus.CHANGED, old_grade_id)
            #lock the selected class
            update_grade_status(self.db, GRADEStatus.PAYED, new_grade_id)
            #insert new class
            student_add_class(self.db, student, new_grade_id, GRADEStatus.PAYED)
            # Return new grade id to speiyou.com TODO
            self.commit()
            # Jump to where TODO
            self.write(message(msg=new_grade_id))
        except:
            self.write_error(500)
        finally:
            self.auto_commit()


@route("/class/(\d+)/(absent)/(\d+)/(\d+)", name="Change class")
class TestClassHandle(BaseHandler):
    """
    转班
    """
    def get(self, old_grade_id, action, student, new_grade_id):
        print old_grade_id, student, new_grade_id, action
        self.write("hello")


#===============================后台管理=====================
@route("/admin", name="Admin Manager")
class AdminClassHandle(BaseHandler):
    def get(self, *args, **kwargs):
        pass