﻿#!/usr/bin/env python
#coding: utf-8



import os.path
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import apps.view_handle
import apps.admin_handles
import apps.teacher_handle
# import apps.test
from tornado.options import define, options
from apps.entry import GradeEntry

from apps.utils import Route
from apps.db_model import set_model
import sys

reload(sys)
sys.setdefaultencoding('utf8')


define("port", default=8088, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="schedule database host")
define("mysql_database", default="schedule", help="schedule database name")
define("mysql_user", default="root", help="schedule database user")
define("mysql_password", default="", help="schedule database password")
# define("solr_path", default="http://110.75.189.239:9990/solr/schedule", help="solr path for search")
define("prefork", default=False, help="pre-fork across all CPUs", type=bool)
define("showurls", default=True, help="Show all routed URLs", type=bool)
define("debug", default=True, help="Show all routed URLs", type=bool)


class Application(tornado.web.Application):
    def __init__(self, mysql_database=None):
        settings = dict(
            site_title=u"培优网－约课系统",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"GradeEntry": GradeEntry},
            # xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/login",
            debug=options.debug,
        )
        handles = Route.get_routes()  # defined with route decorators
        tornado.web.Application.__init__(self, handles, **settings)
        self.database = mysql_database and mysql_database or options.mysql_database
        self.db = torndb.Connection(
            host=options.mysql_host, database=self.database,
            user=options.mysql_user, password=options.mysql_password)
        # self.solr_path = options.solr_path
        self.static_path = settings["static_path"]
        self.db_model = set_model(self.db)

#initialize handles
# __import__('apps', globals(), locals(), ["admin_handles" "class_handle", "test", "entry"], -1)


def main():
    tornado.options.parse_command_line()
    if options.showurls:
        for each in Route.get_routes():
            print each._path.ljust(20), "mapping to RequestHandle-->", each.handler_class.__name__
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    print "Starting tornado server on port", options.port
    if options.prefork:
        print "\tpre-forking"
        http_server.bind(options.port)
        http_server.start()
    else:
        http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

#TODO 自动考勤
if __name__ == "__main__":
    main()
