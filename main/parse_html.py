# encoding:utf-8

from selenium import webdriver
from main.readConfig import Services
from lxml import etree
from functools import wraps
import mysql.connector
from main.utils import gen_rand_str


def singleton(cls):
    """
    单实例模式
    :param cls:
    :return:
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return get_instance


# 数据库连接实例
@singleton
class MySQLSingle(object):
    def __init__(self, conn=''):
        self.conn = conn
        self.get_conn()

    def get_conn(self):
        try:
            self.conn = mysql.connector.connect(host=Services.Mysql.host,
                                                port=Services.Mysql.port,
                                                user=Services.Mysql.username,
                                                password=Services.Mysql.password,
                                                database=Services.Mysql.database,
                                                charset='utf8'
                                                )
        except Exception as e:
            print('File to connect database: %s' % e)
        return self.conn

    def end_conn(self):
        """关闭连接"""
        self.conn.close()

    def insert_one_to_xpath(self, params):
        """xpath表中插入一条数据"""
        sql = "INSERT INTO xpath (id, url, xpath) VALUES(%d, %s, %s)"
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_one_to_relation(self, params):
        """relation表中插入数据"""
        sql = "INSERT INTO relation (layer_number, id, last_id, title, text) VALUES(%d, %s, %d, %s, %s)"
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_many_to_relation(self, params):
        sql = "INSERT INTO relation (layer_number, id, last_id, title, text) VALUES(%d, %s, %d, %s, %s)"
        try:
            # 执行sql语句
            self.conn.cursor().executemany(sql, params)
            # 提交到数据库执行
            self.conn.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.conn.rollback()

# TODO


class Drivers(object):
    """firefox,ie,chrome驱动"""
    def __init__(self):
        self.url = Services.TargetUrl.url
        self.driver = None

    @staticmethod
    def _firefox_driver():
        driver = webdriver.Firefox(executable_path=Services.WebdriverPath.firefox)
        return driver

    @staticmethod
    def _chrome_driver():
        driver = webdriver.Chrome(executable_path=Services.WebdriverPath.chrome)
        return driver

    @staticmethod
    def _ie_driver():
        driver = webdriver.Ie(executable_path=Services.WebdriverPath.ie)
        return driver


class Parser(Drivers):
    def __init__(self, a):
        super(Parser, self).__init__()
        if a.lower() == "firefox":
            self.driver = self._firefox_driver()
        elif a.lower() == "chrome":
            self.driver = self._chrome_driver()
        elif a.lower() == "ie":
            self.driver = self._ie_driver()
        else:
            raise ValueError("Wrong driver！Only for: firefox, chrome, ie.")
        self.current_url = None
        self.current_window_handle = None
        self.Xpath_list = list()
        self.number = 1
        self.new_url = list()
        self.mysql = MySQLSingle()

    def _driver_open_url(self, url):
        """
        打开一个URL
        :param url:
        :return:
        """
        self.driver.get(url=url)
        self._update_current_url()

    @property
    def _parser_by_xml(self):
        """
        将复杂HTML文档转换成树形结构
        :param driver: webdriver对象
        :return: 结构树对象
        """
        html = self.driver.page_source
        page = etree.HTML(html)
        return page

    @staticmethod
    def _tag_a_has_href(page):
        """
        提取可操作a标签
        :param page: 结构树对象
        :return: 目标a标签
        """
        tag_a = page.xpath(u'//a')
        tag_has_href = list()
        for a in tag_a:
            if "href" in a.attrs:
                tag_has_href.append(a)
        return tag_has_href

    def _extract_xpath_from_page(self, page, tag):
        """
        提取Xpath列表
        :param page: 结构树对象
        :param tag: 目标tag
        :return:
        """
        tree = etree.ElementTree(page)
        for e in tag:
            self.Xpath_list.append(tree.getpath(e))

    def _get_xpath(self, page, tag):
        """获取xpath"""
        # page = self._parser_by_xml()
        # tag = self._tag_a_has_href(page=page)
        self._extract_xpath_from_page(page=page, tag=tag)
        self.number = self.number + 1

    def _update_current_url(self):
        """更新当前URL"""
        self.current_url = self.driver.current_url

    def _update_current_windows_handle(self):
        """更新窗口句柄"""
        self.current_window_handle = self.driver.current_window_handle

    def all_aa(self, url):
        self._driver_open_url(url)
        page = self._parser_by_xml()
        tag = self._tag_a_has_href(page)
        self._get_xpath(page=page, tag=tag)
        for i in range(len(self.Xpath_list)):
            try:
                self.driver.find_element_by_xpath(xpath=self.Xpath_list[i]).click()
                if self.driver.current_url == self.current_url:
                    continue
                else:
                    self.new_url.append(self.driver.current_url)
                    self.driver.back()
            except:
                del self.Xpath_list[i]
                print('del wrong xpath')
                pass
            params = (gen_rand_str(length=8, s_type='digit'), self.driver.current_url, self.Xpath_list[i])
            self.mysql.insert_one_to_xpath(params)
        self.mysql.insert_one_to_relation()




















