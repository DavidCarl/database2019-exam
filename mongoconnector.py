import pymongo
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint


client = MongoClient()
db = client.tweet
training = db.training
