# 怎样从0开始搭建一个测试框架_7

> 前面我们都是用的UI自动化的用例来实现的，如果我们想做接口框架怎么办？今天就扩展一下接口测试模块，这里我们需要用到requests库（接口是HTTP类型的，其他类型也有对应的库）

我们先在ReadMe.md中补上新加的依赖库。然后在utils中创建一个client.py的文件，在其中创建一个HTTPClient类：

```python
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
```

接下来写个用例，但是我们接口的用例跟UI混在一起总是不好，所以我们可以在test下创建一个interface的目录，里面创建test_baidu_http.py的用例文件。

这里你也可以在test下分成API和UI两层，分别在其中再进行分层，看情况而定吧。

test_baidu_http.py：

```python
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner


class TestBaiDuHTTP(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.client = HTTPClient(url=self.URL, method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        self.assertIn('百度一下，你就知道', res.text)


if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='接口html报告')
        runner.run(TestBaiDuHTTP('test_baidu_http'))
```

这里我们加了一句断言，没有断言怎么能叫用例，我们之前写的UI用例，也可以自己动手加上断言。

现在我们的框架既可以做UI测试，也能做接口测试了。如果你的接口类型不是HTTP的，请自己封装对应的Client类。socket库测TCP接口、suds库测SOAP接口，不论你是什么类型的接口，总能找到对应的Python库的。