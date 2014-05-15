__author__ = 'windy'
import urllib
import urllib2
import ujson


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

def main():
    posturl = "http://219.236.247.203/api/class/add"
    data = {'email':'myemail', 'password':'mypass', 'autologin':'1', 'submit':"ss", 'type':''}
    print post(posturl, data)

if __name__ == '__main__':
    main()

