#!/usr/bin/python3
#coding=utf8

import esm


def test():
    string="哎呀，今天在楼下看到了宝马，我老家倒是有养马的，以前的邻居有个奔驰，不对是保时捷，大爷的，都是马"
    index = esm.Index()
    index.enter("宝马")
    index.enter("马")
    index.enter("奔腾")
    index.enter("保时捷")
    index.fix()
    data = index.query(string)
    print(data)
    

if __name__ == '__main__':
    test()
