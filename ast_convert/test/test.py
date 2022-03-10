import ast

import astunparse

if __name__ == '__main__':
    code_str = "xdata = joblib.load(xdata_inputpath.path)\n" \
               "ydata = joblib.load(ydata_inputpath.path)\n"
    r_node = ast.parse(code_str)
    origin_params_node = []
    for item in r_node.body:
        class_name = item.__class__.__name__
        if class_name == "Assign":
            origin_params_node.append(item)

    print(astunparse.dump(r_node))
