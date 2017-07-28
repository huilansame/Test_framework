# 怎样从0开始搭建一个测试框架_4

> 这一步我们需要用到并修改HTMLTestRunner.py，它本身是基于PY2的，简单而实用，之前博主对其进行了美化，并且改成了中文（[下载链接](http://download.csdn.net/detail/huilan_same/9598558)）。
> 现在博主基于此进行了对PY3的修改，增加了对subTest的支持。

1. StringIO -> io
2. 去掉decode
3. 增加addSubTest()

部分修改内容：

```python
# import StringIO  # PY3改成了io库
import io
...
  def startTest(self, test):
          TestResult.startTest(self, test)
          # just one buffer for both stdout and stderr
          # self.outputBuffer = StringIO.StringIO()
          self.outputBuffer = io.StringIO()
...
# 添加addSubTest方法，将有subTest的Case拆分成多个Case，均在报告中输出。这点处理与unittest的TextRunner并不相同，细心的同学可以试验下，看看它是怎么处理的。
    def addSubTest(self, test, subtest, err):
            if err is not None:
                if getattr(self, 'failfast', False):
                    self.stop()
                if issubclass(err[0], test.failureException):
                    self.failure_count += 1
                    errors = self.failures
                    errors.append((subtest, self._exc_info_to_string(err, subtest)))
                    output = self.complete_output()
                    self.result.append((1, test, output + '\nSubTestCase Failed:\n' + str(subtest),
                                        self._exc_info_to_string(err, subtest)))
                    if self.verbosity > 1:
                        sys.stderr.write('F  ')
                        sys.stderr.write(str(subtest))
                        sys.stderr.write('\n')
                    else:
                        sys.stderr.write('F')
                else:
                    self.error_count += 1
                    errors = self.errors
                    errors.append((subtest, self._exc_info_to_string(err, subtest)))
                    output = self.complete_output()
                    self.result.append(
                        (2, test, output + '\nSubTestCase Error:\n' + str(subtest), self._exc_info_to_string(err, subtest)))
                    if self.verbosity > 1:
                        sys.stderr.write('E  ')
                        sys.stderr.write(str(subtest))
                        sys.stderr.write('\n')
                    else:
                        sys.stderr.write('E')
                self._mirrorOutput = True
            else:
                self.subtestlist.append(subtest)
                self.subtestlist.append(test)
                self.success_count += 1
                output = self.complete_output()
                self.result.append((0, test, output + '\nSubTestCase Pass:\n' + str(subtest), ''))
                if self.verbosity > 1:
                    sys.stderr.write('ok ')
                    sys.stderr.write(str(subtest))
                    sys.stderr.write('\n')
                else:
                    sys.stderr.write('.')
...
  def run(self, test):
          "Run the given test case or test suite."
          result = _TestResult(self.verbosity)
          test(result)
          self.stopTime = datetime.datetime.now()
          self.generateReport(test, result)
          # print >>>sys.stderr '\nTime Elapsed: %s' % (self.stopTime-self.startTime)  # PY3的print需处理
          print('\nTime Elapsed: %s' % (self.stopTime-self.startTime), file=sys.stderr)
          return result
...
        # PY3这里不用decode了，直接处理
        # if isinstance(o,str):
        #             # TODO: some problem with 'string_escape': it escape \n and mess up formating
        #             # uo = unicode(o.encode('string_escape'))
        #             # uo = o.decode('latin-1')
        #             uo = o.decode('utf-8')
        #         else:
        #             uo = o
        #         if isinstance(e,str):
        #             # TODO: some problem with 'string_escape': it escape \n and mess up formating
        #             # ue = unicode(e.encode('string_escape'))
        #             # ue = e.decode('latin-1')
        #             ue = e.decode('utf-8')
        #         else:
        #             ue = e

                script = self.REPORT_TEST_OUTPUT_TMPL % dict(
                    id = tid,
                    # output = saxutils.escape(uo+ue),
                    output = saxutils.escape(o+e),
                )
```

以上代码列出大部分主要修改。博主在GitHub上上传了该文件，目前仅是简单做了点修改，没有经过正式的测试，之后可能会进行更多改动，感兴趣的可以star下来，或者自己进一步修改。

> **[传送门](https://github.com/huilansame/HTMLTestRunner_PY3)**

你也自己编写自己的Report Runner，并不很复杂。

将其放在utils目录中，然后我们再次修改test_baidu：

```python
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner


class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    excel = DATA_PATH + '/baidu.xlsx'

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def sub_setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + '\chromedriver.exe')
        self.driver.get(self.URL)

    def sub_tearDown(self):
        self.driver.quit()

    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.driver.find_element(*self.locator_kw).send_keys(d['search'])
                self.driver.find_element(*self.locator_su).click()
                time.sleep(2)
                links = self.driver.find_elements(*self.locator_result)
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()


if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='修改html报告')
        runner.run(TestBaiDu('test_search'))
```

执行后，可以在report目录下看到有 `report.html` 文件，我们已经生成测试报告了。