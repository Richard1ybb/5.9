# encoding:utf-8

from selenium import webdriver
import selenium
from main.readConfig import Services
from lxml import etree
from functools import wraps
import pymysql
import mysql.connector
from main.utils import gen_rand_str
from main.log import logger
from selenium.common import exceptions


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
    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        logger.info("connecting to mysql...")
        logger.info((Services.host, Services.port, Services.username, Services.password, Services.database))
        try:
            self.conn = mysql.connector.connect(host=Services.host,
                                                port=Services.port,
                                                user=Services.username,
                                                password=Services.password,
                                                database=Services.database,
                                                charset='utf8'
                                                )
            self.conn.autocommit = True

            # self.conn = pymysql.connect(host=Services.host,
            #                             port=Services.port,
            #                             user=Services.username,
            #                             password=Services.password,
            #                             database=Services.database,
            #                             charset='utf8'
            #                             )
        except Exception as e:
            logger.warning('File to connect database: %s' % e)
            logger.warning('stop')
            pass
        return self.conn

    def end_conn(self):
        """关闭连接"""
        self.conn.close()
        logger.info("close connect")

    def first_data(self, urls):
        """初始化数据"""
        logger.info("first_data")
        sql = "INSERT INTO content (layer_number, url, status) VALUES (%s, '%s', %s)" % (0, urls, 'true')
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("first_data success")

        except Exception as e:
            logger.warning("first_data fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_one_to_xpath(self, params):
        """xpath表中插入一条数据"""
        logger.info("insert_one_to_xpath " + str(params))
        sql = "INSERT INTO xpath (id, url, xpath, point_url) VALUES(%s, %s, %s, %s)"
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("insert_one_to_xpath success")

        except Exception as e:
            logger.warning("insert_one_to_xpath fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_one_to_relation(self, params):
        """
        relation表中插入一条数据
        :param params:
        :return:
        """
        logger.info("insert_one_to_relation " + str(params))
        sql = "INSERT INTO relation (layer_number, id, title, text) VALUES(%s, %s, %s, %s)"
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("insert_one_to_relation success")

        except Exception as e:
            logger.warning("insert_one_to_relation fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_many_to_relation(self, params):
        """
        relation表中插入多条数据
        :param params:
        :return:
        """
        logger.info("insert_many_to_relation " + str(params))
        sql = "INSERT INTO relation (layer_number, id, title, text) VALUES(%s, %s, %s, %s)"
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("insert_many_to_relation success")

        except Exception as e:
            logger.warning("insert_many_to_relation fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

    def insert_many_to_content(self, params):
        """
        content表中插入多条数据(url, father_url, layer_number)
        :param params:
        :return:
        """
        for p in params:
            self.insert_one_to_content(p)

    def insert_one_to_content(self, params):
        """
        content表中插入多条数据(url, father_url, layer_number)
        :param params:
        :return:
        """
        logger.info("insert_many_to_content " + str(params))
        sql = "INSERT INTO content (url, father_url, layer_number) VALUES(%s, %s, %s)"
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql, params)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("insert_many_to_content success")

        except mysql.connector.IntegrityError as e:
            # 唯一性约束去重
            logger.warning("have same url, lose it: %s" % e)

        except mysql.connector.Error as e:
            logger.warning("insert_many_to_content fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

# TODO
    def update_html_to_content(self, url, html):

        pass

        # html = str(html.encode(encoding='UTF-8', errors='strict'))
        # logger.info("insert_html_into_content" + ' url:' + url + ' html:' + html)
        # sql = "UPDATE content SET content = %s WHERE url = %s"
        # logger.debug('sql:' + sql)
        # params = (html, url)
        # try:
        #     # 执行sql语句
        #     self.conn.cursor().execute(sql, params)
        #     # 提交到数据库执行
        #     # self.conn.commit()
        #     logger.info("update_html_to_content success")
        #
        # except Exception as e:
        #     logger.warning("update_html_to_content fail: %s" % e)
        #     # 发生错误时回滚
        #     self.conn.rollback()

    def update_true_status_to_content(self, url):
        logger.info("update_true_status_to_content" + ' url:' + str(url))
        sql = "UPDATE content SET status = TRUE WHERE url = '%s'" % url
        logger.debug('sql:' + sql)
        try:
            # 执行sql语句
            self.conn.cursor().execute(sql)
            # 提交到数据库执行
            # self.conn.commit()
            logger.info("update_true_status_to_content success")

        except Exception as e:
            logger.warning("update_true_status_to_content fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()

    def select_url_from_content(self):
        logger.info("select_url_from_content...")
        sql = "select url from content WHERE status = false"
        logger.debug('sql:' + sql)
        a = list()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            for i in data:
                a.append(i[0])
            logger.info("select_url_from_content success")

        except Exception as e:
            logger.warning("select_url_from_content fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()
        return a

    def select_url(self):
        logger.info("select_distinct_url_from_xpath...")
        sql = "select distinct url from xpath"
        a = list()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            for i in data:
                a.append(i[0])
            logger.info("select point_url from_xpath success")

        except Exception as e:
            logger.warning("select_point_url_from_content fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()
        return a

    def select_text(self, url):
        logger.info("select text...")
        sql = "select relation.id,relation.text from relation,xpath where relation.id = xpath.id and xpath.url = '%s'" % url
        a = list()
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            logger.info("select text success")

        except Exception as e:
            logger.warning("select_text fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()
        return data

    def select_id_text_point_url(self):
        logger.info("select_id_text_point_url...")
        sql = "select x.id, r.text, x.point_url from xpath as x,relation as r where x.id = r.id"
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            logger.info("select text success")

        except Exception as e:
            logger.warning("select_text fail: %s" % e)
            # 发生错误时回滚
            self.conn.rollback()
        return data


class Drivers(object):
    """firefox,ie,chrome驱动"""
    def __init__(self):
        self.url = Services.url
        self.driver = None

    @staticmethod
    def _firefox_driver():
        driver = webdriver.Firefox(executable_path=Services.firefox)
        driver.set_page_load_timeout(Services.timeout)
        return driver

    @staticmethod
    def _chrome_driver():
        driver = webdriver.Chrome(executable_path=Services.chrome)
        driver.set_page_load_timeout(Services.timeout)
        return driver

    @staticmethod
    def _ie_driver():
        driver = webdriver.Ie(executable_path=Services.ie)
        driver.set_page_load_timeout(Services.timeout)
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
            logger.warning("Wrong driver！Only for: firefox, chrome, ie.")
            raise ValueError("Wrong driver！Only for: firefox, chrome, ie.")
        self.current_url = None
        self.current_window_handle = None
        self.Xpath_list = list()
        self.number = 1
        self.new_url = list()
        self.mysql = MySQLSingle()

    def _check_useful_url(self, url):
        """
        检查URL
        :return:
        """
        try:
            logger.info("check url: " + str(url))
            self.driver.get(url=url)
            logger.info("useful url: " + str(url))
            return True
        except selenium.common.exceptions.TimeoutException as e:
            logger.warning("Unuseful url: " + str(url))
            return False

        # except exceptions.InvalidArgumentException as e:
        #     logger.warning("Unuseful url: " + str(url))
        #     return False
        # except exceptions.TimeoutException as e:
        #     logger.warning("Timeout url: " + str(url))
        #     return False

    def _driver_open_url(self, url):
        """
        打开一个URL
        :param url:
        :return:
        """
        try:
            logger.info("open url: " + str(url))
            self.driver.get(url=url)
            logger.info("current url :" + self.driver.current_url)
        except selenium.common.exceptions as e:
            logger.warning("open url: %s fail" % url)
            logger.warning("error:" + e)
        self._update_current_url()

    def _parser_by_xml(self):
        """
        将复杂HTML文档转换成树形结构
        :param driver: webdriver对象
        :return: 结构树对象
        """
        html = self.driver.page_source
        page = etree.HTML(html)
        return page, html

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
            if "href" in a.attrib:
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

    def close_connect(self):
        self.mysql.end_conn()

    def get_back_to_init(self):
        self.current_url = None
        self.current_window_handle = None
        self.Xpath_list = list()
        self.new_url = list()

    def all_aa(self, url, layer_number):
        xpath = list()
        self._driver_open_url(url)
        page, html = self._parser_by_xml()
        self.mysql.update_html_to_content(url=url, html=html)
        tag = self._tag_a_has_href(page)
        text = [a.text for a in tag]
        main_handle = self.driver.current_window_handle
        self._get_xpath(page=page, tag=tag)
        while len(self.Xpath_list) > 0:
            xp = self.Xpath_list.pop()
            te = text.pop()
            logger.debug("len_of_list: " + str(len(self.Xpath_list)))
            logger.debug("xpath:" + str(xp))
            try:
                element = self.driver.find_element_by_xpath(xpath=xp)
            except selenium.common.exceptions.NoSuchElementException as e:
                logger.warning(str(e))
                continue
            if element.is_enabled() is True:
                try:
                    element.click()
                    xpath.append(xp)
                    if self.driver.current_url == self.current_url:
                        continue
                    else:
                        xpath_url = self.driver.current_url
                        self.new_url.append(self.driver.current_url)
                        all_handles = self.driver.window_handles
                        if len(all_handles) > 1:
                            for handle in all_handles:
                                if handle != main_handle:
                                    try:
                                        self.driver.switch_to.window(handle)
                                        self.driver.close()
                                        logger.debug("close window: " + str(handle))
                                    except selenium.common.exceptions.NoSuchWindowException as e:
                                        logger.warning("selenium.common.exceptions.NoSuchWindowException: " + str(e))

                            self.driver.switch_to.window(main_handle)
                            logger.info("back to main_handle")
                        elif len(all_handles) == 1:
                            self.driver.back()
                        else:
                            raise ValueError("window_handle wrong")
                except:
                    logger.info('throw wrong xpath')
                    continue
            else:
                logger.info('throw wrong xpath')
                continue
            uid = int(gen_rand_str(length=7, s_type='digit'))
            logger.debug('(uid, self.driver.current_url, self.Xpath_list[i], self.driver.current_url):' + str(uid) +
                         self.driver.current_url + str(xp) + self.driver.current_url)
            self.mysql.insert_one_to_xpath((uid, url, str(xp), xpath_url))
            self.mysql.insert_one_to_relation((layer_number, uid, self.driver.title, te))
        url_list = list()
        while self.new_url:
            u = self.new_url.pop()
            if self._check_useful_url(u):
                url_list.append(u)
                logger.info("append to url_list: " + str(u))
            else:
                pass
        params = [(Url, url, layer_number) for Url in url_list]
        logger.debug(url_list)
        print(params)
        self.mysql.insert_many_to_content(params=params)
        self.mysql.update_true_status_to_content(url=url)

        self.get_back_to_init()





















