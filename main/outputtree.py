# encoding:utf-8

import networkx as nx
import matplotlib.pyplot as plt
from main.log import logger
from main.parse_html import MySQLSingle

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


class Report(object):
    def __init__(self):
        self.G = nx.Graph()
        self.mysql = MySQLSingle()

    def draw_and_output(self):
        """
        树状图参数设置及输出
        :param pic:
        :return:
        """
        option = {'with_labels': True,
                  'font_size': 3,
                  'font_weight': 'bold',
                  'node_color': '#EEE685',
                  'node_size': 200,
                  'width': 2
                  }
        nx.draw(self.G, nx.spring_layout(self.G), **option)
        plt.savefig('test_report.png')
        plt.show()

    def make_data(self):
        urls = self.mysql.select_url()
        for i in urls:
            data = list()
            text = self.mysql.select_text(i)
            for ii in text:
                li = list()
                li.append(i)
                id_text = str(ii[0])+str(ii[1])
                li.append(id_text)
                tu = tuple(li)
                data.append(tu)
            logger.info("add_edges:" + str(data))
            self.G.add_edges_from(data)

    def add_edges_for_lost(self):
        text = self.mysql.select_id_text_point_url()
        data = list()
        for ii in text:
            li = list()
            id_text = str(ii[0]) + str(ii[1])
            li.append(id_text)
            li.append(ii[2])
            tu = tuple(li)
            data.append(tu)
        logger.info("add_edges_for_lost:" + str(data))
        self.G.add_edges_from(data)


if __name__ == '__main__':
    RE = Report()
    RE.make_data()
    RE.add_edges_for_lost()
    RE.draw_and_output()

