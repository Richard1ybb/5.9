# encoding:utf-8

import os
import configparser


def readconfig():
    config = configparser.RawConfigParser()
    file_path = "C:\\Users\\Summer\\PycharmProjects\\5.9\\main\\init.conf"
    # file_path = os.path.abspath(os.path.dirname(os.getcwd())) + "\\5.9\\main\\init.conf"
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
        return cf.get('target_url', 'url')

    @property
    def host(self):
        return cf.get('MySQL', 'host')

    @property
    def username(self):
        return cf.get('MySQL', 'username')

    @property
    def password(self):
        return cf.get('MySQL', 'password')

    @property
    def port(self):
        return cf.getint('MySQL', 'port')

    @property
    def database(self):
        return cf.get('MySQL', 'database')

    @property
    def firefox(self):
        return cf.get('webdriver_path', 'Firefox')

    @property
    def chrome(self):
        return cf.get('webdriver_path', 'chrome')

    @property
    def ie(self):
        return cf.get('webdriver_path', 'ie')

    @property
    def depth(self):
        return cf.get('depth', 'depth')

    @property
    def timeout(self):
        return cf.getint('load_timeout', 'timeout')


Services = _Services()









