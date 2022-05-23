from resource.递归引入方法.B import func_2


def func_3():
    res = func_2(1)
    return res


def func_c_wrap():
    res3 = func_3()
    return res3



def func_4():
    res = func_2(1)
    res = func_2(1)
    res = func_2(1)
    return res
