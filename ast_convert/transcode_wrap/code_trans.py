import logddd


def transfer(cur_path, save_path):
    """
    代码外包裹

    :param cur_path: 当前代码路径
    :param save_path: 存储代码的路径
    :return:
    """
    with open(cur_path) as f:
        code = f.read()
    logddd.log(cur_path)
    logddd.log(code)
