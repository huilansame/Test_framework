# 怎样从0开始搭建一个测试框架_0

**在开始之前，请让我先声明几点：**

1. 请确保你已经掌握了基本的Python语法
2. 如果你要搭建UI框架，请确保你已经掌握了Selenium的基本用法
3. 这个框架主要面向刚刚会写脚本但是不知道该如何走向下一步的同学，欢迎吐槽，但最好带上改进建议


## 思考：我们需要一个什么样的框架

既然要搭一个框架，我们首先得弄明白我们需要一个什么样的框架，这个框架要支持什么功能？

框架主要的作用就是帮助我们编写更加简单而且好维护的用例，让我们把主要精力放在测试用例的设计上，那么我们就需要把所有额外的东西抽象出来作为框架的部分。

那么，额外的东西是什么？

1. 日志以及报告
2. 日志级别、URL、浏览器类型等基本配置
3. 参数化
4. 公共方法

## 搭建框架目录结构

现在我们很容易就把框架的结构搭建好了：

    Test_framework
        |--config（配置文件）
        |--data（数据文件）
        |--drivers（驱动）
        |--log（日志）
        |--report（报告）
        |--test（测试用例）
        |--utils（公共方法）
        |--ReadMe.md（加个说明性的文件，告诉团队成员框架需要的环境以及用法）

也可以参照这篇目录结构，都是类似的：[简单分享一个轻量级自动化测试框架目录结构设计](http://blog.csdn.net/huilan_same/article/details/52319537)

接下来有一些选择题要做了：

## Python 2 or 3? Selenium 2 or 3?

Python 3的使用越来越多，而且3的unittest中带有subTest，能够通过子用例实现参数化。而用2的话需要unittest2或其他的库来实现，所以我们这里选用Python 3。

Selenium 3刚发布正式版不久，一些功能driver还没来得及跟上，尤其是geckodriver，所以选择Selenium 2（注意PY3的话要选择SE2.53.1）。

环境选择其实影响不大，你也可以选择你自己习惯的环境。

## 配置文件

配置文件我们有多种选择：ini、yaml、xml、properties、txt、py等

鉴于我之前写过一篇yaml的博文，我们这里就用yaml吧。

所以我们在config文件夹里创建config.yml文件，在utils里创建一个config.py文件读取配置，内容暂且不管。

## 简单的对之后的内容勾画一下

1. 首先我们要把配置抽出来，用yaml文件放配置。所以我们要在config层添加配置文件config.yml，在utils层添加file_reader.py与config.py来管理。[怎样从0开始搭建一个测试框架_1](http://blog.csdn.net/huilan_same/article/details/76572428)
2. 然后我们将python自带的logging模块封装了一下，从配置文件读取并设置固定的logger。在utils中创建了log.py。[怎样从0开始搭建一个测试框架_2](http://blog.csdn.net/huilan_same/article/details/76572446)
3. 然后封装xlrd模块，读取excel，实现用例的参数化。[怎样从0开始搭建一个测试框架_3](http://blog.csdn.net/huilan_same/article/details/76572466)
4. 然后是生成HTML测试报告，这个博主修改了网上原有的HTMLTestRunner，改为中文并美化，然后修改其支持PY3。你可以直接拿去用。[怎样从0开始搭建一个测试框架_4](http://blog.csdn.net/huilan_same/article/details/76572481)
5. 然后我们给框架添加了发送邮件报告的能力。在utils中添加了mail.py。[怎样从0开始搭建一个测试框架_5](http://blog.csdn.net/huilan_same/article/details/76572761)
6. 然后我们将测试用例用Page-Object思想进行封装，进一步划分test层的子层。[怎样从0开始搭建一个测试框架_6](http://blog.csdn.net/huilan_same/article/details/76572776)
7. 接下来为了接口测试封装client类。在utils中添加了client.py。[怎样从0开始搭建一个测试框架_7](http://blog.csdn.net/huilan_same/article/details/76572788)
8. 然后添加了一个简单的自定义断言，在utils中添加assertion.py，可用同样的方法自行扩展。[怎样从0开始搭建一个测试框架_8](http://blog.csdn.net/huilan_same/article/details/77367275)
9. 接下来我们为了抽取响应结果，用JMESPath封装Extractor，在utils中添加extractor.py。[怎样从0开始搭建一个测试框架_9](http://blog.csdn.net/huilan_same/article/details/77367283)
10. 然后是生成器。为我们自动生成固定类型的测试数据。utils下创建了generator.py。[怎样从0开始搭建一个测试框架_10](http://blog.csdn.net/huilan_same/article/details/77367293)
11. 最后为了一些项目中的支持方法，如加密、签名等，创建支持库support.py。[怎样从0开始搭建一个测试框架_11](http://blog.csdn.net/huilan_same/article/details/77367303)

整个流程下来我们一个简单的框架就像模像样了，在此基础上可继续完善，实际用在项目中也没有什么问题，再简单结合 `Jenkins` 部署起来，定期或每次代码提交后可自动运行测试，直接把测试报告发送到项目成员手中，妥妥的！接下来就跟我一块学习吧。



> 所有的代码我都放到了**[GITHUB上点我传送](https://github.com/huilansame/Test_framework)**，可以自己下载去学习，有什么好的建议或者问题，可以留言或者加我的**[QQ群:455478219，点击加群](https://jq.qq.com/?_wv=1027&k=4EQQKFg)**讨论。


