# 怎样从0开始搭建一个测试框架_8

> 上次我们的用例中增加了断言。断言（检查点）这个东西对测试来说很重要。不然你怎么知道一个测试结果是对是错呢。unittest为我们提供了很多很好的断言，但是对于我们的项目可能是不够的。我们需要封装自己的断言方法。

这里我们简单封装一个断言，在utils中创建assertion.py文件，在其中创建断言：

```python
"""
在这里添加各种自定义的断言，断言失败抛出AssertionError就OK。
"""


def assertHTTPCode(response, code_list=None):
    res_code = response.status_code
    if not code_list:
        code_list = [200]
    if res_code not in code_list:
        raise AssertionError('响应code不在列表中！')  # 抛出AssertionError，unittest会自动判别为用例Failure，不是Error

```

这个断言传入响应，以及期望的响应码列表，如果响应码不在列表中，则断言失败。

在test_baidu_http.py中添加此断言：

```python
import unittest
from utils.config import Config, REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner import HTMLTestRunner
from utils.assertion import assertHTTPCode


class TestBaiDuHTTP(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.client = HTTPClient(url=self.URL, method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        assertHTTPCode(res, [400])
        self.assertIn('百度一下，你就知道', res.text)


if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='接口html报告')
        runner.run(TestBaiDuHTTP('test_baidu_http'))
```

我们添加断言，响应码在[400]中，执行会发现fail掉了。

在assertion.py中你可以添加更多更丰富的断言，响应断言、日志断言、数据库断言等等，请自行封装。

> 所有的代码我都放到了GITHUB上[传送](https://github.com/huilansame/Test_framework)，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的[QQ群:455478219](https://jq.qq.com/?_wv=1027&k=4EQQKFg)讨论。