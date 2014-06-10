# coding=utf-8
__author__ = 'windy'
import calendar
from tornado.web import gen_log
from torndb import Row
from collections import OrderedDict
from utils import CheckRoll
from utils import sendmail
from datetime import datetime
from datetime import timedelta
from http_msg import single_login

tb_prefix = "mid_"
tb = lambda x: tb_prefix + x
p_size = 15
class_period = 25
#与考勤时间
pre_check = 12
a_dates = ["2014-07-23", "2014-07-24", "2014-07-25", "2014-07-26",
           "2014-07-28", "2014-07-29", "2014-07-30", "2014-07-31",
           "2014-08-01", "2014-08-02", "2014-08-04"]

b_dates = ["2014-08-05", "2014-08-06", "2014-08-07", "2014-08-08",
           "2014-08-09", "2014-08-11", "2014-08-12", "2014-08-13",
           "2014-08-14", "2014-08-15", "2014-08-16"]

c_dates = ["2014-08-18", "2014-08-19", "2014-08-20", "2014-08-21",
           "2014-08-22", "2014-08-23", "2014-08-25", "2014-08-26",
           "2014-08-27", "2014-08-28", "2014-08-29"]


def msg(rlt=True, msg="Success"):
    return Row({"rlt": rlt, "msg": msg})


def split_sort(dates):
    pairs = map(lambda x: x.split("="),  dates.split(","))
    return sorted(pairs, key=lambda p: p[1])


class BaseDBModel(object):
    db = None

    def __init__(self, db):
        self.db = db

    @property
    def get(self):
        return self.db

    @staticmethod
    def get_and_where(*args, **kwargs):
        where = " WHERE 1=1 "
        param_list = []
        for k in kwargs:
            p = kwargs.get(k)
            if p:
                if isinstance(p, list):
                    ins = ",".join(["%s"] * len(p))
                    where += " AND " + k + " IN(" + ins + ")"
                    param_list = param_list + p
                else:
                    where += " AND " + k + "=%s "
                    param_list.append(kwargs.get(k))
        for v in args:
            where += " " + v
        gen_log.debug("where[%s], params[%s]", where, param_list)
        return where, param_list

    def get_one(self, table, where, param=list()):
        return self.db.get("select * from %s %s" % (table, where), *param)

    def get_all_simple(self, table):
        return self.db.query("select * from %s " % table)

    def query(self, table, select="*", where='', param=list()):
        """
        :rtype : list(Row())
        """
        return self.db.query("select %s from %s %s" % (select, table, where), *param)

    def count(self, table, where, params, field="*"):
        row = self.db.get("select count(%s) as count from %s %s " % (field, table, where), *params)
        if row:
            return row.count
        return 0

    def page_count(self, table, where, params=list()):
        cnt = self.count(table, where, params)
        return (cnt + p_size - 1) / p_size

    def insert(self, table, keys=list(), param=list(tuple())):
        if keys:
            fd = ",".join(keys)
            vs = ",".join(["%s"] * len(keys))
            sql = "insert into %s(%s) values(%s) " % (table, fd, vs)
            gen_log.debug("sql[%s], values[%s]", sql, param)
            return self.db.executemany_rowcount(sql, param)

    def update(self, table, keys=list(), values=list(), where='', param=list()):
        if keys:
            sets = ",".join(map(lambda k: k + "=%s", keys))
            return self.db.execute_rowcount("update %s set %s %s" % (table, sets, where), *tuple(values + param))
        return -1

    def update_simple(self, table, fields=list(), values=list(), **kwargs):
        where, params = self.get_and_where(**kwargs)
        return self.update(table, fields, values, where, param=params)

    def delete(self, table, where, params=list()):
        return self.db.execute_rowcount("delete from %s %s" % (table, where), *params)

    @staticmethod
    def check_time(class_date, start_time, check=pre_check):
        """判断是否即将上课"""
        times = str(start_time).split(":")
        now = datetime.now()
        old = datetime(class_date.year, class_date.month, class_date.day, int(times[0]), int(times[1]))
        o_t = calendar.timegm(old.utctimetuple())
        n_t = calendar.timegm(now.utctimetuple())
        dlt = o_t - n_t
        if dlt > 60 * 60 * pre_check:
            return True
        return False

    @staticmethod
    def get_valid_date(check=pre_check):
        now = datetime.now()
        valid = now + timedelta(hours=check)
        s_v = str(valid)
        dt, time = s_v.split(" ")
        return dt, time.split(".")[0]
    @staticmethod
    def check_locked(row):
        """
        检查有没有预考勤
        """
        for r in row:
            #有预考勤
            if r.check_roll == CheckRoll.LOCKED:
                gen_log.info("[%s][%s] was locked", r.class_date, r.time_id)
                return True, "[%s] will start after [%s] our" % (r.class_date, pre_check)
            #未考勤的课程是否即将开始
            if r.check_roll == CheckRoll.NORMAL or r.check_roll == CheckRoll.TRAIL:
                if not BaseDBModel.check_time(r.class_date, r.start_time):
                    gen_log.info("[%s] will start after [%s] our" % (r.class_date, pre_check))
                    return True, "[%s] will start after [%s] our" % (r.class_date, pre_check)

        return False, "None"

    @staticmethod
    def get_change_relation(src, target, select_id):
        """
        获取需要转班的信息，
        1.预考勤不能转班
        2.试听课成记录在考勤
        3.上过的课，跳过的课不做转班
        """
        dlt = []
        ist = []
        ist_records = []
        datas = []
        by_date = dict([(str(t.class_date), t) for t in target])

        for r in src:
            # if r.class_type == CheckRoll.TRAIL or r.check_roll == CheckRoll.NORMAL:
            if r.check_roll == CheckRoll.NORMAL or r.check_roll == CheckRoll.TRAIL:
                right_time = BaseDBModel.check_time(r.class_date, r.start_time)
                if right_time:
                    dlt.append(r.time_id)
                    after = by_date.get(str(r.class_date))
                    ist.append((r.uid, r.cla_id, after.time_id, after.workroom, after.teacher, after.class_date, CheckRoll.NORMAL))
                    ist_records.append((select_id, r.workroom, after.workroom, r.time_id, after.time_id, r.class_date, after.class_date))
                    datas.append(BaseDBModel.set_change_class(r, after))
        return dlt, ist, ist_records, datas

    @staticmethod
    def set_response(rows=list(), cla_id='', uid=''):
        """
           设置聚合的课程返回信息给 speiyou.com
           当调用支付接口时， 返回给培优网的数据
        """
        result = OrderedDict()
        classes = []
        result["claId"] = cla_id
        result["uid"] = uid

        for row in rows:
            c = OrderedDict()
            c["timeId"] = row.time_id
            c["teacherId"] = row.teacher
            c["teacherName"] = row.fullname
            c["classDate"] = str(row.class_date)
            c["startTime"] = str(row.start_time)
            c["endTime"] = str(row.start_time + timedelta(minutes=class_period))
            c["classroom"] = row.workroom
            c["status"] = row.class_type
            classes.append(c)

        result["classes"] = classes
        return result

    @staticmethod
    def set_change_date(src, target):
        data = OrderedDict()
        data["sourceBeiliCucId"] = src.time_id
        data["sourceTeacherId"] = src.teacher
        # data["sourceTeacherName"] = src.fullname
        data["sourceCourseDate"] = str(src.class_date)
        data["sourceStartTime"] = str(src.start_time)
        data["sourceEndTime"] = str(src.start_time + timedelta(minutes=class_period))
        data["sourceClassroom"] = src.workroom
        data["sourceStatus"] = src.class_type
        data["targetBeiliCucId"] = target.time_id
        data["targetTeacherId"] = target.teacher
        # data["targetTeacherName"] = target.fullname
        data["targetCourseDate"] = str(target.class_date)
        data["targetStartTime"] = str(target.start_time)
        data["targetEndTime"] = str(target.start_time + timedelta(minutes=class_period))
        data["targetClassroom"] = target.id
        data["targetStatus"] = target.class_type
        return data

    @staticmethod
    def set_change_class(old, new):
        data = OrderedDict()
        data["sourceBeiliCucId"] = old.time_id
        data["sourceTeacherId"] = old.teacher
        # data["sourceTeacherName"] = old.fullname
        data["sourceCourseDate"] = str(old.class_date)
        data["sourceStartTime"] = str(old.start_time)
        data["sourceEndTime"] = str(old.start_time + timedelta(minutes=class_period))
        data["sourceClassroom"] = old.workroom
        data["sourceStatus"] = old.class_type
        data["targetBeiliCucId"] = new.time_id
        data["targetTeacherId"] = new.teacher
        # data["targetTeacherName"] = new.fullname
        data["targetCourseDate"] = str(new.class_date)
        data["targetStartTime"] = str(new.start_time)
        data["targetEndTime"] = str(new.start_time + timedelta(minutes=class_period))
        data["targetClassroom"] = new.workroom
        data["targetStatus"] = new.class_type
        return data


class LogicModel(BaseDBModel):
    models = None

    def initial(self, **kwargs):
        self.models = Row(kwargs)

    def count_classes(self, cla_id, teacher='', t_interval='', p_no=1, size=p_size, wr_status="normal"):
        count_sql = """
            select count(*) as count
                from mid_course_workroom cwr
                join mid_workroom wr on cwr.workroom=wr.id
                join mid_teacher t on t.id=wr.teacher
        """
        where = " where cwr.cla_id=%s and wr.status=%s "
        params = [cla_id, wr_status]
        if teacher:
            where += " and (t.fullname=%s or t.shortname=%s) "
            params.append(teacher)
            params.append(teacher)
        if t_interval and t_interval != u'0':
            t1, t2 = t_interval.split('-')
            where += " and wr.start_time between %s and %s "
            params.append(t1)
            params.append(t2)
        gen_log.debug("count sql[%s], param[%s]", count_sql + where, params)
        counts = self.db.get(count_sql + where, *params)
        if counts:
            return (counts.count + size - 1) / size
        return 0

    def list_class(self, cla_id, teacher='', t_interval='', p_no=1, size=p_size, wr_status="normal"):
        """
            分页查询课表
        """
        q_sql = """
            select cwr.workroom, cwr.cla_id, wr.id, wr.start_time, wr.description,
                   t.id as teacher, t.fullname, t.shortname,
                   group_concat(wrd.time_id, '=',wrd.class_date,"=", wrd.class_type) as id_dates
                from mid_course_workroom cwr
                join mid_workroom wr on cwr.workroom=wr.id
                join mid_teacher t on t.id=wr.teacher
                join mid_workroom_dates wrd on wr.id= wrd.workroom
        """

        group = " group by wrd.workroom order by wr.start_time"
        limit = ""
        where = " where cwr.cla_id=%s and wr.status=%s "
        params = [cla_id, wr_status]
        if teacher:
            where += " and (t.fullname=%s or t.shortname=%s) "
            params.append(teacher)
            params.append(teacher)
        if t_interval and t_interval != u'0':
            t1, t2 = t_interval.split('-')
            where += " and wr.start_time between %s and %s "
            params.append(t1)
            params.append(t2)
        if size > 0:
            limit = " limit %s, %s " % ((p_no - 1) * size, size)

        results = self.db.query(q_sql + where + group + limit, *params)
        for r in results:
            r["id_dates"] = split_sort(r.id_dates)

        gen_log.debug("query sql[%s], param[%s]", q_sql + where, params)
        return results

    def select_class(self, uid='', cla_id='', workroom=''):
        """
            选课
            1.check if selected
            2.update workroom flag as used
        """
        flag, dt = self.models.mss.check_select(uid, cla_id)
        if flag:
            #判断workroom是否可选
            if self.models.mwr.used_exists(workroom):
                gen_log.info("select a used workroom [%s]", workroom)
                return msg(False, "Class is used By others")
            # Reselect
            if dt:
                if workroom == dt.workroom:
                    return msg()
                rs = self.models.mss.update_by(_id=dt.id, cla_id=cla_id, uid=uid,
                                               fields=["workroom"], values=[workroom])
                rs1 = self.models.mwr.free_lock(dt.workroom, "normal")
                rs2 = self.models.mwr.free_lock(workroom, "used")
                if rs and rs1 and rs2:
                    gen_log.info("Reselect class uid[%s], OldWR[%s], NewWR[%s], Success",
                                 uid, dt.workroom, workroom)
                    return msg()
                else:
                    return msg(False, "Failed on Reselect class")
            # Select Class
            else:
                rs = self.models.mss.add([(uid, "", cla_id, workroom, "selected", "N", 1)])
                rs2 = self.models.mwr.free_lock(workroom, "used")
                if rs and rs2:
                    return msg()
                else:
                    message = "Failed on select class"
                    if rs or rs2:
                        if rs:
                            message = "Failed on select class, Failed to lock workroom[%s]" % workroom
                        else:
                            message = "Failed on select class, Failed to insert to select table"
                    gen_log.info(message)
                    return msg(False, message)

        else:
            gen_log.info(msg(False, "Have Classes already"))
            return msg(False, "Have Classes already")

    def pay(self, cla_id='', uid='', uname='NotSupply'):
        """
            支付课程
            1. insert into student_classes
            2. update student_class_select deal as payed
            3. return class data
        """
        flag, selected = self.models.mss.get_selected_for_pay(uid, cla_id)
        dt, valid_time = BaseDBModel.get_valid_date()
        if flag:
            if selected:
                rows = self.models.mwrd.get_valid_dates(selected.workroom, status="used",
                                                        date_now=dt)
                p = []
                for r in rows:
                    if BaseDBModel.check_time(r.class_date, r.start_time):
                        if r.class_type == CheckRoll.TRAIL:
                            p.append((uid, cla_id, r.time_id, r.workroom, r.teacher, r.class_date, CheckRoll.TRAIL))
                        else:
                            p.append((uid, cla_id, r.time_id, r.workroom, r.teacher, r.class_date, CheckRoll.NORMAL))
                rs = self.models.msc.add(p)
                rs1 = self.models.mss.update_by(_id=selected.id, uid=uid, cla_id=cla_id,
                                                fields=["uname", "deal"], values=[uname, "payed"])
                if rs and rs1:
                    sso = single_login(uid, uname)
                    email = "Student From LJL id=%s, name=%s\n" \
                            "Payed for:%s \n" \
                            "Class Table Link: http://yueke.speiyou.com/timetable/list/moodle?uid=%s&claId=%s\n" \
                            "SSO URL: %s" \
                            % (uid, uname, rows[0].workroom, uid, cla_id, sso)
                    sendmail(msg=email, subject="%s Student Pay For Class" % datetime.now())
                    return {"rlt": True, "msg": "Success", "data": self.set_response(rows, cla_id, uid)}
                else:
                    return {"rlt": False, "msg": "Failed", "data": "支付失败"}
            else:
                return {"rlt": False, "msg": "Success", "data": "没有选课"}
        else:
            #重复调用
            rows = self.models.mwrd.get_by_workroom(selected.workroom)
            return {"rlt": False, "msg": "Fiald", "data": self.set_response(rows, cla_id, uid)}

    def refund(self,  cla_id='', uid=''):
        """
        更新 workroom, 补课表， student_*表
        """
        def get_tip(message):
            gen_log.info("Refund Failed When %s ,uid[%s], cla_id[%s]", message, uid, cla_id)
            return msg(False, "Refund Failed When %s ,uid[%s], cla_id[%s]" % (message, uid, cla_id))

        #插入记录
        rs = self.models.msr.add([(uid, cla_id)])
        if not rs:
            return get_tip("insert records")
        #释放当前关联的workroom
        row = self.models.mss.get_current_select(cla_id=cla_id, uid=uid)
        if row:
            _rs = self.update_simple(MidWorkRoom.TABLE, ["status"], ["normal"], id=row.workroom)
            if not _rs:
                return get_tip("Release used workroom[]" % row.workroom)
            rr = self.models.msdc.get_by_selected_id(select_id=row.id)
            if rr:
                for row in rr:
                    self.models.mwrs.update_simple(
                        MidWorkRoomSingle.TABLE, ["status"], ["normal"], id=row.target_workroom)

        else:
            return get_tip("Get current used workroom")
        #更新选课表
        rs0 = self.models.mss.update_by(cla_id=cla_id, uid=uid,
                                        fields=["uid", "deal"],
                                        values=[uid + "refund", "refund"])
        if not rs0:
            return get_tip("update select_classes")
        #更新课表
        rs1 = self.update_simple(MidStudentClasses.TABLE, ["uid"], [uid + "_refund"], uid=uid, cla_id=cla_id)
        if not rs1:
            return get_tip("update student_classes")

        return msg()

    def change_class(self, cla_id='', uid='', target_wr='', manager=False):
        """
        转班：
        1.判断可否转（客服可以随时来转班）
        2.查询现在所属班级
        3.查询新班级
           3.1查询调课记录（check_roll=7）
        4.设置专版对应关系
        5.更新student_class表
        6.插入专版记录
        7.插入新选班级到student_select
        8.锁定新课
        9.释放愿课
        """
        can_change = True
        selected_row = None
         # 如果不是客服，检查是否可以转班
        if not manager:
            flag, selected_row = self.models.mss.check_will_change(cla_id=cla_id, uid=uid)
            if not flag:
                can_change = False
        if can_change:
            if self.models.mwr.used_exists(target_wr):
                gen_log.info("select a used workroom [%s]", target_wr)
                return msg(False, "Class is used by others or not exists")
            #查询原班数据,新班数据
            src_data = self.models.msc.full_query(uid=uid, cla_id=cla_id)
            target_data = self.models.mwrd.get_by_workroom(target_wr, status='normal')
            if not src_data:
                gen_log.info("Get class_table failed,cla_id[%s], uid=[%s]", cla_id, uid)
                return msg(False, "Get class_table failed,cla_id[%s], uid=[%s]" % (cla_id, uid))
            #检查是否有预考勤的课程, 或者12小时内有上课
            locked, message = self.check_locked(src_data)
            if locked:
                gen_log.info("Can change classes check ,uid[%s], cla_id[%s], message[%s]", uid, cla_id, message)
                return msg(False, "Can change classes check message[%s]" % message)
            if not target_data:
                gen_log.info("Get new WorkRoom failed,cla_id[%s], uid=[%s], workroom[%s]",
                             cla_id, uid, target_wr)
                return msg(False, "Get new WorkRoom failed,cla_id[%s], uid=[%s], workroom[%s]" % (cla_id, uid, target_wr))
            #寻找对应关系
            dlt, ist, ist_records, datas = self.get_change_relation(src_data, target_data, selected_row.id)
            if dlt and ist and ist_records:
                #删除原来课表
                _rs0 = self.models.msc.del_many(time_ids=dlt, cla_id=cla_id, uid=uid)
                if not _rs0:
                    gen_log.info("Change classes failed when delete old datas. "
                                 "uid=[%s],cla_id[%s], times[%s]", uid, cla_id, dlt)
                    return msg(False, "Change Classes Failed")
                #插入新课表
                _rs1 = self.models.msc.add(ist)
                if not _rs1:
                    gen_log.info("Change classes failed when insert new datas. "
                                 "uid=[%s],cla_id[%s]", uid, cla_id)
                    return msg(False, "Change Classes Failed")
                #记录调课内容
                _rs2 = self.models.mscc.add(ist_records)
                if not _rs2:
                    gen_log.info("Change classes failed when insert records datas. "
                                 "selected_id=[%s]", selected_row.id)
                    return msg(False, "Change Classes Failed")
                #释放原来的课程
                _rs3 = self.models.mwr.free_lock(selected_row.workroom, "normal")
                if not _rs3:
                    gen_log.info("Change classes failed when relase old workroom. "
                                 "workroom=[%s]", selected_row.workroom)
                    return msg(False, "Change Classes Failed")
                #锁定新课程
                _rs4 = self.models.mwr.free_lock(target_wr, "used")
                if not _rs4:
                    gen_log.info("Change classes failed when lock new workroom. "
                                 "workroom=[%s]", target_wr)
                    return msg(False, "Change Classes Failed")
                _rs5 = self.models.mss.add([(uid, selected_row.uname, cla_id, target_wr,
                                             "payed", "N", selected_row.version + 1)])
                _rs51 = self.models.mss.update_by(_id=selected_row.id, cla_id=cla_id, uid=uid,
                                                  fields=["deal"], values=["changed"])
                if not _rs5 or not _rs51:
                    gen_log.info("Change classes failed when update select records. "
                                 "select_id=[%s]", selected_row.id)
                    return msg(False, "Change Classes Failed")
                return Row({"rlt": True, "msg": datas})

            else:
                gen_log.info("uid=[%s],cla_id[%s] No classes can be change.", uid, cla_id)
                return msg(False, "No classes can be change.")
        else:
            gen_log.info("uid=[%s],cla_id[%s] Can not change workroom Again.", uid, cla_id)
            return msg(False, "Can not change workroom Again.")

    def change_date(self, cla_id='', uid='',
                    src_time_id=0, target_time_id=0, manager=False):
        """
        1.判断是否可以调课
        2.查询新旧课程
        3.插入到调课记录表
        4.更新原课状态(check_roll=Changed)
        5.更新新课状态(status=used)
        """
        can_change = True
        # 如果不是客服，检查是否已经调过课了
        if not manager:
            rows = self.models.msdc.check_has_changed(cla_id=cla_id, uid=uid)
            if rows:
                can_change = False

        #可以调课
        if can_change:
            #查询调课需要的信息MidStudentClasses
            src_data = self.models.msc.query_one(time_id=src_time_id, cla_id=cla_id, uid=uid)
            current_selected = self.models.mss.get_current_select(cla_id=cla_id, uid=uid, workroom=src_data.workroom)
            target_data = self.models.mwrs.get_by_time_id(time_id=target_time_id)
            if src_data and target_data and current_selected:
                if self.models.mwrs.used_exists(target_data.id):
                    gen_log.info("select a used workroom [%s]", target_data.id)
                    return msg(False, "Class is used By others")
                if src_data.class_type == CheckRoll.TRAIL:
                    gen_log.info("Trail Class Can not change [%s]", target_data.id)
                    return msg(False, "Trail Class Can not change")

                #删除旧课表
                rs = self.models.msc.del_one(time_id=src_data.time_id, cla_id=cla_id, uid=uid)
                if not rs:
                    gen_log.info("Failed to delete old class:uid=[%s], cla_id=[%s], time_id=[%s]",
                                 uid, cla_id, src_data.time_id)
                    return msg(False, "Failed on delete data")
                #插入新课表
                # ["uid", "cla_id", "time_id", "workroom", "teacher", "class_date", "check_roll"]
                rs1 = self.models.msc.add([(uid, cla_id, target_data.time_id, target_data.id,
                                            target_data.teacher, target_data.class_date, CheckRoll.CHANGE)])
                if not rs1:
                    gen_log.info("Failed to Insert to student_classes:uid=[%s], cla_id=[%s], time_id=[%s]"
                                 ", new_time_id[%s], new_workroom[%s]",
                                 uid, cla_id, src_data.time_id, target_data.time_id, target_data.id)
                    return msg(False, "Failed on insert data to student_classes")

                # 插入调课记录
                  # ["select_id", "uid", "cla_id", "src_workroom", "target_workroom",
                  # "src_date", "target_date", "src_time_id", "target_time_id",
                  # "handle", "operate_by"]
                operate_by = "student"
                if manager:
                    operate_by = "manager"
                rs2 = self.models.msdc.add([(current_selected.id, uid, cla_id, src_data.workroom,
                                            target_data.id, src_data.class_date, target_data.class_date,
                                            src_data.time_id, target_data.time_id, "N", operate_by)])
                if not rs2:
                    gen_log.info("Failed to Insert to student_date_changed:uid=[%s], cla_id=[%s], time_id=[%s]"
                                 ", new_time_id[%s], new_workroom[%s], old_time_id[%s], old_workroom[%s]",
                                 uid, cla_id, src_data.time_id, target_data.time_id, target_data.id, src_data.time_id,
                                 src_data.workroom)
                    return msg(False, "Failed on insert data to student_date_changed")
                #更新被调课的状态为used
                rs3 = self.models.mwrs.free_lock(target_data.id, "used")
                if not rs3:
                    gen_log.info("Failed to Lock workroom_single:uid=[%s], cla_id=[%s], new_workroom[%s]",
                                 uid, cla_id, target_data.id)
                    return msg(False, "Failed to Lock workroom workroom_single")
                #返回更改数据对应关系
                rep = self.set_change_date(src_data, target_data)
                email = "Student %s\n" \
                        "src workroom: %s, date:%s time:%s\n" \
                        "target workroom: %s, date:%s time:%s\n"\
                        % (uid, src_data.workroom, src_data.class_date, src_data.start_time,
                           target_data.id, target_data.class_date, target_data.start_time)
                return Row({"rlt": True, "msg": rep, "email": unicode(email)})
            else:
                gen_log.info("Query Change Date Failed src_data, target_data, current_selected")
                gen_log.debug(src_data)
                gen_log.debug(target_data)
                gen_log.debug(current_selected)
                return msg(False, "No Class Can be Changed")
        else:
            gen_log.info("uid=[%s], Can not change class Again.", uid)
            return msg(False, "Can not change class Again.")

    def get_changed_history(self, uid='', cla_id='', deal="changed"):
        sql = "select scc.*, ss.uid, ss.cla_id, ss.uname from mid_student_class_changed scc " \
              "join  mid_student_selected ss on scc.select_id=ss.id" \
              " where ss.uid=%s and  ss.cla_id=%s and ss.deal=%s"

        return self.db.query(sql, uid, cla_id, deal)


class MidCourse(BaseDBModel):
    TABLE = tb("course")

    @property
    def get(self):
        return self.TABLE

    def get_by_id(self, _id):
        return self.get_one(self.TABLE, *BaseDBModel.get_and_where(claId=_id))

    def get_courses(self):
        return self.get_all_simple(self.TABLE)

    def add_course(self):
        pass


class MidCourseWorkRoom(BaseDBModel):
    TABLE = tb("course_workroom")
    fields = ["cla_id", "workroom"]

    @property
    def get(self):
        return self.TABLE

    def get_course_wr(self):
        pass

    def add_by(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def add(self, cla_id, term):
        workrooms = MidWorkRoom(self.db).get_id_by_term(term)
        p = map(lambda r: (cla_id, r.id), workrooms)
        if p:
            return self.insert(self.TABLE, self.fields, p)


class MidWorkRoom(BaseDBModel):
    TABLE = tb("workroom")
    fields = ["id", "term", "teacher", "start_time", "virtual_student", "status", "description"]
    sql = "select mw.*, t.fullname, t.shortname " \
          "from mid_workroom mw " \
          "join mid_teacher t on mw.teacher=t.id where mw.id=%s"

    @property
    def get(self):
        return self.TABLE

    @staticmethod
    def resolve_workroom(workroom):
        term, tm, tid = workroom.split("-")
        return [term, tm[0:2] + ":" + tm[2:], tid]

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def get_id_by_term(self, term):
        where, params = BaseDBModel.get_and_where(term=term)
        return self.query(self.TABLE, select="id", where=where, param=params)

    def free_lock(self, workroom, status):
        return self.update(self.TABLE, ["status"], [status], where=" where id=%s", param=[workroom])

    def get_by_id(self, _id):
        return self.get_one(self.TABLE, where=" where id=%s", param=[_id])

    def get_full_by_id(self, _id):
        return self.db.get(self.sql, _id)

    def used_exists(self, _id):
        r = self.get_by_id(_id)
        if r:
            return r.status == "used"
        return True

    def list_all(self):
        return self.get_all_simple(self.TABLE)


class MidWorkRoomSingle(BaseDBModel):
    TABLE = tb("workroom_single")
    fields = ["id", "cla_id", "time_id", "term", "teacher", "class_date", "start_time",
              "class_type", "virtual_student", "status", "description"]

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def get_id_by_term(self, term):
        where, params = BaseDBModel.get_and_where(term=term)
        return self.query(self.TABLE, select="id", where=where, param=params)

    def free_lock(self, workroom, status):
        return self.update(self.TABLE, ["status"], [status], where=" where id=%s", param=[workroom])

    def get_by_time_id(self, time_id=0):
        return self.get_one(self.TABLE, where=" where time_id=%s ", param=[time_id])

    def get_by_id(self, _id):
        return self.get_one(self.TABLE, where=" where id=%s", param=[_id])

    def used_exists(self, _id):
        r = self.get_by_id(_id)
        if r:
            return r.status == "used"
        return True

    def query_all(self, p_no, size, **kwargs):
        where, params = self.get_and_where(**kwargs)
        count = self.page_count(self.TABLE, where, params=params)
        where2, params2 = self.get_and_where(" limit %s, %s" % ((p_no - 1) * size, size), **kwargs)
        return count, self.query(self.TABLE, where=where2, param=params2)


class MidWorkRoomDates(BaseDBModel):
    TABLE = tb("workroom_dates")
    fields = ["workroom", "class_date", "class_type"]
    sql = "select w.virtual_student, w.start_time, w.description, " \
          "w.teacher, t.fullname, t.shortname, t.fullname, wd.* from mid_workroom w " \
          "join mid_teacher t on t.id=w.teacher "\
          "join mid_workroom_dates wd " \
          "on w.id=wd.workroom " \


    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def get_by_workroom(self, workroom, status=''):
        where = "where w.id=%s order by wd.class_date"
        if status:
            where = "where w.id=%s and status=%s order by wd.class_date"
            return self.db.query(self.sql + where, workroom, status)
        return self.db.query(self.sql + where, workroom)

    def get_valid_dates(self, workroom, status='', date_now=datetime.now(), time_now="00:00:00"):
        where = "where w.id=%s order by wd.class_date"
        if status:
            where = "where w.id=%s and w.status=%s and  wd.class_date >= %s order by wd.class_date"
            print self.sql + where % (workroom, status, date_now)
            return self.db.query(self.sql + where, workroom, status, date_now)
        return self.db.query(self.sql + where, workroom)

    def get_by_time_id(self, time_id=0):
        where = "where wd.time_id=%s order by wd.class_date"
        return self.db.get(self.sql + where, time_id)


class MidStudentSelected(BaseDBModel):
    TABLE = tb("student_selected")
    fields = ["uid", "uname", "cla_id", "workroom", "deal", "handle", "version"]

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def check_select(self, uid, cla_id):
        """判断是否已经选课,并且没有支付"""
        where, params = self.get_and_where(uid=uid, cla_id=cla_id)
        rows = self.query(self.TABLE, where=where, param=params)
        if rows:
            if len(rows) == 1:
                if rows[0].deal == "selected" and rows[0].version == 1:
                    return True, rows[0]
            return False, rows
        else:
            return True, None

    def check_will_change(self, uid='', cla_id=''):
        """
            查询将要转班的选课， 并且转班次数小于3次
        """
        rows = self.query_selected(uid=uid, cla_id=cla_id, deal="payed")
        if rows and len(rows) == 1:
            row = rows[0]
            if row.version > 3:
                return False, row
            else:
                return True, row
        else:
            return False, None

    def query_selected(self, uid='', cla_id='', uname='', deal='', workroom=''):
        where, params = self.get_and_where(uid=uid, cla_id=cla_id,
                                           uname=uname, deal=deal, workroom=workroom)
        return self.query(self.TABLE, where=where, param=params)

    def update_by(self, _id='', cla_id='', uid='', fields=list(), values=list()):
        """更新某些字段，如uname, deal, handle, version"""
        where, params = self.get_and_where(id=_id, cla_id=cla_id, uid=uid)
        return self.update(self.TABLE, fields, values, where, param=params)

    def get_current_select(self, cla_id='', uid='', workroom=''):
        where, param = self.get_and_where(cla_id=cla_id, uid=uid, workroom=workroom, deal="payed")
        return self.get_one(self.TABLE, where, param)

    def get_selected_for_pay(self, uid, cla_id):
        """查询的班级选择， 如果没有查询支付的班级"""
        where, param = self.get_and_where(uid=uid, cla_id=cla_id)
        rows = self.query(self.TABLE, where=where, param=param)
        if rows:
            if len(rows) == 1:
                row = rows[0]
                if row.deal == "selected":
                    return True, row
                else:
                    return False, row
            else:
                return False, None

        else:
            return False, None

    def del_by_id(self, select_id):
        return self.db.execute_rowcount("delete from mid_student_selected where id=%s", select_id)

    def list_selected(self, p_no=0, size=p_size, deal="payed"):
        """分页查询"""
        # if kwargs:
        #     where, param = self.get_and_where((" limit "), **kwargs)
        sql = "select ss.*, t.id as teacher, t.shortname, t.fullname," \
              " mc.class_name, wr.description, wr.virtual_student " \
              "from mid_student_selected ss " \
              "join mid_workroom wr on wr.id=ss.workroom " \
              "join mid_course mc on ss.cla_id=mc.claId " \
              "join mid_teacher t on t.id=wr.teacher"

        # counts = self.db.get(sql % "count(*) as count")
        #TODO, 完善分页，条件等查询
        return self.db.query(sql + " where ss.deal='selected' or ss.deal=%s", deal)


class MidStudentClasses(BaseDBModel):
    TABLE = tb("student_classes")
    fields = ["uid", "cla_id", "time_id", "workroom", "teacher", "class_date", "check_roll"]
    sql = "select sc.*, wd.class_type, wr.start_time, wr.teacher, t.shortname, t.fullname from mid_student_classes sc " \
          "join mid_workroom_dates wd on sc.time_id=wd.time_id " \
          "join mid_workroom wr on wr.id= sc.workroom " \
          "join mid_teacher t on t.id=wr.teacher "

    sql2 = "select sc.*, ws.start_time, ws.class_type, ws.teacher, t.shortname, t.fullname " \
           "from mid_student_classes sc " \
           "join mid_workroom_single ws on sc.time_id=ws.time_id " \
           "join mid_teacher t on t.id=ws.teacher"

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def del_one(self, time_id=0, uid='', cla_id=''):
        where, params = self.get_and_where(time_id=time_id, uid=uid, cla_id=cla_id)
        return self.delete(self.TABLE, where, params)

    def del_many(self, time_ids=list(), uid='', cla_id=''):
        where, params = self.get_and_where(time_id=time_ids, uid=uid, cla_id=cla_id)
        return self.delete(self.TABLE, where, params=params)

    def update_by(self, fields=list(), values=list(), **kwargs):
        """更新某些字段"""
        where, params = self.get_and_where(**kwargs)
        return self.update(self.TABLE, fields, values, where, param=params)

    def update_check_roll(self, uid='', cla_id='', time_id='', check_roll=0):
        return self.update_by(fields=["check_roll"], values=[check_roll], uid=uid, cla_id=cla_id, time_id=time_id)

    def query_one(self, time_id=0, uid='', cla_id=''):
        where = " where sc.time_id=%s and sc.uid=%s and sc.cla_id=%s"
        return self.db.get(self.sql + where, time_id, uid, cla_id)

    def full_query(self, uid='', cla_id=''):
        where = " where sc.uid=%s and sc.cla_id=%s order by class_date "
        classes = self.db.query(self.sql + where, uid, cla_id)
        changed = self.db.query(self.sql2 + where, uid, cla_id)
        if changed:
            return classes + changed
        return classes

    def get_changed_classes(self, uid='', cla_id=''):
        where = " where sc.uid=%s and sc.cla_id=%s order by class_date "
        return self.db.query(self.sql2 + where, uid, cla_id)

    def query_for_bbb(self):
        #TODO query for bigbluebutton
        pass

    def query_single_tb(self, **kwargs):
        where, params = self.get_and_where(**kwargs)
        return self.query(self.TABLE, where=where, param=params)


class MidStudentDateChanged(BaseDBModel):
    TABLE = tb("student_date_changed")
    fields = ["select_id", "uid", "cla_id", "src_workroom", "target_workroom",
              "src_date", "target_date", "src_time_id", "target_time_id",
              "handle", "operate_by"]

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def get_stu_operate_by_id(self, select_id=0, operate_by="student"):
        where, param = self.get_and_where(select_id=select_id, operate_by=operate_by)
        return self.get_one(self.TABLE, where, param)

    def get_by_selected_id(self, select_id=0):
        where, param = self.get_and_where(select_id=select_id)
        return self.query(self.TABLE, where=where, param=param)

    def check_has_changed(self, cla_id='', uid=''):
        where, param = self.get_and_where(cla_id=cla_id, uid=uid)
        return self.query(self.TABLE, where=where, param=param)

    def list_changed(self, p_n=1, size=p_size):
        pass


class MidStudentClassChanged(BaseDBModel):
    TABLE = tb("student_class_changed")
    fields = ["select_id", "src_workroom", "target_workroom",
              "src_time_id", "target_time_id", "src_date", "target_date"]

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def get_by_select_id(self, select_id=0):
        where, param = self.get_and_where(select_id=select_id)
        return self.query(self.TABLE, where=where, param=param)

    def update_by(self, cla_id='', uid='', fields=list(), values=list()):
        """更新某些字段，如uname, deal, handle, version"""
        where, params = self.get_and_where(cla_id=cla_id, uid=uid)
        return self.update(self.TABLE, fields, values, where, param=params)

    def list_changed(self, p_n=1, size=p_size):
        pass


class MidStudentRefund(BaseDBModel):
    TABLE = tb("student_refund")
    fields = ["uid", "cla_id"]

    @property
    def get(self):
        return self.TABLE

    def add(self, params):
        return self.insert(self.TABLE, self.fields, params)

    def list_changed(self, p_n=1, size=p_size):
        pass


def set_model(db):
    _mcwr = MidCourseWorkRoom(db)
    _mwr = MidWorkRoom(db)
    _mwrs = MidWorkRoomSingle(db)
    _mss = MidStudentSelected(db)
    _mwrd = MidWorkRoomDates(db)
    _msc = MidStudentClasses(db)
    _msdc = MidStudentDateChanged(db)
    _mscc = MidStudentClassChanged(db)
    _msr = MidStudentRefund(db)
    model = LogicModel(db)
    model.initial(mwr=_mwr, mcwr=_mcwr,
                  mss=_mss, mwrd=_mwrd,
                  msc=_msc, msdc=_msdc,
                  mwrs=_mwrs, mscc=_mscc,
                  msr=_msr)
    return model

