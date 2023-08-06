import re


def hump2underline(hump_str):
    """
    驼峰形式字符串转成下划线形式
    :param hump_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    """
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hump_str).lower()
    return sub


def underline2hump(underline_str):
    """
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    """
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), underline_str)
    return sub


def json_hump2underline(hump_json_str):
    """
    把一个json字符串中的所有字段名都从驼峰形式替换成下划线形式。
    注意点：因为考虑到json可能具有多层嵌套的复杂结构，所以这里直接采用正则文本替换的方式进行处理，而不是采用把json转成字典再进行处理的方式
    :param hump_json_str: 字段名为驼峰形式的json字符串
    :return: 字段名为下划线形式的json字符串
    """
    # 从json字符串中匹配字段名的正则
    # 注：这里的字段名只考虑由英文字母、数字、下划线组成
    attr_ptn = re.compile(r'"\s*(\w+)\s*"\s*:')
    # 使用hump2underline函数作为re.sub函数第二个参数的回调函数
    sub = re.sub(attr_ptn, lambda x: '"' + hump2underline(x.group(1)) + '" :', hump_json_str)
    return sub

def dict_hump2underline(hump_dict):
    """
    将dict的所有键内的驼峰转换为下划线形式字符串
    :param hump_dict: dict
    :return: 新的字典
    """
    new_dict = {}
    for key, value in hump_dict.items():
        new_dict[hump2underline(key)] = value
    return new_dict

def dict_value_hump2underline(hump_dict):
    """
    将dict的所有键内的驼峰转换为下划线形式字符串
    :param hump_dict: dict
    :return: 新的字典
    """
    if type(hump_dict) == str:
        return hump_dict
    elif type(hump_dict) == list:
        return [dict_value_hump2underline(i) for i in hump_dict]
    elif type(hump_dict) == dict:
        for i in list(hump_dict.keys()):
            new_key = hump2underline(i)
            hump_dict[new_key] = hump_dict[i]
            if new_key != i:
                del hump_dict[i]
        return hump_dict
    return hump_dict
