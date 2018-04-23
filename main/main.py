#encoding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from main.readConfig import Services
from bs4 import BeautifulSoup

class Drivers(object):
    """firefox,ie,chrome驱动"""
    def __init__(self):
        self.url = Services.TargetUrl.url
        self.goal = dict()

    def firefox_driver(self):
        driver = webdriver.Firefox(executable_path=Services.WebdriverPath.firefox)
        driver.get(self.url)
        return driver

    def chrome_driver(self):
        driver = webdriver.Chrome(executable_path=Services.WebdriverPath.chrome)
        driver.get(self.url)
        return driver

    def ie_driver(self):
        driver = webdriver.Ie(executable_path=Services.WebdriverPath.ie)
        driver.get(self.url)
        return driver


class Parser(Drivers):
    def __init__(self, **kwargs):
        super(Parser, self).__init__()

    @property
    def parser_lxml(self, driver):
        """
        将复杂HTML文档转换成一个复杂的树形结构
        :param driver: webdriver对象
        :return: 结构树对象
        """
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        return soup

    @property
    def tag_a_has_href(self, soup):
        """提取可操作a标签"""
        tag_a = soup("a")
        for a in tag_a:
            if "href" in a.attrs:
                return a

    @property
    def














