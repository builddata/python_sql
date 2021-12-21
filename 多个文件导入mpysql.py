# -*- coding: utf-8 -*-
"""
多个文件导入mpysql

"""

import  pymysql,os,time

config = {'host':'localhost',
          'port':3306,
          'user':'root',
          'passwd':'sunboy',
          'charset':'utf8mb4',
          'local_infile':1
          }

conn = pymysql.connect(**config)
cur = conn.cursor()

def load_csv(csv_file_path,table_name,csv_filename,database='test1'):
    #打开csv文件
    file = open(csv_file_path+csv_filename, 'r',encoding='utf-8')
    #读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
   
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),' #varchar可变长字符串
    colum = colum[:-1]
    #编写sql，create_sql负责创建表，data_sql负责导入数据 
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "load data local infile '" + csv_file_path  + csv_filename + "' into table %s \
                        fields terminated by ',' \
                        lines terminated by  '\n' ignore 1 lines"%table_name
   
    #使用数据库
    cur.execute('use %s' % database)
   
    #设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    #执行create_sql，创建表
    cur.execute(create_sql)
    #执行data_sql，导入数据
    cur.execute(data_sql)
    conn.commit()
    
if __name__ == '__main__':  
    csv_file_path ='D:/data_analysis/sklearn/file_test/'
    fileDir = 'file_test'
    i=0
    for csv_filename in os.listdir(fileDir):
        table_name=csv_filename.split(".")[0]
        load_csv(csv_file_path,table_name,csv_filename)
        i+=1
        print (f'num{i}:{csv_filename}')
    conn.close()
    cur.close()
