__author__ = 'windy'
#coding: utf-8

from base import *
from db_model import BaseDBModel
from http_msg import *


#====================== Commons Methods ==========
def get_param(request):
    """获取参数"""
    data = ujson.loads(request.body)
    course_id = data.get("claId", None)
    student_id = data.get("uid", None)
    return course_id, student_id

format_date = lambda x, y: "%s %s" % (x, y)


def args_value(args):
    _value = {}
    for k in args:
        _value[k] = args.get(k)[0]
    return _value


def check_params(args, lens, keys):
    if len(args) > lens:
        return False
    for p in args.keys():
        if not p in keys:
            return False
    return True


#=======================Api to speiyou.com=============
@Route("/api/class/add", name="Ask For Timetable")
class APIAddClassHandle(BaseHandler):
    """
        开课请求接口
        调用方式：post 参数，json格式
    """
    def post(self, *args, **kwargs):
        data = self.request.body
        try:
            data = json.loads(data)
            p = Row(data)
            try:
                summary = p.claId+p.classCount+p.everyHours+p.startDate+p.endDate+p.frequency+p.year+p.termName+p.maxPersons
                if not authorization(summary, self.request.headers):
                    return self.write(msg(False, "authorization error"))
            except AttributeError:
                self.write(msg(False, "authorization error"))
        except:
            logger.info("/api/class/add, Error Msg {%s }" % traceback.format_exc())
            self.write(msg(False, "请求参数异常"))
            return
        try:
            self.db.execute_rowcount("REPLACE INTO mid_course(claId, class_name,class_count, every_hours,"
                                     "start_date, end_date, frequency, year, term_name,"
                                     " max_person, create_date, finished) "
                                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)",
                                     p.claId, p.claName, p.classCount, p.everyHours, p.startDate, p.endDate,
                                     p.frequency, p.year, p.termName, p.maxPersons)
            self.write(msg())
        except AttributeError as ae:
            self.write(msg(False, "%s 参数没有找到" % ae))
            logger.info(msg(False, "%s 参数没有找到" % ae))
        except SyntaxError as it:
            self.write(msg(False, "该课程已经存在 %s" % it))
            logger.info(msg(False, "该课程已经存在 %s" % it))


@Route("/", name="index")
class IndexHandler(BaseHandler):
    def get(self):
        self.render("xes-sk2.html")


@Route("/api/class/timetable/list", name="List TimeTables ")
class TimeTableListHandle(BaseHandler):
    """
     请求课表页面
    /api/class/timetable/list?claId=&uid=
    """
    def get(self):

        args = self.request.query_arguments
        checked = check_params(args, 6, ["claId", "uid", "teacherName", "timeInterval", "pageNo", "action"])
        if not checked:
            self.write(msg(False, "Bad Request"))
            logger.info("请求参数不对，非法请求")
            return

        cla_id = self.get_argument("claId", None)
        uid = self.get_argument("uid", None)
        teacher_name = self.get_argument("teacherName", None)
        time_interval = self.get_argument("timeInterval", None)
        page_no = int(self.get_argument("pageNo", 1))
        action = self.get_argument("action", 0)
        if cla_id and uid:
            page_count = self.db_model.count_classes(cla_id, teacher=teacher_name, t_interval=time_interval)
            if page_no > page_count:
                page_no = page_count
            if page_no < 1:
                page_no = 1
            tables = self.db_model.list_class(cla_id, teacher=teacher_name, t_interval=time_interval, p_no=page_no)
            selected = None
            if tables:
                flag, data = self.db_model.models.mss.check_select(uid, cla_id)
                if flag and data:
                    if data.deal != "selected":
                        return self.render("200.html", entry=msg(False, "You Already have a class"))
                    selected = self.db_model.models.mwr.get_full_by_id(data.workroom)
            self.render("list_timetable.html", entries=tables, action=action,
                        args=args_value(args), page_count=page_count,
                        page_no=page_no, selected=selected)
        else:
            self.write(msg(False, "请求参数不对"))
            logger.info(msg(False, "请求参数不对"))


@Route("/api/class/manage", name="Timetable Manage")
class MyClassHandler(BaseHandler):
    """
    学生课程管理页面
    /api/class/manage?uid=&claId=
    """
    def get(self):
        uid = self.get_argument("uid", None)
        cla_id = self.get_argument("claId", None)
        if uid and cla_id:
            # TODO remove zhushi
            # summary = student_id + course_id
            # if not authorization(summary, self.request.headers):
            #     self.write(msg(False, "authorization failed"))
            #     return
            will_start = (False, "None")
            class_table = self.db_model.models.msc.full_query(uid=uid, cla_id=cla_id)
            b, m = BaseDBModel.check_locked(class_table)
            if b:
                will_start = (b, m)

            class_change, selected_row = self.db_model.models.mss.check_will_change(cla_id=cla_id, uid=uid)
            date_change = self.db_model.models.msdc.check_has_changed(cla_id=cla_id, uid=uid)
            self.render("my_timetable.html", entries=class_table, uid=uid, cla_id=cla_id,
                        class_change=class_change, date_change=date_change, will_start=will_start)
        else:
            self.write(msg(False, "请求参数不对"))


@Route("/timetable/list/moodle", name="List In moodel")
class TimeTableForMoodel(BaseHandler):
    def get(self):
        uid = self.get_argument("uid", None)
        cla_id = self.get_argument("claId", None)
        if uid and cla_id:
            class_table = self.db_model.models.msc.full_query(uid=uid, cla_id=cla_id)
            self.render("list_class_for_moodle.html", entries=class_table)


@Route("/timetable/select", name="select class Timetable")
class TimetableSelectHandle(BaseHandler):
    """
    学生选课
    /timetable/select?uid=&claId=&workroom
    如果oldPlanId 不为空表示转班
    """
    def post(self):
        uid = self.get_argument("uid", None)
        cla_id = self.get_argument("claId", None)
        workroom = self.get_argument("workroom", None)
        if uid and cla_id and workroom:
            try:
                self.auto_commit(False)
                message = self.db_model.select_class(uid=uid, cla_id=cla_id, workroom=workroom)
                if message.rlt:
                    rs = reg_plan_status(uid, cla_id)
                    if rs.rlt:
                        self.commit()
                    else:
                        self.rollback()
                        return self.render("200.html", entry=msg(False, "Failed To invoke inter face "))
                else:
                    self.rollback()
                self.render("200.html", entry=message)
            except:
                self.rollback()
                logger.info(traceback.format_exc())
            finally:
                self.auto_commit()

        else:
            logger.info("请求参数不对 uid=%s, cla_id=%s, workroom=%s" % uid, cla_id)
            self.render("200.html", entry=msg(False,  "请求参数不对"))


@Route("/timetable/change", name="")
class ClassChangeQueryHandle(BaseHandler):
    """
    转班

    """
    def post(self, *args, **kwargs):
         #TODO post ask
        cla_id = self.get_argument("claId", None)
        target_workroom = self.get_argument("workroom", None)
        uid = self.get_argument("uid", None)
        try:
            rs = self.db_model.change_class(cla_id=cla_id, uid=uid, target_wr=target_workroom)
            if rs.rlt:
                h_s = courses(uid, cla_id, rs.msg)
                if h_s.rlt:
                    email = ""
                    for l in rs.msg:
                            email += "src workroom: {0:s}, src date:{1:s}--> " \
                                     "target workroom {0:s}, target date {1:s}\n\n" \
                                .format(l.get("sourceClassroom"), l.get("sourceCourseDate"),
                                        l.get("targetClassroom"), l.get("targetCourseDate"))
                    sendmail(msg=email, subject="%sStudent Changed WorkRoom" % datetime.now())
                    self.render("200.html", entry=msg())
                else:
                    self.rollback()
                    self.render("200.html", entry=msg(False, "Failed to invoke interface"))
            else:
                self.render("200.html", entry=rs)
        except:
            logger.info(traceback.format_exc())
            self.rollback()
            raise tornado.web.HTTPError(500, log_msg="转班失败")
        finally:
            self.auto_commit()



@Route("/timetable/change/time/list", name="class time list")
class BakTimeListHandle(BaseHandler):
    """
    查询可调课列表
    /timetable/change/time/list?planId=&uid=&claId=
    """
    def get(self):
        cla_id = self.get_argument("claId", None)
        #TODO page
        datas = self.db.query("SELECT ws.*, t.shortname "
                              "FROM mid_workroom_single ws "
                              "join mid_teacher t on t.id=ws.teacher "
                              "where status='normal' and  ws.cla_id=%s", cla_id)
        self.render("bak_time.html", entries=datas,
                    args=args_value(self.request.query_arguments))


@Route("/teacher", name="class time list")
class BakTimeListHandle(BaseHandler):
    """
    查询可调课列表
    /timetable/change/time/list?planId=&uid=&claId=
    """
    def get(self):
        tid = self.get_argument("tid")
        if not tid:
            self.render("teacher/xes-teacher.html")
        else:
            self.render("teacher/xes-teacher-%s.html" % tid)


@Route("/timetable/change/time", name="change class time")
class TimetableTimeChangeHandle(BaseHandler):
    """
    /timetable/change/time?planId=&uid=&claId=&timeId&newTimeId
    """
    def post(self):
        uid = self.get_argument("uid", None)
        cla_id = self.get_argument("claId", None)
        old_time_id = self.get_argument("oldTimeId", None)
        new_time_id = self.get_argument("newTimeId", None)
        if uid and cla_id and old_time_id and new_time_id:
            try:
                self.auto_commit(False)
                rs = self.db_model.change_date(cla_id=cla_id, uid=uid,
                                               src_time_id=old_time_id,
                                               target_time_id=new_time_id)
                if rs.rlt:
                    # TODO remember to remove comment
                    http_rsl = courses(uid, cla_id, rs.msg)
                    if http_rsl.rlt:
                        self.commit()
                        sendmail(msg=rs.email, subject="%s Change Class Date" % datetime.now())
                        self.render("200.html", entry=msg())
                    else:
                        self.rollback()
                        self.render("200.html", entry=msg(False, "接口调用失败"))
                else:
                    self.rollback()
                    self.render("200.html", entry=rs)
            except:
                    self.render("200.html", entry=msg(False, "调课失败"))
                    logger.info("Change time error msg{ %s }", traceback.format_exc())
                    self.rollback()
            finally:
                self.auto_commit()
        else:
            logger.info("Not Regular Request for change time")
            self.render("200.html", entry=msg(False,  "请求参数不对"))


@Route("/api/class/release", name="Release Timetable")
class APIClassReleaseHandle(BaseHandler):
    """
    撤销课表锁定-消息互通接口
    /api/class/release?claId=&uid
    """
    def post(self):
        cla_id, uid = get_param(self.request)
        if cla_id and uid:
            summary = uid + cla_id
            if not authorization(summary, self.request.headers):
                self.write(msg(False, "authorization failed"))
                return
            rows = self.db_model.models.mss.query_selected(uid=uid, cla_id=cla_id)
            if len(rows) == 1 and rows[0].deal == 'selected':
                r = self.db_model.models.mss.del_by_id(rows[0].id)
                r1 = self.db_model.models.mwr.free_lock(rows[0].workroom, "normal")
                if r and r1:
                    self.write(msg())
            else:
                self.write(msg(False, "没有任何更新,该课程已支付或者已释放"))
                logger.info("Repeat Regular Request for release")
        else:
            self.write(msg(False, "请求参数不对"))


@Route("/api/class/payed", name="Get payed notify")
class APIClassPayedHandle(BaseHandler):
    """
    学生支付课程-消息互通接口
    /api/class/payed?claId=&uid=
    """
    def post(self):
        data = ujson.loads(self.request.body)
        cla_id = data.get("claId", None)
        uid = data.get("uid", None)
        stu_name = data.get("stuName", u"杨华")
        #TODO build username
        if cla_id and uid:
            summary = uid + cla_id
            if not authorization(summary, self.request.headers):
                self.write(msg(False, "authorization failed"))
                return
            try:
                self.auto_commit(False)
                flag = self.db_model.pay(cla_id=cla_id, uid=uid, uname=stu_name)
                if flag.get("rlt"):
                    # single_login(uid, stu_name)
                    self.commit()
                else:
                    self.rollback()
                self.write(flag)
            except:
                logger.info(traceback.print_exc())
                self.rollback()
            finally:
                self.auto_commit()
        else:
            self.write(msg(False, "请求参数不对"))


@Route("/api/class/refund", name="Get refunded notify")
class APIClassRefundHandle(BaseHandler):
    """
     学生退费-消息互通接口
    /api/class/refund?claId=&uid=
    """
    def post(self):
        cla_id, uid = get_param(self.request)
        if cla_id and uid:
            summary = uid + cla_id
            if not authorization(summary, self.request.headers):
                self.write(msg(False, "authorization failed"))
                return
            try:
                self.auto_commit(False)
                rs = self.db_model.refund(cla_id=cla_id, uid=uid)

                if rs.rlt:
                    self.commit()
                    self.write(msg())
                else:
                    self.rollback()
                    self.write(rs)
            except:
                self.rollback()
                logger.info(traceback.format_exc())
                self.write(msg(False, "更新失败, 服务器端异常"))
            finally:
                self.auto_commit()
        else:
            self.write(msg(False, "请求参数不对"))


@Route("/timetable/notify", name="Kao Qing")
class NotifyHandle(BaseHandler):
    def get(self):
        try:
            cla_id = self.get_argument("cla_id")
            uid = self.get_argument("uid")
            time_id = self.get_argument("time_id")
            check_roll = self.get_argument("check_roll")
            rs = self.db_model.models.msc.update_check_roll(uid=uid, cla_id=cla_id, time_id=time_id, check_roll=check_roll)
            if rs:
                mg = attendances(uid, cla_id, time_id, check_roll)
                if mg.rlt:
                    self.commit()
                    self.render("200.html", entry=mg)
                else:
                    self.rollback()
                    self.render("200.html", entry=msg(False, "Invoke Interface Failed"))
            else:
                self.rollback()
                self.render("200.html", entry=msg(False, "data update failed"))
        except:
            self.rollback()
            logger.info(traceback.format_exc())
        finally:
            self.auto_commit()


# #TODO 登录，单点登录
# #TODO 两个表的Timeiid 要唯一
# #TODO xheader=true
# #TODO 跨站伪造请求的防范
# #TODO 404，500