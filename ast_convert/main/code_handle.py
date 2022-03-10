import ast

import astunparse


def reduction_params(old_params):
    """
        还原一个方法原来的参数
    :param old_params:  传入的是原来参数的参数名
    :return: 返回的是形成的参数还原代码的
    """
    code_str = ""
    for param in old_params:
        single_statement = f"{param} = joblib.load({param}_input.path)[\"{param}\"]\n"
        code_str += single_statement
    r_node = ast.parse(code_str)
    origin_params_node = []
    for item in r_node.body:
        class_name = item.__class__.__name__
        if class_name == "Assign":
            origin_params_node.append(item)
    return origin_params_node
    # print(astunparse.dump(r_node))


def handle_decorators(file_name, packages):
    """
        形成方法上面组件注解的代码
    :param file_name:
    :param packages:
    :return:
    """
    # print(packages)
    # @component(output_component_file='fun1min_component.yaml',packages_to_install=['lmfit', 'numpy', 'matplotlib', 'joblib', 'pandas', ])
    install_package = ""
    for index, package in enumerate(packages):
        if index != len(packages) - 1:
            install_package += "'" + package + "',"
        else:
            install_package += "'" + package + "'"
    #         \ndef func():\n    pass 这一段要加才是一个不会编译出错的语法，才能够parse
    code = f"@component(output_component_file='{file_name}',packages_to_install=[{install_package}])\ndef func():\n    pass"
    # print(code)
    r_node = ast.parse(code)
    for item in r_node.body:
        class_name = item.__class__.__name__
        # print(class_name)
        # 找到装饰器的list，装饰器的节点是在FunctionDef里
        if class_name == "FunctionDef":
            return item.decorator_list
    # print(astunparse.dump(r_node))
    return None
