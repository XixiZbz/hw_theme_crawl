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
to_txt = ToTxt()
to_txt.open_or_new()


def type_in(categories,res):
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
        name,id = x.split("|")
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
        name,id = x.split("|")
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
if __name__ == '__main__':
    # functions = dir(CrawlFont)
    # fuction_myself = [x for x in functions if "__" not in x]
    # print(fuction_myself)
    # c = CrawlFeatured()
    # res = c.fetured_hot_font()
    # categories = "精选-热门字体"
    # type_in(categories, res)
    # c = CrawlFont()
    # res = c.font_get_font_album()
    # print(res.text)
    # for r in res:
    #     print(r.text)
    # categories = "字体-炫动字体-新品"
    # type_in(categories, res)
    run()
    # c = CrawlFeatured()
    # res = c.fetured_dynamic_wallpaper()
    # print(res.text)
    # categories = "动态壁纸"
    # type_in(categories, res)