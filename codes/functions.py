# _*_ coding: UTF-8 _*_
'''
作用：常用的函数
时间：2016-9-27
备注
'''

import json
import codecs
import os, os.path
import shutil

def _rmtree(root):
    """Catch shutil.rmtree failures on Windows when files are read-only."""
    def _handle_error(fn, path, excinfo):
        os.chmod(path, 0666)
        fn(path)
    return shutil.rmtree(root, onerror=_handle_error)

def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

def crete_dir(des_dir):
    if os.path.isdir(des_dir):
        _rmtree(des_dir)
    os.mkdir(des_dir)

def print_to_json(data):
    # json不支持int作为key，所以int会转为str
    print(json.dumps(data, indent = 2))

def output_to_json(data, file_name, indent = None):
    with codecs.open(file_name, 'w', 'utf-8') as file_json:
        file_json.write(json.dumps(data, ensure_ascii = False, indent = indent))
        file_json.close()