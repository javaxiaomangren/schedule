__author__ = 'windy'
import tornado.web


class GradeEntry(tornado.web.UIModule):
    def render(self, entry, show_comments=False):
        self.render_string("modules/grade-entry.html", entry=entry, show_comments=show_comments)