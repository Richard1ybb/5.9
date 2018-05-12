# encoding:utf-8

import inspect
from collections import OrderedDict
import random
import string


def singleton(cls):
    """单例模式装饰器
    :param cls:
    :return:
    """
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton


def singleton_with_parameters(cls):
    """检查参数的单例模式装饰器,与singleton的区别为: 相同的初始化参数为同一个实例
    :param cls:
    :return:
    """
    instances = {}

    def _singleton(*args, **kwargs):
        key = frozenset(inspect.getcallargs(cls.__init__, *args, **kwargs).items())
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]
    return _singleton


class SingletonIfSameParameters(type):
    """如果初始化参数一致，则单实例"""

    _instances = {}
    _init = {}

    def __init__(cls, name, bases, dct):
        cls._init[cls] = dct.get('__init__', None)

    def __call__(cls, *args, **kwargs):
        init = cls._init[cls]
        if init is not None:
            key = (cls, args, repr(OrderedDict(kwargs.items())))
        else:
            key = cls
        if key not in cls._instances:
            cls._instances[key] = super(SingletonIfSameParameters, cls).__call__(*args, **kwargs)
        return cls._instances[key]


def gen_rand_str(length=8, s_type='hex', prefix=None, postfix=None):
    """生成指定长度的随机数，可设置输出字符串的前缀、后缀字符串
    :param length: 随机字符串长度
    :param s_type:
    :param prefix: 前缀字符串
    :param postfix: 后缀字符串
    :return:
    """
    if s_type == 'digit':
        formatter = "{:0" + str(length) + "}"
        mid = formatter.format(random.randrange(10**length))
    elif s_type == 'ascii':
        mid = "".join([random.choice(string.ascii_letters) for _ in range(length)])
    elif s_type == "hex":
        formatter = "{:0" + str(length) + "x}"
        mid = formatter.format(random.randrange(16**length))
    else:
        mid = "".join([random.choice(string.ascii_letters+string.digits) for _ in range(length)])
    if prefix is not None:
        mid = prefix + mid
    if postfix is not None:
        mid = mid + postfix
    return mid
