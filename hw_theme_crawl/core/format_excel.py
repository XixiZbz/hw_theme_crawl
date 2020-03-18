#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/16 4:51 下午
# @Author  : zbz
# @Site    : 
# @File    : format_excel.py
# @Software: PyCharm

from xlrd import open_workbook
from xlutils.copy import copy
import arrow
class ExcelFormat(object):
    def __init__(self,suffix):
        self.date = arrow.now().format("YYYY-MM-DD")
        self.xlsx_name = "{} {}".format(self.date,suffix)
        self.workbook = open_workbook("./db/{}.xls".format(self.xlsx_name))
    def __del__(self):
        self.workbook.close()

    def add_or_select_worksheet(self,worksheet_name):
        worksheet = self.workbook.add_worksheet(worksheet_name)

