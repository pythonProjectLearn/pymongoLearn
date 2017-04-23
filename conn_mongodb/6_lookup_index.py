# coding:utf-8
import sys
from datetime import datetime
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
'''
使用索引快速查找
'''

try:
    conn = MongoClient(host='localhost', port=27017)
    print 'connect sucessfully'
except ConnectionFailure, e:
    # sys.stderr是系统的标准错误流
    sys.stderr.write('Could not connect to Mongodb %s' %e)
    sys.exit(1)

db = conn['test']  # 获得一个数据库指针
assert db.collection == conn


# 复合索引的方向应该相同。

# 1 创建一个单一索引：create_index()
db.users.create_index('username')

# 2 创建一个复合索引
db.users.create_index([
    ('first_name', pymongo.ASCENDING),
    ('last_name', pymongo.ASCENDING)
])

# 给复合索引指定一个名称。
db.users.create_index([("first_name", pymongo.ASCENDING),
                        ("last_name", pymongo.ASCENDING)],
                      name="name_idx")

# 3 指定在后台建立索引: background=True
# 对于数据量大的数据库，建立索引会很耗时，所以为了不影响操作，可以指定 在后台建立索引
db.users.create_index("username", background=True)

# 4 建立唯一性约束的索引：unique=True
db.users.create_index("username", unique=True)

# 使用'drop_dups=True'或者'dropDups=True'参数可以在创建唯一性索引时将除第一条匹配记录外的其他重复数据清除。
# 如不指定该选项，当索引遇到重复项时将 返回一个错误。
db.users.create_index("username", unique=True, drop_dups=True)
# 等价于被写入
db.users.create_index("username", unique=True, dropDups=True)

# 5 删除索引: drop_index()
# 将username字段创建为索引, 索引名称叫username_idx
db.users.create_index("username", name="username_idx")
# 删除刚刚创建的索引
db.users.drop_index("username_idx")

db.users.create_index([
    ("first_name", pymongo.ASCENDING),
    ("last_name",pymongo.ASCENDING)])
# Delete this index
db.users.drop_index([("first_name", pymongo.ASCENDING),
                     ("last_name",pymongo.ASCENDING)])

# 如果要删除所有索引可以使用 Collection.drop_indexes() 方法。
# 如果要查询所有索引，可以使用 Collection.index_information() 方法。
# 这将返 回一个字典，每个key是索引的名称，与key关联的值是另外一个字典。第
# 二级字典总是包含一个特殊的key叫做'key'，它包含了在创建索引时的'原索 引'。
# '原索引'就是在创建索引用 create_index() 方法时输入的语句。
# 第二级索 引也可以包含条件选项，比如唯一性约束等。