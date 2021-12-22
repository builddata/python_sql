# -*- coding: utf-8 -*-
"""
sqlalchemy_单个大文件_数据库
No module named 'mysql'：pip install mysql-connector-python-rf 
只修改列的数据类型的方法:
通常可以写成 alter table 表名 modify column 列名 新的列的类型
"""
import pandas as pd

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
# from config.app_config import *


Base = declarative_base()
class User(Base):   # 实体
    __tablename__ = "big"
    id = Column(Integer, primary_key=True)
   
    total_shares = Column(String(64))#, unique=True
    free_float_shares = Column(String(64))

    

    def __init__(self, total_shares,free_float_shares):

        # self.code = code
        self.total_shares = total_shares
        self.free_float_shares = free_float_shares
    
        
def create_tb():
    """
    创建表
    :return:
    """
    Base.metadata.create_all(engine)


#再来创建读写脚本

from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine
import time

engine = create_engine('mysql+mysqlconnector://root:sunboy@localhost:3306/test1?auth_plugin=mysql_native_password')

DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    time1 = time.time()
    create_tb()
    user_csv_file_path = 'D:/data_analysis/sklearn/file_test/bigfile.csv'
    #import datatable as dt
    #data= dt.fread(csv_file_path).to_pandas() #需要全文件读取  
    chunks = pd.read_csv(user_csv_file_path, chunksize=6000, sep=',', keep_default_na=False)
    
    read_number = 0
    session = DBSession()
    for chunk in chunks:
  
        session.add_all([User( float(row["total_shares"]), float(row["free_float_shares"])) for index, row in chunk.iterrows()]) 
        # for row in chunk.itertuples()  # 没有 index 了，也没有 header 了，但是比 iterrows 快很多，我的 case 快了 50 多倍
        session.commit()   # 提交
        read_number += len(chunk)
        print("read_number: %s" % read_number) 
        session.close()

    time2= time.time()
    print (f'time:{time2-time1}')