# _*_ coding: UTF-8 _*_
'''
作用：常用的函数
时间：2016-9-27
备注
'''

import json

def print_list(data):
    # json不支持int作为key，所以int会转为str
    print(json.dumps(data, indent = 2))