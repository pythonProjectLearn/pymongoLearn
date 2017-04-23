# coding:utf-8
import sys
from datetime import datetime
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

# -----------删除数据
# 注意：remove()方法需要safe参数，建议设置，另外，remove()操作如果找不到匹 配文档将不会引发任何异常或错误。
db.users.remove({"score":1}, safe=True)
# 使用None，可以删除一个集合中的所有文档。
# 使用remove()方法删除文档与使用drop_collection()方法不同，使用drop后的索 引仍然保持不变。
db.users.remove(None, safe=True)