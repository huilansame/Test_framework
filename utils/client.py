import requests
from utils.log import logger

METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


class UnSupportMethodException(Exception):
    pass


class RequestFailed(Exception):
    pass


class HTTPClient(object):
    def __init__(self, url, method='GET', headers=None, cookies=None):
        """headers: Must be a dict. Such as headers={'Content_Type':'text/html'}"""
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            raise UnSupportMethodException('不支持的method:{0}，请检查传入参数！'.format(self.method))

        self.set_headers(headers)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, params=None, data=None, **kwargs):
        response = self.session.request(method=self.method, url=self.url, params=params, data=data, **kwargs)
        response.encoding = 'utf-8'
        logger.debug('{0} {1}'.format(self.method, self.url))
        logger.debug('请求成功: {0}\n{1}'.format(response, response.text))
        return response


if __name__ == '__main__':
    h = HTTPClient('http://www.baixxdu.com')
    print(h.send().text)