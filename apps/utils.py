__author__ = 'windy'
#!/usr/bin/env python
#coding:UTF-8
import tornado.web
from urllib2 import Request, urlopen
import httplib
import ujson
import hashlib
from torndb import Row


class route(object):
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
    route._routes.append(tornado.web.url(from_, tornado.web.RedirectHandler, dict(url=to), name=name))


def nice_bool(value):
    if type(value) is bool:
        return value
    false = ('', 'no', 'off', 'false', 'none', '0', 'f')
    return str(value).lower().strip() not in false


def post_u8(data, url):
    headers = {'Content-type': 'text/plain;charset=UTF-8'}
    req = Request(url, data, headers)
    return urlopen(req).read()


def post2(data):
    conn = httplib.HTTPConnection('10.19.1.130', 10087)
    headers = {'Content-type': 'text/plain;charset=GBK'}
    conn.request('POST', '/CPAPlatform/TransformData', data, headers)
    response = conn.getresponse()
    print response.read()
    resp_data = response.read().decode('GBK').encode('UTF-8')
    return Row(ujson.loads(resp_data))


def mk_md5(summary, plat, sys, key="com.xes.employee"):
    s = summary + plat + sys + key
    #TODO md5 cache
    return hashlib.md5(s.encode("UTF-8")).hexdigest()

print mk_md5("a", "b", "c")
