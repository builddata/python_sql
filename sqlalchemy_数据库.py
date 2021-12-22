# -*- coding: utf-8 -*-
"""
sqlalchemy_数据库
要阻塞在数据库返回结果的过程中。
当前端提交大量查询请求时，查询效率肯定是很低的。
"""

# pip install sqlalchemy
# pip install pymysql

import pandas as pd

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String


#先来创建一个目标表的 domain entity
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

from config.app_config import *

Base = declarative_base()

class User(Base):   # 实体
    __tablename__ = "user"

    user_id = Column(String(32), primary_key=True)
    phone_number = Column(String(11), unique=True)
    name = Column(String(64))
    nick_name = Column(String(40))
    id_card = Column(String(32))
    gender = Column(String(64))
    birthday = Column(Date(64))
    address = Column(String(255))

    created_time = Column(String(32))
    updated_time = Column(String(32))

    def __init__(self, org_id, ………… updated_time):
        self.org_id = org_id
    ……
        self.created_time = created_time
        self.updated_time = updated_time

#再来创建读写脚本

from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy import create_engine
from domain.user import UserRaw
engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s" % (db_username, db_password, db_url, db_port, db_database))
DBSession = sessionmaker(bind=engine)

if __name__ == '__main__':
    user_csv_file_path = '/xxx/xxx/xxx.csv'
    #import datatable as dt
    #data= dt.fread(csv_file_path).to_pandas() #需要全文件读取
    chunks = pd.read_csv(user_csv_file_path, chunksize=3000, sep=',', keep_default_na=False)  # 
    read_number = 0
    session = DBSession()
    for chunk in chunks:
  
        session.add_all([User(row["源用户ID"], row["手机号"], row["姓名"], row["昵称"], row["密码"],
                          row["密码加盐值"], row["微信unionID"], row["性别"], row["生日"], row["省份"],
                          row["城市"], row["区县"], row["详细地址"], row["头像"], row["爱好"],
                          row["创建时间"], row["更新时间"]) for index, row in chunk.iterrows()]) 
        # for row in chunk.itertuples()  # 没有 index 了，也没有 header 了，但是比 iterrows 快很多，我的 case 快了 50 多倍
        session.commit()   # 提交
        read_number += len(chunk)
        print("read_number: %s" % read_number) 
        session.close()


#-----------------------------------------------------------------------------------------------------------------
import datetime

from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 基础类
Base = declarative_base()

# 创建引擎
engine = create_engine(
    "mysql+pymysql://root@127.0.0.1:3306/db1?charset=utf8",
    # "mysql+pymysql://root:123@127.0.0.1:3306/db1?charset=utf8",  # 有密码时
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
    age = Column(Integer,nullable=False)
    phone = Column(String(11))
    addr = Column(String(64), nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now)  # 一定不要加括号

    __table_args__ = (
        UniqueConstraint("id", "name"),  # 创建联合唯一 可指定name给个别名
        Index("phone", "addr", unique=True),  # 创建联合唯一索引  可指定name给个别名
    )

    def __str__(self):
        return "object:<id:%s name:%s>" % (self.id, self.name)


def create_tb():
    """
    创建表
    :return:
    """
    Base.metadata.create_all(engine)


def drop_tb():
    """
    删除表
    :return:
    """
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_tb()
    create_tb()

#表创建好之后，开始链接库
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

#新增单条记录：
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)


user_obj = Users(name="user001", phone="15125352333",age=23, addr="China")
session.add(user_obj)

# 提交
session.commit()

# 关闭链接（可使用session.remove()）
session.close()

#单表 - 修改记录
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 修改名字
session.query(Users).filter_by(id=1).update({"name": "USER001"})
# 修改年龄，使用+号，默认为"fetch"，代表只允许int类型使用+号
session.query(Users).filter_by(id=1).update({"age": Users.age + 1},synchronize_session="fetch")
# 修改地址,使用+号，由于是字符类型，所以要修改synchronize_session=False
session.query(Users).filter_by(id=1).update({"addr":Users.addr + "BeiJing"},synchronize_session=False)

# 提交
session.commit()

# 关闭链接
session.close()

#单表 - 删除记录
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

session.query(Users).filter_by(id=2).delete()

# 提交
session.commit()

# 关闭链接
session.close()

#单表 - 批量增加
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 批量增加
session.add_all([
    Users(name="user002",age=21,phone="13269867233",addr="ShangHai"),
    Users(name="user003",age=18,phone="13269867234",addr="GuangZhou"),
    Users(name="user003",age=24,phone="13269867235",addr="ChongQing"),
])

# 提交
session.commit()

# 关闭链接
session.close()

#单表查询 - 基本查询
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 查询
# -- 查所有 --
result_01 = session.query(Users).all()
# -- 过滤 --
result_02 = session.query(Users).filter(Users.name == "USER001").all()  # Python表达式的形式过滤
result_03 = session.query(Users).filter_by(name="user002").all()  # ORM形式过滤
result_04 = session.query(Users).filter_by(name="user003").first()  # ORM形式过滤 取第一个

print(result_01) # [<models.Users>,<models.Users>,<models.Users>]
print(result_02)
print(result_03)
print(result_04) # object:<id:3 name:user003>  通过__str__拿到结果

# 提交
session.commit()

# 关闭链接
session.close()

#条件查询
# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 只拿某字段
result_00 = session.query(Users.name,Users.age).first()
print(result_00)

# and(用逗号或者用and_)
result_01 = session.query(Users).filter( Users.id > 1,Users.age < 23).all()
print(result_01)

from sqlalchemy import and_
result_02 = session.query(Users).filter(and_( Users.id > 1,Users.age < 23)).all()
print(result_02)

# or
from sqlalchemy import  or_
result_03 = session.query(Users).filter(or_(Users.id > 3,Users.age < 23)).all()
print(result_03)

# and与or的组合使用
result_04 = session.query(Users).filter(or_(
    Users.id > 1,
    and_(Users.id > 2, Users.age < 24)
)).all()
print(result_04)

# 范围
result_05 = session.query(Users).filter(Users.age.between(18,24)).all()
print(result_05)

# 包含
result_06 = session.query(Users).filter(Users.age.in_([18,21,24])).all()
print(result_06)

# 取反 ~
result_07 = session.query(Users).filter(~Users.age.in_([18,21,24])).all()
print(result_07)

# 通配符
result_08 = session.query(Users).filter(Users.name.like("us%")).all()
print(result_08)

# 分页
result_09 = session.query(Users).all()[0:1]
print(result_09)

# 排序
result_10 = session.query(Users).order_by(Users.id.desc()).all()  # 倒序
print(result_10)

result_11 = session.query(Users).order_by(Users.id.asc()).all()  # 正序
print(result_11)

# 分组
result_12 = session.query(Users).group_by(Users.id).all()
print(result_12)


# 聚合函数
from sqlalchemy.sql import func
result_13 = session.query(
    func.max(Users.age),
    func.sum(Users.age),
    func.min(Users.age),
).group_by(Users.name).having(func.max(Users.age > 12)).all()
print(result_13)

# 提交
session.commit()

# 关闭链接
session.close()

#多表相关 - 一对多   ----------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 基础类
Base = declarative_base()

# 创建引擎
engine = create_engine(
    "mysql+pymysql://root@127.0.0.1:3306/db1?charset=utf8",
    # "mysql+pymysql://root:123@127.0.0.1:3306/db1?charset=utf8",  # 有密码时
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    # 真实约束字段：避免脏数据写入，在物理表中会创建真实字段关系
    # 可选级联操作：CASCADE，DELETE、RESTRICT
    fk_class = Column(Integer, ForeignKey("classes.id",ondelete="CASCADE",onupdate="CASCADE"))
    # 逻辑关系字段：不会在真实物理表中创建字段，但是可以通过该逻辑字段进行增删改查
    # backref:反向查询的名字
    re_class = relationship("Classes",backref="students")

def create_tb():
    """
    创建表
    :return:
    """
    Base.metadata.create_all(engine)


def drop_tb():
    """
    删除表
    :return:
    """
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_tb()
    create_tb()

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)


session.add_all(
    [
        Students(name="学生01", re_class=Classes(name="一年级一班")),  # 自动填入fk_class
        Students(name="学生02", re_class=Classes(name="一年级二班")),
    ]
)

# 提交
session.commit()

# 关闭链接
session.close()
#----------------------------------------------------------------------------------------
#.多对多 使用relationship时，传入指定手动生成的第三张表，代表这是多对多关系

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# 基础类
Base = declarative_base()

# 创建引擎
engine = create_engine(
    "mysql+pymysql://root@127.0.0.1:3306/db1?charset=utf8",
    # "mysql+pymysql://root:123@127.0.0.1:3306/db1?charset=utf8",  # 有密码时
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    # 可选级联操作：CASCADE，DELETE、RESTRICT
    fk_class = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE", onupdate="CASCADE"))
    # 逻辑关系字段：不会在真实物理表中创建字段，但是可以通过该逻辑字段进行增删改查
    # backref:反向查询的名字
    re_class = relationship("Classes", backref="students")


class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    # 逻辑字段M2M:指定第三张表，secondary参数为__tablename__，反向查询为teachers
    re_class = relationship("Classes", secondary="teachersm2mclasses", backref="teachers")


class TeachersM2mClasses(Base):
    __tablename__ = "teachersm2mclasses"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))

    __table_args__ = (
        UniqueConstraint("teacher_id", "class_id"),  # 创建联合唯一 可指定name给个别名
    )


def create_tb():
    """
    创建表
    :return:
    """
    Base.metadata.create_all(engine)


def drop_tb():
    """
    删除表
    :return:
    """
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_tb()
    create_tb()
    
    
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

session.add_all(
    [
        Teachers(name="老师01",re_class=[ 
            session.query(Classes).filter_by(id=1).first()
        ]),
        Teachers(name="老师02",re_class=[
            session.query(Classes).filter_by(id=1).first()
        ]),
        Teachers(name="老师03",re_class=[
            session.query(Classes).filter_by(id=2).first()
        ]),
    ]
)

# 提交
session.commit()

# 关闭链接
session.close()


#组合查询
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 必须用filter，获取全部也是，不可以使用all因为他会返回一个list，list不具备union_all
# 使用filter返回的对象是：<class 'sqlalchemy.orm.query.Query'>
# 并且query中必须单拿某一个字段，如果不指定字段就直接返回对象

s = session.query(Students.name).filter()
t = session.query(Teachers.name).filter()
c = session.query(Classes.name).filter()
ret = s.union_all(t).union_all(c).all()  # 用列表显示
print(ret)
# [('学生01',), ('学生02',), ('老师01',), ('老师02',), ('老师03',), ('一年级一班',), ('一年级二班',)]

# 提交
session.commit()

# 关闭链接
session.close()

#使用join进行连表查询：
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

# 手动指定条件查询
result = session.query(Students.name, Classes.name).filter(Students.id == Classes.id).all()
for i in result:
    print(i)

# 连接查询,同上，内部自动指定 Students.fk_class == Classes.id 的条件
result = session.query(Students.name, Classes.name).join(Classes).all()
# 相当于：result = session.query(Students.name,Classes.name).join(Classes, Students.fk_class == Classes.id).all()
for i in result:
    print(i)

# 左链接查询,即使有同学没有班级也拿出来
result = session.query(Students.name, Classes.name).join(Classes, isouter=True).all()
for i in result:
    print(i)

# 如果想查看有哪些班级没有同学，就换一个位置
result = session.query(Students.name, Classes.name).join(Students, isouter=True).all()
for i in result:
    print(i)

# 三表查询,需要自己指定条件
result = session.query(Teachers.name, Classes.name, TeachersM2mClasses.id) \
    .join(Teachers, TeachersM2mClasses.teacher_id == Teachers.id) \
    .join(Classes, TeachersM2mClasses.class_id == Classes.id) \
    .filter()  # 查看原生语句
print(result)
for i in result:
    print(i)

# 提交
session.commit()

# 关闭链接
session.close()

#-----执行原生SQL：----------------------------------------------------------------------------------

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# 导入引擎，模型表等
from models import *

# 通过Session绑定引擎和数据库建立关系
Session = sessionmaker(bind=engine)
# 创建链接池，使用session即可为当前线程拿出一个链接对象。内部采用threading.local进行隔离
session = scoped_session(Session)

cursor = session.execute(r"select * from students where id <= (:num)",params={"num":2})
print(cursor.fetchall())

# 提交
session.commit()

# 关闭链接
session.close()











