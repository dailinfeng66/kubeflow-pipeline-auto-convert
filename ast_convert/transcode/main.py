import ast
import copy
import os
from platform import node

from transcode.class_func_handle import ClassTransformer
from transcode.generate_ast import transfer, CodeTransformer, read_by_self
from transcode.params_save_util import global_param_init, get_class_def_dict, set_class_def_dict


def pre_search_py_file(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            pre_search_py_file(cur_path)
        elif file.endswith(".py"):
            # 如果是py文件就对其进行处理
            save_path = os.path.join(path, file.replace(".py", "_res.py"))
            # transfer(cur_path, save_path)
            with open(cur_path) as f:
                code = f.read()
            r_node = ast.parse(code)
            print("读取文件" + cur_path)
            read_by_self(r_node)
            # print('转换了文件' + save_path)


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
        elif file.endswith(".py"):
            # 如果是py文件就对其进行处理
            save_path = os.path.join(path, file.replace(".py", "_res.py"))
            print('转换文件' + cur_path)
            transfer(cur_path, save_path)


if __name__ == '__main__':
    global_param_init()
    # file_path = "/Users/dailinfeng/Desktop/小项目/爬虫/政府来电爬虫"
    file_path = "/Users/dailinfeng/Desktop/小项目/auto-sklearn"
    # 传入空的list接收文件名
    pre_search_py_file(file_path)
    # 遍历类的节点map 对类的每一个方法进行处理
    class_def_dict = get_class_def_dict()
    transformer = ClassTransformer()

    for node in class_def_dict.keys():
        visit = transformer.visit(class_def_dict[node])
        class_def_dict[node] = visit

    set_class_def_dict(class_def_dict)
    # 循环打印show_files函数返回的文件名列表
    search_py_file(file_path)
