#coding:utf8
import tornado.web


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


class Transaction(object):
    """
        处理事务集合
        db: torndb db connection
        Usage:
        with Transaction(db) as trans_db:
            trans_db.execute(sql)
            trans_db.commit()
    """
    def __init__(self, db):
        self.tran_db = db

    def __enter__(self):
        """set up things and return things"""
        self.tran_db._db.autocommit(False)
        return self.tran_db

    def __exit__(self, type, value, traceback):
        """tear down things"""
        self.tran_db.autocommit(True)


def nice_bool(value):
    if type(value) is bool:
        return value
    false = ('', 'no', 'off', 'false', 'none', '0', 'f')
    return str(value).lower().strip() not in false


def send_post():
    pass