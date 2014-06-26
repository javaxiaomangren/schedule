#coding:UTF-8
__author__ = 'windy'
import urllib
import urllib2
import httplib
import ujson
import traceback
import smtplib
import torndb
import tornado.web
from torndb import Row
from tornado.web import gen_log
from urllib2 import Request, urlopen
from config import *



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


def post2(data):
    conn = httplib.HTTPConnection('10.19.1.130', 10087)
    headers = {'Content-type': 'text/plain;charset=GBK'}
    conn.request('POST', '/CPAPlatform/TransformData', data, headers)
    response = conn.getresponse()
    print response.read()
    resp_data = response.read().decode('GBK').encode('UTF-8')
    return Row(ujson.loads(resp_data))


# def get_mysql():
#     return torndb.Connection(
#         host="localhost", database="schedule",
#         user="root", password="vR9PrPEjeVhBptInCrMBFCi7fBa0I7Y4XzNhK3KwWmQ1l3gYQTEqjnLAvHFZupC")


def get_mysql(dbname='schedule'):
    if debug:
        return torndb.Connection(
            host="localhost", database=dbname,
            user="root", password="")
    else:
        return torndb.Connection(
            host="localhost", database=dbname,
            user="root", password="vR9PrPEjeVhBptInCrMBFCi7fBa0I7Y4XzNhK3KwWmQ1l3gYQTEqjnLAvHFZupC")


def notify_me(func):
    """send a email where exceptions occur"""

    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            _sendmail("message==>%s\n\n\nHost Info:%s " % (traceback.format_exc(), "save deep and rti"),
                      'Exception When Run Function %s' % func.func_name)

    return wrapped


def _sendmail(msg='', subject='', to='windy.yang@huanxunedu.com'):
    """send a email with msg and subject
    :param msg:
    :param subject:
    """
    try:
        frm_user = 'CourseHandler@163.com'
        frm_passwd = '106yh!@#$'

        # smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver = smtplib.SMTP("smtp.163.com", 25)

        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(frm_user, frm_passwd)
        for m in mails:
            to = m
            header = 'To:%s\nFrom:%s\nSubject:%s\n' % (to, frm_user, subject)
            message = header + '\n %s\n\n' % msg.encode("utf-8")
            smtpserver.sendmail(frm_user, to, message)
        smtpserver.close()
    except:
        gen_log.info(traceback.format_exc())


def sendmail(msg='', subject=''):
    _sendmail(msg=msg, subject=subject)


class CheckRoll(object):
    NORMAL = 0
    FINISHED = 1
    LOCKED = 2
    LATE = 3
    ABSENT = 4
    CHANGE = 6
    NAME = {
        0: "等待上课",
        1: "完成",
        2: "预考勤",
        3: "迟到",
        4: "缺席",
        6: "已调课",
        7: "调试课",
    }
    TRAIL = 7


def list_page(display, p_count, p_no):
    x, y = 1, p_count
    rount = p_count - display + 1
    if rount > 0:
        if rount > display:
            if display <= p_no <= rount:
                x = p_no
                y = display + p_no - 1
            elif rount < p_no <= p_count:
                x = rount
                y = p_count
            else:
                x = 1
                y = display
        else:
            if p_no >= display:
                x = rount
                y = p_count
            else:
                x = 1
                y = display
    return range(x, y + 1)


def write_to_file(uid, cla_id, line):
    with open(downloads % (uid + cla_id), 'w') as f:
        f.write(line)
# write_to_file("1223334444", "K00001", "add, student, %s, %s" % ("1223334444", "A-1500-K1-c105"))

