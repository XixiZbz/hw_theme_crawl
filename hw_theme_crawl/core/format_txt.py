#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 7:29 下午
# @Author  : zbz
# @Site    : 
# @File    : format_txt.py
# @Software: PyCharm
import arrow
import os

project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../"

class ToTxt(object):
    def __init__(self):
        self.date = arrow.now().format("YYYY-MM-DD")

    def open_or_new(self):
        exsit_dir = os.listdir(project_path+"/db")
        if "{}.txt".format(self.date) in exsit_dir:
            exsit = True
        else:
            exsit = False
        if exsit:
            return True
        else:
            with open(project_path+"/db/{}.txt".format(self.date), "w+",encoding="GB18030") as f:
                f.write(
                    "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\r".format("所属大类", "专栏名", "名称", "价格", "下载量",
                                                              "星级", "评论数", "收藏数", "点赞数",
                                                              "图片信息", "图片id","作者","上线时间","版本"))
            return False

    def add_content(self, content):
        with open(project_path+"/db/{}.txt".format(self.date), "a+",encoding="GB18030") as f:
            f.write(content + "\r")

    def format_content(self, info_dict):
        print(info_dict)
        categories = info_dict.get("categories", "")
        belong = info_dict.get("belong", "")
        name = info_dict.get("name", "")
        price = info_dict.get("price", "")
        downloadcount = info_dict.get("downloadcount", "")
        stars = info_dict.get("stars", "")
        commentNum = info_dict.get("commentNum", "")
        collectCount = info_dict.get("collectCount", "")
        praiseCount = info_dict.get("praiseCount", "")
        pic_info = info_dict.get("pic_info", "")
        p_id = info_dict.get("p_id", "")
        author = info_dict.get("author", "")
        add_time = info_dict.get("add_time", "")
        version = info_dict.get("version","")
        content = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(categories, belong, name, price, downloadcount, stars,
                                                            commentNum, collectCount, praiseCount, pic_info, p_id,author,add_time,version)
        self.add_content(content)


if __name__ == '__main__':
    # handle = ToTxt()
    # handle.open_or_new()
    import sys
    print(__file__)  # 此py文件所在的路径
    print(sys.path[0])  # 启动的py文件所在的路径
    print(os.getcwd())  # 工作空间的路径(working directory)，默认为启动的py文件所在路径，但ide中可以自定义设置。
    project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/../"
    print(os.path.abspath(project_path))
