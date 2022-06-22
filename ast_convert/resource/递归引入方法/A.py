from resource.递归引入方法.B import func_2

import numpy as np


def func_3(arr):
    res = func_2(arr)
    return res


def func_4():
    res = func_2(1)
    res = func_3(1)
    res = func_2(1)
    return res
