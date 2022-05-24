from resource.递归引入方法.B import func_2


def func_3():
    res = func_2(1)
    return res


def func_4():
    res = func_2(1)
    res = func_3(1)
    res = func_2(1)
    return res
