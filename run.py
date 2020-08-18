#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 11:39 下午
# @Author  : zbz
# @Site    : 
# @File    : run.py
# @Software: PyCharm


from core.format_txt import ToTxt
from core.crawl import *
from core.parsing import *

to_txt = ToTxt("huawei")
to_txt.open_or_new()
to_txt = ToTxt("Vivo")
to_txt.open_or_new()
request_method = "get"


def type_in(categories, res):
    p = ParsingList(res.text)
    info = p.get_info()
    for j in info:
        j["categories"] = categories
        j["belong"] = " "
        to_txt.format_content(j)


def type_in_theme_column():
    c = CrawlThemne()
    result = c.get_theme_column()
    p = ParsingColumn(result.text)
    a = p.mix_name_source_id()
    print(a)
    for x in a:
        name, id = x.split("|")
        if id:
            d = c.get_column_data(id)
        else:
            continue
        for i in d:
            h = ParsingList(i.text)
            info = h.get_info()
            for j in info:
                j["categories"] = "主题-专栏"
                j["belong"] = name
                to_txt.format_content(j)


def type_in_font_column():
    c = CrawlFont()
    result = c.font_get_font_album()
    p = ParsingColumn(result.text)
    a = p.mix_name_source_id()
    print(a)
    for x in a:
        name, id = x.split("|")
        if id:
            d = c.font_get_album_info(id)
        else:
            continue
        for i in d:
            h = ParsingList(i.text)
            info = h.get_info()
            for j in info:
                j["categories"] = "字体-专栏"
                j["belong"] = name
                to_txt.format_content(j)


def theme_to_each(category, content_id, belong):
    unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category), "id": content_id, "viewid": "-100",
                    "cfrom": "404"}
    v = VivoCrawlGetTheme()
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    for x in json.loads(res.text)['data']['views']:
        content_id = x['contentId']
        if content_id:
            pass
        else:
            continue
        v = VivoCrawlGetEachTheme()
        p_encode_str = '{{"isBanner": "1", "o": "", "pageSize": "30", "setId": {}, "startIndex": "0", "tt": {}}}'.format(
            content_id, category)
        p = v.get_param_p(p_encode_str)
        unique_param = {"p": p}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        res_ids = json.loads(res.text)['resList']
        for each in res_ids:
            res_id = each['resId']
            category = each['category']
            p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
            v = VivoCrawlEach()
            p = v.get_param_p(p_encode_str)
            unique_param = {"p": p, "themetype": category, "resId": res_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response(request_method, param_str)
            p = ParsingVivoItem(res.text)
            result = p.get_info(belong, category)
            print(result)


def get_theme_data(each):
    title = each['title']
    description = each["description"]
    category = each["category"]
    content_destination = each.get("contentDestination", "")
    if content_destination and category != -1:
        id = content_destination
        unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category), "id": id, "viewid": "-100",
                        "cfrom": "404"}
        v = VivoCrawlGetTheme()
        param_str = v.get_paramm(unique_param)
        res = v.get_response("get", param_str)
        for x in json.loads(res.text)['data']['views']:
            title = x['title']
            print(title)
            # 排除推荐主题
            content_id = x['contentId']
            contentType = x['contentType']
            # 推荐主题字体中 6个主题
            if contentType == 0:
                v = VivoCrawllist()
                param_p_str = '{{"category":"{}","componentType":"11","page":"103","pageIndex":"1","setId":"{}"}}'.format(
                    category, content_id)
                p = v.get_param_p(param_p_str)
                unique_param = {"showClock": "false", "p": p}
                param_str = v.get_paramm(unique_param)
                res = v.get_response("get", param_str)
                b = json.loads(res.text)['data']["bannerList"]
                for i in b:
                    title = i['title']
                    print(title)
                    category = i['category']
                    content_id = i['contentId']
                    theme_to_each(category, content_id, "中部banner")
            else:
                pass
            if contentType == -1:
                for i in x['list']:
                    content_id = i['contentId']
                    theme_to_each(category, content_id, "小编精选")
            else:
                theme_to_each(category, content_id, "顶部banner")
            if content_id:
                pass
            else:
                continue


def get_recommond_data_fuck(each):
    print(each)
    category = each["category"]
    content_destination = each.get("contentDestination", "")
    if content_destination and category != -1:
        id = content_destination
        unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category)}
        v = VivoCrawlClassifyTheme()
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        print(res.text)
        for x in json.loads(res.text)['data']['views']:
            content_id = x['contentId']
            if content_id:
                pass
            else:
                continue
            v = VivoCrawlThemeFuck()
            p_encode_str = '{{"isBanner": "1", "o": "", "pageSize": "30", "setId": {}, "startIndex": "0", "tt": {}}}'.format(
                content_id, category)
            p = v.get_param_p(p_encode_str)
            unique_param = {"p": p}
            param_str = v.get_paramm(unique_param)
            res = v.get_response(request_method, param_str)
            res_ids = json.loads(res.text)['resList']
            for each in res_ids:
                res_id = each['resId']
                category = each['category']
                p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                v = VivoCrawlEach()
                p = v.get_param_p(p_encode_str)
                unique_param = {"p": p, "themetype": category, "resId": res_id}
                param_str = v.get_paramm(unique_param)
                res = v.get_response(request_method, param_str)
                p = ParsingVivoItem(res.text)
                result = p.get_info()
                print(result)


def get_recommond_data(each, belong):
    pre_belong = belong
    category = each["category"]
    content_destination = each.get("contentDestination", "")
    if content_destination and category != -1:
        id = content_destination
        unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category), "id": id, "viewid": "-100",
                        "cfrom": "404"}
        v = VivoCrawlGetTheme()
        param_str = v.get_paramm(unique_param)
        res = v.get_response("get", param_str)
        try:
            d =json.loads(res.text)['data']['views']
        except Exception as why:
            print(why)
            return
        for x in d:
            title = x['title']
            content_id = x['contentId']
            belong = pre_belong + "_" + title
            print(belong)
            if content_id:
                pass
            else:
                continue
            v = VivoCrawlGetEachTheme()
            p_encode_str = '{{"isBanner":"1","o":"","pageSize":"100","setId":{},"startIndex":"0","tt":{}}}'.format(
                content_id, category)
            p = v.get_param_p(p_encode_str)
            unique_param = {"p": p}
            param_str = v.get_paramm(unique_param)
            res = v.get_response("get", param_str)
            res_ids = json.loads(res.text)['resList']
            for each in res_ids:
                res_id = each['resId']
                category = each['category']
                p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                v = VivoCrawlEach()
                p = v.get_param_p(p_encode_str)
                unique_param = {"p": p, "themetype": category, "resId": res_id}
                param_str = v.get_paramm(unique_param)
                res = v.get_response("get", param_str)
                p = ParsingVivoItem(res.text)
                result = p.get_info(belong=belong, categories=category)
                print(result)


def run():
    # 精选
    c = CrawlFeatured()
    res = c.fetured_dynamic_wallpaper()
    categories = "动态壁纸"
    type_in(categories, res)

    c = CrawlFeatured()
    res = c.fetured_hot_font()
    categories = "精选-热门字体"
    type_in(categories, res)

    c = CrawlFeatured()
    res = c.fetured_new_font()
    categories = "精选-新字体"
    type_in(categories, res)

    c = CrawlFeatured()
    res = c.fetured_theme_new()
    categories = "精选-主题新品榜"
    type_in(categories, res)
    res = c.fetured_theme_free_day()
    categories = "精选-主题免费榜-日"
    type_in(categories, res)
    res = c.fetured_theme_free_month()
    categories = "精选-主题免费榜-月"
    type_in(categories, res)
    res = c.fetured_theme_hot_day()
    categories = "精选-主题热门榜-日"
    type_in(categories, res)
    res = c.fetured_theme_hot_month()
    categories = "精选-主题热门榜-月"
    type_in(categories, res)
    res = c.fetured_wallpaper_new()
    categories = "精选-精选壁纸-新品榜"
    type_in(categories, res)
    res = c.fetured_wallpaper_hot()
    categories = "精选-精选壁纸-热门榜"
    type_in(categories, res)
    res = c.fetured_waterfall()
    categories = "精选-瀑布流"
    type_in(categories, res)

    # 主题
    type_in_theme_column()

    # 字体
    c = CrawlFont()
    res = c.font_column_hot_month()
    categories = "字体-排行-热门-月榜"
    type_in(categories, res)
    res = c.font_column_new()
    categories = "字体-排行-新品"
    type_in(categories, res)
    res = c.font_column_hot_day()
    categories = "字体-排行-热门-日榜"
    type_in(categories, res)
    res = c.font_shining_font_day()
    categories = "字体-炫动字体-热销-日榜"
    type_in(categories, res)
    res = c.font_shining_font_month()
    categories = "字体-炫动字体-热销-月榜"
    type_in(categories, res)
    type_in_font_column()


def run_vivo():
    from core.crawl import VivoCrawlBase, VivoCrawlEach, VivoCrawllist, VivoCrawlPage, VivoCrawlResource
    # banner
    v = VivoCrawlPage()
    request_method = "get"
    unique_num = 99
    unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                    "category": "{}".format(unique_num), "showClock": "false"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)

    # 首页bannner
    for x in json.loads(res.text)['data']['compList'][0:1]:
        pre_belong = "精选banner"
        data = x.get('list', 0)
        if not data:
            continue

        for each in data:
            belong = pre_belong + "_" + each["title"]
            get_recommond_data(each, belong)

    # 精选主题,字体banner
    for x in json.loads(res.text)['data']['compList'][1:2]:
        pre_belong = "精选"
        data = x.get('list',0)
        if not data:
            continue
        for each in data[0:-1]:
            pre_belong_sec = pre_belong + "_" + each["title"]
            p_id = each["contentDestination"]
            v = VivoCrawlPage()
            unique_param = {"showClock": "false", "id": p_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response("get", param_str)
            print(res.text)
            for i in json.loads(res.text)['data']['compList'][0]['list']:
                category = i["category"]
                content_destination = i.get("contentDestination", "")
                if content_destination:
                    id = content_destination
                    unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category), "id": id,
                                    "viewid": "-100", "cfrom": "404"}
                    v = VivoCrawlGetTheme()
                    param_str = v.get_paramm(unique_param)
                    res = v.get_response("get", param_str)
                    first_layer =  json.loads(res.text)['data']
                    title = first_layer['title']
                    for sec in first_layer['views']:
                        if sec.get("contentId","") and  sec.get("contentId","") != '0':
                            sec_layer = sec
                            break
                        else:
                            continue
                    content_id = sec_layer['contentId']
                    belong = pre_belong_sec + "_" + title
                    print(belong)
                    if content_id:
                        pass
                    else:
                        continue
                    v = VivoCrawlGetEachTheme()
                    p_encode_str = '{{"isBanner":"1","o":"","pageSize":"100","setId":{},"startIndex":"0","tt":{}}}'.format(
                        content_id, category)
                    p = v.get_param_p(p_encode_str)
                    unique_param = {"p": p}
                    param_str = v.get_paramm(unique_param)
                    res = v.get_response("get", param_str)
                    res_ids = json.loads(res.text)['resList']
                    for each in res_ids:
                        res_id = each['resId']
                        category = each['category']
                        p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                        v = VivoCrawlEach()
                        p = v.get_param_p(p_encode_str)
                        unique_param = {"p": p, "themetype": category, "resId": res_id}
                        param_str = v.get_paramm(unique_param)
                        res = v.get_response("get", param_str)
                        p = ParsingVivoItem(res.text)
                        result = p.get_info(belong=belong, categories=category)
                        print(result)

    # for x in json.loads(res.text)['data']['compList'][0:1]:
    #     pre_belong = "精选banner"
    #     data = x['list']
    #
    #     for each in data:
    #         belong = pre_belong + "_" + each["title"]
    #         get_recommond_data(each, belong)


    v = VivoCrawlPage()
    request_method = "get"
    unique_num = 99
    unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                    "category": "{}".format(unique_num), "showClock": "false"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    # 小编精选
    for x in json.loads(res.text)['data']['compList'][1:2]:
        pre_belong = "精选"
        data = x.get('list',0)
        if not data:
            continue
        for each in data[0:-1]:
            pre_belong_sec = pre_belong + "_" + each["title"]+ "_" + "小编精选"
            p_id = each["contentDestination"]
            v = VivoCrawlPage()
            unique_param = {"showClock": "false", "id": p_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response("get", param_str)
            print(res.text)
            for i in json.loads(res.text)['data']['compList'][1]['list']:
                category = i["category"]
                content_destination = i.get("contentDestination", "")
                if content_destination:
                    id = content_destination
                    unique_param = {"themetype": "{}".format(category), "tt": "{}".format(category), "id": id,
                                    "viewid": "-100", "cfrom": "404"}
                    v = VivoCrawlGetTheme()
                    param_str = v.get_paramm(unique_param)
                    res = v.get_response("get", param_str)
                    first_layer =  json.loads(res.text)['data']
                    title = first_layer['title']
                    for sec in first_layer['views']:
                        if sec.get("contentId","") and  sec.get("contentId","") != '0':
                            sec_layer = sec
                            break
                        else:
                            continue
                    content_id = sec_layer['contentId']
                    belong = pre_belong_sec + "_" + title
                    print(belong)
                    if content_id:
                        pass
                    else:
                        continue
                    v = VivoCrawlGetEachTheme()
                    p_encode_str = '{{"isBanner":"1","o":"","pageSize":"100","setId":{},"startIndex":"0","tt":{}}}'.format(
                        content_id, category)
                    p = v.get_param_p(p_encode_str)
                    unique_param = {"p": p}
                    param_str = v.get_paramm(unique_param)
                    res = v.get_response("get", param_str)
                    res_ids = json.loads(res.text)['resList']
                    for each in res_ids:
                        res_id = each['resId']
                        category = each['category']
                        p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                        v = VivoCrawlEach()
                        p = v.get_param_p(p_encode_str)
                        unique_param = {"p": p, "themetype": category, "resId": res_id}
                        param_str = v.get_paramm(unique_param)
                        res = v.get_response("get", param_str)
                        p = ParsingVivoItem(res.text)
                        result = p.get_info(belong=belong, categories=category)
                        print(result)
    v = VivoCrawlPage()
    request_method = "get"
    unique_num = 99
    unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                    "category": "{}".format(unique_num), "showClock": "false"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    # 精选 推荐主题
    for x in json.loads(res.text)['data']['compList'][1:2]:
        pre_belong = "精选"
        data = x.get('list', 0)
        if not data:
            continue
        for each in data[0:-1]:
            pre_belong_sec = pre_belong + "_" + each["title"]
            print("pre_belong_sec",pre_belong_sec)
            p_id = each["contentDestination"]
            v = VivoCrawlPage()
            unique_param = {"showClock": "false", "id": p_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response("get", param_str)
            print(res.text)
            # for i in json.loads(res.text)['data']['compList'][2]:
            #  {"category":"1","componentType":"11","page":"103","pageIndex":"1","setId":"2450"}

            # {'id': 5329, 'position': 3, 'type': 1, 'setId': 2450, 'title': '推荐主题', 'redirectType': -1,
            #  'redirectPage': 0, 'category': 1, 'displayNum': 0, 'resList': None, 'bannerList': None}
            layer = json.loads(res.text)['data']['compList'][2]
            title = layer['title']
            belong = pre_belong_sec+"_"+title
            category = layer["category"]
            set_id = layer.get("setId", "")
            p_encode_str = '{{"category":"{}","componentType":"11","page":"103","pageIndex":"1","setId":"{}"}}'.format(
                 category,set_id)
            p = v.get_param_p(p_encode_str)
            unique_param = {"showClock":False,"p":p}
            v = VivoCrawlResource()
            param_str = v.get_paramm(unique_param)
            res = v.get_response("get", param_str)
            first_layer =  json.loads(res.text)['data']

            res_ids = first_layer['resList']
            for each in res_ids:
                res_id = each['resId']
                category = each['category']
                p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                v = VivoCrawlEach()
                p = v.get_param_p(p_encode_str)
                unique_param = {"p": p, "themetype": category, "resId": res_id}
                param_str = v.get_paramm(unique_param)
                res = v.get_response("get", param_str)
                p = ParsingVivoItem(res.text)
                result = p.get_info(belong=belong, categories=category)
                print(result)
    v = VivoCrawlPage()
    request_method = "get"
    unique_num = 99
    unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                    "category": "{}".format(unique_num), "showClock": "false"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    # 精选字体主题壁纸
    for x in json.loads(res.text)['data']['compList'][-1]['itemList']:
        v = VivoCrawllist()
        category = x['category']
        title = x['title']
        if title == "铃声" or title == "锁屏":
            continue
        setId = x['setId']
        request_method = "get"
        param_p_str = '{{"category":"{}","componentType":"11","page":"103","pageIndex":"1","setId":"{}"}}'.format(
            category, setId)
        p = v.get_param_p(param_p_str)
        unique_param = {"showClock": "false", "p": p}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        res_ids = json.loads(res.text)['data']['resList']
        types = {"主题": "1", "字体": "4", "壁纸": "9", "锁屏": "5"}
        for each in res_ids:
            res_id = each['resId']
            category = each['category']
            if category ==1:
                c_type = "主题"
            elif category ==4:
                c_type = "字体"
            elif category ==9:
                c_type = "壁纸"
            elif category ==5:
                c_type = "锁屏"
            belong = "精选"+"_" + c_type
            p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
            v = VivoCrawlEach()
            p = v.get_param_p(p_encode_str)
            unique_param = {"p": p, "themetype": category, "resId": res_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response(request_method, param_str)
            p = ParsingVivoItem(res.text)
            result = p.get_info(belong, category)
            print(result)

    # 分类细项
    # types = {"主题": "1", "字体": "4", "壁纸": "9", "锁屏": "5"}
    types = {"主题": "1", "字体": "4", "锁屏": "5"}
    colum_num = {"主题": 3, "字体": 3, "锁屏": 2}
    cfrom_num = {"主题": 814, "字体": 849, "锁屏": 857, "壁纸": ""}
    for key in types:
        print(key)
        v = VivoCrawlPage()
        colum_num_each = colum_num[key]
        type_num = types[key]

        request_method = "get"
        unique_num = type_num
        unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                        "category": "{}".format(unique_num), "showClock": "false"}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)

        each_classify = json.loads(res.text)['data']['compList']
        v = VivoCrawlClassifyTheme()
        unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        contentId = json.loads(res.text)["data"]["contentId"]
        print(each_classify)

        for x in each_classify[0:colum_num_each]:
            belong = "分类"+"_"+key+"_"+x.get("title", "")
            v = VivoCrawlClassifyThemeEach()
            redirectId = x.get("redirectId", "")
            setId = contentId
            cfrom = cfrom_num[key]
            pageSize = 100
            unique_param = {"tt": "{}".format(unique_num), "ct": redirectId, "setId": setId, "cfrom": cfrom,
                            "pageSize": pageSize, "startIndex": 0}
            param_str = v.get_paramm(unique_param)
            res = v.get_response(request_method, param_str)
            print(res.text)
            res_ids = json.loads(res.text)['resList']
            if not res_ids:
                continue
            for each in res_ids:
                res_id = each['resId']
                category = each['category']
                p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
                v = VivoCrawlEach()
                p = v.get_param_p(p_encode_str)
                unique_param = {"p": p, "themetype": category, "resId": res_id}
                param_str = v.get_paramm(unique_param)
                res = v.get_response(request_method, param_str)
                p = ParsingVivoItem(res.text)
                result = p.get_info(belong, category)
                print(result)

    types = {"壁纸": "9"}
    colum_num = {"壁纸": 2}
    key = "壁纸"
    type_num = "9"
    v = VivoCrawlPage()
    request_method = "get"
    unique_num = type_num
    unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                    "category": "{}".format(unique_num), "showClock": "false"}
    param_str = v.get_paramm(unique_param)
    res = v.get_response(request_method, param_str)
    # 获取壁纸主题2个
    each_classify = json.loads(res.text)['data']['compList']
    for x in each_classify[0:-7]:
        belong = "分类_壁纸_"+x.get("title", "")
        v = VivoCrawlClassifyTheme()
        # unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num, "cfrom": 1070, "viewid": -100,
        #                 "id": redirectId}
        unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)

        contentIds = json.loads(res.text)['data']['contentId']
        v= VivoCrawlClassifyThemeEach()
        unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num,"ct":10,"setId":contentIds,"pageSize":100,"startIndex":0}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        res_ids = json.loads(res.text)['resList']
        for each in res_ids:
            res_id = each['resId']
            category = each['category']
            p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
            v = VivoCrawlEach()
            p = v.get_param_p(p_encode_str)
            unique_param = {"p": p, "themetype": category, "resId": res_id}
            param_str = v.get_paramm(unique_param)
            res = v.get_response(request_method, param_str)
            p = ParsingVivoItem(res.text)
            result = p.get_info(belong, category)
            print(result)



    # 获取官方推荐
    # x = each_classify[2]
    # a = x["list"][0]
    # content_d = a["contentDestination"]
    # unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num, "cfrom": 1070, "viewid": -100,
    #                 "id": content_d}
    # v = VivoCrawlGetTheme()
    # param_str = v.get_paramm(unique_param)
    # res = v.get_response("get", param_str)
    # get_belong = json.loads(res.text)['data']
    # pre_belong = "分类_壁纸"+get_belong['title']
    # content_id = get_belong["views"][0]["contentId"]
    # v = VivoCrawlGetEachTheme()
    # p_encode_str = '{{"isBanner":"1","o":"","pageSize":"100","setId":"{}","startIndex":"0","tt":"{}"}}'.format(
    #     content_id, unique_num)
    # p = v.get_param_p(p_encode_str)
    # unique_param = {"p": p, 'tt': unique_num, "themetype": unique_num}
    # param_str = v.get_paramm(unique_param)
    # res = v.get_response(request_method, param_str)
    # res_ids = json.loads(res.text)['resList']
    # for each in res_ids:
    #     res_id = each['resId']
    #     category = each['category']
    #     p_encode_str = '{{"o": "", "resId": {}, "tt": {}}}'.format(res_id, category)
    #     v = VivoCrawlEach()
    #     p = v.get_param_p(p_encode_str)
    #     unique_param = {"p": p, "themetype": category, "resId": res_id}
    #     param_str = v.get_paramm(unique_param)
    #     res = v.get_response(request_method, param_str)
    #     p = ParsingVivoItem(res.text)
    #     result = p.get_info(belong, category)
    #     print(result)



    # 获取分类
    types = {"主题": "1", "字体": "4", "壁纸": "9", "锁屏": "5"}
    # types = {"主题": "1", "壁纸": "9", "锁屏": "5"}
    cfrom = {"主题": 814, "字体": 815, "锁屏": 403, "壁纸": ""}

    for key in types:
        print(key)
        v = VivoCrawlPage()
        type_num = types[key]
        unique_num = type_num
        unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),
                        "category": "{}".format(unique_num), "showClock": "false"}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        each_classify = json.loads(res.text)['data']['compList']
        v = VivoCrawlClassifyTheme()
        unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num}
        param_str = v.get_paramm(unique_param)
        res = v.get_response(request_method, param_str)
        contentId = json.loads(res.text)["data"]["contentId"]
        if key == "锁屏":
            num = -1
        else:
            num = -2
        for each in each_classify[num:]:
            belong_pre = "分类_"+ key +"_"+each['title']
            print(belong_pre)
            classify_list = each["list"]
            for classify_data in classify_list:
                p_id = classify_data['id']
                if p_id == 22193:
                    cc = "艺术"
                elif p_id == 22194:
                    cc = "古典"
                elif p_id == 22195:
                    cc = "阅读"
                elif p_id == 22196:
                    cc = "可爱"
                elif p_id == 22197:
                    cc = "手写"
                elif p_id == 22198:
                    cc = "书法"
                elif p_id == 22199:
                    cc = "草书"
                elif p_id == 22200:
                    cc = "印刷"
                elif p_id == 22201:
                    cc = "屏显"
                else:
                    cc = classify_data.get("title", "")
                if cc == "官方":
                    continue
                belong = belong_pre + "_" + cc
                if "颜色" in belong_pre:
                    get_recommond_data(classify_data, belong)
                else:
                    print(classify_data['title'])
                    content_d = classify_data["contentDestination"]
                    unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num, "cfrom": cfrom[key],
                                    "si": content_d, "startIndex": 0,"pageSize":100}
                    v = VivoCrawlThemeFuck()
                    param_str = v.get_paramm(unique_param)
                    res = v.get_response("get", param_str)
                    res_ids = json.loads(res.text)['resList']

                    for each in res_ids:

                        res_id = each['resId']

                        category = each['category']
                        p_encode_str = '{{"o":"", "resId":"{}", "tt":"{}"}}'.format(res_id, category)
                        v = VivoCrawlEach()
                        p = v.get_param_p(p_encode_str)
                        unique_param = {"p": p, "themetype": category, "resId": res_id}
                        param_str = v.get_paramm(unique_param)
                        res = v.get_response(request_method, param_str)
                        p = ParsingVivoItem(res.text)
                        result = p.get_info(belong, category)
                        print(result)



if __name__ == '__main__':
    # run()
    run_vivo()

    # 获取分类  # types = { "字体": "4"}  # cfrom = {"主题": 814, "字体": 815, "锁屏": 403, "壁纸": ""}  #  # for key in types:  #     print(key)  #     v = VivoCrawlPage()  #     type_num = types[key]  #     unique_num = type_num  #     unique_param = {"themetype": "{}".format(unique_num), "tt": "{}".format(unique_num),  #                     "category": "{}".format(unique_num), "showClock": "false"}  #     param_str = v.get_paramm(unique_param)  #     res = v.get_response(request_method, param_str)  #     each_classify = json.loads(res.text)['data']['compList']  #     v = VivoCrawlClassifyTheme()  #     unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num}  #     param_str = v.get_paramm(unique_param)  #     res = v.get_response(request_method, param_str)  #     contentId = json.loads(res.text)["data"]["contentId"]  #     if key == "锁屏":  #         num = -1  #     else:  #         num = -2  #     for each in each_classify[num:]:  #         belong_pre = each['title']  #         print(belong_pre)  #         classify_list = each["list"]  #         for classify_data in classify_list:  #             cc = classify_data.get("title", "")  #             if cc == "官方":  #                 continue  #             belong = belong_pre + "_" + cc  #             if belong_pre == "颜色":  #                 get_recommond_data(classify_data, belong)  #             else:  #                 print(classify_data['title'])  #                 content_d = classify_data["contentDestination"]  #                 unique_param = {"tt": "{}".format(unique_num), "themetype": unique_num, "cfrom": cfrom[key],  #                                 "si": content_d, "startIndex": 0}  #                 v = VivoCrawlThemeFuck()  #                 param_str = v.get_paramm(unique_param)  #                 res = v.get_response("get", param_str)  #                 res_ids = json.loads(res.text)['resList']  #                 for each in res_ids:  #                     res_id = each['resId']  #                     category = each['category']  #                     p_encode_str = '{{"o":"", "resId":"{}", "tt":"{}"}}'.format(res_id, category)  #                     v = VivoCrawlEach()  #                     p = v.get_param_p(p_encode_str)  #                     unique_param = {"p": p, "themetype": category, "resId": res_id}  #                     param_str = v.get_paramm(unique_param)  #                     res = v.get_response(request_method, param_str)  #                     p = ParsingVivoItem(res.text)  #                     result = p.get_info(belong, category)  #                     print(result)
