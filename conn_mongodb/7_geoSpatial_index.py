# coding:utf-8
'''
MongoDB主要使用 $near 和 $within 来操作地理空间索引
$near 可以通过给定的点集合进行排序文档； $within 允许你查询一个特殊的区域，
支持的区域定义包含：$box 指定一个矩形区域，$circle 指定一个圆形区域，
在 MongoDB1.9以后还支持使用 $polygon 来指定一个凸凹多边形边界。

在进行这些地理位置查询以前，你必须先建立一个地理空间索引。
地理空间索引有 一个限制，就是一个文档在同一时间只能建立一个有效的地理空间索引。

地理空间索引默认只接收那些GPS内的位置信息，也就是说，坐标范围必须在-180..+180之间，
否则MongoDB将返回一个错误。如果你希望索引数值在GPS范 围之外，你可以在创建地理空间索引时指定。
文档的位置属性必须是一个数组或者子文档，而且最前面的两项必须是 x 和 y ，它们的顺序不重要，
只要在程序中保持一致即可。
'''
import pymongo
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
user_doc = {
    'username': 'foouser',
    'user_location': [x, y]
}

# 基于地理位置的应用，地理空间索引
import bson
loc = bson.SON()
loc['y'] = y
loc['x'] = x
user_doc = {
    'username': 'foouser',
    'user_location': loc
}

# 注意：在Python中字典类型是dict，不保存位置信息，当用Python向子文档中
# 访问位置信息时，要使用bson.SON来代替，bson.SON来自PyMongo模块，使用方法与 dict相同。

# 1 创建地理空间索引: pymongo.GEO2D
# 创建单一地理空间索引
db.users.create_index(['user_location', pymongo.GEO2D])

# 结合一般索引，创建复合索引
db.users.create_index([('user_location', pymongo.GEO2D), ('username', pymongo.ASCENDING)])



# 2 使用 $near 查询地理位置信息
'''
使用$near默认返回的结果是100个记录，有时这会花费一些时间，一般来说，5 度左右的最大距离应该足够了。
由于我们是用的十进制，坐标单位使用度，一度大约69英里。 # 如果您只关心一个相对较小的结果集（例如，在最近的10个咖啡馆），
限制查询 到10个结果，也有助于性能。让我们用一个例子来寻找最近的10个用户，40,40 限制最大距离5度。
'''
nearest_users = db.users.find(
    {'user_location': {'$near': [40, 40], '$maxDistance': 5}}
).limit(10)
for user in nearest_users:
    print 'User %s is at location %s, %s' %(user['username'], user['user_location'][0], user['user_location'][1])


# 3 使用$within 操作地理位置信息
# 首先要指定一个左下角和右上角的矩形坐标。
box = [[50.73083, -83.99756], [50.741404,  -83.988135]]
# 查询在box区域的地理位置信息
users_in_boundary = db.users.find({"user_location": {"$within": {" $box": box}}})
# 查询在圆形区域内的地理位置信息。中心在 40,40 ，半径为5度。
users_in_circle = db.users.find({
    "user_location":{
        "$within":{
            "$center":[40, 40, 5]
        }
    }
}).limit(10)


# 4 球体模型：$nearSpheres
earth_radius_km = 6371.0
max_distance_km = 5.0
max_distance_radians = max_distance_km / earth_radius_km
nearest_users = db.user.find(
    {'user_location':
         {'$nearSphere': [40, 40],
          '$maxDistance': max_distance_radians}}
).limit(10)

for user in nearest_users:
    print 'User %s is at location %s, %s' %(user['username'],
                                            user['user_location'][0],
                                            user['user_location'][1])
