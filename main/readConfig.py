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


class _Write(object):
    def __init__(self, path):
        self.config = configparser.RawConfigParser()
        self.f_path = path
        self.config.read(self.f_path)

    def __del__(self):
        with open(self.f_path, 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

    def set_url(self, url):
        self.config.set('target_url', 'url', url)

    def set_host(self, host):
        self.config.set('MySQL', 'host', host)

    def set_username(self, username):
        self.config.set('MySQL', 'username', username)

    def set_password(self, password):
        self.config.set('MySQL', 'password', password)

    def set_port(self, port):
        self.config.set('MySQL', 'port', port)

    def set_database(self, database):
        self.config.set('MySQL', 'database', database)

    def set_driver_path(self, driver_path):
        self.config.set('webdriver_path', 'Firefox', driver_path)

    def set_timeout(self, timeout):
        self.config.set('load_timeout', 'timeout', timeout)


Services = _Services()


