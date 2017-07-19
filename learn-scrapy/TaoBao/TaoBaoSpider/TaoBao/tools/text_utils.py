import re


def replace(reg, new_string, string):
    """
    用新的字符串替换被则正表达式匹配的字符。
    返回的第一个结果是被替换后的字符串，第二个是替换了多少个。
    如果转换失败则返回源字符串
    """
    result = new_string
    number = 0
    try:
        re_obj = re.compile(reg)
        result, number = re_obj.subn(new_string, string)
    except:
        pass
    return result, number


def to_int(string, default=0):
    """
    返回number，如果转换失败 则返回默认值
    :param string: 要转换的string
    :param default: 默认值
    :return:
    """
    return string if str(string).isdigit() else default


def to_float(string, default=0.0):
    """
    返回float，如果转换失败，返回默认值
    :param string: 要转换的string
    :param default: 默认值
    :return:
    """
    try:
        f = float(string)
    except:
        f = default
    return f


def to_string(string, default=""):
    """
    如果是None转换成默认值或者""
    :param default:
    :param string:
    :return:
    """
    return string if string is not None else default
