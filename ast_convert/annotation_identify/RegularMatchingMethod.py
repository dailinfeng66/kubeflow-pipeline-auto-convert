import re


def get_params_list(annotation: str):
    """
        根据标准的方法注释获取注释中方法的参数内容
    :param annotation: 注释
    :return: 如果当前方法注释有参数则返回当前传入注释的参数列表，如果当前方法注释没有参数则返回None
    """

    if """Parameters
    ----------""" in annotation:
        # 根据---------- 进行分割，参数都在第二个位置
        params_str = code.split("----------")[1]
        # 删除开头的回车
        params_str = re.sub(r'\n', '', params_str, count=1)
        # 查找出所有的参数注释，并删除掉参数注释下面的其他东西 比如Returns
        matcher_params = re.findall(r'[\s\S]+\n{2}', params_str)
        # 如果什么都没有查找到
        if len(matcher_params) == 0:
            pass
        matcher_params_str = matcher_params[0]
        # 匹配出
        params_suffix = re.findall(r'\w+:', matcher_params_str)
        # 参数列表
        params = []
        # 此时匹配出来的参数是带有后缀的，因此现在要删除掉后缀
        for item in params_suffix:
            params.append(item.replace(":", ""))
        return params
    return None


if __name__ == '__main__':
    code = """Chain together an optional series of text processing steps to go from
    a single document to ngrams, with or without tokenizing or preprocessing.

    If analyzer is used, only the decoder argument is used, as the analyzer is
    intended to replace the preprocessor, tokenizer, and ngrams steps.

    Parameters
    ----------
    analyzer: callable, default=None
    tokenizer: callable, default=None
    ngrams: callable, default=None
    preprocessor: callable, default=None
    decoder: callable, default=None
    stop_words: list, default=None

    Returns
    -------
    ngrams: list
        A sequence of tokens, possibly with pairs, triples, etc.
    """
    print(get_params_list(code))
