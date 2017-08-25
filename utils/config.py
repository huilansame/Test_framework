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
        """
        yaml是可以通过'---'分节的。所以读取之后yaml是一个大list，第一项
        """
        return self.config[index].get(element)


if __name__ == '__main__':
    c = Config()
    print(c.get('URL'))