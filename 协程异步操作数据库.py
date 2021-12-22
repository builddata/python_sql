# -*- coding: utf-8 -*-
"""
协程异步操作数据库

"""



# !/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import gevent
import pymysql
from gevent import monkey
 
# 堵塞标记
monkey.patch_all()
 
 
class SqlSave(object):
    """协程方式写入数据库"""
     
    def __init__(self):
        self.conn = pymysql.connect(host="localhost",user="root",password="sunboy",
                                    database="test1",charset="utf8")
        self.cursor = self.conn.cursor()
     
    def process_item(self):
        sql = self.__get_sql()
        # 协程对数据库操作
        print (999)
        gevent.joinall([
            gevent.spawn(self.__go_sql, sql),
        ])
     
    def __go_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    def __get_sql(self):
        
        # 测试数据
        return "create table MyClass(id int(4) not null primary key auto_increment,\
              name char(20) not null,\
              sex int(4) not null default '0',\
              degree double(16,2))"
 
if __name__ == '__main__':
    s = SqlSave()
    s.process_item()
  
    
    
    
    
    
    