# encoding:utf-8

import os
import configparser


def readconfig():
    config = configparser.RawConfigParser()
    file_path = "C:\\Users\\Summer\\PycharmProjects\\5.9\\main\\init.conf"
    #file_path = os.path.abspath(os.path.dirname(os.getcwd())) + "\\5.9\\main\\init.conf"
    config.read(file_path)
    return config


cf = readconfig()

# a_float = config.getfloat('Section1', 'a_float')
# an_int = config.getint('Section1', 'an_int')
# print a_float + an_int
#
# # Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# # This is because we are using a RawConfigParser().
# if config.getboolean('Section1', 'a_bool'):
#     print config.get('Section1', 'foo')


class _Services:

    @property
    def url(self):
        print(cf.get('target_url', 'url'))
        return cf.get('target_url', 'url')

    @property
    def host(self):
        return cf.get('MySQL', 'host')

    @staticmethod
    def userame():
        print(cf.get('MySQL', 'name'))
        return cf.get('MySQL', 'name')

    @staticmethod
    def password():
        return cf.get('MySQL', 'password')

    @staticmethod
    def port():
        return cf.getint('MySQL', 'port')

    @staticmethod
    def database():
        return cf.get('MySQL', 'database')


    @staticmethod
    def firefox():
        return cf.get('webdriver_path', 'Firefox')

    @staticmethod
    def chrome():
        return cf.get('webdriver_path', 'chrome')

    @staticmethod
    def ie():
        return cf.get('webdriver_path', 'ie')


    @staticmethod
    def depth():
        return cf.get('depth', 'depth')


Services = _Services()









