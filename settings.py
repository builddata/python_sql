# -*- coding: utf-8 -*-
"""
settings——

"""
# settings.py

# settings.py文件下添加mysql的配置信息
MY_SETTINGS = {
    "host": "localhost",
    "user": "root",
    "passwd": "sunboy",
    "db": "test1",
    "port": 3306,
    "charset": "utf8",
    'use_unicode': True,
}
# 找到settings文件内ITEM_PIPELINES 让这个pipelines生效
ITEM_PIPELINES = {
   'Ccxi_Spider.pipelines.SaveToMysqlAsynPipeline': 300,
}

