# !/usr/bin/env python
# coding=utf8

import os
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.netutil
from tornado.options import define, options

debug_mode=True

define('port', default=8888, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

HANDLERS = [
    ('/', IndexHandler)

]

settings = {
    'debug': debug_mode,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
}


def main():
    # 转换命令行参数，并将转换后的值对应的设置到全局options对象相关属性上。追加命令行参数的方式是--myoption=myvalue
    # 当我们在代码中调用parse_command_line()或者parse_config_file()的方法时，tornado会默认为我们配置标准logging模块，即默认开启了日志功能，并向标准输出（屏幕）打印日志信息。
    tornado.options.parse_command_line()
    application = tornado.web.Application(HANDLERS, **settings)
    if settings['debug']:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    else:
        sockets = tornado.netutil.bind_sockets(options.port)
        tornado.process.fork_processes(0)
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.add_sockets(sockets)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
    

