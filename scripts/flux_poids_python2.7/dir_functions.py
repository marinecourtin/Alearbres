#! usr/bin/python
# coding: utf-8

import os


def mkdir(path):
    path=path.strip()
    # 去除尾部 \ 符号
    # path=path.rstrip("\\")
    isExists=os.path.exists(path)

    if not isExists:
        # 如果不存在则创建目录
        print path+u' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+u' 目录已存在'
        return False