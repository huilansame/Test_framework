# 怎样从0开始搭建一个测试框架_11

> 框架到这里已经很不错了，后面就需要各位自己去完善了。比如有时候请求需要加密、签名，可以在utils中创建一个encrypt.py，还有一些支持方法，可以在utils中建个support.py放进去。

在utils中创建一个support.py文件，里面可以放需要的一些支持方法，我们示例一个加密和签名的方法：

```python
"""一些支持方法，比如加密"""
import hashlib
from utils.log import logger


class EncryptError(Exception):
    pass


def sign(sign_dict, private_key=None, encrypt_way='MD5'):
    """传入待签名的字典，返回签名后字符串
    1.字典排序
    2.拼接，用&连接，最后拼接上私钥
    3.MD5加密"""
    dict_keys = sign_dict.keys()
    dict_keys.sort()

    string = ''
    for key in dict_keys:
        if sign_dict[key] is None:
            pass
        else:
            string += '{0}={1}&'.format(key, sign_dict[key])
    string = string[0:len(string) - 1]
    string = string.replace(' ', '')

    return encrypt(string, salt=private_key, encrypt_way=encrypt_way)


def encrypt(string, salt='', encrypt_way='MD5'):
    u"""根据输入的string与加密盐，按照encrypt方式进行加密，并返回加密后的字符串"""
    string += salt
    if encrypt_way.upper() == 'MD5':
        hash_string = hashlib.md5()
    elif encrypt_way.upper() == 'SHA1':
        hash_string = hashlib.sha1()
    else:
        logger.exception(EncryptError('请输入正确的加密方式，目前仅支持 MD5 或 SHA1'))
        return False

    hash_string.update(string.encode())
    return hash_string.hexdigest()

if __name__ == '__main__':
    print(encrypt('100000307111111'))
```

根据你实际情况的不同，在其中添加其他支持方法。

> 就写这么多了，你可以根据这个思路补充扩充，来实现你自己的测试框架，也可以自己调整框架的分层与结构，框架的目的是为了简化我们用例编写和维护的工作量，也没必要把框架搞的太过复杂。
> 所有的代码我都放到了GITHUB上[传送](https://github.com/huilansame/Test_framework)，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的[QQ群:455478219](https://jq.qq.com/?_wv=1027&k=4EQQKFg)讨论。
