import ast
import copy
import os
from platform import node
import astunparse

import sys

import logddd

from transcode_wrap.code_trans import transfer

sys.setrecursionlimit(10000)


def search_py_file(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            search_py_file(cur_path)
        elif file.endswith(".py") and not file.endswith("_res.py") and (
                not file.startswith("plot") and file.endswith(".py")):
            # 如果是py文件就对其进行处理
            save_path = os.path.join(path, file.replace(".py", "_res.py"))
            logddd.log('转换文件' + cur_path)
            # transfer(cur_path, save_path)
            try:
                transfer(cur_path, save_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # file_path = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/ast_convert/resource/inittest"
    file_path = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/ast_convert/resource/scikit-learn/sklearn"
    # file_path = "/home/dlf/testCode/ast_convert/resource/递归引入方法"
    # file_path = "/home/dlf/testCode/scikit-learn"
    # file_path = "/home/dlf/testCode/ast_convert/resource/分类器比较"
    # file_path = "/Users/dailinfeng/Desktop/实验室项目/kubeflow/ast_convert/resource/递归引入方法"
    # 传入空的list接收文件名，获取当前项目所有的fun和class
    search_py_file(file_path)
    logddd.log("pre_search_py_file 结束")
