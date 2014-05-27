__author__ = 'windy'
import urllib2
import ujson
from utils import mk_md5


def post(url, data, headers):
    req = urllib2.Request(url, headers=headers)
    # data = urllib.urlencode(data)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

url_prefix = "http://localhost:8081"
uid = "80000000"
claId = "8a8185ce4613b5b6014613cb4fcc0017"
base_data = {"uid": uid, "claId": claId}
plat = "python"
sys = "testing"

header = {"plat": plat, "sys": sys, "md5": ""}


def print_info(**kwargs):
    print "========================================"
    for k in kwargs:
        print k, kwargs[k]


def test_api(data, api, headers):
    url = url_prefix + api
    print_info(test_for=url, data=data)
    print post(url, ujson.dumps(data), headers)


def select_class(data, api):
    url = url_prefix + api
    p = "&".join(map(lambda k: k + "=" + data[k], data))
    real_url = url + "?" + p
    print_info(test_for=real_url)
    print urllib2.urlopen(real_url).read()


#Test Select class
def test_select():
    select_data = dict(base_data)
    select_data["planId"] = "1"
    select_class(select_data, "/timetable/select")


#Test Release
def test_release():
    header["md5"] = mk_md5(uid+claId, plat, sys)
    test_api(base_data, "/api/class/release", header)


def test_payed():
    header["md5"] = mk_md5(uid+claId, plat, sys)
    test_api(base_data, "/api/class/payed", header)


def test_refund():
    header["md5"] = mk_md5(uid+claId, plat, sys)
    test_api(base_data, "/api/class/refund", header)

# test_select()
test_payed()
test_refund()
