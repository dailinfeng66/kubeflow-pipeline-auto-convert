import ast
import sys
from _ast import Return
from typing import Any

from transcode.params_save_util import get_func_dict, get_class_def_dict


class ClassTransformer(ast.NodeTransformer):
    # 保存当前方法
    current_func = None
    # 存储当前方法的名字
    cur_func_name = ""
    # 保存当前方法调用的方法名
    call_func = set([])

    def visit_FunctionDef(self, node):
        # 当前方法的名字
        self.cur_func_name = node.name
        """
        扫描方法节点
        :param node:
        :return:
        """
        self.generic_visit(node)  # 这里表示先去访问里面的children node

        """
            添加当前节点所调用的方法
            遍历
        """
        func_node_list = []  # 当前方法所调用方法的节点列表
        # 遍历当前方法调用的方法列表，检测这些方法是否在当前源文件的方法字典中，如果在的话就将方法node添加到当前方法调用的方法列表中
        for func in self.call_func:
            func_dict = get_func_dict()
            if func in func_dict.keys():
                func_node_list.append(func_dict[func])
            #     如果当前方法是类定义代码的调用
            class_def_dict = get_class_def_dict()
            if func in class_def_dict.keys():
                func_node_list.append(class_def_dict[func])

        # 方法原参数的加载

        """ 
                 方法内代码的重新组合
                 self.imports 导包代码
                 func_node_list 当前方法所调用的方法的代码
                 node.body  当前方法本身的代码
        """

        node.body = func_node_list + node.body

        # 将当前方法调用的方法列表置为空
        self.call_func = set([])
        return node

    def visit_Call(self, node) -> Any:
        """
        获取方法调用的代码
        这个方法会在每一个方法定义代码扫描之前扫描
        :param node:
        :return:
        """
        self.generic_visit(node)

        if hasattr(node.func, "value"):
            # print("call_func_name value:" + node.func.value.id)
            pass
        elif hasattr(node.func, "id"):
            cal_name = node.func.id
            # print("call_func_name id:" + cal_name)
            self.call_func.add(cal_name)
        return node
