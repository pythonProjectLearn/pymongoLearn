# coding:utf-8
# Upserts使用方法

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
可以使用Upserts的方法有三种：
1. Collection.save() save()与insert()的用法非常相似，不同之处在于save()可以同时执行更新插 入，但在同一个命令中不能插入多个文档或记录。
另外，save()只能应用于'_id'的存在检测，对于其它字段则不适用。
2. Collection.update() update()可以检测其它字段的是否存在。如果存在则执行更新操作，如果不存 在则执行插入操作。
3. Collection.find_and_modify()
'''
def edit_or_add_session(description, session_id):
    # 当要更新一条记录时，传统的做法是先查询，如果存在则更新，如果不存在则插入相关数据。(**不推荐**)
    session_doc = db.sessions.find_one({"session_id": session_id})
    if session_doc:
        db.sessions.update({"session_id": session_id},
                            {"$set": {"session_description": description}}, safe=True)
    else:
        db.sessions.insert({"session_description": description,  "session_id": session_id}, safe=True)

# 使用upsert=True参数后，一切都简单了。也避免了一次读操作。
#  upsert=True意思是'更新插入混合操作'。如果不存在则插入，如果存在则更新。
def edit_or_add_session(description, session_id):
    db.sessions.update({'session_id': session_id},
                       {'$set': {'session_description': description}},
                       safe=True, upsert=True)


# ------------读写和修改模式
#c 先对查询的记录进行更新操作，然后返回改变后的新值。
# $inc 是自动增量操作；$dec 是自动减量操作。
ret = db.users.find_and_modify({'username':username},
                               {'$inc': {'account_balance': 20}},
                               safe=True, new=True)

# 快速计数模式
# 在一个子文档中存储一个每周的计分记录。
user_doc = {
    'scores_weekly':{
        '2011-01': 10,
        '2011-02': 3,
        '2011-06': 20
    }
}

# 先写出当前时间，当前年度，当前星期的代码。
import datetime
now = datetime.datetime.utcnow()
current_year = now.year
current_week = now.isocalendar()[1]
# get()的第二个参数为0，表示查询到的记录如果没有赋值则计算为零
user_doc["scores_weekly"].get("%d-%d" %(current_year, current_week), 0)

# 我们同样可以使用自动增量或减量来操作子文档的数据($inc 和 $dec)
username = "foouser"
now = datetime.datetime.utcnow()
current_year = now.year
current_week = now.isocalendar()[1]
# Use atomic update modifier to increment by 24
db.users.update({"username":username},
                {"$inc":{"scores_weekly.%s-%s" %(current_year, current_week):24}},
                safe=True)


# 如果我们需跟踪多个周期的数值，可以同样操作。
username = "foouser"
now = datetime.datetime.utcnow()
current_year = now.year
current_month = now.month
current_week = now.isocalendar()[1]
current_day = now.timetuple().tm_yday
db.users.update({"username":username},
                {"$inc": {"scores_weekly.%s-%s" %(current_year, current_week): 24,
                          "scores_daily.%s-%s" %(current_year, current_day): 24,
                          "scores_monthly.%s-%s" %(current_year, current_month): 24, }},
                safe=True)