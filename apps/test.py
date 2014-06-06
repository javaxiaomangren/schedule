__author__ = 'windy'
#coding: utf-8


from base import BaseHandler
from utils import Route

@Route("/test/post")
class TestPost(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("test_time_list.html")