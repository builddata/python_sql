# -*- coding: utf-8 -*-
"""
pymysql——数据库
mysql默认单个数据包最大为10M，如果单次加载文件过大，就会报错。进入mysql命令行，键入 查看show variables like 'max_allowed_packet';
修改set global max_allowed_packet = 100*1024*1024：100m

net start mysql
mysql -hlocalhost -uroot -p
密码sunboy
show databases;
use which database?
source C:\python\originfiles/wx0706.sql

"""

import time
import pymysql
class dbEXE():
     def __init__(self):            #连接mysql
         self.conn = pymysql.connect("118.124.174.176","root","root123","dbTest",charset="utf8")
         self.cursor = self.conn.cursor()

     def exeQuery(sql=None):  #查询操作
         self.cursor.execute(sql)       #传入sql执行动作       
         res = self.cursor.fetchall()   #取出查询结果返回给res列表
         return res

     def exeCUD(sql=None):   #删除、更新、新增操作
         self.cursor.execute(sql)      #传入sql执行动作
         self.conn.commit()            #提交事务处理
         print("执行完毕...")

     def exeClose(self):     #关闭游标和连接
         self.cursor.close()
         self.conn.close()
if __name__=='__main__':
    demo = dbEXE()                                     #实例化
    res = demo.exeQuery(sql="select * from dbTest")    #执行查询操作
    demo.exeClose()
    print(res)

#单个文件批量导入
if __name__=='__main__':
    fileDir = 'logs'
    ex01 = dbEXE()
    time1 = datetime.now()   #记录起始时间
    with open(file=fileDir + '/2010-05-07.log', mode='r') as f:
        strSQL = ''
        for line in f:
            item1 = list(line.split(","))[0]
            item2 = list(line.split(","))[1]
            item3 = list(line.split(","))[2]
            item4 = list(line.split(","))[3].split('\n')[0]
            strSQL+="('{}','{}','{}',{}),".format(item1,item2,item3,item4)
        sql=strSQL[:-1]
        sql = "insert into daily_data values"+ sql
        ex01.exeCUD(sql) 
        ex01.exeClose()        
    time2= datetime.now()   #记录结束时间
    print("加载开始时间:",time1)           #打印开始时间
    print("加载结束时间:",time2)           #打印结束时间
    
    
    
#多个文件批量导入

    number = 0  #计数
    strSQL= ''  #SQL语句初始为空
    for list1 in os.listdir(fileDir):
        with open(file=fileDir + '/' + list1, mode='r') as f:
            for line in f:
                item1 = list(line.split(","))[0] 
                item2 = list(line.split(","))[1] 
                item3 = list(line.split(","))[2]
                item4 = list(line.split(","))[3].split('\n')[0]
                strSQL += "('{}','{}','{}',{}),".format(item1, item2, item3, item4)
        number +=1   #计数增1
        if number % n ==0:   #当计数增至n步长数时
            sql = strSQL[:-1]   #截取SQL语句，把最后那个逗号去掉
            sql = "insert into goods values " +sql   #拼接为插入SQL语句
            self.exeCUD(sql)    #执行插入操作
            strSQL = ''   #执行完成后清空SQL字符串，重置为空
            print("the {} files have been loading into mysql, yeah! ...".format(number))
            time.sleep(5) #时间设置5秒进行一次
            
#loaddata            
#mysql安全设置中的参数，即原则上不允许外部文件导入，如果使用客户端，如pymsql，就需要在连接对象创建时加入这个参数：
client = pymysql.connect("192.168.58.172","root","root123","supermarket",local_infile =1)
#然后通用在命令行采用导入文件方式加载数据，格式为：加入关键词low_priority，那么MySQL将会等到没有其他人读这个表的时候，才把插入数据  
#load data infile "/logs/demo.txt" into table demo;  #从服务器上读文件
#load data local infile "/logs/demo.txt" into table demo;  #从客户机上读文件
      
load data [low_priority] [local] infile 'file_name txt' [replace | ignore] into table tbl_name
[fields terminated by't']   #指定每行中记录分隔符
[OPTIONALLY] enclosed by ''] #指定每个记录用符号包围
[escaped by'\' ]]            #指定转义字符便于区分
[lines terminated by'n']  #指定行与行之间分隔符，一般为换行
[ignore number lines]     #可以忽略的行数，如第一行如果为文本文件头，可以忽略
[(col_name, )]

#对3000多个文件采用这种方式导入
import  pymysql,os,time

client = pymysql.connect("192.168.58.172","root","root123","supermarket",local_infile =1)
cursor =client.cursor()

fileDir = 'logs'
for file in os.listdir(fileDir):
    sql= "load data local infile '" + fileDir + '/' + file + "' into table daily_income \
                        fields terminated by ',' \
                        lines terminated by '\n' "
    cursor.execute(sql)
    client.commit()    
    time.sleep(2)
client.close()



#导入pymysql方法
import pymysql


#连接数据库
config = {'host':'',
          'port':3306,
          'user':'username',
          'passwd':'password',
          'charset':'utf8mb4',
          'local_infile':1
          }
conn = pymysql.connect(**config)
cur = conn.cursor()


#load_csv函数，参数分别为csv文件路径，表名称，数据库名称
def load_csv(csv_file_path,table_name,database='evdata'):
    #打开csv文件
    file = open(csv_file_path, 'r',encoding='utf-8')
    #读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),'
    colum = colum[:-1]
    #编写sql，create_sql负责创建表，data_sql负责导入数据
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" % (csv_filename,table_name)
 
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
    #关闭连接
    conn.close()
    cur.close()


























   
            
