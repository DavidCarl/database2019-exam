import pymongo
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint
import filemanager


mongodb_config = filemanager.load_file('configs/mysql.json')

client = MongoClient(mongodb_config['ip'], mongodb_config['port'])
# db = client.tweet
# training = db.training
