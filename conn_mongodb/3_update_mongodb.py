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


# 更新文档记录
# 1 先读出旧记录数据，再更新数据，然后向数据库更新记录(不推荐)。
import copy
old_user_doc = db.users.find_one({'username':'janedoe'})
# copy.copy(x)        # 这是浅拷贝，数据的第一层与原数据联动，第二 层数据不会改变。
# copy.deepcopy(x)    # 这是深拷贝，数据的所有层都不随原数据而改变。
new_user_doc = copy.deepcopy(old_user_doc)
new_user_doc['email'] = 'janedoe74@example2.com'
# 更新数据
db.users.update({'username': 'janedoe'}, new_user_doc, safe=True)


# 2 使用$set更新模式
# 直接更新email 属性
db.users.update({"username":"janedoe"},
                {"$set":{"email":"janedoe74@example2.com"}}, safe=True)
# 同时更改email和score属性，但只更改匹配记录的第一条。
db.users.update({"username":"janedoe"},
                {"$set":{"email":"janedoe74@example2.com", "score":1}}, safe=True)
# 如果我们加上"multi=True"参数，就会更改所有匹配的记录。
db.users.update({"score":0}, {"$set":{"flagged":True}}, multi=True, safe=True)
# 注意：未来pymongo可能会将默认值由"multi=False"修改为True，所以在写程 序时最好指定具体参数