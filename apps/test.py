__author__ = 'windy'
#coding: utf-8


from base import BaseHandler
from utils import Route
from utils import sendmail
from http_msg import single_login
from datetime import datetime


@Route("/test/uname")
class TestPost(BaseHandler):
    def get(self, *args, **kwargs):
        uname = self.get_argument("uname")
        uid = self.get_argument("uid")
        if isinstance(uname, unicode):
            uname = uname.encode("utf-8")
            sso = single_login(uid, uname)
            email = "Student From LJL id=%s, name=%s\n" \
                    "Payed for:%s \n" \
                    "Class Table Link: http://yueke.speiyou.com/timetable/list/moodle?uid=%s&claId=%s\n" \
                    "SSO URL: %s" \
                    % (uid, uname, "test 000", uid, "classId", sso)
            sendmail(msg=email, subject="%s Student Pay For Class" % datetime.now())
            self.write("world")
        else:
            self.write("Hello")