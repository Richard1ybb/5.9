# encoding:utf-8

import inspect
from collections import OrderedDict

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
