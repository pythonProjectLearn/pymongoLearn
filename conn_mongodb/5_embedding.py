# coding:utf-8
"""
面向文档：嵌入

什么是嵌入
# 当在字典中的一个值是另一个字典时，我们说后者嵌入了前者。在这里，
即'data '嵌入了'my_document'.
my_document = {"name":"foo document",
               "data":{"name":"bar document"}
                }

"""
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

'''
1 嵌入子文档的查询
user_doc = { "username":"foouser",
             "twitter":{"username":"footwitter", "password":"secret", "email":"twitter@example.com" },
             "facebook":{"username":"foofacebook", "password":"secret", "email":"facebook@example.com" },
             "irc":{ "username":"fooirc", "password":"secret", }}
'''
user_doc = db.users.find_one({"facebook.username":"foofacebook"})

'''
2 嵌入子文档的更新
'''
db.users.update({'facebook.username': 'facebook'},
                {'$set': {'facebook.username': 'bar'}},
                safe=True)

'''
3 嵌入子文档的插入
# 一个使用嵌入数组(emails)来表示一对多关系的文档。
'''
user_doc = {"username":"foouser",
             "emails":[
                {"email":"foouser1@example.com", "primary":True},
                {"email":"foouser2@example2.com", "primary":False},
                 {"email":"foouser3@example3.com", "primary":False}
             ]
            }
db.users.insert(user_doc, safe=True)
user_doc_result = db.users.find_one({"emails.email":"foouser1@exam ple.com"})
assert user_doc == user_doc_result

# 使用$push模式自动追加数据到子文档(列表)的尾部。
new_email = {"email":"fooemail4@exmaple4.com", "primary":False}
db.users.update({"username":"foouser"},
                {"$push":{"emails":new_email}},
                safe=True)

'''
4 嵌入子文档的更新($pull模式)
'''
# 这是使用$set模式进行更新的示例(**不推荐**)
db.users.insert(user_doc, safe=True)
user_doc_result = db.users.find_one({"username":"foouser"})
del user_doc_result["emails"][1]
db.users.update({"username":"foouser"},
                {"$set":{"emails":user_doc_result}},
                safe=True)

# 使用$pull模式进行更新，更简洁高效(**推荐**)。
# 其实就是删除子文档中的一条记录。
db.users.insert(user_doc, safe=True)
db.users.update({"username":"foouser"},
                {"$pull":{"emails":{"email":"foouser2@example2.com"}}},
                safe=True)

# 使用$pull模式更新多个文档。
db.users.update({"username":"foouser"},
                {"$pull": {"emails": {"primary": {"$ne": True}}}},
                 safe=True)
# 注意：$pull不仅可用于嵌入子文档，在基本文档中也可以使用。
# 使用'$'符号进行子文档中数据的原位置修改。
db.users.update({"emails.email": "foouser2@example2.com"},
                {"$set": {"emails.$.primary": True}},
                safe=True)
# Now make the "foouser1@example.com" email address not primary
db.users.update({"emails.email": "foouser1@example.com"},
                {"$set": {"emails.$.primary": False}},
                safe=True)

# 在使用Python执行数据操作时，要注意的是最好控制数据结构的大小。
# 虽然Mon goDB对单文件大小的限制越来越宽松（在1.4和1.6版中最大文件大小是4M，在1. 8版本中增加到16M，可以预见，这个限制可能还会增加）。















