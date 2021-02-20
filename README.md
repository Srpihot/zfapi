# ZF-API 正方教务系统API

##### 正方教务系统信息api，方便开发者二次开发。本着不想重复造轮子的心态，搜索了市面上开源的教务系统爬虫，发现对于本校的教务系统不适用，故参考了部分的正方教务系统的爬虫，尽可能的解决各方面的bug，因此创建此项目。如果有朋友也需要欢迎提issues，尽量解决。

> PS:因为之前写过老版本正方教务系统的爬虫，没想刚写完学校升级教务系统了。后期会把旧版的也改写成api，方便部分没升级的同学使用。也推荐各位大佬推荐其他常用的教务系统，希望打造成一个全面的教务系统api or sdk。

##### 后面会添加选课与抢课功能，与微信公众号小程序配合等等，还有最最最重要的一键评价。

### 原理：

##### 爬虫方面登陆后使用cookies带入，然后抓包分析参数即可，至于登陆方面的加密，百度搜索有比较详细的讲解。

### 已实现功能：

* [x] 支持新版正方教务、旧版正方教务还未支持

* [x] 自动登陆、cookies获取
* [x] 获取个人信息
* [x] 获取学校通知
* [x] 调课、改课消息
* [x] 获取个人成绩
* [x] 获取课程表
* [x] 获取考试信息
* [x] 可返回原始正方数据json格式

### 如何使用：

+ 使用pip命令安装`pip install zfapi`

+ 或者手动安装

  + ```bash
    tar -zxvf 包名.tar.gz
    cd 包名
    python setup.py build
    python setup.py install
    ```

### 小试牛刀

运行如下代码：

```python
from zfapi import *

base_url = 'http://xxxx/'

l = Login(base_url=base_url)
l.login('账号', '密码')
cookies = l.cookies
srpihot = GetInfo(base_url=base_url, cookies=cookies)
print(srpihot.get_information())
```

### 详细API介绍

**详细查看**[这些例子](https://github.com/Srpihot/zfapi/tree/master/examples)

### 感谢以下项目：

+ [NeroAsmarr/新版正方教务教务系统API](https://github.com/NeroAsmarr/zfnew)
+ [dairoot/正方系统 Python SDK](https://github.com/dairoot/school-api)