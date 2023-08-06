# -*- coding: utf-8 -*-
import datetime


def is_valid_date(strdate):
    '''判断是否是一个有效的日期字符串'''
    try:
        data = datetime.datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S.%f")
        return data
    except Exception as e:
        try:
            data = datetime.datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S")
            return data
        except Exception as e:
            try:
                data = datetime.datetime.strptime(strdate, "%Y-%m-%d")
                return data
            except Exception as e:
                return False
