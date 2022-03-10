import ast
from _ast import Call, FunctionDef, Return
from typing import Any

import astunparse
from astroid import Import, ImportFrom
from logddd import log

from main.code_handle import reduction_params, handle_decorators

"""
    处理方法代码
        将需要引入的kubeflow SDK的import代码添加到文件上面
        ✅将import代码添加到方法定义语句的下一行,包括joblib包的添加
        ✅将方法参数修改为元数据形式并添加输出元数据
        ❓删除方法返回type  暂时没有找到方法返回类型声明对应的node节点  找到了 对象是returns  返回值是Return
        ✅还原参数变量
        ✅在方法定义的上面一行添加装饰器 
        ✅修改方法返回值 使用ast的方法暂时做不出来，因此打算使用字符串匹配的方式完成  因此还是存在限制
            🚫 所有的返回值都必须是变量而不能是其他的表达式或者是方法的调用
        ✅扫描当前方法调用了那些方法，并将这些方法添加到当前方法中
"""
# 存储当前源文件中的方法，key为方法名 value为方法节点
func_dict = dict({})


class CodeTransformer(ast.NodeTransformer):
    # 存储导包节点，用于转移到下
    imports = []
    # 存储第三方包的名字，用于装饰器的添加
    imports_names = []
    # 保存当前方法
    current_func = None
    # 存储当前方法的名字
    cur_func_name = ""
    # 保存当前方法调用的方法名
    call_func = set([])

    def visit_Import(self, node: Import):
        """
         扫描import xxx语句
        :param node:
        :return:
        """
        self.imports_names.append(node.names[0].name)
        self.imports.append(node)
        return node

    def visit_ImportFrom(self, node: ImportFrom):
        """
          扫描from xxx import 语句
        :param node:
        :return:
        """
        self.imports.append(node)
        self.imports_names.append(node.module)
        return node

    def visit_Return(self, node: Return):

        """
        扫描方法的返回值
        一个方法会先到这儿
        :param node:
        :return:
        """
        # 反向获取返回值的代码
        return_code = astunparse.unparse(node).replace("return", "")
        # 当返回值有多个时，ast会自动给返回的值转变为一个元组，因此需要删除元组的括号
        return_code = return_code.replace("(", "").replace(")", "").strip()
        # print(return_code)
        return_params = return_code.split(",")
        # return joblib.dump({"model":model},funcname_output.path)
        dict_str = ""
        for index, param in enumerate(return_params):
            if index < len(return_params) - 1:
                dict_str += f"\"{param}\":{param},"
            else:
                dict_str += f"\"{param}\":{param}"
        return_wrap_code = "return joblib.dump({" + dict_str + "}," + f"{self.cur_func_name}_output.path)"
        # print(return_wrap_code)
        r_node = ast.parse(return_wrap_code)
        # print(astunparse.dump(r_node))
        # return node  # 不要返回就表示遍历这个node之后不返回这个node  ----> 删除这个node
        return r_node.body[0]  # 返回新生成的node来替换原来的Return的node

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
            替换形参名字
        """
        # 存储原来的参数,用作后面的参数还原
        old_args = []
        new_args = []
        # 遍历当前方法的所有形参，将每个形参改为元数据方式输入
        for arg in node.args.args:
            old_args.append(arg.arg)
            # 修改形参的定义语句，并在后面加上参数的type
            arg.arg = arg.arg + "_input:input[DataSet]"

            # 设置参数后面的type为None
            arg.annotation = None
            new_args.append(arg)
        """
            给方法添加返回的元数据参数
        """
        output = ast.arg()  # 这是一个arg对象
        output.arg = node.name + "_output:[DataSet]"
        output.annotation = None
        new_args.append(output)

        # 设置参数的默认值
        node.args.defaults = []
        node.args.args = new_args  # 将新的参数赋值给参数对象

        """
            添加当前节点所调用的方法
            遍历
        """
        func_node_list = []  # 当前方法所调用方法的节点列表
        # 遍历当前方法调用的方法列表，检测这些方法是否在当前源文件的方法字典中，如果在的话就将方法node添加到当前方法调用的方法列表中
        for func in self.call_func:
            if func in func_dict.keys():
                func_node_list.append(func_dict[func])

        # 方法原参数的加载

        """ 
                 方法内代码的重新组合
                 self.imports 导包代码
                 func_node_list 当前方法所调用的方法的代码
                 node.body  当前方法本身的代码
        """
        # 添加joblib代码的import
        joblib_module = ast.Import()
        joblib_alias = ast.alias()
        joblib_alias.name = "joblib"
        joblib_alias.asname = None
        joblib_module.names = [joblib_alias]
        # 添加joblib代码的import
        params = reduction_params(old_params=old_args)
        # 获取方法定义代码上组件装饰器代码
        decorator = handle_decorators(node.name + "_component.yaml", self.imports_names)
        node.decorator_list = decorator  # 设置装饰器

        node.body = self.imports + [joblib_module] + func_node_list + params + node.body

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
        # print(node.func.value.id)
        if hasattr(node.func, "value"):
            # print(node.func.value.id)
            pass
        #  有name的才是单个方法的调用
        # if hasattr(node.func, "name"):
        else:
            cal_name = node.func.id
            # print("call_func_name:" + cal_name)
            self.call_func.add(cal_name)
        return node


import copy


# 自己读取的方式
def read_by_self(r_node):
    # 遍历每一个node
    for node in r_node.body:
        node_name = type(node).__name__
        # 如果是方法定义的节点
        if node_name == "FunctionDef":
            # 这儿要用深拷贝，不然node节点是相同的，方法参数修改时方法内的方法代码也会被修改
            func_dict[node.name] = copy.deepcopy(node)


if __name__ == '__main__':
    with open("../resource/envtest.py") as f:
        code = f.read()
    # 首先遍历出当前源文件的方法字典
    r_node = ast.parse(code)
    read_by_self(r_node)
    transformer = CodeTransformer()
    res = transformer.visit(r_node)
    # print(astunparse.dump(r_node))
    source = astunparse.unparse(res)  # astunparse 一般python不自带，需要conda 或者 pip安装
    component_import = "import kfp\nfrom kfp.v2 import dsl\nfrom kfp.v2.dsl import component, Input, Output, OutputPath, Dataset, Model,InputPath\nimport kfp.components as comp\n"
    source = component_import + source
    print(source)
