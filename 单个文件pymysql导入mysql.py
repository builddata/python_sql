# -*- coding: utf-8 -*-
"""
单个csv文件导入mysql
只修改列的数据类型的方法:
通常可以写成 alter table 表名 modify column 列名 新的列的类型
"""
import pymysql
import time

#连接数据库


config = {'host':'localhost','port':3306,'user':'root','passwd':'sunboy','charset':'utf8mb4',
          'local_infile':1}
conn = pymysql.connect(**config)
cur = conn.cursor()

def load_csv(csv_file_path,table_name,csv_filename,database='test1'):
    file = open(csv_file_path+csv_filename, 'r',encoding='utf-8')
    #读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
    print(b)
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),' #varchar可变长字符串
    colum = colum[:-1]
    print (colum)
    #编写sql，create_sql负责创建表，data_sql负责导入数据 
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "load data local infile '" + csv_file_path  + csv_filename + "' into table %s \
                        fields terminated by ',' \
                        lines terminated by '\n' ignore 1 lines"%table_name
   

    cur.execute('use %s' % database)
    #设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute(create_sql)
    cur.execute(data_sql)
    conn.commit()
    conn.close()
    cur.close()
    print ("已创建表%s" % table_name)
    
def drop_table(table_name,database='test1'):
    cur.execute('use  %s' % database)
    cur.execute('DROP TABLE %s' % table_name)
    conn.commit()
    conn.close()
    cur.close()
    print ("已删除表%s" % table_name)
    
if __name__ == '__main__':
    time1 = time.time()
    csv_file_path ='D:/data_analysis/sklearn/file_test/'
    csv_filename ='high_diamond_ranked_10min.csv'
    csv_filename ='testa.txt'
    table_name='testa'
    load_csv(csv_file_path,table_name,csv_filename)
    time2 = time.time()
    print (f'time:{time2-time1}')
    #drop_table(table_name)
    

    
    
    
    
    