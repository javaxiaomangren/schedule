#coding:UTF-8
from collections import OrderedDict

__author__ = 'windy'
#!/usr/bin/env python
import tornado.web
import urllib
import urllib2
from urllib2 import Request, urlopen
import httplib
import ujson
import hashlib
from torndb import Row


class Route(object):
    """
    Example
    -------

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

    @route('/some/path', name='other')
    class SomeOtherRequestHandler(RequestHandler):
        pass

    my_routes = route.get_routes()

    In your Application:
    Application = Application(my_routes, **settings)
    """
    _routes = []

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    def __call__(self, _handler):
        """gets called when we class decorate"""
        name = self.name and self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, name=name))
        return _handler

    @classmethod
    def get_routes(cls):
        return cls._routes


def route_redirect(from_, to, name=None):
    Route._routes.append(tornado.web.url(from_, tornado.web.RedirectHandler, dict(url=to), name=name))


def nice_bool(value):
    if type(value) is bool:
        return value
    false = ('', 'no', 'off', 'false', 'none', '0', 'f')
    return str(value).lower().strip() not in false


def post_u8(url, data, headers):
    data = urllib.urlencode(data)
    req = Request(url, data=data, headers=headers)
    return urlopen(req).read()


def post(url, data):
    req = Request(url)
    data = urllib.urlencode(data)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def get_with_header(headers, url):
    req = Request(url, headers=headers)
    return urlopen(req).read()


def post2(data):
    conn = httplib.HTTPConnection('10.19.1.130', 10087)
    headers = {'Content-type': 'text/plain;charset=GBK'}
    conn.request('POST', '/CPAPlatform/TransformData', data, headers)
    response = conn.getresponse()
    print response.read()
    resp_data = response.read().decode('GBK').encode('UTF-8')
    return Row(ujson.loads(resp_data))

_plat = "php"
_sys = "testing"
url_prefix = "http://phpapi.cakephp.com"


def mk_md5(summary, plat=_plat, sys=_sys, key="com.xes.employee"):
    s = summary + plat + sys + key
    #TODO md5 cache
    return hashlib.md5(s.encode("UTF-8")).hexdigest()


# claId = "8a8185ce45fea8070145feb4f1850006"
# regId : 8a8185ce45fea8070145fec2c9d0001a
# uid = "158023"


def cla_build_status(cla_id):
    """
    http://phpapi.cakephp.com/huanxun/v1/cla_build_status.json
    修改班级构建状态
    """
    #TODO 开班后调用
    url = url_prefix + "/huanxun/v1/cla_build_status.json?claId=%s"
    summary = cla_id
    md5 = mk_md5(summary)
    print "claId", cla_id
    print "summary", summary
    print "md5", md5
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % cla_id)
    return Row(ujson.loads(x))


def reg_plan_status(uid, cla_id):
    """
    更新报课的排课状态接口：
        http://phpapi.cakephp.com/huanxun/v1/reg_plan_status.json
    """
    summary = uid + cla_id
    md5 = mk_md5(summary)
    url = url_prefix + "/huanxun/v1/reg_plan_status.json?uid=%s&claId=%s"
    print "uid", uid
    print "claId", cla_id
    print "summary", summary
    print "md5", md5
    print url % (uid, cla_id)

    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, cla_id))
    return Row(ujson.loads(x))


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
    print "uid", uid
    print "cucId", cuc_id
    print "Status", status
    print "summary", summary
    print "md5", md5

    print url % (uid, cuc_id, cla_id, status)
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, cuc_id, cla_id, status))
    return Row(ujson.loads(x))


def sms(uid, content):
    """
    短信接口：

    """
    md5 = mk_md5(uid)
    url = url_prefix + "/huanxun/v1/sms.json?uid=%s&content=%s"
    print "uid", uid
    print "summary", uid
    print "md5", md5

    print url % (uid, urllib.quote(content))
    x = get_with_header({"sys": _sys, "plat": _plat, "md5": md5}, url % (uid, urllib.quote(content)))
    return Row(ujson.loads(x))


def courses(uid, cla_id, datas):
    """
    修改课程信息接口：
        http://phpapi.cakephp.com/huanxun/v1/courses.json
    datas: [dict, dict] 原课程和目标课程的对应关系
    """

    result = dict()
    result["uid"] = uid
    result["claId"] = cla_id
    # data = OrderedDict()
    # data["sourceBeiliCucId"] = "17"
    # data["sourceTeacherId"] = 2
    # data["sourceCourseDate"] = "2014-05-18"
    # data["sourceStartTime"] = "09:00:00"
    # data["sourceEndTime"] = "09:30:00"
    # data["sourceClassroom"] = "MN0002"
    # data["sourceStatus"] = 0
    # data["targetBeiliCucId"] = "33"
    # data["targetTeacherId"] = 33
    # data["targetCourseDate"] = "2014-08-24"
    # data["targetStartTime"] = "10:00:00"
    # data["targetEndTime"] = "10:30:00"
    # data["targetClassroom"] = "MN001322"
    # data["targetStatus"] = 6
    # data1 = OrderedDict()
    # data1["sourceBeiliCucId"] = "18"
    # data1["sourceTeacherId"] = 2
    # data1["sourceCourseDate"] = "2014-05-19"
    # data1["sourceStartTime"] = "09:00:00"
    # data1["sourceEndTime"] = "09:30:00"
    # data1["sourceClassroom"] = "MN0002"
    # data1["sourceStatus"] = 0
    # data1["targetBeiliCucId"] = "38"
    # data1["targetTeacherId"] = 38
    # data1["targetCourseDate"] = "2014-08-29"
    # data1["targetStartTime"] = "11:00:00"
    # data1["targetEndTime"] = "11:30:00"
    # data1["targetClassroom"] = "MN0013344"
    # data1["targetStatus"] = 6
    data_str = ujson.dumps(datas)
    result["datas"] = data_str
    url = url_prefix + "/huanxun/v1/courses.json"

    summary = uid + cla_id
    md5 = mk_md5(summary)
    print "uid", uid
    print "claId", cla_id
    print "summary", summary
    print "md5", md5
    print "data:", result
    x = post_u8(url, result, {"sys": _sys, "plat": _plat, "md5": md5})
    return Row(ujson.loads(x))

    # test03()
    # test04()
    # test05()