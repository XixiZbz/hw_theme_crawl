#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/9 3:10 下午
# @Author  : zbz
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import json

import requests

import yaml

# 抓取
# s = requests.Session()
# headers = {}
# headers["versioncode"] = "100010331"
# headers["user-agent"] = "com.huawei.android.thememanager/10.0.10.331 (Linux; Android 8.0.0; FRD-AL00) RestClient/1.0.12.300"
# # headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
# # headers["x-clienttraceid"] = "506Z71ATT30I33Z519J457TV0VZL032R"
# headers["accept-encoding"] = "gzip"
# url = "https://servicesupport1.hicloud.com/servicesupport/theme/v2/getThemeList.do"
# data = {"sign":"061l10064111CN@5D0ADE527E85BEAB408A182515AF1DE42032832B17B55E9904959709249FA482","length":10,"ver":"1.7","screen":"1920*1080","appId":"3","cursor":"0","emuiVersion":"8.0","deviceModel":"FRD-AL00","buildNumber":"FRD-AL008.0.0.540(C00)","resourceType":1,"listType":1,"listCode":"hottest","chargeFlag":1,"subType":"0","versionCode":"100010331"}
# res = s.post(url=url,headers=headers,json=data)
# print(res.text)


# 解析
with open("./test",'r+') as f:
    content = f.read()
_dict = json.loads(content)
a = _dict["list"]
print(len(a))

