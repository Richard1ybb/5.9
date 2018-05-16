# encoding:utf-8

from main.parse_html import Drivers, Parser, MySQLSingle
from main.utils import gen_rand_str
from main.readConfig import Services
from main.log import logger


class Main(Parser):
    def __init__(self):
        super(Main, self).__init__(a="firefox")

    def produce_test_case(self, length):
        for i in range(length):
            if i == 0:
                urls = [Services.url]
                MySQLSingle().first_data(urls[0])
            else:
                urls = MySQLSingle.select_url_from_content()
            for ur in urls:
                self.all_aa(url=ur, layer_number=i + 1)

        self.close_connect()

    def check_xpath(self, dr):
        """检查xpath并入库"""
        if dr in ['firefox', 'chrome', 'ie']:
            obj = Parser(dr)
            page = obj.parser_by_lxml()
            tag = obj.tag_a_has_href(page)
            obj.get_xpath(page=page, tag=tag)
            for i in range(len(obj.Xpath_list)):
                try:
                    obj.driver.find_element_by_xpath(xpath=obj.Xpath_list[i]).click()
                    if obj.driver.current_url == obj.current_url:
                        continue
                    else:
                        obj.new_url.append(obj.driver.current_url)
                        all_handles = obj.driver.window_handles
                        main_handle = obj.driver.current_window_handle
                        for handle in all_handles:
                            if handle != obj.driver.current_window_handle:
                                obj.driver.switch_to_window(handle)
                                obj.driver.close()
                        obj.driver.switch_to_window(main_handle)
                        logger.info("back to " + obj.driver.current_url)

                except:
                    del obj.Xpath_list[i]
                    logger.warning('delete wrong xpath')
                    pass
                obj.update_current_url()
                params = (gen_rand_str(length=8, s_type='digit'), obj.driver.current_url, obj.Xpath_list[i])
                self.insert_one_to_xpath(params)

        else:
            logger.warning('wrong driver, only for firefox, chrome, ie!')


if __name__ == "__main__":
    a = Main()
    a.produce_test_case(length=3)









