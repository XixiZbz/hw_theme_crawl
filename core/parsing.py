#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 2:36 下午
# @Author  : zbz
# @Site    : 
# @File    : parsing.py
# @Software: PyCharm
import json


class Parsing:
    def __init__(self,text):
        self.text = json.loads(text)
        self.text_list = self.text["list"]

class ParsingColumn(Parsing):
    def get_module_name(self):
        names = []
        for result in self.text_list:
            names.append(result['moduleName'])
        return names

    def get_module_source_id(self):
        source_ids = []
        for result in self.text_list:
            source_ids.append(result["dataSourceId"])
        return source_ids

    def mix_name_source_id(self):
        mix_info = []
        for result in self.text_list:
            name = result['moduleName']
            source_id = result["dataSourceId"]
            mix_info.append("{}|{}".format(name, source_id))
        return mix_info

class ParsingList(Parsing):
    def __init__(self, text):
        super().__init__(text)
        self.exist = True if self.text_list else False
        if self.exist:
            self.info = self.text_list
        else:
            self.info=False
    def get_info(self):
        if not self.exist:
            return False
        else:
            for info in self.info:
                # price 价格,downloadcount 下载量,stars星级,commentNum评论数,collectCount收藏数,praiseCount点赞数 previews
                name = info.get("title-cn","")
                if name:
                    pass
                else:
                    name = info.get("title-local", "")
                if name:
                    pass
                else:
                    name = info["title"][0].get("title","")

                price = info.get("price",0)
                downloadcount = info.get("downloadcount",0)
                if downloadcount:
                    pass
                else:
                    downloadcount = info.get("downloadCount", 0)
                stars = info.get("stars",0)
                commentNum = info.get("commentNum",0)
                collectCount = info.get("collectCount",0)
                praiseCount = info.get("praiseCount",0)
                pic_info = info.get("previews","")
                p_id = info.get("id","")
                author = info.get("designer","")
                add_time = info.get("addTime","")
                version = info.get("version","")
                yield {"name":name,"price":price,"downloadcount":downloadcount,"stars":stars,"commentNum":commentNum,
                        "collectCount":collectCount,"praiseCount":praiseCount,"pic_info":pic_info,"p_id":p_id,"author":author,"add_time":add_time,"version":version}





if __name__ == '__main__':
    from core.crawl import *

    c = CrawlThemne()
    result = c.get_theme_column()
    print(result.text)
    p = ParsingColumn(result.text)
    a = p.mix_name_source_id()
    print(a)
    for x in a[0:1]:
        name,id = x.split("|")
        if id:
            d = c.get_column_data(id)
        else:
            continue
        for i in d:
            h = ParsingList(i.text)
            info = h.get_info()
            for j in info:
                pass
