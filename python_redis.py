# -*- coding: utf-8 -*-
"""
python_redis

.\redis-server.exe redis.windows.conf  #启动redis
.\redis-cli.exe -h 127.0.0.1 -p 6379   #打开另外一个cmd，测试使用
"""
#https://www.runoob.com/w3cnote/python-redis-intro.html
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  
r.set('name', 'runoob')  # 设置 name 对应的值
print(r.get('name'))  # 取出键 name 对应的值

#1.ex - 过期时间（秒） 这里过期时间是3秒，3秒后p，键food的值就变成None
r.set('food', 'mutton', ex=3)    # key是"food" value是"mutton" 将键值对存入redis缓存
print(r.get('food'))  # mutton 取出键food对应的值

#2.px - 过期时间（豪秒） 这里过期时间是3豪秒，3毫秒后，键foo的值就变成None
r.set('food', 'beef', px=3)
print(r.get('food'))

#3.nx - 如果设置为True，则只有name不存在时，当前set操作才执行 （新建）
print(r.set('fruit', 'watermelon', nx=True))    # True--不存在
# 如果键fruit不存在，那么输出是True；如果键fruit已经存在，输出是None

#4.xx - 如果设置为True，则只有name存在时，当前set操作才执行 （修改）
print((r.set('fruit', 'watermelon', xx=True)))   # True--已经存在
# 如果键fruit已经存在，那么输出是True；如果键fruit不存在，输出是None

#5.setnx(name, value)
#设置值，只有name不存在时，执行设置操作（添加）
print(r.setnx('fruit1', 'banana'))  # fruit1不存在，输出为True

#6.setex(name, time, value) #time - 过期时间（数字秒 或 timedelta对象）

import time
r.setex("fruit2", 5, "orange")
time.sleep(5)
print(r.get('fruit2'))  # 5秒后，取值就从orange变成None

#7.psetex(name, time_ms, value) time_ms - 过期时间（数字毫秒 或 timedelta对象）
r.psetex("fruit3", 5000, "apple")
time.sleep(5)
print(r.get('fruit3'))  # 5000毫秒后，取值就从apple变成None

#8.mset(*args, **kwargs) 批量设置值
r.mget({'k1': 'v1', 'k2': 'v2'})
r.mset(k1="v1", k2="v2") # 这里k1 和k2 不能带引号，一次设置多个键值对
print(r.mget("k1", "k2"))   # 一次取出多个键对应的值
print(r.mget("k1"))

#9.mget(keys, *args) 批量获取
print(r.mget('k1', 'k2'))
print(r.mget(['k1', 'k2']))
print(r.mget("fruit", "fruit1", "fruit2", "k1", "k2"))  # 将目前redis缓存中的键对应的值批量取出来

#10.getset(name, value) 设置新值并获取原来的值
print(r.getset("food", "barbecue"))  # 设置的新值是barbecue 设置前的值是beef

#1.getrange(key, start, end)获取子序列（根据字节获取，非字符）
r.set("cn_name", "君惜大大") # 汉字
print(r.getrange("cn_name", 0, 2))   # 取索引号是0-2 前3位的字节 君 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("cn_name", 0, -1))  # 取所有的字节 君惜大大 切片操作
r.set("en_name","junxi") # 字母
print(r.getrange("en_name", 0, 2))  # 取索引号是0-2 前3位的字节 jun 切片操作 （一个汉字3个字节 1个字母一个字节 每个字节8bit）
print(r.getrange("en_name", 0, -1)) # 取所有的字节 junxi 切片操作

#12.setrange(name, offset, value) 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
#参数：offset - 字符串的索引，字节（一个汉字三个字节）
r.setrange("en_name", 1, "ccc")
print(r.get("en_name"))    # jccci 原始值是junxi 从索引号是1开始替换成ccc 变成 jccci

































