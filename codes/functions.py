# _*_ coding: UTF-8 _*_
'''
作用：常用的函数
时间：2016-9-27
备注
'''

import json
import codecs

def print_to_json(data):
    # json不支持int作为key，所以int会转为str
    print(json.dumps(data, indent = 2))

def output_to_json(data, file_name, indent = None):
    with codecs.open(file_name, 'w', 'utf-8') as file_json:
        file_json.write(json.dumps(data, ensure_ascii = False, indent = indent))
        file_json.close()