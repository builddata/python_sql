# -*- coding: utf-8 -*-
"""
pymysql_增加删除

"""
import pymysql


class SQL_EXE():
    def __init__(self): 
              
        self.conn = pymysql.connect(host="localhost",user="root",password="sunboy",
                                    database="test1",charset="utf8")
        self.cursor = self.conn.cursor()

    def exeQuery(self,sql=None):  #查询操作
        self.cursor.execute(sql)            
        res = self.cursor.fetchall()  
        return res

    def exeCUD(self,sql=None):   #删除、更新、新增操作
    #with 语句适用于对资源进行访问的场合，确保不管使用过程中是否发生异常都会执行必要的“清理”操作，
    #释放资源，比如文件使用后自动关闭、线程中锁的自动获取和释放等
        try:
            with self.cursor as cursor:
                affected_rows = cursor.execute(sql)

            if affected_rows == 1:
                print('修改成功!!!')
            self.conn.commit()
        except pymysql.MySQLError as err:
            self.conn.rollback()
            print(type(err), err)
        finally:
            pass

    def exeClose(self):     #关闭游标和连接
        self.cursor.close()
        self.conn.close()
        
if __name__=='__main__':
    
    demo = SQL_EXE()    
    table='testa'                               
    # res = demo.exeQuery(sql=f"select * from {table} limit 2")    #执行查询操作
    # print(res) 
    # demo.exeCUD(sql=f"insert into {table}  values ('ann',20,'厦门',8000)") #插入数据
    demo.exeCUD(sql=f"UPDATE {table} SET name ='niubia' where salary>5000") #更新数据
    # demo.exeCUD(sql=f"delete from {table} where age>40")     #删除数据
    # demo.exeCUD(sql=f"drop table {table}")       #删除表
    demo.exeClose()
    #批量插入数据
     #sql='insert  userinfo(id,name,passwd) values(%s,%s,%s)'
     #params=[(2,"root","2345"),(3,"test","3456")]
     #reCount = cur.executemany(sql,params)