import ast
import sys
from _ast import Return
from typing import Any

from params_save_util import get_func_dict, get_class_def_dict, get_rec_save
from recursion_func import RecursionGetFunc

import copy


class FuncCallTransformer(ast.NodeTransformer):
    """
        目的：
            扫描传入的方法节点，
            将类中方法所调用的方法添加到类中的方法中来
            并且将这些方法这些类所需要的第三方包也引入进来
    """
    # 保存当前方法
    current_func = None
    # 存储当前方法的名字
    cur_func_name = ""
    # 保存当前方法调用的方法名
    call_func = list([])
    recur_map = dict({})

    def visit_Call(self, node) -> Any:
        """
        获取方法调用的代码
        这个方法会在每一个方法定义代码扫描之前扫描
        :param node:
        :return:
        """
        import astunparse
        self.generic_visit(node)
        source = astunparse.unparse(node)
        print("访问到了方法调用:" + source)

        if hasattr(node.func, "value"):
            # print("call_func_name value:" + node.func.value.id)
            pass
        elif hasattr(node.func, "id"):
            cal_name = node.func.id
            # 获取当前工程的所有方法字典
            # func_dict = get_func_dict()
            # recursionGetFunc = RecursionGetFunc()
            # func_node = func_dict[cal_name]['func']
            # call_node = recursionGetFunc.visit(copy.deepcopy(func_node))
            # self.call_func.append(call_node)
            self.call_func.append(cal_name)

        return node

    def visit_FunctionDef(self, node):
        # 当前方法的名字
        # self.cur_func_name = node.name
        """
        扫描方法节点
        :param node:
        :return:
        """
        self.generic_visit(node)  # 这里表示先去访问里面的children node
        print("访问到了方法定义：" + node.name)
        # 存储所调用方法的import节点
        import_list = []
        # 遍历当前方法调用的方法列表，检测这些方法是否在当前源文件的方法字典中，如果在的话就将方法node添加到当前方法调用的方法列表中
        # func_dict = get_func_dict()
        # class_def_dict = get_class_def_dict()
        # 对当前调用的方法去重
        call_func = list(set(self.call_func))
        # 所使用方法的列表
        used_func_list = []
        func_dict = get_func_dict()
        print("call_func")
        print(call_func)
        print("call_func")
        # 遍历所有的方法
        for func_name in call_func:
            rec_save = get_rec_save()
            # 如果能够z
            # if func_name in rec_save.keys():
            #     used_func_list.append(rec_save[func_name])
            # else:
            
            recursionGetFunc = RecursionGetFunc()
            recursionGetFunc.call_func_nodes = list([])
            recursionGetFunc.import_list = list([])
            func_node = func_dict[func_name]['func']

            # print("进入递归->"+func_node.name)
            call_node = recursionGetFunc.visit(copy.deepcopy(func_node))
            # print("结束递归->"+func_node.name)
            # rec_save[func_name] = call_node
            used_func_list.append(call_node)
            del recursionGetFunc

        # 方法原参数的加载
        """ 
                 方法内代码的重新组合
                 self.imports 导包代码
                 func_node_list 当前方法所调用的方法的代码
                 node.body  当前方法本身的代码
        """
        node.body = list(set(import_list)) + used_func_list + node.body

        return node
