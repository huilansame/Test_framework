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
    def __init__(self, yaml):
        if os.path.exists(yaml):
            self.yaml = yaml
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        if self._data:
            return self._data
        else:
            with open(self.yaml, 'rb') as f:
                return list(yaml.safe_load_all(f))
```

而且我们需要一个Config类来读取配置，config.py：

```python
import os
from utils.file_reader import YamlReader

BASE_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '\..')
CONFIG_FILE = BASE_PATH + '\config\config.yml'
DATA_PATH = BASE_PATH + '\data\\'
DRIVER_PATH = BASE_PATH + '\drivers\\'
LOG_PATH = BASE_PATH + '\log\\'
REPORT_PATH = BASE_PATH + '\\report\\'


class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlReader(config).data

    def get(self, element, index=0):
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