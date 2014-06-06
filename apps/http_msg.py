#coding:UTF-8
__author__ = 'windy'
import hashlib
import urllib
import ujson
from urllib2 import Request, urlopen
from torndb import Row
from tornado.web import gen_log as logger
from utils import post_u8
import calendar
from datetime import datetime

_plat = "php"
_sys = "testing"
url_prefix = "http://ft.speiyou.com"
# ft.speiyou.com  59.151.117.147


def get_with_header(headers, url):
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

#0未考勤，1完成， 2预考勤
# print attendances('234878', "ff80808146463d4301466b45a38b0208", '4168', '1').data
# print attendances('234878', "ff80808146463d4301466b45a38b0208", '4169', '2').data
# print attendances('191655', "ff80808146463d4301465fb3307000a1", '141', '3').data
# print attendances('191655', "ff80808146463d4301465fb3307000a1", '142', '2').data
# print attendances('191655', "ff80808146463d4301465fb3307000a1", '143', '1').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '80', '1').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '81', '1').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '82', '1').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '83', '3').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '84', '1').data
# print attendances('172479', "ff80808146463d430146476fad76003d", '85', '0').data
# print attendances('172001', "ff808081462d55560146415cc0770165", '500', '0').data


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
    x = post_u8(url, result, {"sys": _sys, "plat": _plat, "md5": md5})
    return log_it(x)


def single_login(uid, uname):
    #TODO single login
    secret_salt = '123456'
    timestamp = calendar.timegm(datetime.now().utctimetuple())
    user = str(uid)
    newuser = '1'
    fn = ''
    ln = uname
    cohortname = ''
    email = uid+"@101tal.com"
    city = 'Beijing'
    country = 'CN'
    token = hashlib.md5(str(timestamp) + user + email + secret_salt).hexdigest()
    url = "http://localhost:8080/moodle22/auth/token/index.php"
    sso_url = url + '?user=%s&token=%s&timestamp=%s' \
                    '&email=%s&newuser=%s&cohortname=%s' \
                    '&fn=%s&ln=%s&city=%s&country=%s' % \
              (user, token, timestamp, email, newuser, cohortname, fn, ln, city, country)
    print sso_url
    return urlopen(sso_url)

# print single_login('121212', "XiaoMIng")


#
# $token = crypt($timestamp.$user.$email,$secret_salt);
#
# $url = 'http://lms.astm.org/auth/token/index.php';
#
# $sso_url = $url.'?user='.$user.'&token='.$token.'&timestamp='.$timestamp.'&email='.$email.'&newuser='.$newuser.'&cohortname='.$cohortname.'&fn='.$fn.'&ln='.$ln.'&city='.$city.'&country='.$country;
#
# header("Location: ".$sso_url);