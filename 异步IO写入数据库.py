# -*- coding: utf-8 -*-
"""
异步IO写入数据库

"""

# pipelines.py

from settings import MY_SETTINGS
from pymysql import cursors
# twisted 网络框架
# API 接口
from twisted.enterprise import adbapi
import json
import os
import Bloomfilter
import hashlib
class SaveToMysqlAsynPipeline(object):
    # 从配置文件中读取配置
    @classmethod
    def from_settings(cls, settings):
        asyn_mysql_settings = MY_SETTINGS
        asyn_mysql_settings['cursorclass'] = cursors.DictCursor
        dbpool = adbapi.ConnectionPool("pymysql", **asyn_mysql_settings)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool
        if os.path.exists("job.state"):
            bloom = Bloomfilter("job.state")
        else:
            bloom = Bloomfilter(1000000)
        self.bloom = bloom
        query = self.dbpool.runInteraction(self.db_create)
        query.addErrback(self.db_create_err)

    def db_create(self, cursor):
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS `job` (
                    job_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    job_name text COMMENT '工作名称', 
                    job_money text COMMENT '工作薪资',
                    max_money FLOAT COMMENT '最大薪资',
                    min_money FLOAT COMMENT '最少薪资',
                    job_date text COMMENT '工作发布时间',
                    company_name text COMMENT '公司名称',
                    job_place text COMMENT '工作地点',
                    job_city text COMMENT '工作城市',
                    job_area text COMMENT '工作地区',
                    job_education text COMMENT '工作学历',
                    job_fuli text COMMENT '公司福利',
                    job_from text COMMENT '工作所属网站',
                    job_type text COMMENT '工作类型',
                    job_detail_href text COMMENT '详情地址',
                    job_state text COMMENT '工作数据的加密信息'
                )
                """)

    def db_create_err(self, failure):
        print('---------------------------', failure)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.db_insert, item)
        query.addErrback(self.handle_error, item)
        return item

    def handle_error(self, failure, item):
        print('============================', failure, item)

    def db_insert(self, cursor, item):
        job_state = json.dumps(dict(item))
        hl = hashlib.md5()
        hl.update(job_state.encode(encoding='utf-8'))
        job_state = hl.hexdigest()

        if not self.bloom.test(item['job_detail_href']):
            print("添加数据========================")
            cursor.execute("""
                   INSERT INTO job ( job_name, job_money, max_money, min_money, job_date, company_name, job_place, job_city, job_area, job_education, job_fuli, job_from, job_type, job_detail_href, job_state ) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )
                   """, (item['job_name'], item['job_money'], item['max_money'], item['min_money'], item['job_date'],
                         item['company_name'], item['job_place'], item['job_city'], item['job_area'],
                         item['job_education'], item['job_fuli'], item['job_from'], item['job_type'],
                         item['job_detail_href'], job_state))
            self.bloom.add(item['job_detail_href'])
            self.bloom.save("job.state")
        else:
            cursor.execute("""SELECT job_state from job WHERE job_detail_href=%s""", (item['job_detail_href'],))
            result = cursor.fetchone()
            if result and result['job_state'] != job_state:
                print("更新数据=========================")
                cursor.execute("""
                      UPDATE job set job_name=%s, job_money=%s, max_money=%s, min_money=%s, job_date=%s, company_name=%s, job_place=%s, job_city=%s, job_area=%s, job_education=%s, job_fuli=%s, job_from=%s, job_type=%s WHERE job_detail_href=%s
                      """, (item['job_name'], item['job_money'], item['max_money'], item['min_money'], item['job_date'],
                            item['company_name'], item['job_place'], item['job_city'], item['job_area'], item['job_education'],
                            item['job_fuli'], item['job_from'], item['job_type'], item['job_detail_href']))
            else:
                print("不用更新数据=========================")
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

if __name__ == '__main__':
    SaveToMysqlAsynPipeline()