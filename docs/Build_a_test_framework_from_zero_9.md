# 怎样从0开始搭建一个测试框架_9

> 对接口测试来说，很多时候，我们的用例不是一次请求就OK了的，而是多个请求复合的，我们第二个请求可能会用到第一个请求返回值中的数据，这就要我们再次进行封装，做一个抽取器，从结果中抽取部分信息。
> 这里我们会用到JMESPath库，这是一个让我们通过类似于xpath或点分法来定位json中的节点的库

别忘了我们先在ReadMe.md中添加上依赖的库。

我们在utils中创建extractor.py文件，实现对响应中数据的抽取

```python
"""抽取器，从响应结果中抽取部分数据"""

import json
import jmespath


class JMESPathExtractor(object):
    """
    用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))


if __name__ == '__main__':
    from utils.client import HTTPClient
    res = HTTPClient(url='http://wthrcdn.etouch.cn/weather_mini?citykey=101010100').send()
    print(res.text)
    # {"data": {
    #     "yesterday": {"date": "17日星期四", "high": "高温 31℃", "fx": "东南风", "low": "低温 22℃", "fl": "<![CDATA[<3级]]>",
    #                   "type": "多云"},
    #     "city": "北京",
    #     "aqi": "91",
    #     "forecast": [
    #         {"date": "18日星期五", "high": "高温 28℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 22℃", "fengxiang": "东北风",
    #          "type": "多云"},
    #         {"date": "19日星期六", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 22℃", "fengxiang": "东风",
    #          "type": "雷阵雨"},
    #         {"date": "20日星期天", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 23℃", "fengxiang": "东南风",
    #          "type": "阴"},
    #         {"date": "21日星期一", "high": "高温 30℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 24℃", "fengxiang": "西南风",
    #          "type": "晴"},
    #         {"date": "22日星期二", "high": "高温 29℃", "fengli": "<![CDATA[<3级]]>", "low": "低温 24℃", "fengxiang": "北风",
    #          "type": "雷阵雨"}
    #     ],
    #     "ganmao": "各项气象条件适宜，无明显降温过程，发生感冒机率较低。", "wendu": "25"
    #  },
    # "status": 1000,
    # "desc": "OK"}

    j = JMESPathExtractor()
    j_1 = j.extract(query='data.forecast[1].date', body=res.text)
    j_2 = j.extract(query='data.ganmao', body=res.text)
    print(j_1, j_2)
    # 结果：
    # 19日星期六 各项气象条件适宜，无明显降温过程，发生感冒机率较低。
```

这样我们就完成了对JSON格式的抽取器，如果返回结果是JSON串，我们可以通过这个抽取器找到我们想要的数据，再进行下一步的操作，或者用来做断言。

这里仅仅完成了对JSON格式响应的抽取，之后读者可以自己添加XML格式、普通字符串格式、Header的抽取器，逐步进行完善。

> 所有的代码我都放到了GITHUB上[传送](https://github.com/huilansame/Test_framework)，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的[QQ群:455478219](https://jq.qq.com/?_wv=1027&k=4EQQKFg)讨论。
