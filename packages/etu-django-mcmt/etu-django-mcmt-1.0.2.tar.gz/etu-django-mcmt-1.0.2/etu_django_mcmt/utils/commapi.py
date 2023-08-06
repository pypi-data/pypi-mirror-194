# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 09:55
# @Author  : Jieay
# @File    : commapi.py
import datetime


def datetime_to_str(o):
    """
    封装将 datetime 时间对象转换字符串格式
    :param o: 时间对象：datetime.datetime or datetime.date
    :return:
    """
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(o, datetime.date):
        return o.strftime('%Y-%m-%d')
    else:
        return str(o)
