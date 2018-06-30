# encoding: utf-8

from tkinter import *
import tkinter.filedialog
from main.readConfig import _Write
from main.ma import *


class App(object):
    def __init__(self):
        self.driver_path = None
        self.browser = None
        self.root = Tk()
        self.root.title('Web自动化测试系统')
        # self.root.geometry('800x400')
        # self.title = Label(self.root, text="Web自动化测试系统", font=('Arial', 18), width=30, height=2).grid(row=0)

        Label(self.root, text="配置中心", font=('Arial', 15)).grid(row=1, column=0, columnspan=1)
        self.Config = Frame(self.root, width=10, height=10)
        self.target_url = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.target_url.grid(row=2, column=1, columnspan=1)
        Label(self.Config, text='目标站点', width=10, font=('Verdana', 13)).grid(row=2, column=0, columnspan=1)

        # MySQL参数
        Label(self.Config, text='MySQL参数', font=('Arial', 15)).grid(row=3, column=0, columnspan=1)

        # host
        Label(self.Config, text='HOST', width=10, font=('Verdana', 13)).grid(row=4, column=0, columnspan=1)
        self.host = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.host.grid(row=4, column=1, columnspan=1)

        # username
        Label(self.Config, text='USERNAME', width=10, font=('Verdana', 13)).grid(row=5, column=0, columnspan=1)
        self.username = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.username.grid(row=5, column=1, columnspan=1)

        # passward
        Label(self.Config, text='PASSWORD', width=10, font=('Verdana', 13)).grid(row=6, column=0, columnspan=1)
        self.password = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.password.grid(row=6, column=1, columnspan=1)

        # port
        Label(self.Config, text='PORT', width=10, font=('Verdana', 13)).grid(row=7, column=0, columnspan=1)
        self.port = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.port.grid(row=7, column=1, columnspan=1)

        # database
        Label(self.Config, text='DATABASE', width=10, font=('Verdana', 13)).grid(row=8, column=0, columnspan=1)
        self.database = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.database.grid(row=8, column=1, columnspan=1)

        # 浏览器选择及驱动
        Label(self.Config, text='浏览器选择及驱动', font=('Arial', 15)).grid(row=9, column=0, columnspan=1)

        Label(self.Config, text='Browser', width=10, font=('Verdana', 13)).grid(row=10, column=0, columnspan=1)
        self.Browser = Frame(self.Config)
        Button(self.Browser, text="FireFox", width=5, font=('Verdana', 11), command=self.chose_firefox).grid(row=0,
                                                                                                             column=0,
                                                                                                             columnspan=1)
        Button(self.Browser, text="Chrome", width=5, font=('Verdana', 11), command=self.chose_chrome).grid(row=0,
                                                                                                           column=1,
                                                                                                           columnspan=1)
        Button(self.Browser, text="IE", width=5, font=('Verdana', 11), command=self.chose_ie).grid(row=0, column=2,
                                                                                                   columnspan=1)
        self.Browser.grid(row=10, column=1, columnspan=1)

        Label(self.Config, text='Driver Path', width=10, font=('Verdana', 13)).grid(row=11, column=0, columnspan=1)
        self.Path = Frame(self.Config)
        Button(self.Path, text="选择文件", command=self.xz, width=5, font=('Verdana', 13)).grid(row=0, column=0,
                                                                                            columnspan=1)
        self.lb = Label(self.Path, text='', width=30, height=3, wraplength=280, font=('Verdana', 13))
        self.lb.grid(row=0, column=1, columnspan=2)
        self.Path.grid(row=11, column=1, columnspan=2)

        # timeout
        Label(self.Config, text='超时时间', font=('Arial', 15)).grid(row=12, column=0, columnspan=1)

        Label(self.Config, text='Time Out', width=10, font=('Verdana', 13)).grid(row=13, column=0, columnspan=1)
        self.timeout = Entry(self.Config, textvariable=StringVar(), width=20, font=('Verdana', 15))
        self.timeout.grid(row=13, column=1, columnspan=1)

        # 默认设置
        Button(self.Config, text="恢复默认", command=self.change_default, width=8, height=5, font=('Verdana', 15)).grid(row=14,
                                                                                                            column=0,
                                                                                                            columnspan=2)
        Button(self.Config, text="修改配置", command=self.change_config, width=8, height=5, font=('Verdana', 15)).grid(row=14,
                                                                                                             column=1,
                                                                                                             columnspan=2)

        self.Config.grid(row=2, column=1, columnspan=3)

        # self.create = Frame(self.root)
        self.create = Frame(self.root)

        Label(self.create, text="生成用例", font=('Arial', 15)).grid(row=0, column=0, columnspan=1)

        Button(self.create, text="Run", command=self.run, width=8, font=('Verdana', 15)).grid(row=0, column=1)
        Button(self.create, text="Stop", command=self.stop, width=8, font=('Verdana', 15)).grid(row=0, column=2)

        Label(self.create, text='测试用时', font=('Arial', 15)).grid(row=1, column=0, columnspan=1)
        self.use_time = Text(Frame(self.create))
        self.use_time.grid(row=1, column=1, columnspan=1)

        Label(self.create, text='生成测试用例数', font=('Arial', 15)).grid(row=2, column=0, columnspan=1)
        self.case_num = Text(Frame(self.create))
        self.case_num.grid(row=2, column=1, columnspan=1)

        Label(self.create, text="测试用例树状图", font=('Arial', 15)).grid(row=3, column=0, columnspan=1)

        Button(self.create, text="Report", command=self.run, width=8, font=('Verdana', 15)).grid(row=3, column=1,
                                                                                                 columnspan=1)
        Button(self.create, text="Quit", command=self.stop, width=8, font=('Verdana', 15)).grid(row=3, column=2,
                                                                                                columnspan=1)

        self.create.grid(row=0, column=4, columnspan=1, rowspan=3)

        self.root.mainloop()

    def chose_firefox(self):
        self.browser = "firefox"

    def chose_chrome(self):
        self.browser = "chrome"

    def chose_ie(self):
        self.browser = "ie"

    def xz(self):
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            self.lb.config(text=filename)
            self.driver_path = filename
        else:
            self.lb.config(text="您没有选择任何文件")

    def change_default(self):
        write = _Write('/Users/ybbrichard/PycharmProjects/5.9/main/init.conf')
        self.target_url.delete(0, END)
        self.target_url.insert(0, 'https://www.dji.com/cn')
        write.set_url('https://www.dji.com/cn')

        self.host.delete(0, END)
        self.host.insert(0, 'localhost')
        write.set_host('localhost')

        self.username.delete(0, END)
        self.username.insert(0, 'root')
        write.set_username('root')

        self.password.delete(0, END)
        self.password.insert(0, '12345')
        write.set_password('12345')

        self.port.delete(0, END)
        self.port.insert(0, '3306')
        write.set_port('3306')

        self.database.delete(0, END)
        self.database.insert(0, 'test2')
        write.set_database('test2')

        self.lb.config(text="默认路径")
        write.set_driver_path('C:\\Users\\Summer\\Desktop\\geckodriver.exe')

        self.timeout.delete(0, END)
        self.timeout.insert(0, '20')
        write.set_timeout('20')
        del write

    def change_config(self):
        write = _Write('/Users/ybbrichard/PycharmProjects/5.9/main/init.conf')
        write.set_url(self.target_url.get())
        write.set_host(self.host.get())
        write.set_username(self.username.get())
        write.set_password(self.password.get())
        write.set_port(self.port.get())
        write.set_database(self.database.get())
        write.set_driver_path(self.driver_path)
        write.set_timeout(self.timeout.get())
        del write

    def run(self):
        pass

    def stop(self):
        pass


App()

