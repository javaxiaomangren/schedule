__author__ = 'windy'
#coding: utf-8
import traceback
import ujson
import json
from datetime import datetime, timedelta
from utils import *
from http_msg import mk_md5
import sys
if sys.version_info < (2, 7):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

import tornado.web
from torndb import Row
from tornado.log import gen_log as logger
from db_model import msg


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    @property
    def db_model(self):
        return self.application.db_model

    def auto_commit(self, flag=True):
        self.db._db.autocommit(flag)

    def commit(self):
        self.db._db.commit()

    def rollback(self):
        self.db._db.rollback()

    def get_template_namespace(self):
        ns = super(BaseHandler, self).get_template_namespace()
        ns.update({
            'CheckRoll': CheckRoll,
            "get_pages": list_page
        })

        return ns

    def get_current_user(self):
        user = self.get_secure_cookie("user_speiyou")
        row = self.db.get("SELECT role, password FROM user where username=%s", user)
        if row:
            return user
        return None

    def write_error(self, status_code, **kwargs):

        if status_code in [403, 404, 500, 503]:
            filename = '200.html'
            print 'rendering filename: ', filename
            return self.render_string(filename, entry=msg())
        #
        # return "<html><title>%(code)d: %(message)s</title>" \
        #         "<body class='bodyErrorPage'>%(code)d: %(message)s</body>"\
        #         "</html>" % {
        #         "code": status_code,
        #         "message": httplib.responses[status_code],
        #         }


@Route("/login", name="Login")
class LoginHandle(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("login.html", msg=None)

    def post(self, *args, **kwargs):
        user = self.get_argument("username")
        passwd = self.get_argument("passwd")
        row = self.db.get("SELECT role, password FROM user where username=%s", user)
        md5 = mk_md5(passwd)
        if row and row.password == unicode(md5):
            self.set_secure_cookie("user_speiyou", user, expires_days=1)
            if row.role == "teacher":
                self.render("admin/base_teacher.html", tid=user)
            else:
                self.render("admin/base.html")
        else:
            self.render("login.html", entry=Row({"msg": "Wrong login"}))


@Route("/logout", name="Log Out")
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user_speiyou")
        self.redirect(self.get_argument("next", "/login"))


def authorization(summary, headers):
    """头部信息加密验证"""
    plat = headers.get("plat", None)
    sys = headers.get("sys", None)
    md5 = headers.get("md5", None)
    if summary and plat and sys and md5:
        m_md5 = mk_md5(summary, plat, sys)
        return md5 == m_md5
    return None



