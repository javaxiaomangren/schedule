import unittest
from urllib import urlencode

import tornado.testing
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from tornado.httpclient import HTTPRequest

from app import Application


class BaseHttpTestCase(AsyncHTTPTestCase, LogTrapTestCase):

    def setUp(self):
        super(BaseHttpTestCase, self).setUp()

    def get_app(self):
        return Application(mysql_database='test_insurance')

    def get(self, url, data=None, headers=None, follow_redirects=False):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, True)
            if '?' in url:
                url += '&%s' % data
            else:
                url += '?%s' % data
        return self._fetch(url, 'GET', headers, follow_redirects=follow_redirects)

    def post(self, url, data=None, headers=None, follow_redirects=False):
        if data is not None:
            if isinstance(data, dict):
                data = urlencode(data, True)

        return self._fetch(url, 'POST', data, headers, follow_redirects=follow_redirects)

    def _fetch(self, url, method, data=None, headers=None, follow_redirects=True):
        full_url = self.get_url(url)
        request = HTTPRequest(full_url, follow_redirects=follow_redirects,
                              headers=headers, method=method, body=data)
        self.http_client.fetch(request, self.stop)
        return self.wait()


class AdminHandlersTest(BaseHttpTestCase):

    def test_login(self):
        response = self.get('/auth/login')
        self.assertTrue('username' in response.body)
        response = self.post('/auth/login', data={'username': 'a', 'password': 'b'})
        self.assertTrue('success' in response.body)

    def test_add_company(self):
        data = {'company_name': 'test', 'logo': 'adfjoj91023osdaijdfasdjfasf.png'}
        rep = self.post('/admin/company', data=data)
        self.assertTrue(int(rep.body) > 0)
        #TODO test get
        # rep = self.get('/admin/company')
        # print rep

    def test_add_category(self):
        data = {'category_name': 'test_category_name'}
        rep = self.post('/admin/category', data=data)
        self.assertTrue(int(rep.body) > 0)
        #TODO test get category

    def test_add_tags(self):
        data = {'tag_name': 'tag_name_value'}
        rep = self.post('/admin/tags/', data=data)
        self.assertTrue(int(rep.body) > 0)
        #TODO test get category

    def test_add_image(self):
        data = {'img_name': 'test_name', 'img_url': 'test_url', 'refered_id': 1, 'type': 0}
        rep = self.post('/admin/img', data=data)
        self.assertTrue(int(rep.body) > 0)
        #TODO test get category

    def test_add_insurance(self):
        data = {'pro_name': 'test_name',
                'min_age': 7,
                'max_age': 36500,
                'notice': 'important things',
                'description': 'description',
                'tags': 'tag1,tag2,tag3',
                'suitable': 'people older',
                'company_id': 1,
                'category_id': 1,
                'example': 'example files',
                'price': 1.0,
                'sales_volume': 10,
                'buy_count': 1
                }
        rep = self.post('/admin/insurance', data=data)
        self.assertTrue(int(rep.body) > 0)

    def test_add_clause(self):
        data = {'clause_name': 'this is a clause name',
                'description': 'desc',
                'category_id': 1}
        rep = self.post('/admin/clause', data=data)
        self.assertTrue(int(rep.body) > 0)

    def test_add_insu_clause(self):
        data = {'insu_id': 1, 'clause_id': 1, 'limits': 1, 'insu_days': 1, 'price': 1}
        rep = self.post('/admin/insu_clause', data=data)
        self.assertTrue(int(rep.body) > 0)

    # def test_test(self):
    #     self.get('/admin/test')


def all():
    return unittest.defaultTestLoader.loadTestsFromName('test_handles')

if __name__ == '__main__':
    tornado.testing.main()    
