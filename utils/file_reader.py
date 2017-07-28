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


class ExcelReader:
    def __init__(self, excel):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('文件不存在！')

    @property
    def data(self):
        pass



if __name__ == '__main__':
    # y = 'E:\Test_framework\config\config.yml'
    # reader = YamlReader(y)
    # print(reader.data)

    e = 'E:/Test_framework/data/baidu.xlsx'
    reader = ExcelReader(e)
    print(reader.data)
