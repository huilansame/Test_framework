# 怎样从0开始搭建一个测试框架_1

> 这一步我们用到了selenium的基本的知识，以及一些unittest和PyYaml库的内容，有问题的同学可以参考我之前的博客：
> [Python Selenium自动化测试详解](http://blog.csdn.net/column/details/12694.html)
> [Python必会的单元测试框架 —— unittest](http://blog.csdn.net/huilan_same/article/details/52944782)
> [自动化项目配置或用例文件格式推荐--yaml](http://blog.csdn.net/huilan_same/article/details/52625230)

我们先创建一个简单的脚本吧，在test文件夹创建test_baidu.py：

```python
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "http://www.baidu.com"
base_path = os.path.dirname(os.path.abspath(__file__)) + '\..'
driver_path = os.path.abspath(base_path+'\drivers\chromedriver.exe')

locator_kw = (By.ID, 'kw')
locator_su = (By.ID, 'su')
locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

driver = webdriver.Chrome(executable_path=driver_path)
driver.get(URL)
driver.find_element(*locator_kw).send_keys('selenium 灰蓝')
driver.find_element(*locator_su).click()
time.sleep(2)
links = driver.find_elements(*locator_result)
for link in links:
    print(link.text)
driver.quit()
```

脚本打开chrome，输入“selenium 灰蓝”，然后把所有结果中的标题打印出来。

如果想要搜索“Python selenium”，是不是要再创建一个脚本？还是把原来的脚本修改一下？

或者我们可以用unittest来改一下，把两次搜索分别写一个测试方法：

```python
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestBaiDu(unittest.TestCase):
    URL = "http://www.baidu.com"
    base_path = os.path.dirname(os.path.abspath(__file__)) + '\..'
    driver_path = os.path.abspath(base_path+'\drivers\chromedriver.exe')

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        self.driver.find_element(*self.locator_kw).send_keys('selenium 灰蓝')
        self.driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            print(link.text)

    def test_search_1(self):
        self.driver.find_element(*self.locator_kw).send_keys('Python selenium')
        self.driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            print(link.text)


if __name__ == '__main__':
    unittest.main()
```

现在，我们把配置抽出来放到config.yml中：

```yaml
URL: http://www.baidu.com
```

为了读取yaml文件，我们需要一个封装YamlReader类，在utils中创建file_reader.py文件：

```python
import yaml
import os


class YamlReader:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data
```

而且我们需要一个Config类来读取配置，config.py：

```python
"""
读取配置。这里配置文件用的yaml，也可用其他如XML,INI等，需在file_reader中添加相应的Reader进行处理。
"""
import os
from utils.file_reader import YamlReader

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。如果你的结构不同，可自行修改。
# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台，也建议大家多用os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'这样
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)

```

修改test_baidu.py:

```python
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH


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
            print(link.text)

    def test_search_1(self):
        self.driver.find_element(*self.locator_kw).send_keys('Python selenium')
        self.driver.find_element(*self.locator_su).click()
        time.sleep(2)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            print(link.text)


if __name__ == '__main__':
    unittest.main()
```

我们已经把配置分离出来了，虽然现在看起来似乎很麻烦，但是想想如果你有50个用例文件甚至更多，一旦项目URL变了，你还要一个个去修改吗？

> 所有的代码我都放到了GITHUB上[传送](https://github.com/huilansame/Test_framework)，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的[QQ群:455478219](https://jq.qq.com/?_wv=1027&k=4EQQKFg)讨论。