# coding:utf-8
import sys
from datetime import datetime
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    conn = MongoClient(host='localhost', port=27017)
    print 'connect sucessfully'
except ConnectionFailure, e:
    # sys.stderr是系统的标准错误流
    sys.stderr.write('Could not connect to Mongodb %s' %e)
    sys.exit(1)

db = conn['test']  # 获得一个数据库指针
assert db.collection == conn

# -----------单条记录查询
# 如果查询一个数值大于0的记录可以这样写
#  { "score" : { "$gt" : 0 }}
#  $lt(<) $lte(<=) $gt(>) $gte(>=)  $ne(!=)
user_doc = db.users.find_one({"username" : "janedoe"})
# 如果find_one()没有找到记录将返回None.
if not user_doc:
    print "no document found for username janedoe"


# -----------多条记录查询
users = db.users.find({"firstname":"jane"})
# 如果仅需要查询某一项内容，比如这里只需要打印出email信息，就可以象这样加入一个条件参数，
# 这样做的好处是当查询结果集合很大时，可以节约带宽和资源。
#  users = dbh.users.find({"firstname":"jane"},{"email":1})
for user in users:
    # 这里使用了字典中的get方法来打印邮箱信息，如果确信结果记录都包含email属性，也可以使用字典访问
    #  print user['email']
    print user.get("email")


# -----------查询结果计数
# 查询在users集合中有多少有效文档
userscount = db.users.find().count()
print "There are %d documents in users collection" % userscount

# ------------查询结果排序(两种方式)
users = db.users.find({"firstname":"jane"},
                      sort=[("dateofbirth", pymongo.DESCENDING)])
users = db.users.find({ "firstname":"jane"}).sort(("dateofbirth", pymongo.DESCENDING))
for user in users:
    print user.get("email")

# -----------限制查询结果记录数量
# 如果limit(0) 即为没有限制
user = db.users.find().sort(("score", pymongo.DESCENDING)).limit(10)
for user in users:
    print user.get('username'), user.get('score', 0)


# -----------跳过一部分结果记录
# 比如应用于显示每页20个记录的第二页
users = db.users.find().sort(("surname", pymongo.ASCENDING)).limit(20).skip(20)

# ------------使用快照模式
for user in db.users.find(snapshot=True):
    print user.get('username'), user.get('score', 0)

