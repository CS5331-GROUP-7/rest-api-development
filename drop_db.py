
from flask_mongoengine import MongoEngine
from mongoengine import connect
db = connect('db_test',host='mongodb')
db.drop_database('db_test')
db.close()
