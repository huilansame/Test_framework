# 怎样从0开始搭建一个测试框架_2

> 这部分需要预先了解Python的内置库logging

接下来我们为我们的框架加上log，在utils中创建一个log.py文件，Python有很方便的logging库，我们对其进行简单的封装，使框架可以很简单地打印日志（输出到控制台以及日志文件）。

```python
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.config import LOG_PATH


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = 'test.log'
        self.backup_count = 5
        # 日志输出级别
        self.console_output_level = 'WARNING'
        self.file_output_level = 'DEBUG'
        # 日志输出格式
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=LOG_PATH + self.log_file_name,
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()
```

然后修改test_baidu.py，将输出改到log中：

```python
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH
from utils.log import logger


class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + '\chromedriver.exe')
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        self.driver.find_element(*self.locator_kw).send_keys('selenium 灰蓝')
        self.driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            logger.info(link.text)

    def test_search_1(self):
        self.driver.find_element(*self.locator_kw).send_keys('Python selenium')
        self.driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            logger.info(link.text)


if __name__ == '__main__':
    unittest.main()
```

执行后，可以看到在log文件夹下创建了test.log文件，打印的信息都输出到了文件中：

```log
2017-07-26 16:00:59,457 - framework - INFO - Python selenium —— 一定要会用selenium的等待,三种..._CSDN博客
2017-07-26 16:00:59,487 - framework - INFO - Selenium - 灰蓝 - CSDN博客
2017-07-26 16:00:59,515 - framework - INFO - ...教你在Windows上搭建Python+Selenium环境 - 灰蓝 - CSDN博客...
2017-07-26 16:00:59,546 - framework - INFO - Python selenium —— 父子、兄弟、相邻节点定位方式详..._CSDN博客
2017-07-26 16:00:59,572 - framework - INFO - Selenium - 灰蓝 - CSDN博客
2017-07-26 16:00:59,595 - framework - INFO - selenium之 时间日期控件的处理 - 灰蓝 - CSDN博客
...
```

我们还可以把log的设置放到config中，修改config.yml，将几项重要的设置都写进去：

```yaml
URL: http://www.baidu.com
log:
    file_name: test.log
    backup: 5
    console_level: WARNING
    file_level: DEBUG
    pattern: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

同时修改log.py，读取config，如果config中有，则采用文件中的设置，否则，采用默认设置

```python
"""
日志类。通过读取配置文件，定义日志级别、日志文件名、日志格式等。
一般直接把logger import进去
from utils.log import logger
logger.info('test log')
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        self.log_file_name = c.get('file_name') if c and c.get('file_name') else 'test.log'  # 日志文件
        self.backup_count = c.get('backup') if c and c.get('backup') else 5  # 保留的日志数量
        # 日志输出级别
        self.console_output_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_output_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        # 日志输出格式
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。
        """
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

logger = Logger().get_logger()

```

现在，我们已经可以很方便地输出日志了，并且可以通过配置config.yml来修改log的设置。

> 所有的代码我都放到了GITHUB上[传送](https://github.com/huilansame/Test_framework)，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的[QQ群:455478219](https://jq.qq.com/?_wv=1027&k=4EQQKFg)讨论。
