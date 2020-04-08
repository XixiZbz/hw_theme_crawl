#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 4:56 下午
# @Author  : zbz
# @Site    : 
# @File    : crawl.py
# @Software: PyCharm
import os

import requests
import yaml
project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../"
from encry import encrypt_key
s = requests.Session()

class BaseCrawl(object):
    def __init__(self):
        self.num_count = 10
        self.length = 100
        self.headers = {"versioncode": "100010331",
                        "user-agent": "com.huawei.android.thememanager/10.0.10.331 (Linux; Android 8.0.0; FRD-AL00) RestClient/1.0.12.300",

                        "accept-encoding": "gzip"}

        # chargeFlag 参数决定属于哪个子类 listcode 决定分类方法 begin为部分方法参数,一般为1,length 为返回长度 ,pageId 为获取活动特有参数,以及字体banner所用,banner还有location
        self.list_data = {"sign": "061l10064111CN@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D",
                          "ver": "1.7", "screen": "1920*1080", "deviceId": "869953023104979",
                          "userToken": "028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf",
                          "deviceType": "2", "appId": "3", "cursor": "0", "emuiVersion": "8.0",
                          "deviceModel": "FRD-AL00", "buildNumber": "FRD-AL008.0.0.540(C00)", "resourceType": 1,
                          "listType": 1, "subType": "0", "versionCode": "100010331","length":self.length}
        # 动态壁纸&formatType=-1,liveCharge=true sourceFlag=1 ,获取活动 paperChargeFlag = -1,其余为null.isPay=1获取活动没有,其余有
        self.waterfall_data = "&chargeflag=-1&screen=1920*1080&buildNumber=FRD-AL008.0.0.540(C00)" \
                              "&sign=061l10064111CN@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D" \
                              "&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&deviceId=869953023104979" \
                              "&deviceType=2&versionCode=100010331"
        #
        self.activity_url = "https://servicesupport1.hicloud.com/servicesupport/theme/getModuleList.do?&type=4&language=zh_CN&begin=1&length=30&sort=latestrec"

        self.topic_column_url = "https://servicesupport1.hicloud.com/servicesupport/theme/getModuleList.do?&type=1&language=zh_CN&begin=1&length=30&sort=latestre"

        self.theme_list_url = "https://servicesupport1.hicloud.com/servicesupport/theme/v2/getThemeList.do"

        self.wallpaper_url = "https://servicesupport1.hicloud.com/servicesupport/theme/v2/getStaticWallpaperList.do?"

        self.waterfall_url = "https://servicesupport1.hicloud.com/servicesupport/theme/getMixRecommenGroup.do?"

        self.font_list_url = "https://servicesupport1.hicloud.com/servicesupport/theme/v2/getFontList.do"
class CrawlFeatured(BaseCrawl):
    def fetured_theme_hot_day(self):
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 1
        result = s.post(url=self.theme_list_url,headers=self.headers,json=self.list_data)
        return result
    def fetured_theme_hot_month(self):
        self.list_data["listCode"] = "hottest_month"
        self.list_data["chargeFlag"] = 1
        result = s.post(url=self.theme_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_theme_new(self):
        self.list_data["listCode"] = "latest"
        self.list_data["chargeFlag"] = -1
        result = s.post(url=self.theme_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_theme_free_day(self):
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 0
        result = s.post(url=self.theme_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_theme_free_month(self):
        self.list_data["listCode"] = "hottest_month"
        self.list_data["chargeFlag"] = 0
        result = s.post(url=self.theme_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_dynamic_wallpaper(self):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        self.url = "https://servicesupport1.hicloud.com/servicesupport/theme/getResourceInfo.do?&type=3&language=zh_CN&begin=1&length=120&sort=bistream&categoryId=0&ver=1.6"
        self.waterfall_data = "&chargeflag=-1&formatType=-1&screen=1920*1080&liveCharge=true&buildNumber=FRD-AL008.0.0.540(C00)&sign=061l10064111CN@444CCBE65FED5BAFDB4D3A061A81E29B8978A5105490660C803CA3D567DF08F8&isPay=1&paperChargeFlag=null&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&deviceId=869953023104979&deviceType=2&sourceFlag=&versionCode=100010331"
        result = s.post(url=self.url,headers=self.headers,data=self.waterfall_data)
        return result
    def fetured_hot_font(self):
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 1
        self.list_data["resourceType"] = "4"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_new_font(self):
        self.list_data["listCode"] = "latest"
        self.list_data["chargeFlag"] = -1
        self.list_data["resourceType"] = "4"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_wallpaper_hot(self):
        self.list_data["resourceType"] = "2"
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 1
        result = s.post(url=self.wallpaper_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_wallpaper_new(self):
        self.list_data["resourceType"] = "2"
        self.list_data["listCode"] = "latest"
        self.list_data["chargeFlag"] = -1
        result = s.post(url=self.wallpaper_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_wallpaper_free(self):
        self.list_data["resourceType"] = "2"
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 0
        result = s.post(url=self.wallpaper_url, headers=self.headers, json=self.list_data)
        return result
    def fetured_waterfall(self):
        data = {"sign":"061l10064111CN@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D","begin":1,"length":15,"ver":"1.7","versionCode":"100010331","deviceId":"869953023104979","userToken":"028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf","deviceType":"2","appId":"3","cursor":"11","emuiVersion":"8.0","deviceModel":"FRD-AL00","buildNumber":"FRD-AL008.0.0.540(C00)","mixingListType":"1,11,12,2,41,5","sourceType":"bihottest","screen":"1920*1080"}
        result = s.post(url=self.waterfall_url, headers=self.headers, json=data)
        return result
class CrawlThemne(BaseCrawl):
    def get_theme_column(self):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        url = "https://servicesupport1.hicloud.com/servicesupport/theme/getModuleList.do?&type=1&language=zh_CN&begin=1&length=30&sort=latestre"
        data = "&pageId=10010001&paperChargeFlag=-1&buildNumber=FRD-AL008.0.0.540(C00)&themeVersion=8.0&sign=061l10064111CN@FCEEDB909678E1D8ED3039F48FAAE60FE0E848B9BC833598E72CC5C3353B149A&subType=0,1,2&ver=2.0&packageType=0,1,3&versionCode=100010331"
        result = s.post(url=url,headers=self.headers,data=data)
        return result
    def get_column_data(self,source_id):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        if source_id.isdigit():
            format_url = "https://servicesupport1.hicloud.com/servicesupport/theme/gettheme.do?&type=4&language=zh_CN&" \
                      "begin={}&length=15&sort=hottest&categoryId={}&ver=1.6"
            data = "&themeVersion=8.0&filetype=hwt&chargeflag=-1&supportType=1&phoneType=FRD-AL00&buildNumber=FRD-AL008.0.0.540(C00)&" \
                   "sign=061l10064111CN@444CCBE65FED5BAFDB4D3A061A81E29B8978A5105490660C803CA3D567DF08F8&isoCode=CN&" \
                   "categoryId={}&isPay=1&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&" \
                   "deviceId=869953023104979&deviceType=2&subType=0,1,2&screen=1920*1080&versionCode=100010331".format(
                source_id)
        else:
            format_url = "https://servicesupport1.hicloud.com/servicesupport/theme/gettheme.do?&type=4&language=zh_CN&" \
                         "begin={}&length=12&sort={}&ver=1.6"
            data = "&themeVersion=8.0&filetype=hwt&supportType=1&phoneType=FRD-AL00&buildNumber=FRD-AL008.0.0.540(C00)&" \
                   "sign=061l10064111CN@444CCBE65FED5BAFDB4D3A061A81E29B8978A5105490660C803CA3D567DF08F8&isoCode=CN&" \
                   "isPay=1&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&" \
                   "deviceId=869953023104979&deviceType=2&subType=0&screen=1920*1080&fixNumberFlag=0&versionCode=100010331"
        for num in range(1,self.num_count+1):
            url = format_url.format(num,source_id)
            result = s.post(url=url, headers=self.headers, data=data)
            yield result
class CrawlFont(BaseCrawl):
    def font_banner(self):
        url = "https://servicesupport1.hicloud.com/servicesupport/theme/v2/getAdvertisementContent.do?"
        data = {"sign":"061l10064111CN@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D","userToken":"028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf","deviceId":"869953023104979","deviceType":"2","begin":1,"length":40,"emuiVersion":"8.0","pageId":"10010004","location":"1","cursor":"0","ver":"2.0","versionCode":"100010331"}
        result = s.post(url=url,headers=self.headers,json=data)
        return result
    def font_column_hot_day(self):
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 1
        self.list_data["resourceType"] = "4"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_column_hot_month(self):
        self.list_data["listCode"] = "hottest_month"
        self.list_data["chargeFlag"] = 1
        self.list_data["resourceType"] = "4"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_column_new(self):
        self.list_data["listCode"] = "latest"
        self.list_data["chargeFlag"] = -1
        self.list_data["resourceType"] = "4"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_new(self):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        for num in range(1,self.num_count+1):
            url = "https://servicesupport1.hicloud.com/servicesupport/theme/getResourceInfo.do?&type=2&language=zh_CN&begin={}" \
                  "&length=10&sort=hottest&categoryId=820022759&ver=1.6".format(num)
            data = "&fontversion=3.0&chargeflag=-1&packageType=0,1,3&buildNumber=FRD-AL008.0.0.540(C00)&sign=061l10064111CN" \
                   "@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D&isPay=1" \
                   "&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&deviceId=869953023104979" \
                   "&deviceType=2&versionCode=100010331"
            result = s.post(url=url, headers=self.headers, data=data)
            yield result
    def font_shining_font_day(self):
        self.list_data["listCode"] = "hottest"
        self.list_data["chargeFlag"] = 1
        self.list_data["resourceType"] = "4"
        self.list_data["subType"] = "1,3"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_shining_font_month(self):
        self.list_data["listCode"] = "hottest_month"
        self.list_data["chargeFlag"] = 1
        self.list_data["resourceType"] = "4"
        self.list_data["subType"] = "1,3"
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_shining_font_new(self):
        self.list_data["listCode"] = "latest"
        self.list_data["chargeFlag"] = -1
        self.list_data["resourceType"] = "4"
        self.list_data["subType"] = "1,3"
        self.list_data = {"sign":"061l10064111CN@29D383AAA1F3D18259707B190B3850B43B3429B805B91059E341DA58A0F2B96D","length":15,"ver":"1.7","versionCode":"100010331","deviceId":"869953023104979","userToken":"028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf","deviceType":"2","cursor":"0","emuiVersion":"8.0","deviceModel":"FRD-AL00","buildNumber":"FRD-AL008.0.0.540(C00)","resourceType":"4","listType":1,"listCode":"hottest","chargeFlag":1,"subType":"1,3"}
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    # 解析出名字和id
    def font_get_font_album(self):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        url = "https://servicesupport1.hicloud.com/servicesupport/theme/getModuleList.do?&type=4&language=zh_CN&begin=1&" \
              "length=30&sort=latestrec"
        data = "&pageId=10010004&paperChargeFlag=-1&buildNumber=FRD-AL008.0.0.540(C00)&themeVersion=8.0&sign=061l10064111CN@3E3C4C6B7F7A2A50E3B6B01F5A1EF8497E2B7F76DDBD2B79F87CCFA32127A9D9&subType=0,1,2&ver=2.0&packageType=0,1,3&versionCode=100010331"
        result = s.post(url=url, headers=self.headers, data=data)

        return result
    def font_hit_album(self):
        self.list_data["resourceType"] = "4"
        self.list_data["listCode"] = "bihottest"
        self.list_data["chargeFlag"] = 1
        self.list_data["subType"] = "0，1，3"
        self.list_data["fixNumberFlag"] = 0
        result = s.post(url=self.font_list_url, headers=self.headers, json=self.list_data)
        return result
    def font_get_album_info(self,category_id):
        self.headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        for num in range(1,self.num_count+1):
            url= "https://servicesupport1.hicloud.com/servicesupport/theme/getResourceInfo.do?&type=2&language=zh_CN&" \
                 "begin={}&length=10&sort=hottest&categoryId={}&ver=1.6".format(num,category_id)
            data ="&fontversion=3.0&chargeflag=-1&packageType=0,1,3&buildNumber=FRD-AL008.0.0.540(C00)&sign=061l10064111CN@" \
                  "FCEEDB909678E1D8ED3039F48FAAE60FE0E848B9BC833598E72CC5C3353B149A&isPay=1&userToken=028500860003392476417e6d404e7cd8a8ffcf997f393e67439e90c29094b4d0b5d5b4e9cdd142e6cebf&" \
                  "deviceId=869953023104979&deviceType=2&versionCode=100010331"
            result = s.post(url=url, headers=self.headers, data=data)
            num +=1
            yield result

class VivoCrawlBase:
    def __init__(self):
        self.common_param_str = ""
        with open("{}param_vivo.yaml".format(project_path), 'r') as f:
            res = yaml.load(f,Loader=yaml.FullLoader)
        res_common = res['common']
        self.common_param_str = '&'.join("{}={}".format(param,res_common[param]) for param in res_common)

    def get_paramm(self,param_list):
        for key in param_list:
             self.common_param_str += "&{}={}".format(key,param_list[key])
        return self.common_param_str
    def get_response(self,request_method,param_str):
        request_url = self.url +param_str
        for x in range(4):
            try:
                if request_method == "get":
                    res = requests.get(request_url)
                elif request_method =='post':
                    res = requests.post(requests)
                else:
                    res = False
                break
            except:
                continue
        else:
            raise IOError("network fail")
        return res
    def get_param_p(self,encode_str):
        param_p = encrypt_key(encode_str)
        return param_p

class VivoCrawlClassifyTheme(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api18.do?"
class VivoCrawlClassifyThemeEach(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api8.do?"
class VivoCrawlPage(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api/page/query.do?"
class VivoCrawlResource(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api/resource/list.do?"

class VivoCrawllist(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api/resource/list.do?"

class VivoCrawlEach(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api11.do?"
        with open("{}param_vivo.yaml".format(project_path), 'r') as f:
            res = yaml.load(f,Loader=yaml.FullLoader)
        res_common = res['common_each']
        self.common_param_str = '&'.join("{}={}".format(param,res_common[param]) for param in res_common)
class VivoCrawlGetTheme(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api2.do?"

class VivoCrawlGetEachTheme(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api19.do?"

class VivoCrawlThemeFuck(VivoCrawlBase):
    def __init__(self):
        super().__init__()
        self.url = "https://theme.vivo.com.cn/api10.do?"


if __name__ == '__main__':

    v = VivoCrawlEach()
    # page test
    # request_method="get"
    # unique_num = 99
    # unique_param = {"themetype":"{}".format(unique_num),"tt":"{}".format(unique_num),"category":"{}".format(unique_num),"showClock":"false"}
    # param_str = v.get_paramm(unique_param)
    # res = v.get_response(request_method,param_str)
    # print(res.text)

    # source test
    # request_method = "get"
    # param_p_str = {"category":"4","componentType":"11","page":"102","pageIndex":"1","setId":"1992"}
    # p = v.get_param_p(param_p_str.__str__())
    # unique_param = {"showClock": "false","p":p}
    # param_str = v.get_paramm(unique_param)
    # res = v.get_response(request_method, param_str)
    # print(res.text)

    #list test
    # request_method = "get"
    # param_p_str = '{"category":"4","componentType":"11","page":"103","pageIndex":"1","setId":"2451"}'
    # p = v.get_param_p(param_p_str)
    # print(p)
    # unique_param = {"showClock": "false","p":p}
    # param_str = v.get_paramm(unique_param)
    # res = v.get_response(request_method, param_str)
    # print(res.text)


    #each test
    request_method = "get"
    param_p_str = '{"o":"","resId":"100026873","tt":"1"}'
    p = v.get_param_p(param_p_str)
    unique_param = {"p": p,"themetype":"1","resId":"100026872"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    print(res.text)