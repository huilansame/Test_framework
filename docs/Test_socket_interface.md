# 测试socket接口

> 接口测试时，除了常见的http接口，还有一种比较多见，就是socket接口，今天讲解下怎么用Python自带的socket库进行socket接口测试。

我们就用之前搭建的测试框架来实现。具体可见 [从零搭建自动化测试框架系列](http://blog.csdn.net/column/details/16677.html)

1. socket接口

`socket` 又叫 `套接字`，可以理解为是一个应用程序的地址，是实现网络通信的关键。我们可以通过IP找到一台主机，可以通过主机的端口找到该主机上的某个应用程序。

这样，就可以通过socket进行两个应用程序之间的通信。具体实现就是在一端实现一个一直在监听的server，另一端向其发送请求，并获取响应。server对不同的请求进行不同的处理并返回，这就是socket接口。

下面我们就实现一个socket的接口并对其进行测试。

2. 实现一个socket server接口

在test下创建mock文件夹，并在其中创建mock_socket_server.py文件：

```python
"""
socket server 的mock。
两个接口，add和sub
接收：
{
    "action": "add",
    "params": {"a": 1, "b": 2}
}
返回：
{
    "action": "add",
    "result": 3
}
"""
import socket
import json


def add(a, b):
    return a + b


ip_port = ('127.0.0.1', 8080)
server = socket.socket()
server.bind(ip_port)
server.listen(5)

while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    try:
        ddata = json.loads(data)
        action = ddata.get('action')
        params = ddata.get('params')
        if action == 'add':
            res = add(**params)
            conn.send(b'{"action": "add", "result": %d}' % res)
        else:
            conn.send(b'{"code":-2, "message":"Wrong Action"}')
    except (AttributeError, ValueError):
        conn.send(b'{"code":-1, "message":"Data Error"}')
    finally:
        conn.close()
```

我们就实现了一个简单的socket server，有一个接口add。开发给你的接口文档可能是这样的：

> 接口类型： socket
> 接口地址： 127.0.0.1
> 端口： 8080
> 接口名称： 加法
> action name: add
> 入参：
> | 名称 | 类型 | 是否必须 |
> | :-: | :-: | :-: |
> | a | int | 是 |
> | b | int | 是 |
> 出参：
> | 名称 | 类型 | 含义 |
> | :-: | :-:| :-: |
> | result | int | 结果 |
> 入参示例：
> ```
{
    "action": "add",
    "params": {"a": 1, "b": 2}
}
```
> 出参示例：
> ```
{
    "action": "add",
    "result": 3
}
```
> error code:
> | code | message |
> | :-: | :-: |
> | -1 | Data Error |
> | -2 | Wrong Action |

拿到接口文档，接下来我们该怎么进行测试呢？

首先我们需要一个通用的client类，把socket接口测试通用的方法封装起来，免得每次都得写一堆。在client.py中添加TCPClient

```python
class TCPClient(object):
    """用于测试socket请求"""
    def __init__(self, domain, port, timeout=30, max_receive=102400):
        self.domain = domain
        self.port = port
        self.connected = 0  # 连接后置为1
        self.max_receive = max_receive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)

    def connect(self):
        """连接指定IP、端口"""
        if not self.connected:
            try:
                self._sock.connect((self.domain, self.port))
            except socket.error as e:
                logger.exception(e)
            else:
                self.connected = 1
                logger.debug('TCPClient connect to {0}:{1} success.'.format(self.domain, self.port))

    def send(self, data, dtype='str', suffix=''):
        """向服务器端发送send_string，并返回信息，若报错，则返回None"""
        if dtype == 'json':
            send_string = json.dumps(data) + suffix
        else:
            send_string = data + suffix
        self.connect()
        if self.connected:
            try:
                self._sock.send(send_string.encode())
                logger.debug('TCPClient Send {0}'.format(send_string))
            except socket.error as e:
                logger.exception(e)

            try:
                rec = self._sock.recv(self.max_receive).decode()
                if suffix:
                    rec = rec[:-len(suffix)]
                logger.debug('TCPClient received {0}'.format(rec))
                return rec
            except socket.error as e:
                logger.exception(e)

    def close(self):
        """关闭连接"""
        if self.connected:
            self._sock.close()
            logger.debug('TCPClient closed.')
````

然后在config.yml中添加socket的接口的基本配置：

```yaml
ip: 127.0.0.1
port: 8080
```

然后在interface中创建我们的测试test_socket.py

```python
import unittest
from utils.client import TCPClient
from utils.config import Config
from utils.extractor import JMESPathExtractor

je = JMESPathExtractor()


class TestAdd(unittest.TestCase):

    def setUp(self):
        c = Config()
        ip = c.get('ip')
        port = c.get('port')
        self.client = TCPClient(ip, port)

    def tearDown(self):
        self.client.close()

    def test_add(self):
        data = {
            'action': 'add',
            'params': {'a': 1, 'b': 2}
        }
        res = self.client.send(data, dtype='json')
        self.assertEqual(je.extract('result', res), 3)
        self.assertEqual(je.extract('action', res), 'add')

    def test_wrong_action(self):
        data = {
            'action': 'sub',
            'params': {'a': 1, 'b': 2}
        }
        res = self.client.send(data, dtype='json')
        self.assertEqual(je.extract('code', res), -2)
        self.assertEqual(je.extract('message', res), 'Wrong Action')

    def test_wrong_data(self):
        data = 'xxxxx'
        res = self.client.send(data)
        self.assertEqual(je.extract('code', res), -1)
        self.assertEqual(je.extract('message', res), 'Data Error')


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

简单的测试用例完成了，执行下（先把mock server跑起来哟）：

```
test_add (__main__.TestAdd) ... ok
test_wrong_action (__main__.TestAdd) ... ok
test_wrong_data (__main__.TestAdd) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.009s

OK
```

当然，接口不可能这么简单，用例也不可能就这几个，这里只是简单举个栗子，会应用了，再复杂的socket接口都是一个样子。

这里我们用了自己mock的server，当开发真正的接口通了之后，改改config.yml中的ip和port，就可以直接执行测试了。