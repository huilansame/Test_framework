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


if __name__ == '__main__':
    # y = 'E:\Test_framework\config\config.yml'
    # reader = YamlReader(y)
    # print(reader.data)

    e = 'E:/Test_framework/data/baidu.xlsx'
    reader = ExcelReader(e, title_line=True)
    print(reader.data)
