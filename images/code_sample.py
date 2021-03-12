





from pymongo_ssh import MongoSession



session = MongoSession(
    host='db.example.com',
    port='21',
    user='myuser',
    key='/home/myplace/.ssh/id_rsa',
    to_port='37017',
    to_host='0.0.0.0'
)



db = session.connection['mydb']
col = db['products']
pipeline = [
    {'$match': {'active': True}},
    {'$unwind': '$product'},
    {'$project': {
        '_id': '$_id',
        'product_sku': '$product.sku',
        'product_price': '$product.price',
        'created_date': 
            {'$dateToString': 
                 {'format': '%Y-%m-%d', 
                  'date': '$createdAt'}},
    }}
]



df = session.pd_aggregate(col, pipeline)

...
session.stop()




