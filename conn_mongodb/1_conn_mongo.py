# coding:utf-8

import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


try:
    client = MongoClient(host='localhost', port=27017)
    print 'connect sucessfully'
except ConnectionFailure, e:
    # sys.stderr是系统的标准错误流
    sys.stderr.write('Could not connect to Mongodb %s' %e)
    sys.exit(1)

db = client['test']  # 获得一个数据库指针

users = db.users
# 插入一条数据
user_doc = {
    'username': 'janedoe',
    'firstname': 'Jane',
    'surname': 'Doe',
    'dateofbirth': datetime(1974, 4, 12),
    'email': 'janedoe74@example.com',
    'score': 0
}
user = users.insert_one(user_doc)
# 查看插入的id
user_id = user.inserted_id
# 查找数据
user.find_one()
user.find_one({"author": "Mike"})
# 通过id查找
user.find_one({"_id": user_id})

# 不要转化ObjectId的类型为String：
# 否则查找不到数据
user_id_as_str = str(user_id)
users.find_one({"_id": user_id_as_str})
# 如果你有一个post_id字符串，怎么办呢？
from bson.objectid import ObjectId
def get(user_id_as_str):
  # 将string转化成ObjectId:
  document = user.find_one({'_id': ObjectId(user_id_as_str)})



# 如果多条数据一起插入，使用usee_doc=[{}, {}, {}]





#  dbh数据库的users集合不需事先创建，在插入数据时会自动建立。

print "Successfully inserted document: %s" % user_doc
# dbh.users.insert(user_doc, w=2)
# w = 2    表示写操作将不会成功，直到它已被写入到至少2台服务器的
# 一个副本集。 注意：如果参数只使用w，而没有任何赋值，则意味着进入写模式，与使用
# safe = True功能相同。


