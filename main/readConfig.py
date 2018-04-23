#encoding:utf-8

import os
import configparser

def readconfig():
    config = configparser.RawConfigParser()
    file_path = os.path.abspath(os.path.dirname(os.getcwd())) + "\init.cfg"
    config.read(file_path)
    return config

# a_float = config.getfloat('Section1', 'a_float')
# an_int = config.getint('Section1', 'an_int')
# print a_float + an_int
#
# # Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# # This is because we are using a RawConfigParser().
# if config.getboolean('Section1', 'a_bool'):
#     print config.get('Section1', 'foo')


class _Services:
    class TargetUrl:
        @property
        def url(self):
            return readconfig().get('target_url', 'url')


    class Mysql:
        @property
        def host(self):
            return readconfig().get('MySQL', 'host')

        @property
        def username(self):
            return readconfig().get('MySQL', 'name')

        @property
        def password(self):
            return readconfig().get('MySQL', 'password')

        @property
        def port(self):
            return readconfig().get('MySQL', 'port')

    class WebdriverPath:
        @property
        def firefox(self):
            return readconfig().get('webdriver_path', 'Firefox')

        @property
        def chrome(self):
            return readconfig().get('webdriver_path', 'chrome')

        @property
        def ie(self):
            return readconfig().get('webdriver_path', 'ie')

    class Depth:
        @property
        def depth(self):
            return readconfig().get('depth', 'depth')


Services = _Services()









