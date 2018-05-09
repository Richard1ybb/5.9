# encoding:utf-8

from main.parse_html import Drivers, Parser


class Main:
    def check_xpath():
        obj = Parser("firefox")
        page = obj.parser_by_lxml()
        tag = obj.tag_a_has_href(page)
        obj.get_xpath(page=page, tag=tag)
        for xpath in obj.Xpath_list:
            try:
                obj.driver.find_element_by_xpath(xpath=xpath).click()
            except Exception as e:
                print(e)
                pass




