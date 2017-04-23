# coding:utf-8
'''
文档型数据库的最大特点就是不执行键约束，但这样一来，在使用MongoDB时必 须保持警惕，在处理查询结果时，可能有些字段会没有匹配的数据。
有时候这也会 使数据库状态出现不一致，比如，有些数据被更新，而有些则没有更新
'''
# 保守写代 码以避免键错误和其它错误

# 1 字典get()方法
# get("score", 0)意思是取出数值score，如果没有数值则为零。
total_score = 0
for username in ('jill', 'sam', 'cathy'):
    user_doc = db.users.find_one({'username': username})
    total_score += user_doc.get('score', 0)

# get()在嵌入循环时也能很好的工作
for supplier in product_doc.get('suppliers', []):
    email_supplier(supplier)
# 为了避免输入数据类型的错误，强烈建议在编写的程序中进行校验数据类型。