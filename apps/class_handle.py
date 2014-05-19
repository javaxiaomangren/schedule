__author__ = 'windy'
#coding: utf-8

from base import *


#====================== Commons Methods ==========
def get_param(request):
    """获取参数"""
    data = ujson.loads(request.body)
    course_id = data.get("claId", None)
    student_id = data.get("uid", None)
    return course_id, student_id


def select_class(db, course_id, class_id, student_id, status_new, status_old):
    """
    选课操作：
    插入学生ID到数据库， 更新课程状态为1
    """
    return db.execute_rowcount("UPDATE timetable SET student_id=%s, class_status=%s "
                               "WHERE course_id=%s AND class_id=%s AND class_status=%s",
                               student_id, status_new, course_id, class_id, status_old)


format_date = lambda x, y: "%s %s" % (x, y)

insert_record = """INSERT INTO timetable_record
                (time_id,course_id,course_name,class_id,class_room,teacher_id,teacher_name,student_id,
                start_time,period,class_date,class_status,time_status,time_desc,check_roll,time_changed,
                class_changed) SELECT time_id,course_id,course_name,class_id,class_room,teacher_id,teacher_name,%s,
                start_time,period,class_date,class_status,time_status,time_desc,check_roll,time_changed,
                class_changed FROM timetable WHERE time_id=%s
              """
records_insert = """INSERT INTO records (src_id, tar_id, cla_id, course_id, uid, flag) VALUES(%s,%s,%s,%s,%s,%s)"""
insert_record_all = "insert into timetable_record select x.*, NOW() from timetable x %s"


def check_params(args, lens, keys):
    if len(args) > lens:
        return False
    for p in args.keys():
        if not p in keys:
            return False
    return True


def check_time(time_changed, time_status, class_date, start_time, for_change=None):
    """
    是否可以调课
    1. 调课3次后不能再调节
    2.等待上课的才可以调
    3.提前24小时调课
    """
    b1 = time_changed < 3
    # 转班只能转没有调过的
    if for_change:
        b2 = time_status == TimeStatus.PAYED
    else:
        b2 = time_status == TimeStatus.PAYED or time_status == TimeStatus.CHANGED
    now = datetime.now()
    times = str(start_time).split(":")
    old = datetime(class_date.year, class_date.month, class_date.day, int(times[0]), int(times[1]))
    s = old - now
    b3 = s.days > 1 or (s.days == 1 and s.seconds > 60)
    return b1 and b2 and b3


def check_class(value):
    """
    是否可以转班
    1.最多三次转班
    2.只能转24小时以后的课程
    3.调课后的不参与转班
    """
    return value.get("class_changed", 0) < 3


def set_response(dc, value):
    """
       设置聚合的课程返回信息给 speiyou.com
       当调用支付接口时， 返回给培优网的数据
    """
    old = dc.get(value.class_id)
    classes = OrderedDict()
    classes["timeId"] = value.time_id
    classes["teacherId"] = value.teacher_id
    classes["classDate"] = str(value.class_date)
    classes["startTime"] = str(value.start_time)
    classes["endTime"] = str(value.start_time + timedelta(minutes=value.period))
    classes["classroom"] = value.class_room
    classes["status"] = value.time_status

    if old:
        data_list = old.get("classes")
        data_list.append(classes)
        old["classes"] = data_list
    else:
        result = OrderedDict()
        result["claId"] = value.course_id
        result["uid"] = value.student_id
        result["classes"] = [classes]
        dc[value.class_id] = result


def set_for_my(dc, value):
    """
        设置聚合信息给课程管理
    """
    old = dc.get(value.student_id)
    clazz = Row()
    clazz["time_id"] = value.time_id
    clazz["date"] = str(value.class_date)
    clazz["time"] = str(value.start_time)
    clazz["period"] = value.period
    clazz["time_status"] = value.time_status
    clazz["teacher_id"] = value.teacher_id
    clazz["teacher_name"] = value.teacher_name
    clazz["can_time_change"] = check_time(value.time_changed, value.time_status, value.class_date, value.start_time)

    if old:
        classes = old.classes
        classes.append(clazz)
    else:
        new = Row()
        new["course_id"] = value.course_id
        # new["course_name"] = value.course_name
        new["class_id"] = value.class_id
        new["student_id"] = value.student_id
        new["class_status"] = value.class_status
        new["time_desc"] = value.time_desc
        # new["time_changed"] = value.time_changed
        # new["class_changed"] = value.class_changed
        new["can_change"] = check_class(value)
        new["classes"] = [clazz]
        dc[value.student_id] = new


def set_for_change(old, new, time_id=None):
    #如可time_id 为None表示调课，否则表示转班
    data = OrderedDict()
    data["sourceBeiliCucId"] = old.time_id
    data["sourceTeacherId"] = old.teacher_id
    data["sourceCourseDate"] = str(old.class_date)
    data["sourceStartTime"] = str(old.start_time)
    data["sourceEndTime"] = str(old.start_time + timedelta(minutes=old.period))
    data["sourceClassroom"] = old.class_room
    data["sourceStatus"] = old.time_status
    data["targetBeiliCucId"] = time_id or new.time_id
    data["targetTeacherId"] = new.teacher_id
    data["targetCourseDate"] = str(new.class_date)
    data["targetStartTime"] = str(new.start_time)
    data["targetEndTime"] = str(new.start_time + timedelta(minutes=new.period))
    data["targetClassroom"] = new.class_room
    data["targetStatus"] = TimeStatus.PAYED
    return data


def aggregate_by_date(rows):
    dic = {}
    for r in rows:
        dic[str(r.class_date)] = r
    return dic


def get_changes(old, new):
    """
        转班
    """
    datas = []
    ids = []
    if old and new:
        if old[0].class_changed < 3:
            # old_dic = aggregate_by_date(old)
            new_dic = aggregate_by_date(new)
            for row in old:
                ck = check_time(1, row.time_status, row.class_date, row.start_time, for_change=1)
                if ck:
                    new_row = new_dic.get(str(row.class_date), 0)
                    if new_row:
                        ids.append((row.time_id, new_row.time_id))
                        datas.append(set_for_change(row, new_row))
    return ids, datas


def update_class_status(db, course_id, class_id, student_id, old_status, new_status):
    return db.execute_rowcount("UPDATE timetable SET class_status=%s "
                               "WHERE course_id=%s AND class_id=%s AND student_id=%s AND class_status=%s",
                               new_status, course_id, class_id, student_id, old_status)


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
                    return self.write(message(False, "authorization error"))
            except AttributeError:
                self.write(message(False, "authorization error"))
        except:
            logger.info("/api/class/add, Error Msg {%s }" % traceback.format_exc())
            self.write(message(False, "请求参数异常"))
            return
        try:
            self.db.execute_rowcount("REPLACE INTO course(claId, class_name,class_count, every_hours,"
                                     "start_date, end_date, frequency, year, term_name,"
                                     " max_person, create_date, finished) "
                                     "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 0)",
                                     p.claId, p.claName, p.classCount, p.everyHours, p.startDate, p.endDate,
                                     p.frequency, p.year, p.termName, p.maxPersons)
            self.write(message())
        except AttributeError as ae:
            self.write(message(False, "%s 参数没有找到" % ae))
            logger.info(message(False, "%s 参数没有找到" % ae))
        except SyntaxError as it:
            self.write(message(False, "该课程已经存在 %s" % it))
            logger.info(message(False, "该课程已经存在 %s" % it))


@Route("/api/class/timetable/list", name="List TimeTables ")
class TimeTableListHandle(BaseHandler):
    """
     请求课表页面
    /api/class/timetable/list?claId=&uid=
    """
    def get(self):
        args = self.request.query_arguments
        checked = check_params(args, 5, ["claId", "uid", "teacherName", "timeInterval", "pageNo"])
        if not checked:
            self.write(message(False, "Bad Request"))
            logger.info("请求参数不对，非法请求")
            return

        course_id = self.get_argument("claId", None)
        student_id = self.get_argument("uid", None)
        teacher_name = self.get_argument("teacherName", None)
        time_interval = self.get_argument("timeInterval", None)
        page_no = int(self.get_argument("pageNo", 1))
        page_size = 10
        if course_id and student_id:
            where = get_query_where(course_id, teacher_name, time_interval)
            page_count = get_page_count(self.db, where, page_size)
            if page_no > page_count:
                page_no = page_count
            if page_no < 1:
                page_no = 1
            timetable = query_timetables(self.db, course_id, where, page_no, page_size)
            self.render("timetable_list.html", entries=timetable.values(),
                        args=args_value(args), page_count=page_count, page_no=page_no)
        else:
            self.write(message(False, "请求参数不对"))
            logger.info(message(False, "请求参数不对"))


@Route("/api/class/manage", name="Timetable Manage")
class MyClassHandler(BaseHandler):
    """
    学生课程管理页面
    /api/class/manage?uid=&claId=&planId=
    """
    def get(self):
        #TODO post, and check header
        checked = check_params(self.request.query_arguments, 2, ["uid", "claId"])
        if not checked:
            self.write(message(False, "Bad Request"))
            logger.info(message(False, "请求参数不对"))
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        if student_id and course_id:
            rows = self.db.query("SELECT * FROM timetable WHERE class_id > 0 AND student_id=%s AND course_id=%s "
                                 "ORDER BY class_date, start_time",
                                 student_id, course_id)
            class_time = aggregate_by_grade(rows, set_for_my)
            self.render("my_timetable.html", entries=class_time.values(), studentId=student_id)
        else:
            self.write(message(False, "请求参数不对"))


@Route("/timetable/select", name="select class Timetable")
class TimetableSelectHandle(BaseHandler):
    """
    学生选课
    /timetable/select?uid=&claId=&planId=&oldPlanId=
    如果oldPlanId 不为空表示转班
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 4, ["uid", "claId", "planId"])
        if not checked:
            self.write(message(False, "Bad Request"))
            logger.info(message(False, "请求参数不对"))
            return
        student_id = self.get_argument("uid", None)
        course_id = self.get_argument("claId", None)
        class_id = self.get_argument("planId", None)
        if student_id and course_id and class_id:
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
                                try:
                                    rs_data = reg_plan_status(student_id, course_id)
                                    if not rs_data.rlt:
                                        self.write(message(False, "Invoke interface reg_plan_status field"))
                                        return
                                except:
                                    logger.info(traceback)
                                    self.write(message(False, "Invoke interface reg_plan_status field"))
                                    return
                                data = {"rlt": True, "msg": "success",
                                        "data": {"claId": course_id, "uid": student_id, "planId": class_id}
                                        }
                                self.commit()
                                self.write(data)
                                return
                            else:
                                self.rollback()
                                self.write(message(False, "选课失败"))
                                return
                        self.auto_commit()
                    except:
                        self.rollback()
                        self.write(message(False, traceback.format_exc()))
                        logger.info(message(False, traceback.format_exc()))
                    finally:
                        self.auto_commit()

            else:
                try:
                    rs = select_class(self.db, course_id, class_id, student_id,
                                      TimeStatus.APPOINTED, TimeStatus.NORMAL)
                    if not rs:
                        self.write(message(False, "%s 课程不存在，或者已被选了" % class_id))
                        logger.info("%s 课程不存在，或者已被选了, 非法访问" % class_id)
                        return
                    try:
                        rs_data = reg_plan_status(student_id, course_id)
                        if not rs_data.rlt:
                            self.write(message(False, "Invoke interface reg_plan_status field"))
                            return
                    except:
                        logger.info(traceback)
                        self.write(message(False, "Invoke interface reg_plan_status field"))
                        return
                    data = {"rlt": True,
                            "msg": "success",
                            "data": {"claId": course_id,
                                     "uid": student_id,
                                     "planId": class_id
                                }
                            }
                    self.commit()
                    self.write(data)
                    return

                except:
                    self.write(message(False, "课程 %s 不存在，或者已被选了" % class_id))
                    logger.info("%s 课程不存在，或者已被选了, 非法访问" % class_id)
                    return

            self.write(message(False, "%s Can not select class again" % student_id))
        else:
            self.write(message(False, "请求参数不对"))
            logger.info("请求参数不对 student_id=%s, class_id=%s" % student_id, class_id)


@Route("/timetable/change/all/query", name="Change class List")
class ClassChangeQueryHandle(BaseHandler):
    """
    学生转班查询
    /timetable/change/all/query?planId=&uid=&claId=&newPlanId
    """
    def get(self):
        args = self.request.query_arguments
        checked = check_params(args, 6, ["uid", "claId", "planId", "teacherName", "timeInterval", "pageNo"])
        if not checked:
            self.write(message(False, "Bad Request Params"))
            return
        course_id = self.get_argument("claId", None)
        student_id = self.get_argument("uid", None)
        teacher_name = self.get_argument("teacherName", None)
        time_interval = self.get_argument("timeInterval", None)
        page_no = int(self.get_argument("pageNo", 1))
        page_size = 10
        if course_id and student_id:
            time_desc = self.db.query("SELECT time_desc FROM timetable "
                                      "WHERE course_id=%s AND student_id=%s limit 1", course_id, student_id)
            args["change"] = [1]
            args["url"] = ['/timetable/change/all/query']
            if time_desc:
                where = get_query_where(course_id, teacher_name, time_interval,
                                        time_desc=time_desc[0].time_desc)
                page_count = get_page_count(self.db, where, page_size)
                if page_no > page_count:
                    page_no = page_count
                if page_no < 1:
                    page_no = 1
                timetable = query_timetables(self.db, course_id, where, page_no, page_size)
                self.render("timetable_change_list.html", entries=timetable.values(),
                            args=args_value(args), page_count=page_count,
                            page_no=page_no)
            else:
                self.render("timetable_change_list.html", entries=[],
                            args=args_value(args), page_count=0, page_no=page_no)

        else:
            self.write(message(False, "请求参数不对"))


@Route("/timetable/change", name="")
class ClassChangeQueryHandle(BaseHandler):
    """
    转班

    """
    def get(self, *args, **kwargs):
         #TODO post ask
        course_id = self.get_argument("c", None)
        new_class_id = self.get_argument("np", None)
        student_id = self.get_argument("u")
        try:
            old_class = get_by_id(self.db, course_id=course_id, student_id=student_id)
            new_class = get_by_id(db=self.db, course_id=course_id, class_id=new_class_id)
            if old_class and new_class_id:
                ids, datas = get_changes(old_class, new_class)
                if ids and datas:
                    self.auto_commit(False)
                    #1.插入到新班级
                    #2.更新就的班级, 被调课的课程
                    #3.记录操作日志
                    params = []
                    records_params = []
                    class_changed = old_class[0].class_changed
                    time_changed = old_class[0].time_changed
                    old_class_id = old_class[0].class_id

                    for oid, nid in ids:
                        params.append((None, -1, 0, 0, 0, 0, course_id, oid))
                        params.append((student_id, old_class_id, TimeStatus.PAYED,
                                       TimeStatus.PAYED, class_changed + 1, time_changed, course_id, nid))
                        #src_id, tar_id, cla_id, course_id, uid, flag
                        records_params.append((oid, nid, new_class_id, course_id, student_id, -2))
                    ched = self.db.execute_rowcount("UPDATE timetable set class_status = %s "
                                                    "WHERE course_id=%s AND class_id=%s",
                                                    TimeStatus.CHANGED, course_id, new_class_id)
                    updates = self.db.executemany_rowcount("UPDATE timetable set student_id=%s, class_id=%s,"
                                                           "class_status=%s, time_status=%s, class_changed=%s,"
                                                           " time_changed=%s WHERE course_id=%s AND time_id=%s", params)
                    ch = self.db.execute_rowcount("UPDATE timetable set class_changed = class_changed + 1 "
                                                  "WHERE course_id=%s AND student_id=%s", course_id, student_id)
                    if ched and updates and ch:
                        self.db.executemany_rowcount(records_insert, records_params)

                        try:
                            rs_data = courses(student_id, course_id, datas)
                            if not rs_data.rlt:
                                self.write(message(False, "Invoke interface courses field"))
                                return
                        except:
                            logger.info(traceback)
                            self.rollback()
                            self.write(message(False, "Invoke interface courses field"))
                            return
                        # TODO return page 1
                        self.write(message())
                        self.commit()
                    else:
                        self.rollback()
                        raise tornado.web.HTTPError(404, log_message="No data will be update")
                else:
                    self.write(message(False, "不可以再转班了"))
        except:
            logger.info(traceback.format_exc())
            self.rollback()
            raise tornado.web.HTTPError(500, log_message="专版失败")
        finally:
            self.auto_commit()


@Route("/timetable/change/time/list", name="class time list")
class BakTimeListHandle(BaseHandler):
    """
    查询可调课列表
    /timetable/change/time/list?planId=&uid=&claId=
    """
    def get(self):
        checked = check_params(self.request.query_arguments, 7,
                               ["uid", "claId", "planId", "timeId", "teacherName", "timeInterval", "pageNo"])
        if not checked:
            self.write(message(False, "参数不对"))
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
                if not old_row:
                    raise tornado.web.HTTPError(403, log_message="Forbidden")
                teacher_name = self.get_argument("teacherName", None)
                time_interval = self.get_argument("timeInterval", None)
                page_no = int(self.get_argument("pageNo", 1))
                where = "WHERE flag=0 AND class_date > '%s' " % old_row.class_date
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
                rows = self.db.query("SELECT * FROM timetable_bak %s ORDER BY class_date, start_time %s" % (where, limit))
                self.render("bak_time.html", entries=rows, old_entry=old_row,
                            args=args_value(self.request.query_arguments), page_no=page_no,
                            page_count=page_count)
            else:
                self.write(message(False, "请求参数不对"))


@Route("/timetable/change/time", name="change class time")
class TimetableTimeChangeHandle(BaseHandler):
    """
    调课,1.更新要调的课，插入新的课，记录操作
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
                valid = check_time(old_row.time_changed, old_row.time_status, old_row.class_date, old_row.start_time)
                if not valid:
                    raise tornado.web.HTTPError(403, log_message="该课程不能调了")
                try:
                    self.auto_commit(False)
                    #进攻式SQL,如果更新成功，表明没有调过课程
                    rs = self.db.execute_rowcount("UPDATE timetable SET class_id=-1, class_status=0, time_status=0,"
                                                  " student_id=NULL, time_changed=0, class_changed=0"
                                                  " WHERE time_id=%s AND class_id=%s AND student_id=%s "
                                                  " AND time_changed < %s", time_id, class_id, student_id, 3)
                    #记录调课次数
                    rs1 = self.db.execute_rowcount("UPDATE timetable SET time_changed=time_changed + 1 "
                                                   "WHERE student_id=%s AND course_id=%s", student_id, course_id)
                    if rs and rs1:
                        #TODO 是否可以把这个放到 timetable表
                        last_time_id = \
                            self.db.execute_lastrowid("INSERT INTO timetable (course_id, course_name, class_id,"
                                                      "class_room, teacher_id, teacher_name, student_id, start_time,"
                                                      "period, class_date, class_status, time_status, time_desc, "
                                                      "check_roll, time_changed, class_changed) VALUES"
                                                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                                      course_id, old_row.course_name, class_id, row.class_room,
                                                      row.teacher_id, row.teacher_name, student_id, row.start_time,
                                                      row.period, row.class_date, old_row.class_status,
                                                      TimeStatus.CHANGED, old_row.time_desc, old_row.check_roll,
                                                      old_row.time_changed + 1, old_row.class_changed)

                        self.db.execute_rowcount("UPDATE timetable_bak SET flag=1 WHERE id=%s", time_id_new)
                        # TODO 记录对应关系，是否释放课程
                        # self.db.execute_rowcount(insert_record, student_id, time_id)
                        #flag -1表示调课的id
                        self.db.execute_rowcount(records_insert,
                                                 time_id, time_id_new, class_id, course_id, student_id, -1)

                        # result = OrderedDict()
                        data = OrderedDict()
                        # result["uid"] = student_id
                        # result["claId"] = course_id
                        #TODO extract a method
                        data["sourceBeiliCucId"] = time_id
                        data["sourceTeacherId"] = old_row.teacher_id
                        data["sourceCourseDate"] = str(old_row.class_date)
                        data["sourceStartTime"] = str(old_row.start_time)
                        data["sourceEndTime"] = str(old_row.start_time + timedelta(minutes=old_row.period))
                        data["sourceClassroom"] = old_row.class_room
                        data["sourceStatus"] = old_row.time_status
                        data["targetBeiliCucId"] = last_time_id
                        data["targetTeacherId"] = row.teacher_id
                        data["targetCourseDate"] = str(row.class_date)
                        data["targetStartTime"] = str(row.start_time)
                        data["targetEndTime"] = str(row.start_time + timedelta(minutes=row.period))
                        data["targetClassroom"] = row.class_room
                        data["targetStatus"] = TimeStatus.CHANGED
                        # result["data"] = data

                        try:
                            rs_data = courses(student_id, course_id, [data])
                            if not rs_data.rlt:
                                self.write(message(False, "Invoke interface courses field"))
                                return
                        except:
                            logger.info(traceback)
                            self.rollback()
                            self.write(message(False, "Invoke interface courses field"))
                            return
                        self.commit()
                        #TODO return page 2
                        self.write(message())
                    else:
                        self.write(message(False, "您已调课3次, 不能调课了"))
                        logger.info("Not Regular Request")
                    self.auto_commit()
                except:
                    logger.info("Change time error msg{ %s }", traceback.format_exc())
                    self.rollback()
                finally:
                    self.auto_commit()
            else:
                self.write(message(False,  "请求错误， 没有查询到调课信息"))
                logger.info("Not Regular Request for change class time ")
        else:
            self.write(message(False,  "请求参数不对"))
            logger.info("Not Regular Request for change time")


@Route("/api/class/release", name="Release Timetable")
class APIClassReleaseHandle(BaseHandler):
    """
    撤销课表锁定-消息互通接口
    /api/class/release?claId=&uid
    """
    def post(self):
        course_id, student_id = get_param(self.request)
        if course_id and student_id:
            summary = student_id + course_id
            if not authorization(summary, self.request.headers):
                self.write(message(False, "authorization failed"))
                return
            rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, student_id=Null "
                                          "WHERE course_id=%s AND student_id=%s"
                                          " AND class_status=%s", TimeStatus.NORMAL, course_id,
                                          student_id, TimeStatus.APPOINTED)
            if rs:
                self.write(message())
            else:
                self.write(message(False, "没有任何更新,该课程已支付或者已释放"))
                logger.info("Repeat Regular Request for release")
        else:
            self.write(message(False, "请求参数不对"))


@Route("/api/class/payed", name="Get payed notify")
class APIClassPayedHandle(BaseHandler):
    """
    学生支付课程-消息互通接口
    /api/class/payed?claId=&uid=
    """
    def post(self):
        data = ujson.loads(self.request.body)
        course_id = data.get("claId", None)
        student_id = data.get("uid", None)
        stuName = data.get("stuName", None)
        #TODO build username
        if course_id and student_id:
            summary = student_id + course_id
            if not authorization(summary, self.request.headers):
                self.write(message(False, "authorization failed"))
                return
            try:
                self.auto_commit(False)
                rs = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s "
                                              "WHERE course_id=%s AND student_id=%s "
                                              "AND class_status=%s", TimeStatus.PAYED, TimeStatus.PAYED,
                                              course_id, student_id, TimeStatus.APPOINTED)

                if rs:
                    rows = self.db.query("SELECT * FROM timetable "
                                         "WHERE course_id=%s AND student_id=%s "
                                         "ORDER BY class_date, start_time, time_id",
                                         course_id, student_id)
                    data = aggregate_by_grade(rows, set_response).values()[0]
                    self.write({"rlt": True, "msg": "Success", "data": data})
                    self.commit()
                else:
                    #todo remove query
                    rows = self.db.query("SELECT * FROM timetable "
                                         "WHERE course_id=%s AND student_id=%s "
                                         "ORDER BY class_date, start_time, time_id",
                                         course_id, student_id)
                    data = aggregate_by_grade(rows, set_response).values()[0]
                    self.write({"rlt": False, "msg": "更新失败", "data": data})
            except:
                self.rollback()
            finally:
                self.auto_commit()
        else:
            self.write(message(False, "请求参数不对"))


@Route("/api/class/refund", name="Get refunded notify")
class APIClassRefundHandle(BaseHandler):
    """
     学生退费-消息互通接口
    /api/class/refund?claId=&uid=
    """
    def post(self):
        course_id, student_id = get_param(self.request)
        if course_id and student_id:
            summary = student_id + course_id
            if not authorization(summary, self.request.headers):
                self.write(message(False, "authorization failed"))
                return
            where = " WHERE course_id=%s AND student_id=%s "
            rs1 = self.db.execute_rowcount("UPDATE timetable SET class_status=%s, time_status=%s "
                                           "WHERE course_id=%s AND student_id=%s "
                                           "AND class_status=%s", TimeStatus.REFUND, TimeStatus.REFUND,
                                           course_id, student_id, TimeStatus.PAYED)
            rs2 = self.db.execute_rowcount(insert_record_all % where, course_id, student_id)
            rs3 = self.db.execute_rowcount("UPDATE timetable SET class_status=0, time_status=0, "
                                           "student_id=null, class_changed=0, time_changed=0, check_roll=0"
                                           " WHERE course_id=%s AND student_id=%s "
                                           , course_id, student_id)

            if rs1 and rs2 and rs3:
                self.write(message())
            else:
                self.write(message(False, "更新失败:"))

        else:
            self.write(message(False, "请求参数不对"))


#TODO 查询被调课老师，查询被转班老师
#TODO 和网校底层数据库交互
#TODO 登录，单点登录
#TODO 两个表的Timeiid 要唯一
#TODO js close page
#TODO 学生和课程关系变化如何和网校互通接口
#TODO xheader=true
#TODO 跨站伪造请求的防范
# TODO 重排列班级
#TODO 404，500