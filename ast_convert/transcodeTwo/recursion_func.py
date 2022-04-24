import ast
import sys
from _ast import Return
from typing import Any
import copy
from params_save_util import get_func_dict, get_class_def_dict

"""
    给一个方法调用，递归的去访问当前方法所调用的方法
"""


class RecursionGetFunc(ast.NodeTransformer):
    """
    访问一个方法 并查询当前方法所调用的方法
    然后递归的去方法当前方法所调用的方法
    最后将所有的方法进行返回
    """
    # 当前层方法所调用的方法节点
    call_func_nodes = list([])
    import_list = list([])

    def visit_FunctionDef(self, node):
        """
            当前方法的作用是：
                将被调用到方法的方法体添加到当前方法体中
        """
        self.generic_visit(node)  # 这里表示先去访问里面的children node
        node.body = copy.deepcopy(list(self.import_list)) + copy.deepcopy(self.call_func_nodes) + node.body
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
            pass
        # 方法调用，如果是方法那就递归的去访问其下层方法
        elif hasattr(node.func, "id"):
            cal_name = node.func.id
            # 获取当前工程的所有方法字典
            func_dict = get_func_dict()
            #
            class_def_dict = get_class_def_dict()
            # 如果当前调用的方法属于本项目源码中的方法
            if cal_name in func_dict.keys():
                # 从方法字典中找到被调用的方法ast node 再将该node进行转换
                recursion_get_func = RecursionGetFunc()
                # 获取当前被调用方法的node
                func_node = func_dict[cal_name]
                # print("进入递归->"+node.name)
                # 对当前被调用方法进行检查，看看它是否调用了其他方法
                call_func_node = recursion_get_func.visit(copy.deepcopy(func_node['func']))
                # print("退出递归->"+node.name)
                # 将当前被调用方法 处理之后的方法节点和所需要引入的包都添加到这一层来
                self.import_list.append(func_node['imports'])
                self.call_func_nodes.append(call_func_node)
                del recursion_get_func

        return node
