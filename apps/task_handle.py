__author__ = 'windy'
#coding: UTF8
import utils
from http_msg import single_login
from db_model import *
import config
from tornado.web import gen_log
import traceback
import wget
import re


db = utils.get_mysql(dbname=config.moodle_db)
# task_model = MidTask(db)
task_model = None


def get(url):
    try:
        print url
        gen_log.info("GET: URL[%s]", url)
        return utils.urlopen(url).read()
    except:
        gen_log.info(traceback.format_exc())
        print traceback.format_exc()
        return None


def ssoed(uid):
    """
    Check if user is registered int
    """
    url = config.moodle_url + '/speiyou/check_sso.php?uid=' + uid
    rs = get(url)
    if rs and "EMPTY_USER" != rs:
        gen_log.info("Token User Exists uid=[%s], moodleUserId[%s]", uid, rs)
        return rs


def touch_sso(task):
    uid, uname = task.content.split("=")
    for x in range(3):
        single_login(uid, uname)
        if ssoed(uid):
            task_model.finished(task.id)
            return True


def check_enrolled(uid, workroom):
    url = config.moodle_url + "/speiyou/check_enrol.php?uid=%s&idnumber=%s" % (uid, workroom)
    rs = get(url)
    if rs and rs == "True":
        return True


def get_classtable_url(uid='981495', cla_id='ff808081468666ee01468f7ee78d1142'):
    """
    设置课表链接
    """
    url = "%s/timetable/list/moodle?uid=%s&claId=%s" % (config.mid_url, uid, cla_id)
    template = '<p style="margin: 0 0 0 0;">' \
               '<iframe scrolling="no" width="%s" height="250px" ' \
               'src="%s" frameborder="0"></p>'

    return template % ("100%", url)


def get_course(idnumber):
    return db.get("select id from mdl_course where idnumber=%s", idnumber)


def get_course_url(idnumber):
    return "%s/course/view.php?id=%s" % (config.moodle_url, get_course(idnumber).id)


def get_section(idnumber):
    course = get_course(idnumber)
    section = db.get("select id from  mdl_course_sections cs "
                     "where cs.course=%s and cs.section=%s and cs.name=%s",
                      course.id, config.moodle_section, config.moodle_section_name)
    return section.id


def get_labels(src, target):
    sql = """SELECT cm.id as edit, cm.course, cm.instance, l.intro
             FROM mdl_course_modules cm
                join mdl_course c on c.id=cm.course
                join mdl_label l on cm.instance = l.id
             where c.idnumber=%s
            """
    src = db.get(sql, src)
    target = db.get(sql, target)
    #已经更改了course的name 和idnumber
    return target, src



def clear_course_cache(idnumber=''):
    return db.execute_rowcount("update mdl_course set modinfo=%s, sectioncache=%s where idnumber=%s", None, None, idnumber)


def update_class_table(url, idnumber):
    course = get_course(idnumber)
    if course:
        db.execute_rowcount("update mdl_course_sections cs set cs.summary=%s "
                            "where cs.course=%s and cs.section=%s and cs.name=%s",
                            url, course.id, config.moodle_section, config.moodle_section_name)
        db.execute_rowcount("update mdl_course set modinfo=null , sectioncache=null where id=%s", course.id)
        return True

    return None


def update_moodle_course_name(src, target):
    src_c = get_course(src)
    target_c = get_course(target)
    try:
        db._db.autocommit(False)
        rs1 = db.execute_rowcount("update mdl_course set fullname=%s, idnumber=%s "
                                  "where id=%s ", target, target, src_c.id)
        if rs1:
            rs2 = db.execute_rowcount("update mdl_course set fullname=%s, shortname=%s, idnumber=%s "
                                      "where id=%s ", src, src, src, target_c.id)
            if rs2:
                db._db.commit()
                return True
        db._db.rollback()
    except:
        db._db.rollback()
    finally:
        db._db.autocommit(True)


def update_vc_id(src, target):
    src_course = get_course(src).id
    target_course = get_course(target).id
    # http://localhost:8080/c03/index/course/modedit.php?update=6286&return=0&sr=0
    src_lab = db.get("select id, intro from mdl_label l join mdl_course c on l.course=c.id  where c.id=%s", src_course)
    target_lab = db.get("select id, intro from mdl_label l join mdl_course c on l.course=c.id  where c.id=%s", target_course)
    if src_lab and target_lab:
        db.executemany("update mdl_label set intro=%s where id=%s",
                       [(target_lab.intro, src_lab.id), (src_lab.intro, target_lab.id)])
    return src_lab, target_lab


def update_course_shortname(idnumber, name):
    return db.execute_rowcount("update mdl_course set shortname=%s where idnumber=%s", name, idnumber)


def change_workroom(src, target):
    #get one id
    #set src.fullname=target, src.idnumber=target
    #set target.fullname=src, target.shortname=src target.idnumber=src
    pass


def update_tid(idnumber, tid):
    pass


def set_file_url(uid, cla_id):
    """设置enrol文件链接"""
    url = config.moodle_url + '/speiyou/download_flatfile.php?fileName=%s&domain=%s' % \
        (uid+cla_id, config.mid_domain)
    return url


def get_cron_url():
    return config.moodle_url + '/admin/cron.php'


def get_edit_classtable(workroom):
    section = get_section(workroom)
    # http://localhost:8080/c03/index/course/editsection.php?id=2259&sr=0
    return "%s/course/editsection.php?id=%s&sr=0" % (config.moodle_url, section)


def get_edit_label(_id):
    return "%s/course/modedit.php?update=%s&return=0&sr=0" % (config.moodle_url, _id)


def exe_cron():
    url = get_cron_url()
    wget.download(url)


def send_enrol_file(uid, cla_id):
    url = set_file_url(uid, cla_id)
    if ssoed(uid):
        rs = get(url)
        if rs == "True":
            exe_cron()
            return True
        else:
            gen_log.info("Failed to send enrol file [%s], result[%s]", uid + cla_id, rs)
    return False

def change_teacher(task):
    """
    转班信息转换，
     1.enrol stu and teacher
     2.change course name
     3.change VC
     4.change Teacher
    """
    pass


def set_when_payed(uid, cla_id, uname, workroom):
    send_enrol_file(uid, cla_id)
    url = get_classtable_url(uid, cla_id)
    update_class_table(url, workroom)
    update_course_shortname(workroom, uname)



# set_when_payed("1234", "K00002", u'细化', "A-1400-K2-m208")
# update_course_shortname(u'李新华', "A-0930-K2-m208")

# update_vc_id(291)