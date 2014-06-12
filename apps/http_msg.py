#coding:UTF-8
__author__ = 'windy'
import hashlib
import urllib
import ujson
from urllib2 import Request, urlopen
from torndb import Row
from tornado.web import gen_log as logger
from utils import post_u8
import traceback

_plat = "php"
_sys = "testing"
url_prefix = "http://ft.speiyou.com"
# url_prefix = "http://wjiao.speiyou.cn"
url_sso = "http://waijiao.speiyou.com/auth/token/auto_login.php"
debug = "no-debug"


def get_with_header(headers, url):
    if debug == "debug":
        return ujson.dumps({"rlt": True, "msg": "True", "data": "Skip invoke "})
    req = Request(url, headers=headers)
    return urlopen(req).read()


def mk_md5(summary, plat=_plat, sys=_sys, key="com.xes.employee"):
    s = summary + plat + sys + key
    return hashlib.md5(s.encode("UTF-8")).hexdigest()


def log_it(rs):
    rlt = Row(ujson.loads(rs))
    logger.info("Result: rlt:[%s], data:[%s]", rlt.rlt, rlt.data)
    return rlt


def cla_build_status(cla_id):
    """
        http://phpapi.cakephp.com/huanxun/v1/cla_build_status.json
        修改班级构建状态
    """
    #TODO 开班后调用
    url = url_prefix + "/huanxun/v1/cla_build_status.json?claId=%s"
    summary = cla_id
    md5 = mk_md5(summary)
    logger.info("Invoke %s ", url)
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % cla_id)
    return log_it(x)


def reg_plan_status(uid, cla_id):
    """
    更新报课的排课状态接口：
        http://phpapi.cakephp.com/huanxun/v1/reg_plan_status.json
    """
    summary = uid + cla_id
    md5 = mk_md5(summary)
    url = url_prefix + "/huanxun/v1/reg_plan_status.json?uid=%s&claId=%s"
    logger.info("Invoke %s ", url)

    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, cla_id))
    return log_it(x)


def attendances(uid, cla_id, cuc_id, status):
    """
    # 修改考勤状态接口：
    uid:
    cuc_id:课时Id
    status:考勤状态
    # http://phpapi.cakephp.com/huanxun/v1/attendances.json
    """
    # status = '0'
    # cuc_id = "16"
    summary = uid + cuc_id + status
    md5 = mk_md5(summary)
    url = url_prefix + "/huanxun/v1/attendances.json?uid=%s&cucId=%s&claId=%s&Status=%s"
    logger.info("Invoke %s ", url)
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, cuc_id, cla_id, status))
    return log_it(x)


def sms(uid, content):
    """
    短信接口：

    """
    md5 = mk_md5(uid)
    url = url_prefix + "/huanxun/v1/sms.json?uid=%s&content=%s"
    logger.info("Invoke %s ", url)
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, urllib.quote(content)))
    return log_it(x)


def courses(uid, cla_id, datas):
    """
    修改课程信息接口：
        http://phpapi.cakephp.com/huanxun/v1/courses.json
    datas: [dict, dict] 原课程和目标课程的对应关系
    """
    result = dict()
    result["uid"] = uid
    result["claId"] = cla_id
    data_str = ujson.dumps(datas)
    result["datas"] = data_str
    url = url_prefix + "/huanxun/v1/courses.json"

    summary = uid + cla_id
    md5 = mk_md5(summary)
    logger.info("Invoke %s ", url)
    if debug == "debug":
        return Row({"rlt": True, "data": "Skip invoke "})
    logger.info(data_str)
    x = post_u8(url, result, {"sys": _sys, "plat": _plat, "md5": md5})
    return log_it(x)


def single_login(uid, uname):
    sso_url = url_sso + '?uname=%s&user=%s' % (uname, uid)
    try:
        rs = None
        try:
            rs = urlopen(sso_url)
        except:
            logger.info("1-Single Login Failed, %s", traceback.format_exc())
        if not rs:
            try:
                print url_sso + '?uname=%s&user=%s' % (urllib.quote(uname), uid)
                rs = urlopen(url_sso + '?uname=%s&user=%s' % (urllib.quote(uname), uid))
                logger.info(rs)
            except:
                logger.info("2-Single Login Failed, %s", traceback.format_exc())
    except:
        logger.info("Single Login Failed, %s", traceback.format_exc())
    finally:
        return sso_url
        # print single_login(uid='987654321000', uname=u'李华人')