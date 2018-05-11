# encoding:utf-8

from main.parse_html import Drivers, Parser, MySQLSingle
from main.utils import gen_rand_str

class Main(MySQLSingle):
    def __init__(self):
        super(Main, self).__init__()

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
                        obj.driver.back()
                except:
                    del obj.Xpath_list[i]
                    print('delete wrong xpath')
                    pass
                obj.update_current_url()
                params = (gen_rand_str(length=8, s_type='digit'), obj.driver.current_url, obj.Xpath_list[i])
                self.insert_one_to_xpath(params)
            
        else:
            print('wrong driver, only for firefox, chrome, ie!')














