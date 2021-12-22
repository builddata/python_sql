# -*- coding: utf-8 -*-
"""
sql_导出excel
"""

import openpyxl
import pymysql

workbook = openpyxl.Workbook()
sheet = workbook.active
# 修改工作表的标题
sheet.title = '员工基本信息'
# 给工作表添加表头
sheet.append(( '姓名', '年龄', '城市', '月薪'))

conn = pymysql.connect(host='localhost', port=3306,
                       user='root', password='sunboy',
                       database='test1', charset='utf8mb4')
try:
    with conn.cursor() as cursor:
        cursor.execute(
            'select name, age, city, salary from testa'
        )

        row = cursor.fetchone()
        while row:
            sheet.append(row)
            row = cursor.fetchone()

    workbook.save('hrs.xlsx')
    
except pymysql.MySQLError as err:
    print(err)
    
finally:
    conn.close()
