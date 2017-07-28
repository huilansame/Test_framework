# 怎样从0开始搭建一个测试框架_3

> 这一步我们需要用到Python库xlrd

我们已经把配置分离，并添加了log，接下来我们应该尝试着进行数据分离，进行参数化了。

我们修改file_reader.py文件，添加ExcelReader类，实现读取excel内容的功能：

```python
import yaml
import os
from xlrd import open_workbook


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


class SheetTypeError(Exception):
    pass


class ExcelReader:
    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if self._data:
            return self._data
        else:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)
                for col in range(1, s.nrows):
                    self._data.append(dict(zip(title, s.row_values(col))))
                return self._data
            else:
                for col in range(0, s.nrows):
                    self._data.append(s.row_values(col))
            return self._data
```

我们添加title_line参数，用来声明是否在excel表格里有标题行，如果有标题行，返回dict列表，否则返回list列表，如下：

```
# excel表格如下:
# | title1 | title2 |
# | value1 | value2 |
# | value3 | value4 |

# 如果title_line=True
[{"title1": "value1", "title2": "value2"}, {"title1": "value3", "title2": "value4"}]

# 如果title_line=False
[["title1", "title2"], ["value1", "value2"], ["value3", "value4"]]
```

在data目录下创建baidu.xlsx，如下：

```
| search |
| selenium 灰蓝 |
| Python selenium |
```

然后我们再修改我们可怜的小用例：

```python
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config, DRIVER_PATH, DATA_PATH
from utils.log import logger
from utils.file_reader import ExcelReader


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
    unittest.main(verbosity=2)
```

subTest是PY3 unittest里带的功能，PY2中没有，PY2中要想使用，需要用unittest2库。subTest是没有setUp和tearDown的，所以需要自己手动添加并执行。

现在我们就实现了数据分离，之后如果要搜索“张三”、“李四”，只要在excel里添加行就可以了。subTest参数化也帮助我们少写了很多用例方法，不用一遍遍在Case里copy and paste了。



